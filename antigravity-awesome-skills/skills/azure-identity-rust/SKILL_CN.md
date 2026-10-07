---
name: azure-identity-rust
description: Azure Identity Rust SDK 身份验证。用于 DeveloperToolsCredential、ManagedIdentityCredential、ClientSecretCredential 和基于令牌的身份验证。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Identity Rust SDK

使用 Microsoft Entra ID（原 Azure AD）的 Azure SDK 客户端认证库。

## 安装

```sh
cargo add azure_identity
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

## DeveloperToolsCredential

推荐用于本地开发的凭证。按顺序尝试开发者工具（Azure CLI、Azure Developer CLI）：

```rust
use azure_identity::DeveloperToolsCredential;
use azure_security_keyvault_secrets::SecretClient;

let credential = DeveloperToolsCredential::new(None)?;
let client = SecretClient::new(
    "https://my-vault.vault.azure.net/",
    credential.clone(),
    None,
)?;
```

### 凭证链顺序

| 顺序 | 凭证 | 环境 |
|-------|-----------|-------------|
| 1 | AzureCliCredential | `az login` |
| 2 | AzureDeveloperCliCredential | `azd auth login` |

## 凭证类型

| 凭证 | 用法 |
|------------|-------|
| `DeveloperToolsCredential` | 本地开发 - 尝试 CLI 工具 |
| `ManagedIdentityCredential` | Azure VMs、App Service、Functions、AKS |
| `WorkloadIdentityCredential` | Kubernetes 工作负载身份 |
| `ClientSecretCredential` | 带有密钥的服务主体 |
| `ClientCertificateCredential` | 带有证书的服务主体 |
| `AzureCliCredential` | 直接 Azure CLI 身份验证 |
| `AzureDeveloperCliCredential` | 直接 azd CLI 身份验证 |
| `AzurePipelinesCredential` | Azure Pipelines 服务连接 |
| `ClientAssertionCredential` | 自定义断言（联合身份） |

## ManagedIdentityCredential

用于 Azure 托管资源：

```rust
use azure_identity::ManagedIdentityCredential;

// 系统分配的托管身份
let credential = ManagedIdentityCredential::new(None)?;

// 用户分配的托管身份
let options = ManagedIdentityCredentialOptions {
    client_id: Some("<user-assigned-mi-client-id>".into()),
    ..Default::default()
};
let credential = ManagedIdentityCredential::new(Some(options))?;
```

## ClientSecretCredential

用于带有密钥的服务主体：

```rust
use azure_identity::ClientSecretCredential;

let credential = ClientSecretCredential::new(
    "<tenant-id>".into(),
    "<client-id>".into(),
    "<client-secret>".into(),
    None,
)?;
```

## 最佳实践

1. **在本地开发中使用 `DeveloperToolsCredential`** — 自动检测 Azure CLI
2. **在生产中使用 `ManagedIdentityCredential`** — 无需管理密钥
3. **克隆凭证** — 凭证被 `Arc` 包装且克隆成本低
4. **重用凭证实例** — 同一凭证可用于多个客户端
5. **使用 `tokio` 特性** — `cargo add azure_identity --features tokio`

## 参考链接

| 资源 | 链接 |
|----------|------|
| API 参考 | https://docs.rs/azure_identity |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/identity/azure_identity |
| crates.io | https://crates.io/crates/azure_identity |

## 何时使用

本技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功条件，请停止并寻求澄清。
