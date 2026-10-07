---
name: azure-eventgrid-py
description: Azure Event Grid Python SDK。用于发布事件、处理 CloudEvents 和构建事件驱动的架构。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Event Grid Python SDK

用于构建事件驱动应用程序并实现发布/订阅语义的事件路由服务。

## 安装

```bash
pip install azure-eventgrid azure-identity
```

## 环境变量

```bash
EVENTGRID_TOPIC_ENDPOINT=https://<topic-name>.<region>.eventgrid.azure.net/api/events
EVENTGRID_NAMESPACE_ENDPOINT=https://<namespace>.<region>.eventgrid.azure.net
```

## 身份验证

```python
from azure.identity import DefaultAzureCredential
from azure.eventgrid import EventGridPublisherClient

credential = DefaultAzureCredential()
endpoint = "https://<topic-name>.<region>.eventgrid.azure.net/api/events"

client = EventGridPublisherClient(endpoint, credential)
```

## 事件类型

| 格式 | 类 | 用例 |
|--------|-------|----------|
| Cloud Events 1.0 | `CloudEvent` | 标准、可互操作（推荐） |
| Event Grid Schema | `EventGridEvent` | Azure 原生格式 |

## 发布 CloudEvents

```python
from azure.eventgrid import EventGridPublisherClient, CloudEvent
from azure.identity import DefaultAzureCredential

client = EventGridPublisherClient(endpoint, DefaultAzureCredential())

# 单个事件
event = CloudEvent(
    type="MyApp.Events.OrderCreated",
    source="/myapp/orders",
    data={"order_id": "12345", "amount": 99.99}
)
client.send(event)

# 多个事件
events = [
    CloudEvent(
        type="MyApp.Events.OrderCreated",
        source="/myapp/orders",
        data={"order_id": f"order-{i}"}
    )
    for i in range(10)
]
client.send(events)
```

## 发布 EventGridEvents

```python
from azure.eventgrid import EventGridEvent
from datetime import datetime, timezone

event = EventGridEvent(
    subject="/myapp/orders/12345",
    event_type="MyApp.Events.OrderCreated",
    data={"order_id": "12345", "amount": 99.99},
    data_version="1.0"
)

client.send(event)
```

## 事件属性

### CloudEvent 属性

```python
event = CloudEvent(
    type="MyApp.Events.ItemCreated",      # 必需：事件类型
    source="/myapp/items",                 # 必需：事件来源
    data={"key": "value"},                 # 事件有效载荷
    subject="items/123",                   # 可选：主题/路径
    datacontenttype="application/json",   # 可选：内容类型
    dataschema="https://schema.example",  # 可选：模式 URL
    time=datetime.now(timezone.utc),      # 可选：时间戳
    extensions={"custom": "value"}         # 可选：自定义属性
)
```

### EventGridEvent 属性

```python
event = EventGridEvent(
    subject="/myapp/items/123",            # 必需：主题
    event_type="MyApp.ItemCreated",        # 必需：事件类型
    data={"key": "value"},                 # 必需：事件有效载荷
    data_version="1.0",                    # 必需：架构版本
    topic="/subscriptions/.../topics/...", # 可选：自动设置
    event_time=datetime.now(timezone.utc)  # 可选：时间戳
)
```

## 异步客户端

```python
from azure.eventgrid.aio import EventGridPublisherClient
from azure.identity.aio import DefaultAzureCredential

async def publish_events():
    credential = DefaultAzureCredential()
    
    async with EventGridPublisherClient(endpoint, credential) as client:
        event = CloudEvent(
            type="MyApp.Events.Test",
            source="/myapp",
            data={"message": "hello"}
        )
        await client.send(event)

import asyncio
asyncio.run(publish_events())
```

## 命名空间主题（Event Grid 命名空间）

对于 Event Grid 命名空间（拉取交付）：

```python
from azure.eventgrid.aio import EventGridPublisherClient

# 命名空间端点（不同于自定义主题）
namespace_endpoint = "https://<namespace>.<region>.eventgrid.azure.net"
topic_name = "my-topic"

async with EventGridPublisherClient(
    endpoint=namespace_endpoint,
    credential=DefaultAzureCredential()
) as client:
    await client.send(
        event,
        namespace_topic=topic_name
    )
```

## 最佳实践

1. **使用 CloudEvents** 处理新应用程序（行业标准）
2. **批量发布事件** 处理多个事件时
3. **包含有意义的主题** 用于过滤
4. **使用异步客户端** 用于高吞吐量场景
5. **处理重试** — Event Grid 有内置重试机制
6. **设置适当的事件类型** 用于路由和过滤

## 何时使用

本技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功条件，请停止并寻求澄清。
