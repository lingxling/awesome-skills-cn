---
name: container-hardening
description: 保护 Docker 镜像和容器运行时配置。
category: security
risk: critical
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: 需要相关的安全工具（扫描程序、vault CLI）和任何活跃评估的授权范围。仅文档；辅助脚本和模板不包含。
metadata:
  author: devops-skills
  version: '1.0'
---

# 容器加固

保护容器镜像和运行时配置。

## 何时使用此技能

在以下情况下使用此技能：
- 构建安全的容器镜像
- 加固容器部署
- 满足容器安全要求
- 实施深度防御

## Dockerfile 安全

```dockerfile
# 使用最小基础镜像
FROM alpine:3.18

# 不要以 root 身份运行
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# 复制具有特定所有权的文件
COPY --chown=appuser:appgroup . /app

# 删除不必要的包
RUN apk del --purge build-dependencies && \
    rm -rf /var/cache/apk/*

# 使用非 root 用户
USER appuser

# 只读文件系统支持
WORKDIR /app
```

## 运行时安全

```bash
# 使用安全选项运行
docker run -d \
  --read-only \
  --tmpfs /tmp \
  --security-opt=no-new-privileges:true \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --user 1001:1001 \
  myapp:latest
```

## Kubernetes 安全上下文

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    fsGroup: 1001
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
```

## 镜像扫描

```bash
# 使用 Trivy 扫描
trivy image --severity HIGH,CRITICAL myapp:latest

# 使用 distroless 镜像
FROM gcr.io/distroless/static-debian11
```

## 最佳实践

- 使用最小基础镜像
- 以非 root 用户身份运行
- 启用只读文件系统
- 删除所有功能
- 定期扫描镜像
- 签署并验证镜像
- 使用密钥管理

## 相关技能

- container-scanning (`container-scanning`) - 漏洞扫描
- kubernetes-hardening (`kubernetes-hardening`) - K8s 安全

## 限制

- 仅在授权范围内应用指导；在非生产环境中测试破坏性步骤。
- 仅文档导入：上游脚本和模板不包含。

### 示例

```bash
# 首先只读：在任何主动步骤之前进行清点。
which <tool> && <tool> --help | head -n 20
```

> 改编自 [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills)（MIT）；已添加前置元数据、何时使用/限制和安全边界以符合上游要求。仅文档导入：辅助脚本和模板不包含。
