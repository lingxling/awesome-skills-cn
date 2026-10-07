---
name: azure-mgmt-apimanagement-py
description: 用于 Python 的 Azure API 管理 SDK。用于管理 APIM 服务、API、产品、订阅和策略。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure API 管理 SDK（Python）

管理 Azure API 管理服务、API、产品和策略。

## 安装

```bash
pip install azure-mgmt-apimanagement
pip install azure-identity
```

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

## 身份验证

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.apimanagement import ApiManagementClient
import os

client = ApiManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)
```

## 创建 APIM 服务

```python
from azure.mgmt.apimanagement.models import (
    ApiManagementServiceResource,
    ApiManagementServiceSkuProperties,
    SkuType
)

service = client.api_management_service.begin_create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    parameters=ApiManagementServiceResource(
        location="eastus",
        publisher_email="admin@example.com",
        publisher_name="My Organization",
        sku=ApiManagementServiceSkuProperties(
            name=SkuType.DEVELOPER,
            capacity=1
        )
    )
).result()

print(f"Created APIM: {service.name}")
```

## 从 OpenAPI 导入 API

```python
from azure.mgmt.apimanagement.models import (
    ApiCreateOrUpdateParameter,
    ContentFormat,
    Protocol
)

api = client.api.begin_create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    api_id="my-api",
    parameters=ApiCreateOrUpdateParameter(
        display_name="My API",
        path="myapi",
        protocols=[Protocol.HTTPS],
        format=ContentFormat.OPENAPI_JSON,
        value='{"openapi": "3.0.0", "info": {"title": "My API", "version": "1.0"}, "paths": {"/health": {"get": {"responses": {"200": {"description": "OK"}}}}}}'
    )
).result()

print(f"Imported API: {api.display_name}")
```

## 从 URL 导入 API

```python
api = client.api.begin_create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    api_id="petstore",
    parameters=ApiCreateOrUpdateParameter(
        display_name="Petstore API",
        path="petstore",
        protocols=[Protocol.HTTPS],
        format=ContentFormat.OPENAPI_LINK,
        value="https://petstore.swagger.io/v2/swagger.json"
    )
).result()
```

## 列出 API

```python
apis = client.api.list_by_service(
    resource_group_name="my-resource-group",
    service_name="my-apim"
)

for api in apis:
    print(f"{api.name}: {api.display_name} - {api.path}")
```

## 创建产品

```python
from azure.mgmt.apimanagement.models import ProductContract

product = client.product.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    product_id="premium",
    parameters=ProductContract(
        display_name="Premium",
        description="Premium tier with unlimited access",
        subscription_required=True,
        approval_required=False,
        state="published"
    )
)

print(f"Created product: {product.display_name}")
```

## 将 API 添加到产品

```python
client.product_api.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    product_id="premium",
    api_id="my-api"
)
```

## 创建订阅

```python
from azure.mgmt.apimanagement.models import SubscriptionCreateParameters

subscription = client.subscription.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    sid="my-subscription",
    parameters=SubscriptionCreateParameters(
        display_name="My Subscription",
        scope=f"/products/premium",
        state="active"
    )
)

print(f"Subscription key: {subscription.primary_key}")
```

## 设置 API 策略

```python
from azure.mgmt.apimanagement.models import PolicyContract

policy_xml = """
<policies>
    <inbound>
        <rate-limit calls="100" renewal-period="60" />
        <set-header name="X-Custom-Header" exists-action="override">
            <value>CustomValue</value>
        </set-header>
    </inbound>
    <backend>
        <forward-request />
    </backend>
    <outbound />
    <on-error />
</policies>
"""

client.api_policy.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    api_id="my-api",
    policy_id="policy",
    parameters=PolicyContract(
        value=policy_xml,
        format="xml"
    )
)
```

## 创建命名值（秘密）

```python
from azure.mgmt.apimanagement.models import NamedValueCreateContract

named_value = client.named_value.begin_create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    named_value_id="backend-api-key",
    parameters=NamedValueCreateContract(
        display_name="Backend API Key",
        value="secret-key-value",
        secret=True
    )
).result()
```

## 创建后端

```python
from azure.mgmt.apimanagement.models import BackendContract

backend = client.backend.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    backend_id="my-backend",
    parameters=BackendContract(
        url="https://api.backend.example.com",
        protocol="http",
        description="My backend service"
    )
)
```

## 创建用户

```python
from azure.mgmt.apimanagement.models import UserCreateParameters

user = client.user.create_or_update(
    resource_group_name="my-resource-group",
    service_name="my-apim",
    user_id="newuser",
    parameters=UserCreateParameters(
        email="user@example.com",
        first_name="John",
        last_name="Doe"
    )
)
```

## 操作组

| 组 | 用途 |
|-------|---------|
| `api_management_service` | APIM 实例管理 |
| `api` | API 操作 |
| `api_operation` | API 操作详情 |
| `api_policy` | API 级别策略 |
| `product` | 产品管理 |
| `product_api` | 产品-API 关联 |
| `subscription` | 订阅管理 |
| `user` | 用户管理 |
| `named_value` | 命名值/秘密 |
| `backend` | 后端服务 |
| `certificate` | 证书 |
| `gateway` | 自托管网关 |

## 最佳实践

1. **使用命名值**管理秘密和配置
2. **在适当范围**应用策略（全局、产品、API、操作）
3. **使用产品**捆绑 API 并管理访问
4. **启用 Application Insights** 进行监控
5. **使用后端**抽象后端服务
6. **对 API 进行版本控制**使用 APIM 的版本功能

## 使用场景

本技能适用于执行上述概述中描述的工作流或操作。

## 限制条件

- 仅在任务明确符合上述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
