---
name: azure-messaging-webpubsubservice-py
description: Azure Web PubSub Service Python SDK。用于实时消息传递、WebSocket 连接和发布/订阅模式。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Web PubSub Service Python SDK

大规模实时消息传递与 WebSocket 连接。

## 安装

```bash
# 服务 SDK（服务器端）
pip install azure-messaging-webpubsubservice

# 客户端 SDK（用于 Python WebSocket 客户端）
pip install azure-messaging-webpubsubclient
```

## 环境变量

```bash
AZURE_WEBPUBSUB_CONNECTION_STRING=Endpoint=https://<name>.webpubsub.azure.com;AccessKey=...
AZURE_WEBPUBSUB_HUB=my-hub
```

## 服务客户端（服务器端）

### 身份验证

```python
from azure.messaging.webpubsubservice import WebPubSubServiceClient

# 连接字符串
client = WebPubSubServiceClient.from_connection_string(
    connection_string=os.environ["AZURE_WEBPUBSUB_CONNECTION_STRING"],
    hub="my-hub"
)

# Entra ID
from azure.identity import DefaultAzureCredential

client = WebPubSubServiceClient(
    endpoint="https://<name>.webpubsub.azure.com",
    hub="my-hub",
    credential=DefaultAzureCredential()
)
```

### 生成客户端访问令牌

```python
# 匿名用户的令牌
token = client.get_client_access_token()
print(f"URL: {token['url']}")

# 带用户 ID 的令牌
token = client.get_client_access_token(
    user_id="user123",
    roles=["webpubsub.sendToGroup", "webpubsub.joinLeaveGroup"]
)

# 带组的令牌
token = client.get_client_access_token(
    user_id="user123",
    groups=["group1", "group2"]
)
```

### 发送给所有客户端

```python
# 发送文本
client.send_to_all(message="Hello everyone!", content_type="text/plain")

# 发送 JSON
client.send_to_all(
    message={"type": "notification", "data": "Hello"},
    content_type="application/json"
)
```

### 发送给用户

```python
client.send_to_user(
    user_id="user123",
    message="Hello user!",
    content_type="text/plain"
)
```

### 发送给组

```python
client.send_to_group(
    group="my-group",
    message="Hello group!",
    content_type="text/plain"
)
```

### 发送给连接

```python
client.send_to_connection(
    connection_id="abc123",
    message="Hello connection!",
    content_type="text/plain"
)
```

### 组管理

```python
# 将用户添加到组
client.add_user_to_group(group="my-group", user_id="user123")

# 从组中移除用户
client.remove_user_from_group(group="my-group", user_id="user123")

# 将连接添加到组
client.add_connection_to_group(group="my-group", connection_id="abc123")

# 从组中移除连接
client.remove_connection_from_group(group="my-group", connection_id="abc123")
```

### 连接管理

```python
# 检查连接是否存在
exists = client.connection_exists(connection_id="abc123")

# 检查用户是否有连接
exists = client.user_exists(user_id="user123")

# 检查组是否有连接
exists = client.group_exists(group="my-group")

# 关闭连接
client.close_connection(connection_id="abc123", reason="Session ended")

# 关闭用户的所有连接
client.close_all_connections(user_id="user123")
```

### 授予/撤销权限

```python
from azure.messaging.webpubsubservice import WebPubSubServiceClient

# 授予权限
client.grant_permission(
    permission="joinLeaveGroup",
    connection_id="abc123",
    target_name="my-group"
)

# 撤销权限
client.revoke_permission(
    permission="joinLeaveGroup",
    connection_id="abc123",
    target_name="my-group"
)

# 检查权限
has_permission = client.check_permission(
    permission="joinLeaveGroup",
    connection_id="abc123",
    target_name="my-group"
)
```

## 客户端 SDK（Python WebSocket 客户端）

```python
from azure.messaging.webpubsubclient import WebPubSubClient

client = WebPubSubClient(credential=token["url"])

# 事件处理器
@client.on("connected")
def on_connected(e):
    print(f"Connected: {e.connection_id}")

@client.on("server-message")
def on_message(e):
    print(f"Message: {e.data}")

@client.on("group-message")
def on_group_message(e):
    print(f"Group {e.group}: {e.data}")

# 连接和发送
client.open()
client.send_to_group("my-group", "Hello from Python!")
```

## 异步服务客户端

```python
from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.identity.aio import DefaultAzureCredential

async def broadcast():
    credential = DefaultAzureCredential()
    client = WebPubSubServiceClient(
        endpoint="https://<name>.webpubsub.azure.com",
        hub="my-hub",
        credential=credential
    )
    
    await client.send_to_all("Hello async!", content_type="text/plain")
    
    await client.close()
    await credential.close()
```

## 客户端操作

| 操作 | 描述 |
|-----------|-------------|
| `get_client_access_token` | 生成 WebSocket 连接 URL |
| `send_to_all` | 广播给所有连接 |
| `send_to_user` | 发送给特定用户 |
| `send_to_group` | 发送给组成员 |
| `send_to_connection` | 发送给特定连接 |
| `add_user_to_group` | 将用户添加到组 |
| `remove_user_from_group` | 从组中移除用户 |
| `close_connection` | 断开客户端连接 |
| `connection_exists` | 检查连接状态 |

## 最佳实践

1. **使用角色** 限制客户端权限
2. **使用组** 进行目标消息传递
3. **生成短期令牌** 以确保安全
4. **使用用户 ID** 跨连接发送给用户
5. **在客户端应用程序中处理重新连接**
6. **使用 JSON** 内容类型处理结构化数据
7. **优雅地关闭连接** 并提供原因

## 何时使用

本技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功条件，请停止并寻求澄清。
