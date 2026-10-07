---
name: ai-sre-incident-response
description: 构建以 AI 为核心的 SRE 事件响应实践,应对 LLM 中断、质量下降、失控的成本事件和安全性回归问题。
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
  version: '1.0'
---

# AI SRE 事件响应

将 SRE 的严谨方法应用于 AI 系统,其中的事件包括质量回归、不安全输出以及预算爆增。

## 何时使用此技能

- LLM 端点开始返回质量下降或出现幻觉的答案
- 令牌消耗超出预算阈值而骤增
- 模型提供商宕机,流量需要故障切换
- 安全护栏以异常高的频率触发
- 新的模型部署导致延迟或准确性回归

## 前提条件

- 已部署 Prometheus 和 Alertmanager,并为 AI 服务配置了抓取目标
- 配置了黄金信号(延迟、错误率、成本、质量)的 Grafana 仪表盘
- 在 PagerDuty、Opsgenie 或同类工具中配置了值班轮换
- 响应人员可访问的运行手册(runbook)仓库
- 模型与提示词版本的回滚机制(GitOps 或功能开关)

## AI 事件类别

- **可用性事件**:模型/提供商不可用、超时风暴。
- **质量事件**:答案准确性或工具调用成功率跌破 SLO。
- **安全事件**:有害或违反策略的输出增加。
- **成本事件**:意外的令牌或提供商支出骤增。

## 严重程度框架

| 严重程度 | 判定标准 | 响应时间 | 通知方式 |
|----------|----------|---------------|--------------|
| SEV1 | 面向用户的中断、合规风险、数据泄露 | 5 分钟 | 呼叫值班人员 + 事件指挥官 |
| SEV2 | 关键流程中出现重大劣化 | 15 分钟 | 呼叫值班人员 |
| SEV3 | 影响有限或仅限内部的问题 | 1 小时 | Slack 告警 |
| SEV4 | 表面性或低优先级的回归 | 下一个工作日 | 工单 |

## AI 服务的黄金信号

- 请求成功率
- 延迟(排队 + 生成 + 工具执行)
- 幻觉/事实依据(groundedness)代理指标
- 每分钟及每租户的成本
- 护栏违规率

## Prometheus 告警规则

```yaml
# prometheus-ai-alerts.yaml
groups:
  - name: ai-service-alerts
    rules:
      - alert: ModelEndpointDown
        expr: up{job="llm-inference"} == 0
        for: 2m
        labels:
          severity: sev1
        annotations:
          summary: "LLM inference endpoint {{ $labels.instance }} is down"
          runbook_url: "https://runbooks.internal/ai/model-outage"

      - alert: HighHallucinationRate
        expr: |
          rate(llm_hallucination_detected_total[10m])
          / rate(llm_requests_total[10m]) > 0.15
        for: 5m
        labels:
          severity: sev2
        annotations:
          summary: "Hallucination rate above 15% for {{ $labels.model }}"
          runbook_url: "https://runbooks.internal/ai/quality-regression"

      - alert: TokenCostExplosion
        expr: |
          sum(rate(llm_token_cost_dollars[5m])) by (tenant)
          > 0.50
        for: 3m
        labels:
          severity: sev2
        annotations:
          summary: "Token spend exceeds $0.50/min for tenant {{ $labels.tenant }}"
          runbook_url: "https://runbooks.internal/ai/cost-spike"

      - alert: LatencyP95Exceeded
        expr: |
          histogram_quantile(0.95,
            rate(llm_request_duration_seconds_bucket[5m])
          ) > 5
        for: 5m
        labels:
          severity: sev2
        annotations:
          summary: "LLM p95 latency exceeds 5s for {{ $labels.service }}"

      - alert: GuardrailViolationSpike
        expr: |
          rate(llm_guardrail_violations_total[10m])
          / rate(llm_requests_total[10m]) > 0.05
        for: 5m
        labels:
          severity: sev1
        annotations:
          summary: "Guardrail violations above 5% for {{ $labels.model }}"
          runbook_url: "https://runbooks.internal/ai/safety-incident"

      - alert: ModelQualityDrop
        expr: |
          llm_eval_score{metric="groundedness"} < 0.70
        for: 10m
        labels:
          severity: sev2
        annotations:
          summary: "Groundedness score dropped below 0.70 for {{ $labels.model }}"

      - alert: ProviderErrorRateHigh
        expr: |
          rate(llm_provider_errors_total[5m])
          / rate(llm_provider_requests_total[5m]) > 0.10
        for: 3m
        labels:
          severity: sev2
        annotations:
          summary: "Provider {{ $labels.provider }} error rate above 10%"
```

## 响应手册

### 模型中断运行手册

```text
TRIGGER: ModelEndpointDown fires for > 2 minutes
RESPONDER: On-call AI platform engineer

1. Acknowledge alert in PagerDuty.
2. Check provider status page (e.g., status.openai.com).
3. Verify network connectivity:
     curl -s -o /dev/null -w "%{http_code}" https://api.provider.com/health
4. If provider is down:
     a. Enable fallback model route in gateway config.
     b. kubectl set env deployment/llm-gateway FALLBACK_ENABLED=true
     c. Verify fallback traffic is flowing via Grafana dashboard.
5. If self-hosted model is down:
     a. Check pod status: kubectl get pods -l app=llm-inference -n ai
     b. Check GPU health: kubectl logs -l app=llm-inference --tail=50
     c. Restart if OOM: kubectl rollout restart deployment/llm-inference -n ai
6. Freeze all deployments:
     kubectl annotate deployment --all deploy-freeze=true -n ai
7. Communicate ETA in #incident-channel.
8. When resolved, unfreeze and run smoke tests.
```

### 质量回归运行手册(幻觉骤增)

```text
TRIGGER: HighHallucinationRate or ModelQualityDrop fires
RESPONDER: On-call AI engineer + ML lead

1. Acknowledge alert. Open incident ticket.
2. Identify scope:
     - Which model version? Check deployment metadata.
     - Which routes/tenants affected? Filter by labels in Grafana.
3. Check recent changes:
     - Model version promotion in last 24h?
     - Prompt template changes in last 24h?
     - Retrieval index rebuild in last 24h?
4. If recent model change:
     kubectl rollout undo deployment/llm-inference -n ai
5. If recent prompt change:
     git revert <commit> && git push  # triggers GitOps redeploy
6. Increase trace sampling to 100% for affected route:
     kubectl set env deployment/llm-gateway TRACE_SAMPLE_RATE=1.0
7. Run offline eval suite against current production:
     python run_evals.py --target prod --suite quality --compare baseline
8. Confirm metrics return to baseline before closing.
```

### 令牌成本爆增运行手册

```text
TRIGGER: TokenCostExplosion fires
RESPONDER: On-call platform engineer

1. Identify top consumers:
     Query: topk(10, sum(rate(llm_token_cost_dollars[15m])) by (tenant, model, route))
2. Check for runaway loops:
     - Agent retry storms (exponential token growth per request)
     - Missing max_tokens caps on new routes
     - Cache bypass due to config change
3. Apply immediate caps:
     kubectl patch configmap llm-quotas -n ai --patch '
       data:
         max_tokens_per_request: "4096"
         rpm_limit: "60"
     '
4. Enable semantic cache if disabled:
     kubectl set env deployment/llm-gateway CACHE_ENABLED=true
5. Route traffic to cheaper model tier:
     kubectl set env deployment/llm-gateway DEFAULT_MODEL=gpt-4o-mini
6. Notify affected tenants of temporary limits.
7. Open postmortem with cost attribution analysis.
```

## 升级流程

```text
Level 1 (0-15 min):  On-call AI platform engineer
Level 2 (15-30 min): AI platform team lead + affected product owner
Level 3 (30-60 min): Engineering director + security (if safety incident)
Level 4 (60+ min):   VP Engineering + legal (if compliance/data incident)

Safety incidents always start at Level 2 minimum.
Provider-side incidents: open support ticket immediately at Level 1.
```

## 检测查询(PromQL)

```promql
# Request success rate by model
1 - (
  sum(rate(llm_requests_total{status="error"}[5m])) by (model)
  / sum(rate(llm_requests_total[5m])) by (model)
)

# Cost per successful answer
sum(rate(llm_token_cost_dollars[5m])) by (route)
/ sum(rate(llm_requests_total{status="success"}[5m])) by (route)

# Hallucination rate trend (1h window, 5m steps)
rate(llm_hallucination_detected_total[1h])
/ rate(llm_requests_total[1h])

# Latency breakdown by stage
histogram_quantile(0.95, rate(llm_retrieval_duration_seconds_bucket[5m]))
histogram_quantile(0.95, rate(llm_generation_duration_seconds_bucket[5m]))
histogram_quantile(0.95, rate(llm_tool_execution_duration_seconds_bucket[5m]))

# Tenant cost leaderboard
topk(10, sum(rate(llm_token_cost_dollars[1h])) by (tenant))
```

## 事后分析要求

- 带检测者和响应者时间戳的时间线
- 按租户和功能划分的影响范围
- 遗漏的信号以及告警调优措施
- 带负责人和截止日期的具体加固任务
- 成本影响(美元、令牌数、受影响的请求数)
- 客户沟通日志

## 事后分析模板

```markdown
## Incident Summary
- **Severity**: SEVx
- **Duration**: start_time - end_time (Xh Ym)
- **Detection**: How was it detected? (alert / customer report / manual)
- **Impact**: X tenants, Y requests, $Z cost

## Timeline
| Time (UTC) | Event |
|------------|-------|
| HH:MM | Alert fired |
| HH:MM | Responder acknowledged |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Incident resolved |

## Root Cause
[Description]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Tune alert threshold | @engineer | YYYY-MM-DD | Open |
| Add fallback route | @platform | YYYY-MM-DD | Open |
```

## AI 系统的混沌工程

定期测试事件应对能力:

- **提供商故障切换演练**:在网络层屏蔽提供商 API,验证回退方案在 SLO 范围内启动。
- **模型回滚演练**:部署已知存在问题的模型版本,验证自动化质量关口能够捕获它。
- **成本上限演练**:模拟失控的令牌用量,验证配额在超出预算阈值之前生效。
- **缓存故障演练**:禁用语义缓存,验证系统能够优雅降级。

## 故障排查

| 症状 | 检查项 | 修复方法 |
|---------|-------|-----|
| 所有请求均超时 | 提供商状态页、DNS 解析 | 启用回退提供商 |
| 质量逐渐下降 | 近期的模型/提示词部署 | 回滚到最近一个已知良好的版本 |
| 成本骤增 | 按租户的令牌用量仪表盘 | 应用紧急令牌上限 |
| 护栏违规骤增 | 模型版本、提示注入日志 | 启用更严格的输入过滤 |
| 间歇性 503 错误 | Pod 重启、GPU OOM 事件 | 增加内存限制或减小批处理大小 |

## 相关技能

- incident-response (`incident-response`) - 标准事件处理流程和证据留存
- alerting-oncall (`alerting-oncall`) - 寻呼与升级策略
- llm-cost-optimization (`llm-cost-optimization`) - 支出控制与效率模式
- agent-observability (`agent-observability`) - 请求、追踪与成本的埋点
- rag-observability-evals (`rag-observability-evals`) - RAG 质量监控

## 限制

- 本指导会作用于真实环境:应用任何操作前,先确认目标范围、影响面和回滚方案。
- 未经明确批准,切勿部署到生产环境。仅导入文档:上游脚本和模板未随附。

### 示例

```bash
git status && git diff --stat
kubectl diff -f manifest.yaml
```

> 改编自 [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills) (MIT);为符合上游合规要求,新增了 frontmatter、"何时使用"/"限制"部分及安全边界说明。仅导入文档:未随附辅助脚本和模板。
