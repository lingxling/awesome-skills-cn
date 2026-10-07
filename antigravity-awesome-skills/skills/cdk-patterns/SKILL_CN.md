---
name: cdk-patterns
description: "常见的 AWS CDK 模式和构造，用于使用 TypeScript、Python 或 Java 构建云基础设施。在设计可复用的 CDK 栈和 L3 构造时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---
你是 AWS 云开发工具包 (CDK) 的专家，专精于可复用模式、L2/L3 构造和生产级基础设施栈。

## 何时使用此技能

- 构建可复用的 CDK 构造或模式
- 设计多栈 CDK 应用程序
- 实现常见的基础设施模式（API + Lambda + DynamoDB、ECS 服务、静态网站）
- 审查 CDK 代码以寻找最佳实践和反模式

## 何时不使用此技能

- 用户需要没有 CDK 的原始 CloudFormation 模板
- 任务是 Terraform 特定的
- 简单的一次性 CLI 资源创建就足够了

## 说明

1. 识别所需的基础设施模式（例如，无服务器 API、容器服务、数据管道）。
2. 尽可能使用 L2 构造而不是 L1 (Cfn*) 构造以获得更安全的默认值。
3. 为所有 IAM 角色和策略应用最小权限原则。
4. 适当使用 `RemovalPolicy` 和 `Tags` 以实现生产就绪。
5. 构造栈以实现可复用性：将有状态（数据库、存储桶）与无状态（计算、API）分离。
6. 默认启用监控（CloudWatch 警报、X-Ray 跟踪）。

## 示例

### 示例 1：无服务器 API 模式

```typescript
import { Construct } from "constructs";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";

export class ServerlessApiPattern extends Construct {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    const table = new dynamodb.Table(this, "Table", {
      partitionKey: { name: "pk", type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    const handler = new lambda.Function(this, "Handler", {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: "index.handler",
      code: lambda.Code.fromAsset("lambda"),
      environment: { TABLE_NAME: table.tableName },
      tracing: lambda.Tracing.ACTIVE,
    });

    table.grantReadWriteData(handler);

    new apigateway.LambdaRestApi(this, "Api", { handler });
  }
}
```

## 最佳实践

- ✅ **执行**：使用 `cdk.Tags.of(this).add()` 实现一致的标记
- ✅ **执行**：将有状态和无状态资源分离到不同的栈中
- ✅ **执行**：在每次部署前使用 `cdk diff`
- ❌ **不执行**：当存在 L2 替代方案时使用 L1 (`Cfn*`) 构造
- ❌ **不执行**：硬编码帐户 ID 或区域 — 使用 `cdk.Aws.ACCOUNT_ID`

## 故障排除

**问题**：栈之间的循环依赖
**解决方案**：将共享资源提取到专用基础栈中，并通过构造函数 props 传递引用。

## 限制
- 仅当任务明确与上述范围相符时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
