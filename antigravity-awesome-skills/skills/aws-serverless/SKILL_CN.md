---
name: aws-serverless
description: 用于在 AWS 上构建生产就绪的无服务器应用的专门技能。
  涵盖 Lambda 函数、API Gateway、DynamoDB、SQS/SNS
  事件驱动模式、SAM/CDK 部署和冷启动优化。
risk: critical
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# AWS 无服务器

用于在 AWS 上构建生产就绪的无服务器应用的专门技能。
涵盖 Lambda 函数、API Gateway、DynamoDB、SQS/SNS 事件驱动模式、
SAM/CDK 部署和冷启动优化。

## 详细指南

在执行此技能之前，请阅读[详细指南](references/detailed-guide.md)。它包含完整的流程和参考资料。将其安全性、前置条件和验证要求视为强制性的。对于专注的工作，加载相关部分；对于端到端的工作，完整阅读指南。

## 监视内存使用

```javascript
exports.handler = async (event, context) => {
  const used = process.memoryUsage();
  console.log('内存：', {
    heapUsed: Math.round(used.heapUsed / 1024 / 1024) + 'MB',
    heapTotal: Math.round(used.heapTotal / 1024 / 1024) + 'MB'
  });
  // ...
};
```

## 何时使用
当请求清楚地匹配上述描述的功能和模式时使用此技能。

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
