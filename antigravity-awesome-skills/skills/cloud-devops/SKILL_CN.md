---
name: cloud-devops
description: "云基础设施和 DevOps 工作流，涵盖 AWS、Azure、GCP、Kubernetes、Terraform、CI/CD、监控和云原生开发。"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# 云/DevOps 工作流束

## 概览

针对基础设施配置、容器编排、CI/CD 管道、监控和云原生应用开发的全面云和 DevOps 工作流。

## 何时使用此工作流

在以下情况下使用此工作流：
- 设置云基础设施
- 实现 CI/CD 管道
- 部署 Kubernetes 应用
- 配置监控和可观测性
- 管理云成本
- 实现 DevOps 实践

## 工作流阶段

### 阶段 1：云基础设施设置

#### 要调用的技能
- `cloud-architect` - 云架构
- `aws-skills` - AWS 开发
- `azure-functions` - Azure 开发
- `gcp-cloud-run` - GCP 开发
- `terraform-skill` - Terraform IaC
- `terraform-specialist` - 高级 Terraform

#### 操作
1. 设计云架构
2. 设置账户和计费
3. 配置网络
4. 配置资源
5. 设置 IAM

#### 复制粘贴提示
```
使用 @cloud-architect 设计多云架构
```

```
使用 @terraform-skill 配置 AWS 基础设施
```

### 阶段 2：容器编排

#### 要调用的技能
- `kubernetes-architect` - Kubernetes 架构
- `docker-expert` - Docker 容器化
- `helm-chart-scaffolding` - Helm 图表
- `k8s-manifest-generator` - K8s 清单
- `k8s-security-policies` - K8s 安全

#### 操作
1. 设计容器架构
2. 创建 Dockerfile
3. 构建容器镜像
4. 编写 K8s 清单
5. 部署到集群
6. 配置网络

#### 复制粘贴提示
```
使用 @kubernetes-architect 设计 K8s 架构
```

```
使用 @docker-expert 对应用容器化
```

```
使用 @helm-chart-scaffolding 创建 Helm 图表
```

### 阶段 3：CI/CD 实现

#### 要调用的技能
- `deployment-engineer` - 部署工程
- `cicd-automation-workflow-automate` - CI/CD 自动化
- `github-actions-templates` - GitHub Actions
- `gitlab-ci-patterns` - GitLab CI
- `deployment-pipeline-design` - 管道设计

#### 操作
1. 设计部署管道
2. 配置构建自动化
3. 设置测试自动化
4. 配置部署阶段
5. 实现回滚策略
6. 设置通知

#### 复制粘贴提示
```
使用 @cicd-automation-workflow-automate 设置 CI/CD 管道
```

```
使用 @github-actions-templates 创建 GitHub Actions 工作流
```

### 阶段 4：监控和可观测性

#### 要调用的技能
- `observability-engineer` - 可观测性工程
- `grafana-dashboards` - Grafana 仪表板
- `prometheus-configuration` - Prometheus 设置
- `datadog-automation` - Datadog 集成
- `sentry-automation` - Sentry 错误跟踪

#### 操作
1. 设计监控策略
2. 设置指标收集
3. 配置日志聚合
4. 实现分布式追踪
5. 创建仪表板
6. 设置警报

#### 复制粘贴提示
```
使用 @observability-engineer 设置可观测性堆栈
```

```
使用 @grafana-dashboards 创建监控仪表板
```

### 阶段 5：云安全

#### 要调用的技能
- `cloud-penetration-testing` - 云渗透测试
- `aws-penetration-testing` - AWS 安全
- `k8s-security-policies` - K8s 安全
- `secrets-management` - 密钥管理
- `mtls-configuration` - mTLS 设置

#### 操作
1. 评估云安全
2. 配置安全组
3. 设置密钥管理
4. 实现网络策略
5. 配置加密
6. 设置审计日志

#### 复制粘贴提示
```
使用 @cloud-penetration-testing 评估云安全
```

```
使用 @secrets-management 配置密钥
```

### 阶段 6：成本优化

#### 要调用的技能
- `cost-optimization` - 云成本优化
- `database-cloud-optimization-cost-optimize` - 数据库成本优化

#### 操作
1. 分析云支出
2. 识别优化机会
3. 调整资源大小
4. 实现自动扩展
5. 使用预留实例
6. 设置成本警报

#### 复制粘贴提示
```
使用 @cost-optimization 降低云成本
```

### 阶段 7：灾难恢复

#### 要调用的技能
- `incident-responder` - 事件响应
- `incident-runbook-templates` - 运行手册创建
- `postmortem-writing` - 事后分析文档

#### 操作
1. 设计 DR 策略
2. 设置备份
3. 创建运行手册
4. 测试故障转移
5. 文档化程序
6. 培训团队

#### 复制粘贴提示
```
使用 @incident-runbook-templates 创建运行手册
```

## 云提供者工作流

### AWS
```
技能：aws-skills, aws-serverless, aws-penetration-testing
服务：EC2, Lambda, S3, RDS, ECS, EKS
```

### Azure
```
技能：azure-functions, azure-ai-projects-py, azure-monitor-opentelemetry-py
服务：Functions, App Service, AKS, Cosmos DB
```

### GCP
```
技能：gcp-cloud-run
服务：Cloud Run, GKE, Cloud Functions, BigQuery
```

## 质量门槛

- [ ] 基础设施已配置
- [ ] CI/CD 管道工作正常
- [ ] 监控已配置
- [ ] 安全措施已到位
- [ ] 成本优化已应用
- [ ] DR 程序已文档化

## 相关工作流束

- `development` - 应用开发
- `security-audit` - 安全测试
- `database` - 数据库操作
- `testing-qa` - 测试工作流

## 限制
- 仅在任务与上述范围匹配时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果需要的输入、权限、安全边界或成功标准缺失，请停止并寻求澄清。
