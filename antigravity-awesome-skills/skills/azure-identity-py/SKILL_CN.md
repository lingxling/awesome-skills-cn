---
name: azure-identity-py
description: Azure Identity Python SDK 身份验证。用于 DefaultAzureCredential、托管身份、服务主体和令牌缓存。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Identity Python SDK

使用 Microsoft Entra ID（原 Azure AD）的 Azure SDK 客户端认证库。

## 安装

```bash
pip install azure-identity
```

## 环境变量

```bash
# 服务主体（用于生产/CI）
AZURE_TENANT_ID=<your-tenant-id>
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>

# 用户分配的托管身份（可选）
AZURE_CLIENT_ID=<managed-identity-client-id>
```

## DefaultAzureCredential

大多数场景下的推荐凭证。按顺序尝试多种身份验证方法：

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# 在本地开发和生产中都能工作，无需更改代码
credential = DefaultAzureCredential()

client = BlobServiceClient(
    account_url="https://<account>.blob.core.windows.net",
    credential=credential
)
```

### 凭证链顺序

| 顺序 | 凭证 | 环境 |
|-------|-----------|-------------|
| 1 | EnvironmentCredential | CI/CD、容器 |
| 2 | WorkloadIdentityCredential | Kubernetes |
| 3 | ManagedIdentityCredential | Azure VMs、App Service、Functions |
| 4 | SharedTokenCacheCredential | 仅 Windows |
| 5 | VisualStudioCodeCredential | VS Code with Azure 扩展 |
| 6 | AzureCliCredential | `az login` |
| 7 | AzurePowerShellCredential | `Connect-AzAccount` |
| 8 | AzureDeveloperCliCredential | `azd auth login` |

### 自定义 DefaultAzureCredential

```python
# 排除您不需要的凭证
credential = DefaultAzureCredential(
    exclude_environment_credential=True,
    exclude_shared_token_cache_credential=True,
    managed_identity_client_id="<user-assigned-mi-client-id>"  # 用于用户分配的 MI
)

# 启用交互式浏览器（默认禁用）
credential = DefaultAzureCredential(
    exclude_interactive_browser_credential=False
)
```

## 特定凭证类型

### ManagedIdentityCredential

用于 Azure 托管资源（VMs、App Service、Functions、AKS）：

```python
from azure.identity import ManagedIdentityCredential

# 系统分配的托管身份
credential = ManagedIdentityCredential()

# 用户分配的托管身份
credential = ManagedIdentityCredential(
    client_id="<user-assigned-mi-client-id>"
)
```

### ClientSecretCredential

用于带有密钥的服务主体：

```python
from azure.identity import ClientSecretCredential

credential = ClientSecretCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"]
)
```

### AzureCliCredential

使用 `az login` 中的帐户：

```python
from azure.identity import AzureCliCredential

credential = AzureCliCredential()
```

### ChainedTokenCredential

自定义凭证链：

```python
from azure.identity import (
    ChainedTokenCredential,
    ManagedIdentityCredential,
    AzureCliCredential
)

# 首先尝试托管身份，回退到 CLI
credential = ChainedTokenCredential(
    ManagedIdentityCredential(client_id="<user-assigned-mi-client-id>"),
    AzureCliCredential()
)
```

## 凭证类型表

| 凭证 | 用例 | 身份验证方法 |
|------------|----------|-------------|
| `DefaultAzureCredential` | 大多数场景 | 自动检测 |
| `ManagedIdentityCredential` | Azure 托管应用 | 托管身份 |
| `ClientSecretCredential` | 服务主体 | 客户端密钥 |
| `ClientCertificateCredential` | 服务主体 | 证书 |
| `AzureCliCredential` | 本地开发 | Azure CLI |
| `AzureDeveloperCliCredential` | 本地开发 | Azure Developer CLI |
| `InteractiveBrowserCredential` | 用户登录 | 浏览器 OAuth |
| `DeviceCodeCredential` | 无头/SSH | 设备代码流 |

## 直接获取令牌

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# 获取特定范围的令牌
token = credential.get_token("https://management.azure.com/.default")
print(f"Token expires: {token.expires_on}")

# 对于 Azure Database for PostgreSQL
token = credential.get_token("https://ossrdbms-aad.database.windows.net/.default")
```

## 异步客户端

```python
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

async def main():
    credential = DefaultAzureCredential()
    
    async with BlobServiceClient(
        account_url="https://<account>.blob.core.windows.net",
        credential=credential
    ) as client:
        # ... 异步操作
        pass
    
    await credential.close()
```

## 最佳实践

1. **使用 DefaultAzureCredential** 处理在本地和 Azure 中运行的代码
2. **永远不要硬编码凭证** — 使用环境变量或托管身份
3. **在生产 Azure 部署中优先使用托管身份**
4. **在需要自定义凭证顺序时使用 ChainedTokenCredential**
5. **显式关闭异步凭证** 或使用上下文管理器
6. **为用户分配的托管身份设置 AZURE_CLIENT_ID**
7. **排除未使用的凭证** 以加快身份验证

## 何时使用

本技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功条件，请停止并寻求澄清。
