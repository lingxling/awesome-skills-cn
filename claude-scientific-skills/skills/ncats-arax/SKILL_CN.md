---
name: ncats-arax
description: 查询 NCATS Translator ARAX 生产环境 API，获取有边界、有类型、具有丰富来源出处信息的一跳关系以及端点固定的两跳生物医学知识图谱关系。用于受 Biolink 约束的 RTX-KG2 查找、显式选定提供商的 ARAX 联合查询、独立的实体规范化、具有限定词意识的图遍历，以及检查 TRAPI 边绑定、出版物和知识来源出处。不要用于推断、排名、开放式路径查找、临床指导，或敏感查询。
allowed-tools: Read Bash
license: MIT
compatibility: Requires Python 3.10+ and outbound HTTPS access to arax.transltr.io. The client uses only the Python standard library and needs no API key. Queries and caller metadata may be publicly visible; never submit sensitive or patient-specific content.
metadata:
  version: "1.2"
  last-reviewed: "2026-09-30"
  skill-author: neuroepithelial
---

# NCATS ARAX

将 ARAX 用作一个受约束的知识图谱查找服务。提交经过审查的 CURIE 和显式的
Biolink 类型，保留精确的 TRAPI 交换内容，检查查询边绑定和来源出处，并将每一条
返回的路径都视为需要后续验证的候选项。

在构建查询之前，请阅读 [query-contract.md](references/query-contract.md)。在
解读已保存的工件、警告、来源出处或部分结果时，请阅读
[output-schema.md](references/output-schema.md)。

## 安全边界

- 只使用公开的、非敏感的研究问题。即使请求了 `store=false`，ARAX 的状态设施
  也可能暴露查询和调用方的元数据。
- 不要提交患者信息、保密的研究问题、未公开的化合物研发项目，或专有的靶点
  假设。
- 不要将返回的路径呈现为已验证的机制或临床建议。
- 将零结果报告为“在这些约束条件下未返回”，绝不要将其作为不存在该关系的证据。
- 将位置描述为未经评分的响应顺序，绝不要将其描述为排名。
- 单独使用文献和权威数据库验证重要的候选项。

## 工作流程

1. 单独对自由文本进行规范化，然后审查并报告所提议的 CURIE 和类别。
2. 选择一个有类型的一跳查询，或一个两端都固定的、恰好两跳的查询。
3. 除非用户明确指定了两到五个提供商，否则使用默认的 RTX-KG2 查找。
4. 确认该生物医学查询是公开的，并选择一个新的或空的输出目录。
5. 运行客户端一次。在失败或空结果之后，不要悄悄更改提供商选择或扩展顺序。
6. 检查 `summary.json` 中有边界的绑定和来源出处，以及 `response.json` 中
   精确的 TRAPI 负载。
7. 在 ARAX 之外验证在科学上重要的路径。

## 预检

在不进行生物医学查询的情况下检查生产环境 OpenAPI：

```bash
python skills/ncats-arax/scripts/arax_client.py preflight
```

客户端会验证该服务是否将自身标识为 ARAX，是否暴露了 `POST /query` 和
`GET /entity`，以及是否报告了受支持的 TRAPI 版本。它读取
`info.x-trapi.version`，对于较旧的 OpenAPI 文档则回退读取标题。使用非生产
环境端点或未经测试的 TRAPI 系列需要显式覆盖；这两种覆盖都不会改变固定的
查询形状或操作。

## 规范化一个实体

规范化仅用于审查，绝不会触发图查询：

```bash
python skills/ncats-arax/scripts/arax_client.py normalize "ivacaftor" \
  --expected-category biolink:SmallMolecule \
  --max-synonyms 10 \
  --acknowledge-public-query \
  --output-dir outputs/normalize-ivacaftor
```

在使用一个 CURIE 之前，审查规范标识符、名称、类别和同义词预览。无论查询
结果如何，都要报告所有 CURIE 和类别。类别警告或零结果是整理标识符的理由，
而不是自动串接到 `/query` 的理由。

## 一跳查找

固定至少一个端点，并为两个节点都指定类型：

```bash
python skills/ncats-arax/scripts/arax_client.py one-hop \
  --subject-id CHEBI:31690 \
  --subject-category biolink:SmallMolecule \
  --predicate biolink:affects \
  --object-id NCBIGene:25 \
  --object-category biolink:Gene \
  --qualifier biolink:object_aspect_qualifier=activity_or_abundance \
  --qualifier biolink:object_direction_qualifier=decreased \
  --acknowledge-public-query \
  --output-dir outputs/imatinib-abl1
```

查找模式是默认模式，并将扩展固定为 `infores:rtx-kg2`。默认返回 20 个结果。
使用 `--result-limit N` 请求 1 到 50 个结果；在任一模式下，50 都是硬性上限。

## 端点固定的两跳查找

恰好使用一个有类型、未固定的中间节点：

```bash
python skills/ncats-arax/scripts/arax_client.py two-hop \
  --subject-id CHEBI:66901 \
  --subject-category biolink:SmallMolecule \
  --predicate-1 biolink:affects \
  --intermediate-category biolink:Gene \
  --predicate-2 biolink:associated_with \
  --object-id MONDO:0009061 \
  --object-category biolink:Disease \
  --qualifier-1 biolink:object_aspect_qualifier=activity_or_abundance \
  --qualifier-1 biolink:object_direction_qualifier=increased \
  --expand-order right-first \
  --acknowledge-public-query \
  --output-dir outputs/ivacaftor-cystic-fibrosis
```

默认采用从右侧开始的扩展顺序。如果空结果值得再次尝试，请使用
`--expand-order left-first` 显式运行一次新的查询，并将这两次运行分开保存。

## 选定提供商的联合查询

联合查询是显式的，接受两到五个具名的提供商：

```bash
python skills/ncats-arax/scripts/arax_client.py one-hop \
  --subject-id CHEBI:31690 \
  --subject-category biolink:SmallMolecule \
  --predicate biolink:affects \
  --object-id NCBIGene:25 \
  --object-category biolink:Gene \
  --mode federated \
  --kp infores:rtx-kg2 \
  --kp infores:molepro \
  --acknowledge-public-query \
  --output-dir outputs/federated-imatinib-abl1
```

联合查询默认使用 50 个结果的硬性上限。提供商错误可能与有用的结果同时存在；
这样的一次运行在保留其工件后会以退出码 7 退出，并被标记为部分结果。这同样
适用于查找模式下某个提供商失败的情况。明确的非成功 ARAX 响应状态会以退出码
6 退出，同时保留原始响应；不能将其报告为一次成功的零结果查询。

## 检查已保存的来源出处

在不访问网络的情况下重建一份有边界的摘要：

```bash
python skills/ncats-arax/scripts/arax_client.py summarize \
  --request outputs/ivacaftor-cystic-fibrosis/request.json \
  --response outputs/ivacaftor-cystic-fibrosis/response.json \
  --format text
```

检查工具只接受与实时命令生成的相同的受约束请求形状和固定操作。使用
`--format json` 可在标准输出上获得规范化的视图。

## 解读结果

- 跟踪每次分析的查询边绑定；不要概括总结每一条知识图谱边。
- 保留 ARAX 返回的物理边主体、谓词、客体和限定词值。返回的谓词或限定词方面
  可能比查询约束更具体。
- 检查所有来源对象，包括 primary、aggregator、supporting-data、
  upstream-resource 和 source-record URL 字段。
- 在声称得到印证之前，将聚合器边追溯到其主要/上游来源和出版物。多个提供商
  可能转发同一条记录；要报告独立不同的主要证据，而不是把提供商数量当作置信度
  或独立重复验证的依据。
- 将 `publication_availability: not_returned` 视为缺失的元数据，而不是没有
  相关出版物存在的证据。
- 将缺失的辅助图引用和提供商故障视为明确的警告。
- 每当有边界的摘要省略了细节，或该服务的响应是部分的、不熟悉的，或在科学上
  令人意外时，查阅原始响应。

## 刻意排除的功能

该客户端没有原始查询、工作流、操作、叠加（overlay）、排名、推断、链接预测、
Pathfinder、ARS、批处理、全提供商、三跳、缓存、守护进程、SDK、MCP，或自然
语言到 TRAPI 的接口。不要在此技能下使用直接的 HTTP 调用来绕过这些限制。

## 官方参考资料

于 2026-09-30 对照生产环境 ARAX 1.5.4 / TRAPI 1.5.0 进行审查（该 URL 中仍
包含 `v1.4`）。预检、规范化、带限定词的一跳查找、端点固定的两跳查找，以及
RTX-KG2/MolePro 联合查询的实时公开冒烟测试均已通过。结果和提供商可用性可能
会发生变化。官方入门指南中包含较旧的响应示例；请使用已部署的模式和当前的
ARAX 源码来确定字段和操作契约。该客户端未使用任何 Python SDK。

- [ARAX 文档](https://ncatstranslator.github.io/TranslatorTechnicalDocumentation/architecture/ara/arax/)
- [ARAX 生产环境 OpenAPI](https://arax.transltr.io/api/arax/v1.4/openapi.json)
- [ARAXi 操作文档](https://github.com/RTXteam/RTX/blob/master/code/ARAX/Documentation/DSL_Documentation.md)
- [ARAX 查询执行与无评分结果化](https://github.com/RTXteam/RTX/blob/master/code/ARAX/ARAXQuery/ARAX_query.py)
- [Translator Reasoner API](https://github.com/NCATSTranslator/ReasonerAPI)
- [Biolink Model](https://biolink.github.io/biolink-model/)
