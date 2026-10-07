---
name: aws-cost-optimizer
description: "使用 AWS CLI 和 Cost Explorer 进行全面的 AWS 成本分析和优化建议"
risk: safe
source: community
date_added: "2026-02-27"
---

# AWS 成本优化器

分析 AWS 支出模式，识别浪费，并提供可操作的成本降低策略。

## 何时使用此技能

当需要分析 AWS 支出、识别成本优化机会或减少云浪费时使用此技能。

## 核心功能

**成本分析**
- 分析 AWS Cost Explorer 数据中的趋势和异常
- 按服务、区域和资源标签分解成本
- 识别月度支出增长

**资源优化**
- 检测空闲 EC2 实例（低 CPU 利用率）
- 查找未连接的 EBS 卷和旧快照
- 识别未使用的弹性 IP
- 定位利用不足的 RDS 实例
- 查找符合生命周期策略条件的旧 S3 对象

**节省建议**
- 建议 Reserved Instance/Savings Plans 机会
- 基于 CloudWatch 指标推荐实例大小调整
- 识别昂贵区域中的资源
- 计算具体操作的潜在节省

## AWS CLI 命令

### 获取成本和使用情况
```bash
# 过去 30 天的按服务分类的成本
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

# 当前月份的每日成本
aws ce get-cost-and-usage \
  --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics UnblendedCost
```

### 查找未使用的资源
```bash
# 未连接的 EBS 卷
aws ec2 describe-volumes \
  --filters Name=status,Values=available \
  --query 'Volumes[*].[VolumeId,Size,VolumeType,CreateTime]' \
  --output table

# 未使用的弹性 IP
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].[PublicIp,AllocationId]' \
  --output table

# 空闲 EC2 实例（需要 CloudWatch）
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average

# 旧 EBS 快照（>90 天）
aws ec2 describe-snapshots \
  --owner-ids self \
  --query 'Snapshots[?StartTime<=`'$(date -d '90 days ago' --iso-8601)'`].[SnapshotId,StartTime,VolumeSize]' \
  --output table
```

### 大小调整分析
```bash
# 列出具有其类型的 EC2 实例
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# 获取 RDS 实例利用率
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=mydb \
  --start-time $(date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 86400 \
  --statistics Average,Maximum
```

## 优化工作流

1. **基线评估**
   - 拉取 3-6 个月的成本数据
   - 识别前 5 个支出服务
   - 计算增长率

2. **快速获胜**
   - 删除未连接的 EBS 卷
   - 释放未使用的弹性 IP
   - 停止/终止空闲 EC2 实例
   - 删除旧快照

3. **战略优化**
   - 分析 Reserved Instance 覆盖范围
   - 审查实例类型与工作负载
   - 实施 S3 生命周期策略
   - 考虑非关键工作负载的 Spot 实例

4. **持续监控**
   - 使用警报设置 AWS Budgets
   - 启用成本异常检测
   - 标记资源以进行成本分配
   - 月度成本审查会议

## 成本优化清单

- [ ] 启用 AWS Cost Explorer
- [ ] 设置成本分配标记
- [ ] 使用警报创建 AWS Budget
- [ ] 审查并删除未使用的资源
- [ ] 分析 Reserved Instance 机会
- [ ] 实施 S3 Intelligent-Tiering
- [ ] 审查数据传输成本
- [ ] 优化 Lambda 内存分配
- [ ] 使用 CloudWatch Logs 保留策略
- [ ] 考虑多区域成本差异

## 示例提示

**分析**
- "显示过去 3 个月的 AWS 成本（按服务分类）"
- "我最昂贵的 10 个资源是什么？"
- "比较本月支出与上月"

**优化**
- "查找所有未连接的 EBS 卷并计算节省"
- "识别 CPU 利用率 <5% 的 EC2 实例"
- "根据使用情况建议购买 Reserved Instance"
- "计算删除超过 90 天的快照的节省"

**实施**
- "创建脚本以删除未连接的卷"
- "设置预算警报为 $1000/月"
- "为领导层生成成本优化报告"

## 最佳实践

- 始终首先在非生产环境中测试
- 在删除前验证资源是否确实未使用
- 记录所有成本优化操作
- 计算优化工作的 ROI
- 自动化重复的优化任务
- 使用 AWS Trusted Advisor 建议
- 启用 AWS 成本异常检测

## 与 Kiro CLI 的集成

此技能与 Kiro CLI 的 AWS 集成无缝配合：

```bash
# 使用 Kiro 分析成本
kiro-cli chat "Use aws-cost-optimizer to analyze my spending"

# 生成优化报告
kiro-cli chat "Create a cost optimization plan using aws-cost-optimizer"
```

## 安全说明

- **风险级别：低** - 只读分析是安全的
- **删除操作：中等风险** - 始终在删除资源前验证
- **生产变更：高风险** - 首先在开发/分阶段测试大小调整
- 在任何删除前维护备份
- 在可用时使用 `--dry-run` 标志

## 其他资源

- [AWS 成本优化最佳实践](https://aws.amazon.com/pricing/cost-optimization/)
- [AWS Well-Architected Framework - 成本优化](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- [AWS Cost Explorer API](https://docs.aws.amazon.com/cost-management/latest/APIReference/Welcome.html)

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
