---
name: azure-ai-projects-java
description: Azure AI Projects SDK for Java。用于 Azure AI Foundry 项目管理的高级 SDK，包括连接、数据集、索引和评估。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure AI Projects SDK for Java

用于 Azure AI Foundry 项目管理的高级 SDK，可访问连接、数据集、索引和评估。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-projects</artifactId>
    <version>1.0.0-beta.1</version>
</dependency>
```

## 环境变量

```bash
PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
```

## 认证

```java
import com.azure.ai.projects.AIProjectClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

AIProjectClientBuilder builder = new AIProjectClientBuilder()
    .endpoint(System.getenv("PROJECT_ENDPOINT"))
    .credential(new DefaultAzureCredentialBuilder().build());
```

## 客户端层次结构

SDK 为不同的操作提供了多个子客户端：

| 客户端 | 目的 |
|--------|---------|
| `ConnectionsClient` | 枚举连接的 Azure 资源 |
| `DatasetsClient` | 上传文档和管理数据集 |
| `DeploymentsClient` | 枚举 AI 模型部署 |
| `IndexesClient` | 创建和管理搜索索引 |
| `EvaluationsClient` | 运行 AI 模型评估 |
| `EvaluatorsClient` | 管理评估程序配置 |
| `SchedulesClient` | 管理计划操作 |

```java
// 从构建器构建子客户端
ConnectionsClient connectionsClient = builder.buildConnectionsClient();
DatasetsClient datasetsClient = builder.buildDatasetsClient();
DeploymentsClient deploymentsClient = builder.buildDeploymentsClient();
IndexesClient indexesClient = builder.buildIndexesClient();
EvaluationsClient evaluationsClient = builder.buildEvaluationsClient();
```

## 核心操作

### 列出连接

```java
import com.azure.ai.projects.models.Connection;
import com.azure.core.http.rest.PagedIterable;

PagedIterable<Connection> connections = connectionsClient.listConnections();
for (Connection connection : connections) {
    System.out.println("Name: " + connection.getName());
    System.out.println("Type: " + connection.getType());
    System.out.println("Credential Type: " + connection.getCredentials().getType());
}
```

### 列出索引

```java
indexesClient.listLatest().forEach(index -> {
    System.out.println("Index name: " + index.getName());
    System.out.println("Version: " + index.getVersion());
    System.out.println("Description: " + index.getDescription());
});
```

### 创建或更新索引

```java
import com.azure.ai.projects.models.AzureAISearchIndex;
import com.azure.ai.projects.models.Index;

String indexName = "my-index";
String indexVersion = "1.0";
String searchConnectionName = System.getenv("AI_SEARCH_CONNECTION_NAME");
String searchIndexName = System.getenv("AI_SEARCH_INDEX_NAME");

Index index = indexesClient.createOrUpdate(
    indexName,
    indexVersion,
    new AzureAISearchIndex()
        .setConnectionName(searchConnectionName)
        .setIndexName(searchIndexName)
);

System.out.println("Created index: " + index.getName());
```

### 访问 OpenAI 评估

SDK 公开了 OpenAI 用于评估的官方 SDK：

```java
import com.openai.services.EvalService;

EvalService evalService = evaluationsClient.getOpenAIClient();
// 直接使用 OpenAI 评估 API
```

## 最佳实践

1. **为生产认证使用 DefaultAzureCredential**
2. **重用客户端构建器** 以高效创建多个子客户端
3. **在使用 `PagedIterable` 列出资源时处理分页**
4. **对连接名称和配置使用环境变量**
5. **在访问凭据前检查连接类型**

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;
import com.azure.core.exception.ResourceNotFoundException;

try {
    Index index = indexesClient.get(indexName, version);
} catch (ResourceNotFoundException e) {
    System.err.println("Index not found: " + indexName);
} catch (HttpResponseException e) {
    System.err.println("Error: " + e.getResponse().getStatusCode());
}
```

## 参考链接

| 资源 | URL |
|----------|-----|
| 产品文档 | https://learn.microsoft.com/azure/ai-studio/ |
| API 参考 | https://learn.microsoft.com/rest/api/aifoundry/aiprojects/ |
| GitHub 源 | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-projects |
| 示例 | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-projects/src/samples |

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
