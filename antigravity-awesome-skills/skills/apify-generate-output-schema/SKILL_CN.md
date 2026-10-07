---
name: apify-generate-output-schema
description: 通过分析 Apify Actor 的源代码，为其生成输出 schema（dataset_schema.json、output_schema.json、key_value_store_schema.json）。在创建或更新
  Actor 输出 schema 时使用。
source_repo: apify/agent-skills
source_type: official
source: apify
date_added: '2026-09-21'
risk: unknown
---
## 何时使用
- 当该上游工作流与用户陈述的目标相符时使用。
- 当任务需要本 skill 所记录的流程时使用。

# 生成 Actor 输出 schema

你正在为一个 Apify Actor 生成输出 schema 文件。输出 schema 告诉 Apify Console 如何展示运行结果。你需要分析该 Actor 的源代码,创建 `dataset_schema.json`、`output_schema.json`,以及(如果该 Actor 使用了 key-value store)`key_value_store_schema.json`,并更新 `actor.json`。

## 核心原则

- **先分析代码**:阅读 Actor 的源代码以了解它实际推送到 dataset 的数据——绝不要猜测
- **每个字段都是可为空的**:API 和网站是不可预测的——始终设置 `"nullable": true`
- **匿名化示例**:示例中绝不使用真实的用户 ID、用户名或个人数据
- **对照代码验证**:如果存在 TypeScript 类型,要同时对照类型定义和生成这些值的代码来交叉检查 schema
- **复用现有模式**:在生成 schema 之前,检查同一仓库中的其他 Actor 是否已经有输出 schema——匹配它们的结构、命名约定、描述风格和格式
- **不要重复发明轮子**:复用代码库中已有的类型定义、接口和工具函数,而不是创建重复的定义

---

## 阶段 1:发现 Actor 结构

**目标**:定位 Actor 并理解其输出

初始请求: $ARGUMENTS

**操作**:
1. 创建包含所有阶段的待办列表
2. 找到包含 `actor.json` 的 `.actor/` 目录
3. 阅读 `actor.json` 以理解该 Actor 的配置
4. 检查 `dataset_schema.json`、`output_schema.json` 和 `key_value_store_schema.json` 是否已经存在
5. **在仓库中搜索现有 schema**:查找其他 `.actor/` 目录或 schema 文件(例如 `**/dataset_schema.json`、`**/output_schema.json`、`**/key_value_store_schema.json`)以了解该仓库的约定——匹配它们的描述风格、字段命名、示例格式和整体结构
6. 找到所有向 dataset 推送数据的位置:
   - **JavaScript/TypeScript**:搜索 `Actor.pushData(`、`dataset.pushData(`、`Dataset.pushData(`
   - **Python**:搜索 `Actor.push_data(`、`dataset.push_data(`、`Dataset.push_data(`
7. 找到所有在 key-value store 中存储数据的位置:
   - **JavaScript/TypeScript**:搜索 `Actor.setValue(`、`keyValueStore.setValue(`、`KeyValueStore.setValue(`
   - **Python**:搜索 `Actor.set_value(`、`key_value_store.set_value(`、`KeyValueStore.set_value(`
8. 找到输出类型定义——**直接复用它们**,而不是从零开始重新创建:
   - **TypeScript**:查找输出类型接口/类型(例如在 `src/types/`、`src/types/output.ts` 中)。如果某个接口或类型已经定义了输出形态,就从中派生 schema 字段——不要创建并行的定义
   - **Python**:查找 TypedDict、dataclass 或 Pydantic 模型定义。使用现有的字段名、类型和 docstring 作为事实来源
9. 检查代码库中是否存在处理 schema 生成或验证的现有共享 schema 工具或辅助函数——复用它们,而不是创建新逻辑
10. 如果 `actor.json` 中存在内联的 `storages.dataset` 或 `storages.keyValueStore` 配置,记下来以便后续迁移

向用户展示发现结果:列出所有发现的 dataset 输出字段、key-value store 的键、它们的类型,以及它们的来源。

---

## 阶段 2:生成 `dataset_schema.json`

**目标**:创建一个完整的 dataset schema,包含字段定义和展示视图

### 文件结构

```json
{
    "actorSpecification": 1,
    "fields": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            // 所有输出字段都放这里 —— Actor 可能产生的每一个字段,
            // 不仅仅是在概览视图中展示的那些
        },
        "required": [],
        "additionalProperties": true
    },
    "views": {
        "overview": {
            "title": "Overview",
            "description": "Most important fields at a glance",
            "transformation": {
                "fields": [
                    // 8-12 个最重要的字段名
                ]
            },
            "display": {
                "component": "table",
                "properties": {
                    // 每个概览字段的显示配置
                }
            }
        }
    }
}
```

### 与现有 schema 保持一致

如果在阶段 1(第 5 步)中在仓库中发现了现有的输出 schema,遵循它们的约定:
- 匹配**描述的写法风格**(句首大写还是全小写、是否以句号结尾等)
- 匹配**字段命名约定**(camelCase 还是 snake_case)——这也必须与 Actor 代码实际生成的键保持一致
- 匹配**示例值的风格**(例如日期格式、URL 模式、占位名称)
- 匹配**视图结构**(概览中字段数量、展示格式选择)
- 匹配**JSON 格式**(缩进、属性顺序、空格)——同一仓库中的所有 schema 必须使用完全相同的格式,包括独立的 Actor

当 Actor 代码中已经有定义良好的 TypeScript 接口或 Python 类型类时,直接从这些类型派生字段,而不是从头重新分析 pushData/push_data 调用。类型定义是权威来源。

### 硬性规则(无例外)

| 规则 | 详情 |
|------|------|
| **`properties` 中包含所有字段** | `fields.properties` 对象必须包含 Actor **能够**输出的**每一个**字段,而不仅仅是概览视图中展示的字段。views 部分只是选取一个子集用于展示——`properties` 部分必须是完整的超集 |
| `"nullable": true` | 每个字段都要有——API 是不可预测的 |
| `"additionalProperties": true` | 在**顶层 `fields` 对象**上以及 `properties` 中的**每个嵌套对象**上都要有。这是最常被漏掉的规则——两个层级都必须出现 |
| `"required": []` | 始终为空数组——在**顶层 `fields` 对象**上以及 `properties` 中的**每个嵌套对象**上都要有 |
| 匿名化的示例 | 不包含真实的用户 ID、用户名或内容 |
| `"type"` 必须与 `"nullable"` 同时出现 | AJV 会拒绝同一字段上有 `nullable` 但没有 `type` 的情况 |

> **警告 —— 最常见的错误**:
> 1. 只包含出现在概览视图中的字段。`fields.properties` 必须列出所有输出字段,即使它们不在 `views` 部分中。
> 2. 只在嵌套的对象类型属性上添加 `"required": []` 和 `"additionalProperties": true`,却忘了在顶层 `fields` 对象上也添加。两个层级都需要。

> **注意**:`nullable` 是 Apify 对 JSON Schema draft-07 的特有扩展。这是有意为之且正确的。

### 字段类型模式

**字符串字段:**
```json
"title": {
    "type": "string",
    "description": "Title of the scraped item",
    "nullable": true,
    "example": "Example Item Title"
}
```

**数字字段:**
```json
"viewCount": {
    "type": "number",
    "description": "Number of views",
    "nullable": true,
    "example": 15000
}
```

**布尔字段:**
```json
"isVerified": {
    "type": "boolean",
    "description": "Whether the account is verified",
    "nullable": true,
    "example": true
}
```

**数组字段:**
```json
"hashtags": {
    "type": "array",
    "description": "Hashtags associated with the item",
    "items": { "type": "string" },
    "nullable": true,
    "example": ["#example", "#demo"]
}
```

**嵌套对象字段:**
```json
"authorInfo": {
    "type": "object",
    "description": "Information about the author",
    "properties": {
        "name": { "type": "string", "nullable": true },
        "url": { "type": "string", "nullable": true }
    },
    "required": [],
    "additionalProperties": true,
    "nullable": true,
    "example": { "name": "Example Author", "url": "https://example.com/author" }
}
```

**枚举字段:**
```json
"contentType": {
    "type": "string",
    "description": "Type of content",
    "enum": ["article", "video", "image"],
    "nullable": true,
    "example": "article"
}
```

**联合类型(例如 TypeScript 的 `ObjectType | string`):**
```json
"metadata": {
    "type": ["object", "string"],
    "description": "Structured metadata object, or error string if unavailable",
    "nullable": true,
    "example": { "key": "value" }
}
```

### 匿名化示例值

使用真实但通用的值。遵循平台 ID 格式惯例:

| 字段类型 | 示例处理方式 |
|---|---|
| ID | 匹配平台格式和长度(例如 YouTube 视频 ID 为 11 个字符) |
| 用户名 | `"exampleuser"`、`"sampleuser123"` |
| 显示名称 | `"Example Channel"`、`"Sample Author"` |
| URL | 使用平台标准的 URL 格式,配合虚构 ID |
| 日期 | `"2025-01-15T12:00:00.000Z"`(ISO 8601) |
| 文本内容 | 通用的描述性文本,例如 `"This is an example description."` |

### 视图部分

- `transformation.fields`:列出 8–12 个最重要的字段名(顺序 = UI 中的列顺序)
- `display.properties`:为每个概览字段提供一个条目,包含 `label` 和 `format`
- 可用格式:`"text"`、`"number"`、`"date"`、`"link"`、`"boolean"`、`"image"`、`"array"`、`"object"`

选择能为用户提供最有用的数据一览摘要的字段。

---

## 阶段 3:生成 `key_value_store_schema.json`(如适用)

**目标**:如果该 Actor 在 key-value store 中存储数据,定义 key-value store 的集合

> 如果在阶段 1 中没有发现 `Actor.setValue()` / `Actor.set_value()` 调用(默认的 `INPUT` 键之外),**跳过此阶段**。

### 文件结构

```json
{
    "actorKeyValueStoreSchemaVersion": 1,
    "title": "<Descriptive title — what the key-value store contains>",
    "description": "<One sentence describing the stored data>",
    "collections": {
        "<collectionName>": {
            "title": "<Human-readable title>",
            "description": "<What this collection contains>",
            "keyPrefix": "<prefix->"
        }
    }
}
```

### 如何识别集合

按键的模式对发现的 `setValue` / `set_value` 调用进行分组:

1. **固定键**(例如 `"RESULTS"`、`"summary"`)——使用 `"key"`(精确匹配)
2. **带前缀的动态键**(例如 `"screenshot-${id}"`、`f"image-{name}"`)——使用 `"keyPrefix"`

每个分组就是一个集合。

### 集合属性

| 属性 | 是否必需 | 描述 |
|----------|----------|------|
| `title` | 是 | 显示在 UI 标签中 |
| `description` | 否 | 显示在 UI 提示中 |
| `key` | 条件性 | 单键集合的精确键(使用 `key` 或 `keyPrefix`,二者选一) |
| `keyPrefix` | 条件性 | 多键集合的前缀(使用 `key` 或 `keyPrefix`,二者选一) |
| `contentTypes` | 否 | 限制允许的 MIME 类型(例如 `["image/jpeg"]`、`["application/json"]`) |
| `jsonSchema` | 否 | 用于验证 `application/json` 内容的 JSON Schema draft-07 |

### 示例

**单文件输出(例如一份报告):**
```json
{
    "actorKeyValueStoreSchemaVersion": 1,
    "title": "Analysis Results",
    "description": "Key-value store containing analysis output",
    "collections": {
        "report": {
            "title": "Report",
            "description": "Final analysis report",
            "key": "REPORT",
            "contentTypes": ["application/json"]
        }
    }
}
```

**带前缀的多文件(例如截图):**
```json
{
    "actorKeyValueStoreSchemaVersion": 1,
    "title": "Scraped Files",
    "description": "Key-value store containing downloaded files and screenshots",
    "collections": {
        "screenshots": {
            "title": "Screenshots",
            "description": "Page screenshots captured during scraping",
            "keyPrefix": "screenshot-",
            "contentTypes": ["image/png", "image/jpeg"]
        },
        "documents": {
            "title": "Documents",
            "description": "Downloaded document files",
            "keyPrefix": "doc-",
            "contentTypes": ["application/pdf", "text/html"]
        }
    }
}
```

---

## 阶段 4:生成 `output_schema.json`

**目标**:创建输出 schema,告知 Apify Console 在哪里能找到结果

对于大多数将数据推送到 dataset 的 Actor,这是一个极简文件:

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "<Descriptive title — what the Actor returns>",
    "description": "<One sentence describing the output data>",
    "properties": {
        "dataset": {
            "type": "string",
            "title": "Results",
            "description": "Dataset containing all scraped data",
            "template": "{{links.apiDefaultDatasetUrl}}/items"
        }
    }
}
```

> **关键**:每个属性条目**必须**包含 `"type": "string"`——这是 Apify 特有的约定。Apify 的元验证器会拒绝没有它的属性(并且会拒绝 `"type": "object"`——此处只有 `"string"` 是有效的)。

如果在阶段 3 生成了 `key_value_store_schema.json`,添加第二个属性:
```json
"files": {
    "type": "string",
    "title": "Files",
    "description": "Key-value store containing downloaded files",
    "template": "{{links.apiDefaultKeyValueStoreUrl}}/keys"
}
```

### 可用的模板变量

- `{{links.apiDefaultDatasetUrl}}` —— 默认 dataset 的 API URL
- `{{links.apiDefaultKeyValueStoreUrl}}` —— 默认 key-value store 的 API URL
- `{{links.publicRunUrl}}` —— 公开的运行 URL
- `{{links.consoleRunUrl}}` —— Console 中的运行 URL
- `{{links.apiRunUrl}}` —— 运行的 API URL
- `{{links.containerRunUrl}}` —— 在运行内部运行的 web 服务器的 URL
- `{{run.defaultDatasetId}}` —— 默认 dataset 的 ID
- `{{run.defaultKeyValueStoreId}}` —— 默认 key-value store 的 ID

---

## 阶段 5:更新 `actor.json`

**目标**:将 schema 文件接入 Actor 配置

**操作**:
1. 阅读当前的 `actor.json`
2. 添加或更新 `storages.dataset` 引用:
   ```json
   "storages": {
       "dataset": "./dataset_schema.json"
   }
   ```
3. 如果生成了 `key_value_store_schema.json`,添加该引用:
   ```json
   "storages": {
       "dataset": "./dataset_schema.json",
       "keyValueStore": "./key_value_store_schema.json"
   }
   ```
4. 添加或更新 `output` 引用:
   ```json
   "output": "./output_schema.json"
   ```
5. 如果 `actor.json` 中原有内联的 `storages.dataset` 或 `storages.keyValueStore` 对象(而非字符串路径),将其内容迁移到对应的 schema 文件中,并将内联对象替换为文件路径字符串

---

## 阶段 6:审查与验证

**目标**:确保正确性和完整性

**检查清单**:
- [ ] 源代码中的**每一个**输出字段都在 `dataset_schema.json` 的 `fields.properties` 中——不仅是概览视图的字段,而是 Actor 能产生的所有字段
- [ ] 每个字段都有 `"nullable": true`
- [ ] **顶层 `fields` 对象**同时具有 `"additionalProperties": true` 和 `"required": []`
- [ ] `properties` 中的每个**嵌套对象**也同时具有 `"additionalProperties": true` 和 `"required": []`
- [ ] 每个字段都有 `"description"` 和 `"example"`
- [ ] 所有示例值都已匿名化
- [ ] 每个带有 `"nullable"` 的字段都有 `"type"`
- [ ] 视图列出了 8–12 个最有用的字段,并带有正确的展示格式
- [ ] `output_schema.json` 中每个属性都有 `"type": "string"`
- [ ] 如果使用了 key-value store:`key_value_store_schema.json` 的集合与所有 `setValue`/`set_value` 调用相匹配
- [ ] 如果使用了 key-value store:每个集合使用 `key` 或 `keyPrefix` 中的一个(不是两个都用)
- [ ] `actor.json` 引用了所有生成的 schema 文件
- [ ] Schema 字段名与代码中实际的键一致(camelCase/snake_case 一致性)
- [ ] 如果在仓库中发现了现有 schema,新 schema 遵循它们的约定(描述风格、示例格式、视图结构)
- [ ] 在可能的情况下,schema 字段从现有的类型定义(接口、TypedDict、dataclass)派生——没有重复或不一致的字段定义

将生成的 schema 展示给用户审查后再写入。

---

## 阶段 7:总结

**目标**:记录所创建的内容

报告:
- 创建或更新的文件
- dataset schema 中的字段数量
- key-value store schema 中的集合数量(如果生成了)
- 为概览视图选择的字段
- 任何需要用户澄清的字段(类型模糊、可空性不明确)
- 建议的后续步骤(用 `apify run --user-agent apify-agent-skills/apify-generate-output-schema` 进行本地测试,在 Console 中验证输出标签)


## 示例

```text
User: Apply this skill to my current task.
Assistant: Follow the workflow in this skill, cite limitations, and ask before risky steps.
```

## 限制

- 导入的上游 skill;执行前请验证凭据、权限和安全边界。
- 不能替代特定环境下的验证、测试或维护者审查。
</content>
