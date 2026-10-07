---
name: azure-eventhub-ts
description: "高吞吐量事件流和实时数据摄取。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Azure Event Hubs TypeScript SDK

高吞吐量事件流和实时数据摄取。

## 安装

```bash
npm install @azure/event-hubs @azure/identity
```

对于消费者组的检查点：
```bash
npm install @azure/eventhubs-checkpointstore-blob @azure/storage-blob
```

## 环境变量

```bash
EVENTHUB_NAMESPACE=<namespace>.servicebus.windows.net
EVENTHUB_NAME=my-eventhub
STORAGE_ACCOUNT_NAME=<storage-account>
STORAGE_CONTAINER_NAME=checkpoints
```

## 身份验证

```typescript
import { EventHubProducerClient, EventHubConsumerClient } from "@azure/event-hubs";
import { DefaultAzureCredential } from "@azure/identity";

const fullyQualifiedNamespace = process.env.EVENTHUB_NAMESPACE!;
const eventHubName = process.env.EVENTHUB_NAME!;
const credential = new DefaultAzureCredential();

// 生产者
const producer = new EventHubProducerClient(fullyQualifiedNamespace, eventHubName, credential);

// 消费者
const consumer = new EventHubConsumerClient(
  "$Default", // 消费者组
  fullyQualifiedNamespace,
  eventHubName,
  credential
);
```

## 核心工作流

### 发送事件

```typescript
const producer = new EventHubProducerClient(namespace, eventHubName, credential);

// 创建批次并添加事件
const batch = await producer.createBatch();
batch.tryAdd({ body: { temperature: 72.5, deviceId: "sensor-1" } });
batch.tryAdd({ body: { temperature: 68.2, deviceId: "sensor-2" } });

await producer.sendBatch(batch);
await producer.close();
```

### 发送到特定分区

```typescript
// 按分区 ID
const batch = await producer.createBatch({ partitionId: "0" });

// 按分区键（一致性哈希）
const batch = await producer.createBatch({ partitionKey: "device-123" });
```

### 接收事件（简单）

```typescript
const consumer = new EventHubConsumerClient("$Default", namespace, eventHubName, credential);

const subscription = consumer.subscribe({
  processEvents: async (events, context) => {
    for (const event of events) {
      console.log(`Partition: ${context.partitionId}, Body: ${JSON.stringify(event.body)}`);
    }
  },
  processError: async (err, context) => {
    console.error(`Error on partition ${context.partitionId}: ${err.message}`);
  },
});

// 一段时间后停止
setTimeout(async () => {
  await subscription.close();
  await consumer.close();
}, 60000);
```

### 接收并检查点（生产环境）

```typescript
import { EventHubConsumerClient } from "@azure/event-hubs";
import { ContainerClient } from "@azure/storage-blob";
import { BlobCheckpointStore } from "@azure/eventhubs-checkpointstore-blob";

const containerClient = new ContainerClient(
  `https://${storageAccount}.blob.core.windows.net/${containerName}`,
  credential
);

const checkpointStore = new BlobCheckpointStore(containerClient);

const consumer = new EventHubConsumerClient(
  "$Default",
  namespace,
  eventHubName,
  credential,
  checkpointStore
);

const subscription = consumer.subscribe({
  processEvents: async (events, context) => {
    for (const event of events) {
      console.log(`Processing: ${JSON.stringify(event.body)}`);
    }
    // 处理批次后检查点
    if (events.length > 0) {
      await context.updateCheckpoint(events[events.length - 1]);
    }
  },
  processError: async (err, context) => {
    console.error(`Error: ${err.message}`);
  },
});
```

### 从特定位置接收

```typescript
const subscription = consumer.subscribe({
  processEvents: async (events, context) => { /* ... */ },
  processError: async (err, context) => { /* ... */ },
}, {
  startPosition: {
    // 从开始
    "0": { offset: "@earliest" },
    // 从末尾（仅新事件）
    "1": { offset: "@latest" },
    // 从特定偏移
    "2": { offset: "12345" },
    // 从特定时间
    "3": { enqueuedOn: new Date("2024-01-01") },
  },
});
```

## Event Hub 属性

```typescript
// 获取中心信息
const hubProperties = await producer.getEventHubProperties();
console.log(`Partitions: ${hubProperties.partitionIds}`);

// 获取分区信息
const partitionProperties = await producer.getPartitionProperties("0");
console.log(`Last sequence: ${partitionProperties.lastEnqueuedSequenceNumber}`);
```

## 批处理选项

```typescript
const subscription = consumer.subscribe(
  {
    processEvents: async (events, context) => { /* ... */ },
    processError: async (err, context) => { /* ... */ },
  },
  {
    maxBatchSize: 100,           // 每批最大事件数
    maxWaitTimeInSeconds: 30,    // 批次最大等待时间
  }
);
```

## 关键类型

```typescript
import {
  EventHubProducerClient,
  EventHubConsumerClient,
  EventData,
  ReceivedEventData,
  PartitionContext,
  Subscription,
  SubscriptionEventHandlers,
  CreateBatchOptions,
  EventPosition,
} from "@azure/event-hubs";

import { BlobCheckpointStore } from "@azure/eventhubs-checkpointstore-blob";
```

## 事件属性

```typescript
// 发送属性
const batch = await producer.createBatch();
batch.tryAdd({
  body: { data: "payload" },
  properties: {
    eventType: "telemetry",
    deviceId: "sensor-1",
  },
  contentType: "application/json",
  correlationId: "request-123",
});

// 在接收器中访问
consumer.subscribe({
  processEvents: async (events, context) => {
    for (const event of events) {
      console.log(`Type: ${event.properties?.eventType}`);
      console.log(`Sequence: ${event.sequenceNumber}`);
      console.log(`Enqueued: ${event.enqueuedTimeUtc}`);
      console.log(`Offset: ${event.offset}`);
    }
  },
});
```

## 错误处理

```typescript
consumer.subscribe({
  processEvents: async (events, context) => {
    try {
      for (const event of events) {
        await processEvent(event);
      }
      await context.updateCheckpoint(events[events.length - 1]);
    } catch (error) {
      // 出错时不检查点 - 事件将被重新处理
      console.error("Processing failed:", error);
    }
  },
  processError: async (err, context) => {
    if (err.name === "MessagingError") {
      // 瞬时错误 - SDK 将重试
      console.warn("Transient error:", err.message);
    } else {
      // 致命错误
      console.error("Fatal error:", err);
    }
  },
});
```

## 最佳实践

1. **使用检查点** - 在生产环境中始终检查点以实现恰好一次处理
2. **批量发送** - 使用 `createBatch()` 以高效发送
3. **分区键** - 使用分区键确保相关事件的顺序
4. **消费者组** - 为不同的处理管道使用单独的消费者组
5. **优雅地处理错误** - 在处理失败时不检查点
6. **关闭客户端** - 完成后始终关闭生产者/消费者
7. **监控延迟** - 追踪 `lastEnqueuedSequenceNumber` 与已处理序列

## 何时使用

本技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代。
- 如果缺少必需的输入、权限、安全边界或成功条件，请停止并寻求澄清。
