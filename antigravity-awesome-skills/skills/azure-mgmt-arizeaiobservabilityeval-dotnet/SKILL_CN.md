---
name: azure-mgmt-arizeaiobservabilityeval-dotnet
description: 用于 Arize AI 可观测性和评估的 Azure Resource Manager SDK (.NET)。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.ArizeAIObservabilityEval

用于在 Azure 上管理 Arize AI 可观测性和评估资源的 .NET SDK。

## 安装

```bash
dotnet add package Azure.ResourceManager.ArizeAIObservabilityEval --version 1.0.0
```

## 包信息

| 属性 | 值 |
|----------|-------|
| 包 | `Azure.ResourceManager.ArizeAIObservabilityEval` |
| 版本 | `1.0.0` (GA) |
| API 版本 | `2024-10-01` |
| ARM 类型 | `ArizeAi.ObservabilityEval/organizations` |
| 依赖项 | `Azure.Core` >= 1.46.2, `Azure.ResourceManager` >= 1.13.1 |

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_TENANT_ID=<your-tenant-id>
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.ArizeAIObservabilityEval;

// Always use DefaultAzureCredential
var credential = new DefaultAzureCredential();
var armClient = new ArmClient(credential);
```

## 核心工作流

### 创建 Arize AI 组织

```csharp
using Azure.Core;
using Azure.ResourceManager.Resources;
using Azure.ResourceManager.ArizeAIObservabilityEval;
using Azure.ResourceManager.ArizeAIObservabilityEval.Models;

// Get subscription and resource group
var subscriptionId = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID");
var subscription = await armClient.GetSubscriptionResource(
    SubscriptionResource.CreateResourceIdentifier(subscriptionId)).GetAsync();
var resourceGroup = await subscription.Value.GetResourceGroupAsync("my-resource-group");

// Get the organization collection
var collection = resourceGroup.Value.GetArizeAIObservabilityEvalOrganizations();

// Create organization data
var data = new ArizeAIObservabilityEvalOrganizationData(AzureLocation.EastUS)
{
    Properties = new ArizeAIObservabilityEvalOrganizationProperties
    {
        Marketplace = new ArizeAIObservabilityEvalMarketplaceDetails
        {
            SubscriptionId = "marketplace-subscription-id",
            OfferDetails = new ArizeAIObservabilityEvalOfferDetails
            {
                PublisherId = "arikimlabs1649082416596",
                OfferId = "arize-liftr-1",
                PlanId = "arize-liftr-1-plan",
                PlanName = "Arize AI Plan",
                TermUnit = "P1M",
                TermId = "term-id"
            }
        },
        User = new ArizeAIObservabilityEvalUserDetails
        {
            FirstName = "John",
            LastName = "Doe",
            EmailAddress = "john.doe@example.com"
        }
    },
    Tags = { ["environment"] = "production" }
};

// Create (long-running operation)
var operation = await collection.CreateOrUpdateAsync(
    WaitUntil.Completed,
    "my-arize-org",
    data);

var organization = operation.Value;
Console.WriteLine($"Created: {organization.Data.Name}");
```

### 获取组织

```csharp
// Option 1: From collection
var org = await collection.GetAsync("my-arize-org");

// Option 2: Check if exists first
var exists = await collection.ExistsAsync("my-arize-org");
if (exists.Value)
{
    var org = await collection.GetAsync("my-arize-org");
}

// Option 3: GetIfExists (returns null if not found)
var response = await collection.GetIfExistsAsync("my-arize-org");
if (response.HasValue)
{
    var org = response.Value;
}
```

### 列出组织

```csharp
// List in resource group
await foreach (var org in collection.GetAllAsync())
{
    Console.WriteLine($"Org: {org.Data.Name}, State: {org.Data.Properties?.ProvisioningState}");
}

// List in subscription
await foreach (var org in subscription.Value.GetArizeAIObservabilityEvalOrganizationsAsync())
{
    Console.WriteLine($"Org: {org.Data.Name}");
}
```

### 更新组织

```csharp
// Update tags
var org = await collection.GetAsync("my-arize-org");
var updateData = new ArizeAIObservabilityEvalOrganizationPatch
{
    Tags = { ["environment"] = "staging", ["team"] = "ml-ops" }
};
var updated = await org.Value.UpdateAsync(updateData);
```

### 删除组织

```csharp
var org = await collection.GetAsync("my-arize-org");
await org.Value.DeleteAsync(WaitUntil.Completed);
```

## 关键类型

| 类型 | 用途 |
|------|---------|
| `ArizeAIObservabilityEvalOrganizationResource` | Arize 组织的主要 ARM 资源 |
| `ArizeAIObservabilityEvalOrganizationCollection` | 用于 CRUD 操作的集合 |
| `ArizeAIObservabilityEvalOrganizationData` | 资源数据模型 |
| `ArizeAIObservabilityEvalOrganizationProperties` | 组织属性 |
| `ArizeAIObservabilityEvalMarketplaceDetails` | Azure 市场订阅信息 |
| `ArizeAIObservabilityEvalOfferDetails` | 市场套餐配置 |
| `ArizeAIObservabilityEvalUserDetails` | 用户联系信息 |
| `ArizeAIObservabilityEvalOrganizationPatch` | 用于更新的补丁模型 |
| `ArizeAIObservabilityEvalSingleSignOnPropertiesV2` | SSO 配置 |

## 枚举

| 枚举 | 值 |
|------|--------|
| `ArizeAIObservabilityEvalOfferProvisioningState` | `Succeeded`, `Failed`, `Canceled`, `Provisioning`, `Updating`, `Deleting`, `Accepted` |
| `ArizeAIObservabilityEvalMarketplaceSubscriptionStatus` | `PendingFulfillmentStart`, `Subscribed`, `Suspended`, `Unsubscribed` |
| `ArizeAIObservabilityEvalSingleSignOnState` | `Initial`, `Enable`, `Disable` |
| `ArizeAIObservabilityEvalSingleSignOnType` | `Saml`, `OpenId` |

## 最佳实践

1. **使用异步方法** — 所有操作都支持 async/await
2. **处理长期运行操作** — 使用 `WaitUntil.Completed` 或手动轮询
3. **使用 GetIfExistsAsync** — 避免为条件逻辑抛出异常
4. **实现重试策略** — 通过 `ArmClientOptions` 配置
5. **使用资源标识符** — 用于直接资源访问而不列出
6. **正确关闭客户端** — 使用 `using` 语句或显式释放

## 错误处理

```csharp
try
{
    var org = await collection.GetAsync("my-arize-org");
}
catch (Azure.RequestFailedException ex) when (ex.Status == 404)
{
    Console.WriteLine("Organization not found");
}
catch (Azure.RequestFailedException ex)
{
    Console.WriteLine($"Azure error: {ex.Message}");
}
```

## 直接资源访问

```csharp
// Access resource directly by ID (without listing)
var resourceId = ArizeAIObservabilityEvalOrganizationResource.CreateResourceIdentifier(
    subscriptionId,
    "my-resource-group",
    "my-arize-org");

var org = armClient.GetArizeAIObservabilityEvalOrganizationResource(resourceId);
var data = await org.GetAsync();
```

## 链接

- [NuGet 包](https://www.nuget.org/packages/Azure.ResourceManager.ArizeAIObservabilityEval)
- [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net)
- [Arize AI](https://arize.com/)

## 使用场景

本技能适用于执行上述概述中描述的工作流或操作。

## 限制条件

- 仅在任务明确符合上述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
