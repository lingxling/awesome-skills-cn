---
name: azure-eventhub-py
description: Azure Event Hubs Python SDK 流传输。用于高吞吐量事件摄取、生产者、消费者和检查点。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Event Hubs Python SDK

用于高吞吐量事件摄取的大数据流平台。

## 安装

```bash
pip install azure-eventhub azure-identity
# 用于通过 Blob 存储进行检查点
pip install azure-eventhub-checkpointstoreblob-aio
```

## 环境变量

```bash
EVENT_HUB_FULLY_QUALIFIED_NAMESPACE=<namespace>.servicebus.windows.net
EVENT_HUB_NAME=my-eventhub
STORAGE_ACCOUNT_URL=https://<account>.blob.core.windows.net
CHECKPOINT_CONTAINER=checkpoints
```

## 身份验证

```python
from azure.identity import DefaultAzureCredential
from azure.eventhub import EventHubProducerClient, EventHubConsumerClient

credential = DefaultAzureCredential()
namespace = "<namespace>.servicebus.windows.net"
eventhub_name = "my-eventhub"

# 生产者
producer = EventHubProducerClient(
    fully_qualified_namespace=namespace,
    eventhub_name=eventhub_name,
    credential=credential
)

# 消费者
consumer = EventHubConsumerClient(
    fully_qualified_namespace=namespace,
    eventhub_name=eventhub_name,
    consumer_group="$Default",
    credential=credential
)
```

## 客户端类型

| 客户端 | 用途 |
|--------|---------|
| `EventHubProducerClient` | 向 Event Hub 发送事件 |
| `EventHubConsumerClient` | 从 Event Hub 接收事件 |
| `BlobCheckpointStore` | 追踪消费者进度 |

## 发送事件

```python
from azure.eventhub import EventHubProducerClient, EventData
from azure.identity import DefaultAzureCredential

producer = EventHubProducerClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    eventhub_name="my-eventhub",
    credential=DefaultAzureCredential()
)

with producer:
    # 创建批次（处理大小限制）
    event_data_batch = producer.create_batch()
    
    for i in range(10):
        try:
            event_data_batch.add(EventData(f"Event {i}"))
        except ValueError:
            # 批次已满，发送并创建新批次
            producer.send_batch(event_data_batch)
            event_data_batch = producer.create_batch()
            event_data_batch.add(EventData(f"Event {i}"))
    
    # 发送剩余事件
    producer.send_batch(event_data_batch)
```

### 发送到特定分区

```python
# 按分区 ID
event_data_batch = producer.create_batch(partition_id="0")

# 按分区键（一致性哈希）
event_data_batch = producer.create_batch(partition_key="user-123")
```

## 接收事件

### 简单接收

```python
from azure.eventhub import EventHubConsumerClient

def on_event(partition_context, event):
    print(f"Partition: {partition_context.partition_id}")
    print(f"Data: {event.body_as_str()}")
    partition_context.update_checkpoint(event)

consumer = EventHubConsumerClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    eventhub_name="my-eventhub",
    consumer_group="$Default",
    credential=DefaultAzureCredential()
)

with consumer:
    consumer.receive(
        on_event=on_event,
        starting_position="-1",  # 流的开始
    )
```

### 使用 Blob 检查点存储（生产环境）

```python
from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblob import BlobCheckpointStore
from azure.identity import DefaultAzureCredential

checkpoint_store = BlobCheckpointStore(
    blob_account_url="https://<account>.blob.core.windows.net",
    container_name="checkpoints",
    credential=DefaultAzureCredential()
)

consumer = EventHubConsumerClient(
    fully_qualified_namespace="<namespace>.servicebus.windows.net",
    eventhub_name="my-eventhub",
    consumer_group="$Default",
    credential=DefaultAzureCredential(),
    checkpoint_store=checkpoint_store
)

def on_event(partition_context, event):
    print(f"Received: {event.body_as_str()}")
    # 处理后更新检查点
    partition_context.update_checkpoint(event)

with consumer:
    consumer.receive(on_event=on_event)
```

## 异步客户端

```python
from azure.eventhub.aio import EventHubProducerClient, EventHubConsumerClient
from azure.identity.aio import DefaultAzureCredential
import asyncio

async def send_events():
    credential = DefaultAzureCredential()
    
    async with EventHubProducerClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        eventhub_name="my-eventhub",
        credential=credential
    ) as producer:
        batch = await producer.create_batch()
        batch.add(EventData("Async event"))
        await producer.send_batch(batch)

async def receive_events():
    async def on_event(partition_context, event):
        print(event.body_as_str())
        await partition_context.update_checkpoint(event)
    
    async with EventHubConsumerClient(
        fully_qualified_namespace="<namespace>.servicebus.windows.net",
        eventhub_name="my-eventhub",
        consumer_group="$Default",
        credential=DefaultAzureCredential()
    ) as consumer:
        await consumer.receive(on_event=on_event)

asyncio.run(send_events())
```

## 事件属性

```python
event = EventData("My event body")

# 设置属性
event.properties = {"custom_property": "value"}
event.content_type = "application/json"

# 读取属性（接收时）
print(event.body_as_str())
print(event.sequence_number)
print(event.offset)
print(event.enqueued_time)
print(event.partition_key)
```

## 获取 Event Hub 信息

```python
with producer:
    info = producer.get_eventhub_properties()
    print(f"Name: {info['name']}")
    print(f"Partitions: {info['partition_ids']}")
    
    for partition_id in info['partition_ids']:
        partition_info = producer.get_partition_properties(partition_id)
        print(f"Partition {partition_id}: {partition_info['last_enqueued_sequence_number']}")
```

## 最佳实践

1. **使用批次** 发送多个事件
2. **在生产环境中使用检查点存储** 以实现可靠的处理
3. **在高吞吐量场景中使用异步客户端**
4. **使用分区键** 确保分区内的有序交付
5. **处理批次大小限制** — 当批次满时捕获 ValueError
6. **使用上下文管理器** (`with`/`async with`) 以确保正确清理
7. **为不同应用程序设置适当的消费者组**

## 参考文件

| 文件 | 内容 |
|------|----------|
| references/checkpointing.md | 检查点存储模式、Blob 检查点、检查点策略 |
| references/partitions.md | 分区管理、负载平衡、起始位置 |
| scripts/setup_consumer.py | 用于 Event Hub 信息、消费者设置和事件发送/接收的 CLI |

## 何时使用

本技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功条件，请停止并寻求澄清。
