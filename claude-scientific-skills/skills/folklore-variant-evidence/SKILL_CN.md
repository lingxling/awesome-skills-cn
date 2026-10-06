---
name: folklore-variant-evidence
description: "通过Folklore Clinical Variant Interpretation MCP检索公开基因或疾病的ClinGen基因-疾病有效性断言，并查看一个受支持的GRCh38生殖线核SNV或简单插入缺失变异的源链接公开证据和文献。当一个科学代理必须针对已解析、模糊、未找到、无效、不受支持或不可用的变异结果进行确定性分支判断时使用；将一个已解析的公开变异链接到相关文献或出版物细节时使用；或在不接受患者、表型、家族、共分离或私人病例数据的前提下保留证据溯源时使用。"
license: MIT
compatibility: Requires network access to api.helena.bio (stateless Streamable HTTP MCP, no credentials) and a host supporting its advertised protocol, or curl for direct JSON-RPC POST requests.
metadata:
  version: "1.2"
  last-reviewed: "2026-09-30"
  skill-author: "Helena Bioinformatics"
  website: "https://folklore.helena.bio"
  github: "https://github.com/helena-bioinformatics/folklore-mcp"
---

# Folklore 变异证据

使用 Folklore Clinical Variant Interpretation MCP 来检索结构化的公开
变异证据、自动化的变异级ACMG/AMP决策支持、溯源信息，以及供专业人员
审查的源链接文献。将工作流限制在公开标识符范围内，并保留每一个显式
的结果状态。适配器 1.5.0 还提供 ClinGen 基因-疾病有效性断言；来源
覆盖范围是有限的，并非所有已知关联都会包含在内。

Folklore Clinical Variant Interpretation MCP 由 Helena Bioinformatics
发布。其托管端点为：

```text
https://api.helena.bio/folklore/v1/mcp
```

不需要账户或API密钥。公开的Apache-2.0适配器和契约可在
<https://github.com/helena-bioinformatics/folklore-mcp> 获取。

## 最简连接示例

一个没有原生MCP支持的宿主可以发起相同的公开JSON-RPC调用：

```bash
curl --silent --show-error --fail-with-body --max-time 60 \
  -X POST https://api.helena.bio/folklore/v1/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2026-07-28' \
  -H 'Mcp-Method: tools/call' \
  -H 'Mcp-Name: search_variant_evidence' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}},"name":"search_variant_evidence","arguments":{"assembly":"GRCh38","query":"rs80357914"}}}'
```

路由标头必须与JSON-RPC方法和工具名称相匹配。一个成功的HTTP响应是
不够的：先检查JSON-RPC的 `error`，然后检查
`result.structuredContent.adapter_error`，最后检查该工具的
`result.structuredContent.result.status`。其他工具使用不同的响应
形状；请使用[契约表](references/mcp-contract.md)。

在继续之前检查返回的结果。这个示例可能会返回带有多个候选项的
`ambiguous`：此时应停止，并要求提供一个无歧义的公开变异标记法，而
不是自动选择某个候选项。

## 选择正确的技能

当任务是将一个公开变异转换为结构化的Folklore证据、显式处理解析
状态、链接变异相关文献，或进行ClinGen基因到疾病/疾病到基因断言时，
使用本技能。

- 对于跨ClinVar、dbSNP、gnomAD、Ensembl VEP、COSMIC或多个数据库的
  广泛直接查询，使用 `database-lookup`。
- 当基因组装、坐标约定、重叠群名称或变异表示形式不确定时，先使用
  `genomic-coordinates`。
- 不要将本技能用于VCF注释、批处理、体细胞变异、结构变异、多基因
  评分或针对特定患者的解读。

Folklore Clinical Variant Interpretation MCP 以一个源链接的公开证据
契约来补充这些技能。它不能取代直接的数据库查阅或合格的临床判断。

## 执行输入边界

在调用任何变异工具之前：

1. 只提取一个公开变异标识符或标记法。
2. 要求使用GRCh38，以及一个短于50个碱基对的生殖线核SNV或简单插入/
   缺失。一个不受支持的基因组可能在任何科学意义上的 `unsupported`
   状态出现之前，就已被输入架构拒绝。
3. 移除或拒绝患者姓名、病例标识符、表型、家族史、共分离证据、临床
   记录、上传的文件以及其他私人或患者特定的背景信息。
4. 如果任务依赖于患者背景信息，停止并说明Folklore Clinical Variant
   Interpretation MCP不接受也不评估这类信息。
5. 永远不要在暗示结果能回答患者特定问题的同时，把一个患者特定请求
   转换成一个公开变异查询。

可接受的公开变异形式包括基因组坐标、基因组/编码/蛋白质HGVS、SPDI、
rsID，或Folklore Clinical Variant Interpretation MCP返回的
`canonical_key`。

## 验证实时工具目录

连接到托管端点并调用 `tools/list`。核实可用工具，而不要依赖模型的
记忆。已记录的公开目录包含：

- `search_variant_evidence`
- `search_variant_literature`
- `get_publication_details`
- `search_literature_corpus`
- `get_gene_disease_associations`
- `search_disease_genes`

单独的第七个工具 `support_helena` 不是科学证据；只有在明确要求时
才使用它。

如果发现过程或工具调用失败，将其保留为一个可用性问题。不要将其
重新解读为缺乏科学证据。

在编写工具调用或解读响应状态之前，请阅读
[公开MCP契约](references/mcp-contract.md)。

## 检索基因-疾病断言

对一个确切的基因符号或HGNC标识符使用
`get_gene_disease_associations`，或者对一个确切的MONDO标识符或公开
疾病名称子字符串使用 `search_disease_genes`。两者都接受 `limit`
（默认20，1–50）和 `offset`（默认0，0–1000）。请求示例见参考文档。
这是一个独立的来源查询，不需要变异输入或基因组装。

保留每一个返回的疾病身份、遗传方式、证据评估、来源URL、日期、
`source.version` 和 `source.snapshotSha256`。这是一个本地ClinGen
快照，不保证是最新的ClinGen发布版本。只要
`pagination.nextOffset` 存在，就继续跟进；保留分页上限警告。在超过
总数之后出现的空页面，并不意味着最初的查询没有匹配项。不要合并
不同的疾病，也不要在名称匹配项之间默默选择。基因-疾病有效性并不
对特定变异进行分类。`not_found` 响应意味着在可用来源中没有匹配的
断言，不是不存在关联。不得发送任何患者、表型、家族、共分离的私人
病例数据或测序文件。仍然需要合格的专业人员审查。

## 运行变异证据工作流

### 1. 解析并检索证据

使用以下参数调用 `search_variant_evidence`：

```text
assembly: GRCh38
query: <一个公开变异标识符或标记法>
```

不要在此调用中添加表型、疾病、患者、家族或治疗相关的背景信息。
保留返回的契约字段、来源链接、局限性和使用边界。

### 2. 根据返回状态进行分支判断

先阅读传输层/JSON-RPC错误和 `adapter_error`。对于
`search_variant_evidence`，令 `envelope =
result.structuredContent`；只有当 `envelope.result` 不为null时，才
根据 `envelope.result.status` 进行分支判断。`invalid_arguments`
适配器错误与科学意义上的 `invalid_request` 是不同的。保留
`isError` 以及任何已分类的失败，包括
`resolution_unavailable`。将该状态当作控制流值处理，而不是普通文字：

| 状态 | 所需操作 |
|---|---|
| `resolved` | 复用返回的`canonical_key`；审查结构化的解读、溯源信息、来源链接以及局限性。 |
| `ambiguous` | 展示返回的候选项，并要求明确选择一个公开变异。永远不要自动选择一个候选项。 |
| `not_found` | 报告在该服务和查询范围内未找到结果。不要声称全局范围内不存在。 |
| `invalid_request` | 报告验证问题，并要求提供一个已更正的公开变异。不要悄悄地重新解读输入。 |
| `unsupported` | 说明相关的服务边界并停止。不要强行将查询转换为受支持的形式。 |
| `resolution_unavailable` | 报告一次临时性的解析或可用性失败。不要将其视为证据缺失。 |

只有 `resolved` 结果才可以自动继续进入一个变异相关的文献工作流。
其canonical key是 `envelope.result.identity.canonical_key`。如果
`envelope.result.interpretation.status` 为 `unavailable`，保留其
已分类的错误；身份解析已经成功，但分类尚未完成。不要为这种结果
读取或杜撰一个分类。

### 3. 审查证据而不过度宣称

对于一个已解析的结果：

- 展示返回的变异身份和 `canonical_key`。
- 原样保留返回的自动化变异级ACMG/AMP决策支持结果。
- 引用返回的公开来源和溯源信息。
- 按照[上游解读指南](https://github.com/helena-bioinformatics/folklore-mcp)
  的要求，将提交的ClinVar断言与Folklore的自动化结果分开处理。如果
  两者不一致，报告每一项断言及其来源/日期，并保留这种不一致；不要
  呈现一个合并后的共识分类。
- 将返回的事实与代理的综合分析分开。
- 说明需要合格的专业人员审查。
- 不要把该结果变成诊断、个体风险评估、治疗建议，或独立的临床
  报告。

## 链接到文献

### 变异相关文献

在一次已解析的证据调用之后，将返回的 `canonical_key` 传递给
`search_variant_literature`。保持 `assembly` 为 `GRCh38`。可以使用
一个可选的 `question` 来缩小文献的关注范围，但它必须仍是一个公开
的科学问题，且不得包含患者背景信息。

区分每个结果的匹配类型：

- `exact_variant`：与已解析变异的直接匹配
- `variant_alias`：通过一个已报告别名的匹配
- `gene_association`：更广泛的基因级关联，不是变异特定的证明

文献关联不会改变已返回的ACMG/AMP分类。

### 出版物详情

只使用文献工具返回的PMID来调用 `get_publication_details`。保留
PubMed URL、存在时的DOI/PMCID字段、撤稿状态，以及基因提及和变异
提及之间的区别。

### 语义语料库搜索

对于一个公开的自然语言科学问题，或按出版物标识符、基因、变异、
表型、HPO或OMIM概念进行发现，使用 `search_literature_corpus`。将
结果视为供专业人员审查的源链接候选项。零结果响应意味着该受限查询
没有返回结果，不代表任何地方都不存在相关出版物。

查询长度为3–200个字符，`limit` 为1–25，`sort` 设置为
`relevance`、`newest` 或 `oldest`。对于另一页，使用相同的查询和
排序方式复用返回的不透明 `next_cursor`；不要自行构造偏移量。将
`match_types` 和 `article_entities` 与变异文献的匹配类型区分开来。
报告 `semantic_index_used` 和 `semantic_degraded_reason`；一个返回
的词法匹配并不能证明语义检索确实生效了。保留实时服务返回的其他
检索元数据。

即使查询不涉及特定变异，也不要在语料库查询中放入患者信息。

## 报告一个可重现的结果

包含：

1. 确切的公开查询以及 `GRCh38` 基因组装。
2. 返回的状态，如果已解析，还包括 `canonical_key`。
3. 结构化的证据或文献结果，且不改变其含义。
4. 来源链接和出版物标识符。
5. 文献结果的匹配类型。
6. 访问日期以及任何可用性限制。
7. 以下边界声明：

> 这是供合格专业人员审查使用的公开、变异级别的决策支持。它不评估
> 患者、表型、家族、共分离或私人病例数据，也不是诊断或治疗建议。

## 可证伪的冒烟测试

使用公开的rsID `rs80357914` 来测试歧义处理：

```text
使用assembly GRCh38和query rs80357914调用search_variant_evidence。
如果结果是ambiguous，列出返回的候选项并停止以等待明确选择。不要
选择某个候选项，也不要调用下游的文献工具。
```

只有当一个ambiguous响应导致工作流在没有自动候选项选择的情况下停止
时，这个歧义分支才算通过。如果实时响应发生变化，记录实际的状态；
一个resolved响应并不能测试歧义处理。

在2026-09-30，实时发现报告的适配器版本为1.5.0，协议版本为
2026-07-28。该rsID示例返回了 `ambiguous`；另一个独立的公开HGVS
查询成功解析，并通过其返回的键链接到了文献和一个返回的PMID。测试
了语料库游标分页和基因-疾病偏移量分页。这些是带日期的协议检查，
不是对临床准确性的验证。确切的响应形状和来源/实时差异，请参见
参考文档。

## 官方参考文献

- 集成设置：<https://folklore.helena.bio/integrations>
- 技术指南：<https://folklore.helena.bio/docs/folklore-connector>
- 公开适配器和契约：<https://github.com/helena-bioinformatics/folklore-mcp>
- 官方MCP注册表身份标识：`io.github.helena-bioinformatics/folklore`
