---
name: azure-ai-textanalytics-py
description: Azure AI 文本分析 SDK，用于情感分析、实体识别、关键短语、语言检测、PII 检测和医疗保健 NLP。用于对文本进行自然语言处理。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure AI Text Analytics SDK for Python

Azure AI 语言服务 NLP 功能的客户端库，包括情感分析、实体识别、关键短语等。

## 安装

```bash
pip install azure-ai-textanalytics
```

## 环境变量

```bash
AZURE_LANGUAGE_ENDPOINT=https://<resource>.cognitiveservices.azure.com
AZURE_LANGUAGE_KEY=<your-api-key>  # 如果使用 API 密钥
```

## 认证

### API 密钥

```python
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
key = os.environ["AZURE_LANGUAGE_KEY"]

client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))
```

### Entra ID（推荐）

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential

client = TextAnalyticsClient(
    endpoint=os.environ["AZURE_LANGUAGE_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## 情感分析

```python
documents = [
    "I had a wonderful trip to Seattle last week!",
    "The food was terrible and the service was slow."
]

result = client.analyze_sentiment(documents, show_opinion_mining=True)

for doc in result:
    if not doc.is_error:
        print(f"Sentiment: {doc.sentiment}")
        print(f"Scores: pos={doc.confidence_scores.positive:.2f}, "
              f"neg={doc.confidence_scores.negative:.2f}, "
              f"neu={doc.confidence_scores.neutral:.2f}")
        
        # 意见挖掘（基于方面的情感）
        for sentence in doc.sentences:
            for opinion in sentence.mined_opinions:
                target = opinion.target
                print(f"  Target: '{target.text}' - {target.sentiment}")
                for assessment in opinion.assessments:
                    print(f"    Assessment: '{assessment.text}' - {assessment.sentiment}")
```

## 实体识别

```python
documents = ["Microsoft was founded by Bill Gates and Paul Allen in Albuquerque."]

result = client.recognize_entities(documents)

for doc in result:
    if not doc.is_error:
        for entity in doc.entities:
            print(f"Entity: {entity.text}")
            print(f"  Category: {entity.category}")
            print(f"  Subcategory: {entity.subcategory}")
            print(f"  Confidence: {entity.confidence_score:.2f}")
```

## PII 检测

```python
documents = ["My SSN is 123-45-6789 and my email is john@example.com"]

result = client.recognize_pii_entities(documents)

for doc in result:
    if not doc.is_error:
        print(f"Redacted: {doc.redacted_text}")
        for entity in doc.entities:
            print(f"PII: {entity.text} ({entity.category})")
```

## 关键短语提取

```python
documents = ["Azure AI provides powerful machine learning capabilities for developers."]

result = client.extract_key_phrases(documents)

for doc in result:
    if not doc.is_error:
        print(f"Key phrases: {doc.key_phrases}")
```

## 语言检测

```python
documents = ["Ce document est en francais.", "This is written in English."]

result = client.detect_language(documents)

for doc in result:
    if not doc.is_error:
        print(f"Language: {doc.primary_language.name} ({doc.primary_language.iso6391_name})")
        print(f"Confidence: {doc.primary_language.confidence_score:.2f}")
```

## 医疗保健文本分析

```python
documents = ["Patient has diabetes and was prescribed metformin 500mg twice daily."]

poller = client.begin_analyze_healthcare_entities(documents)
result = poller.result()

for doc in result:
    if not doc.is_error:
        for entity in doc.entities:
            print(f"Entity: {entity.text}")
            print(f"  Category: {entity.category}")
            print(f"  Normalized: {entity.normalized_text}")
            
            # 实体链接 (UMLS 等)
            for link in entity.data_sources:
                print(f"  Link: {link.name} - {link.entity_id}")
```

## 批量多重分析

```python
from azure.ai.textanalytics import (
    RecognizeEntitiesAction,
    ExtractKeyPhrasesAction,
    AnalyzeSentimentAction
)

documents = ["Microsoft announced new Azure AI features at Build conference."]

poller = client.begin_analyze_actions(
    documents,
    actions=[
        RecognizeEntitiesAction(),
        ExtractKeyPhrasesAction(),
        AnalyzeSentimentAction()
    ]
)

results = poller.result()
for doc_results in results:
    for result in doc_results:
        if result.kind == "EntityRecognition":
            print(f"Entities: {[e.text for e in result.entities]}")
        elif result.kind == "KeyPhraseExtraction":
            print(f"Key phrases: {result.key_phrases}")
        elif result.kind == "SentimentAnalysis":
            print(f"Sentiment: {result.sentiment}")
```

## 异步客户端

```python
from azure.ai.textanalytics.aio import TextAnalyticsClient
from azure.identity.aio import DefaultAzureCredential

async def analyze():
    async with TextAnalyticsClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    ) as client:
        result = await client.analyze_sentiment(documents)
        # 处理结果...
```

## 客户端类型

| 客户端 | 目的 |
|--------|---------|
| `TextAnalyticsClient` | 所有文本分析操作 |
| `TextAnalyticsClient` (aio) | 异步版本 |

## 可用操作

| 方法 | 描述 |
|--------|-------------|
| `analyze_sentiment` | 情感分析和意见挖掘 |
| `recognize_entities` | 命名实体识别 |
| `recognize_pii_entities` | PII 检测和编辑 |
| `recognize_linked_entities` | 实体链接到 Wikipedia |
| `extract_key_phrases` | 关键短语提取 |
| `detect_language` | 语言检测 |
| `begin_analyze_healthcare_entities` | 医疗保健 NLP（长时间运行） |
| `begin_analyze_actions` | 批量多重分析 |

## 最佳实践

1. **对多个文档使用批量操作**（每个请求最多 10 个）
2. **启用意见挖掘**以进行详细的基于方面的情感分析
3. **对高吞吐量场景使用异步客户端**
4. **处理文档错误** — 结果列表中可能包含某些文档的错误
5. **在已知时指定语言**以提高准确性
6. **使用上下文管理器**或显式关闭客户端

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
