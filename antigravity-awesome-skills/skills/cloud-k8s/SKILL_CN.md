---
name: cloud-k8s
description: "授权的云、容器和 Kubernetes 安全评估：元数据 SSRF、IAM 错误配置、容器逃逸路径和集群 RBAC 审查。"
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ 仅授权使用**
> 此技能仅用于教育目的或授权的安全评估。
> 在使用此工具前，您必须获得系统所有者的明确书面许可。
> 滥用此工具是违法的，严格禁止。

> **强制确认门槛**
> 在运行任何探测、利用、改变、持久化、从目标提取数据或尝试凭据访问的命令前：
> 1. 要求用户说明确切的目标 URL、IP、账户或资源。
> 2. 要求用户确认书面授权和允许的范围。
> 3. 显示确切的命令并解释其预期效果。
> 4. 等待当前对话中的明确确认。
>
> 没有该确认，保持只读并仅提供防御性指导。优先选择沙箱、可弃用的 VM 或受控实验室。

# 云 / 容器 / Kubernetes 安全
## 何时使用

- 在批准的范围内评估云工作负载或 Kubernetes 集群安全。
- 审查 IAM/RBAC 配置以查找权限提升路径。


## 适用场景

- 云元数据 SSRF（169.254.169.254 / IMDS）
- IAM 过度权限、公开存储桶、错误安全组
- Docker/containerd 逃逸路径评估
- Kubernetes RBAC、Secrets、Admission、供应链镜像
- 容器镜像漏洞（可联动 `supply-chain-security/`）

## 工作流

### 阶段 1 — 身份与边界

```text
□ 当前身份：云 AK/SK、K8s SA、节点 SSH？
□ 范围：单账号 / 单 cluster / 单 namespace
□ 网络档：authorized_target_only
```

### 阶段 2 — 云控制面

```bash
# 示例（按厂商替换；MUST 在授权账号内）
aws sts get-caller-identity
aws s3 ls
# Azure / GCP 对应 identity 命令
```

```text
□ 公开桶 / 错误 ACL
□ 元数据：IMDSv1 vs v2；SSRF 链
□ 角色可扮演（PassRole）与横向
```

### 阶段 3 — 容器

```text
□ 是否 privileged / hostPath / hostNetwork
□ capabilities（SYS_ADMIN 等）
□ 可写宿主机路径 → 逃逸候选
□ 镜像历史与已知 CVE → Trivy
```

### 阶段 4 — Kubernetes

```bash
kubectl auth can-i --list
kubectl get pods,secrets,svc -A
kubectl get clusterrolebindings
```

```text
□ SA token 挂载与权限
□ 危险 admission webhook 缺失
□ etcd / dashboard 暴露
□ 网络策略是否默认放行
```

## 工具链

| 工具 | 用途 | 自举 |
|------|------|------|
| kubectl | 集群交互 | 手动 |
| trivy | 镜像/IaC | bootstrap `trivy` 若可用 |
| kube-bench / kubeaudit | CIS/配置 | 手动 |
| pacu / scoutsuite | 云审计（授权） | 手动 |
| nuclei | 已知云漏洞模板 | bootstrap nmap/nuclei 生态 |

## 参考

- `references/k8s-cloud-checklist.md`
- CTF 对照：`../../CTF-Sandbox-Orchestrator/competition-agent-cloud/`
- `../supply-chain-security/` `../pentest-tools/`

## 路由上下文

**上游**: MASTER R23  
**下游**: 拿到节点 shell → `attack-chain` / `windows-ad`；镜像漏洞 → supply-chain  
**MUST NOT**: 未授权扫公有云其他租户

## 任务完成自检

- [ ] 是否限定在授权账号/cluster？
- [ ] 发现是否含复现与影响？
- [ ] 是否避免破坏性操作？
- [ ] 报告 / journal？

## 限制

- 云提供者 API 调用可能会产生成本并触发警报；与所有者协调。
- 逃逸路径验证必须保留在可弃用的实验室集群内。

> 适配自 [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT)。
