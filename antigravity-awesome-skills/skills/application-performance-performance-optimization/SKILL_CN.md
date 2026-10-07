---
name: application-performance-performance-optimization
description: "通过性能剖析、可观测性以及后端/前端调优,进行端到端的应用性能优化。在需要跨整个技术栈协调性能优化工作时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

使用专门的性能与优化代理,端到端地优化应用性能：

[扩展思考：本工作流在整个应用技术栈范围内,组织一套全面的性能优化流程。从深度性能剖析和基线建立开始,工作流依次推进到各系统层级的针对性优化,通过负载测试验证改进效果,并为持续性能表现建立长期监控。每个阶段都基于前一阶段的洞见展开,形成一套数据驱动的优化策略,针对真实瓶颈而非理论上的改进。该工作流强调现代可观测性实践、以用户为中心的性能指标,以及具有成本效益的优化策略。]

## 何时使用本技能

- 在后端、前端和基础设施之间协调性能优化工作
- 建立基线并进行性能剖析以识别瓶颈
- 设计负载测试、性能预算或容量规划
- 为性能和可靠性目标构建可观测性体系

## 何时不使用本技能

- 任务只是一个没有更大性能目标的小范围局部修复
- 无法访问指标、追踪或性能剖析数据
- 请求与性能或可扩展性无关

## 操作说明

1. 确认性能目标、约束条件和目标指标。
2. 通过性能剖析、追踪和真实用户数据建立基线。
3. 在整个技术栈中分阶段执行可衡量的优化。
4. 验证改进效果,并设置防护措施以防止性能回退。

## 安全事项

- 避免在没有审批和保障措施的情况下对生产环境进行负载测试。
- 分阶段逐步推出性能变更,并制定回滚方案。

## 第一阶段：性能剖析与基线建立

### 1. 全面性能剖析

- 使用 Task 工具,subagent_type="performance-engineer"
- 提示词："为以下目标全面剖析应用性能：$ARGUMENTS。为 CPU 使用情况生成火焰图,为内存分析生成堆转储,追踪 I/O 操作,并识别热点路径。如可用,使用 DataDog 或 New Relic 等 APM 工具。包括数据库查询性能剖析、API 响应时间,以及前端渲染指标。为所有关键用户路径建立性能基线。"
- 上下文：初步性能调查
- 输出：包含火焰图、内存分析、瓶颈识别和基线指标的详细性能剖析报告

### 2. 可观测性体系评估

- 使用 Task 工具,subagent_type="observability-engineer"
- 提示词："评估以下目标的当前可观测性建设情况：$ARGUMENTS。审查现有监控体系、基于 OpenTelemetry 的分布式追踪、日志聚合以及指标采集。识别可观测性方面的盲区、缺失的指标,以及需要更好埋点的领域。为业务关键操作推荐 APM 工具集成方案和自定义指标。"
- 上下文：第 1 步得到的性能剖析结果
- 输出：可观测性评估报告、埋点盲区、监控建议

### 3. 用户体验分析

- 使用 Task 工具,subagent_type="performance-engineer"
- 提示词："分析以下目标的用户体验指标：$ARGUMENTS。测量核心网页指标（Core Web Vitals,LCP、FID、CLS）、页面加载时间、可交互时间,以及感知性能。如可用,使用真实用户监控（RUM）数据。识别性能表现不佳的用户路径及其业务影响。"
- 上下文：第 1 步得到的性能基线
- 输出：用户体验性能报告、Core Web Vitals 分析、用户影响评估

## 第二阶段：数据库与后端优化

### 4. 数据库性能优化

- 使用 Task 工具,subagent_type="database-cloud-optimization::database-optimizer"
- 提示词："基于第一阶段的剖析数据：{context_from_phase_1},优化以下目标的数据库性能：$ARGUMENTS。分析慢查询日志,创建缺失的索引,优化执行计划,使用 Redis/Memcached 实现查询结果缓存。审查连接池、预编译语句以及批处理机会。如有需要,考虑引入只读副本和数据库分片。"
- 上下文：第一阶段的性能瓶颈
- 输出：优化后的查询、新索引、缓存策略、连接池配置

### 5. 后端代码与 API 优化

- 使用 Task 工具,subagent_type="backend-development::backend-architect"
- 提示词："针对以下瓶颈：{context_from_phase_1},优化以下目标的后端服务：$ARGUMENTS。实现高效算法,添加应用层缓存,优化 N+1 查询,有效运用 async/await 模式。实现分页、响应压缩、GraphQL 查询优化以及批量 API 操作。为提升弹性,添加熔断器和舱壁隔离机制。"
- 上下文：第 4 步的数据库优化结果,以及第一阶段的性能剖析数据
- 输出：优化后的后端代码、缓存实现、API 改进、弹性模式

### 6. 微服务与分布式系统优化

- 使用 Task 工具,subagent_type="performance-engineer"
- 提示词："优化以下目标的分布式系统性能：$ARGUMENTS。分析服务间通信,实施服务网格优化,优化消息队列性能（Kafka/RabbitMQ）,减少网络跳数。实施分布式缓存策略并优化序列化/反序列化。"
- 上下文：第 5 步的后端优化结果
- 输出：服务通信改进、消息队列优化、分布式缓存搭建方案

## 第三阶段：前端与 CDN 优化

### 7. 前端打包与加载优化

- 使用 Task 工具,subagent_type="frontend-developer"
- 提示词："针对核心网页指标：{context_from_phase_1},优化以下目标的前端性能：$ARGUMENTS。实现代码拆分、tree shaking、懒加载和动态导入。借助 webpack/rollup 分析优化打包体积。实现资源预加载提示（prefetch、preconnect、preload）。优化关键渲染路径并消除阻塞渲染的资源。"
- 上下文：第一阶段的用户体验分析结果,以及第二阶段的后端优化结果
- 输出：优化后的打包文件、懒加载实现、改善后的 Core Web Vitals

### 8. CDN 与边缘优化

- 使用 Task 工具,subagent_type="cloud-infrastructure::cloud-architect"
- 提示词："优化以下目标的 CDN 和边缘性能：$ARGUMENTS。配置 CloudFlare/CloudFront 以实现最优缓存,为动态内容实施边缘函数,通过响应式图片以及 WebP/AVIF 格式搭建图片优化方案。配置 HTTP/2 和 HTTP/3,实施 Brotli 压缩。为全球用户设置地理分布方案。"
- 上下文：第 7 步的前端优化结果
- 输出：CDN 配置、边缘缓存规则、压缩设置、地理优化方案

### 9. 移动端与渐进式 Web 应用优化

- 使用 Task 工具,subagent_type="frontend-mobile-development::mobile-developer"
- 提示词："优化以下目标的移动端体验：$ARGUMENTS。实现 Service Worker 以支持离线功能,针对慢速网络实现自适应加载。减少移动端 CPU 上的 JavaScript 执行时间。为长列表实现虚拟滚动。优化触控响应性和动画流畅度。如适用,考虑针对 React Native/Flutter 的专门优化。"
- 上下文：第 7-8 步的前端优化结果
- 输出：移动端优化后的代码、PWA 实现、离线功能

## 第四阶段：负载测试与验证

### 10. 全面负载测试

- 使用 Task 工具,subagent_type="performance-engineer"
- 提示词："使用 k6/Gatling/Artillery 为以下目标进行全面的负载测试：$ARGUMENTS。基于生产流量模式设计真实的负载场景。测试正常负载、峰值负载和压力场景。如适用,包括 API 测试、基于浏览器的测试以及 WebSocket 测试。测量不同负载水平下的响应时间、吞吐量、错误率和资源利用率。"
- 上下文：第一至第三阶段的所有优化成果
- 输出：负载测试结果、负载下的性能表现、系统临界点、可扩展性分析

### 11. 性能回归测试

- 使用 Task 工具,subagent_type="performance-testing-review::test-automator"
- 提示词："为以下目标创建自动化性能回归测试：$ARGUMENTS。为关键指标设置性能预算,使用 GitHub Actions 或类似工具将其集成到 CI/CD 流水线中。为前端创建 Lighthouse CI 测试,使用 Artillery 创建 API 性能测试,以及数据库性能基准测试。实现针对性能回退的自动回滚触发机制。"
- 上下文：第 10 步的负载测试结果,以及第一阶段的基线指标
- 输出：性能测试套件、CI/CD 集成、回归预防体系

## 第五阶段：监控与持续优化

### 12. 生产环境监控搭建

- 使用 Task 工具,subagent_type="observability-engineer"
- 提示词："为以下目标实现生产环境性能监控：$ARGUMENTS。使用 DataDog/New Relic/Dynatrace 搭建 APM,配置基于 OpenTelemetry 的分布式追踪,实现自定义业务指标。为关键指标创建 Grafana 仪表盘,为性能退化设置 PagerDuty 告警。为关键服务定义带有错误预算的 SLI/SLO。"
- 上下文：前几个阶段取得的所有性能改进
- 输出：监控仪表盘、告警规则、SLI/SLO 定义、运维手册（runbook）

### 13. 持续性能优化

- 使用 Task 工具,subagent_type="performance-engineer"
- 提示词："为以下目标建立持续优化流程：$ARGUMENTS。创建性能预算跟踪机制,为性能变更实施 A/B 测试,在生产环境中搭建持续性能剖析。记录优化机会待办清单,创建容量规划模型,并建立定期的性能复盘机制。"
- 上下文：第 12 步的监控搭建结果,以及之前所有的优化工作
- 输出：性能预算跟踪、优化待办清单、容量规划、复盘流程

## 配置选项

- **performance_focus**："latency"（延迟) | "throughput"（吞吐量) | "cost"（成本) | "balanced"（均衡,默认值）
- **optimization_depth**："quick-wins"（速效改进) | "comprehensive"（全面,默认值) | "enterprise"（企业级）
- **tools_available**：["datadog", "newrelic", "prometheus", "grafana", "k6", "gatling"]
- **budget_constraints**：为基础设施变更设置最大可接受成本
- **user_impact_tolerance**："zero-downtime"（零停机) | "maintenance-window"（维护窗口) | "gradual-rollout"（渐进发布）

## 成功标准

- **响应时间**：关键端点 P50 < 200ms,P95 < 1s,P99 < 2s
- **核心网页指标（Core Web Vitals）**：LCP < 2.5s,FID < 100ms,CLS < 0.1
- **吞吐量**：以 <1% 的错误率支持当前峰值负载的 2 倍
- **数据库性能**：查询 P95 < 100ms,无耗时超过 1s 的查询
- **资源利用率**：正常负载下 CPU < 70%,内存 < 80%
- **成本效率**：单位成本的性能至少提升 30%
- **监控覆盖率**：100% 的关键路径均完成埋点并配置告警

性能优化目标：$ARGUMENTS

## 示例

**用户请求：**

> Coordinate performance optimization across backend, frontend, and infrastructure.

## 局限性
- 仅在任务明确符合上述范围描述时使用本技能。
- 不要将输出当作特定环境验证、测试或专家评审的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,请停下来请求澄清。
