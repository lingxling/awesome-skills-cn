---
name: azure-storage-queue-py
description: 用于 Python 的 Azure 队列存储 SDK。用于可靠的消息队列、任务分发和异步处理。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure 队列存储 SDK (Python)

用于异步通信的简单、经济高效的消息队列。

## 安装

```bash
pip install azure-storage-queue azure-identity
```

## 环境变量

```bash
AZURE_STORAGE_ACCOUNT_URL=https://<account>.queue.core.windows.net
```

## 身份验证

```python
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueServiceClient, QueueClient

credential = DefaultAzureCredential()
account_url = "https://<account>.queue.core.windows.net"

# 服务客户端
service_client = QueueServiceClient(account_url=account_url, credential=credential)

# 队列客户端
queue_client = QueueClient(account_url=account_url, queue_name="myqueue", credential=credential)
```

## 队列操作

```python
# 创建队列
service_client.create_queue("myqueue")

# 获取队列客户端
queue_client = service_client.get_queue_client("myqueue")

# 删除队列
service_client.delete_queue("myqueue")

# 列表队列
for queue in service_client.list_queues():
    print(queue.name)
```

## 发送消息

```python
# 发送消息（字符串）
queue_client.send_message("Hello, Queue!")

# 带选项发送
queue_client.send_message(
    content="Delayed message",
    visibility_timeout=60,  # 隐藏 60 秒
    time_to_live=3600       # 1 小时后过期
)

# 发送 JSON
import json
data = {"task": "process", "id": 123}
queue_client.send_message(json.dumps(data))
```

## 接收消息

```python
# 接收消息（暂时将其隐藏）
messages = queue_client.receive_messages(
    messages_per_page=10,
    visibility_timeout=30  # 30 秒用于处理
)

for message in messages:
    print(f"ID: {message.id}")
    print(f"Content: {message.content}")
    print(f"Dequeue count: {message.dequeue_count}")
    
    # 处理消息...
    
    # 处理后删除
    queue_client.delete_message(message)
```

## 查看消息

```python
# 查看而不隐藏（不影响可见性）
messages = queue_client.peek_messages(max_messages=5)

for message in messages:
    print(message.content)
```

## 更新消息

```python
# 延长可见性或更新内容
messages = queue_client.receive_messages()
for message in messages:
    # 延长超时时间（需要更多时间）
    queue_client.update_message(
        message,
        visibility_timeout=60
    )
    
    # 更新内容和超时时间
    queue_client.update_message(
        message,
        content="Updated content",
        visibility_timeout=60
    )
```

## 删除消息

```python
# 成功处理后删除
messages = queue_client.receive_messages()
for message in messages:
    try:
        # 处理...
        queue_client.delete_message(message)
    except Exception:
        # 消息在超时后再次变为可见
        pass
```

## 清空队列

```python
# 删除所有消息
queue_client.clear_messages()
```

## 队列属性

```python
# 获取队列属性
properties = queue_client.get_queue_properties()
print(f"Approximate message count: {properties.approximate_message_count}")

# 设置/获取元数据
queue_client.set_queue_metadata(metadata={"environment": "production"})
properties = queue_client.get_queue_properties()
print(properties.metadata)
```

## 异步客户端

```python
from azure.storage.queue.aio import QueueServiceClient, QueueClient
from azure.identity.aio import DefaultAzureCredential

async def queue_operations():
    credential = DefaultAzureCredential()
    
    async with QueueClient(
        account_url="https://<account>.queue.core.windows.net",
        queue_name="myqueue",
        credential=credential
    ) as client:
        # 发送
        await client.send_message("Async message")
        
        # 接收
        async for message in client.receive_messages():
            print(message.content)
            await client.delete_message(message)

import asyncio
asyncio.run(queue_operations())
```

## Base64 编码

```python
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy

# 用于二进制数据
queue_client = QueueClient(
    account_url=account_url,
    queue_name="myqueue",
    credential=credential,
    message_encode_policy=BinaryBase64EncodePolicy(),
    message_decode_policy=BinaryBase64DecodePolicy()
)

# 发送字节
queue_client.send_message(b"Binary content")
```

## 最佳实践

1. **处理后删除消息** - 防止重复处理
2. **根据处理时间设置适当的可见性超时** - 避免超时过短或过长
3. **处理 `dequeue_count`** - 用于检测有问题的消息
4. **对于高吞吐量场景使用异步客户端** - 提高性能
5. **使用 `peek_messages` 监控** - 不影响队列的情况下查看消息
6. **设置 `time_to_live`** - 防止过时消息
7. **考虑使用 Service Bus** - 用于高级功能（会话、主题）

## 何时使用

此技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出作为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
