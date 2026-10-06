---
name: hf-cloud-sagemaker-iam-preflight
description: '在部署或训练之前，确保存在一个可用的 SageMaker 执行角色（execution role）。每当即将创建一个 SageMaker 端点、模型、训练任务，或任何需要执行角色的资源时使用本技能。尤其是在用户没有明确提供角色 ARN 时、脚本即将调用 `iam:CreateRole` 时，或某个 AccessDenied 错误提到了某个 IAM 操作时使用。永远不要盲目调用 `iam:CreateRole` —— 始终先检查是否已存在角色。本技能可以防止最常见的 SageMaker 部署失败：试图从一个没有 IAM 写权限的 SSO 主体创建 IAM 资源。'
---

# SageMaker IAM 预检（Preflight）

每一个 SageMaker 资源都需要一个**执行角色（execution role）**——即 SageMaker 用来从 S3 读取模型工件、从 ECR 拉取服务容器,并写入日志所假设（assume）的 IAM 角色。大多数部署都在这一步失败，因为脚本试图创建一个新角色却没有先检查是否已有可用的角色，结果因为调用者是一个 SSO 主体而报错崩溃。

本技能编码了正确的顺序：先发现、再验证、只有在必要时才创建。

## 运行辅助脚本（跨平台）

这些辅助脚本是用 Python 写的，因此在 Windows、macOS 和 Linux 上运行方式完全相同：

```bash
python3 scripts/check_role.py        # macOS / Linux
python  scripts/check_role.py        # Windows (PowerShell / cmd)
```

**应在 AWS CLI 已经能正常工作的那个 shell 中运行它们** —— 也就是任何能让 `aws sts get-caller-identity` 成功执行的环境。该脚本会调用同一个 `aws` 二进制程序，并继承该 shell 的 profile、区域、SSO 会话、代理和凭证链。

> **Windows / WSL / Git Bash 的注意事项。** 在 Windows 上，**不要**通过 Bash 模拟层（WSL、Git Bash、MSYS）来调用这些脚本。这些 Bash 环境通常**不会**共享 Windows 的 AWS 配置、凭证、SSO 会话、环境变量或代理设置 —— 所以即使 `aws sts get-caller-identity` 在 PowerShell 中原生可以正常工作，它在 Bash 内部也会失败。（这正是旧版 `.sh` 辅助脚本在 Windows 上失败,而被替换为 Python 版本的原因。）如果你在 PowerShell 中，就直接在 PowerShell 里运行 `python ...\check_role.py`。如果该辅助脚本仍然无法识别你的身份，请在能让 `aws sts get-caller-identity` 返回你的 ARN 的那个 shell 中，原生地执行相同的发现流程（见下文的"原生 AWS CLI 等效方案"）。

## 操作顺序

### 第一步 —— 用户是否提供了一个角色？

专门验证那一个角色：

```bash
python3 scripts/check_role.py "<role-name-or-arn>"
```

成功时，它会将 ARN 打印到 stdout（退出码 0）。失败时，它会在 stderr 上记录原因。不要试图默默地修复一个有问题的角色 —— 要把问题暴露出来。

### 第二步 —— 发现现有的角色

```bash
python3 scripts/check_role.py
```

列出匹配常见 SageMaker 模式的角色（`AmazonSageMaker-ExecutionRole-*`、`SageMakerExecutionRole*` 等），**按最后使用日期排序**（最近的排在前面），按该顺序验证信任策略，返回第一个可用的 ARN。大多数曾经用过 SageMaker 的账户已经有这样的角色。

为什么按最后使用日期排序：在有多个角色的账户中（2021 年自动生成的角色 + 手动创建的项目角色 + 其他等等），按字母顺序排第一的角色很少是当前正在积极维护的那一个。最近使用过的角色更可能拥有最新的策略 —— 包括跨账户 ECR 拉取权限。该脚本会打印出排序结果，以便你能看到选中了哪一个。

IAM 经常会**完全不**报告 `RoleLastUsed`（跟踪机制只覆盖近期活动）。当所有候选角色在"从未使用过"上打成平手时，脚本会回退到**最新的创建日期** —— 一个较新的角色比 2021 年遗留下来的角色更可能拥有当前的策略。

### 第三步 —— 只有在发现阶段一无所获时才创建

**如果用户可以创建**（拥有 IAM 权限）：

```bash
python3 scripts/create_role.py "<role-name>" "<model-bucket>"
```

第二个参数将 S3 访问范围限定到特定的桶（bucket）。如果未知可以省略；脚本会发出警告，用户可以之后再更新策略。

**如果用户不能创建**（SSO 主体 —— `hf-cloud-aws-context-discovery` 会标记出这一点）：

应停下来并明确地指出这一点。不要去反复尝试其他 IAM 操作并期望其中一个能成功：

> 我找不到现有的 SageMaker 执行角色，而且你是通过 SSO 认证的，所以无法直接创建一个。请选择以下方式之一：
>   - 向你的 AWS 管理员申请一个 SageMaker 执行角色的 ARN，或者
>   - 让他们为你的 SSO 权限集授予 `iam:CreateRole`、`iam:PutRolePolicy` 权限

具体的说明能让问题快速解决；模糊的"权限被拒绝"消息则不能。

## "已验证"的含义

一个角色是可用的，当（1）它存在，（2）它的信任策略允许 `sagemaker.amazonaws.com` 执行 `sts:AssumeRole`，并且（3）它的权限仅授予本次部署所需的操作和资源。规范的信任策略见 `references/trust-policy.json`。

`check_role.py` 会验证角色的存在性和信任关系，因为策略评估取决于本次部署确切的 S3、ECR、日志记录,以及可选输出资源。在部署之前，应检查所选角色的策略，并将其与 `references/minimum-permissions.json` 进行比较；只添加缺失的操作，并将其范围限定在所需的资源上。不要附加 `AmazonSageMakerFullAccess`，也不要把权限审查推迟到出现 `AccessDenied` 失败之后。

## 最小权限

`references/minimum-permissions.json` 是用于端点执行的独立内联策略：
- 针对模型工件桶的 `s3:GetObject` + `s3:ListBucket`
- ECR 拉取权限
- CloudWatch 日志和指标

`create_role.py` 会安装这个内联策略，而不附加任何托管的 FullAccess 策略。将模板中的 `REPLACE_WITH_MODEL_BUCKET` 替换为实际的桶名称 —— 当将桶作为第二个参数提供给 `create_role.py` 时，它会自动完成这一替换。对于可选功能（例如异步输出或数据捕获），应单独添加范围狭窄的权限。

## 原生 AWS CLI 等效方案（备用方案）

如果 Python 辅助脚本无法运行，或无法识别你的身份（这种情况很少见 —— 通常是 PATH 配置有问题，或者运行在一个缺少 AWS 上下文的 Bash 模拟层中），可以在能让 `aws sts get-caller-identity` 正常工作的那个 shell 中手动执行同样的预检流程。其逻辑本质上就是一些 AWS CLI 调用；这个辅助脚本的存在只是为了把它们打包并排序。

PowerShell：

```powershell
# 1. 列出候选的 SageMaker 角色
aws iam list-roles --query "Roles[?contains(RoleName,'SageMaker') || contains(RoleName,'sagemaker')]" --output json

# 2. 对每个候选角色，确认其信任策略允许 sagemaker.amazonaws.com
aws iam get-role --role-name <role-name> --query "Role.AssumeRolePolicyDocument" --output json

# 3. 优先选择最近使用过、且命名符合 SageMaker 执行角色规范的角色
#    （LastUsedDate 对每个角色往往都是 None —— 这种情况下优先选择最新的 CreateDate）
aws iam get-role --role-name <role-name> --query "Role.[RoleLastUsed.LastUsedDate, CreateDate]" --output text
```

选择信任策略中包含 `sagemaker.amazonaws.com`、且最近使用过的角色。将得到的 ARN 直接使用，就如同是 `check_role.py` 返回的一样。Bash/macOS/Linux 使用相同的命令。
