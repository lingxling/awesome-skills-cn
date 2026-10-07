---
name: azure-keyvault-py
description: Azure Key Vault Python SDK。用于管理机密、密钥和证书的安全存储。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Key Vault Python SDK

机密、密码学密钥和证书的安全存储和管理。

## 安装

```bash
# 机密
pip install azure-keyvault-secrets azure-identity

# 密钥（密码学操作）
pip install azure-keyvault-keys azure-identity

# 证书
pip install azure-keyvault-certificates azure-identity

# 全部
pip install azure-keyvault-secrets azure-keyvault-keys azure-keyvault-certificates azure-identity
```

## 环境变量

```bash
AZURE_KEYVAULT_URL=https://<vault-name>.vault.azure.net/
```

## 机密

### SecretClient 设置

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
vault_url = "https://<vault-name>.vault.azure.net/"

client = SecretClient(vault_url=vault_url, credential=credential)
```

### 机密操作

```python
# 设置机密
secret = client.set_secret("database-password", "super-secret-value")
print(f"Created: {secret.name}, version: {secret.properties.version}")

# 获取机密
secret = client.get_secret("database-password")
print(f"Value: {secret.value}")

# 获取特定版本
secret = client.get_secret("database-password", version="abc123")

# 列出机密（仅名称，不是值）
for secret_properties in client.list_properties_of_secrets():
    print(f"Secret: {secret_properties.name}")

# 列出版本
for version in client.list_properties_of_secret_versions("database-password"):
    print(f"Version: {version.version}, Created: {version.created_on}")

# 删除机密（软删除）
poller = client.begin_delete_secret("database-password")
deleted_secret = poller.result()

# 清除（永久删除，如果启用软删除）
client.purge_deleted_secret("database-password")

# 恢复已删除的机密
client.begin_recover_deleted_secret("database-password").result()
```

## 密钥

### KeyClient 设置

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient

credential = DefaultAzureCredential()
vault_url = "https://<vault-name>.vault.azure.net/"

client = KeyClient(vault_url=vault_url, credential=credential)
```

### 密钥操作

```python
from azure.keyvault.keys import KeyType

# 创建 RSA 密钥
rsa_key = client.create_rsa_key("rsa-key", size=2048)

# 创建 EC 密钥
ec_key = client.create_ec_key("ec-key", curve="P-256")

# 获取密钥
key = client.get_key("rsa-key")
print(f"Key type: {key.key_type}")

# 列出密钥
for key_properties in client.list_properties_of_keys():
    print(f"Key: {key_properties.name}")

# 删除密钥
poller = client.begin_delete_key("rsa-key")
deleted_key = poller.result()
```

### 密码学操作

```python
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm

# 获取特定密钥的加密客户端
crypto_client = CryptographyClient(key, credential=credential)
# 或从密钥 ID
crypto_client = CryptographyClient(
    "https://<vault>.vault.azure.net/keys/<key-name>/<version>",
    credential=credential
)

# 加密
plaintext = b"Hello, Key Vault!"
result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, plaintext)
ciphertext = result.ciphertext

# 解密
result = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, ciphertext)
decrypted = result.plaintext

# 签名
from azure.keyvault.keys.crypto import SignatureAlgorithm
import hashlib

digest = hashlib.sha256(b"data to sign").digest()
result = crypto_client.sign(SignatureAlgorithm.rs256, digest)
signature = result.signature

# 验证
result = crypto_client.verify(SignatureAlgorithm.rs256, digest, signature)
print(f"Valid: {result.is_valid}")
```

## 证书

### CertificateClient 设置

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.certificates import CertificateClient, CertificatePolicy

credential = DefaultAzureCredential()
vault_url = "https://<vault-name>.vault.azure.net/"

client = CertificateClient(vault_url=vault_url, credential=credential)
```

### 证书操作

```python
# 创建自签名证书
policy = CertificatePolicy.get_default()
poller = client.begin_create_certificate("my-cert", policy=policy)
certificate = poller.result()

# 获取证书
certificate = client.get_certificate("my-cert")
print(f"Thumbprint: {certificate.properties.x509_thumbprint.hex()}")

# 获取带有私钥的证书（作为机密）
from azure.keyvault.secrets import SecretClient
secret_client = SecretClient(vault_url=vault_url, credential=credential)
cert_secret = secret_client.get_secret("my-cert")
# cert_secret.value 包含 PEM 或 PKCS12

# 列出证书
for cert in client.list_properties_of_certificates():
    print(f"Certificate: {cert.name}")

# 删除证书
poller = client.begin_delete_certificate("my-cert")
deleted = poller.result()
```

## 客户端类型表

| 客户端 | 包 | 用途 |
|--------|---------|---------|
| `SecretClient` | `azure-keyvault-secrets` | 存储/检索机密 |
| `KeyClient` | `azure-keyvault-keys` | 管理密码学密钥 |
| `CryptographyClient` | `azure-keyvault-keys` | 加密/解密/签名/验证 |
| `CertificateClient` | `azure-keyvault-certificates` | 管理证书 |

## 异步客户端

```python
from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient

async def get_secret():
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    async with client:
        secret = await client.get_secret("my-secret")
        print(secret.value)

import asyncio
asyncio.run(get_secret())
```

## 错误处理

```python
from azure.core.exceptions import ResourceNotFoundError, HttpResponseError

try:
    secret = client.get_secret("nonexistent")
except ResourceNotFoundError:
    print("Secret not found")
except HttpResponseError as e:
    if e.status_code == 403:
        print("Access denied - check RBAC permissions")
    raise
```

## 最佳实践

1. **使用 DefaultAzureCredential** 进行身份验证
2. **在 Azure 托管应用程序中使用托管身份**
3. **启用软删除** 以进行恢复（默认启用）
4. **使用 RBAC** 而不是访问策略以实现细粒度控制
5. **定期轮换机密** 使用版本控制
6. **在 App Service/Functions 配置中使用 Key Vault 引用**
7. **适当缓存机密** 以减少 API 调用
8. **在高吞吐量场景中使用异步客户端**

## 何时使用

本技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功条件，请停止并寻求澄清。
