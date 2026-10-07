---
name: container-security-hardening
description: >
  使用安全基础镜像、非 root 用户、CVE 扫描、SBOM/签名、seccomp/AppArmor 和 Kubernetes pod 安全控制加固 Docker/容器镜像和运行时部署。用于 Dockerfile 安全审查、容器 CVE、镜像扫描、distroless 镜像或生产环境加固。
category: security
risk: safe
source: community
date_added: "2026-05-30"
---

# 容器安全加固技能

从 Dockerfile 编写到运行时强制执行和供应链完整性的生产级容器安全构建、扫描和运行指南。

---

## 详细指南

在执行此技能之前，请阅读 [详细指南](references/detailed-guide.md)。它保留了完整的程序和参考材料。将其安全、前置条件和验证要求视为强制性的。对于重点工作，加载相关部分；对于端到端工作，完全阅读指南。

## 何时使用此技能

- 用户提到 Docker 安全、容器加固或 Dockerfile 安全审查
- 用户询问关于 distroless 镜像、非 root 容器或只读文件系统
- 用户想使用 Trivy、Grype 或 Snyk 扫描镜像以查找 CVE
- 用户提到 seccomp、AppArmor、Linux 功能或运行时安全
- 用户问"我的 Dockerfile 是否安全？"或"我如何减少镜像的攻击面？"
- 用户想使用 Cosign 签署/验证镜像或生成 SBOM
- 用户询问关于 Kubernetes pod 安全、NetworkPolicy 或 RBAC 加固
- 用户说"修复容器 CVE"或"为生产环境加固容器"

## 何时不使用此技能

- 用户主要询问关于 GitHub Actions CI/CD → 推荐 `github-actions-advanced`
- 用户需要常规 Docker 使用帮助（不是安全）→ 推荐 `docker-expert`
- 用户在处理超出安全范围的 Kubernetes 编排 → 推荐 `kubernetes-architect`
- 用户需要应用级安全（SQL 注入、XSS）→ 推荐 `api-security-best-practices`

---

## 安全检查清单

### Dockerfile
- [ ] 最小基础镜像（distroless、slim 或 alpine — 不是完整的 debian/ubuntu）
- [ ] 多阶段构建 — 运行时镜像中没有构建工具、devDependencies 或编译器
- [ ] 在 `CMD`/`ENTRYPOINT` 之前声明了非 root `USER`
- [ ] 基础镜像固定到 `@sha256:...` 摘要（不仅仅是标签）
- [ ] `ENV`、`ARG` 或 `RUN` 命令中没有秘密
- [ ] 定义了 `HEALTHCHECK`
- [ ] 存在 OCI 标签（`org.opencontainers.image.*`）
- [ ] `.dockerignore` 排除了 `.git`、`.env`、秘密、测试
- [ ] `ENTRYPOINT` 使用 exec 形式，而不是 shell 形式

### 镜像扫描
- [ ] Trivy 或 Grype 在 CI 中扫描（在 HIGH/CRITICAL 时失败）
- [ ] Hadolint 无警告通过
- [ ] 在镜像上运行秘密扫描（`trivy --scanners secret`）
- [ ] SBOM 已生成并存储
- [ ] `.trivyignore` 对已接受的 CVE 有合理的条目

### 运行时
- [ ] `--read-only` 文件系统
- [ ] `--cap-drop ALL`（仅添加回文档记载为必需的内容）
- [ ] 应用了 `--security-opt no-new-privileges:true`
- [ ] 应用了 `--security-opt seccomp=<profile>`
- [ ] 设置了资源限制（`--memory`、`--cpus`、`--pids-limit`）
- [ ] 镜像使用 Cosign 签署；在部署前验证

### Kubernetes
- [ ] `readOnlyRootFilesystem: true`
- [ ] `allowPrivilegeEscalation: false`
- [ ] `runAsNonRoot: true` 及显式 UID
- [ ] `capabilities.drop: ["ALL"]`
- [ ] 定义了资源 `requests` 和 `limits`
- [ ] `automountServiceAccountToken: false`
- [ ] 命名空间 PSA 在 `restricted` 级别强制执行
- [ ] `NetworkPolicy` 默认拒绝已应用
- [ ] RBAC 使用特定资源名称和最小动词

---

## 限制

- 仅在任务清楚地符合上述范围时使用此技能。
- 不要将输出作为环境特定渗透测试或正式安全审计的替代品。
- Seccomp 配置文件和 AppArmor 仅限于 Linux；macOS/Windows Docker Desktop 使用不同的机制。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
