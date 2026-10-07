---
name: aws-security-audit
description: "使用 AWS CLI 和安全最佳实践的全面 AWS 安全态势评估"
category: security
risk: safe
source: community
tags: "[aws, security, audit, compliance, kiro-cli, security-assessment]"
date_added: "2026-02-27"
---

# AWS 安全审计

执行 AWS 环境的全面安全评估以识别漏洞和配置错误。

## 何时使用
当您需要审计 AWS 安全态势、识别漏洞或准备合规性评估时，使用此技能。

## 审计类别

**身份和访问管理**
- 过度宽松的 IAM 策略
- 未使用的 IAM 用户和角色
- MFA 实施缺口
- 根账户使用
- 访问密钥轮换

**网络安全**
- 开放的安全组 (0.0.0.0/0)
- 公开 S3 存储桶
- 未加密的传输中数据
- VPC 流日志已禁用
- 网络 ACL 配置错误

**数据保护**
- 未加密的 EBS 卷
- 未加密的 RDS 实例
- S3 存储桶加密已禁用
- 备份策略缺失
- KMS 密钥轮换已禁用

**日志和监控**
- CloudTrail 已禁用
- CloudWatch 警报缺失
- VPC 流日志已禁用
- S3 访问日志已禁用
- Config 记录已禁用

## 安全审计命令

### IAM 安全检查

```bash
# 列出没有 MFA 的用户
aws iam get-credential-report --output text | \
  awk -F, '$4=="false" && $1!="<root_account>" {print $1}'

# 查找未使用的 IAM 用户 (90 天内无活动)
aws iam list-users --query 'Users[*].[UserName]' --output text | \
while read user; do
  last_used=$(aws iam get-user --user-name "$user" \
    --query 'User.PasswordLastUsed' --output text)
  echo "$user: $last_used"
done

# 列出过度宽松的策略 (AdministratorAccess)
aws iam list-policies --scope Local \
  --query 'Policies[?PolicyName==`AdministratorAccess`]'

# 查找超过 90 天的访问密钥
aws iam list-users --query 'Users[*].UserName' --output text | \
while read user; do
  aws iam list-access-keys --user-name "$user" \
    --query 'AccessKeyMetadata[*].[AccessKeyId,CreateDate]' \
    --output text
done

# 检查根账户访问密钥
aws iam get-account-summary \
  --query 'SummaryMap.AccountAccessKeysPresent'
```

### 网络安全检查

```bash
# 查找对世界开放的安全组
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' \
  --output table

# 列出公开 S3 存储桶
aws s3api list-buckets --query 'Buckets[*].Name' --output text | \
while read bucket; do
  acl=$(aws s3api get-bucket-acl --bucket "$bucket" 2>/dev/null)
  if echo "$acl" | grep -q "AllUsers"; then
    echo "PUBLIC: $bucket"
  fi
done

# 检查 VPC 流日志状态
aws ec2 describe-vpcs --query 'Vpcs[*].VpcId' --output text | \
while read vpc; do
  flow_logs=$(aws ec2 describe-flow-logs \
    --filter "Name=resource-id,Values=$vpc" \
    --query 'FlowLogs[*].FlowLogId' --output text)
  if [ -z "$flow_logs" ]; then
    echo "No flow logs: $vpc"
  fi
done

# 查找没有加密的 RDS 实例
aws rds describe-db-instances \
  --query 'DBInstances[?StorageEncrypted==`false`].[DBInstanceIdentifier]' \
  --output table
```

### 数据保护检查

```bash
# 查找未加密的 EBS 卷
aws ec2 describe-volumes \
  --query 'Volumes[?Encrypted==`false`].[VolumeId,Size,State]' \
  --output table

# 检查 S3 存储桶加密
aws s3api list-buckets --query 'Buckets[*].Name' --output text | \
while read bucket; do
  encryption=$(aws s3api get-bucket-encryption \
    --bucket "$bucket" 2>&1)
  if echo "$encryption" | grep -q "ServerSideEncryptionConfigurationNotFoundError"; then
    echo "No encryption: $bucket"
  fi
done

# 查找公开的 RDS 快照
aws rds describe-db-snapshots \
  --query 'DBSnapshots[*].[DBSnapshotIdentifier]' --output text | \
while read snapshot; do
  attrs=$(aws rds describe-db-snapshot-attributes \
    --db-snapshot-identifier "$snapshot" \
    --query 'DBSnapshotAttributesResult.DBSnapshotAttributes[?AttributeName==`restore`].AttributeValues' \
    --output text)
  if echo "$attrs" | grep -q "all"; then
    echo "PUBLIC SNAPSHOT: $snapshot"
  fi
done

# 检查 KMS 密钥轮换
aws kms list-keys --query 'Keys[*].KeyId' --output text | \
while read key; do
  rotation=$(aws kms get-key-rotation-status --key-id "$key" \
    --query 'KeyRotationEnabled' --output text 2>/dev/null)
  if [ "$rotation" = "False" ]; then
    echo "Rotation disabled: $key"
  fi
done
```

### 日志和监控检查

```bash
# 检查 CloudTrail 状态
aws cloudtrail describe-trails \
  --query 'trailList[*].[Name,IsMultiRegionTrail,LogFileValidationEnabled]' \
  --output table

# 验证 CloudTrail 是否记录
aws cloudtrail get-trail-status --name my-trail \
  --query 'IsLogging'

# 检查 AWS Config 是否启用
aws configservice describe-configuration-recorders \
  --query 'ConfigurationRecorders[*].[name,roleARN]' \
  --output table

# 列出没有访问日志的 S3 存储桶
aws s3api list-buckets --query 'Buckets[*].Name' --output text | \
while read bucket; do
  logging=$(aws s3api get-bucket-logging --bucket "$bucket" 2>&1)
  if ! echo "$logging" | grep -q "LoggingEnabled"; then
    echo "No access logging: $bucket"
  fi
done
```

## 自动化安全审计脚本

```bash
#!/bin/bash
# comprehensive-security-audit.sh

echo "=== AWS 安全审计报告 ==="
echo "生成时间: $(date)"
echo ""

# IAM 检查
echo "## IAM 安全"
echo "没有 MFA 的用户："
aws iam get-credential-report --output text | \
  awk -F, '$4=="false" && $1!="<root_account>" {print "  - " $1}'

echo ""
echo "根账户访问密钥："
aws iam get-account-summary \
  --query 'SummaryMap.AccountAccessKeysPresent' --output text

# 网络检查
echo ""
echo "## 网络安全"
echo "对 0.0.0.0/0 开放的安全组："
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].GroupId' \
  --output text | wc -l

# 数据保护
echo ""
echo "## 数据保护"
echo "未加密的 EBS 卷："
aws ec2 describe-volumes \
  --query 'Volumes[?Encrypted==`false`].VolumeId' \
  --output text | wc -l

echo ""
echo "未加密的 RDS 实例："
aws rds describe-db-instances \
  --query 'DBInstances[?StorageEncrypted==`false`].DBInstanceIdentifier' \
  --output text | wc -l

# 日志
echo ""
echo "## 日志和监控"
echo "CloudTrail 状态："
aws cloudtrail describe-trails \
  --query 'trailList[*].[Name,IsLogging]' \
  --output table

echo ""
echo "=== 报告结束 ==="
```

## 安全分数计算器

```python
#!/usr/bin/env python3
# security-score.py

import boto3
import json

def calculate_security_score():
    iam = boto3.client('iam')
    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')
    
    score = 100
    issues = []
    
    # 检查 MFA
    try:
        report = iam.get_credential_report()
        users_without_mfa = 0
        # 解析报告并计数
        if users_without_mfa > 0:
            score -= 10
            issues.append(f"{users_without_mfa} 个用户没有 MFA")
    except:
        pass
    
    # 检查开放的安全组
    sgs = ec2.describe_security_groups()
    open_sgs = 0
    for sg in sgs['SecurityGroups']:
        for perm in sg.get('IpPermissions', []):
            for ip_range in perm.get('IpRanges', []):
                if ip_range.get('CidrIp') == '0.0.0.0/0':
                    open_sgs += 1
                    break
    
    if open_sgs > 0:
        score -= 15
        issues.append(f"{open_sgs} 个安全组对互联网开放")
    
    # 检查未加密的卷
    volumes = ec2.describe_volumes()
    unencrypted = sum(1 for v in volumes['Volumes'] if not v['Encrypted'])
    
    if unencrypted > 0:
        score -= 20
        issues.append(f"{unencrypted} 个未加密的 EBS 卷")
    
    print(f"安全分数: {score}/100")
    print("\n发现的问题:")
    for issue in issues:
        print(f"  - {issue}")
    
    return score

if __name__ == "__main__":
    calculate_security_score()
```

## 合规性映射

**CIS AWS 基础基准**
- 1.1: 根账户使用
- 1.2-1.14: IAM 策略和 MFA
- 2.1-2.9: 日志 (CloudTrail、Config、VPC 流日志)
- 4.1-4.3: 监控和警报

**PCI-DSS**
- 要求 1: 网络安全控制
- 要求 2: 安全配置
- 要求 8: 访问控制和 MFA
- 要求 10: 日志和监控

**HIPAA**
- 访问控制 (IAM)
- 审计控制 (CloudTrail)
- 加密 (EBS、RDS、S3)
- 传输安全 (TLS/SSL)

## 补救优先级

**严重 (立即修复)**
- 根账户访问密钥
- 公开 RDS 快照
- 对 0.0.0.0/0 敏感端口开放的安全组
- CloudTrail 已禁用

**高 (在 7 天内修复)**
- 没有 MFA 的用户
- 静止数据未加密
- 缺少 VPC 流日志
- 过度宽松的 IAM 策略

**中 (在 30 天内修复)**
- 旧访问密钥 (>90 天)
- 缺少 S3 访问日志
- 未使用的 IAM 用户
- KMS 密钥轮换已禁用

## 示例提示

- "对我的 AWS 账户进行全面安全审计"
- "检查 IAM 安全问题"
- "查找所有未加密的资源"
- "生成安全合规报告"
- "计算我的 AWS 安全分数"

## 最佳实践

- 每周运行审计
- 使用 Lambda/EventBridge 自动化
- 将结果导出到 S3 以进行趋势分析
- 与 SIEM 工具集成
- 跟踪补救进度
- 用业务理由记录异常

## Kiro CLI 集成

```bash
kiro-cli chat "使用 aws-security-audit 来评估我的安全态势"
kiro-cli chat "使用 aws-security-audit 生成安全审计报告"
```

## 其他资源

- [AWS 安全最佳实践](https://aws.amazon.com/security/best-practices/)
- [CIS AWS 基础基准](https://www.cisecurity.org/benchmark/amazon_web_services)
- [AWS Security Hub](https://aws.amazon.com/security-hub/)

## 限制
- 仅当任务明确符合上述范围时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
