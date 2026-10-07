---
name: azure-keyvault-secrets-ts
description: "使用 Azure Key Vault Secrets SDK for JavaScript (@azure/keyvault-secrets) 管理机密。存储和检索应用程序机密或配置值时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Azure Key Vault Secrets TypeScript SDK

使用 Azure Key Vault 管理机密。

## 安装

```bash
# Secrets SDK
npm install @azure/keyvault-secrets @azure/identity
```

## 环境变量

```bash
KEY_VAULT_URL=https://<vault-name>.vault.azure.net
# 或
AZURE_KEYVAULT_NAME=<vault-name>
```

## 身份验证

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { SecretClient } from "@azure/keyvault-secrets";

const credential = new DefaultAzureCredential();
const vaultUrl = `https://${process.env.AZURE_KEYVAULT_NAME}.vault.azure.net`;

const keyClient = new KeyClient(vaultUrl, credential);
const secretClient = new SecretClient(vaultUrl, credential);
```

## 机密操作

### 创建/设置机密

```typescript
const secret = await secretClient.setSecret("MySecret", "secret-value");

// 具有属性
const secretWithAttrs = await secretClient.setSecret("MySecret", "value", {
  enabled: true,
  expiresOn: new Date("2025-12-31"),
  contentType: "application/json",
  tags: { environment: "production" }
});
```

### 获取机密

```typescript
// 获取最新版本
const secret = await secretClient.getSecret("MySecret");
console.log(secret.value);

// 获取特定版本
const specificSecret = await secretClient.getSecret("MySecret", {
  version: secret.properties.version
});
```

### 列出机密

```typescript
for await (const secretProperties of secretClient.listPropertiesOfSecrets()) {
  console.log(secretProperties.name);
}

// 列出版本
for await (const version of secretClient.listPropertiesOfSecretVersions("MySecret")) {
  console.log(version.version);
}
```

### 删除机密

```typescript
// 软删除
const deletePoller = await secretClient.beginDeleteSecret("MySecret");
await deletePoller.pollUntilDone();

// 清除（永久）
await secretClient.purgeDeletedSecret("MySecret");

// 恢复
const recoverPoller = await secretClient.beginRecoverDeletedSecret("MySecret");
await recoverPoller.pollUntilDone();
```

## 密钥操作

### 创建密钥

```typescript
// 通用密钥
const key = await keyClient.createKey("MyKey", "RSA");

// 具有大小的 RSA 密钥
const rsaKey = await keyClient.createRsaKey("MyRsaKey", { keySize: 2048 });

// 椭圆曲线密钥
const ecKey = await keyClient.createEcKey("MyEcKey", { curve: "P-256" });

// 具有属性
const keyWithAttrs = await keyClient.createKey("MyKey", "RSA", {
  enabled: true,
  expiresOn: new Date("2025-12-31"),
  tags: { purpose: "encryption" },
  keyOps: ["encrypt", "decrypt", "sign", "verify"]
});
```

### 获取密钥

```typescript
const key = await keyClient.getKey("MyKey");
console.log(key.name, key.keyType);
```

### 列出密钥

```typescript
for await (const keyProperties of keyClient.listPropertiesOfKeys()) {
  console.log(keyProperties.name);
}
```

### 轮换密钥

```typescript
// 手动轮换
const rotatedKey = await keyClient.rotateKey("MyKey");

// 设置轮换策略
await keyClient.updateKeyRotationPolicy("MyKey", {
  lifetimeActions: [{ action: "Rotate", timeBeforeExpiry: "P30D" }],
  expiresIn: "P90D"
});
```

### 删除密钥

```typescript
const deletePoller = await keyClient.beginDeleteKey("MyKey");
await deletePoller.pollUntilDone();

// 清除
await keyClient.purgeDeletedKey("MyKey");
```

## 密码学操作

### 创建 CryptographyClient

```typescript
import { CryptographyClient } from "@azure/keyvault-keys";

// 从密钥对象
const cryptoClient = new CryptographyClient(key, credential);

// 从密钥 ID
const cryptoClient = new CryptographyClient(key.id!, credential);
```

### 加密/解密

```typescript
// 加密
const encryptResult = await cryptoClient.encrypt({
  algorithm: "RSA-OAEP",
  plaintext: Buffer.from("My secret message")
});

// 解密
const decryptResult = await cryptoClient.decrypt({
  algorithm: "RSA-OAEP",
  ciphertext: encryptResult.result
});

console.log(decryptResult.result.toString());
```

### 签名/验证

```typescript
import { createHash } from "node:crypto";

// 创建摘要
const hash = createHash("sha256").update("My message").digest();

// 签名
const signResult = await cryptoClient.sign("RS256", hash);

// 验证
const verifyResult = await cryptoClient.verify("RS256", hash, signResult.result);
console.log("Valid:", verifyResult.result);
```

### 包装/解包密钥

```typescript
// 包装密钥（为存储加密）
const wrapResult = await cryptoClient.wrapKey("RSA-OAEP", Buffer.from("key-material"));

// 解包
const unwrapResult = await cryptoClient.unwrapKey("RSA-OAEP", wrapResult.result);
```

## 备份和恢复

```typescript
// 备份
const keyBackup = await keyClient.backupKey("MyKey");
const secretBackup = await secretClient.backupSecret("MySecret");

// 恢复（可以恢复到不同的保管库）
const restoredKey = await keyClient.restoreKeyBackup(keyBackup!);
const restoredSecret = await secretClient.restoreSecretBackup(secretBackup!);
```

## 关键类型

```typescript
import {
  KeyClient,
  KeyVaultKey,
  KeyProperties,
  DeletedKey,
  CryptographyClient,
  KnownEncryptionAlgorithms,
  KnownSignatureAlgorithms
} from "@azure/keyvault-keys";

import {
  SecretClient,
  KeyVaultSecret,
  SecretProperties,
  DeletedSecret
} from "@azure/keyvault-secrets";
```

## 错误处理

```typescript
try {
  const secret = await secretClient.getSecret("NonExistent");
} catch (error: any) {
  if (error.code === "SecretNotFound") {
    console.log("Secret does not exist");
  } else {
    throw error;
  }
}
```

## 最佳实践

1. **使用 DefaultAzureCredential** - 在开发和生产中都能工作
2. **启用软删除** - 生产保管库需要此功能
3. **设置过期日期** - 在密钥和机密上
4. **使用密钥轮换策略** - 自动化密钥轮换
5. **限制密钥操作** - 仅授予所需的操作（加密、签名等）
6. **浏览器不支持** - 这些 SDK 仅针对 Node.js

## 何时使用

本技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功条件，请停止并寻求澄清。
