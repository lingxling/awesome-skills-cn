---
name: azure-ai-projects-ts
description: "适用于 Azure AI Foundry 项目的高级 SDK，包含代理、连接、部署和评估功能。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Azure AI Projects SDK for TypeScript

适用于 Azure AI Foundry 项目的高级 SDK，包含代理、连接、部署和评估功能。

## 安装

```bash
npm install @azure/ai-projects @azure/identity
```

用于追踪：
```bash
npm install @azure/monitor-opentelemetry @opentelemetry/api
```

## 环境变量

```bash
AZURE_AI_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
MODEL_DEPLOYMENT_NAME=gpt-4o
```

## 认证

```typescript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";

const client = new AIProjectClient(
  process.env.AZURE_AI_PROJECT_ENDPOINT!,
  new DefaultAzureCredential()
);
```

## 操作组

| 组 | 目的 |
|-------|---------|
| `client.agents` | 创建和管理 AI 代理 |
| `client.connections` | 列出已连接的 Azure 资源 |
| `client.deployments` | 列出模型部署 |
| `client.datasets` | 上传和管理数据集 |
| `client.indexes` | 创建和管理搜索索引 |
| `client.evaluators` | 管理评估指标 |
| `client.memoryStores` | 管理代理内存 |

## 获取 OpenAI 客户端

```typescript
const openAIClient = await client.getOpenAIClient();

// 用于响应
const response = await openAIClient.responses.create({
  model: "gpt-4o",
  input: "What is the capital of France?"
});

// 用于对话
const conversation = await openAIClient.conversations.create({
  items: [{ type: "message", role: "user", content: "Hello!" }]
});
```

## 代理

### 创建代理

```typescript
const agent = await client.agents.createVersion("my-agent", {
  kind: "prompt",
  model: "gpt-4o",
  instructions: "You are a helpful assistant."
});
```

### 带工具的代理

```typescript
// 代码解释器
const agent = await client.agents.createVersion("code-agent", {
  kind: "prompt",
  model: "gpt-4o",
  instructions: "You can execute code.",
  tools: [{ type: "code_interpreter", container: { type: "auto" } }]
});

// 文件搜索
const agent = await client.agents.createVersion("search-agent", {
  kind: "prompt",
  model: "gpt-4o",
  tools: [{ type: "file_search", vector_store_ids: [vectorStoreId] }]
});

// 网络搜索
const agent = await client.agents.createVersion("web-agent", {
  kind: "prompt",
  model: "gpt-4o",
  tools: [{
    type: "web_search_preview",
    user_location: { type: "approximate", country: "US", city: "Seattle" }
  }]
});

// Azure AI 搜索
const agent = await client.agents.createVersion("aisearch-agent", {
  kind: "prompt",
  model: "gpt-4o",
  tools: [{
    type: "azure_ai_search",
    azure_ai_search: {
      indexes: [{
        project_connection_id: connectionId,
        index_name: "my-index",
        query_type: "simple"
      }]
    }
  }]
});

// 函数工具
const agent = await client.agents.createVersion("func-agent", {
  kind: "prompt",
  model: "gpt-4o",
  tools: [{
    type: "function",
    function: {
      name: "get_weather",
      description: "Get weather for a location",
      strict: true,
      parameters: {
        type: "object",
        properties: { location: { type: "string" } },
        required: ["location"]
      }
    }
  }]
});

// MCP 工具
const agent = await client.agents.createVersion("mcp-agent", {
  kind: "prompt",
  model: "gpt-4o",
  tools: [{
    type: "mcp",
    server_label: "my-mcp",
    server_url: "https://mcp-server.example.com",
    require_approval: "always"
  }]
});
```

### 运行代理

```typescript
const openAIClient = await client.getOpenAIClient();

// 创建对话
const conversation = await openAIClient.conversations.create({
  items: [{ type: "message", role: "user", content: "Hello!" }]
});

// 使用代理生成响应
const response = await openAIClient.responses.create(
  { conversation: conversation.id },
  { body: { agent: { name: agent.name, type: "agent_reference" } } }
);

// 清理资源
await openAIClient.conversations.delete(conversation.id);
await client.agents.deleteVersion(agent.name, agent.version);
```

## 连接

```typescript
// 列出所有连接
for await (const conn of client.connections.list()) {
  console.log(conn.name, conn.type);
}

// 按名称获取连接
const conn = await client.connections.get("my-connection");

// 获取带凭证的连接
const connWithCreds = await client.connections.getWithCredentials("my-connection");

// 按类型获取默认连接
const defaultAzureOpenAI = await client.connections.getDefault("AzureOpenAI", true);
```

## 部署

```typescript
// 列出所有部署
for await (const deployment of client.deployments.list()) {
  if (deployment.type === "ModelDeployment") {
    console.log(deployment.name, deployment.modelName);
  }
}

// 按发布者筛选
for await (const d of client.deployments.list({ modelPublisher: "OpenAI" })) {
  console.log(d.name);
}

// 获取特定部署
const deployment = await client.deployments.get("gpt-4o");
```

## 数据集

```typescript
// 上传单个文件
const dataset = await client.datasets.uploadFile(
  "my-dataset",
  "1.0",
  "./data/training.jsonl"
);

// 上传文件夹
const dataset = await client.datasets.uploadFolder(
  "my-dataset",
  "2.0",
  "./data/documents/"
);

// 获取数据集
const ds = await client.datasets.get("my-dataset", "1.0");

// 列出版本
for await (const version of client.datasets.listVersions("my-dataset")) {
  console.log(version);
}

// 删除
await client.datasets.delete("my-dataset", "1.0");
```

## 索引

```typescript
import { AzureAISearchIndex } from "@azure/ai-projects";

const indexConfig: AzureAISearchIndex = {
  name: "my-index",
  type: "AzureSearch",
  version: "1",
  indexName: "my-index",
  connectionName: "search-connection"
};

// 创建索引
const index = await client.indexes.createOrUpdate("my-index", "1", indexConfig);

// 列出索引
for await (const idx of client.indexes.list()) {
  console.log(idx.name);
}

// 删除
await client.indexes.delete("my-index", "1");
```

## 关键类型

```typescript
import {
  AIProjectClient,
  AIProjectClientOptionalParams,
  Connection,
  ModelDeployment,
  DatasetVersionUnion,
  AzureAISearchIndex
} from "@azure/ai-projects";
```

## 最佳实践

1. **使用 getOpenAIClient()** - 用于响应、对话、文件和向量存储
2. **为代理设置版本** - 使用 `createVersion` 以获得可重现的代理定义
3. **清理资源** - 完成后删除代理、对话
4. **使用连接** - 从项目连接获取凭证，不要硬编码
5. **筛选部署** - 使用 `modelPublisher` 筛选器查找特定模型

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
