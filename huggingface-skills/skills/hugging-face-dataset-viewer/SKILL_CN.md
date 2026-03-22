---
name: hugging-face-dataset-viewer
description: 使用此技能执行 Hugging Face 数据集查看器 API 工作流，包括获取子集/分割元数据、分页行、搜索文本、应用过滤器、下载 parquet URL 以及读取大小或统计信息。
---

# Hugging Face 数据集查看器

使用此技能执行只读的数据集查看器 API 调用来进行数据集探索和提取。

## 核心工作流程

1. 可选：使用 `/is-valid` 验证数据集可用性。
2. 使用 `/splits` 解析 `config` + `split`。
3. 使用 `/first-rows` 预览。
4. 使用 `offset` 和 `length`（最大 100）通过 `/rows` 分页内容。
5. 使用 `/search` 进行文本匹配，使用 `/filter` 进行行谓词。
6. 通过 `/parquet` 检索 parquet 链接，通过 `/size` 和 `/statistics` 检索总数/元数据。

## 默认值

- 基础 URL: `https://datasets-server.huggingface.co`
- 默认 API 方法: `GET`
- 查询参数应进行 URL 编码。
- `offset` 从 0 开始。
- `length` 最大值通常为行类端点的 `100`。
-  gated/私有数据集需要 `Authorization: Bearer <HF_TOKEN>`。

## 数据集查看器

- `验证数据集`: `/is-valid?dataset=<namespace/repo>`
- `列出子集和分割`: `/splits?dataset=<namespace/repo>`
- `预览首行`: `/first-rows?dataset=<namespace/repo>&config=<config>&split=<split>`
- `分页行`: `/rows?dataset=<namespace/repo>&config=<config>&split=<split>&offset=<int>&length=<int>`
- `搜索文本`: `/search?dataset=<namespace/repo>&config=<config>&split=<split>&query=<text>&offset=<int>&length=<int>`
- `使用谓词过滤`: `/filter?dataset=<namespace/repo>&config=<config>&split=<split>&where=<predicate>&orderby=<sort>&offset=<int>&length=<int>`
- `列出 parquet 分片`: `/parquet?dataset=<namespace/repo>`
- `获取大小总数`: `/size?dataset=<namespace/repo>`
- `获取列统计信息`: `/statistics?dataset=<namespace/repo>&config=<config>&split=<split>`
- `获取 Croissant 元数据（如果可用）`: `/croissant?dataset=<namespace/repo>`

分页模式：

```bash
curl "https://datasets-server.huggingface.co/rows?dataset=stanfordnlp/imdb&config=plain_text&split=train&offset=0&length=100"
curl "https://datasets-server.huggingface.co/rows?dataset=stanfordnlp/imdb&config=plain_text&split=train&offset=100&length=100"
```

当分页是部分的时，使用响应字段如 `num_rows_total`、`num_rows_per_page` 和 `partial` 来驱动继续逻辑。

搜索/过滤说明：

- `/search` 匹配字符串列（全文样式行为在 API 内部）。
- `/filter` 需要 `where` 中的谓词语法和 `orderby` 中的可选排序。
- 保持过滤和搜索为只读且无副作用。

## 查询数据集

使用 `npx parquetlens` 和 Hub parquet 别名路径进行 SQL 查询。

Parquet 别名格式：

```text
hf://datasets/<namespace>/<repo>@~parquet/<config>/<split>/<shard>.parquet
```

从数据集查看器 `/parquet` 派生 `<config>`、`<split>` 和 `<shard>`：

```bash
curl -s "https://datasets-server.huggingface.co/parquet?dataset=cfahlgren1/hub-stats" \
  | jq -r '.parquet_files[] | "hf://datasets/\(.dataset)@~parquet/\(.config)/\(.split)/\(.filename)"'
```

运行 SQL 查询：

```bash
npx -y -p parquetlens -p @parquetlens/sql parquetlens \
  "hf://datasets/<namespace>/<repo>@~parquet/<config>/<split>/<shard>.parquet" \
  --sql "SELECT * FROM data LIMIT 20"
```

### SQL 导出

- CSV: `--sql "COPY (SELECT * FROM data LIMIT 1000) TO 'export.csv' (FORMAT CSV, HEADER, DELIMITER ',')"`
- JSON: `--sql "COPY (SELECT * FROM data LIMIT 1000) TO 'export.json' (FORMAT JSON)"`
- Parquet: `--sql "COPY (SELECT * FROM data LIMIT 1000) TO 'export.parquet' (FORMAT PARQUET)"`

## 创建和上传数据集

根据依赖约束使用以下流程之一。

零本地依赖（Hub UI）：

- 在浏览器中创建数据集仓库：`https://huggingface.co/new-dataset`
- 在仓库的"文件和版本"页面上传 parquet 文件。
- 验证分片是否出现在数据集查看器中：

```bash
curl -s "https://datasets-server.huggingface.co/parquet?dataset=<namespace>/<repo>"
```

低依赖 CLI 流程 (`npx @huggingface/hub` / `hfjs`)：

- 设置认证令牌：

```bash
export HF_TOKEN=<your_hf_token>
```

- 将 parquet 文件夹上传到数据集仓库（如果仓库缺失则自动创建）：

```bash
npx -y @huggingface/hub upload datasets/<namespace>/<repo> ./local/parquet-folder data
```

- 创建时上传为私有仓库：

```bash
npx -y @huggingface/hub upload datasets/<namespace>/<repo> ./local/parquet-folder data --private
```

上传后，调用 `/parquet` 以发现 `<config>/<split>/<shard>` 值，用于使用 `@~parquet` 进行查询。