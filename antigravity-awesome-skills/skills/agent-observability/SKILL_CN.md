---
name: agent-observability
description: 为 AI 智能体添加追踪、Token 指标、延迟和成本可观测性的能力。适用于可靠性与调试场景。
category: devops
risk: critical
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: Requires the relevant platform CLIs (kubectl, helm, terraform, git,
  CI runners) and authorized access to the target environment. Docs-only; helper scripts
  and templates not bundled.
metadata:
  author: devops-skills
  version: '2.0'
---

# 智能体可观测性(Agent Observability)

使用日志、追踪、指标和成本遥测来监控 AI 智能体的行为。本技能涵盖了面向 LLM 驱动应用的完整可观测性栈:从原始的 Prometheus 计数器到 Grafana 仪表盘、OpenTelemetry 追踪、结构化日志、成本追踪、SLO 定义,以及 PII 脱敏。

---

## 核心指标

在应用层定义这些指标。所有示例均使用 Prometheus 客户端库的命名约定。

### 延迟

```python
from prometheus_client import Histogram

# Total end-to-end latency for a full agent turn (user prompt -> final response)
AGENT_LATENCY = Histogram(
    "agent_request_duration_seconds",
    "End-to-end latency of an agent request",
    labelnames=["agent_name", "model", "status"],
    buckets=(0.25, 0.5, 1, 2, 5, 10, 30, 60, 120),
)

# Latency of a single LLM API call (one completion request)
LLM_CALL_LATENCY = Histogram(
    "llm_call_duration_seconds",
    "Latency of an individual LLM API call",
    labelnames=["model", "provider", "stream"],
    buckets=(0.1, 0.25, 0.5, 1, 2, 5, 10, 30),
)

# Latency of tool/function calls executed by the agent
TOOL_CALL_LATENCY = Histogram(
    "agent_tool_call_duration_seconds",
    "Latency of a tool call executed by the agent",
    labelnames=["tool_name", "agent_name", "status"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10),
)
```

### Token 使用量

```python
from prometheus_client import Counter, Histogram

PROMPT_TOKENS = Counter(
    "llm_prompt_tokens_total",
    "Total prompt tokens sent to the model",
    labelnames=["model", "agent_name"],
)

COMPLETION_TOKENS = Counter(
    "llm_completion_tokens_total",
    "Total completion tokens received from the model",
    labelnames=["model", "agent_name"],
)

CACHED_TOKENS = Counter(
    "llm_cached_tokens_total",
    "Prompt tokens served from KV-cache (provider-reported)",
    labelnames=["model", "agent_name"],
)

TOKENS_PER_REQUEST = Histogram(
    "llm_tokens_per_request",
    "Total tokens (prompt + completion) per request",
    labelnames=["model", "agent_name"],
    buckets=(100, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000),
)
```

### 成本

```python
from prometheus_client import Counter

LLM_COST = Counter(
    "llm_cost_dollars_total",
    "Estimated cost in USD for LLM usage",
    labelnames=["model", "agent_name", "cost_type"],  # cost_type: prompt | completion
)
```

### 工具调用

```python
from prometheus_client import Counter

TOOL_CALLS_TOTAL = Counter(
    "agent_tool_calls_total",
    "Total tool calls made by agents",
    labelnames=["tool_name", "agent_name", "status"],  # status: success | error | timeout
)
```

### 错误与重试

```python
from prometheus_client import Counter, Gauge

LLM_ERRORS = Counter(
    "llm_errors_total",
    "Errors returned by the LLM provider",
    labelnames=["model", "provider", "error_type"],  # error_type: rate_limit | timeout | 5xx | auth
)

LLM_RETRIES = Counter(
    "llm_retries_total",
    "Retried LLM API calls",
    labelnames=["model", "provider", "retry_reason"],
)

AGENT_ACTIVE_REQUESTS = Gauge(
    "agent_active_requests",
    "Number of agent requests currently in flight",
    labelnames=["agent_name"],
)
```

---

## OpenTelemetry 集成

使用 OpenTelemetry Python SDK 创建能够捕获一次智能体回合中每一步的追踪:顶层请求、每次 LLM 调用、每次工具执行,以及检索操作。

### 配置

```python
# otel_setup.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

def init_tracing(service_name: str, otlp_endpoint: str = "http://localhost:4317"):
    resource = Resource.create({
        "service.name": service_name,
        "service.version": "1.0.0",
        "deployment.environment": "production",
    })
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)
```

### 追踪 LLM 调用

```python
# llm_tracing.py
import time
from opentelemetry import trace
from opentelemetry.trace import StatusCode

tracer = trace.get_tracer("agent.llm")

def traced_llm_call(client, messages, model="gpt-4o", **kwargs):
    """Wrap an LLM completion call with a full OpenTelemetry span."""
    with tracer.start_as_current_span("llm.chat_completion") as span:
        span.set_attribute("llm.model", model)
        span.set_attribute("llm.provider", "openai")
        span.set_attribute("llm.message_count", len(messages))
        span.set_attribute("llm.temperature", kwargs.get("temperature", 1.0))
        span.set_attribute("llm.max_tokens", kwargs.get("max_tokens", 0))

        start = time.perf_counter()
        try:
            response = client.chat.completions.create(
                model=model, messages=messages, **kwargs
            )
            elapsed = time.perf_counter() - start

            usage = response.usage
            span.set_attribute("llm.prompt_tokens", usage.prompt_tokens)
            span.set_attribute("llm.completion_tokens", usage.completion_tokens)
            span.set_attribute("llm.total_tokens", usage.total_tokens)
            span.set_attribute("llm.duration_seconds", elapsed)
            span.set_attribute("llm.finish_reason", response.choices[0].finish_reason)
            span.set_status(StatusCode.OK)

            # Update Prometheus counters
            PROMPT_TOKENS.labels(model=model, agent_name="default").inc(usage.prompt_tokens)
            COMPLETION_TOKENS.labels(model=model, agent_name="default").inc(usage.completion_tokens)
            LLM_CALL_LATENCY.labels(model=model, provider="openai", stream="false").observe(elapsed)

            return response

        except Exception as exc:
            elapsed = time.perf_counter() - start
            span.set_status(StatusCode.ERROR, str(exc))
            span.record_exception(exc)
            LLM_ERRORS.labels(model=model, provider="openai", error_type=type(exc).__name__).inc()
            raise
```

### 追踪工具执行

```python
# tool_tracing.py
import functools
from opentelemetry import trace
from opentelemetry.trace import StatusCode

tracer = trace.get_tracer("agent.tools")

def traced_tool(tool_name: str):
    """Decorator that wraps a tool function with an OTel span and Prometheus metrics."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(f"tool.{tool_name}") as span:
                span.set_attribute("tool.name", tool_name)
                span.set_attribute("tool.args_count", len(args) + len(kwargs))

                import time
                start = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    elapsed = time.perf_counter() - start
                    span.set_attribute("tool.duration_seconds", elapsed)
                    span.set_status(StatusCode.OK)
                    TOOL_CALLS_TOTAL.labels(
                        tool_name=tool_name, agent_name="default", status="success"
                    ).inc()
                    TOOL_CALL_LATENCY.labels(
                        tool_name=tool_name, agent_name="default", status="success"
                    ).observe(elapsed)
                    return result
                except Exception as exc:
                    elapsed = time.perf_counter() - start
                    span.set_status(StatusCode.ERROR, str(exc))
                    span.record_exception(exc)
                    TOOL_CALLS_TOTAL.labels(
                        tool_name=tool_name, agent_name="default", status="error"
                    ).inc()
                    TOOL_CALL_LATENCY.labels(
                        tool_name=tool_name, agent_name="default", status="error"
                    ).observe(elapsed)
                    raise
        return wrapper
    return decorator

# Usage
@traced_tool("web_search")
def web_search(query: str) -> str:
    # ... tool implementation ...
    pass

@traced_tool("sql_query")
def sql_query(statement: str) -> list:
    # ... tool implementation ...
    pass
```

### 跨服务传播追踪上下文

```python
# context_propagation.py
from opentelemetry import context
from opentelemetry.propagate import inject, extract
import httpx

def call_downstream_service(url: str, payload: dict) -> dict:
    """Propagate the current trace context to a downstream HTTP service."""
    headers = {}
    inject(headers)  # injects traceparent + tracestate headers
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_context_from_request(request_headers: dict):
    """Extract trace context from incoming request headers (for the receiving service)."""
    ctx = extract(request_headers)
    token = context.attach(ctx)
    return token  # call context.detach(token) when done
```

---


## 目录

- [结构化日志](references/details.md)
- [Grafana 仪表盘](references/details.md)
- [成本追踪](references/details.md)
- [Langfuse / Helicone 集成](references/details.md)
- [SLO 定义](references/details.md)
- [调试工作流](references/details.md)
- [追踪中的 PII 脱敏](references/details.md)
- [最佳实践](references/details.md)
- [相关技能](references/details.md)

## 何时使用

在以下场景中应用本技能:

- **自主 AI 智能体**,它们会进行多步骤的工具调用(例如编码智能体、支持类智能体、数据管道智能体)。
- **LLM 驱动的 API**,在 REST 或 gRPC 网关之后提供聊天补全、摘要生成或分类服务。
- **RAG 管道**,其中检索器在向模型提示之前从向量存储中获取上下文。
- **多智能体编排**(crew 式或基于图的),多个智能体协作完成单个任务。
- **批量推理任务**,针对某个模型端点处理成千上万条提示。

你需要本技能的关键信号:

1. 你无法回答"本周智能体响应的 p95 延迟是多少?"
2. 你没有按请求归因的成本数据。
3. 调试一个糟糕的智能体响应需要在原始应用日志中进行 grep。
4. 你对 Token 使用量激增或错误率升高没有任何告警机制。

---

## 局限性

- 本指南会在真实环境中执行:在应用任何内容之前,请确认目标、影响范围和回滚方案。
- 未经明确批准,切勿部署到生产环境。本次为纯文档导入:未附带上游脚本和模板。

### 示例

```bash
git status && git diff --stat
kubectl diff -f manifest.yaml
```

> 改编自 [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills) (MIT);为符合上游合规要求,新增了 frontmatter、"何时使用/局限性"以及安全边界说明。本次为纯文档导入:未附带辅助脚本和模板。
