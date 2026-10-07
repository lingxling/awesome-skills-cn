---
name: ai-inference-service-mesh
description: 使用服务网格模式进行 AI 推理流量管理、mTLS、金丝雀发布、策略强制实施以及跨集群弹性保障。
category: devops
risk: critical
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: Requires the relevant OS/platform tooling and privileged access where
  noted. Docs-only; helper scripts and templates not bundled.
metadata:
  author: devops-skills
  version: '1.0'
---

# AI Inference Service Mesh

应用 Istio/Linkerd 网格控制措施，保护和优化跨推理微服务的东西向 AI 流量。

## 为什么要为 AI 使用服务网格

- 在网关、检索器、重排序器和模型服务之间强制实施 mTLS
- 在不修改应用代码的情况下应用细粒度的流量策略
- 为模型服务后端运行渐进式发布
- 观察检索 + 生成链路中各跳的延迟
- 按模型版本、租户或优先级层路由推理请求
- 保护开销高昂的 GPU 支持服务，防止级联故障

## 前提条件

```bash
# 使用生产配置安装 Istio
istioctl install --set profile=default \
  --set meshConfig.accessLogFile=/dev/stdout \
  --set meshConfig.defaultConfig.holdApplicationUntilProxyStarts=true

# 为推理命名空间打标签以启用 sidecar 注入
kubectl create namespace ai-inference
kubectl label namespace ai-inference istio-injection=enabled

# 验证安装
istioctl verify-install
istioctl analyze -n ai-inference
```

## 核心模式

### 集群范围内的 mTLS 严格模式

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
---
# 如需渐进式发布，可在命名空间级别覆盖
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: ai-inference-mtls
  namespace: ai-inference
spec:
  mtls:
    mode: STRICT
  portLevelMtls:
    # gRPC 推理端口
    8081:
      mode: STRICT
    # Prometheus 指标端口——允许明文抓取
    9090:
      mode: PERMISSIVE
```

### 按服务账户设置的 AuthorizationPolicy

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: model-server-access
  namespace: ai-inference
spec:
  selector:
    matchLabels:
      app: model-server
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - "cluster.local/ns/ai-inference/sa/api-gateway"
        - "cluster.local/ns/ai-inference/sa/orchestrator"
    to:
    - operation:
        methods: ["POST"]
        paths: ["/v1/predict", "/v1/embeddings", "/v2/models/*/infer"]
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-external-to-retriever
  namespace: ai-inference
spec:
  selector:
    matchLabels:
      app: vector-retriever
  action: DENY
  rules:
  - from:
    - source:
        notNamespaces: ["ai-inference"]
```

### 针对已批准模型端点的出站策略

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: openai-api
  namespace: ai-inference
spec:
  hosts:
  - api.openai.com
  ports:
  - number: 443
    name: https
    protocol: TLS
  resolution: DNS
  location: MESH_EXTERNAL
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: openai-api-tls
  namespace: ai-inference
spec:
  host: api.openai.com
  trafficPolicy:
    tls:
      mode: SIMPLE
    connectionPool:
      http:
        h2UpgradePolicy: UPGRADE
      tcp:
        maxConnections: 50
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: restrict-egress
  namespace: ai-inference
spec:
  action: ALLOW
  rules:
  - to:
    - operation:
        hosts:
        - "api.openai.com"
        - "models.anthropic.com"
        - "*.blob.core.windows.net"
```

## 流量管理

### 用于 A/B 模型测试的 VirtualService

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: model-server
  namespace: ai-inference
spec:
  hosts:
  - model-server
  http:
  # 按 header 路由以明确选择模型版本
  - match:
    - headers:
        x-model-version:
          exact: "v2-experimental"
    route:
    - destination:
        host: model-server
        subset: v2-experimental
    timeout: 120s
  # 按 header 路由以选择 A/B 测试分组
  - match:
    - headers:
        x-ab-cohort:
          exact: "treatment"
    route:
    - destination:
        host: model-server
        subset: v2-experimental
      weight: 100
    timeout: 120s
  # 默认流量拆分：90/10 金丝雀发布
  - route:
    - destination:
        host: model-server
        subset: v1-stable
      weight: 90
    - destination:
        host: model-server
        subset: v2-experimental
      weight: 10
    timeout: 60s
    retries:
      attempts: 2
      perTryTimeout: 30s
      retryOn: unavailable,resource-exhausted
```

### 带 Subsets 的 DestinationRule

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: model-server
  namespace: ai-inference
spec:
  host: model-server
  trafficPolicy:
    connectionPool:
      http:
        h2UpgradePolicy: UPGRADE
        maxRequestsPerConnection: 100
      tcp:
        maxConnections: 200
        connectTimeout: 5s
    loadBalancer:
      simple: LEAST_REQUEST
  subsets:
  - name: v1-stable
    labels:
      version: v1
    trafficPolicy:
      connectionPool:
        http:
          maxRequestsPerConnection: 50
  - name: v2-experimental
    labels:
      version: v2
    trafficPolicy:
      connectionPool:
        http:
          maxRequestsPerConnection: 20
```

### 推理后端的断路器

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: model-server-circuit-breaker
  namespace: ai-inference
spec:
  host: model-server
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 10s
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 200
        maxRequestsPerConnection: 10
        maxRetries: 3
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 15s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 30
      splitExternalLocalOriginErrors: true
---
# 用于向量检索器的独立断路器
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: vector-retriever-circuit-breaker
  namespace: ai-inference
spec:
  host: vector-retriever
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 300
      http:
        http1MaxPendingRequests: 200
        http2MaxRequests: 500
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 15s
      maxEjectionPercent: 30
```

### 流式请求的重试预算

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: streaming-inference
  namespace: ai-inference
spec:
  hosts:
  - model-server
  http:
  # 流式端点：不重试，长超时
  - match:
    - uri:
        prefix: /v1/stream
    route:
    - destination:
        host: model-server
        subset: v1-stable
    timeout: 300s
    retries:
      attempts: 0
  # 嵌入端点：可以安全重试，短超时
  - match:
    - uri:
        prefix: /v1/embeddings
    route:
    - destination:
        host: model-server
        subset: v1-stable
    timeout: 15s
    retries:
      attempts: 3
      perTryTimeout: 5s
      retryOn: 5xx,reset,connect-failure,retriable-status-codes
```

## 弹性

### 本地可用区感知路由

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: model-server-locality
  namespace: ai-inference
spec:
  host: model-server
  trafficPolicy:
    loadBalancer:
      localityLbSetting:
        enabled: true
        distribute:
        - from: "us-east-1/us-east-1a/*"
          to:
            "us-east-1/us-east-1a/*": 80
            "us-east-1/us-east-1b/*": 20
        failover:
        - from: us-east-1
          to: us-west-2
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
```

## 可观测性

```yaml
# 用于推理服务自定义指标的 Telemetry 资源
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: inference-telemetry
  namespace: ai-inference
spec:
  metrics:
  - providers:
    - name: prometheus
    overrides:
    - match:
        metric: REQUEST_DURATION
        mode: CLIENT_AND_SERVER
      tagOverrides:
        model_name:
          operation: UPSERT
          value: "request.headers['x-model-name']"
        tenant_id:
          operation: UPSERT
          value: "request.headers['x-tenant-id']"
  tracing:
  - providers:
    - name: zipkin
    randomSamplingPercentage: 10.0
```

### Kiali 仪表盘检查

```bash
# 端口转发 Kiali
kubectl port-forward svc/kiali -n istio-system 20001:20001 &

# 通过 API 验证网格健康状况
curl -s http://localhost:20001/kiali/api/namespaces/ai-inference/health | jq .

# 检查代理同步状态
istioctl proxy-status -n ai-inference

# 调试某个特定 pod 的 sidecar 配置
istioctl proxy-config routes deploy/model-server -n ai-inference -o json
istioctl proxy-config cluster deploy/model-server -n ai-inference
```

## 应避免的坑

- 激进的超时设置会破坏流式响应——为生成端点设置 300 秒以上的超时
- 一刀切的重试会放大开销高昂的生成调用——对非幂等路由禁用重试
- 面向租户和内部服务之间缺少身份边界
- 忘记将健康检查和指标端口排除在严格 mTLS 之外
- 在规模较小的连接池上将异常值剔除设置得过于激进（maxEjectionPercent 过高）
- 不使用 `holdApplicationUntilProxyStarts` 会导致启动时的竞态条件

## 相关技能

- service-mesh（`service-mesh`）——基础网格概念
- llm-gateway（`llm-gateway`）——南北向 API 网关控制
- opentelemetry（`opentelemetry`）——端到端追踪与指标

## 何时使用

- 当你正在为本技能所涵盖的基础设施组件（服务器、存储、数据库、网络、云、本地 AI）进行配置、设置或故障排查时。

## 局限性

- 基础设施命令可能会中断服务：在变更状态之前，确认目标主机/范围，并确保有备份/快照。
- 仅为文档导入：未附带上游脚本和模板。
</content>
