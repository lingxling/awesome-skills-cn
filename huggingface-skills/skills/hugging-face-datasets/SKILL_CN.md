---
name: hugging-face-datasets
description: 在 Hugging Face Hub 上创建和管理数据集。支持初始化存储库、定义配置/系统提示、流式行更新以及基于 SQL 的数据集查询/转换。设计用于与 HF MCP 服务器配合使用,以实现全面的数据集工作流程。
---

# 概述
此技能提供工具来在 Hugging Face Hub 上管理数据集,重点关注创建、配置、内容管理和基于 SQL 的数据操作。它旨在补充现有的 Hugging Face MCP 服务器,通过提供数据集编辑和查询功能。

## 与 HF MCP 服务器的集成
- **使用 HF MCP 服务器进行**: 数据集发现、搜索和元数据检索
- **使用此技能进行**: 数据集创建、内容编辑、SQL 查询、数据转换和结构化数据格式化

# 版本
2.1.0

# 依赖项
# 此技能使用 PEP 723 脚本,具有内联依赖项管理
# 使用以下命令运行脚本时会自动安装要求: uv run scripts/script_name.py

- uv(Python 包管理器)
- 入门: 参见下面的"使用说明"了解 PEP 723 用法

# 核心功能

## 1. 数据集生命周期管理
- **初始化**: 使用适当的结构创建新数据集存储库
- **配置**: 存储详细配置,包括系统提示和元数据
- **流式更新**: 高效地添加行而无需下载整个数据集

## 2. 基于 SQL 的数据集查询(新增)
使用 `scripts/sql_manager.py` 通过 DuckDB SQL 查询任何 Hugging Face 数据集:
- **直接查询**: 使用 `hf://` 协议对数据集运行 SQL
- **架构发现**: 描述数据集结构和列类型
- **数据采样**: 获取随机样本以进行探索
- **聚合**: 计数、直方图、唯一值分析
- **转换**: 使用 SQL 过滤、联接、重塑数据
- **导出和推送**: 本地保存结果或推送到新 Hub 存储库

## 3. 多格式数据集支持
通过模板系统支持多样化的数据集类型:
- **聊天/对话**: 聊天模板、多轮对话、工具使用示例
- **文本分类**: 情感分析、意图检测、主题分类
- **问答**: 阅读理解、事实性问答、知识库
- **文本补全**: 语言建模、代码补全、创意写作
- **表格数据**: 用于回归/分类任务的结构化数据
- **自定义格式**: 用于专业需求的灵活架构定义

## 4. 质量保证功能
- **JSON 验证**: 确保上传期间的数据完整性
- **批处理**: 高效处理大型数据集
- **错误恢复**: 优雅地处理上传失败和冲突

# 使用说明

该技能包含两个使用 PEP 723 内联依赖项管理的 Python 脚本:

> **所有路径都是相对于包含此 SKILL.md 文件的目录。**
> 脚本使用以下命令运行: `uv run scripts/script_name.py [arguments]`

- `scripts/dataset_manager.py` - 数据集创建和管理
- `scripts/sql_manager.py` - 基于 SQL 的数据集查询和转换

### 先决条件
- 已安装 `uv` 包管理器
- 必须设置 `HF_TOKEN` 环境变量,使用写访问令牌

---
# SQL 数据集查询(sql_manager.py)

使用 DuckDB SQL 查询、转换和推送 Hugging Face 数据集。`hf://` 协议提供对任何公共数据集(或使用令牌的私有数据集)的直接访问。

## 快速入门

```bash
# 查询数据集
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition' LIMIT 10"

# 获取数据集架构
uv run scripts/sql_manager.py describe --dataset "cais/mmlu"

# 采样随机行
uv run scripts/sql_manager.py sample --dataset "cais/mmlu" --n 5

# 使用过滤器计数行
uv run scripts/sql_manager.py count --dataset "cais/mmlu" --where "subject='nutrition'"
```

## SQL 查询语法

在 SQL 中使用 `data` 作为表名 - 它会被实际的 `hf://` 路径替换:
```sql
-- 基本选择
SELECT * FROM data LIMIT 10

-- 过滤
SELECT * FROM data WHERE subject='nutrition'

-- 聚合
SELECT subject, COUNT(*) as cnt FROM data GROUP BY subject ORDER BY cnt DESC

-- 列选择和转换
SELECT question, choices[answer] AS correct_answer FROM data

-- 正则表达式匹配
SELECT * FROM data WHERE regexp_matches(question, 'nutrition|diet')

-- 字符串函数
SELECT regexp_replace(question, '\n', '') AS cleaned FROM data
```

## 常见操作

### 1. 探索数据集结构
```bash
# 获取架构
uv run scripts/sql_manager.py describe --dataset "cais/mmlu"

# 获取列中的唯一值
uv run scripts/sql_manager.py unique --dataset "cais/mmlu" --column "subject"

# 获取值分布
uv run scripts/sql_manager.py histogram --dataset "cais/mmlu" --column "subject" --bins 20
```

### 2. 过滤和转换
```bash
# 使用 SQL 进行复杂过滤
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT subject, COUNT(*) as cnt FROM data GROUP BY subject HAVING cnt > 100"

# 使用转换命令
uv run scripts/sql_manager.py transform \
  --dataset "cais/mmlu" \
  --select "subject, COUNT(*) as cnt" \
  --group-by "subject" \
  --order-by "cnt DESC" \
  --limit 10
```

### 3. 创建子集并推送到 Hub
```bash
# 查询并推送到新数据集
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition'" \
  --push-to "username/mmlu-nutrition-subset" \
  --private

# 转换并推送
uv run scripts/sql_manager.py transform \
  --dataset "ibm/duorc" \
  --config "ParaphraseRC" \
  --select "question, answers" \
  --where "LENGTH(question) > 50" \
  --push-to "username/duorc-long-questions"
```

### 4. 导出到本地文件
```bash
# 导出到 Parquet
uv run scripts/sql_manager.py export \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition'" \
  --output "nutrition.parquet" \
  --format parquet

# 导出到 JSONL
uv run scripts/sql_manager.py export \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data LIMIT 100" \
  --output "sample.jsonl" \
  --format jsonl
```

### 5. 使用数据集配置/拆分
```bash
# 指定配置(子集)
uv run scripts/sql_manager.py query \
  --dataset "ibm/duorc" \
  --config "ParaphraseRC" \
  --sql "SELECT * FROM data LIMIT 5"

# 指定拆分
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --split "test" \
  --sql "SELECT COUNT(*) FROM data"

# 查询所有拆分
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --split "*" \
  --sql "SELECT * FROM data LIMIT 10"
```

### 6. 带有完整路径的原始 SQL
对于复杂查询或联接数据集:
```bash
uv run scripts/sql_manager.py raw --sql "
  SELECT a.*, b.* 
  FROM 'hf://datasets/dataset1@~parquet/default/train/*.parquet' a
  JOIN 'hf://datasets/dataset2@~parquet/default/train/*.parquet' b
  ON a.id = b.id
  LIMIT 100
"
```

## Python API 用法

```python
from sql_manager import HFDatasetSQL

sql = HFDatasetSQL()

# 查询
results = sql.query("cais/mmlu", "SELECT * FROM data WHERE subject='nutrition' LIMIT 10")

# 获取架构
schema = sql.describe("cais/mmlu")

# 采样
samples = sql.sample("cais/mmlu", n=5, seed=42)

# 计数
count = sql.count("cais/mmlu", where="subject='nutrition'")

# 直方图
dist = sql.histogram("cais/mmlu", "subject")

# 过滤和转换
results = sql.filter_and_transform(
    "cais/mmlu",
    select="subject, COUNT(*) as cnt",
    group_by="subject",
    order_by="cnt DESC",
    limit=10
)

# 推送到 Hub
url = sql.push_to_hub(
    "cais/mmlu",
    "username/nutrition-subset",
    sql="SELECT * FROM data WHERE subject='nutrition'",
    private=True
)

# 本地导出
sql.export_to_parquet("cais/mmlu", "output.parquet", sql="SELECT * FROM data LIMIT 100")

sql.close()
```

## HF 路径格式

DuckDB 使用 `hf://` 协议访问数据集:
```
hf://datasets/{dataset_id}@{revision}/{config}/{split}/*.parquet
```

示例:
- `hf://datasets/cais/mmlu@~parquet/default/train/*.parquet`
- `hf://datasets/ibm/duorc@~parquet/ParaphraseRC/test/*.parquet`

`@~parquet` 修订版为任何数据集格式提供自动转换的 Parquet 文件。

## 有用的 DuckDB SQL 函数

```sql
-- 字符串函数
LENGTH(column)                    -- 字符串长度
regexp_replace(col, '\n', '')     -- 正则表达式替换
regexp_matches(col, 'pattern')    -- 正则表达式匹配
LOWER(col), UPPER(col)           -- 大小写转换

-- 数组函数  
choices[0]                        -- 数组索引(从 0 开始)
array_length(choices)             -- 数组长度
unnest(choices)                   -- 将数组扩展为行

-- 聚合
COUNT(*), SUM(col), AVG(col)
GROUP BY col HAVING condition

-- 采样
USING SAMPLE 10                   -- 随机采样
USING SAMPLE 10 (RESERVOIR, 42)   -- 可重现的采样

-- 窗口函数
ROW_NUMBER() OVER (PARTITION BY col ORDER BY col2)
```

---
# 数据集创建(dataset_manager.py)

### 推荐工作流程

**1. 发现(使用 HF MCP 服务器):**
```python
# 使用 HF MCP 工具查找现有数据集
search_datasets("conversational AI training")
get_dataset_details("username/dataset-name")
```

**2. 创建(使用此技能):**
```bash
# 初始化新数据集
uv run scripts/dataset_manager.py init --repo_id "your-username/dataset-name" [--private]

# 使用详细的系统提示配置
uv run scripts/dataset_manager.py config --repo_id "your-username/dataset-name" --system_prompt "$(cat system_prompt.txt)"
```

**3. 内容管理(使用此技能):**
```bash
# 使用任何模板进行快速设置
uv run scripts/dataset_manager.py quick_setup \
  --repo_id "your-username/dataset-name" \
  --template classification

# 使用模板验证添加数据
uv run scripts/dataset_manager.py add_rows \
  --repo_id "your-username/dataset-name" \
  --template qa \
  --rows_json "$(cat your_qa_data.json)"
```

### 基于模板的数据结构

**1. 聊天模板(`--template chat`)**
```json
{
  "messages": [
    {"role": "user", "content": "Natural user request"},
    {"role": "assistant", "content": "Response with tool usage"},
    {"role": "tool", "content": "Tool response", "tool_call_id": "call_123"}
  ],
  "scenario": "Description of use case",
  "complexity": "simple|intermediate|advanced"
}
```

**2. 分类模板(`--template classification`)**
```json
{
  "text": "Input text to be classified",
  "label": "classification_label",
  "confidence": 0.95,
  "metadata": {"domain": "technology", "language": "en"}
}
```

**3. 问答模板(`--template qa`)**
```json
{
  "question": "What is the question being asked?",
  "answer": "The complete answer",
  "context": "Additional context if needed",
  "answer_type": "factual|explanatory|opinion",
  "difficulty": "easy|medium|hard"
}
```

**4. 补全模板(`--template completion`)**
```json
{
  "prompt": "The beginning text or context",
  "completion": "The expected continuation",
  "domain": "code|creative|technical|conversational",
  "style": "description of writing style"
}
```

**5. 表格模板(`--template tabular`)**
```json
{
  "columns": [
    {"name": "feature1", "type": "numeric", "description": "First feature"},
    {"name": "target", "type": "categorical", "description": "Target variable"}
  ],
  "data": [
    {"feature1": 123, "target": "class_a"},
    {"feature1": 456, "target": "class_b"}
  ]
}
```

### 高级系统提示模板

用于高质量训练数据生成:
```text
You are an AI assistant expert at using MCP tools effectively.

## MCP SERVER DEFINITIONS
[Define available servers and tools]

## TRAINING EXAMPLE STRUCTURE
[Specify exact JSON schema for chat templating]

## QUALITY GUIDELINES
[Detail requirements for realistic scenarios, progressive complexity, proper tool usage]

## EXAMPLE CATEGORIES
[List development workflows, debugging scenarios, data management tasks]
```

### 示例类别和模板

该技能包含超越仅 MCP 使用的多样化训练示例:

**可用示例集:**
- `training_examples.json` - MCP 工具使用示例(调试、项目设置、数据库分析)
- `diverse_training_examples.json` - 更广泛的场景,包括:
  - **教育聊天** - 解释编程概念、教程
  - **Git 工作流程** - 功能分支、版本控制指导
  - **代码分析** - 性能优化、架构审查
  - **内容生成** - 专业写作、创意头脑风暴
  - **代码库导航** - 遗留代码探索、系统分析
  - **对话支持** - 问题解决、技术讨论

**使用不同的示例集:**
```bash
# 添加 MCP 专注的示例
uv run scripts/dataset_manager.py add_rows --repo_id "your-username/dataset-name" \
  --rows_json "$(cat examples/training_examples.json)"

# 添加多样化的对话示例
uv run scripts/dataset_manager.py add_rows --repo_id "your-username/dataset-name" \
  --rows_json "$(cat examples/diverse_training_examples.json)"

# 混合两者以获得全面的训练数据
uv run scripts/dataset_manager.py add_rows --repo_id "your-username/dataset-name" \
  --rows_json "$(jq -s '.[0] + .[1]' examples/training_examples.json examples/diverse_training_examples.json)"
```

### 命令参考

**列出可用模板:**
```bash
uv run scripts/dataset_manager.py list_templates
```

**快速设置(推荐):**
```bash
uv run scripts/dataset_manager.py quick_setup --repo_id "your-username/dataset-name" --template classification
```

**手动设置:**
```bash
# 初始化存储库
uv run scripts/dataset_manager.py init --repo_id "your-username/dataset-name" [--private]

# 使用系统提示配置
uv run scripts/dataset_manager.py config --repo_id "your-username/dataset-name" --system_prompt "Your prompt here"

# 使用验证添加数据
uv run scripts/dataset_manager.py add_rows \
  --repo_id "your-username/dataset-name" \
  --template qa \
  --rows_json '[{"question": "What is AI?", "answer": "Artificial Intelligence..."}]'
```

**查看数据集统计信息:**
```bash
uv run scripts/dataset_manager.py stats --repo_id "your-username/dataset-name"
```

### 错误处理
- **存储库存在**: 脚本将通知并继续配置
- **无效的 JSON**: 清晰的错误消息和解析详细信息
- **网络问题**: 瞬态失败的自动重试
- **令牌权限**: 操作开始前的验证

---
# 组合工作流程示例

## 示例 1: 从现有数据集创建训练子集
```bash
# 1. 探索源数据集
uv run scripts/sql_manager.py describe --dataset "cais/mmlu"
uv run scripts/sql_manager.py histogram --dataset "cais/mmlu" --column "subject"

# 2. 查询并创建子集
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject IN ('nutrition', 'anatomy', 'clinical_knowledge')" \
  --push-to "username/mmlu-medical-subset" \
  --private
```

## 示例 2: 转换和重塑数据
```bash
# 将 MMLU 转换为 QA 格式,提取正确答案
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT question, choices[answer] as correct_answer, subject FROM data" \
  --push-to "username/mmlu-qa-format"
```

## 示例 3: 合并多个数据集拆分
```bash
# 导出多个拆分并组合
uv run scripts/sql_manager.py export \
  --dataset "cais/mmlu" \
  --split "*" \
  --output "mmlu_all.parquet"
```

## 示例 4: 质量过滤
```bash
# 过滤高质量示例
uv run scripts/sql_manager.py query \
  --dataset "squad" \
  --sql "SELECT * FROM data WHERE LENGTH(context) > 500 AND LENGTH(question) > 20" \
  --push-to "username/squad-filtered"
```

## 示例 5: 创建自定义训练数据集
```bash
# 1. 查询源数据
uv run scripts/sql_manager.py export \
  --dataset "cais/mmlu" \
  --sql "SELECT question, subject FROM data WHERE subject='nutrition'" \
  --output "nutrition_source.jsonl" \
  --format jsonl

# 2. 使用您的管道处理数据(添加答案、格式等)

# 3. 推送处理后的数据
uv run scripts/dataset_manager.py init --repo_id "username/nutrition-training"
uv run scripts/dataset_manager.py add_rows \
  --repo_id "username/nutrition-training" \
  --template qa \
  --rows_json "$(cat processed_data.json)"
```
