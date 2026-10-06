---
name: bids
description: >
  组织、查询、验证和转换脑成像数据结构（Brain Imaging Data Structure, BIDS）数据集。支持
  组织神经科学和生物医学数据（MRI、EEG、MEG、iEEG、PET、显微成像、
  NIRS、动作捕捉、EMG、磁共振谱、行为数据），查询BIDS布局，
  验证合规性，将DICOM转换为BIDS，编写元数据sidecar文件，或
  创建BIDS衍生数据（derivatives）。
license: https://creativecommons.org/licenses/by/4.0/
compatibility: Requires Python 3.10+ for PyBIDS and the validator wrapper; dcm2niix for DICOM conversion. Network access for installation and schema updates; no API credentials required.
metadata:
  version: "1.3"
  last-reviewed: "2026-09-30"
  skill-author: Yaroslav Halchenko
---

# 脑成像数据结构（BIDS）

## 概述

脑成像数据结构（BIDS）是一个用于组织和描述神经科学与生物医学研究数据集的社区标准。它定义了一致的文件命名约定、目录层级和元数据schema，使数据集能够立即被人类和软件工具同时理解。BIDS由BIDS规范（已对照v1.11.2版本进行审查，发布于2026-09-29）治理，并由社区通过BIDS-Standard GitHub组织维护。

尽管BIDS起源于MRI，但它的发展已远远超出了神经影像学的范畴。该规范现在涵盖11种模态，横跨影像、电生理学和行为数据：

- **影像**：MRI（结构、功能、弥散、场图、灌注/ASL）、PET、显微成像
- **电生理学**：EEG、MEG、iEEG（颅内EEG）、EMG
- **其他**：NIRS（近红外光谱）、动作捕捉、行为数据（无影像）、磁共振谱

活跃中的BEP正在进一步扩展BIDS——尤其是BEP032（微电极电生理学）提议支持包括Neuropixels探针的细胞外记录，将BIDS引入动物神经科学研究中一种普遍采用的方法（另见neuropixels-analysis技能）。

仓库的提交要求因模态和存档库而异；准备提交之前请检查目标存档库的要求。

BIDS的Python生态系统以用于查询和索引BIDS数据集的**PyBIDS**（`pybids`）以及用于合规性检查的**bids-validator**（基于Deno，可通过PyPI包`bids-validator-deno`或直接通过Deno获得）为核心。从DICOM转换通常使用**HeuDiConv**、**dcm2bids**或**BIDScoin**完成。

## 何时使用此技能

在以下情况下应用此技能：
- 将原始神经科学数据（影像、电生理学、行为）组织成符合BIDS规范的目录结构
- 查询一个现有的BIDS数据集，按受试者、会话、任务、运行或模态查找特定文件
- 在共享或提交之前，针对BIDS规范验证一个数据集
- 将扫描仪的DICOM数据转换为BIDS格式
- 编写或编辑JSON sidecar元数据文件
- 创建符合BIDS规范的衍生数据（预处理数据、分析输出）
- 为一个新数据集设置 `dataset_description.json`
- 处理BIDS实体（受试者、会话、任务、采集、运行等）
- 配置 `.bidsignore` 以将文件排除在验证之外
- 准备数据以上传到OpenNeuro、DANDI或其他支持BIDS的存储库

## 安装

```bash
# 核心BIDS查询库
uv pip install pybids

# BIDS验证器（基于Deno，通过PyPI包装器安装）
uv pip install bids-validator-deno
# 替代方案：直接通过Deno安装
# deno install -ERWN -g -n bids-validator jsr:@bids/validator

# DICOM到BIDS转换器（按需安装）
uv pip install heudiconv       # HeuDiConv ——基于启发式规则的DICOM转换
uv pip install dcm2bids        # dcm2bids ——基于配置文件的转换
# BIDScoin: uv pip install bidscoin

# 有用的配套工具
uv pip install nibabel          # NIfTI/其他神经影像文件I/O
uv pip install pydicom          # DICOM文件读取（转换器使用）
```

## 核心工作流程

[references/core_workflows.md](references/core_workflows.md) 中记录了十二个工作流程领域，
每个都附有可运行的代码：

1. **BIDS目录结构** ——所需的布局以及每种模态所属的位置。
2. **`dataset_description.json`** ——所需的字段以及如何生成它。
3. **使用PyBIDS查询** ——`BIDSLayout`、实体筛选器、带自动继承功能的
   sidecar元数据，以及从实体构建路径。
4. **验证** ——通过PyPI包装器（推荐）使用`bids-validator`、直接通过Deno
   使用、旧版的Node验证器，以及使用`.bidsignore`排除文件。
5. **实体和文件命名** ——实体顺序和命名语法。
6. **DICOM到BIDS转换** ——HeuDiConv（包括一站式的ReproIn路径以及
   侦察→启发式规则→转换的流程）和dcm2bids（基于配置文件）。
7. **元数据sidecar文件** ——每种模态所需和推荐的JSON字段。
8. **事件文件** ——任务态fMRI的事件时序和列约定。
9. **参与者文件** ——`participants.tsv`及其数据字典。
10. **衍生数据** ——衍生数据布局及其 `dataset_description.json`。
11. **高级PyBIDS** ——索引缓存，包括衍生数据、混杂回归量和
    DataFrame输出。
12. **BIDS-Apps** ——标准调用模式，以及fMRIPrep、MRIQC和QSIPrep。

使用BIDS验证器进行验证，同时也使用PyBIDS进行索引。成功的索引
不等同于完整的合规性检查；记录验证器和BIDS schema版本，并在分析
之前检视警告和元数据继承情况。

## 参考材料

此技能包含详细的参考文档：

- **bids_schema.json**：机器可读的BIDS schema（来自https://bids-specification.readthedocs.io/en/stable/schema.json）。这是实体定义、排序规则、文件名模板、每种数据类型允许的后缀以及元数据字段要求的权威来源。特定于BEP的schema位于https://github.com/bids-standard/bids-schema/tree/main/BEPs。
- **beps.yml**：所有BIDS扩展提议的当前列表，包括标题、负责人、状态和链接（来自[bids-website](https://github.com/bids-standard/bids-website/blob/main/data/beps/beps.yml)）
- **bids_specification.md**：实体表、数据类型参考、目录结构规则、模板空间和规范更新日志的人类可读摘要
- **metadata_fields.md**：每种BIDS模态（anat、func、dwi、fmap、eeg、meg、pet等）所需和推荐的JSON sidecar字段
- **conversion_tools.md**：HeuDiConv、dcm2bids和BIDScoin的详细工作流程，包括启发式规则/配置示例以及故障排除

从该技能目录中，使用 `python scripts/update_schema.py` 更新schema和BEP。
内置的快照是BIDS 1.11.2 / schema 2.0.0；BEP提议不是已采用的要求。
如果ReadTheDocs阻止了自动抓取，请使用更新器帮助中记录的、带版本号的GitHub导出方式。

## 常见问题和解决方案

### 1. 验证器报告"Not a BIDS dataset"
**原因**：根目录缺少 `dataset_description.json`。
**修复**：创建该文件，至少包含 `{"Name": "...", "BIDSVersion": "1.11.2"}`。

### 2. 受试者不一致警告
**原因**：不是所有受试者都有相同的文件集（有些缺少会话、运行等）。
**修复**：在验证器的JSON报告中审查严重程度和确切的问题代码，并在 `participants.tsv` 或 `scans.tsv` 中记录缺失的数据。当前的schema验证器不提供旧版的 `--ignoreSubjectConsistency` 标志；只对经过审查的例外情况使用一个范围严格限定的 `--config`。

### 3. 缺少SliceTiming
**原因**：`dcm2niix` 无法从DICOM文件头中提取切片时序。
**修复**：从扫描仪元数据或经过验证的序列协议中恢复实际的切片采集偏移量。仅凭切片顺序无法确定时序，尤其是在使用多频段采集或存在死区时间的情况下。按切片索引顺序以秒为单位存储偏移量，并考虑 `SliceEncodingDirection`；记录缺失的时序，而不是编造它。

### 4. 相位编码方向混淆
**原因**：坐标轴标签（i/j/k vs x/y/z vs LR/AP/SI）令人困惑。
**修复**：在BIDS中，使用NIfTI图像坐标轴：`i`=第一轴，`j`=第二轴，`k`=第三轴。`-` 表示负方向。解剖学方向取决于NIfTI的affine矩阵和转换器的方向约定；不要仅凭一个AP/PA序列标签推断 `j` 或其符号。请对照扫描仪元数据和图像方向进行验证。

### 5. PyBIDS在大型数据集上运行缓慢
**原因**：每次调用 `BIDSLayout()` 都进行完整的文件系统索引。
**修复**：使用 `database_path` 将索引缓存到数据集之外的一个目录中：
```python
layout = BIDSLayout("/data", database_path="/cache/pybids")
# 数据集更改后，使用reset_database=True重建索引。
```

### 6. PyBIDS找不到衍生数据
**原因**：衍生数据目录缺少自己的 `dataset_description.json`。
**修复**：每个衍生数据目录都必须有一个带 `"DatasetType": "derivative"` 的 `dataset_description.json`。

### 7. 事件文件时序偏差
**原因**：`onset` 时间相对于错误的参考点（例如触发时间而非第一个volume）。
**修复**：Onset是相对于对应记录中第一个存储的数据点的秒数。如果在存储之前丢弃了伪影volume，请将时间零点重置为第一个保留的volume；允许负的onset值。

### 8. TSV文件验证失败
**原因**：编码或分隔符问题（空格代替制表符，BOM字符）。
**修复**：确保使用UTF-8编码和Unix行结束符（`\n`）的制表符分隔值。缺失值使用 `n/a`（不是 `NA`、`NaN`或空值）。

## 最佳实践

1. **尽早且频繁地验证** ——每次转换或修改后都运行BIDS验证器。在错误累积之前修复它们。

2. **使用元数据继承** ——将共享的元数据（例如 `TaskName`、扫描仪参数）放在顶层的sidecar文件中，而不是在每个受试者的目录中重复。

3. **保留sourcedata** ——在受控存储中保留源DICOM文件和转换溯源；`sourcedata/` 被排除在原始BIDS验证之外，但并不等同于已去标识化。分享之前请审查标识符。

4. **从一开始就使用一致的命名** ——在数据收集之前定义你的BIDS命名方案。对扫描协议使用ReproIn命名约定以便实现自动转换。

5. **记录你的数据集** ——撰写一份详尽的 `README`，描述研究设计、采集参数、已知问题以及与BIDS的任何偏差。

6. **使用scans.tsv记录运行级元数据** ——记录每次运行的采集时间和质量说明：
   ```
   filename	acq_time	quality
   func/sub-01_task-rest_bold.nii.gz	2025-01-15T10:30:00	good
   ```

7. **为你的数据集设置版本** ——使用 `CHANGES` 记录数据集的修改。考虑使用DataLad对大型数据集进行完整的版本控制。

8. **对解剖图像去面部化** ——在共享T1w/T2w图像之前移除面部特征（例如使用 `pydeface`、`mri_deface`或 `afni_refacer`）。将去面部化的版本存储为主要数据，或使用 `_defacemask` 文件。

9. **使用BIDS URI进行溯源** ——在衍生数据中，对原始来源使用 `bids:raw:sub-01/anat/sub-01_T1w.nii.gz`，并在衍生数据根目录为 `raw/derivatives/pipeline/` 时定义 `"DatasetLinks": {"raw": "../.."}`。`bids::` 在当前数据集内解析，在一个衍生数据集中，这指的是该衍生数据集本身。

10. **优先使用社区工具** ——尽可能使用成熟的BIDS-Apps（fMRIPrep、MRIQC、QSIPrep），而不是自定义流程。检查所选发行版支持的输入和输出约定；软件的输出仍需要验证。

11. **研究bids-examples** ——[bids-examples](https://github.com/bids-standard/bids-examples) 仓库是涵盖不同模态和用例（MRI、fMRI、DWI、EEG、MEG、iEEG、PET、ASL、基因组学、衍生数据等）的典范BIDS数据集的权威集合。可将其用作组织自己数据集时的参考、BIDS工具的测试数据，或用来理解某种特定模态应如何组织。请固定一个示例版本以及验证器/schema版本；上游测试套件在实现演变过程中也会跟踪预期的失败情况。

## BIDS扩展提议（BEP）

BEP是由社区驱动的提议，用于将BIDS扩展到新的模态、衍生数据或元数据。包含状态、负责人和链接的完整列表位于 `references/beps.yml`（来自[bids-website](https://github.com/bids-standard/bids-website/blob/main/data/beps/beps.yml)）。特定于BEP的schema预览渲染于https://github.com/bids-standard/bids-schema/tree/main/BEPs。

内置的BEP列表已于2026-09-30更新。在使用草案实体之前，请阅读每一个条目的提议/PR和状态；BEP032仍是一个提议，不属于稳定版1.11.2的一部分。使用仓库的目录列表来发现预览schema路径；不要假设一个 `BEPs/BEP032/schema.json` URL存在。

**相关标准：**
- **BIDS-Stats模型**：用于定义基于GLM的神经影像分析的JSON规范
- **BIDS衍生数据**（BEP003）：预处理/分析输出的标准（已部分合并入规范）

## 相关工具生态系统

| 工具 | 用途 |
|------|------|
| **fMRIPrep** | fMRI预处理（生成BIDS衍生数据） |
| **MRIQC** | MRI质量控制（生成BIDS衍生数据） |
| **QSIPrep** | 弥散MRI预处理 |
| **TemplateFlow** | 带有类BIDS命名的神经影像模板和图谱 |
| **Fitlins** | BIDS Stats模型的实现 |
| **DataLad** | 用于大型数据集的版本控制，与BIDS集成 |
| **OpenNeuro** | 免费的BIDS数据集存储库 |
| **DANDI** | 神经生理学数据存档（部分模态使用BIDS） |
| **HeuDiConv** | 使用启发式Python文件的DICOM转BIDS工具 |
| **dcm2bids** | 使用JSON配置的DICOM转BIDS工具 |
| **BIDScoin** | 带有GUI和YAML配置的DICOM转BIDS工具 |
| **nwb2bids** | 将NWB（Neurodata Without Borders）文件转换为BIDS |
| **CuBIDS** | BIDS数据集整理和协调 |
| **bids2table** | BIDS数据集的高效表格化索引 |
| **bids-examples** | 涵盖所有模态的典范BIDS数据集集合 |

## 文档

- **BIDS规范**：https://bids-specification.readthedocs.io/
- **BIDS网站**：https://bids.neuroimaging.io/
- **PyBIDS文档**：https://bids-standard.github.io/pybids/
- **BIDS验证器**：https://github.com/bids-standard/bids-validator
- **BIDS入门套件**：https://bids-standard.github.io/bids-starter-kit/
- **BIDS示例**：https://github.com/bids-standard/bids-examples ——每种BIDS模态的典范参考数据集；用作模板和测试数据
- **HeuDiConv文档**：https://heudiconv.readthedocs.io/
- **原始BIDS论文**：Gorgolewski et al. (2016) Scientific Data, doi:10.1038/sdata.2016.44
