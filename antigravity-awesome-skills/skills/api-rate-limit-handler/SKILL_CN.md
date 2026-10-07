---
name: api-rate-limit-handler
description: "为 429 和临时性 5xx 响应实现有边界、支持幂等性的 API 限流、退避和重试处理。"
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
author: Prajeeth-12
tags: [rate-limiting, retry, backoff, api, resilience, throttle, 429]
tools: [claude, cursor, codex, gemini]
license: "MIT"
---

# API 速率限制处理器

## 概述

一个用于在与外部 API 集成时实现生产级速率限制、指数退避和重试策略的技能。防止级联故障、遵守上游配额，并在负载下保持应用程序的韧性。

## 何时使用本技能

- 当调用强制实施速率限制的外部 API 时使用(OpenAI、Stripe、GitHub 等)
- 当收到 429 Too Many Requests 或 5xx 错误、需要优雅恢复时使用
- 当构建必须遵守 `Retry-After` 头的客户端时使用
- 当设计一个需要分发请求到多个 API 提供方的系统时使用
- 当用户说"处理速率限制"、"添加重试逻辑"、"退避策略"或"不要被限流"时使用

## 工作原理

### 第 1 步：对响应进行分类

判断失败的请求是可重试的还是终态错误。

| 状态码 | 分类 | 操作 |
|--------|---------------|--------|
| 200-299 | 成功 | 返回响应 |
| 400、401、403、404 | 终态客户端错误 | 不要重试——修复请求 |
| 408、429 | 可重试(速率限制 / 超时) | 带退避重试 |
| 500、502、503、504 | 可重试(服务器错误) | 带退避重试 |

### 第 2 步：解析速率限制相关的头

在自行计算延迟之前，始终先检查上游给出的提示。

```typescript
function getRetryDelay(
  response: Response,
  attempt: number,
  maxDelayMs = 60_000
): number {
  // 优先采用上游提示
  const retryAfter = response.headers.get("Retry-After");
  if (retryAfter) {
    const seconds = Number(retryAfter);
    if (Number.isFinite(seconds) && seconds >= 0) {
      return Math.min(seconds * 1000, maxDelayMs);
    }
    // HTTP 日期格式
    const date = new Date(retryAfter).getTime();
    if (Number.isFinite(date)) {
      return Math.min(Math.max(0, date - Date.now()), maxDelayMs);
    }
  }

  // GitHub 将 x-ratelimit-reset 记录为 Unix 纪元秒数。
  const githubReset = Number(response.headers.get("x-ratelimit-reset"));
  if (Number.isFinite(githubReset)) {
    return Math.min(
      Math.max(0, githubReset * 1000 - Date.now()),
      maxDelayMs
    );
  }

  // 兜底方案：带有封顶和全抖动的指数退避。
  const cap = Math.min(1000 * 2 ** attempt, maxDelayMs);
  return Math.floor(Math.random() * cap);
}
```

不同提供方特定的重置请求头不共享统一的单位或格式。例如，
某些 API 返回的是持续时间，而 GitHub 返回的是纪元秒数。只有在查阅
该提供方当前文档之后，才能解析额外的头字段。

### 第 3 步：实现重试循环

```typescript
async function fetchWithRetry(
  url: string,
  options: RequestInit,
  maxRetries = 3,
  maxElapsedMs = 120_000,
  retryNonIdempotent = false
): Promise<Response> {
  const startedAt = Date.now();
  const method = (options.method ?? "GET").toUpperCase();
  const replaySafe = ["GET", "HEAD", "OPTIONS", "PUT", "DELETE"].includes(method)
    || retryNonIdempotent;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const response = await fetch(url, options);

    if (response.ok) return response;

    // 终态错误——不要重试
    if ([400, 401, 403, 404, 422].includes(response.status)) {
      throw new Error(`Terminal error ${response.status}: ${response.statusText}`);
    }

    if (!replaySafe) {
      throw new Error(
        `${method} was not retried because replay safety was not explicitly established`
      );
    }

    // 可重试——但已耗尽尝试次数
    if (attempt === maxRetries) {
      throw new Error(`Failed after ${maxRetries} retries: ${response.status}`);
    }

    const remaining = maxElapsedMs - (Date.now() - startedAt);
    const delay = Math.min(getRetryDelay(response, attempt), remaining);
    if (delay <= 0) {
      throw new Error(`Retry deadline exceeded after ${maxElapsedMs}ms`);
    }

    // 若不需要响应体，在等待前先释放连接。
    await response.body?.cancel();
    console.warn(
      `Request failed (${response.status}), retrying in ${Math.round(delay)}ms (attempt ${attempt + 1}/${maxRetries})`
    );
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  throw new Error("Unreachable");
}
```

### 第 4 步：添加客户端侧速率限制器(主动式)

使用令牌桶或滑动窗口机制，从源头上防止触及上游限制。

```typescript
class TokenBucket {
  private tokens: number;
  private lastRefill: number;
  private queue: Promise<void> = Promise.resolve();

  constructor(
    private maxTokens: number,
    private refillRate: number // 每秒的令牌数
  ) {
    this.tokens = maxTokens;
    this.lastRefill = Date.now();
  }

  async acquire(): Promise<void> {
    const ticket = this.queue.then(() => this.acquireOnce());
    this.queue = ticket.catch(() => undefined);
    return ticket;
  }

  private async acquireOnce(): Promise<void> {
    this.refill();
    if (this.tokens < 1) {
      const waitMs = ((1 - this.tokens) / this.refillRate) * 1000;
      await new Promise(resolve => setTimeout(resolve, waitMs));
      this.refill();
    }
    this.tokens -= 1;
  }

  private refill(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(this.maxTokens, this.tokens + elapsed * this.refillRate);
    this.lastRefill = now;
  }
}

// 用法：限制为每分钟 60 次请求
const limiter = new TokenBucket(60, 1);

async function rateLimitedFetch(url: string, options: RequestInit) {
  await limiter.acquire();
  return fetchWithRetry(url, options);
}
```

## 示例

### 示例 1：带重试的幂等 API 读取操作

```typescript
const response = await fetchWithRetry(
  "https://api.github.com/repos/OWNER/REPO",
  {
    method: "GET",
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${githubToken}`,
    },
  },
  3
);
```

对于 POST 或其他有副作用的操作，除非提供方文档说明了幂等性
机制，并且每次尝试都复用同一个稳定的幂等性键，否则应保持
`retryNonIdempotent` 为 false。

### 示例 2：Python 实现

```python
import time
import random
import httpx

def fetch_with_retry(url: str, max_retries: int = 3, **kwargs) -> httpx.Response:
    for attempt in range(max_retries + 1):
        response = httpx.request("GET", url, **kwargs)

        if response.is_success:
            return response

        if response.status_code in (400, 401, 403, 404, 422):
            response.raise_for_status()

        if attempt == max_retries:
            response.raise_for_status()

        # 解析 Retry-After 或计算退避时间
        retry_after = response.headers.get("retry-after")
        if retry_after and retry_after.isdigit():
            delay = int(retry_after)
        else:
            delay = min(2 ** attempt + random.uniform(0, 1), 60)

        print(f"Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})")
        time.sleep(delay)

    raise RuntimeError("Unreachable")
```

## 最佳实践

- ✅ 始终遵守 `Retry-After` 头——它来自了解自身限制的提供方
- ✅ 在退避中加入抖动，以防止多个客户端同时重试引发的惊群效应
- ✅ 记录每一次重试，包含状态码、延迟和尝试次数，便于调试
- ✅ 设置最大总超时时间，避免无限期挂起
- ✅ 主动使用客户端侧速率限制器，而不仅仅是对 429 做出被动反应
- ✅ 仅在提供方有文档记录的幂等性机制和稳定键的情况下，才对状态变更请求进行重试
- ❌ 不要重试 4xx 客户端错误(408 和 429 除外)——应修复请求
- ❌ 不要使用固定延迟——指数退避能更均匀地分散负载
- ❌ 不要无限制地重试——无边界的重试会放大故障影响
- ❌ 不要忽略单端点限制——某些 API 对不同路由有不同的配额

## 局限性

- 本技能不能替代特定环境的验证、测试或专家审查。
- 令牌桶机制对分布式系统而言只是近似方案——对于多实例部署，请使用基于 Redis 的速率限制(例如 `upstash-ratelimit` 技能，或任何共享存储的限制器)。
- 部分 API 使用非标准的速率限制头；请查阅提供方文档。
- 本文展示的耗时上限约束的是重试等待时间，而非单次网络调用的挂起时长；应将其与 `AbortSignal` 或客户端超时结合使用。

## 常见陷阱

- **问题：** 在故障期间过于激进地重试会放大问题。
  **解决方案：** 对持续性故障使用带抖动的指数退避以及断路器。

- **问题：** 应用程序的多个实例同时进行重试(惊群效应)。
  **解决方案：** 添加随机抖动(`Math.random() * 0.3 * delay`)以消除重试之间的相关性。

- **问题：** Retry-After 头包含 HTTP 日期格式而非秒数。
  **解决方案：** 同时解析两种格式——先检查该值是否为数字，再尝试日期解析。

- **问题：** 客户端侧限制器没有考虑到已在进行中的并发请求。
  **解决方案：** 在单个进程内串行化获取过程，发送前先扣减额度，并在多个实例间使用共享的分布式限制器。

## 相关技能

- `@poka-yoke` - 对 API 进行防错设计，使无效请求永远不会进入重试路径
- `@circuit-breaker` - 何时应完全停止重试并快速失败
