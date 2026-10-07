---
name: azure-ai-agents-persistent-java
description: Azure AI Agents Persistent SDK for Java。用于创建和管理带有线程、消息、运行和工具的 AI 代理的低级 SDK。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure AI Agents Persistent SDK for Java

用于创建和管理具有线程、消息、运行和工具的持久 AI 代理的低级 SDK。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents-persistent</artifactId>
    <version>1.0.0-beta.1</version>
</dependency>
```

## 环境变量

```bash
PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
MODEL_DEPLOYMENT_NAME=gpt-4o-mini
```

## 认证

```java
import com.azure.ai.agents.persistent.PersistentAgentsClient;
import com.azure.ai.agents.persistent.PersistentAgentsClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

String endpoint = System.getenv("PROJECT_ENDPOINT");
PersistentAgentsClient client = new PersistentAgentsClientBuilder()
    .endpoint(endpoint)
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();
```

## 关键概念

Azure AI Agents Persistent SDK 为管理可以跨会话重用的持久代理提供了低级 API。

### 客户端层次结构

| 客户端 | 目的 |
|--------|---------|
| `PersistentAgentsClient` | 代理操作的同步客户端 |
| `PersistentAgentsAsyncClient` | 代理操作的异步客户端 |

## 核心工作流

### 1. 创建代理

```java
// 使用工具创建代理
PersistentAgent agent = client.createAgent(
    modelDeploymentName,
    "数学导师",
    "You are a personal math tutor."
);
```

### 2. 创建线程

```java
PersistentAgentThread thread = client.createThread();
```

### 3. 添加消息

```java
client.createMessage(
    thread.getId(),
    MessageRole.USER,
    "I need help with equations."
);
```

### 4. 运行代理

```java
ThreadRun run = client.createRun(thread.getId(), agent.getId());

// 轮询完成
while (run.getStatus() == RunStatus.QUEUED || run.getStatus() == RunStatus.IN_PROGRESS) {
    Thread.sleep(500);
    run = client.getRun(thread.getId(), run.getId());
}
```

### 5. 获取响应

```java
PagedIterable<PersistentThreadMessage> messages = client.listMessages(thread.getId());
for (PersistentThreadMessage message : messages) {
    System.out.println(message.getRole() + ": " + message.getContent());
}
```

### 6. 清理

```java
client.deleteThread(thread.getId());
client.deleteAgent(agent.getId());
```

## 最佳实践

1. **为生产认证使用 DefaultAzureCredential**
2. **以适当的延迟轮询** — 建议在状态检查之间 500ms
3. **清理资源** — 完成后删除线程和代理
4. **处理所有运行状态** — 检查 RequiresAction、Failed、Cancelled
5. **在高并发场景中使用异步客户端** 以获得更好的吞吐量

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    PersistentAgent agent = client.createAgent(modelName, name, instructions);
} catch (HttpResponseException e) {
    System.err.println("Error: " + e.getResponse().getStatusCode() + " - " + e.getMessage());
}
```

## 参考链接

| 资源 | URL |
|----------|-----|
| Maven 软件包 | https://central.sonatype.com/artifact/com.azure/azure-ai-agents-persistent |
| GitHub 源 | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-agents-persistent |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
