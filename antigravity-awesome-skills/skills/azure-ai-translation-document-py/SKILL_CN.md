---
name: azure-ai-translation-document-py
description: Azure AI 文档翻译 SDK，用于批量翻译文档并保留格式。用于大规模翻译 Word、PDF、Excel、PowerPoint 和其他文档格式。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure AI Document Translation SDK for Python

Azure AI 转译者文档翻译服务的客户端库，支持批量文档翻译并保留格式。

## 安装

```bash
pip install azure-ai-translation-document
```

## 环境变量

```bash
AZURE_DOCUMENT_TRANSLATION_ENDPOINT=https://<resource>.cognitiveservices.azure.com
AZURE_DOCUMENT_TRANSLATION_KEY=<your-api-key>  # 如果使用 API 密钥

# 源和目标文档存储
AZURE_SOURCE_CONTAINER_URL=https://<storage>.blob.core.windows.net/<container>?<sas>
AZURE_TARGET_CONTAINER_URL=https://<storage>.blob.core.windows.net/<container>?<sas>
```

## 认证

### API 密钥

```python
import os
from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["AZURE_DOCUMENT_TRANSLATION_ENDPOINT"]
key = os.environ["AZURE_DOCUMENT_TRANSLATION_KEY"]

client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))
```

### Entra ID（推荐）

```python
from azure.ai.translation.document import DocumentTranslationClient
from azure.identity import DefaultAzureCredential

client = DocumentTranslationClient(
    endpoint=os.environ["AZURE_DOCUMENT_TRANSLATION_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## 基本文档翻译

```python
from azure.ai.translation.document import DocumentTranslationInput, TranslationTarget

source_url = os.environ["AZURE_SOURCE_CONTAINER_URL"]
target_url = os.environ["AZURE_TARGET_CONTAINER_URL"]

# 启动翻译作业
poller = client.begin_translation(
    inputs=[
        DocumentTranslationInput(
            source_url=source_url,
            targets=[
                TranslationTarget(
                    target_url=target_url,
                    language="es"  # 翻译为西班牙语
                )
            ]
        )
    ]
)

# 等待完成
result = poller.result()

print(f"Status: {poller.status()}")
print(f"Documents translated: {poller.details.documents_succeeded_count}")
print(f"Documents failed: {poller.details.documents_failed_count}")
```

## 多个目标语言

```python
poller = client.begin_translation(
    inputs=[
        DocumentTranslationInput(
            source_url=source_url,
            targets=[
                TranslationTarget(target_url=target_url_es, language="es"),
                TranslationTarget(target_url=target_url_fr, language="fr"),
                TranslationTarget(target_url=target_url_de, language="de")
            ]
        )
    ]
)
```

## 翻译单个文档

```python
from azure.ai.translation.document import SingleDocumentTranslationClient

single_client = SingleDocumentTranslationClient(endpoint, AzureKeyCredential(key))

with open("document.docx", "rb") as f:
    document_content = f.read()

result = single_client.translate(
    body=document_content,
    target_language="es",
    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

# 保存翻译后的文档
with open("document_es.docx", "wb") as f:
    f.write(result)
```

## 检查翻译状态

```python
# 获取所有翻译操作
operations = client.list_translation_statuses()

for op in operations:
    print(f"Operation ID: {op.id}")
    print(f"Status: {op.status}")
    print(f"Created: {op.created_on}")
    print(f"Total documents: {op.documents_total_count}")
    print(f"Succeeded: {op.documents_succeeded_count}")
    print(f"Failed: {op.documents_failed_count}")
```

## 列出文档状态

```python
# 获取作业中各个文档的状态
operation_id = poller.id
document_statuses = client.list_document_statuses(operation_id)

for doc in document_statuses:
    print(f"Document: {doc.source_document_url}")
    print(f"  Status: {doc.status}")
    print(f"  Translated to: {doc.translated_to}")
    if doc.error:
        print(f"  Error: {doc.error.message}")
```

## 取消翻译

```python
# 取消正在进行的翻译
client.cancel_translation(operation_id)
```

## 使用词汇表

```python
from azure.ai.translation.document import TranslationGlossary

poller = client.begin_translation(
    inputs=[
        DocumentTranslationInput(
            source_url=source_url,
            targets=[
                TranslationTarget(
                    target_url=target_url,
                    language="es",
                    glossaries=[
                        TranslationGlossary(
                            glossary_url="https://<storage>.blob.core.windows.net/glossary/terms.csv?<sas>",
                            file_format="csv"
                        )
                    ]
                )
            ]
        )
    ]
)
```

## 支持的文档格式

```python
# 获取支持的格式
formats = client.get_supported_document_formats()

for fmt in formats:
    print(f"Format: {fmt.format}")
    print(f"  Extensions: {fmt.file_extensions}")
    print(f"  Content types: {fmt.content_types}")
```

## 支持的语言

```python
# 获取支持的语言
languages = client.get_supported_languages()

for lang in languages:
    print(f"Language: {lang.name} ({lang.code})")
```

## 异步客户端

```python
from azure.ai.translation.document.aio import DocumentTranslationClient
from azure.identity.aio import DefaultAzureCredential

async def translate_documents():
    async with DocumentTranslationClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    ) as client:
        poller = await client.begin_translation(inputs=[...])
        result = await poller.result()
```

## 支持的格式

| 类别 | 格式 |
|----------|---------|
| 文档 | DOCX、PDF、PPTX、XLSX、HTML、TXT、RTF |
| 结构化 | CSV、TSV、JSON、XML |
| 本地化 | XLIFF、XLF、MHTML |

## 存储要求

- 源容器和目标容器必须是 Azure Blob 存储
- 使用具有适当权限的 SAS 令牌：
  - 源：读取、列表
  - 目标：写入、列表

## 最佳实践

1. **使用 SAS 令牌**（具有最小所需权限）
2. **使用 `poller.status()` 监控长时间运行的操作**
3. **通过迭代文档状态处理文档级错误**
4. **使用词汇表**（用于特定领域的术语）
5. **为每种语言分离目标容器**
6. **使用异步客户端**（用于多个并发作业）
7. **在提交文档前检查支持的格式**

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
