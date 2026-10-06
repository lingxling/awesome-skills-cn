---
name: tamarind
description: 通过 REST API 或 MCP 服务器访问 Tamarind Bio 平台上一系列开源分子设计和结构生物学工具——无需本地 GPU。Tamarind 集成了用于结构预测（AlphaFold、Boltz、Chai、ESMFold）、蛋白质/结合体/全新设计（RFdiffusion、ProteinMPNN、BoltzGen）、抗体与纳米抗体设计与可开发性评估、蛋白质-配体对接（DiffDock、Autodock Vina）、结合亲和力预测、MSA 生成以及分子动力学的热门开源模型。当用户提到 Tamarind 或 tamarind.bio、想要在云端运行这些开源工具、提到 app.tamarind.bio/api 或 x-api-key 请求头，或需要批量提交序列进行结构或生物物理表征时使用。
license: MIT
compatibility: Requires Python 3.10+, a Tamarind Bio account, and an API key from app.tamarind.bio. Uses the `requests` library against the public REST API (these recipes use HTTP directly). Network access required. Optional MCP server at mcp.tamarind.bio/mcp for agent hosts.
metadata:
  version: "1.3"
  last-reviewed: "2026-09-30"
  skill-author: Tamarind Bio
  trigger-keywords: protein structure prediction, AlphaFold, Boltz, Chai, ESMFold, protein design, binder design, de novo design, antibody design, nanobody, protein-ligand docking, DiffDock, Autodock Vina, binding affinity, MSA generation, inverse folding, ProteinMPNN, RFdiffusion, BoltzGen, cloud GPU biology, structure prediction API, x-api-key, developability, adme, enzyme, peptide, protein language models, molecular design
  openclaw:
    primaryEnv: TAMARIND_API_KEY
    envVars:
    - name: TAMARIND_API_KEY
      required: true
      description: Tamarind Bio API key sent as the x-api-key header.
---

# Tamarind Bio

Tamarind 在托管计算资源上运行分子设计和结构生物学工具：结构预测、蛋白质与抗体设计、对接、结合亲和力预测、MSA 生成以及分子动力学。当用户请求使用 Tamarind、其 REST API/MCP 服务器，或在云端执行这些科学工具时使用本技能。对于本地序列处理或分子描述符计算，请使用本地库。

## 来源和审查范围

REST 接口约定和公开目录的审查日期为 **2026-09-30**。示例在针对用户账户验证之前仅作示意；本次审查没有运行经过身份验证的任务，也未对任何模型的科学准确性做出验证。

- [API 索引](https://app.tamarind.bio/llms.txt) 和
  [完整指南](https://app.tamarind.bio/llms-full.txt)。
- [当前 OpenAPI](https://app.tamarind.bio/api/openapi.json) 包含发现、
  验证、任务、文件以及更新的流水线/自定义工具接口。
  [openapi.yaml](https://app.tamarind.bio/openapi.yaml) 同样可用。请检查
  所需路径是否存在：当后端规范无法获取时，合并后的规范仍可能返回 HTTP 200，
  但只包含其经典接口部分。
- [公开目录](https://app.tamarind.bio/tools.json) 不需要密钥；可用 `?type=`
  或 `?tag=` 查询。它记录的是公开工具及其条件性必填设置，而非每一个可选参数
  或账户权限。
- [产品文档索引](https://docs.tamarind.bio/llms.txt) 链接到
  Markdown 页面，包括 [MCP 指南](https://docs.tamarind.bio/tamarind/mcp-server.md)。

在编写运行任务之前，先获取账户当前的模式（schema）。当文字说明指南与 OpenAPI
存在差异时，字段结构以操作/模式定义为准，并记录任何无法解决的差异，而不要
去猜测。

## 访问

1. 使用用户的 Tamarind 部署。共享基址为
   `https://app.tamarind.bio/api`；专用的组织部署有自己的
   主机和账户数据。以下所有相对 REST 路径都位于 `/api` 之下。
2. 从部署的 API 设置中获取密钥，并从
   `TAMARIND_API_KEY` 读取它；以 `x-api-key` 的形式发送。切勿将密钥写入文件或日志中。
3. 在扩大规模之前，先检查账户当前的额度和算力预算。
   免费用量是按月计算的额度，不是永久无条件提供十个任务的承诺；
   计费和权限可能会变化。

```bash
# 公开发现接口无需凭证。
curl --fail-with-body 'https://app.tamarind.bio/tools.json?type=alphafold'
# 账户范围内的发现接口：
curl --fail-with-body 'https://app.tamarind.bio/api/tools' \
  -H "x-api-key: $TAMARIND_API_KEY"
```

对于 REST 示例，请在执行环境中安装 `requests`。官方
CLI 发行版是 **`tamarind-cli`**，其 Custom Tools Python 客户端的导入方式
为 `from tamarind import Tamarind`；名为 `tamarind` 的另一个不相关软件包
并不是这个客户端。参见 [SDK 参考文档](https://app.tamarind.bio/api-docs/custom-tools-sdk-reference)。
下文的核心任务示例直接使用 HTTP。

## 工作流程

1. **发现。** 读取 `GET /tools`，并将用户的科学任务与工具
   描述相匹配。内置工具返回一个数组；`?custom=true` 仅列出旧版
   自定义工具。当前部署的自定义工具可能不在这个列表里：在断定它不可用之前，
   先用已知的已部署名称及其模式尝试一次。
2. **读取模式。** `GET /tools/{name}/schema` 返回 `settings` 对象的
   JSON Schema。`GET /tools` 也会提供一份精简的 `settings` 参数
   列表。检查与任务相关的字段、文件扩展名、列表值和默认值。
3. **验证。** 发送 `POST /validate-job`，带上 `type`、`settings`，以及可选的
   `jobName`。先检查 HTTP 状态码，再检查 JSON 中的 `valid`。成功时，检查并
   使用返回的 `normalized` 作为要提交的设置。即使返回了 `valid: true`，
   也要处理返回的 `unrecognized_settings`：一个可选字段的拼写错误否则会悄悄地
   让默认值继续生效。验证只检查字段，不检查全部提交策略、
   队列限制或部署可用性。
4. **只提交一次。** `POST /submit-job` 接受 `jobName`、`type`、`settings`，
   自定义工具构建时的可选 `version`，以及可选/组织要求的
   `projectTag`。保存提交的名称和设置。成功响应
   是纯文本，不是 JSON 格式的回执。使用返回的存储名称。
5. **轮询。** `GET /jobs?jobName=...` 直接返回一行记录。单个任务的终止
   状态是 `Complete`、`Stopped` 和 `Failed`；要处理旧版的 `Deleted` 状态，
   或在精确查找出错时也不要无限循环。使用
   `batchStatus` 轮询批处理父任务，更新的流水线则在其各自的运行端点上轮询。
6. **下载并检查。** `POST /result` 在返回 **200** 时给出一个 JSON 字符串 URL，
   或返回 **202** 并附带 `status: "preparing"`。在 202 之后重试结果获取，
   而不要重新提交计算任务。在不带 Tamarind API 密钥请求头的情况下 GET 该签名 URL。
   只对成功运行的任务下载归档文件；对停止/失败的任务请求
   `fileName: "output.log"`。下载后请验证科学输出结果。

[工作流程示例](references/workflows.md) 实现了验证、存储名称、
有限轮询、202 处理、批量验证和分页。它们在本地用模拟响应
进行了烟雾测试；经过身份验证的实际执行尚未经过测试。

## 选择工具并解读结果

根据输入、预期输出和建模假设进行选择，然后在实际目录中
确认候选工具。以下是参考方向，而不是保证的完整目录：

| 任务 | 候选工具与决策要点 |
|---|---|
| 蛋白质/复合物结构 | `alphafold` 用于 AF2 单体/多体；`boltz`、`chai` 或 `protenix` 用于联合折叠，包括配体/核酸；`esmfold` 用于快速单序列蛋白质折叠。应单独检查 `esmfold2`：它当前的目录包含蛋白质、DNA、RNA 和配体复合物。 |
| 结合体/motif 设计 | `bindcraft`、`boltzgen`、`rfdiffusion`；根据靶点类型、骨架约束和所需的结构输入进行选择。 |
| 反折叠（Inverse folding） | `proteinmpnn`/`ligandmpnn` 以结构为输入、设计出序列。重新折叠设计结果，并与预期的骨架/界面进行比较。 |
| 小分子对接 | `autodock-vina` 用于固定受体和搜索框；`diffdock` 用于扩散式对接；`boltz`/`chai` 用于联合折叠。根据任务选择建模方式，而不是为了回避提供某个必填输入而做选择。 |
| 抗体/可开发性/MSA/MD | 根据具体任务筛选描述和模式；不同工具的可用性和输入要求各不相同。 |

置信度分数描述的是模型的信心，不是实验验证的结合、特异性
或亲和力。要对比设计出的骨架、界面、碰撞、链/残基映射
以及可开发性。检查配体的化学结构和立体化学；对接分数
不能与实测的结合自由能互换。记录工具/模型、
输入来源、链映射、随机种子/采样数、MSA/模板选择、归一化后的
设置，以及用户选定的任何筛选阈值。

尊重用户选定的工具和预算。对常规选择使用已授权的默认值；
在开展大规模任务之前，先提出那些会实质性影响科学任务或
计算范围、尚未解决的选择。永远不要因为某个科学任务的输入更容易提供，
就悄悄替换成另一个科学任务。

## 文件输入与串联

- 使用 `PUT /upload/{filename}` 上传结构文件（二进制正文；遵循
  文档中说明的重定向），然后引用注册后的相对名称，例如
  在使用了 `?folder=inputs` 时为 `target.pdb` 或 `inputs/target.pdb`。
- 使用 `GET /files` 确认名称；它为所选文件夹返回一个不分页的
  数组，而不是某个任务输出结果的列表。
- 优先使用这些路径，而不是内联的文件内容。当前指南说明，重复的
  账户邮箱前缀会被自动去除；不再存在普遍性的
  双重前缀失败问题。任意字符串并不一定是文件引用。
- 复用已完成任务的文件时，格式为 `JobName/path/to/file.ext`，要与
  下一个参数支持的扩展名及列表/标量结构相匹配。不要猜测文件名。
- ProteinMPNN 的设计结果必须送入折叠工具的 **sequence** 字段。
  结构模板字段并不意味着"折叠这个设计出的序列"。要读取生成的
  FASTA/CSV 序列，并为每个序列验证一个折叠设置对象。
- 不要自行编写内部字段，如 `submit_method`、`msa` 或 `monomer_msa`。

## 批处理与流水线

`POST /submit-batch` 接受一个 `type`、一个非空的 `settings` 数组、`batchName`，
以及可选的并行 `jobNames`。使用数组模式的
`/validate-job`（每次调用最多 1,000 行）验证**每一行**，并使用每行
返回的归一化设置。提交允许最多 **30,000 个展开后的任务**（包括设计
扇出产生的任务），并有一个单独的约 **4.5 MB** 的请求大小限制。按两个限制
分别拆分请求。不要假设旧版的 `weightedHoursBudget`、`maxRuntimeSeconds` 或
`gpuType` 请求字段会强制执行某种上限：它们已不在当前的批处理模式中。
请使用经过确认的账户控制项和双方约定好的任务/样本数量。

轮询 `GET /jobs?jobName=<batchName>`，直到 `batchStatus` 变为 `Complete`、`Stopped`
或 `AggregationFailed`。子任务可能在聚合完成之前就已完成。通过
`/result` 获取归档文件，并处理 202 响应；`resultUrl` 是可选的，不是
可靠的就绪信号。使用 `startKey` 分页浏览 `GET /jobs?batch=...` 以检查子任务。

对于新的已保存工作流，使用 `/pipelines` 下的模板/运行 API：先阅读
当前的流水线图约定，用
`POST /pipelines/validate` 验证提议的运行，用 `POST /pipelines/submit` 提交
（必填 `name`、`bindings`，以及 `templateId`/`pipeline` 二者之一），并轮询
`GET /pipelines/runs/{run_id}`。它的状态是小写的，与任务
状态是分开的两套体系。旧版的 `/submit-pipeline` 和 `/run-pipeline` 仍有文档记录；
[API 参考文档](references/api_reference.md) 给出了它们实际必填的字段。

## MCP 替代方案

使用 OAuth 2.1 或 `x-api-key` 请求头连接到 `https://mcp.tamarind.bio/mcp`。
官方指南确认支持 `submitJob`、`submitBatch`、`getJobs`、`getResult`、
`uploadFile` 和 `getFiles`。在使用其签名或解读结果包裹结构之前，
先阅读连接服务器的 `tools/list` 模式。

如果连接提供了诸如 `getAvailableTools`、`getJobSchema` 或 `validateJob` 之类
的发现/验证辅助方法，请使用它们当前的模式。额外的辅助方法、
筛选词汇表、`submitBatch(fromJob=...)`，以及通过 MCP 上传的
变体，并不受公开指南保证一定存在。本次审查匿名发起的
`tools/list` 请求返回了 401，因此其当前的接口约定未经验证。
需要时请使用文档记录的 REST 对应接口。

## 故障恢复

不同路由的 HTTP 身份验证失败表现不同：经典端点可能返回 **400**，
任务相关端点可能返回 **401** 或网关层的 **403**，用量相关端点可能返回 **401**。
403 并不能证明是预算错误。在更改设置之前，先检查状态码
和实际的响应正文。提交错误可能是 JSON 或纯文本，与 Content-Type 无关。

提交时的超时/5xx 错误并不能证明没有任何任务被排队。在重试之前
先查找已保存的名称；对于大规模任务，使用 `POST /jobs/search`，
每次请求最多 1,000 个名称。遵守速率限制，避免在大规模场景下
逐个任务地轮询。413 错误会在创建任务之前拒绝过大的请求；应拆分请求体
或单独上传文件内容。`DELETE /delete-job` 是**软删除**：它只是隐藏
该任务，已保存的结果文件保持不变。

## 参考文件

- [API 参考文档](references/api_reference.md)：接口结构、验证、
  分页、身份验证的差异，以及旧版/新版流水线的边界。
- [工具目录](references/tool_catalog.md)：模式解读与发现方法。
- [示例](references/examples.md)：基于当前目录的设置
  示例以及特定工具的注意事项，并明确说明了验证范围的局限。
- [工作流程](references/workflows.md)：可执行的 HTTP 示例，并在本地使用模拟
  响应进行了验证；本次审查未运行任何经过身份验证的实际科学任务。
