---
name: azure-storage-queue-rust
description: 用于 Rust 的 Azure 队列存储库。发送、接收和管理队列消息。触发词："queue storage rust"、"QueueClient rust"、"send message rust"、"receive messages rust"、"QueueServiceClient rust"、"queue rust"。
risk: critical
source: https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-rust/skills/azure-storage-queue-rust
source_repo: microsoft/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/microsoft/skills/blob/main/LICENSE
---

# 用于 Rust 的 Azure 队列存储库

## 何时使用

当您需要用于 Rust 的 Azure 队列存储库时，请使用此技能。发送、接收和管理队列消息。触发词："queue storage rust"、"QueueClient rust"、"send message rust"、"receive messages rust"、"QueueServiceClient rust"、"queue rust"。

用于 Azure 队列存储的客户端库 — 发送、接收和管理队列消息。

在以下情况下使用此技能：

- 应用需要在 Rust 中从 Azure 队列存储发送或接收消息
- 您需要创建或管理队列
- 您需要查看、接收或删除队列消息
- 您需要基于 RBAC 的队列操作身份验证

> **重要提示：** 仅使用由 [azure-sdk](https://crates.io/users/azure-sdk) crates.io 用户发布的官方 `azure_storage_queue` crate。不要使用非官方或社区 crate。官方 crate 使用下划线命名，版本都不是 0.21.0。

## 安装

```sh
cargo add azure_storage_queue azure_identity azure_core tokio
```

> 如果您的代码直接使用 `azure_core` 类型，请将 `azure_core` 添加到 `Cargo.toml`。如果您仅使用 `azure_storage_queue` 重新导出，直接的 `azure_core` 依赖项是可选的。

## 环境变量

```bash
AZURE_STORAGE_QUEUE_ENDPOINT=https://<account>.queue.core.windows.net/ # 所有操作都需要
```

## 身份验证

```rust
use azure_core::http::Url;
use azure_identity::DeveloperToolsCredential;
use azure_storage_queue::QueueServiceClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 本地开发：DeveloperToolsCredential。生产环境：使用 ManagedIdentityCredential。
    let credential = DeveloperToolsCredential::new(None)?;
    let service_url = Url::parse("https://<storage_account_name>.queue.core.windows.net/")?;
    let service_client = QueueServiceClient::new(service_url, Some(credential), None)?;

    // 按名称派生队列客户端。
    let queue_client = service_client.queue_client("<queue_name>")?;
    Ok(())
}
```

## 客户端类型

| 客户端 | 用途 | 访问方式 |
| -------------------- | ------------------------------------- | ---------------------------------------- |
| `QueueServiceClient` | 帐户级操作、列表队列 | `QueueServiceClient::new()` |
| `QueueClient` | 队列操作、发送/接收/删除 | `service_client.queue_client("<name>")?` |

## 核心工作流

### 发送消息

```rust
use azure_core::http::Url;
use azure_identity::DeveloperToolsCredential;
use azure_storage_queue::{models::QueueMessage, QueueServiceClient};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let credential = DeveloperToolsCredential::new(None)?;
    let service_url = Url::parse("https://<storage_account_name>.queue.core.windows.net/")?;
    let service_client = QueueServiceClient::new(service_url, Some(credential), None)?;
    let queue_client = service_client.queue_client("<queue_name>")?;

    let message = QueueMessage {
        message_text: Some("hello world".to_string()),
    };
    queue_client.send_message(message.try_into()?, None).await?;
    Ok(())
}
```

### 接收消息

```rust
use azure_core::http::Url;
use azure_identity::DeveloperToolsCredential;
use azure_storage_queue::QueueServiceClient;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let credential = DeveloperToolsCredential::new(None)?;
    let service_url = Url::parse("https://<storage_account_name>.queue.core.windows.net/")?;
    let service_client = QueueServiceClient::new(service_url, Some(credential), None)?;
    let queue_client = service_client.queue_client("<queue_name>")?;

    let response = queue_client.receive_messages(None).await?;
    let messages = response.into_model()?;
    for msg in messages.items.unwrap_or_default() {
        println!("{}", msg.message_text.as_deref().unwrap_or("<empty>"));
    }
    Ok(())
}
```

### 删除消息

接收消息后，使用消息 ID 和弹出回执将其删除：

```rust
let response = queue_client.receive_messages(None).await?;
let messages = response.into_model()?;
for msg in messages.items.unwrap_or_default() {
    if let (Some(id), Some(pop_receipt)) = (&msg.message_id, &msg.pop_receipt) {
        queue_client.delete_message(id, pop_receipt, None).await?;
    }
}
```

### 查看消息

查看消息而不将其从队列中删除：

```rust
let response = queue_client.peek_messages(None).await?;
let messages = response.into_model()?;
for msg in messages.items.unwrap_or_default() {
    println!("Peeked: {}", msg.message_text.as_deref().unwrap_or("<empty>"));
}
```

## RBAC 角色

对于 Entra ID 身份验证，为身份分配以下角色之一：

| 角色 | 访问权限 |
| -------------------------------------- | ---------------------- |
| `Storage Queue Data Reader` | 读取和查看消息 |
| `Storage Queue Data Contributor` | 读/写消息 |
| `Storage Queue Data Message Sender` | 仅发送消息 |
| `Storage Queue Data Message Processor` | 接收和删除 |

## 最佳实践

1. **使用 `cargo add` 管理依赖项，从不直接编辑 `Cargo.toml`。** 使用 cargo 命令添加和删除 Rust SDK 依赖项，而不是手动编辑清单。
2. **仅在直接导入 `azure_core` 类型时添加 `azure_core`。** 如果您的代码导入 `azure_core::http::Url`、`azure_core::http::RequestContent` 或 `azure_core::error::ErrorKind`，请包含 `azure_core`；否则直接依赖项是可选的。
3. **本地开发使用 `DeveloperToolsCredential`**，**生产环境使用 `ManagedIdentityCredential`** — Rust 不提供单一的 `DefaultAzureCredential` 类型
4. **从不硬编码凭证** — 使用环境变量或托管身份
5. **分配 RBAC 角色** — 确保身份具有适当的队列数据角色
6. **将 `QueueServiceClient` 用作入口点** 并通过 `queue_client()` 从中派生 `QueueClient`
7. **处理后删除消息** — 使用来自 `receive_messages` 的消息 ID 和弹出回执
8. **重用客户端** — 客户端是线程安全的；创建一次，在任务间共享

## 参考链接

| 资源 | 链接 |
| ------------- | ------------------------------------------------------------------------------------- |
| API 参考 | https://docs.rs/crate/azure_storage_queue/latest |
| crates.io | https://crates.io/crates/azure_storage_queue |
| 源代码 | https://github.com/Azure/azure-sdk-for-rust/tree/main/sdk/storage/azure_storage_queue |

## 限制

- 仅在任务明确符合其上游源和本地项目上下文时使用此技能。
- 在应用更改前验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例作为环境特定测试、安全审查或用户批准破坏性或成本高昂操作的替代品。
