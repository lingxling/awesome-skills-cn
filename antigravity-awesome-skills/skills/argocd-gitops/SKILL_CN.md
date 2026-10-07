---
name: argocd-gitops
description: 使用 ArgoCD 实现 Kubernetes 声明式部署的 GitOps。
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

# ArgoCD GitOps

使用 ArgoCD 为 Kubernetes 实现声明式持续交付。

## 何时使用此技能

在以下场景使用此技能:
- 为 Kubernetes 实现 GitOps 工作流
- 自动化从 Git 仓库进行部署
- 以声明式方式管理多个环境
- 实现渐进式交付策略
- 将集群状态与 Git 同步

## 前置条件

- 已安装 ArgoCD 的 Kubernetes 集群
- 已配置 kubectl
- 用于存放清单文件的 Git 仓库
- ArgoCD CLI(可选)

## 安装

```bash
# 创建命名空间
kubectl create namespace argocd

# 安装 ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 获取管理员密码
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d

# 端口转发以访问 UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# 使用 CLI 登录
argocd login localhost:8080
```

## 应用定义

### 基本应用

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/myapp-manifests.git
    targetRevision: main
    path: environments/production
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Helm 应用

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-helm
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/myapp-chart.git
    targetRevision: main
    path: charts/myapp
    helm:
      valueFiles:
        - values.yaml
        - values-production.yaml
      parameters:
        - name: replicaCount
          value: "3"
        - name: image.tag
          value: "2.0.0"
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Kustomize 应用

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-kustomize
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/myapp-manifests.git
    targetRevision: main
    path: overlays/production
    kustomize:
      images:
        - myapp=myregistry/myapp:2.0.0
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp
```

## 项目(Projects)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: myproject
  namespace: argocd
spec:
  description: My Project
  sourceRepos:
    - https://github.com/org/*
  destinations:
    - namespace: myapp-*
      server: https://kubernetes.default.svc
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
  namespaceResourceWhitelist:
    - group: '*'
      kind: '*'
  roles:
    - name: developer
      description: Developer role
      policies:
        - p, proj:myproject:developer, applications, get, myproject/*, allow
        - p, proj:myproject:developer, applications, sync, myproject/*, allow
      groups:
        - developers
```

## Application Sets

### Git 生成器

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-environments
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/org/myapp-manifests.git
        revision: main
        directories:
          - path: environments/*
  template:
    metadata:
      name: 'myapp-{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/myapp-manifests.git
        targetRevision: main
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: 'myapp-{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

### List 生成器

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-clusters
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - cluster: production
            url: https://prod-cluster.example.com
          - cluster: staging
            url: https://staging-cluster.example.com
  template:
    metadata:
      name: 'myapp-{{cluster}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/myapp-manifests.git
        targetRevision: main
        path: 'environments/{{cluster}}'
      destination:
        server: '{{url}}'
        namespace: myapp
```

### Matrix 生成器

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-matrix
  namespace: argocd
spec:
  generators:
    - matrix:
        generators:
          - git:
              repoURL: https://github.com/org/myapp-manifests.git
              revision: main
              directories:
                - path: apps/*
          - list:
              elements:
                - env: staging
                - env: production
  template:
    metadata:
      name: '{{path.basename}}-{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/myapp-manifests.git
        targetRevision: main
        path: '{{path}}/overlays/{{env}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}-{{env}}'
```

## 同步策略

### 自动同步

```yaml
syncPolicy:
  automated:
    prune: true          # 删除 Git 中不存在的资源
    selfHeal: true       # 还原手动改动
    allowEmpty: false    # 不同步空目录
  syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

### 同步波次(Sync Waves)

```yaml
# 在 Kubernetes 清单中
apiVersion: v1
kind: ConfigMap
metadata:
  name: myconfig
  annotations:
    argocd.argoproj.io/sync-wave: "-1"  # 先同步
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/sync-wave: "0"   # 后同步
```

### 同步钩子(Sync Hooks)

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: myapp:latest
          command: ["./migrate.sh"]
      restartPolicy: Never
```

## CLI 命令

```bash
# 列出应用
argocd app list

# 获取应用详情
argocd app get myapp

# 同步应用
argocd app sync myapp

# 强制同步(忽略差异)
argocd app sync myapp --force

# 查看差异
argocd app diff myapp

# 回滚
argocd app rollback myapp

# 删除应用
argocd app delete myapp

# 查看日志
argocd app logs myapp

# 硬刷新(清除缓存)
argocd app get myapp --hard-refresh
```

## 仓库配置

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: private-repo
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  url: https://github.com/org/private-repo.git
  username: git
  password: ghp_xxxx
---
# SSH 密钥
apiVersion: v1
kind: Secret
metadata:
  name: private-repo-ssh
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  url: git@github.com:org/private-repo.git
  sshPrivateKey: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    ...
    -----END OPENSSH PRIVATE KEY-----
```

## 通知

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token
  template.app-deployed: |
    message: Application {{.app.metadata.name}} is now {{.app.status.sync.status}}.
  trigger.on-deployed: |
    - when: app.status.operationState.phase in ['Succeeded']
      send: [app-deployed]
```

## 常见问题

### 问题: 同步失败并出现差异
**问题现象**: 资源显示有差异,但实际上是正确的
**解决方案**: 配置忽略差异

```yaml
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
```

### 问题: 无法访问仓库
**问题现象**: ArgoCD 无法克隆仓库
**解决方案**: 检查仓库密钥,验证 URL 和凭据

### 问题: 应用一直处于 OutOfSync 状态
**问题现象**: 应用始终无法变为已同步状态
**解决方案**: 检查资源状态,查看事件,验证清单文件

### 问题: 健康检查失败
**问题现象**: 应用显示健康状态为 degraded
**解决方案**: 检查自定义健康检查,验证探针配置

## 最佳实践

- 使用 ApplicationSet 实现多环境部署
- 使用同步波次实现有序部署
- 使用项目(project)隔离应用
- 为部署事件配置通知
- 使用项目实现适当的 RBAC
- 使用健康检查进行部署验证
- 启用自动清理(auto-pruning)以移除已删除的资源
- 将清单文件保存在专用仓库中

## 相关技能

- kubernetes-ops (`kubernetes-ops`) —— K8s 基础
- helm-charts (`helm-charts`) —— Helm 部署
- kustomize (`kustomize`) —— Kustomize overlay

## 局限性

- 本指导会对真实环境执行操作: 在应用任何变更之前,确认目标、影响范围和回滚计划。
- 未经明确批准,切勿部署到生产环境。仅为文档导入: 不包含上游脚本和模板。

### 示例

```bash
git status && git diff --stat
kubectl diff -f manifest.yaml
```

> 改编自 [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills)(MIT);为符合上游合规要求,添加了前言、何时使用/局限性以及安全边界内容。仅为文档导入: 不包含辅助脚本和模板。
