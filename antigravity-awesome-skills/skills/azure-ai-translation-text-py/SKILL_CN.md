---
name: azure-ai-translation-text-py
description: Azure AI 文本翻译 SDK，用于实时文本翻译、音译、语言检测和词典查询。用于在应用程序中翻译文本内容。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure AI Text Translation SDK for Python

Azure AI 转译者文本翻译服务的客户端库，用于实时文本翻译、音译和语言操作。

## 安装

```bash
pip install azure-ai-translation-text
```

## 环境变量

```bash
AZURE_TRANSLATOR_KEY=<your-api-key>
AZURE_TRANSLATOR_REGION=<your-region>  # 例如：eastus、westus2
# 或使用自定义端点
AZURE_TRANSLATOR_ENDPOINT=https://<resource>.cognitiveservices.azure.com
```

## 认证

### 带区域的 API 密钥

```python
import os
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

key = os.environ["AZURE_TRANSLATOR_KEY"]
region = os.environ["AZURE_TRANSLATOR_REGION"]

# 创建带区域的凭证
credential = AzureKeyCredential(key)
client = TextTranslationClient(credential=credential, region=region)
```

### 带自定义端点的 API 密钥

```python
endpoint = os.environ["AZURE_TRANSLATOR_ENDPOINT"]

client = TextTranslationClient(
    credential=AzureKeyCredential(key),
    endpoint=endpoint
)
```

### Entra ID（推荐）

```python
from azure.ai.translation.text import TextTranslationClient
from azure.identity import DefaultAzureCredential

client = TextTranslationClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["AZURE_TRANSLATOR_ENDPOINT"]
)
```

## 基本翻译

```python
# 翻译为单一语言
result = client.translate(
    body=["Hello, how are you?", "Welcome to Azure!"],
    to=["es"]  # 西班牙语
)

for item in result:
    for translation in item.translations:
        print(f"Translated: {translation.text}")
        print(f"Target language: {translation.to}")
```

## 翻译为多种语言

```python
result = client.translate(
    body=["Hello, world!"],
    to=["es", "fr", "de", "ja"]  # 西班牙语、法语、德语、日语
)

for item in result:
    print(f"Source: {item.detected_language.language if item.detected_language else 'unknown'}")
    for translation in item.translations:
        print(f"  {translation.to}: {translation.text}")
```

## 指定源语言

```python
result = client.translate(
    body=["Bonjour le monde"],
    from_parameter="fr",  # 源语言是法语
    to=["en", "es"]
)
```

## 语言检测

```python
result = client.translate(
    body=["Hola, como estas?"],
    to=["en"]
)

for item in result:
    if item.detected_language:
        print(f"Detected language: {item.detected_language.language}")
        print(f"Confidence: {item.detected_language.score:.2f}")
```

## 音译

将文本从一种脚本转换为另一种脚本：

```python
result = client.transliterate(
    body=["konnichiwa"],
    language="ja",
    from_script="Latn",  # 从拉丁文字
    to_script="Jpan"      # 到日语文字
)

for item in result:
    print(f"Transliterated: {item.text}")
    print(f"Script: {item.script}")
```

## 词典查询

查找替代翻译和定义：

```python
result = client.lookup_dictionary_entries(
    body=["fly"],
    from_parameter="en",
    to="es"
)

for item in result:
    print(f"Source: {item.normalized_source} ({item.display_source})")
    for translation in item.translations:
        print(f"  Translation: {translation.normalized_target}")
        print(f"  Part of speech: {translation.pos_tag}")
        print(f"  Confidence: {translation.confidence:.2f}")
```

## 词典示例

获取翻译的用法示例：

```python
from azure.ai.translation.text.models import DictionaryExampleTextItem

result = client.lookup_dictionary_examples(
    body=[DictionaryExampleTextItem(text="fly", translation="volar")],
    from_parameter="en",
    to="es"
)

for item in result:
    for example in item.examples:
        print(f"Source: {example.source_prefix}{example.source_term}{example.source_suffix}")
        print(f"Target: {example.target_prefix}{example.target_term}{example.target_suffix}")
```

## 获取支持的语言

```python
# 获取所有支持的语言
languages = client.get_supported_languages()

# 翻译语言
print("Translation languages:")
for code, lang in languages.translation.items():
    print(f"  {code}: {lang.name} ({lang.native_name})")

# 音译语言
print("\nTransliteration languages:")
for code, lang in languages.transliteration.items():
    print(f"  {code}: {lang.name}")
    for script in lang.scripts:
        print(f"    {script.code} -> {[t.code for t in script.to_scripts]}")

# 词典语言
print("\nDictionary languages:")
for code, lang in languages.dictionary.items():
    print(f"  {code}: {lang.name}")
```

## 识别句子边界

识别句子边界：

```python
result = client.find_sentence_boundaries(
    body=["Hello! How are you? I hope you are well."],
    language="en"
)

for item in result:
    print(f"Sentence lengths: {item.sent_len}")
```

## 翻译选项

```python
result = client.translate(
    body=["Hello, world!"],
    to=["de"],
    text_type="html",           # "plain" 或 "html"
    profanity_action="Marked",  # "NoAction"、"Deleted"、"Marked"
    profanity_marker="Asterisk", # "Asterisk"、"Tag"
    include_alignment=True,      # 包括字对齐
    include_sentence_length=True # 包括句子边界
)

for item in result:
    translation = item.translations[0]
    print(f"Translated: {translation.text}")
    if translation.alignment:
        print(f"Alignment: {translation.alignment.proj}")
    if translation.sent_len:
        print(f"Sentence lengths: {translation.sent_len.src_sent_len}")
```

## 异步客户端

```python
from azure.ai.translation.text.aio import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

async def translate_text():
    async with TextTranslationClient(
        credential=AzureKeyCredential(key),
        region=region
    ) as client:
        result = await client.translate(
            body=["Hello, world!"],
            to=["es"]
        )
        print(result[0].translations[0].text)
```

## 客户端方法

| 方法 | 描述 |
|--------|-------------|
| `translate` | 将文本翻译为一种或多种语言 |
| `transliterate` | 在脚本之间转换文本 |
| `detect` | 检测文本语言 |
| `find_sentence_boundaries` | 识别句子边界 |
| `lookup_dictionary_entries` | 词典查询以获取翻译 |
| `lookup_dictionary_examples` | 获取使用示例 |
| `get_supported_languages` | 列出支持的语言 |

## 最佳实践

1. **批量翻译** — 在一个请求中发送多个文本（最多 100 个）
2. **在已知时指定源语言**以提高准确性
3. **对高吞吐量场景使用异步客户端**
4. **缓存语言列表** — 支持的语言不会经常更改
5. **适当处理不当内容**（根据您的应用程序需要）
6. **在翻译 HTML 内容时使用 html text_type**
7. **包括对齐**（用于需要字映射的应用程序）

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
