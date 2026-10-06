---
name: bgpt-paper-search
description: 按主题或 DOI 搜索 BGPT 科学论文，并检索从全文中提取的声明级（claim-level）证据，包括实验、报告的统计数据、适用范围、局限性和来源出处。用于文献综述、证据综合，以及查找超出摘要范围的实验细节。
license: MIT
compatibility: Requires a configured remote BGPT MCP connection and internet access to bgpt.pro. A stdio bridge additionally needs Node.js/npm. Paid access requires a BGPT API key configured as an Authorization header.
metadata:
  version: "1.3"
  skill-author: BGPT
  website: https://bgpt.pro/mcp/
  last-reviewed: "2026-09-30"
---

# BGPT Paper Search

## 何时使用

使用 BGPT 为一个研究问题或一个已知的 DOI 查找来自全文的证据。它返回的是
提取出的声明（claims）及其支持性实验，而不仅仅是文献元数据。使用这些记录
来构建可追溯的证据表；它们不是一次完整的系统综述检索，也不是经过验证的
偏倚风险（risk-of-bias）评估。

## 连接

在使用之前需要在主机中配置 BGPT；安装此技能并不会自动注册 MCP 服务器。
该提供商同时支持两种传输方式：

| 传输方式 | 端点 |
| --- | --- |
| Streamable HTTP | `https://bgpt.pro/mcp/stream` |
| SSE | `https://bgpt.pro/mcp/sse` |

在支持的情况下使用主机原生的远程 MCP 配置。对于使用 `mcpServers` JSON 并
需要本地 stdio 桥接的主机，以下配置使用了 `mcp-remote`（请根据主机实际的
设置格式进行调整）：

```json
{
  "mcpServers": {
    "bgpt": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://bgpt.pro/mcp/stream", "--transport", "http-only"]
    }
  }
}
```

已发布的 `bgpt-mcp` 1.1.0 npm 包只是 `mcp-remote` 的一个薄 SSE 封装，而不是
一个本地论文数据库。其附带的 README 早于当前的工具契约和定价。请优先使用
上述原生连接或可配置的桥接方式。审查时该 GitHub 仓库链接的 BGPT 仓库不可用；
请使用[当前提供商文档](https://bgpt.pro/mcp/)和实时工具模式（schema）。

免费访问不需要密钥。对于付费使用，请使用主机的凭据存储，在主机的远程服务器
请求头中配置 `Authorization: Bearer <key>`。对于桥接方式，
[`mcp-remote` 支持 `--header-file`](https://github.com/punkpeye/mcp-remote#custom-headers)
配合本地凭据文件使用。不要在 MCP 工具调用中放入 `api_key`：当前两个工具都
没有声明这个参数。请通过连接本身进行身份认证。

## 搜索与 DOI 查找

在调用之前先发现已连接服务器的工具。在 2026-09-30 审查时实时的 BGPT 2.14.7
模式暴露了以下内容：

| 工具/参数 | 契约 |
| --- | --- |
| `search_papers.query` | 必需字符串。使用简短的英文搜索词。 |
| `num_results` | 整数，1–100；默认 16。显式设置它以控制结果用量。 |
| `days_back` | 可选整数；限定在最近 N 天内发表的论文。省略表示所有日期。 |
| `min_citations` | 可选整数；指**论文引用的参考文献数量**的最小值，而不是该论文被引用的次数。 |
| `study_type` | 可选字符串：`primary study`、`systematic review`、`meta-analysis`、`narrative review`、`protocol`、`dataset`、`commentary` 或 `other`。 |
| `output_format` | `evidence`（默认）、`full` 或 `legacy`。 |
| `lookup_paper.doi` | 必需的 DOI 字符串；也接受 `output_format`。找到的论文计为一个结果。 |

使用筛选参数，而不要把年份或筛选条件写进查询字符串中。此模式没有记录布尔
查询语法、offset、page 或 cursor。结果数量限制不等于分页：不要凭空设想续
查参数，也不要声称搜索会枚举所有匹配的论文。为获得更广泛的覆盖，可运行多个
明确的问题变体，并按 DOI 去重，同时保留查询历史。

一个经过验证、返回一个公开结果的搜索示例（通过已连接的工具接口调用）：

```json
{"query": "CRISPR human cells", "num_results": 1, "output_format": "full"}
```

示例性的带筛选条件搜索（这些筛选条件经过模式检查，但未实际执行）：

```json
{"query": "CRISPR delivery neurons", "num_results": 5, "days_back": 90, "study_type": "primary study", "output_format": "evidence"}
```

对于已经识别出的论文，使用其纯 DOI 调用 `lookup_paper`，而不是指望标题搜索
恰好返回那篇论文：

```json
{"doi": "10.1016/j.ymeth.2015.10.014", "output_format": "evidence"}
```

不要把连接错误、配额错误或工具错误解释为一个空的证据集。提供商公布了结果
配额，但审查页面上没有数值化的请求速率限制；不要假设请求吞吐量无限制。

## 解读结果契约

搜索返回一个包含 `results` 列表和 `count` 的信封（envelope）；同时记录返回
的 `query`，因为该服务可能会重写搜索词。DOI 查找返回 `found` 和单个
`result`；在读取之前先处理未找到的情况。在解读信封之前，先检查 MCP 结果中
是否存在工具错误。

- `evidence` 给出精简的证据记录；空的可选字段可能会被省略。
- `full` 在证据记录基础上添加了旧版（legacy）论文元数据。
- `legacy` 请求旧版的论文元数据表示形式。不要假设每篇论文都具有所有之前宣传
  过的字段或质量评分。

提供商表示，evidence/full 格式会省略没有提取到证据的论文。但是，实时冒烟
测试在两种格式中都返回了一条记录，其中 `schema_version: "legacy"`、
`extraction_status: "legacy"`，且 `evidence_units` 列表为空。因此，返回的
记录并不保证具有声明级的来源出处。搜索为空或 DOI 未找到，也不能证明该论文
不存在。在可用时保留 `doi`、`title`、`publication_date` 和 `publication_name`，
然后检查 `central_claim` 和 `evidence.evidence_units`。每个单元将其声明与一个
实验、报告的统计数据、已证明的适用范围和来源出处相关联。保留模式版本：旧
记录可能具有不同的结构。旧版的完整元数据可能包含 null 值、数字字符串和序列
化文本，而不是原生列表；请保留原始值，切勿将其作为代码执行。

提供商文档记录了 V4 的限制：每条记录最多五个证据单元，每个单元最多两段来源
出处段落，每段最多 320 个字符。这些是有边界的提取结果，不是完整文章。在综合
之前检查 `extraction_status`、`normalization_warnings` 和
`evidence.record_provenance`（包括截断信息）。

## 证据核查

对于每个提取出的结果，保留 DOI 以及来源章节、表格或图表。在将样本量、单位、
实验组、报告的统计数据和不确定性用于综合之前，对照原文进行核实。区分作者
报告的局限性与提取生成的解读。保留矛盾或混合的证据，以及已证明的适用范围。
如果存在旧版质量评分，只将其用作筛选辅助工具，而不是针对特定研究的偏倚风险
评估。

## 配额与审查范围

在审查日期，提供商宣传每个网络有 50 个免费**结果**，之后每个返回结果
0.02 美元。一次成功的 DOI 查找计为一个结果；未找到的查找不计费。在进行大批量
查询之前，请重新检查配额和定价。不要对已耗尽配额的请求反复重试。

来源：[提供商设置、记录格式和计费](https://bgpt.pro/mcp/)、
[实时 MCP 端点](https://bgpt.pro/mcp/stream)、
[已发布的 BGPT 封装器元数据](https://registry.npmjs.org/bgpt-mcp/latest)，
以及[桥接文档](https://github.com/punkpeye/mcp-remote)。
工具模式、单结果的完整搜索、匹配证据格式的 DOI 查找，以及 SSE 握手均使用未
经身份验证的请求进行了检查。公开的搜索/查找返回了一条旧版模式的记录，而不是
V4 的示例数据。付费身份验证、带筛选条件的搜索行为，以及主机特定的配置均未
经过测试。
