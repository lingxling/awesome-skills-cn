---
name: azure-keyvault-keys-rust
description: 'Azure Key Vault Keys Rust SDK。用于创建、管理和使用密码学密钥。触发词："keyvault keys rust"、"KeyClient rust"、"create key rust"、"encrypt rust"、"sign rust"。'
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Key Vault Keys Rust SDK

Azure Key Vault Keys 的客户端库——安全存储和管理密码学密钥。

## 安装

```sh
cargo add azure_security_keyvault_keys azure_identity
```

## 环境变量

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net/
```

## 身份验证

```rust
use azure_identity::DeveloperToolsCredential;
use azure_security_keyvault_keys::KeyClient;

let credential = DeveloperToolsCredential::new(None)?;
let client = KeyClient::new(
    "https://<vault-name>.vault.azure.net/",
    credential.clone(),
    None,
)?;
```

## 密钥类型

| 类型 | 描述 |
|------|-------------|
| RSA | RSA 密钥（2048、3072、4096 位） |
| EC | 椭圆曲线密钥（P-256、P-384、P-521） |
| RSA-HSM | HSM 保护的 RSA 密钥 |
| EC-HSM | HSM 保护的 EC 密钥 |

## 核心操作

### 获取密钥

```rust
let key = client
    .get_key("key-name", None)
    .await?
    .into_model()?;

println!("Key ID: {:?}", key.key.as_ref().map(|k| &k.kid));
```

### 创建密钥

```rust
use azure_security_keyvault_keys::models::{CreateKeyParameters, KeyType};

let params = CreateKeyParameters {
    kty: KeyType::Rsa,
    key_size: Some(2048),
    ..Default::default()
};

let key = client
    .create_key("key-name", params.try_into()?, None)
    .await?
    .into_model()?;
```

### 创建 EC 密钥

```rust
use azure_security_keyvault_keys::models::{CreateKeyParameters, KeyType, CurveName};

let params = CreateKeyParameters {
    kty: KeyType::Ec,
    curve: Some(CurveName::P256),
    ..Default::default()
};

let key = client
    .create_key("ec-key", params.try_into()?, None)
    .await?
    .into_model()?;
```

### 删除密钥

```rust
client.delete_key("key-name", None).await?;
```

### 列出密钥

```rust
use azure_security_keyvault_keys::ResourceExt;
use futures::TryStreamExt;

let mut pager = client.list_key_properties(None)?.into_stream();
while let Some(key) = pager.try_next().await? {
    let name = key.resource_id()?.name;
    println!("Key: {}", name);
}
```

### 备份密钥

```rust
let backup = client.backup_key("key-name", None).await?;
// 安全地存储 backup.value
```

### 恢复密钥

```rust
use azure_security_keyvault_keys::models::RestoreKeyParameters;

let params = RestoreKeyParameters {
    key_bundle_backup: backup_bytes,
};

client.restore_key(params.try_into()?, None).await?;
```

## 密码学操作

Key Vault 可以执行密码学操作而无需暴露私钥：

```rust
// 对于密码学操作，使用密钥的操作
// 可用操作取决于密钥类型和权限：
// - 加密/解密 (RSA)
// - 签名/验证 (RSA, EC)
// - wrapKey/unwrapKey (RSA)
```

## 最佳实践

1. **使用 Entra ID 身份验证** — 开发使用 `DeveloperToolsCredential`，生产使用 `ManagedIdentityCredential`
2. **对敏感工作负载使用 HSM 密钥** — 硬件保护的密钥
3. **使用 EC 进行签名** — 比 RSA 更高效
4. **使用 RSA 进行加密** — 加密数据时
5. **备份密钥** — 用于灾难恢复
6. **启用软删除** — 生产保管库需要此功能
7. **使用密钥轮换** — 定期创建新版本

## RBAC 权限

分配这些 Key Vault 角色：
- `Key Vault Crypto User` — 使用密钥进行密码学操作
- `Key Vault Crypto Officer` — 密钥的完整 CRUD

## 参考链接

| 资源 | 链接 |
|----------|------|
| API 参考 | https://docs.rs/azure_security_keyvault_keys |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/keyvault/azure_security_keyvault_keys |
| crates.io | https://crates.io/crates/azure_security_keyvault_keys |

## 何时使用

本技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功条件，请停止并寻求澄清。
