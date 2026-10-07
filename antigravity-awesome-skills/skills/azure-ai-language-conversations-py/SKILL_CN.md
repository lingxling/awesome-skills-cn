---
name: azure-ai-language-conversations-py
description: 使用 azure-ai-language-conversations Python SDK 实现对话语言理解（CLU）。当使用 ConversationAnalysisClient 分析对话意图和实体、构建 NLP 功能或集成语言理解到应用时使用。
risk: critical
source: https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/azure-ai-language-conversations-py
source_repo: microsoft/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/microsoft/skills/blob/main/LICENSE
---

# Azure AI Language Conversations for Python
## 何时使用

当需要使用 azure-ai-language-conversations Python SDK 实现对话语言理解（CLU）时使用此技能。当使用 ConversationAnalysisClient 分析对话意图和实体、构建 NLP 功能或集成语言理解到应用时使用。


## 系统提示
你是一位专门从事 Azure AI 服务和自然语言处理的专家 Python 开发人员。
你的任务是帮助用户使用 `azure-ai-language-conversations` SDK 实现对话语言理解（CLU）。

当响应有关 Azure AI Language Conversations 的请求时：
1. 始终使用最新版本的 `azure-ai-language-conversations` SDK。
2. 强调使用带有 `DefaultAzureCredential` 的 `ConversationAnalysisClient`。
3. 提供清晰的代码示例，演示如何构造对话负载。
4. 正确处理异常。

## 认证和生命周期

> **🔑 两条规则适用于下面的每个代码示例：**
>
> 1. **优先使用 `DefaultAzureCredential`。** 它在本地（Azure CLI / VS Code / Developer CLI）和 Azure（托管身份、工作负载身份）中工作，无需代码更改。避免连接字符串、帐户/API 密钥——它们绕过 Entra 审计和轮换。
>    - 本地开发：`DefaultAzureCredential` 按原样工作。
>    - 生产：设置 `AZURE_TOKEN_CREDENTIALS=prod`（或 `AZURE_TOKEN_CREDENTIALS=<specific_credential>`）来限制凭据链至生产安全凭据。
> 2. **在上下文管理器中包装每个客户端** 以便 HTTP 传输、套接字和令牌缓存被确定性释放：
>    - 同步：`with <Client>(...) as client:`
>    - 异步：`async with <Client>(...) as client:` **和** `async with DefaultAzureCredential() as credential:`（来自 `azure.identity.aio`）
>
> 片段可能会缩写此设置，但生产代码应始终遵循两条规则。

`ConversationAnalysisClient` 接受令牌凭据，如 `DefaultAzureCredential`。使用令牌凭据——它在本地（Azure CLI / VS Code / Developer CLI）和 Azure（托管身份、工作负载身份）中工作，无需代码更改。

### 传统：API 密钥（现有密钥化部署）

新代码应使用 `DefaultAzureCredential`。仅当您有尚未迁移到 Entra ID 的现有密钥化部署时，才使用 `AzureKeyCredential`——例如，受管环境仍在完成其 Entra 推出。

```python
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
key = os.environ["AZURE_CONVERSATIONS_KEY"]

with ConversationAnalysisClient(endpoint, AzureKeyCredential(key)) as client:
    # 详见下面的"基本对话分析"获取 analyze_conversation 负载
    ...
```

## 最佳实践
- **选择同步或异步并保持一致。** 不要在同一调用路径中混合 `azure.ai.language.conversations` 同步客户端和 `azure.ai.language.conversations.aio` 异步客户端。每个模块选择一种模式。
- **始终为客户端和异步凭据使用上下文管理器。** 在 `with ConversationAnalysisClient(...) as client:`（同步）或 `async with ConversationAnalysisClient(...) as client:`（异步）中包装每个客户端。对于来自 `azure.identity.aio` 的异步 `DefaultAzureCredential`，也使用 `async with credential:`，以便令牌和传输被清理。
- **使用 `DefaultAzureCredential`** 在本地开发和 Azure 中实现可移植的认证（避免 API 密钥；它们绕过 Entra 审计和轮换）。
- 对端点、项目名称和部署名称使用环境变量。
- 清晰地映射 `conversationItem` 负载中的 `participantId` 和 `id`。

## 示例

### 基本对话分析
```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.language.conversations import ConversationAnalysisClient

endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
project_name = os.environ["AZURE_CONVERSATIONS_PROJECT"]
deployment_name = os.environ["AZURE_CONVERSATIONS_DEPLOYMENT"]

# DefaultAzureCredential 在本地和 Azure 中工作，无需代码更改。
credential = DefaultAzureCredential()

with ConversationAnalysisClient(endpoint, credential) as client:
    query = "Send an email to Carol about the tomorrow's meeting"
    result = client.analyze_conversation(
        task={
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "participantId": "1",
                    "id": "1",
                    "modality": "text",
                    "language": "en",
                    "text": query
                },
                "isLoggingEnabled": False
            },
            "parameters": {
                "projectName": project_name,
                "deploymentName": deployment_name,
                "verbose": True
            }
        }
    )

    print(f"Top intent: {result['result']['prediction']['topIntent']}")

## 限制

- 仅当任务清楚地匹配其上游来源和本地项目背景时使用此技能。
- 在应用更改前验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例视为特定于环境的测试、安全审查或用户对破坏性或昂贵操作的批准的替代品。
