# Scientific Agent Skills 中文翻译

> 本文档是 [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) 项目的中文翻译版本。

## 关于本翻译

### 原项目介绍

**Scientific Agent Skills** 是由 [K-Dense](https://k-dense.ai) 创建的综合性科学与研究技能集合，目前包含 **177 个即用型科学和研究技能**，涵盖生物学、化学、医学、物理学、工程学、地球科学、数据分析和科学交流等领域，并记录了 100+ 个科学与金融数据库。该集合遵循开放的 [Agent Skills](https://agentskills.io/) 标准，适用于 **Cursor、Claude Code、Codex、Google Antigravity** 等任何支持该标准的 AI 代理，可将您的 AI 代理转变为能够跨多个科学领域执行复杂多步骤研究工作流的"AI 科学家"。

每个技能都是自包含的，在自己的文件夹中包含 `SKILL.md` 文件，其中包含 AI 代理使用的指令和元数据。

### 翻译说明

本翻译包含以下技能的中文翻译：

- [scientific-skills/](scientific-skills/) - 177 个科学和研究技能，涵盖生物信息学、化学信息学、临床研究、机器学习、数据可视化等多个领域

### 原项目链接

- [GitHub 仓库](https://github.com/K-Dense-AI/scientific-agent-skills)
- [Agent Skills 规范](https://agentskills.io/)
- [K-Dense 官网](https://k-dense.ai/)

### 翻译项目

本翻译属于 [awesome-skills-cn](https://github.com/lingxling/awesome-skills-cn) 项目的一部分，致力于将优秀的英文 SKILL 翻译成中文。

---

# Scientific Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![arXiv](https://img.shields.io/badge/arXiv-2609.00065-b31b1b.svg)](https://arxiv.org/abs/2609.00065)
[![Version](https://img.shields.io/badge/Version-2.72.0-blue.svg)](pyproject.toml)
[![Skills](https://img.shields.io/badge/Skills-177-brightgreen.svg)](#-whats-included)
[![Databases](https://img.shields.io/badge/Databases-100%2B-orange.svg)](#-whats-included)
[![Agent Skills](https://img.shields.io/badge/Standard-Agent_Skills-blueviolet.svg)](https://agentskills.io/)
[![Agent Plugins](https://img.shields.io/badge/Standard-Agent_Plugins-0A7A72.svg)](https://agent-plugins.org/)
[![Security Scan](https://github.com/K-Dense-AI/scientific-agent-skills/actions/workflows/security-scan.yml/badge.svg)](https://github.com/K-Dense-AI/scientific-agent-skills/actions/workflows/security-scan.yml)
[![Skill Tests](https://github.com/K-Dense-AI/scientific-agent-skills/actions/workflows/skill-tests.yml/badge.svg)](https://github.com/K-Dense-AI/scientific-agent-skills/actions/workflows/skill-tests.yml)
[![Works with](https://img.shields.io/badge/Works_with-Cursor_|_Claude_Code_|_Codex_|_Google_Antigravity-blue.svg)](#-getting-started)
[![X](https://img.shields.io/badge/Follow_on_X-%40k__dense__ai-000000?logo=x)](https://x.com/k_dense_ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-K--Dense_Inc.-0A66C2?logo=linkedin)](https://www.linkedin.com/company/k-dense-inc)
[![YouTube](https://img.shields.io/badge/YouTube-K--Dense_Inc.-FF0000?logo=youtube)](https://www.youtube.com/@K-Dense-Inc)
[![Reddit](https://img.shields.io/badge/Reddit-u%2F--k--dense---FF4500?logo=reddit&logoColor=white)](https://www.reddit.com/user/-k-dense-/)

> **🔔 Claude Scientific Skills 现已更名为 Scientific Agent Skills。** 技能不变，兼容性更广——现在可与任何支持开放 [Agent Skills](https://agentskills.io/) 标准的 AI 代理配合使用，不再局限于 Claude。

> **全新：[K-Dense BYOK](https://github.com/K-Dense-AI/k-dense-byok)** —— 一款免费、开源的 AI 共同科学家，运行在您的桌面上，由 Scientific Agent Skills 驱动。自带 API 密钥，可从 40+ 模型中选择，获得一个完整的研究工作区：网络搜索、文件处理、100+ 科学数据库，以及本仓库全部 177 个技能的访问权限。您的数据保留在您的电脑上，对于繁重的工作负载，也可以选择通过 [Modal](https://modal.com/) 扩展到云计算。[从这里开始。](https://github.com/K-Dense-AI/k-dense-byok)

> **🎥 网络研讨会录像 —— [K-Dense BYOK 入门指南](https://youtu.be/Du3BIE48DKc?si=9dPpETKSc2PeQbvU)**
> 对 [K-Dense BYOK](https://github.com/K-Dense-AI/k-dense-byok) 的实操讲解——这是一款免费、开源、在您自己机器上本地运行的 AI 共同科学家，由 Scientific Agent Skills 提供支持。我们介绍了如何设置它、使用自己的 API 密钥，以及如何用这些技能运行真实的研究工作流。无需任何技术背景。**[观看录像 →](https://youtu.be/Du3BIE48DKc?si=9dPpETKSc2PeQbvU)**

> **保持关注：** 在 [X](https://x.com/k_dense_ai)、[LinkedIn](https://www.linkedin.com/company/k-dense-inc)、[YouTube](https://www.youtube.com/@K-Dense-Inc) 和 [Reddit](https://www.reddit.com/user/-k-dense-/) 上关注 K-Dense，获取新技能、发布公告、演示讲解、研究工作流演示，以及可用于您自己 AI 代理的示例。

> **📄 论文：** Scientific Agent Skills 已在论文 [*Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*](https://arxiv.org/abs/2609.00065)（arXiv:2609.00065）中描述。如果您在研究中使用了这些技能，请[引用该论文](#-citation)。

一个综合性集合，包含 **177 个科学和研究技能**，由 [K-Dense](https://k-dense.ai) 创建。这些技能涵盖生物学、化学、医学、物理学、工程学、地球科学、数据分析和科学交流。每个技能都为特定的软件包、数据源或工作流提供指导，包括使用它所需的科学规范和验证检查。

该集合遵循开放的 [Agent Skills](https://agentskills.io/) 标准，可与 **Cursor、Claude Code、Codex、Google Antigravity 以及其他兼容主机**配合使用。它同时也是一个可移植的 [Agent Plugins](https://agent-plugins.org/) 软件包（`plugin.json` + `skills/`），因此支持该标准的客户端可以将整个集合作为一个插件加载。浏览[图解技能指南](docs/skill-guides/README.md)、[技能分类](#-available-skills)或[完整目录](docs/skills.md)，选择与您的工作相关的技能。

> ⭐ **帮助让 AI 用于科学更易被发现：** 如果 Scientific Agent Skills 为您节省了时间，教会您的代理某种工作流，或帮助您的实验室更快推进，请 [为此仓库加星标](https://github.com/K-Dense-AI/scientific-agent-skills)。星标是一个公开信号，表明这些开放、可重用的研究技能值得维护：它帮助科学家、工程师和开源贡献者找到这个项目，显示哪些代理技能标准正在获得真正的采用，并给我们一个明确的理由，为社区继续扩展这个集合。

---

这些技能让您的 AI 代理能够无缝地跨多个科学领域使用专业的科学库、数据库和工具。虽然代理本身也能独立使用任何 Python 包或 API，但这些明确定义的技能提供了精心策划的文档和示例，使其在以下工作流中显著更强大、更可靠：
- 🧬 生物信息学与基因组学 - 序列分析、单细胞 RNA-seq、合并 CRISPR 筛选、引物设计、扩增子微生物组、变异注释、系统发育学
- 🧪 化学信息学与药物发现 - 分子性质预测、虚拟筛选、ADMET 分析、分子对接、先导化合物优化、经校准的一维 NMR 处理
- 🔬 蛋白质组学与质谱 - LC-MS/MS 处理、肽段鉴定、光谱匹配、蛋白质定量
- 🏥 临床研究与证据工作流 - 临床试验、药物基因组学、变异证据审查、药代动力学/药效动力学建模与给药方案评估、汇总型决策支持评估、源证据支撑的报告草稿结构，以及临床医生所做治疗决策的格式化
- 🧠 医疗 AI 与生物信号研究 - EHR 与模型研究、生理信号分析、回顾性验证——而非针对具体患者的诊断、治疗、报警或部署决策
- 🐭 临床前研究与动物福利 - 面向实验动物研究的多变量严重程度评分与人道终点预测，用于 3R（减少、优化、替代）/优化分析和 EU 指令 2010/63/EU 报告——是严重程度评估的辅助工具，绝非决策规则
- 🖼️ 显微成像、医学影像与数字病理 - 定量荧光显微成像、注重隐私的 DICOM 处理、仅限研究用途的全切片图像分析、计算病理学，以及放射学数据工作流
- 🧠 神经科学与电生理学 - BIDS 数据集、NWB 转换与时钟对齐、细胞外记录以及生理信号
- 🤖 机器学习与 AI - 深度学习、强化学习、时间序列分析、模型可解释性、贝叶斯方法
- 🔮 材料科学与化学 - 晶体结构分析、CALPHAD 相平衡、代谢建模、计算化学
- 🌌 物理学与天文学 - 天文数据分析、坐标变换、宇宙学计算、符号数学、物理计算
- ⚙️ 工程与仿真 - 电池循环模型、化学动力学与点火延迟、流体力学、实验室硬件 CAD 与定制零件制造、离散事件仿真、过程优化
- 📊 数据分析与可视化 - 统计分析、网络分析、时间序列、出版级图形、大规模数据处理、EDA
- 🌊 海洋化学 - 海水碳酸盐化学、海洋酸化、矿物饱和度以及测量不确定度
- 🌍 地理空间科学与遥感 - 卫星影像处理、GIS 分析、空间统计、地形分析、面向地球观测的机器学习
- 🧪 实验室自动化 - 液体处理协议、实验室设备控制、工作流自动化、LIMS 集成
- 📚 科学交流 - 证据可追溯的写作、保密授权的同行评审、文献综述、文档处理、无宏 PPTX 海报、幻灯片、示意图和引用管理
- 🔬 多组学与系统生物学 - 多模态数据整合、通路分析、碳-13 代谢流推断、生化动力学模型
- 🧬 蛋白质工程与设计 - 蛋白质语言模型、结构预测、冷冻电镜精修、序列设计、功能注释
- 🧰 代理平台与基础设施 - 基于 Pi 构建，涵盖 SDK、RPC、扩展、自定义 provider/模型、包、TUI 组件和会话工具
- 🎓 研究方法论 - 证据约束下的候选假设、科学头脑风暴、批判性思维、资助写作，以及对学术著作的低风险定性评估
- ⚖️ 监管与标准 - 为 ISO 管理体系和实验室标准起草证据准备文件，以及依据 ICH/USP/CLSI 框架开展的分析方法验证、确认与转移——供具备资质的审查人员使用，绝非认证、资质认定或方法放行的决定

**将您的 AI 编码代理转变为桌面上的"AI 科学家"！**

> 🎬 **Scientific Agent Skills 新手？** 观看我们的 [Scientific Agent Skills 入门指南](https://youtu.be/ZxbnDaD_FVg) 视频，快速了解如何上手。

### 🎥 更多教程

来自 [K-Dense YouTube 频道](https://www.youtube.com/@K-Dense-Inc) 的真实研究任务实操录像：

| 视频 | 内容概要 |
|-------|----------------|
| [技能 101：打造你自己的 Scientific Agent Skill](https://youtu.be/lVZbHiwzMEg) | 从零开始编写、测试并打包一个新技能 |
| [文献综述与假设生成](https://youtu.be/wKJp8y4ZyiM) | 检索文献并生成有据可依的假设 |
| [起草并预算一份实验方案](https://youtu.be/Yz2L5s_M_34) | 将一个计划中的实验转化为带预算的书面方案 |
| [起草对审稿人意见的回复](https://youtu.be/0MmU-Pmtg1o) | 根据审稿反馈逐条构建回复意见 |
| [AI 能否复现一篇 Nature Medicine 论文？](https://youtu.be/4WTCK9kSfdk) | 对一篇已发表分析进行端到端复现的尝试 |

---

## 📦 包含内容

本仓库提供 **177 个科学和研究技能**，组织成以下类别：

- **100+ 科学与金融数据库** - [Database Lookup](skills/database-lookup/SKILL.md) 技能记录了 80 个具有公开、注册或授权访问权限的数据库（PubChem、ChEMBL、UniProt、COSMIC、ClinicalTrials.gov、FRED、USPTO 等），包括端点选择、分页和溯源信息。专门的技能覆盖了 DepMap、Imaging Data Commons、PrimeKG、NCATS ARAX、U.S. Treasury Fiscal Data、Hugging Science、OneKGPd、Genomic Intelligence 和 AlphaGenome。像 BioServices、Biopython 和 gget 等多数据库包进一步增加了覆盖范围
- **70+ 经过优化的 Python 包技能** - 为 RDKit、Scanpy、PyTorch Lightning、scikit-learn、PyTDC、PathML、pydicom、NeuroKit2、PufferLib、QuTiP、GeoPandas、pymatgen、BioPython、Qiskit、分子动力学（OpenMM/MDAnalysis）等明确定义、具备版本意识的工作流。代理仍然可以使用*任何* Python 包；这些技能为所列出的包提供更强、更安全的指导
- **9 个科学集成技能** - 为 Benchling、DNAnexus、LatchBio、OMERO、Protocols.io、Open Notebook、Ginkgo Cloud Lab、LabArchives 和 Opentrons 明确定义的技能。同样，代理并不局限于这些——任何可以从 Python 访问的 API 或平台都可以使用；这些技能是已优化、预先记录的路径
- **30+ 分析与交流工具** - 文献综述、证据可追溯的科学写作、保密的同行评审、文档处理、Paperclip（带有行级定位引用的全文论文、FDA/PMDA/EMA 申报文件和试验注册库）、Paperzilla、Exa Search、无宏 PPTX 海报、幻灯片、示意图、信息图表、Mermaid 图表等
- **10+ 研究与临床工具** - 证据约束下的假设生成、资助写作、汇总型临床决策支持研究、临床医生所写治疗方案的格式化、PK/PD 建模与仿真（NCA、群体 PK、暴露-反应、生物等效性、首次人体给药）、BIDS、ISO 标准合规证据准备（ISO 13485、ISO 14971、ISO/IEC 17025、ISO 15189）、分析方法验证与转移（ICH Q2(R2)/Q14、ICH M10、USP、CLSI EP）、情景分析，以及通过 Autoskill 进行的工作流派生技能起草

每个技能都有一个 `SKILL.md` 文件，说明其目的、工作流和版本元数据。根据工作流的不同，它还可能包含代码示例、参考文档、可执行辅助脚本或模板。带有 `scripts/` 的技能在 `tests/<skill-name>/` 下有对应的测试套件，并在 [`tests/skill-requirements.toml`](tests/skill-requirements.toml) 中有依赖项条目。

### 2.72.0 版本的新内容

`docx`、`pdf`、`pptx` 和 `xlsx` 文档技能此前是从 [anthropics/skills](https://github.com/anthropics/skills) 以 Anthropic 自己的许可证引入（vendored）的，现已不再随本仓库打包。该集合现在共有 **177 个技能**；如果您依赖这四个技能，请从 Anthropic 的仓库中单独安装。[Scientific Slides](skills/scientific-slides/SKILL.md) 现在使用 PptxGenJS 或 python-pptx 构建 PowerPoint 演示文稿，并通过 LibreOffice 以及自带的渲染与验证脚本进行审查。

### 2.71.0 版本的新内容

此次更新刷新了全部 **181 个技能**，包括软件包和 API 指南、依赖项要求、参考文档和验证工作流。主要亮点包括：

- **数据库检索：** [Database Lookup](skills/database-lookup/SKILL.md) 现在编目了 80 个数据源，包含访问要求、检索契约和溯源检查。
- **软件包兼容性：** 更新后的文档基线包括 [PathML 3.0.8](skills/pathml/SKILL.md)、[GeoPandas 1.2.0](skills/geopandas/SKILL.md)，以及用于实验室硬件 CAD 的 [build123d 0.13.0](skills/lab-hardware-cad/SKILL.md)。[PufferLib](skills/pufferlib/SKILL.md) 区分了原生 5.0、PyPI 3.0.0 和历史版本 4.0 的工作流。
- **图像生成与代理工具：** [Generate Image](skills/generate-image/SKILL.md) 使用 OpenRouter Image API，具备模型发现和请求验证功能。[Pi Agent](skills/pi-agent/SKILL.md) 记录了 Pi 0.99.2、原生 MCP 以及更新后的生态系统软件包。
- **RNA-seq 工作流边界：** [Bulk RNA-seq](skills/bulk-rnaseq/SKILL.md) 为交接给 [PyDESeq2](skills/pydeseq2/SKILL.md) 准备读取数据和经过验证的计数；[Pathway Enrichment](skills/pathway-enrichment/SKILL.md) 负责下游的富集分析。

每个技能都记录了自己的兼容性要求和验证范围。在复用较旧的工作流之前，请检查这些细节；本地测试、实时服务检查和示例说明的覆盖范围各不相同。

### 近期新增的工作流

| 研究任务 | 技能 | 工作流重点 |
|---|---|---|
| 设计并分析实验 | [Primer Design](skills/primer-design/SKILL.md)、[FlowKit](skills/flowkit/SKILL.md)、[MAGeCK](skills/mageck/SKILL.md)、[CellProfiler](skills/cellprofiler/SKILL.md) | PCR 特异性筛选、流式细胞仪补偿与门控、合并 CRISPR 对比分析，以及显微成像分割质控 |
| 处理光谱并建模代谢 | [nmrglue](skills/nmrglue/SKILL.md)、[13C Metabolic Flux](skills/13c-metabolic-flux/SKILL.md)、[Tellurium](skills/tellurium/SKILL.md) | 经校准的一维 NMR、带可辨识性检查的同位素追踪推断，以及可重复的生化仿真 |
| 重建结构并保存神经数据 | [RELION](skills/relion/SKILL.md)、[NWB Conversion](skills/nwb-conversion/SKILL.md) | 冷冻电镜半图验证，以及带时钟对齐的双光子成像/行为转换 |
| 分析微生物组与海水化学 | [QIIME 2 Amplicon](skills/qiime2-amplicon/SKILL.md)、[Marine Carbonate Chemistry](skills/marine-carbonate-chemistry/SKILL.md) | 带读取保留率检查的双端 16S 处理、碳酸盐分布计算以及测量不确定度 |
| 模拟能源与材料系统 | [PyBaMM](skills/pybamm/SKILL.md)、[Cantera](skills/cantera/SKILL.md)、[pycalphad](skills/pycalphad/SKILL.md) | 电池循环、点火延迟，以及带数值检查和输入溯源的合金相平衡 |

---

## 📋 目录

- [包含内容](#-whats-included)
- [2.72.0 版本的新内容](#whats-new-in-2720)
- [近期新增的工作流](#recently-added-workflows)
- [为什么使用这个？](#-why-use-this)
- [入门指南](#-getting-started)
- [安全免责声明](#%EF%B8%8F-security-disclaimer)
- [支持开源社区](#%EF%B8%8F-support-the-open-source-community)
- [先决条件](#%EF%B8%8F-prerequisites)
- [快速示例](#-quick-examples)
- [用例](#-use-cases)
- [可用技能](#-available-skills)
- [来自博客](#-from-the-blog)
- [贡献](#-contributing)
- [故障排除](#-troubleshooting)
- [常见问题](#-faq)
- [支持](#-support)
- [引用](#-citation)
- [许可证](#-license)

---

## 🚀 为什么使用这个？

### ⚡ **加速您的研究**
- **节省数天的工作** - 跳过 API 文档研究和集成设置
- **经过审查的起点** - 具备明确验证、溯源和安全边界的测试示例；请在目标环境中自行验证
- **多步骤工作流** - 通过单个提示执行复杂的流水线

### 🎯 **全面覆盖**
- **177 个技能** - 覆盖所有主要科学领域
- **100+ 数据库** - Database Lookup 记录了 80 个数据库，加上专用的数据访问技能，以及 BioServices、Biopython、gget 等多数据库包
- **70+ 经过优化的 Python 包技能** - 为 RDKit、Scanpy、PyTorch Lightning、scikit-learn、PyTDC、pydicom、PufferLib、QuTiP、GeoPandas、pymatgen、Qiskit、分子动力学（OpenMM/MDAnalysis）、scVelo 和 TimesFM 等软件包提供最新的、按版本限定的指南（代理可以使用任何 Python 包；这些是预先记录好的路径）

### 🔧 **易于集成**
- **简单设置** - 将技能复制到您的技能目录并开始工作
- **配置化发现** - 兼容的主机可以从其配置的技能路径中发现并使用相关技能
- **文档完善** - 每个技能都包含示例、用例和最佳实践

### 🌟 **持续维护与支持**
- **定期更新** - 由 K-Dense 团队持续维护和扩展
- **CI 中的验证** - 相关的拉取请求会运行仓库范围的结构检查，以及仅依赖标准库的技能测试套件。科学依赖项会在独立环境中测试；完整的验证工作流请参见[测试](#testing)
- **社区驱动** - 开源，具有活跃的社区贡献
- **企业就绪** - 为高级需求提供商业支持

---

## 🎯 入门指南

### 选项 1：npx（受支持的主机）

使用单个命令安装 Scientific Agent Skills：

```bash
npx skills add K-Dense-AI/scientific-agent-skills
```

这是一种基于通用标准的安装器，适用于受支持的 Agent Skills 主机，包括当前版本的 **Claude Code**、**Claude Cowork**、**Codex**、**Gemini CLI**、**Google Antigravity** 和 **Cursor**。请以您所用主机的最新文档确认安装路径和可选元数据的具体行为。

### 选项 2：GitHub CLI (`gh skill`)

如果您使用 [GitHub CLI](https://cli.github.com/)（v2.90.0+），可以使用 [`gh skill`](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) 安装技能：

```bash
# 交互式浏览和安装
gh skill install K-Dense-AI/scientific-agent-skills

# 直接安装特定技能
gh skill install K-Dense-AI/scientific-agent-skills scanpy

# 针对特定代理主机
gh skill install K-Dense-AI/scientific-agent-skills --agent cursor
gh skill install K-Dense-AI/scientific-agent-skills --agent claude-code
gh skill install K-Dense-AI/scientific-agent-skills --agent codex
gh skill install K-Dense-AI/scientific-agent-skills --agent gemini
```

`gh skill` 会自动安装到适合您的代理主机的正确目录，并为供应链完整性记录来源元数据。

#### 版本固定

固定到特定的发布标签或提交 SHA，以实现可重复的安装：

```bash
# 固定到发布标签
gh skill install K-Dense-AI/scientific-agent-skills --pin v2.71.0

# 固定到提交 SHA
gh skill install K-Dense-AI/scientific-agent-skills --pin abc123def
```

#### 保持技能更新

```bash
# 交互式检查更新
gh skill update

# 更新所有已安装的技能
gh skill update --all
```

### 选项 3：Agent Plugins（Cursor、Codex 及其他插件客户端）

本仓库是一个有效的 [Agent Plugins](https://agent-plugins.org/) 1.0.0 软件包：根目录下的 [`plugin.json`](plugin.json) 加上 `skills/` 下的 Agent Skills。支持该标准的客户端会发现 `skills/` 下每一个包含 `SKILL.md` 的直接子目录。

**Cursor** —— 将仓库软链接或复制到本地插件目录，然后重新加载：

```bash
mkdir -p ~/.cursor/plugins/local
ln -s "$(pwd)" ~/.cursor/plugins/local/scientific-agent-skills
```

重启 Cursor 或运行 **Developer: Reload Window**，然后在 **Customize** 下确认插件及其技能已出现。参见 [Cursor plugins](https://cursor.com/docs/plugins)。

**Codex** —— 从本地检出目录安装（请以 Codex 文档确认当前 CLI 标志名称）：

```bash
codex plugins install .
```

兼容的客户端（Cursor、Codex、GitHub Copilot、VS Code、Kiro 以及 [agent-plugins.org](https://agent-plugins.org/compatible-clients) 上列出的其他客户端）共享相同的软件包结构；安装体验仍因客户端而异。

### 其他 Agent Skills 主机（OpenClaw、NemoClaw、Pi、Hermes 等）

不同的代理主机在安装路径、发现设置以及对可选前置数据字段的支持上各不相同。`npx skills add`（选项 1）通常会安装到 `~/.agents/skills/` 这一惯例目录，项目范围的安装则位于 `.agents/skills/` 下；请以您所用主机的最新文档确认这两个路径。若要在配置为扫描上述位置之一的主机上手动安装：

```bash
git clone https://github.com/K-Dense-AI/scientific-agent-skills.git ~/.agents/skills/scientific-agent-skills   # 用户级别
git clone https://github.com/K-Dense-AI/scientific-agent-skills.git .agents/skills/scientific-agent-skills      # 项目级别
```

对于支持技能 tap 的 Hermes 版本，将本仓库添加为 tap：

```bash
hermes skills tap add K-Dense-AI/scientific-agent-skills
```

每个 `SKILL.md` 都使用带有带引号 `metadata.version` 的 YAML 前置数据。仓库贡献必须使用块状 YAML；JSON 风格的流式映射无法通过参考验证器。可选的主机专属配置应放在 `metadata` 下，主机清单块保持为嵌套映射。完整规则参见 [AGENTS.md](AGENTS.md#frontmatter)。不同主机对可选元数据和凭据提示的解释可能不同，请在目标主机上验证行为。只安装与您工作相关的主题子集，可以让可用的技能目录保持聚焦。

> **NemoClaw 说明：** NemoClaw 在 NVIDIA OpenShell 内运行代理，默认拒绝一切出站网络访问。技能会正常被发现和加载，但任何需要网络的技能——通过 `uv` 安装包，或调用 API（Exa、Parallel、Benchling、NCBI、Materials Project 等）——只有在操作员在 OpenShell TUI 中预先批准相关域名后才能工作。

**就这样！** 兼容的主机可以从其配置的路径中发现技能，并在相关时使用它们。您还可以通过在提示中提及技能名称来手动调用任何技能。

---

## ⚠️ 安全免责声明

> **技能可以执行代码并影响您的编码代理的行为。请审查您安装的内容。**

Agent Skills 非常强大——它们可以指示您的 AI 代理运行任意代码、安装软件包、发出网络请求，并修改您系统上的文件。恶意或编写不良的技能有可能把您的编码代理引导至有害行为。

我们重视安全。所有贡献都要经过审查流程，我们还会对本仓库中的每一个技能运行基于 LLM 的安全扫描（通过 [Cisco AI Defense Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner)）。然而，作为一个小团队，面对日益增多的社区贡献，我们无法保证每个技能都已针对所有可能的风险进行了详尽审查。

**最终，审查您所安装的技能并决定信任哪些技能，是您自己的责任。**

我们建议：

- **不要一次性安装所有内容。** 只安装您实际工作所需的技能。在 K-Dense 创建并维护每一个技能时，安装完整集合是合理的，但如今仓库中已包含大量社区贡献，我们可能没有同样彻底地审查过。
- **安装前先阅读 `SKILL.md`。** 每个技能的文档都描述了它的作用、使用的软件包，以及连接的外部服务。如果有任何可疑之处，请不要安装它。
- **检查贡献历史。** 由 K-Dense（`K-Dense-AI`）编写的技能都经过了我们的内部审查流程。社区贡献的技能也已尽我们所能进行了审查，但资源有限。
- **自行运行安全扫描器。** 在安装第三方技能之前，在本地扫描它们：
  ```bash
  uv pip install cisco-ai-skill-scanner
  skill-scanner scan /path/to/skill --use-behavioral
  ```
- **报告任何可疑内容。** 如果您发现某个技能看起来有恶意或行为异常，请立即[提交 issue](https://github.com/K-Dense-AI/scientific-agent-skills/issues)，以便我们进行调查。

技能每周都会被扫描一次——以增量方式进行，未变更的技能会沿用之前的扫描结果，并且至少每 30 天、以及每当扫描器或模型发生变化时会进行一次全量重新扫描——结果会发布到 [docs/security-report.md](docs/security-report.md)。我们的安全政策、适用范围、私密报告漏洞的方式，以及如何对扫描结论提出异议，请参见 [SECURITY.md](SECURITY.md)。我们会尽力随时解决出现的安全缺口。

---

## ❤️ 支持开源社区

Scientific Agent Skills 由 **50+ 个了不起的开源项目**提供支持，这些项目由全球各地敬业的开发者和研究社区维护。像 Biopython、Scanpy、RDKit、scikit-learn、PyTorch Lightning 等项目构成了这些技能的基础。

**如果您在本仓库中发现了价值，请考虑支持让它成为可能的这些项目：**

- ⭐ 在 GitHub 上**为它们的仓库加星**
- 💰 通过 GitHub Sponsors 或 NumFOCUS **赞助维护者**
- 📝 在您的出版物中**引用这些项目**
- 💻 **贡献**代码、文档或错误报告

👉 **[查看完整的待支持项目列表](docs/open-source-sponsors.md)**

---

## ⚙️ 先决条件

- **Python**：仓库工具需要 3.13+；个别技能的依赖项可能支持更广泛的 Python 版本范围
- **uv**：Python 包管理器（安装技能依赖项所必需）
- **客户端**：任何支持 [Agent Skills](https://agentskills.io/) 标准的代理（Cursor、Claude Code、Gemini CLI、Codex、Google Antigravity 等）
- **系统**：macOS、Linux，或带有 WSL2 的 Windows
- **依赖项**：请遵循各技能的 `compatibility` 字段和设置说明来安装软件包、系统工具、凭据和网络访问。仅安装技能文件并不会安装它们的依赖项

请为每个科学工作流使用独立的环境：部分技能需要不同的 Python 版本，或存在不兼容的软件包固定版本。`uv sync` 只会安装仓库的开发与验证工具，并不会安装集合中的每一个科学软件包。

### 安装 uv

这些技能使用 `uv` 作为安装 Python 依赖项的包管理器。请按照您操作系统对应的说明进行安装：

**macOS 和 Linux：**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows：**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**替代方案（通过 pip）：**
```bash
pip install uv
```

安装完成后，运行以下命令验证它是否正常工作：
```bash
uv --version
```

更多安装选项和细节，请访问[官方 uv 文档](https://docs.astral.sh/uv/)。

---

## 💡 快速示例

安装好技能之后，您可以让 AI 代理执行复杂的多步骤科学工作流。以下是一些示例提示：

### 🧪 药物发现流水线
**目标**：为肺癌临床前研究筛选并优先排序 EGFR 抑制剂候选物

**提示**：
```
Use available skills you have access to whenever possible. Query ChEMBL for EGFR inhibitors (IC50 < 50nM), analyze structure-activity relationships 
with RDKit, generate improved analogs with datamol, perform virtual screening with DiffDock 
against AlphaFold EGFR structure, search PubMed for resistance mechanisms, check COSMIC for 
mutations, and create visualizations and a comprehensive report.
```

**使用的技能**：database-lookup、rdkit、datamol、diffdock、paper-lookup、scientific-visualization

---

### 🔬 单细胞 RNA-seq 分析
**目标**：对 10X Genomics 数据进行综合分析，并整合公共数据

**提示**：
```
Use available skills you have access to whenever possible. Load 10X dataset with Scanpy, perform QC and doublet removal, integrate with Cellxgene 
Census data, identify cell types using NCBI Gene markers, run differential expression with 
PyDESeq2, infer gene regulatory networks with Arboreto, enrich pathways via Reactome/KEGG, 
and identify therapeutic targets with Open Targets.
```

**使用的技能**：scanpy、cellxgene-census、database-lookup、pydeseq2、arboreto

---

### 🧬 多组学生物标志物发现
**目标**：整合 RNA-seq、蛋白质组学和代谢组学数据以预测患者结局

**提示**：
```
Use available skills you have access to whenever possible. Analyze RNA-seq with PyDESeq2, process mass spec with pyOpenMS, integrate metabolites from 
HMDB/Metabolomics Workbench, map proteins to pathways (UniProt/KEGG), find interactions via 
STRING, correlate omics layers with statsmodels, build predictive model with scikit-learn, 
and search ClinicalTrials.gov for relevant trials.
```

**使用的技能**：pydeseq2、pyopenms、database-lookup、statsmodels、scikit-learn

---

### 🎯 虚拟筛选活动
**目标**：发现蛋白质-蛋白质相互作用的变构调节剂

**提示**：
```
Use available skills you have access to whenever possible. Retrieve AlphaFold structures, identify interaction interface with BioPython, search ZINC 
for allosteric candidates (MW 300-500, logP 2-4), filter with RDKit, dock with DiffDock, 
rank with DeepChem, check PubChem suppliers, search USPTO patents, and optimize leads with 
MedChem/molfeat.
```

**使用的技能**：database-lookup、biopython、rdkit、diffdock、deepchem、medchem、molfeat

---

### 🏥 研究性变异证据审查
**目标**：为遗传性癌症研究和合格人员审查，注释一份合成或经过适当去标识化处理的 VCF 文件

**提示**：
```
Use available skills you have access to whenever possible. Work only with authorized synthetic
or de-identified data. Parse the VCF with pysam, annotate variants with Ensembl VEP, retrieve
ClinVar/COSMIC/NCBI Gene/UniProt evidence, and verify literature sources. Build an evidence-
traceable research summary with scientific-writing. If clinical-reports is used, create only a
visibly marked draft structure from a verified source-fact manifest for qualified review; do not
diagnose, assess individual risk, recommend treatment, or determine trial eligibility.
```

**使用的技能**：pysam、database-lookup、paper-lookup、scientific-writing、clinical-reports

---

### 🌐 系统生物学网络分析
**目标**：从 RNA-seq 数据分析基因调控网络

**提示**：
```
Use available skills you have access to whenever possible. Query NCBI Gene for annotations, retrieve sequences from UniProt, identify interactions via 
STRING, map to Reactome/KEGG pathways, analyze topology with Torch Geometric, reconstruct 
GRNs with Arboreto, assess druggability with Open Targets, model with PyMC, visualize 
networks, and search GEO for similar patterns.
```

**使用的技能**：database-lookup、torch-geometric、arboreto、pymc、networkx、scientific-visualization

> 📖 **想要更多示例？** 查看 [docs/examples.md](docs/examples.md)，获取涵盖所有科学领域的综合工作流示例和详细用例。

---

## 🔬 用例

### 🧪 药物发现与药物化学
- **虚拟筛选**：从 PubChem/ZINC 中筛选数百万个化合物，针对蛋白质靶点进行比对
- **先导化合物优化**：使用 RDKit 分析结构-活性关系，使用 datamol 生成类似物
- **ADMET 预测**：使用 DeepChem 预测吸收、分布、代谢、排泄和毒性
- **分子对接**：使用 DiffDock 预测结合姿势，并使用面向结合亲和力的工具对姿势重新打分
- **生物活性挖掘**：查询 ChEMBL 获取已知抑制剂并分析 SAR 模式

### 🧬 生物信息学与基因组学
- **序列分析**：使用 BioPython 和 pysam 处理 DNA/RNA/蛋白质序列
- **单细胞分析**：使用 Scanpy 分析 10X Genomics 数据、识别细胞类型，使用 Arboreto 推断 GRN
- **变异注释**：使用 Ensembl VEP 注释研究用 VCF 文件，检索 ClinVar 证据以供合格人员解读
- **变异数据库管理**：使用 TileDB-VCF 构建可扩展的 VCF 数据库，支持增量样本添加、高效的群体规模查询，以及基因组变异数据的压缩存储
- **群体基因组学**：使用 OneKGPd 查询 3,202 人规模 GRCh38 1000 Genomes 队列中的变异、队列样本 ID 和亲缘关系
- **调控序列模型**：运行 Genomic Intelligence 的托管启动子、剪接、增强子、染色质、表达和基因注释预测，供研究使用——而非临床或诊断决策
- **变异效应预测**：查询 AlphaGenome Atlas，获取任意 GRCh38 SNV 的 AVI 分数、Phred 排名、特征归因以及各组织的 track 效应，或使用 AlphaGenome 模型对变异打分并运行计算突变分析——用于研究优先级排序，而非诊断
- **病原体监测**：通过 GenSpectrum LAPIS API 追踪当前正在流行的病毒谱系及其增长速度（SARS-CoV-2、流感包括 H5N1、RSV、mpox、麻疹、登革热），报告滞后以实测而非假定方式给出
- **基因发现**：查询 NCBI Gene、UniProt 和 Ensembl 获取全面的基因信息
- **网络分析**：通过 STRING 识别蛋白质-蛋白质相互作用，并映射到通路（KEGG、Reactome）

### 🏥 临床研究与证据工作流
- **临床试验**：分析汇总的试验格局和方案标准，而不决定具体受试者的入选资格
- **变异证据审查**：使用 ClinVar、COSMIC 和 ClinPGx 注释经授权的研究数据；解读责任仍由具备资质的专业人员承担
- **药物安全研究**：查询 FDA 数据库，获取汇总的不良事件、相互作用和召回证据
- **临床药理学**：从浓度-时间数据推导暴露量指标，拟合房室模型和群体 PK 模型，将暴露量与药效关联，并评估给药方案、生物等效性和首次人体给药剂量
- **全文证据检索**：使用 Paperclip 端到端搜索和阅读论文、监管申报文件和试验记录，引用直接定位到具体行号，而非仅摘要
- **决策支持评估**：准备合成或汇总型评估、证据概况、隐私和治理相关文件——而非实时临床决策
- **临床医生撰写的文档**：构建有源证据支撑的报告草稿结构，并格式化由具备资质的授权专业人员已经做出的治疗决策

### 🔬 多组学与系统生物学
- **多组学整合**：结合 RNA-seq、蛋白质组学和代谢组学数据
- **通路分析**：在 KEGG/Reactome 通路中富集差异表达基因
- **网络生物学**：重建基因调控网络，识别枢纽基因
- **生物标志物发现**：整合多组学层数据以预测患者结局

### 📊 数据分析与可视化
- **统计分析**：执行假设检验、功效分析和实验设计
- **出版级图形**：使用 matplotlib 和 seaborn 创建出版质量的可视化图形
- **网络可视化**：使用 NetworkX 可视化生物网络
- **报告生成**：使用 Scientific Writing 和文档工具生成证据可追溯的研究报告；Clinical Reports 的输出始终是明显标记的草稿，仅基于经过验证的合成、去标识化或汇总型源证据构建

### 🧪 实验室自动化
- **协议设计**：在训练合格的操作员审查之前，编写并模拟 Opentrons 或 PyLabRobot 协议
- **LIMS/ELN 集成**：在明确授权远程写入的前提下，准备限定范围的 Benchling 和 LabArchives 操作
- **工作流自动化**：离线验证和模拟多步骤实验室工作流；物理执行仍受限于特定设备的操作员安全门槛
- **定制实验室硬件制造**：对 STEP 文件进行预检，然后在 Fictiv 上获取 CNC 加工或 3D 打印零件的报价，附带 DFM 反馈和交货周期选项；在未明确确认具体总价之前，不会下单

---

## 📚 可用技能

本仓库包含跨多个领域组织的 **177 个科学和研究技能**。每个技能都为使用科学库、数据库和工具提供了全面的文档、代码示例和最佳实践。

### 技能分类

> **注意：** 下面列出的 Python 包和集成技能是*明确定义*的技能——经过精心策划，配有文档、示例和最佳实践，以获得更强、更可靠的性能。它们并不是上限：代理可以安装并使用*任何* Python 包或调用*任何* API，即使没有专用技能。列出的这些技能只是让常见工作流更快、更可靠。

分类之间存在重叠：一个技能可能出现在多个领域中，因此各分类的技能数量之和并不等于 177 个唯一技能。

下面的软件包版本标明了各技能所记录的基线版本。各技能完整的依赖栈、运行时要求和验证范围，请参阅对应链接的 `SKILL.md`。

#### 🧬 **生物信息学与基因组学**（32 个技能）
- RNA-seq 预处理：[Bulk RNA-seq](skills/bulk-rnaseq/SKILL.md)（FASTQ 和定量工作流、样本/参考基因组质控，以及为交接给 PyDESeq2 准备经过验证的基因级计数）
- 序列分析：BioPython、pysam、scikit-bio、BioServices
- PCR 检测设计：[Primer Design](skills/primer-design/SKILL.md)（Primer3 候选引物、热力学、变异位点屏蔽、引物尾、以及受限的本地或 BLAST 辅助特异性筛选）
- 单细胞分析：Scanpy、AnnData、scvi-tools、scVelo（RNA 速度）、Arboreto、Cellxgene Census
- 基因组学工具：gget、当前版本的 geniml/Gtars 区间工作流、deepTools、Polars-Bio、Zarr、TileDB-VCF
- 流式细胞术：FlowIO（FCS 输入/输出）、[FlowKit](skills/flowkit/SKILL.md)（补偿、变换、层级门控以及 FlowJo 工作区分析）
- 坐标规范化：Genomic Coordinates（在 BED/GFF/GTF/VCF/SAM/WIG 等约定之间转换区间，规范化变异表示，并在 0-based 与 1-based 坐标、基因组组装/contig 命名不一致破坏分析之前将其捕获）
- 群体与序列智能：OneKGPd（个体级别的 1000 Genomes 队列查询）和 Genomic Intelligence（托管的调控/基因表达预测；仅限研究用途）
- 变异效应预测：AlphaGenome（DeepMind 的 AlphaGenome Atlas，预先计算了每个 GRCh38 SNV 的效应——AVI 分数附带 Phred 排名和 18 个 SHAP 特征归因，以及跨 9,440 个 RNA-seq、DNase、ATAC、ChIP、CAGE、剪接和接触图谱 track 的原始分数与分位数分数——还支持按需模型打分、计算突变分析以及人类和小鼠的 REF 与 ALT track 预测；仅限研究用途，非临床用途）
- 差异表达：PyDESeq2
- 合并 CRISPR 筛选：[MAGeCK](skills/mageck/SKILL.md)（向导 RNA 计数、重复样本质控、明确的对比设置以及基因打分排序）
- 扩增子微生物组：[QIIME 2 Amplicon](skills/qiime2-amplicon/SKILL.md)（双端 16S 导入、引物修剪、去噪、分类学注释以及读取保留率检查）
- 功能富集分析：Pathway Enrichment（通过 gseapy + g:Profiler 实现 ORA、GSEA/预排序、ssGSEA；涵盖 GO、KEGG、Reactome、WikiPathways、MSigDB）
- 系统发育学：ETE Toolkit、Phylogenetics（MAFFT、IQ-TREE 2、FastTree）
- 微生物组基础模型：Waypoint（Outpost Bio 开放的 Waypoint-6m/45m/170m 检查点、含 539k 样本的 Atlas MGnify 预训练语料库，以及八项任务的 Compass 基准——在分类学丰度谱上进行嵌入、微调、基准评测和预训练，并支持 MetaPhlAn/Kraken2/QIIME 2 格式转换）

#### 🧪 **化学信息学与药物发现**（11 个技能）
- 分子操作：RDKit、Datamol、Molfeat
- NMR 处理：[nmrglue](skills/nmrglue/SKILL.md)（经校准的一维 FID、相位/基线校正、候选峰以及带符号积分）
- 深度学习：DeepChem、TorchDrug
- 对接与筛选：DiffDock
- 分子动力学：OpenMM + MDAnalysis（MD 仿真与轨迹分析）
- 云端量子化学：Rowan（pKa、对接、共折叠）
- 药物相似性：MedChem
- 基准测试：基于已验证 CPython 3.11 兼容栈的 PyTDC 1.1.15

#### 🔬 **蛋白质组学与质谱**（2 个技能）
- 光谱处理：matchms、pyOpenMS

#### 🏥 **临床研究与证据工作流**（8 个技能）
- 临床数据库：通过 Database Lookup（ClinicalTrials.gov、ClinVar、ClinPGx、COSMIC、FDA、cBioPortal、Monarch 等）
- 临床药理学：PK/PD Modeling（非房室分析、房室模型和群体 PK、暴露-反应与 Emax、TMDD、PBPK 定位、生物等效性包括 RSABE/ABEL、异速生长缩放和首次人体给药剂量、依据 ICH M12 的 DDI 预测、浓度-QTc，以及贝叶斯治疗药物监测——仅依赖标准库 + numpy/scipy，不调用任何专有估算软件）
- 癌症基因组学：DepMap（癌症依赖性评分、药物敏感性）
- 癌症影像：Imaging Data Commons（通过 idc-index 访问的 NCI 放射学与病理学数据集）
- 医疗 AI 研究：PyHealth
- 决策支持研究：仅限本地、汇总或合成的 Clinical Decision Support 评估与治理相关文件
- 临床文档：使用 Clinical Reports 生成有源证据支撑的草稿，使用 Treatment Plans 格式化经过验证的、由临床医生撰写的决策；这两个技能均不进行诊断或提供治疗建议

#### 🐭 **临床前研究与动物福利**（1 个技能）
- 严重程度评估：RELSA Severity Assessment（基于体重、体温、临床/筑窝评分、生物标志物、活动量、心率、掘穴和轮跑数据计算多变量 RELSA 分数；带 95% 预测区间的 ARIMA 人道终点预测；基于 KDE 的关注区与危险区，用于 3R/优化分析及 EU 指令 2010/63/EU 的严重程度报告）——是严重程度评估的辅助工具，绝非决策规则

#### 🖼️ **显微成像、医学影像与数字病理**（5 个技能）
- DICOM 处理：pydicom 3.0.2，具备注重隐私的本地预检功能，不作任何诊断或去标识化合规方面的声明
- 全切片成像：histolab 以及仅限研究用途的 [PathML 3.0.8](skills/pathml/SKILL.md)
- 定量显微成像：[CellProfiler](skills/cellprofiler/SKILL.md)（可复用的细胞核测量流水线、通道清单、分割叠加图以及测量检查）
- 虚拟空间转录组学：非商业用途的 DeepSpot-M，用于从 224x224 H&E 图像块生成全转录组空间基因表达

#### 🧠 **神经科学与电生理学**（4 个技能）
- 数据标准：BIDS（面向神经科学和生物医学数据集的脑成像数据结构；与用于检索数据的 DataLad 配合使用——OpenNeuro（github.com/OpenNeuroDatasets）和 DANDI（github.com/dandisets）都以 DataLad 数据集的形式发布其资源——并在有记录溯源的前提下运行 BIDS-App，BEP028 是衍生数据溯源记录的扩展提案）
- 神经记录：Neuropixels-Analysis（细胞外尖峰信号、硅探针、尖峰分类）
- 数据转换：[NWB Conversion](skills/nwb-conversion/SKILL.md)（双光子 TIFF 和行为位置数据、时钟对齐、往返保真转换，以及 NWB 验证）
- 生理信号：NeuroKit2 0.2.13，用于可重复的研究工作流——不用于诊断、监测决策或医疗器械验证

#### 🤖 **机器学习与 AI**（14 个核心技能）
- 深度学习：PyTorch Lightning、Transformers、Stable Baselines3，以及 [PufferLib](skills/pufferlib/SKILL.md) 针对原生 5.0、已发布的 3.0.0 和固定的历史版本 4.0 的工作流
- 经典机器学习：scikit-learn、scikit-survival 0.28 和 SHAP
- 时间序列：aeon、TimesFM（Google 面向单变量预测的零样本基础模型）
- 贝叶斯方法：PyMC
- 优化：PyMOO
- 图机器学习：Torch Geometric
- 降维：UMAP-learn
- 统计建模：statsmodels

#### 🔮 **材料科学、化学与物理学**（8 个技能）
- 材料：当前拆分后的 pymatgen 包装层/核心，以及明确限定范围的 Materials Project 查询
- 合金热力学：[pycalphad](skills/pycalphad/SKILL.md)（基于 TDB 的相平衡、相分数、成分检查以及数据库溯源）
- 代谢建模：COBRApy
- 天文学：Astropy
- 量子计算：Cirq、PennyLane、Qiskit、[QuTiP 5.3.1](skills/qutip/SKILL.md)

#### ⚙️ **工程与仿真**（9 个技能）
- 实验室硬件 CAD：参数化的 [build123d 0.13.0 工作流](skills/lab-hardware-cad/SKILL.md)，用于微流控芯片和模具、光机械支架、微孔板和比色皿适配器以及行为实验装置，附带接口检查和多视角渲染
- 定制零件制造：Fictiv（基于浏览器驱动的 CNC 加工、3D 打印、钣金加工、聚氨酯铸造和模具成型报价，DFM 审查，交货周期和地区档位，以及结账流程，带有 CAD 预检以及下单/报价/分享前明确的审批关卡）
- 数值计算：[MATLAB 和 GNU Octave](skills/matlab/SKILL.md) 规划/审查工作流，附带 R2026b 文档、明确的 R2026a Python 集成基线，以及 GNU Octave 11.3.0
- 计算流体力学：受限范围内的 FluidSim 0.9 仿真，带数值有效性和 HPC 检查
- 实验流场测量：OpenPIV（从 PIV 图像对计算速度场、询问窗口互相关、伪矢量验证、涡度/应变率/湍流统计）
- 离散事件仿真：带重复实验、预热和输出分析指导的 SimPy 4.1.2
- 化学动力学：[Cantera](skills/cantera/SKILL.md)（均相点火延迟、机理快照、数值精修以及守恒检查）
- 电池实验：[PyBaMM](skills/pybamm/SKILL.md)（充放电协议、参数溯源、数值检查以及与实测曲线的比较）
- 符号数学：SymPy

#### 🌊 **海洋化学**（1 个技能）

- [Marine Carbonate Chemistry](skills/marine-carbonate-chemistry/SKILL.md)：使用 PyCO2SYS 处理配对的海水测量数据，涵盖碳酸盐分布计算、pH 标度处理、实验室到现场原位条件的校正、文石/方解石饱和度以及不确定度传播

#### 📊 **数据分析与可视化**（18 个技能）
- 可视化：Matplotlib、Seaborn、Scientific Visualization
- 地理空间分析：[GeoPandas 1.2.0](skills/geopandas/SKILL.md) 和 GeoMaster（遥感、GIS、卫星影像以及空间机器学习）
- 数据处理：Dask、Polars、Vaex
- 网络分析：NetworkX
- 文档处理：LiteParse（带边界框和 OCR 的本地 PDF/文档解析）和 MarkItDown
- 信息图表：Infographics（AI 驱动的专业信息图表创建）
- 图表：Markdown & Mermaid Writing（将基于文本的图表作为默认文档标准）
- 探索性数据分析：针对明确支持的格式进行受限范围的本地 EDA，未知格式则默认拒绝处理
- 统计分析：Statistical Analysis 工作流
- 单位与测量不确定度：Uncertainty & Units（pint 量纲检查、GUM 不确定度预算、A/B 类评定、覆盖因子与扩展不确定度、蒙特卡洛传播、CODATA 常数）
- 实验设计：Experimental Design（随机化、区组化、全因子/部分因子 DOE、交叉设计、整群设计、序贯设计；pyDOE3）
- 统计功效：Statistical Power（t 检验、ANOVA、比例、相关性、回归的样本量与功效计算——闭式解，以及针对 GLM、混合模型和整群设计的基于模拟的方法）

#### 🧪 **实验室自动化**（6 个技能）
- 液体处理：以离线为先的 PyLabRobot 规划/仿真，以及 Opentrons 协议编写，物理执行受限于明确的操作员安全关卡
- 云实验室：Ginkgo Cloud Lab（跨无细胞/大肠杆菌/毕赤酵母的蛋白质表达与纯化、IVT RNA 合成、热迁移和 Echo-MS 检测、SPR 入门，以及通过自主 RAC 基础设施实现的荧光像素艺术）
- 协议管理：对已记录的 v3/v4 端点进行受限范围的 protocols.io 读取，以及非执行型写入计划
- LIMS/ELN 集成：Benchling，以及独立的 LabArchives 传统 ELN 和 Inventory v1 API

#### 🔬 **多组学与系统生物学**（5 个技能）
- 通路分析：通过 Database Lookup（KEGG、Reactome、STRING）和 PrimeKG
- 数据管理：LaminDB
- 生化动力学：[Tellurium](skills/tellurium/SKILL.md)（动力学模型、时程仿真、扰动实验以及可重复的模型交换）
- 碳-13 代谢流推断：[13C Metabolic Flux](skills/13c-metabolic-flux/SKILL.md)（经验证的原子映射、稳态同位素仿真、约束拟合以及通量可辨识性分析）

#### 🧬 **蛋白质工程与设计**（5 个技能）
- 蛋白质语言模型：ESM
- 实验结构重建：[RELION](skills/relion/SKILL.md)（提取颗粒精修、光学/STAR 验证以及半图/FSC 检查）
- 糖工程：Glycoengineering（N/O-糖基化预测、治疗性抗体优化）
- 云实验室平台：Adaptyv（自动化蛋白质测试与验证）
- 云结构与设计平台：Tamarind（通过 REST API 或 MCP 提供对 AlphaFold、Boltz、Chai、ESMFold、RFdiffusion、ProteinMPNN、BoltzGen 的托管 GPU 访问，涵盖抗体/纳米抗体设计、DiffDock/Vina 对接、结合亲和力以及 MSA 生成）

#### 📚 **科学交流**（23 个技能）
- 文献：Paper Lookup（PubMed、PMC、bioRxiv、medRxiv、arXiv、OpenAlex、Crossref、Semantic Scholar、CORE、Unpaywall）、Literature Review、Paperzilla
- 全文语料库访问：Paperclip（面向约 1100 万篇全文论文、21.7 万+ 份 FDA/PMDA/EMA 监管文件、临床试验注册库以及 UniProt/PDB/ChEMBL 条目的只读虚拟文件系统——源范围限定的语义搜索、全语料库 grep、SQL 元数据查询、跨多篇论文的 map/reduce 式阅读、图表视觉分析，以及行级定位引用）
- 高级论文搜索：BGPT Paper Search（每篇论文 25+ 个结构化字段——方法、结果、样本量、质量评分——来自全文而非仅摘要）
- 网络智能：Parallel Web（网络搜索、URL/PDF 提取、深度研究、结构化信息补全、实体发现以及周期性监控）、Exa Search 和 Research Lookup
- 研究笔记本：Open Notebook（自托管的 NotebookLM 替代方案——PDF、视频、音频、网页；16+ 种 AI 提供商；多说话人播客生成）
- 写作：证据可追溯的 Scientific Writing，以及本地、保密、经授权的 Peer Review
- 文档处理：LiteParse 和 MarkItDown
- 出版与论文工作流：Venue Templates
- 演示文稿：Scientific Slides、LaTeX Posters，以及从作者批准的本地清单生成的无宏 PPTX Posters
- 图表：Scientific Schematics、Markdown & Mermaid Writing
- 信息图表：Infographics（10 种类型、8 种风格、色盲安全调色板）
- 引用：Citation Management、pyzotero
- 插图：[Generate Image](skills/generate-image/SKILL.md)（通过 OpenRouter Image API 进行生成、编辑和合成，具备模型发现、能力检查和空跑测试）

#### 🔬 **科学数据库与数据访问**（13 个技能 → 共 100+ 个数据库）
> [Database Lookup](skills/database-lookup/SKILL.md) 记录了横跨科学与金融领域的 80 个具有公开、注册或授权访问权限的数据库，包含检索契约、分页/计数核对以及端点溯源。专用技能覆盖专门的数据平台。像 BioServices、Biopython 和 gget 等多数据库包进一步增加了覆盖范围。
- 统一访问：Database Lookup（横跨化学、基因组学、临床、通路、专利、经济学等领域的 80 个数据库——PubChem、ChEMBL、UniProt、PDB、AlphaFold、KEGG、Reactome、STRING、ClinVar、COSMIC、ClinicalTrials.gov、FDA、FRED、USPTO、SEC EDGAR 等数十个数据库——具有可审计的筛选器和溯源信息）
- 癌症基因组学：DepMap（癌细胞系依赖性、药物敏感性、基因效应谱）
- 公开的生殖细胞变异证据：[Folklore Variant Evidence](skills/folklore-variant-evidence/SKILL.md)（ClinGen 基因-疾病有效性断言，以及针对一个受支持的 GRCh38 变异的带来源链接证据，具有明确的歧义处理和相关文献，供具备资质的专业人员审查）
- 癌症影像：Imaging Data Commons（通过 idc-index 访问的 NCI 放射学与病理学数据集）
- 知识图谱：PrimeKG（精准医学知识图谱——基因、药物、疾病、表型）
- 生物医学知识图谱搜索：[NCATS ARAX](skills/ncats-arax/)（在知识图谱上进行受限范围的、受 Biolink 约束的单跳查询，以及端点锁定的双跳查询，最多可明确选择五个 NCATS Translator 提供方，并保留溯源信息）
- 财政数据：U.S. Treasury Fiscal Data（国家债务、财政部报表、拍卖、汇率）
- 科学 ML 资源目录：Hugging Science（跨 17 个科学领域——天文学、生物学、化学、气候、基因组学、材料科学、医学、物理学、科学推理等——的数据集、模型、博客文章和交互式 Spaces 精选索引，包含 `datasets`、`transformers` 和 `gradio_client` 的使用模式）
- 个体级群体基因组学：OneKGPd（3,202 人高覆盖度 1000 Genomes 队列查询）
- 托管调控基因组学：Genomic Intelligence（供研究使用的启动子、剪接、增强子、染色质、表达和基因注释预测）
- 预计算变异效应：AlphaGenome（针对每个 GRCh38 SNV 的 Atlas 查询，包含 AVI、Phred、SHAP 特征归因以及各 track 分数；针对插入缺失、小鼠和自定义打分器的按需 AlphaGenome 模型打分；Atlas 网站深度链接）
- 本体术语标识：Ontology Term Resolution（将自由文本的组织、细胞类型、疾病、表型、检测方法、化学物质、物种和发育阶段标签解析为术语 ID，并对照 EBI OLS4 验证 CURIE，适用于 GEO/ENA/BioSamples/CELLxGENE/HCA/ISA-Tab 元数据）
- 实时病原体监测：Pathogen Variant Surveillance（当前正在流行的病毒谱系、其增长速度，以及携带的突变——通过 GenSpectrum LAPIS API 覆盖 SARS-CoV-2、流感包括 H5N1、RSV、mpox、麻疹、登革热等，谱系名称对照实时的 pango-designation 命名法进行解析，报告滞后以实测而非假定方式给出）

#### 🔧 **基础设施与平台**（12 个技能）
- 云计算：Modal
- 数据分发与溯源：DataLad（通过 git-annex 克隆和获取 OpenNeuro、DANDI 和 registry.datalad.org 数据集，使用 datalad run/rerun 和 containers-run 捕获可重新执行的溯源信息，并发布到 sibling 仓库）
- GPU 加速：Optimize for GPU（CuPy、Numba CUDA、Warp、cuDF、cuML、cuGraph、KvikIO、cuCIM、cuxfilter、cuVS、cuSpatial、RAFT）
- 基因组学平台：DNAnexus、LatchBio
- 工作流引擎：Nextflow（构建/运行/调试 Nextflow 和 nf-core 流水线——DSL2 模块、执行器/容器、HPC/云端扩展）以及 pacsomatic（面向 nf-core/pacsomatic 肿瘤-正常体细胞变异检测工作流的操作工具集）
- 显微成像：OMERO
- 自动化：Opentrons
- 资源检测：在请求时或在明显资源敏感的本地工作负载之前检测 Get Available Resources；经过信息脱敏且不进行压力测试
- 工作流挖掘：Autoskill（基于本地 screenpipe 的重复工作流检测和技能起草）
- 代理平台开发：[Pi Agent](skills/pi-agent/SKILL.md)（Pi 0.99.2 终端执行环境、SDK、RPC/JSONL、原生 MCP、扩展、provider/模型、软件包、TUI 组件和会话工具）

#### 🎓 **研究方法论与规划**（13 个技能）
- 构思：具备证据意识的 Scientific Brainstorming，以及不打分、始终将假设标记为候选项的 Hypothesis Generation
- 文本数据集假设软件：HypoGeniC/HypoRefine 生成候选文本模式和任务预测统计量，而非经过验证的科学假设
- 自主优化：Arbor（假设树精化——在开发评估器上迭代改进代码/模型/代理执行环境/数据产物，同时用留出测试门防止过拟合）
- 批判性分析：Scientific Critical Thinking，以及对学术著作进行定性、低风险的 Scholar Evaluation——绝不对人进行排名或支持重大决策
- 情景分析：What-If Oracle（4-6 个分支的可能性探索、应急规划、决策压力测试）
- 多视角审议：Consciousness Council（多样化的专家观点、魔鬼代言人分析）
- 认知分析：DHDNA Profiler（从任意文本中提取思维模式和认知签名）
- 资助：Research Grants
- 发现：Research Lookup、Paper Lookup（10 个学术数据库）
- 市场分析：证据可追溯的 Market Research Reports，具有明确假设驱动的规模估算和预测敏感性分析

#### ⚖️ **监管与标准**（2 个技能）
- 标准合规准备：为 ISO 13485（医疗器械质量管理体系）、ISO 14971（器械风险管理）、ISO/IEC 17025（检测和校准实验室）以及 ISO 15189（医学实验室）起草证据准备文件，各标准对应的流程域通过 `--standard` 配置项选定
- 分析方法验证：依据适用的框架——基于公开授权文本编码的 ICH Q2(R2)/Q14 和 ICH M10，以及仅按名称和范围引用的 USP `<1220>`/`<1225>`/`<1226>`、CLSI EP 系列和 ISO/IEC 17025——规划、评估并记录分析程序（HPLC、LC-MS/MS、GC、CE、ICP-MS、溶出度、qNMR、qPCR、NIR、配体结合和细胞法检测）的验证、确认和转移；仅使用标准库统计方法，不进行网络访问
- 保证路径分离：使 ISO 认证、实验室资质认定、FDA QMSR 检查、CLIA 认证、MDSAP 以及 EU MDR/IVDR 的证据边界保持清晰区分——实验室是经过资质认定而非认证，ISO 15189 资质认定并不满足 CLIA 要求
- 绝非合规、审计、评估、认证、资质认定或方法放行的决定；需要具备资质的 RA/QA、法务、实验室主任、评估员和认证机构进行审查

> 📖 **有关所有技能的完整详细信息**，请参见 [docs/skills.md](docs/skills.md)

> 💡 **寻找实用示例？** 查看 [docs/examples.md](docs/examples.md)，获取涵盖所有科学领域的综合工作流示例。

---

## 📝 来自博客

来自 [K-Dense 博客](https://www.k-dense.ai/blog) 的深度解析、基准测试和指南，与在本仓库中使用这些技能直接相关。

### 从这里开始

- **[Agent Skills：AI 驱动科学研究的最后一块拼图](https://www.k-dense.ai/blog/agent-skills-final-piece-for-ai-powered-research)** —— 什么是 Agent Skills，为什么经过策划的领域指导胜过纯粹的模型能力，以及对本仓库的介绍。
- **[K-Dense Web 对比 Scientific Agent Skills：我们为何两者都做（以及您该用哪一个）](https://www.k-dense.ai/blog/k-dense-web-vs-scientific-agent-skills)** —— 什么时候开源技能是正确的工具，什么时候带有托管计算资源的云平台更合适。
- **[AI 共同科学家问答：来自某大学研究中心一场现场交流会的 20 个问题](https://www.k-dense.ai/blog/ai-co-scientists-answered-20-questions)** —— 一个正在评估 AI 共同科学家的研究中心提出的实际问题：哪些部分保持开源和 MIT 许可、本地和桌面部署如何运作、数据如何处理，以及如何在托管平台和运行这些技能的 BYOK 配置之间做选择。
- **[如何使用 Multica 进行科学研究](https://www.k-dense.ai/blog/multica-scientific-research)** —— 一个自托管的 Multica 工作区，加上这些技能的一个精选子集：临床试验与变异分析、文献综述、每周自动巡检，以及第二模型审核，每个技能均从 `skills/<name>/` 导入。

### 技能基准测试与深度解析

- **[沉默的 97%：介绍 waypoint-bio Agent Skill](https://www.k-dense.ai/blog/introducing-waypoint-agent-skill)** —— [waypoint-bio](skills/waypoint-bio/) 针对静默数据丢失的测试：一个未转换的 MetaPhlAn 表格仍保留 3% 的丰度质量，并仍能返回有效的嵌入；配备技能的代理在配对测试中以 16 比 0 获胜。
- **[毫米级问题：介绍 lab-hardware-cad Agent Skill](https://www.k-dense.ai/blog/lab-hardware-cad-skill)** —— [lab-hardware-cad](skills/lab-hardware-cad/) 在 98 次几何打分测试中：技能组在全部 49 个案例中都生成了参数化、可重新生成的模型（基线组 49 个案例中为 0），并指出了缺失的 Y 字迷宫标准，而非凭空发明。
- **[一个技能，78 个数据库：我们为什么没有做 78 个技能](https://www.k-dense.ai/blog/database-lookup-one-skill-78-databases)** —— [database-lookup](skills/database-lookup/) 背后的设计理念：整合将常驻上下文成本降低了 13.9 倍，同时在五个模型上保持了路由准确性。
- **[AI 代理能运行你的质谱流水线吗？对 PyOpenMS 技能的基准测试](https://www.k-dense.ai/blog/benchmarking-pyopenms-skill-mass-spectrometry)** —— 对 [pyopenms](skills/pyopenms/) 的 250 次运行研究：使用该技能的任务成功率为 100%，不使用则为 96%，pyOpenMS API 错误减少 92%，成本降低 10%。
- **[超越 RDKit：将 Rowan Agent Skill 与实验数据进行对比基准测试](https://www.k-dense.ai/blog/benchmarking-rowan-skill-chemistry)** —— [rowan](skills/rowan/) 与 RDKit 和实验数据的对比：pKa 平均绝对误差 0.23（R² 0.986）、logD₇.₄ 平均绝对误差 1.15，以及约 0.52 美元计算成本下 0.19 Å 的对接姿势 RMSD 恢复精度。
- **[GPU 加速你的科学计算：单个技能带来 58 倍的平均加速](https://www.k-dense.ai/blog/optimize-for-gpu-skill)** —— [optimize-for-gpu](skills/optimize-for-gpu/) 在 12 个库中重写受 CPU 限制的 Python 代码，加速比从 1.7 倍到 492 倍不等。
- **[迈向更智能的科学搜索：Exa 加入 Scientific Agent Skills 库](https://www.k-dense.ai/blog/towards-smarter-scientific-search-exa-scientific-agent-skills)** —— [exa-search](skills/exa-search/) 带来了什么：针对学术发现调优的神经语义搜索和 URL 提取，而非关键词匹配。
- **[为科学图像生成对 Nano Banana 2 Lite 进行基准测试](https://www.k-dense.ai/blog/benchmarking-nano-banana-2-lite-scientific-image-model)** —— 对科学示意图模型的 240 张图像对比，在为 [generate-image](skills/generate-image/) 选择后端时很有参考价值：Nano Banana 2 Lite 的延迟中位数为 3.8 秒，而 GPT Image 2 为 49 秒，但存在质量上的取舍。
- **[为 NIM 微服务对 NVIDIA BioNeMo Agent Toolkit 技能进行基准测试](https://www.k-dense.ai/blog/benchmarking-nvidia-bionemo-nim-skill)** —— 一套独立于本仓库的 NVIDIA 技能集，但结论可以推广：技能在路由到不明显的端点和提升弱模型可靠性方面帮助最大，而不会提升底层科学模型本身的准确性。

### 为什么工作流层很重要

- **[模型不再是瓶颈](https://www.k-dense.ai/blog/the-model-is-no-longer-the-bottleneck)** —— 为什么像这样的仓库值得存在：前沿模型如今在原始能力上已能匹敌专业科学软件（在 NMR 氢位移预测上误差 ±0.079 ppm），因此限制因素已转移到围绕模型的工作流——数据访问、代码执行、验证和可审计的输出。
- **[AI 共同科学家已经到来。瓶颈在于验证。](https://www.k-dense.ai/blog/ai-co-scientist-verification-bottleneck)** —— 一份用于评估研究代理的 10 条检查清单，围绕暴露来源、代码、数据溯源和中间过程而非一个打磨光鲜的最终答案构建——与 [database-lookup](skills/database-lookup/) 和 [scientific-writing](skills/scientific-writing/) 等技能中溯源和检索契约要求背后的思路一致。
- **[复现而非生成，才是 AI 在科学领域的杀手级应用](https://www.k-dense.ai/blog/reproduction-not-generation-ai-for-science)** —— 为什么重新运行已发表的分析是代理最具价值的用途：在一项涵盖 221 项研究的基准测试中，78% 的论文和 93% 的单项分析任务得到了复现，因为复现结果可以与已知数字对照检验，而生成的结论则无法这样检验。
- **[介绍 K-Bench 01：九个前沿模型、178 个真实科学任务，以及大量自信的错误答案](https://www.k-dense.ai/blog/introducing-k-bench-01-internal-benchmark)** —— 九个前沿模型在 178 个真实用户任务上的测试，其中 40% 的运行存在过度宣称的情况。这为判断代理报告成功时该检查什么提供了有用的校准，也为上文临床、监管和研究方法论技能中写入的验证边界提供了背景。

### 安全与安全部署

- **[科学代理时代的安全：每个实验室在安装技能之前都应了解的事](https://www.k-dense.ai/blog/skill-security-before-you-install)** —— 本仓库[安全免责声明](#%EF%B8%8F-security-disclaimer)背后的实际审查清单：安装前阅读完整的 `SKILL.md` 和 `scripts/`，先扫描再安装，并固定版本而非跟踪某个分支。
- **[沙箱化的 AI 科学家：将 NVIDIA OpenShell 与 Scientific Agent Skills 配对](https://www.k-dense.ai/blog/sandboxed-ai-scientist-openshell-skills)** —— 在受策略治理的沙箱中运行这些技能；另见[入门指南](#-getting-started)中的 NemoClaw 说明。

### 互补的开源项目

- **[介绍 Science Superpowers：为你的研究代理赋予科学纪律](https://www.k-dense.ai/blog/introducing-science-superpowers)** —— 假设预注册、可重复工作流，以及"先验证后宣称"，这些机制环绕在这些技能周围，用以防范 p-hacking 和 HARKing。
- **[你的 AI 助手像通才一样推理。科学需要专家。](https://www.k-dense.ai/blog/introducing-scientific-agents)** —— 503 个开源的 `AGENTS.md` 档案，为这些技能中的"做什么"流程补上了"如何思考"的那一层。
- **[介绍 mimeo 以及 80+ 个 Mimeograph](https://www.k-dense.ai/blog/introducing-mimeo-and-mimeographs)** —— 通过提炼某位实践者的推理方式，生成你自己的 `SKILL.md` / `AGENTS.md` 专家档案。
- **[Agentic Data Scientist：一个真正能完成分析的开源 AI](https://www.k-dense.ai/blog/agentic-data-scientist-open-source)** —— 一个多代理的规划、执行与验证框架，加载这些技能以完成端到端的数据科学工作流。
- **[Karpathy：一个开源的代理式机器学习工程师](https://www.k-dense.ai/blog/karpathy-agentic-ml-engineer)** —— 一个自主的 ML 训练代理，构建用于消费 Scientific Agent Skills，覆盖从预处理到超参数搜索的全过程。

---

## 🤝 贡献

我们欢迎为扩展和改进这个科学技能仓库所做的贡献！

在创建或更改技能之前，请先阅读 [AGENTS.md](AGENTS.md)；详细的工作流程和拉取请求流程请参见 [CONTRIBUTING.md](CONTRIBUTING.md)。贡献应聚焦于某个科学软件包、数据库、平台或研究工作流；宽泛的编码、基础设施和路由类技能超出了本仓库的范围。

### 贡献方式

✨ **添加新技能**
- 为额外的科学软件包或数据库创建技能
- 为科学平台和工具添加集成

📚 **改进现有技能**
- 通过更多示例和用例增强文档
- 添加新的工作流和参考材料
- 改进代码示例和脚本
- 修复错误或更新过时的信息

🐛 **报告问题**
- 提交带有详细复现步骤的错误报告
- 建议改进或新功能

### 如何贡献

1. **Fork** 本仓库
2. **创建**一个功能分支（`git checkout -b feature/amazing-skill`）
3. **遵循** [CONTRIBUTING.md](CONTRIBUTING.md) 和现有的目录结构
4. **确保**所有新技能都包含带有必要前置数据和 `metadata.version` 的有效 `SKILL.md` 文件
5. **充分测试**您的示例和工作流，如果您的技能附带 `scripts/`，还需在 `tests/<skill-name>/` 下添加测试套件
6. **提交**您的更改（`git commit -m 'Add amazing skill'`）
7. **推送**到您的分支（`git push origin feature/amazing-skill`）
8. **提交**带有清晰更改说明的拉取请求

### 贡献指南

✅ **遵守 [Agent Skills 规范](https://agentskills.io/specification)** —— 每个技能都必须遵循官方规范（有效的 `SKILL.md` 前置数据、命名约定、目录结构）
✅ 在每个 `SKILL.md` 中包含一个带引号的 `metadata.version` 值
✅ 更新现有技能时递增 `metadata.version`
✅ 保持与现有技能文档格式的一致性
✅ 确保所有代码示例都经过测试且功能正常
✅ 在示例和工作流中遵循科学最佳实践
✅ 新增功能时更新相关文档
✅ 在代码中提供清晰的注释和文档字符串
✅ 包含对官方文档的引用

### 测试

每个附带 `scripts/` 的技能都必须在 `tests/<skill-name>/` 下有一个测试套件，并在 [`tests/skill-requirements.toml`](tests/skill-requirements.toml) 中有对应条目。`tests/_meta` 守护检查会核实这一覆盖情况以及共享的结构契约：前置数据、文档长度、本地链接、脚本语法、字节码以及硬编码的本地路径。它还会依据内置的 Agent Plugins schema 验证 `plugin.json`，并检查其版本号是否与 `pyproject.toml` 一致。CLI `--help` 和示例执行检查属于各个技能自己的测试套件。

```bash
# 安装仓库的开发与验证工具
uv sync

# 结构契约与覆盖率守护检查 —— 仅需数秒，无需任何科学软件包
uv run python -m pytest tests/_meta -q

# 验证某个技能的 Agent Skills 前置数据
uv run skills-ref validate skills/<skill-name>

# 在当前环境中运行某个技能的测试套件
uv run --with pytest python -m pytest tests/<skill-name> -q

# 使用某个技能声明的软件包和 Python 版本运行该技能
uv run python tests/run_all.py --isolated <skill-name>

# 运行全部测试套件，每个都在独立的临时环境中
uv run python tests/run_all.py --isolated
```

每个 pytest 进程只运行一个技能：不同技能会复用诸如 `_common` 这样的模块名，因此一起收集多个套件可能会导入错误的模块。`tests/run_all.py` 负责进程隔离；`--isolated` 还会为每个技能提供其声明的依赖环境。在当前环境中运行某个套件时，如果所需软件包缺失，可能会跳过相应检查。

[Skill Tests](https://github.com/K-Dense-AI/scientific-agent-skills/actions/workflows/skill-tests.yml) 工作流会针对相关的拉取请求和推送到 `main` 的提交运行契约检查和仅依赖标准库的测试套件，也可以手动触发。完整的科学依赖项扫描并不在 CI 中运行；请在发布前或更改共享契约时运行它。部分技能需要外部运行时或系统工具；安装缺口记录在 [`tests/skill-requirements.toml`](tests/skill-requirements.toml) 中。

### 安全扫描

本仓库中的所有技能都使用 [Cisco AI Defense Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) 进行安全扫描，这是一个开源工具，用于检测 Agent Skills 中的提示注入、数据渗漏和恶意代码模式。

如果您正在贡献新技能，建议在提交拉取请求之前先在本地运行扫描器：

```bash
uv pip install cisco-ai-skill-scanner
skill-scanner scan /path/to/your/skill --use-behavioral
```

> **注意：** 干净的扫描结果能减少审查中的噪音，但不能保证技能没有任何风险。贡献的技能在合并之前还会经过人工审查。

### 认可

贡献者将在我们的社区中得到认可，并可能在以下地方被重点介绍：
- 仓库贡献者列表
- 发布说明中的特别提及
- K-Dense 社区精选

您的贡献让科学计算更易获取，也让研究人员能够更有效地利用 AI 工具！

### 支持开源

本项目建立在 50+ 个了不起的开源项目之上。如果您在这些技能中发现了价值，请考虑[支持我们所依赖的项目](docs/open-source-sponsors.md)。

---

## 🔧 故障排除

### 常见问题

**问题：技能未加载**
- 确认技能文件夹位于正确的目录中（参见[入门指南](#-getting-started)）
- 每个技能文件夹必须包含一个 `SKILL.md` 文件
- 复制技能后重启您的代理/IDE
- 在 Cursor 中，检查 Settings → Rules，确认技能已被发现

**问题：缺少 Python 依赖项**
- 解决方案：检查具体的 `SKILL.md` 文件，了解所需的软件包
- 安装依赖项：`uv pip install package-name`

**问题：API 速率限制**
- 解决方案：许多数据库都有速率限制。请查阅具体数据库的文档
- 考虑实现缓存或批量请求

**问题：身份验证错误**
- 解决方案：部分服务需要 API 密钥。请查看 `SKILL.md` 中的身份验证设置
- 验证您的凭据和权限

**问题：示例已过时**
- 解决方案：通过 GitHub Issues 报告问题
- 查阅官方软件包文档以获取更新的语法

**问题：`gh skill install` 或文档中指向 `scientific-skills/` 的链接失效（v2.43.0+）**
- 从 v2.43.0 起，技能位于 `skills/` 下（而非 `scientific-skills/`），以匹配 GitHub CLI 所期望的 Agent Skills 布局
- 请将手动复制路径、书签和引用中的 `scientific-skills/<name>` 更新为 `skills/<name>`
- 拉取最新版本后，重新运行 `gh skill install K-Dense-AI/scientific-agent-skills`

---

## ❓ 常见问题

### 一般问题

**问：这个免费使用吗？**
答：是的！本仓库采用 MIT 许可证。但是，每个单独的技能都在其 `SKILL.md` 文件的 `license` 元数据字段中指定了自己的许可证——请务必查看并遵守这些条款。

**问：为什么所有技能都打包在一起，而不是作为独立的软件包？**
答：我们相信，在 AI 时代，好的科学研究本质上是跨学科的。将所有技能打包在一起，使您（以及您的代理）可以轻松地跨领域连接——例如在一个工作流中结合基因组学、化学信息学、临床数据和机器学习——而不必担心该安装或连接哪些单独的技能。

**问：我可以将其用于商业项目吗？**
答：本仓库本身采用 MIT 许可证，允许商业使用。但是，单独的技能可能有不同的许可证——请查看每个技能 `SKILL.md` 文件中的 `license` 字段，以确保符合您的预期用途。

**问：所有技能都使用相同的许可证吗？**
答：不是。每个技能都在其 `SKILL.md` 文件的 `license` 元数据字段中指定了自己的许可证。这些许可证可能与本仓库的 MIT 许可证不同。用户有责任查看并遵守他们所使用的每个单独技能的许可证条款。

**问：这个仓库多久更新一次？**
答：我们会定期更新技能，以反映软件包和 API 的最新版本。重大更新会在发布说明中公布。

**问：我可以将其与其他 AI 模型一起使用吗？**
答：这些技能遵循开放的 [Agent Skills](https://agentskills.io/) 标准，可以与任何兼容的代理一起使用，包括 Cursor、Claude Code、Codex 和 Google Antigravity。

### 安装与设置

**问：我需要安装所有 Python 软件包吗？**
答：不需要。只需按照每个 `SKILL.md` 的说明，安装您所使用的工作流所需的依赖项。如果某些工作流的软件包或 Python 版本要求不兼容，请将它们放在不同的环境中。

**问：如果某个技能不起作用怎么办？**
答：首先查看[故障排除](#-troubleshooting)部分。如果问题仍然存在，请在 GitHub 上提交 issue，并附上详细的复现步骤。

**问：这些技能可以离线使用吗？**
答：一旦本地分析所需的依赖项、参考数据和模型文件都已就位，本地分析就可以离线工作。数据库查询、托管模型和云平台需要网络访问；请检查具体技能的要求。

### 贡献

**问：我可以贡献自己的技能吗？**
答：当然可以！我们欢迎贡献。请参阅[贡献](#-contributing)部分获取指南和最佳实践。

**问：如何报告错误或建议新功能？**
答：在 GitHub 上提交一个 issue，并附上清晰的描述。对于错误，请包含复现步骤以及预期行为与实际行为的对比。

---

## 💬 支持

需要帮助？以下是获取支持的方式：

- 📖 **文档**：查看相关的 `SKILL.md` 和 `references/` 文件夹
- 🐛 **错误报告**：[提交 issue](https://github.com/K-Dense-AI/scientific-agent-skills/issues)
- 💡 **功能请求**：[提交功能请求](https://github.com/K-Dense-AI/scientific-agent-skills/issues/new)
- 📣 **更新与演示**：关注 [X](https://x.com/k_dense_ai)、[LinkedIn](https://www.linkedin.com/company/k-dense-inc)、[YouTube](https://www.youtube.com/@K-Dense-Inc) 和 [Reddit](https://www.reddit.com/user/-k-dense-/)，随时了解新技能、教程和 Scientific Agent Skills 的发布动态
- 💼 **企业支持**：联系 [K-Dense](https://k-dense.ai/) 获取商业支持

---

## 📖 引用

如果您在研究或项目中使用了 Scientific Agent Skills，请引用我们的论文：

> Timothy Kassis, Vinayak Agarwal, Yuhuan He, Darshil Patel, and Aubrey M. Brueckner. **Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents.** arXiv:2609.00065, 2026. [https://arxiv.org/abs/2609.00065](https://arxiv.org/abs/2609.00065)

在相关的情况下，也请引用对您的工作有实质性帮助的具体技能。

GitHub 的 **Cite this repository** 按钮由 [`CITATION.cff`](CITATION.cff) 支持，可生成 APA 或 BibTeX 格式的相同论文引用。

论文引用有助于他人找到本仓库，理解您工作流中所使用的更广泛的技能生态系统，并认可 Scientific Agent Skills 背后的维护工作。单个技能的引用则能为您的代理所使用的具体软件包、数据库或工作流指导提供更精确的归属。

推荐做法：
- 始终使用下方格式之一引用 **Scientific Agent Skills 论文**。
- 同时引用每个直接贡献于您的分析、代码、图表、报告或研究工作流的具体技能。
- 如果某个技能是对外部软件包、数据库或平台的封装或文档化，并且您所在领域的规范要求，也请引用该上游项目。

### 论文引用

#### BibTeX
```bibtex
@misc{kassis2026scientificagentskills,
  title         = {Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents},
  author        = {Kassis, Timothy and Agarwal, Vinayak and He, Yuhuan and Patel, Darshil and Brueckner, Aubrey M.},
  year          = {2026},
  eprint        = {2609.00065},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CL},
  url           = {https://arxiv.org/abs/2609.00065}
}
```

#### APA
```
Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent Skills: A library of procedural knowledge for research agents. arXiv. https://arxiv.org/abs/2609.00065
```

#### MLA
```
Kassis, Timothy, et al. "Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents." arXiv, 2026, arxiv.org/abs/2609.00065.
```

#### 纯文本
```
Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065. https://arxiv.org/abs/2609.00065
```

### 软件引用

如果您还需要引用本仓库本身的某个特定版本（例如，为了固定某次分析所依据的确切技能集），请在论文引用的同时附加一个软件引用，并记录您所使用的发布标签或提交版本：

```bibtex
@software{scientific_agent_skills_2026,
  author = {{K-Dense Inc.}},
  title = {Scientific Agent Skills: A Comprehensive Collection of Scientific Tools for AI Agents},
  year = {2026},
  url = {https://github.com/K-Dense-AI/scientific-agent-skills},
  note = {177 skills covering databases, packages, integrations, and analysis tools}
}
```

### 单个技能引用

引用某个具体技能时，请包含技能名称、该技能 `SKILL.md` 中 `metadata.version` 给出的版本号，以及该技能的直接链接。例如：

```bibtex
@software{scientific_agent_skills_astropy_2026,
  author = {{K-Dense Inc.}},
  title = {Astropy Skill for Scientific Agent Skills},
  year = {2026},
  url = {https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/astropy},
  note = {Version 1.5, part of Scientific Agent Skills}
}
```

纯文本格式：

```text
Astropy skill for Scientific Agent Skills, version 1.5.
K-Dense Inc. (2026).
https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/astropy
```

我们感谢在受益于这些技能的出版物、演示文稿或项目中给予的致谢。

---

## 📄 许可证

本项目采用 **MIT 许可证**。

**版权 © 2026 K-Dense Inc.**（[k-dense.ai](https://k-dense.ai/)）

### 要点：
- ✅ **可免费用于任何用途**（商业和非商业）
- ✅ **开源** —— 可自由修改、分发和使用
- ✅ **宽松** —— 对重用的限制极少
- ⚠️ **不提供担保** —— 按"原样"提供，不附带任何形式的担保

完整条款请参见 [LICENSE.md](LICENSE.md)。

### 单个技能的许可证

> ⚠️ **重要**：每个技能都在其 `SKILL.md` 文件的 `license` 元数据字段中指定了自己的许可证。这些许可证可能与本仓库的 MIT 许可证不同，并可能包含附加条款或限制。**用户有责任查看并遵守他们所使用的每个单独技能的许可证条款。**
