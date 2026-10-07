---
name: azure-ai-contentsafety-py
description: Azure AI Content Safety SDK for Python。用于通过多严重性分类检测文本和图像中的有害内容。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure AI Content Safety SDK for Python

检测应用中用户生成和 AI 生成的有害内容。

## 安装

```bash
pip install azure-ai-contentsafety
```

## 环境变量

```bash
CONTENT_SAFETY_ENDPOINT=https://<resource>.cognitiveservices.azure.com
CONTENT_SAFETY_KEY=<your-api-key>
```

## 认证

### API 密钥

```python
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import os

client = ContentSafetyClient(
    endpoint=os.environ["CONTENT_SAFETY_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["CONTENT_SAFETY_KEY"])
)
```

### Entra ID

```python
from azure.ai.contentsafety import ContentSafetyClient
from azure.identity import DefaultAzureCredential

client = ContentSafetyClient(
    endpoint=os.environ["CONTENT_SAFETY_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## 分析文本

```python
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

request = AnalyzeTextOptions(text="Your text content to analyze")
response = client.analyze_text(request)

# 检查每个类别
for category in [TextCategory.HATE, TextCategory.SELF_HARM, 
                 TextCategory.SEXUAL, TextCategory.VIOLENCE]:
    result = next((r for r in response.categories_analysis 
                   if r.category == category), None)
    if result:
        print(f"{category}: severity {result.severity}")
```

## 分析图像

```python
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData
from azure.core.credentials import AzureKeyCredential
import base64

client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

# 从文件
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

request = AnalyzeImageOptions(
    image=ImageData(content=image_data)
)

response = client.analyze_image(request)

for result in response.categories_analysis:
    print(f"{result.category}: severity {result.severity}")
```

### 从 URL 获取图像

```python
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData

request = AnalyzeImageOptions(
    image=ImageData(blob_url="https://example.com/image.jpg")
)

response = client.analyze_image(request)
```

## 文本阻止列表管理

### 创建阻止列表

```python
from azure.ai.contentsafety import BlocklistClient
from azure.ai.contentsafety.models import TextBlocklist
from azure.core.credentials import AzureKeyCredential

blocklist_client = BlocklistClient(endpoint, AzureKeyCredential(key))

blocklist = TextBlocklist(
    blocklist_name="my-blocklist",
    description="Custom terms to block"
)

result = blocklist_client.create_or_update_text_blocklist(
    blocklist_name="my-blocklist",
    options=blocklist
)
```

### 添加阻止项

```python
from azure.ai.contentsafety.models import AddOrUpdateTextBlocklistItemsOptions, TextBlocklistItem

items = AddOrUpdateTextBlocklistItemsOptions(
    blocklist_items=[
        TextBlocklistItem(text="blocked-term-1"),
        TextBlocklistItem(text="blocked-term-2")
    ]
)

result = blocklist_client.add_or_update_blocklist_items(
    blocklist_name="my-blocklist",
    options=items
)
```

### 使用阻止列表进行分析

```python
from azure.ai.contentsafety.models import AnalyzeTextOptions

request = AnalyzeTextOptions(
    text="Text containing blocked-term-1",
    blocklist_names=["my-blocklist"],
    halt_on_blocklist_hit=True
)

response = client.analyze_text(request)

if response.blocklists_match:
    for match in response.blocklists_match:
        print(f"Blocked: {match.blocklist_item_text}")
```

## 严重性级别

文本分析默认返回 4 个严重性级别（0、2、4、6）。对于 8 个级别（0-7）：

```python
from azure.ai.contentsafety.models import AnalyzeTextOptions, AnalyzeTextOutputType

request = AnalyzeTextOptions(
    text="Your text",
    output_type=AnalyzeTextOutputType.EIGHT_SEVERITY_LEVELS
)
```

## 伤害类别

| 类别 | 说明 |
|----------|-------------|
| `Hate` | 基于身份的攻击（种族、宗教、性别等） |
| `Sexual` | 性内容、关系、解剖学 |
| `Violence` | 身体伤害、武器、伤害 |
| `SelfHarm` | 自伤、自杀、饮食失调 |

## 严重性量表

| 级别 | 文本范围 | 图像范围 | 含义 |
|-------|------------|-------------|---------|
| 0 | 安全 | 安全 | 无有害内容 |
| 2 | 低 | 低 | 轻微参考 |
| 4 | 中等 | 中等 | 中等内容 |
| 6 | 高 | 高 | 严重内容 |

## 客户端类型

| 客户端 | 目的 |
|--------|---------|
| `ContentSafetyClient` | 分析文本和图像 |
| `BlocklistClient` | 管理自定义阻止列表 |

## 最佳实践

1. **为特定领域的术语使用阻止列表**
2. **设置适合您用例的严重性阈值**
3. **处理多个类别** — 内容可能以多种方式有害
4. **使用 halt_on_blocklist_hit** 进行即时拒绝
5. **记录分析结果** 用于审计和改进
6. **考虑 8 严重性模式** 用于更细粒度的控制
7. **在向用户展示前进行预调查 AI 输出**

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
