---
name: cloudflare-deploy
description: 使用 Workers、Pages 和相关平台服务将应用程序和基础设施部署到 Cloudflare。当用户要求部署、托管、发布或在 Cloudflare 上设置项目时使用。
---

# Cloudflare 部署

用于在 Cloudflare 平台上构建的整合技能。使用下面的决策树找到正确的产品，然后加载详细的参考文档。

## 前置条件

- 当沙箱阻止部署网络调用时，使用 `sandbox_permissions=require_escalated` 重新运行
- 部署可能需要几分钟。使用适当的超时值。

## 身份验证（部署前必需）

在 `wrangler deploy`、`wrangler pages deploy` 或 `npm run deploy` 之前验证身份：

```bash
npx wrangler whoami    # 显示是否已通过身份验证
```

未通过身份验证？→ `references/wrangler/auth.md`
- 交互/本地：`wrangler login`（一次性 OAuth）
- CI/CD：设置 `CLOUDFLARE_API_TOKEN` 环境变量

## 快速决策树

### "我需要运行代码"

```
需要运行代码？
├─ 边缘的无服务器函数 → workers/
├─ 具有部署的 Git 的全栈 Web 应用 → pages/
├─ 有状态协调/实时 → durable-objects/
├─ 长时间运行的多步骤任务 → workflows/
├─ 运行容器 → containers/
├─ 多租户（客户部署代码）→ workers-for-platforms/
├─ 计划任务（cron）→ cron-triggers/
├─ 轻量级边缘逻辑（修改 HTTP）→ snippets/
├─ 处理 Worker 执行事件（日志/可观察性）→ tail-workers/
└─ 优化后端基础设施的延迟 → smart-placement/
```

### "我需要存储数据"

```
需要存储？
├─ 键值（配置、会话、缓存）→ kv/
├─ 关系型 SQL → d1/（SQLite）或 hyperdrive/（现有的 Postgres/MySQL）
├─ 对象/文件存储（S3 兼容）→ r2/
├─ 消息队列（异步处理）→ queues/
├─ 向量嵌入（AI/语义搜索）→ vectorize/
├─ 强一致性每实体状态 → durable-objects/（DO 存储）
├─ 密钥管理 → secrets-store/
├─ 流式 ETL 到 R2 → pipelines/
└─ 持久缓存（长期保留）→ cache-reserve/
```

### "我需要 AI/ML"

```
需要 AI？
├─ 运行推理（LLMs、嵌入、图像）→ workers-ai/
├─ 向量数据库用于 RAG/搜索 → vectorize/
├─ 构建有状态的 AI 智能体 → agents-sdk/
├─ 任何 AI 提供商的网关（缓存、路由）→ ai-gateway/
└─ AI 驱动的搜索小部件 → ai-search/
```

### "我需要网络/连接性"

```
需要网络？
├─ 将本地服务暴露到互联网 → tunnel/
├─ TCP/UDP 代理（非 HTTP）→ spectrum/
├─ WebRTC TURN 服务器 → turn/
├─ 私有网络连接性 → network-interconnect/
├─ 优化路由 → argo-smart-routing/
├─ 优化后端延迟（非用户）→ smart-placement/
└─ 实时视频/音频 → realtimekit/ 或 realtime-sfu/
```

### "我需要安全性"

```
需要安全性？
├─ Web 应用程序防火墙 → waf/
├─ DDoS 保护 → ddos/
├─ 机器人检测/管理 → bot-management/
├─ API 保护 → api-shield/
├─ CAPTCHA 替代方案 → turnstile/
└─ 凭证泄漏检测 → waf/（托管规则集）
```

### "我需要媒体/内容"

```
需要媒体？
├─ 图像优化/转换 → images/
├─ 视频流式传输/编码 → stream/
├─ 浏览器自动化/截图 → browser-rendering/
└─ 第三方脚本管理 → zaraz/
```

### "我需要基础设施即代码"

```
需要 IaC？→ pulumi/（Pulumi）、terraform/（Terraform）或 api/（REST API）
```

## 产品索引

### 计算与运行时
| 产品 | 参考 |
|---------|-----------|
| Workers | `references/workers/` |
| Pages | `references/pages/` |
| Pages Functions | `references/pages-functions/` |
| Durable Objects | `references/durable-objects/` |
| Workflows | `references/workflows/` |
| Containers | `references/containers/` |
| Workers for Platforms | `references/workers-for-platforms/` |
| Cron Triggers | `references/cron-triggers/` |
| Tail Workers | `references/tail-workers/` |
| Snippets | `references/snippets/` |
| Smart Placement | `references/smart-placement/` |

### 存储与数据
| 产品 | 参考 |
|---------|-----------|
| KV | `references/kv/` |
| D1 | `references/d1/` |
| R2 | `references/r2/` |
| Queues | `references/queues/` |
| Hyperdrive | `references/hyperdrive/` |
| DO Storage | `references/do-storage/` |
| Secrets Store | `references/secrets-store/` |
| Pipelines | `references/pipelines/` |
| R2 Data Catalog | `references/r2-data-catalog/` |
| R2 SQL | `references/r2-sql/` |

### AI 与机器学习
| 产品 | 参考 |
|---------|-----------|
| Workers AI | `references/workers-ai/` |
| Vectorize | `references/vectorize/` |
| Agents SDK | `references/agents-sdk/` |
| AI Gateway | `references/ai-gateway/` |
| AI Search | `references/ai-search/` |

### 网络与连接性
| 产品 | 参考 |
|---------|-----------|
| Tunnel | `references/tunnel/` |
| Spectrum | `references/spectrum/` |
| TURN | `references/turn/` |
| Network Interconnect | `references/network-interconnect/` |
| Argo Smart Routing | `references/argo-smart-routing/` |
| Workers VPC | `references/workers-vpc/` |

### 安全性
| 产品 | 参考 |
|---------|-----------|
| WAF | `references/waf/` |
| DDoS Protection | `references/ddos/` |
| Bot Management | `references/bot-management/` |
| API Shield | `references/api-shield/` |
| Turnstile | `references/turnstile/` |

### 媒体与内容
| 产品 | 参考 |
|---------|-----------|
| Images | `references/images/` |
| Stream | `references/stream/` |
| Browser Rendering | `references/browser-rendering/` |
| Zaraz | `references/zaraz/` |

### 实时通信
| 产品 | 参考 |
|---------|-----------|
| RealtimeKit | `references/realtimekit/` |
| Realtime SFU | `references/realtime-sfu/` |

### 开发者工具
| 产品 | 参考 |
|---------|-----------|
| Wrangler | `references/wrangler/` |
| Miniflare | `references/miniflare/` |
| C3 | `references/c3/` |
| Observability | `references/observability/` |
| Analytics Engine | `references/analytics-engine/` |
| Web Analytics | `references/web-analytics/` |
| Sandbox | `references/sandbox/` |
| Workerd | `references/workerd/` |
| Workers Playground | `references/workers-playground/` |

### 基础设施即代码
| 产品 | 参考 |
|---------|-----------|
| Pulumi | `references/pulumi/` |
| Terraform | `references/terraform/` |
| API | `references/api/` |

### 其他服务
| 产品 | 参考 |
|---------|-----------|
| Email Routing | `references/email-routing/` |
| Email Workers | `references/email-workers/` |
| Static Assets | `references/static-assets/` |
| Bindings | `references/bindings/` |
| Cache Reserve | `references/cache-reserve/` |

## 故障排除

### 升级的网络访问

如果由于网络问题（超时、DNS 错误、连接重置）导致部署失败，使用提升的权限重新运行部署（使用 `sandbox_permissions=require_escalated`）。部署需要提升的网络访问权限，当沙箱网络阻止出站请求时。

给用户的示例指导：

```
部署需要提升的网络访问权限才能部署到 Cloudflare。我可以使用提升的权限重新运行命令—要我继续吗？
```
