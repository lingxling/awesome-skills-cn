---
name: nextflow
description: 端到端构建、运行和调试Nextflow数据管道和nf-core工作流。只要用户提到Nextflow、nf-core、.nf文件、nextflow.config、DSL2、processes/channels/operators、samplesheets，或想要运行社区管道（例如nf-core/rnaseq、nf-core/sarek），使用nf-test编写或测试模块/子工作流，配置executors/containers（Docker、Singularity/Apptainer、Conda、Waves），将工作流扩展到HPC/SLURM或云（AWS Batch、Google Batch、Azure、Kubernetes），或调试失败/-resume运行，请务必使用此技能进行任何可重现的科学/生物信息学工作流工作，即使用户没有说"Nextflow"一词，也用于编写符合nf-core规范的管道、模块、配置和linting。
license: Apache-2.0
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# Nextflow

## 概述

Nextflow 是用于构建**可重复、可移植、可扩展**数据管道的workflow语言和运行时。它在生物信息学领域占主导地位，但适用于任何数据密集型计算。nf-core 是一个社区管理的生产级 Nextflow 管道、可重用模块，以及基于 Nextflow 的 `nf-core` 工具。

关键概念：
- **数据流编程**：管道是由**通道**连接的 `process` 任务。Nextflow 从数据依赖推断执行顺序和并行性 — 无需编写显式调度器。
- **编写一次，随处运行**：相同的管道通过更改配置/配置文件（而非代码）在本地、HPC（SLURM、SGE、LSF、PBS）和云（AWS Batch、Google Batch、Azure Batch、Kubernetes）上运行。
- **可重现性**：每任务容器（Docker/Singularity/Apptainer/Conda/Wave）+ `-resume` 缓存 + 固定的管道修订版。
- **DSL2** 是现代的必需语法：模块化的 `process`/`workflow`/`include` 定义。

此技能涵盖**运行**现有管道和**开发**自己的管道（Nextflow 语言 + nf-core 约定、使用 nf-test 测试、配置和部署）。

## 何时使用此技能

当用户想要以下操作时使用此技能：
- 运行 nf-core 或自定义 Nextflow 管道，或调试失败/恢复的运行。
- 编写或修改 `.nf` 脚本、`nextflow.config`、配置文件或 `nextflow_schema.json`。
- 编写或测试 nf-core 风格的模块/子工作流（`main.nf`、`meta.yml`、`tests/`、nf-test）。
- 配置执行器、容器或资源；扩展到 HPC 或云。
- 构建可重现的科学/生物信息学工作流程（即使没有提到"Nextflow"）。
- 理解 processes、channels、operators、`take`/`emit`、`publishDir`、`ext.args`、meta maps。

## 设置

Nextflow 需要 **Bash** 和 **Java 17 或更新版本**（支持 17–25）。用 `java -version` 验证。

```bash
# 安装 Nextflow（自包含启动器）
curl -s https://get.nextflow.io | bash      # 创建 ./nextflow
sudo mv nextflow /usr/local/bin/             # 放到 PATH 上
nextflow info                                # 验证

# 或通过 conda/bioconda（也获得托管 Java）
conda create -n nf -c bioconda -c conda-forge nextflow nf-core
```

```bash
# nf-core 工具（Python）用于创建/lint/运行 nf-core 资产
pip install nf-core            # 或: conda install -c bioconda nf-core
nf-core --version
```

固定引擎以确保可重现性：`export NXF_VER=24.10.0`（仅在需要时使用 [edge] 版本）。对于气隙/HPC，见 `references/running-pipelines.md`（离线模式）和 `references/configuration.md`。

## 两种工作模式

确定用户在哪条路径上 — 这会改变一切：

| 目标 | 从这里开始 |
|------|-----------|
| **运行**现有管道（nf-core 或给定的 `.nf`） | `references/running-pipelines.md` |
| **开发**新管道/模块/子工作流 | `references/language.md` + `references/developing.md` |
| **配置/扩展**（HPC、云、容器、资源） | `references/configuration.md` + `references/containers.md` |
| **测试**模块/管道 | `references/testing.md` |

## 快速开始

### 运行 nf-core 管道

首先始终用捆绑的 `test` 配置进行冒烟测试；它使用小型数据并证明您的环境工作正常。

```bash
# 1. 确认设置工作（下载管道 + 小型测试数据）
nextflow run nf-core/rnaseq -profile test,docker --outdir results

# 2. 实际运行：固定修订版 (-r)，选择容器引擎，传递输入
nextflow run nf-core/rnaseq -r 3.14.0 \
  -profile docker \
  --input samplesheet.csv \
  --genome GRCh38 \
  --outdir results \
  -resume
```

- `-profile`（单破折号）选择捆绑的配置文件；**组合**它们用逗号分隔，例如 `test,docker`。容器/基础设施配置文件（`docker`、`singularity`、`conda`）互斥 — 选择一个。
- `--input`、`--genome`、`--outdir`（双破折号）是**管道**参数。nf-core 管道接受**样本表 CSV**，而不是松散文件。
- `-resume` 重用上次运行的缓存结果。`-r <version>` 固定发布版本以确保可重现性。

使用 `nf-core pipelines launch <name>` 获取交互式、模式验证的方式来构建命令和 `-params-file`。见 `references/running-pipelines.md`。

### 编写最小管道

```nextflow
#!/usr/bin/env nextflow

process SAYHELLO {
    tag "$greeting"
    publishDir "results", mode: 'copy'

    input:
    val greeting

    output:
    path "${greeting}.txt"

    script:
    """
    echo '$greeting world' > ${greeting}.txt
    """
}

workflow {
    channel.of('hello', 'bonjour', 'hola') | SAYHELLO
}
```

```bash
nextflow run main.nf            # 重新运行时添加 -resume
```

完整语言（processes、channels、operators、带有 `take`/`main`/`emit` 的 DSL2 工作流、modules）在 `references/language.md` 中。

## 核心概念一览

- **Process**：运行脚本的工作单元（默认 Bash）。声明 `input:`、`output:`、可选的 `directives`（资源、容器、`publishDir`、`tag`、`errorStrategy`）和 `script:`/`shell:`/`exec:` 块。每个任务在自己的隔离工作目录（`work/xx/yy…`）中运行。
- **Channel**：连接进程的异步队列。**队列通道**是可消耗流；**值通道**保存单个可重用值。使用 `channel.of`、`channel.fromPath`、`channel.fromFilePairs`、`channel.value` 等工厂创建。
- **Operator**：转换/组合通道 — `map`、`filter`、`collect`、`groupTuple`、`join`、`combine`、`mix`、`flatten`、`branch`、`multiMap`、`splitCsv`、`view`、`set`。
- **Workflow**：组合进程。DSL2 工作流可以声明 `take:`（输入）、`main:`（逻辑）、`emit:`（命名输出）并作为子工作流包含。无名的 `workflow {}` 是入口点。
- **Module**：通过 `include { NAME } from './path'`（支持 `as` 别名）公开进程/工作流的 `.nf` 文件。
- **Configuration**：`nextflow.config` 设置 `params`、`process` 指令、`executor`、容器引擎和命名 `profiles`。选择器 `withName:`/`withLabel:` 定位特定进程。详见 `references/configuration.md`。
- **meta map** (nf-core)：在输入/输出元组中随文件一起传递元数据映射（`[ id:'sample1', single_end:false ]`）的约定，使样本在管道中保持标签。详见 `references/developing.md`。

## nf-core 工具 CLI

nf-core 工具（v3+）将子命令分组在 `pipelines`、`modules` 和 `subworkflows` 下。（像 `nf-core lint` 这样的裸形式仍然可以工作但会警告 — 优先使用分组形式。）

| 命令 | 用途 |
|------|------|
| `nf-core pipelines list` | 列出/搜索 nf-core 管道（`--json`、关键词） |
| `nf-core pipelines create` | 从 nf-core 模板脚手架新管道 |
| `nf-core pipelines launch <name>` | 交互式、模式驱动的运行命令 + 参数文件 |
| `nf-core pipelines download <name>` | 下载管道 + 容器用于离线/HPC 使用 |
| `nf-core pipelines lint` | 根据 nf-core 标准对管道进行 lint（在仓库根目录运行） |
| `nf-core pipelines schema build` | 通过 Web GUI 构建/编辑 `nextflow_schema.json` |
| `nf-core pipelines create-params-file <name>` | 生成文档化的 YAML 参数文件 |
| `nf-core pipelines bump-version` / `sync` | 提升版本 / 与模板更新同步 |
| `nf-core modules list/info/install/update/remove` | 管理来自 nf-core/modules 的模块 |
| `nf-core modules create` / `lint` / `test` | 编写、lint 和 nf-test 模块 |
| `nf-core modules patch` / `bump-versions` | 修补已安装的模块 / 提升工具版本 |
| `nf-core subworkflows install/create/lint/test` | 子工作流的相同生命周期 |

完整命令参考、标志和示例：`references/nf-core-tools.md`。

## 必需 `nextflow` CLI

| 命令 | 用途 |
|------|------|
| `nextflow run <pipeline> -profile <p> --outdir <dir>` | 运行管道（路径、`.nf` 或 `user/repo`） |
| `-resume` | 重用之前运行的缓存结果 |
| `-r <rev>` | 运行特定的 git 修订版/标签/分支 |
| `-params-file params.yml` | 从 YAML/JSON 提供参数 |
| `-c custom.config` | 叠加额外配置文件 |
| `-with-report -with-trace -with-timeline -with-dag flow.html` | 执行报告、跟踪、时间线、DAG |
| `-stub-run` | 仅运行 `stub:` 块（干运行管道） |
| `nextflow log` | 检查过去的运行 |
| `nextflow clean -f -before <run>` | 删除旧的 `work/` 数据 |
| `nextflow pull / drop / list / info <repo>` | 管理缓存的远程管道 |

配置、执行器、缓存内部和跟踪详情：`references/configuration.md`。

## 最佳实践（高价值习惯）

- **始终先 `test`**：在真实数据之前使用 `-profile test,docker`（或 `singularity`/`conda`）— 快速且能发现环境问题。
- **固定一切**：管道修订版（`-r`）、`NXF_VER` 和工具版本（容器）。不要为您将发表的科学运行 `latest`。
- **使用 `-resume`** 并理解缓存：如果其输入、脚本或容器更改，任务将重新运行。详见 `references/configuration.md` 中的缓存调试。
- **通过 config/params-file 参数化**，而非硬编码路径。将 `params` 和 profiles 保存在 `nextflow.config` 中。
- **每个进程一个容器/conda 环境**；永远不要依赖主机上安装的工具。
- **对于 nf-core 开发**：在编写新模块之前重用现有模块（`nf-core modules install`）；通过 `ext.args` 传递工具标志（而非在脚本中硬编码）；始终包含 `stub:` 块和 nf-test 测试；在提交之前运行 `nf-core pipelines lint` 和 `prettier`。
- **正确调整资源大小**使用 `process_low/medium/high` 标签和 `errorStrategy 'retry'` 以及动态 `task.attempt` 扩展，而非一个巨大请求。
- **编写向前兼容的语法**：严格语法解析器将在 Nextflow 26.04 中成为默认。优先使用小写 `channel.of(...)`、显式闭包参数（`{ v -> ... }`）、所有变量使用 `def`，以及 `emit:` 命名输出。用 `nextflow lint` 检查。

## 参考文件

需要深度时阅读相关文件 — 每个都是独立的：

- `references/language.md` — DSL2 语言：processes、directives、channels、operators、工作流（`take`/`emit`）、modules、动态资源、错误处理。
- `references/configuration.md` — `nextflow.config`、作用域、`profiles`、`withName`/`withLabel` 选择器、执行器（local/SLURM/云）、缓存/`-resume` 内部、跟踪/报告、`nextflow` CLI。
- `references/containers.md` — Docker、Singularity/Apptainer、Podman、Conda、Wave 容器；选择和启用引擎；常见陷阱。
- `references/running-pipelines.md` — 查找/运行 nf-core 管道、样本表、参数文件、参考基因组（iGenomes）、离线运行、机构配置、Seqera 平台。
- `references/nf-core-tools.md` — 完整 `nf-core` CLI 参考（pipelines/modules/subworkflows）、标志和工作流。
- `references/developing.md` — 编写 nf-core 管道和模块：模板布局、模块 `main.nf`/`meta.yml`、meta maps、`ext.args`/`modules.config`、子工作流、资源标签、linting 和 Harshil 对齐风格。
- `references/testing.md` — 模块/子工作流/管道的 nf-test：测试结构、断言、快照、标签、运行测试、CI。

官方文档：Nextflow https://www.nextflow.io/docs/latest/ · nf-core https://nf-co.re/docs/ · 培训 https://training.nextflow.io/
