---
name: asset-inventory
description: 维护 IT 资产清单和配置管理数据库。跟踪硬件、软件和云资源。用于管理 IT 资产时使用。
category: security
risk: safe
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: 仅为清单和框架指导；不需要特权工具。通过你自己的变更流程落实控制项。
metadata:
  author: devops-skills
  version: '1.0'
---

# Asset Inventory（资产清单）

通过自动化发现、AWS Config 规则、云资产发现脚本、CMDB 集成和标签强制执行，维护全面的 IT 资产清单，以实现合规性和运营可见性。

## 资产分类与模式

```yaml
asset_categories:
  compute:
    cloud:
      - EC2 instances / Azure VMs / GCE instances
      - Lambda functions / Azure Functions / Cloud Functions
      - ECS/EKS clusters and tasks
      - Container images in registries
    on_premise:
      - Physical servers
      - Virtual machines (VMware, Hyper-V)

  storage:
    - S3 buckets / Azure Storage / GCS buckets
    - EBS volumes / Managed Disks / Persistent Disks
    - RDS instances / Azure SQL / Cloud SQL
    - DynamoDB tables / Cosmos DB / Firestore
    - EFS / Azure Files / Filestore

  network:
    - VPCs / VNets / VPC Networks
    - Load balancers (ALB, NLB, Azure LB, GCP LB)
    - DNS zones and records
    - VPN gateways and connections
    - CDN distributions

  security:
    - IAM users, roles, and policies
    - KMS keys / Key Vault keys
    - Certificates (ACM, Key Vault, Certificate Manager)
    - Security groups / NSGs / Firewall rules
    - WAF configurations

  applications:
    - SaaS subscriptions
    - Licensed software
    - Custom applications
    - APIs and integrations

  endpoints:
    - Laptops and desktops
    - Mobile devices
    - Printers and peripherals

asset_record_schema:
  required_fields:
    asset_id: "Unique identifier (auto-generated)"
    name: "Human-readable name"
    type: "Category from above taxonomy"
    provider: "AWS / Azure / GCP / On-Premise / SaaS"
    account_or_subscription: "Cloud account ID"
    region: "Deployment region/location"
    owner: "Team or individual responsible"
    data_classification: "Public / Internal / Confidential / Restricted"
    environment: "Production / Staging / Development / Sandbox"
    status: "Active / Decommissioning / Retired"
    created_date: "When the asset was provisioned"
    last_seen: "Last automated discovery timestamp"

  optional_fields:
    cost_center: "For cost allocation"
    compliance_scope: "SOC2 / HIPAA / PCI / None"
    backup_policy: "Backup schedule reference"
    dr_tier: "Critical / Essential / Standard / Non-essential"
    expiration_date: "For time-limited resources"
    tags: "Key-value pairs from cloud provider"
    dependencies: "Upstream and downstream services"
```

## AWS 资源发现脚本

```bash
#!/usr/bin/env bash
# aws-asset-discovery.sh - 发现并清点所有 AWS 资源

OUTPUT_DIR="./asset-inventory/aws/$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "=== AWS Asset Discovery for Account $ACCOUNT_ID ==="

# EC2 实例
echo "--- EC2 Instances ---"
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].{
    InstanceId:InstanceId,
    Type:InstanceType,
    State:State.Name,
    AZ:Placement.AvailabilityZone,
    VpcId:VpcId,
    PrivateIP:PrivateIpAddress,
    PublicIP:PublicIpAddress,
    LaunchTime:LaunchTime,
    Name:Tags[?Key==`Name`].Value|[0],
    Owner:Tags[?Key==`Owner`].Value|[0],
    Environment:Tags[?Key==`Environment`].Value|[0]
  }' --output json | jq 'flatten' > "$OUTPUT_DIR/ec2-instances.json"

# RDS 数据库
echo "--- RDS Instances ---"
aws rds describe-db-instances \
  --query 'DBInstances[*].{
    DBInstanceId:DBInstanceIdentifier,
    Engine:Engine,
    EngineVersion:EngineVersion,
    Class:DBInstanceClass,
    Status:DBInstanceStatus,
    MultiAZ:MultiAZ,
    Encrypted:StorageEncrypted,
    Endpoint:Endpoint.Address,
    BackupRetention:BackupRetentionPeriod
  }' --output json > "$OUTPUT_DIR/rds-instances.json"

# S3 桶
echo "--- S3 Buckets ---"
aws s3api list-buckets --query 'Buckets[*].{Name:Name,Created:CreationDate}' --output json | \
  jq -c '.[]' | while read -r bucket; do
    name=$(echo "$bucket" | jq -r '.Name')
    region=$(aws s3api get-bucket-location --bucket "$name" --query 'LocationConstraint' --output text 2>/dev/null)
    encryption=$(aws s3api get-bucket-encryption --bucket "$name" 2>/dev/null | jq -r '.ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm' 2>/dev/null)
    versioning=$(aws s3api get-bucket-versioning --bucket "$name" --query 'Status' --output text 2>/dev/null)
    echo "{\"Name\":\"$name\",\"Region\":\"${region:-us-east-1}\",\"Encryption\":\"${encryption:-none}\",\"Versioning\":\"${versioning:-Disabled}\"}"
  done | jq -s '.' > "$OUTPUT_DIR/s3-buckets.json"

# Lambda 函数
echo "--- Lambda Functions ---"
aws lambda list-functions \
  --query 'Functions[*].{
    Name:FunctionName,
    Runtime:Runtime,
    MemorySize:MemorySize,
    Timeout:Timeout,
    LastModified:LastModified,
    CodeSize:CodeSize
  }' --output json > "$OUTPUT_DIR/lambda-functions.json"

# VPC 和安全组
echo "--- VPCs ---"
aws ec2 describe-vpcs \
  --query 'Vpcs[*].{
    VpcId:VpcId,
    CidrBlock:CidrBlock,
    State:State,
    IsDefault:IsDefault,
    Name:Tags[?Key==`Name`].Value|[0]
  }' --output json > "$OUTPUT_DIR/vpcs.json"

echo "--- Security Groups ---"
aws ec2 describe-security-groups \
  --query 'SecurityGroups[*].{
    GroupId:GroupId,
    GroupName:GroupName,
    VpcId:VpcId,
    Description:Description,
    IngressRuleCount:length(IpPermissions),
    EgressRuleCount:length(IpPermissionsEgress)
  }' --output json > "$OUTPUT_DIR/security-groups.json"

# IAM 用户和角色
echo "--- IAM Users ---"
aws iam list-users \
  --query 'Users[*].{UserName:UserName,Created:CreateDate,PasswordLastUsed:PasswordLastUsed}' \
  --output json > "$OUTPUT_DIR/iam-users.json"

echo "--- IAM Roles ---"
aws iam list-roles \
  --query 'Roles[*].{RoleName:RoleName,Created:CreateDate,LastUsed:RoleLastUsed.LastUsedDate}' \
  --output json > "$OUTPUT_DIR/iam-roles.json"

# EKS 集群
echo "--- EKS Clusters ---"
aws eks list-clusters --query 'clusters' --output json | jq -r '.[]' | while read -r cluster; do
  aws eks describe-cluster --name "$cluster" \
    --query 'cluster.{Name:name,Version:version,Status:status,Endpoint:endpoint,Created:createdAt}'
done | jq -s '.' > "$OUTPUT_DIR/eks-clusters.json" 2>/dev/null

# KMS 密钥
echo "--- KMS Keys ---"
aws kms list-keys --query 'Keys[*].KeyId' --output text | tr '\t' '\n' | while read -r key_id; do
  aws kms describe-key --key-id "$key_id" \
    --query 'KeyMetadata.{KeyId:KeyId,Description:Description,State:KeyState,Created:CreationDate,Manager:KeyManager}' 2>/dev/null
done | jq -s '.' > "$OUTPUT_DIR/kms-keys.json"

# 生成汇总
echo "=== Inventory Summary ==="
echo "EC2 Instances: $(jq 'length' "$OUTPUT_DIR/ec2-instances.json")"
echo "RDS Instances: $(jq 'length' "$OUTPUT_DIR/rds-instances.json")"
echo "S3 Buckets: $(jq 'length' "$OUTPUT_DIR/s3-buckets.json")"
echo "Lambda Functions: $(jq 'length' "$OUTPUT_DIR/lambda-functions.json")"
echo "VPCs: $(jq 'length' "$OUTPUT_DIR/vpcs.json")"
echo "Security Groups: $(jq 'length' "$OUTPUT_DIR/security-groups.json")"
echo "IAM Users: $(jq 'length' "$OUTPUT_DIR/iam-users.json")"
echo "IAM Roles: $(jq 'length' "$OUTPUT_DIR/iam-roles.json")"

echo "Inventory saved to $OUTPUT_DIR"
```

## 用于清单合规的 AWS Config 规则

```bash
# 启用 AWS Config 记录器
aws configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::123456789012:role/aws-config-role \
  --recording-group allSupported=true,includeGlobalResourceTypes=true

# 开始记录
aws configservice start-configuration-recorder --configuration-recorder-name default

# 启用 required-tags Config 规则
aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "required-tags",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "REQUIRED_TAGS"
  },
  "InputParameters": "{\"tag1Key\":\"Owner\",\"tag2Key\":\"Environment\",\"tag3Key\":\"CostCenter\",\"tag4Key\":\"DataClassification\"}",
  "Scope": {
    "ComplianceResourceTypes": [
      "AWS::EC2::Instance",
      "AWS::RDS::DBInstance",
      "AWS::S3::Bucket",
      "AWS::Lambda::Function"
    ]
  }
}'

# 加密合规的 Config 规则
aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "encrypted-volumes",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "ENCRYPTED_VOLUMES"
  }
}'

aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "rds-storage-encrypted",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "RDS_STORAGE_ENCRYPTED"
  }
}'

aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "s3-bucket-server-side-encryption-enabled",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED"
  }
}'

# 查询 AWS Config 中某类型的所有资源
aws configservice list-discovered-resources --resource-type AWS::EC2::Instance
aws configservice list-discovered-resources --resource-type AWS::RDS::DBInstance

# 使用 AWS Config SQL 进行高级查询
aws configservice select-resource-config \
  --expression "SELECT resourceId, resourceType, tags, configuration.instanceType
                WHERE resourceType = 'AWS::EC2::Instance'
                AND tags.tag('Environment') = 'production'"

# 获取合规汇总
aws configservice get-compliance-summary-by-config-rule
aws configservice get-compliance-summary-by-resource-type
```

## 标签强制执行

```yaml
# AWS 标签策略（通过 AWS Organizations 应用）
tag_policy:
  tags:
    Owner:
      tag_key:
        "@@assign": "Owner"
      enforced_for:
        "@@assign":
          - "ec2:instance"
          - "rds:db"
          - "s3:bucket"
          - "lambda:function"

    Environment:
      tag_key:
        "@@assign": "Environment"
      tag_value:
        "@@assign":
          - "production"
          - "staging"
          - "development"
          - "sandbox"

    DataClassification:
      tag_key:
        "@@assign": "DataClassification"
      tag_value:
        "@@assign":
          - "public"
          - "internal"
          - "confidential"
          - "restricted"

    CostCenter:
      tag_key:
        "@@assign": "CostCenter"
```

```hcl
# Terraform - 通过 default_tags 对所有资源强制打标签
provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      ManagedBy          = "terraform"
      Environment        = var.environment
      Owner              = var.team_name
      CostCenter         = var.cost_center
      DataClassification = var.data_classification
    }
  }
}
```

## 多云发现

```bash
#!/usr/bin/env bash
# multi-cloud-discovery.sh - 发现 AWS、Azure 和 GCP 中的资产

OUTPUT_DIR="./asset-inventory/multi-cloud/$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

echo "=== Multi-Cloud Asset Discovery ==="

# AWS - 使用 Resource Groups Tagging API
echo "--- AWS Resources ---"
aws resourcegroupstaggingapi get-resources \
  --query 'ResourceTagMappingList[*].{ARN:ResourceARN,Tags:Tags}' \
  --output json > "$OUTPUT_DIR/aws-all-resources.json"
echo "AWS resources: $(jq 'length' "$OUTPUT_DIR/aws-all-resources.json")"

# Azure - 使用 Resource Graph
echo "--- Azure Resources ---"
az graph query -q "Resources | project name, type, location, resourceGroup, subscriptionId, tags" \
  --output json > "$OUTPUT_DIR/azure-all-resources.json" 2>/dev/null

# GCP - 使用 Cloud Asset Inventory
echo "--- GCP Resources ---"
gcloud asset search-all-resources \
  --scope="organizations/ORG_ID" \
  --format=json > "$OUTPUT_DIR/gcp-all-resources.json" 2>/dev/null

# 查找未打标签的资源
echo "=== Untagged Resources ==="
jq '[.[] | select(.Tags == null or .Tags == [])] | length' "$OUTPUT_DIR/aws-all-resources.json"

echo "Discovery complete. Results in $OUTPUT_DIR"
```


## 目录

- [CMDB 集成](references/details.md)
- [资产清单检查清单](references/details.md)
- [最佳实践](references/details.md)

## 何时使用

- 为合规框架（ISO 27001、SOC 2、FedRAMP）构建或维护 IT 资产清单
- 在多个账户和区域中实施自动化云资源发现
- 强制执行标签标准,用于成本分配、归属和数据分类
- 将资产数据与 CMDB 集成以支持运营工作流
- 为需要完整系统组件清单的审计做准备

## 局限性

- 仅为指导和检查清单；非法律意见，也不能替代合格审计师。
- 仅导入文档：未附带上游模板和脚本。

### 示例

```markdown
将本技能的控制检查清单映射到我们当前的证据,并列出差距。
```

> 改编自 [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills)（MIT 许可）；为符合上游合规要求，添加了 frontmatter、"何时使用/局限性"以及安全边界内容。仅导入文档：未附带辅助脚本和模板。

