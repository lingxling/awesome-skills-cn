---
name: bids
description: >
license: https://creativecommons.org/licenses/by/4.0/
metadata: {"version": "1.0", "skill-author": "Yaroslav Halchenko"}
---






# 脑成像数据结构 (BIDS)

## 概述

脑成像数据结构 (BIDS) 是组织和描述神经科学及生物医学研究数据集的社区标准。它定义了一致的文件命名约定、目录层次结构和元数据模式，使数据集对人和软件工具都能立即理解。BIDS 由 BIDS 规范（当前 v1.x）管理，并通过 BIDS-Standard GitHub 组织由社区维护。

虽然 BIDS 起源于 MRI，但现在已经远远超出神经影像学。规范涵盖了跨越成像、电生理和行为数据的 11 种模态：

- **成像**：MRI（结构、功能、扩散、场图、灌注/ASL）、PET、显微镜
- **电生理**：EEG、MEG、iEEG（颅内 EEG）、EMG
- **其他**：NIRS（近红外光谱）、运动捕捉、行为数据（无成像）、磁共振波谱

活跃的 BEP 正在进一步扩展 BIDS — 特别是 BEP032（微电极电生理学）将添加对细胞外记录的支持，包括 Neuropixels 探针，将 BIDS 带入动物神经科学研究中的流行方法论（另见 neuropixels-analysis 技能）。

主要数据存储库（OpenNeuro、DANDI）、领先期刊（NeuroImage、Human Brain Mapping、Scientific Data）和资助机构（NIH、ERC）要求或强烈鼓励采用 BIDS。

BIDS 的 Python 生态系统以 **PyBIDS** (`pybids`) 为中心，用于查询和索引 BIDS 数据集，以及 **bids-validator**（基于 Deno，可通过 PyPI 包 `bids-validator-deno` 或直接通过 Deno 使用）进行合规性检查。DICOM 到 BIDS 的转换通常使用 **HeuDiConv**、**dcm2bids** 或 **BIDScoin** 完成。

## 何时使用此技能

在以下情况下应用此技能：
- 将原始神经科学数据（成像、电生理、行为）组织成符合 BIDS 的目录结构
- 查询现有 BIDS 数据集以按受试者、会话、任务、运行或模态查找特定文件
- 在共享或提交之前验证数据集是否符合 BIDS 规范
- 将扫描仪的 DICOM 数据转换为 BIDS 格式
- 编写或编辑 JSON 侧边栏元数据文件
- 创建符合 BIDS 的衍生数据（预处理数据、分析输出）
- 为新数据集设置 `dataset_description.json`
- 使用 BIDS 实体（subject、session、task、acquisition、run 等）
- 配置 `.bidsignore` 从验证中排除文件
- 准备上传到 OpenNeuro、DANDI 或其他支持 BIDS 的存储库

## 安装

```bash
# 核心 BIDS 查询库
uv pip install pybids

# BIDS 验证器（基于 Deno，通过 PyPI 包装器安装）
uv pip install bids-validator-deno
# 备选：通过 Deno 直接安装
# deno install -g -A npm:bids-validator

# DICOM 到 BIDS 转换器（按需安装）
uv pip install heudiconv       # HeuDiConv - 基于启发式的 DICOM 转换
uv pip install dcm2bids        # dcm2bids - 基于配置文件的转换
# BIDScoin: uv pip install bidscoin

# 有用的伴侣库
uv pip install nibabel          # NIfTI/其他神经影像文件 I/O
uv pip install pydicom          # DICOM 文件读取（转换器使用）
```

## 核心工作流程

### 1. BIDS 目录结构

最小的 BIDS 数据集遵循以下布局：

```
my_dataset/
  dataset_description.json      # 必需：name、BIDSVersion 等
  participants.tsv            # 推荐：受试者层面的表型数据
  participants.json           # 推荐：列描述
  README                      # 推荐：数据集文档
  CHANGES                     # 推荐：版本历史
  .bidsignore                 # 可选：验证中排除的模式
  sub-01/
    anat/
      sub-01_T1w.nii.gz
      sub-01_T1w.json           # 侧边栏元数据
    func/
      sub-01_task-rest_bold.nii.gz
      sub-01_task-rest_bold.json
      sub-01_task-rest_events.tsv     # 任务 fMRI 的事件时间
      sub-01_task-rest_events.json
    dwi/
      sub-01_dwi.nii.gz
      sub-01_dwi.json
      sub-01_dwi.bvec
      sub-01_dwi.bval
    fmap/
      sub-01_phasediff.nii.gz
      sub-01_phasediff.json
      sub-01_magnitude1.nii.gz
    perf/
      sub-01_asl.nii.gz
      sub-01_asl.json
  sub-01/
    ses-pre/
      anat/
        sub-01_ses-pre_T1w.nii.gz
      func/
        sub-01_ses-pre_task-nback_bold.nii.gz
    ses-post/
      ...
```

**要点：**
- 每个 NIfTI 文件都应该有对应的 `.json` 侧边栏
- 文件名编码实体：`sub-<label>[_ses-<label>][_task-<label>][_acq-<label>][_run-<index>]_<suffix>.<extension>`
- 文件名中实体的顺序由规范固定
- 根目录下只有 `dataset_description.json` 是严格必需的

### 2. 创建 dataset_description.json

```python
import json

dataset_description = {
    "Name": "My Neuroimaging Study",
    "BIDSVersion": "1.10.0",
    "DatasetType": "raw",
    "License": "CC0",
    "Authors": ["First Author", "Second Author"],
    "Acknowledgements": "Funded by NIH R01-MH123456",
    "HowToAcknowledge": "Please cite: Author et al. (2025) Journal Name.",
    "Funding": ["NIH R01-MH123456", "NSF BCS-7654321"],
    "ReferencesAndLinks": ["https://doi.org/10.xxxx/xxxxx"],
    "DatasetDOI": "10.18112/openneuro.ds000001.v1.0.0",
    "GeneratedBy": [
        {
            "Name": "HeuDiConv",
            "Version": "1.3.1",
            "CodeURL": "https://github.com/nipy/heudiconv"
        }
    ]
}

with open("dataset_description.json", "w") as f:
    json.dump(dataset_description, f, indent=4)
```

对于**衍生数据**，设置 `"DatasetType": "derivative"` 并添加列出流水线的 `"GeneratedBy"`：

```python
deriv_description = {
    "Name": "fMRIPrep - fMRI PREProcessing",
    "BIDSVersion": "1.10.0",
    "DatasetType": "derivative",
    "GeneratedBy": [
        {
            "Name": "fMRIPrep",
            "Version": "24.1.0",
            "CodeURL": "https://github.com/nipreps/fmriprep"
        }
    ]
}
```

### 3. 使用 PyBIDS 查询 BIDS 数据集

```python
from bids import BIDSLayout

# 索引 BIDS 数据集（加载时验证结构）
layout = BIDSLayout("/path/to/bids_dataset")

# 基本查询
subjects = layout.get_subjects()          # ['01', '02', '03', ...]
sessions = layout.get_sessions()          # ['pre', 'post'] or []
tasks = layout.get_tasks()                # ['rest', 'nback']
runs = layout.get_runs()                  # [1, 2] or []

# 查找特定文件
bold_files = layout.get(
    suffix="bold",
    extension=".nii.gz",
    return_type="filename"
)

# 按受试者、任务、会话筛选
nback_sub01 = layout.get(
    subject="01",
    task="nback",
    suffix="bold",
    extension=".nii.gz",
    return_type="filename"
)

# 从 JSON 侧边栏获取元数据（自动继承）
metadata = layout.get_metadata("/path/to/sub-01/func/sub-01_task-rest_bold.nii.gz")
tr = metadata["RepetitionTime"]

# 获取文件的所有实体
entities = layout.get_entities()

# 使用 BIDSLayout 根据实体构建路径
bids_file = layout.get(subject="01", suffix="T1w", extension=".nii.gz")[0]
print(bids_file.path)
print(bids_file.get_entities())
```

**要点：**
- `BIDSLayout` 在初始化时索引整个数据集；对于大型数据集，使用 `database_path` 缓存索引
- 元数据继承：更高级别（例如根目录或受试者级别）的 JSON 侧边栏会被下方所有文件继承，除非被覆盖
- 使用 `return_type="filename"` 获取路径，`return_type="object"`（默认）获取 `BIDSFile` 对象

### 4. 验证 BIDS 数据集

#### 通过 PyPI 使用 bids-validator（推荐）

`bids-validator-deno` PyPI 包将基于 Deno 的验证器打包为独立 CLI：

```bash
# 安装
uv pip install bids-validator-deno

# 验证数据集
bids-validator /path/to/bids_dataset

# 忽略特定警告/错误
bids-validator /path/to/bids_dataset --ignoreNiftiHeaders --ignoreSubjectConsistency
```

#### 通过 Deno 直接使用 bids-validator

如果 Deno 已可用，您可以安装或运行验证器而不使用 PyPI：

```bash
# 通过 Deno 全局安装
deno install -g -A npm:bids-validator

# 或不安装直接运行
deno run -A npm:bids-validator /path/to/bids_dataset
```

#### 旧的 Node.js 验证器

旧的基于 Node.js 的验证器（`npm install -g bids-validator`）已被弃用，推荐使用基于 Deno 的版本。Deno 版本是 BIDS 规范 v1.9+ 的参考实现。

#### 使用 .bidsignore

在数据集根目录创建 `.bidsignore` 以从验证中排除文件（gitignore 语法）：

```
# 排除 sourcedata 和额外文件
sourcedata/
extra_data/
*.log
*_sbref.nii.gz
**/.DS_Store
```

### 5. BIDS 实体和文件命名

实体、其排序、允许的后缀和所有文件名规则的权威、可读的真相来源是 **BIDS Schema** — 规范的结构化 YAML/JSON 表示。JSON 导出随本技能一起提供，位于 `references/bids_schema.json`。模式定义在 [bids-specification `src/schema/`](https://github.com/bids-standard/bids-specification/tree/master/src/schema) 目录，发布于 https://bids-specification.readthedocs.io/en/stable/schema.json。BEP 特定的模式预览见 https://github.com/bids-standard/bids-schema/tree/main/BEPs。

运行 `scripts/update_schema.py` 刷新上游的模式和 BEP 列表（除了标准库无依赖）。

下表是方便的总结；有疑问时，请查阅模式。

BIDS 文件名由有序的键值实体对构建：

| 实体 | 键 | 示例 | 必需用于 |
|------|-----|---------|----------|
| Subject | `sub-` | `sub-01` | 所有文件 |
| Session | `ses-` | `ses-pre` | 多会话研究 |
| Task | `task-` | `task-rest` | func (bold, cbv, phase)、eeg、meg |
| Acquisition | `acq-` | `acq-highres` | 区分采集参数 |
| Contrast enhancing agent | `ce-` | `ce-gadolinium` | 对比增强图像 |
| Reconstruction | `rec-` | `rec-magnitude` | 重建变体 |
| Direction | `dir-` | `dir-AP` | 场图、DWI、相位编码 |
| Run | `run-` | `run-01` | 多次相同采集 |
| Echo | `echo-` | `echo-1` | 多回波序列 |
| Part | `part-` | `part-mag` | 幅值/相位分割 |
| Space | `space-` | `space-MNI152NLin2009cAsym` | 模板空间的衍生数据 |
| Description | `desc-` | `desc-preproc` | 仅衍生数据 |

**文件名中的实体顺序** 由规范固定（在 `bids_schema.json` 的 `rules.entities` 中定义）。见 `references/bids_specification.md` 获取完整的编号排序表。常见子集：
`sub-<label>[_ses-<label>][_task-<label>][_acq-<label>][_ce-<label>][_rec-<label>][_dir-<label>][_run-<index>][_echo-<index>][_part-<label>][_space-<label>][_desc-<label>]_<suffix>.<extension>`

**按数据类型的常见后缀：**

| 数据类型 | 后缀 |
|----------|------|
| anat | `T1w`、`T2w`、`FLAIR`、`T2star`、`T1map`、`T2map`、`defacemask` |
| func | `bold`、`cbv`、`sbref`、`events`、`physio`、`stim` |
| dwi | `dwi`、`sbref` |
| fmap | `phasediff`、`phase1`、`phase2`、`magnitude1`、`magnitude2`、`fieldmap`、`epi` |
| perf | `asl`、`m0scan`、`aslcontext` |
| eeg | `eeg`、`channels`、`electrodes`、`events` |
| meg | `meg`、`channels`、`coordsystem`、`events` |
| ieeg | `ieeg`、`channels`、`electrodes`、`coordsystem`、`events` |
| pet | `pet`、`blood` |

### 6. DICOM 到 BIDS 转换

#### HeuDiConv

HeuDiConv 是最灵活的 DICOM 到 BIDS 转换器。它支持三种使用模式 — 从全自动到完全自定义 — 并开箱即用处理重复项、溯源跟踪和 sourcedata 归档。

**模式 1：ReproIn（现成，推荐用于新研究）**

如果扫描协议名称遵循 [ReproIn 命名约定](https://github.com/repronim/reproin)，转换完全自动化 — 无需编写启发式文件：

```bash
# 现成转换：HeuDiConv 自动将 ReproIn 协议名称映射到 BIDS
heudiconv --files dicom/001 -o /path/to/bids -f reproin --bids --minmeta
```

ReproIn 协议名称直接编码 BIDS 实体：
- `anat-T1w` → `sub-XX/anat/sub-XX_T1w.nii.gz`
- `func-bold_task-rest` → `sub-XX/func/sub-XX_task-rest_bold.nii.gz`
- `dwi_dir-AP` → `sub-XX/dwi/sub-XX_dir-AP_dwi.nii.gz`
- `fmap_dir-PA` → `sub-XX/fmap/sub-XX_dir-PA_epi.nii.gz`

会话可以在本地化器上设置一次（例如 `anat-scout_ses-pre`），ReproIn 会将其传播到该程序中的所有序列。主题 ID 从 DICOM 元数据中提取。重复运行自动编号。

**模式 2：自定义启发式映射到 ReproIn（用于现有数据）**

如果您已有具有非 ReproIn 协议名称的数据，您可以编写一个薄的启发式文件，将您的名称映射到 ReproIn 约定，从而获得所有 ReproIn 优势（自动实体处理、重复管理等）。见 https://github.com/repronim/reproin/issues/18 获取操作指南。

**模式 3：自定义启发式（完全灵活性）**

对于复杂映射，编写 Python 启发式文件：

```bash
# 步骤 1：侦察 — 发现 DICOM 系列
heudiconv --files dicom/219/itbs/*/*.dcm -o Nifti/ -f convertall -s 219 -c none

# 这创建了 .heudiconv/219/info/dicominfo.tsv — 检查它以了解
# 获取了什么并将系列映射到 BIDS 名称。

# 步骤 2：编写启发式文件（见 references/conversion_tools.md）

# 步骤 3：转换
heudiconv --files dicom/219/itbs/*/*.dcm -s 219 -ss itbs \
  -f Nifti/code/heuristic.py -c dcm2niix --bids --minmeta -o Nifti/
```

完整的启发式文件示例见 `references/conversion_tools.md`。

**要点：**
- HeuDiConv 包装 `dcm2niix` 进行实际的 DICOM 到 NIfTI 转换
- **`--minmeta`**：始终使用此标志以防止过量 DICOM 元数据溢出 JSON 侧边栏（可能使 fMRIPrep/MRIQC 崩溃）
- **重复处理**：在同一协议运行多次时，在模板中使用 `{item:03d}` 进行自动编号；否则后面的运行会覆盖前面的
- **`.heudiconv/` 目录**：与输出一起创建，存储溯源（使用的启发式文件、dicominfo.tsv、转换记录）。保留它与您的数据一起以确保可重复性
- **`sourcedata/`**：HeuDiConv 将原始 DICOM 归档为 `.tgz` 文件放在 `sourcedata/` 下以确保可重复性
- **`is_motion_corrected` 过滤器**：在启发式文件中使用以排除扫描仪生成的 MOCO 系列（例如 `if not s.is_motion_corrected`）
- 支持 `--files`（显式路径）和 `-d`（带 `{subject}`、`{session}` 占位符的模板）来指定 DICOM 输入

#### dcm2bids（基于配置文件）

```bash
# 步骤 1：生成辅助输出以检查系列
dcm2bids_helper -d /path/to/dicom

# 步骤 2：创建配置文件 (dcm2bids_config.json)
# 步骤 3：转换
dcm2bids -d /path/to/dicom -p 01 -c dcm2bids_config.json -o /path/to/bids_output
```

详细配置示例见 `references/conversion_tools.md`。

### 7. 元数据侧边栏

每个 BIDS 数据文件都应该有一个包含采集参数的 JSON 侧边栏。元数据字段遵循继承原则：更高级别目录的侧边栏适用于其下方的所有匹配文件。

**继承示例：**
```
my_dataset/
  task-rest_bold.json           # 适用于所有 rest BOLD 文件
  sub-01/
    func/
      sub-01_task-rest_bold.json  # 仅覆盖/扩展 sub-01
```

**按模态的关键元数据字段：**

对于 **func (BOLD)**：
```json
{
    "RepetitionTime": 2.0,
    "TaskName": "rest",
    "PhaseEncodingDirection": "j-",
    "TotalReadoutTime": 0.05,
    "SliceTiming": [0, 0.5, 1.0, 1.5],
    "EffectiveEchoSpacing": 0.00058,
    "EchoTime": 0.03
}
```

对于 **anat**：
```json
{
    "MagneticFieldStrength": 3,
    "Manufacturer": "Siemens",
    "ManufacturersModelName": "Prisma",
    "RepetitionTime": 2.3,
    "EchoTime": 0.00293,
    "FlipAngle": 8
}
```

对于 **DWI**：
```json
{
    "PhaseEncodingDirection": "j-",
    "TotalReadoutTime": 0.05,
    "EchoTime": 0.089,
    "RepetitionTime": 3.4,
    "MultipartID": "dwi_1"
}
```

**要点：**
- `dcm2niix` 自动从 DICOM 头生成大多数侧边栏字段
- `RepetitionTime` 和 `TaskName` 对 BOLD 是必需的
- `SliceTiming` 对 fMRI 预处理中的切片时间校正至关重要
- `PhaseEncodingDirection` 和 `TotalReadoutTime`（或 `EffectiveEchoSpacing`）是失真校正所需的
- 综合字段参考见 `references/metadata_fields.md`

### 8. 任务 fMRI 的事件文件

基于任务的 fMRI 需要 `_events.tsv` 文件：

```
onset	duration	trial_type	response_time
0.0	0.5	face	0.435
2.5	0.5	house	0.367
5.0	0.5	face	0.512
7.5	0.5	scrambled	0.298
```

**必需列：**
- `onset` - 相对于采集开始的时间（秒）
- `duration` - 持续时间（秒）（瞬时事件使用 `n/a`）

**推荐列：**
- `trial_type` - 条件的分类标签
- `response_time` - 反应时间（秒）
- 自定义列（如需要，在对应的 `.json` 侧边栏中描述）

### 9. 参与者文件

```
participant_id	age	sex	group	handedness
sub-01	25	M	control	right
sub-02	30	F	patient	left
sub-03	28	M	control	right
```

`participants.json` 侧边栏描述列：

```json
{
    "age": {
        "Description": "Age of the participant at time of scanning",
        "Units": "years"
    },
    "sex": {
        "Description": "Biological sex",
        "Levels": {
            "M": "male",
            "F": "female"
        }
    },
    "group": {
        "Description": "Experimental group",
        "Levels": {
            "control": "Healthy control",
            "patient": "Patient group"
        }
    },
    "handedness": {
        "Description": "Dominant hand",
        "Levels": {
            "right": "Right-handed",
            "left": "Left-handed",
            "ambidextrous": "Ambidextrous"
        }
    }
}
```

### 10. BIDS 衍生数据

处理后的输出放在 `derivatives/` 目录下：

```
my_dataset/
  derivatives/
    fmriprep-24.1.0/
      dataset_description.json      # DatasetType: "derivative"
      sub-01/
        anat/
          sub-01_space-MNI152NLin2009cAsym_desc-preproc_T1w.nii.gz
          sub-01_space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz
        func/
          sub-01_task-rest_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz
          sub-01_task-rest_desc-confounds_timeseries.tsv
    mriqc-24.0.0/
      dataset_description.json
      sub-01/
        anat/
          sub-01_T1w.html
        func/
          sub-01_task-rest_bold.html
      group_T1w.tsv
      group_bold.tsv
```

**衍生数据约定：**
- `space-<label>` - 模板/参考空间（例如 `MNI152NLin2009cAsym`、`T1w`）
- `desc-<label>` - 处理描述（例如 `preproc`、`brain`、`smoothed`）
- `res-<label>` - 分辨率（例如 `2` 表示 2mm 各向同性）
- 每个流水线在 `derivatives/` 下有自己的目录
- 必须有自己的 `dataset_description.json`，包含 `GeneratedBy`

### 11. PyBIDS：高级用法

```python
from bids import BIDSLayout
from bids.layout import BIDSLayoutIndexer

# 缓存布局索引以加快重复访问
layout = BIDSLayout("/path/to/dataset", database_path="/path/to/cache.db")

# 包含衍生数据
layout = BIDSLayout(
    "/path/to/dataset",
    derivatives=["/path/to/dataset/derivatives/fmriprep-24.1.0"]
)

# 获取衍生文件
preproc = layout.get(
    subject="01",
    task="rest",
    desc="preproc",
    suffix="bold",
    space="MNI152NLin2009cAsym",
    extension=".nii.gz",
    return_type="filename"
)

# 获取混淆回归因子
confounds = layout.get(
    subject="01",
    task="rest",
    desc="confounds",
    suffix="timeseries",
    extension=".tsv",
    return_type="filename"
)

# 根据实体构建 BIDS 路径
from bids import BIDSLayout
layout = BIDSLayout("/path/to/dataset")
path = layout.build_path(
    {
        "subject": "01",
        "session": "pre",
        "task": "rest",
        "suffix": "bold",
        "extension": ".nii.gz",
        "datatype": "func"
    },
    validate=True
)

# 获取受试者的所有文件作为 DataFrame
import pandas as pd
files_df = layout.to_df()
sub01_df = files_df[files_df["subject"] == "01"]
```

### 12. BIDS-Apps

BIDS-Apps 是容器化的分析管道，接受 BIDS 数据集作为输入：

```bash
# 通用 BIDS-App 调用模式
docker run -v /path/to/bids:/data:ro -v /path/to/output:/out \
    <bids-app-image> /data /out participant --participant_label 01

# 常见 BIDS-Apps：
# fMRIPrep - fMRI 预处理
docker run nipreps/fmriprep /data /out participant \
    --participant-label 01 --fs-license-file /license.txt

# MRIQC - MRI 质量控制
docker run nipreps/mriqc /data /out participant \
    --participant-label 01

# QSIPrep - 扩散 MRI 预处理
docker run pennbbl/qsiprep /data /out participant \
    --participant-label 01
```

**BIDS-App 接口约定：**
```
bids-app input_dataset output_dir {participant|group} [options]
```

- `participant` 级别：每个受试者运行
- `group` 级别：跨所有受试者运行（聚合/组统计）

## 参考材料

本技能包含详细参考文档：

- **bids_schema.json**：机器可读的 BIDS 模式（来自 https://bids-specification.readthedocs.io/en/stable/schema.json）。这是实体定义、排序规则、文件名模板、每个数据类型允许的后缀和元数据字段要求的权威来源。BEP 特定模式见 https://github.com/bids-standard/bids-schema/tree/main/BEPs。
- **beps.yml**：所有 BIDS 扩展提案的当前列表，包含标题、负责人、状态和链接（来自 [bids-website](https://github.com/bids-standard/bids-website/blob/main/data/beps/beps.yml)）
- **bids_specification.md**：实体表、数据类型参考、目录结构规则、模板空间和规范变更日志的人类可读摘要
- **metadata_fields.md**：每个 BIDS 模态（anat、func、dwi、fmap、eeg、meg、pet 等）所需和推荐的 JSON 侧边栏字段
- **conversion_tools.md**：HeuDiConv、dcm2bids 和 BIDScoin 的详细工作流程，包括启发式/配置示例和故障排除

更新模式和 BEP：`python scripts/update_schema.py`

## 常见问题和解决方案

### 1. 验证器报告"不是 BIDS 数据集"
**原因**：根目录缺少 `dataset_description.json`。
**修复**：创建文件，至少包含 `{"Name": "...", "BIDSVersion": "1.10.0"}`。

### 2. 不一致的受试者警告
**原因**：并非所有受试者都有相同的文件集（某些缺少会话、运行等）。
**修复**：这是警告，不是错误。如果是有意的，使用 `--ignoreSubjectConsistency`。在 `participants.tsv` 或 `scans.tsv` 中记录缺失数据。

### 3. 缺少 SliceTiming
**原因**：`dcm2niix` 无法从 DICOM 头提取切片时间。
**修复**：从扫描协议确定切片顺序并手动添加到 JSON 侧边栏。常见模式：升序、降序、交错（奇数优先或偶数优先）。

### 4. 相位编码方向混淆
**原因**：轴标签（i/j/k vs x/y/z vs LR/AP/SI）令人困惑。
**修复**：在 BIDS 中，使用 NIfTI 图像轴：`i`=第一轴，`j`=第二轴，`k`=第三轴。`-` 表示负方向。对于标准轴向采集：`j` 通常是前-后。从采集协议验证。

### 5. PyBIDS 在大型数据集上很慢
**原因**：每次 `BIDSLayout()` 调用都进行完整文件系统索引。
**修复**：使用 `database_path` 将索引缓存到 SQLite 文件：
```python
layout = BIDSLayout("/data", database_path="/data/.pybids_cache.db")
```

### 6. 衍生数据未被 PyBIDS 找到
**原因**：衍生数据目录缺少自己的 `dataset_description.json`。
**修复**：每个衍生数据目录必须包含 `dataset_description.json`，其中 `"DatasetType": "derivative"`。

### 7. 事件文件时间不对
**原因**：onset 时间参考错误（例如，触发时间 vs 第一个 volume）。
**修复**：onset 必须是相对于该 run 采集的第一个 volume 的秒数。如果丢弃了 dummy scans，需要考虑这些。

### 8. TSV 文件验证失败
**原因**：编码或分隔符问题（空格而非制表符、BOM 字符、Windows 换行符）。
**修复**：确保使用 UTF-8 编码和制表符分隔的值以及 Unix 换行符（`\n`）。使用 `n/a`（而非 `NA`、`NaN` 或空）表示缺失值。

## 最佳实践

1. **尽早并经常验证** - 每次转换或修改后运行 BIDS 验证器。修复错误后再继续。

2. **使用元数据继承** - 将共享的元数据（例如 `TaskName`、扫描仪参数）放在顶层侧边栏文件中，而不是在每个受试者的目录中重复。

3. **保留 sourcedata** - 将原始 DICOM（或其他原始数据）存储在 `sourcedata/` 下，以便转换可重现。将 `sourcedata/` 添加到 `.bidsignore`。

4. **从一开始就使用一致的命名** - 在数据收集之前定义您的 BIDS 命名方案。使用 ReproIn 命名约定进行扫描协议以启用自动转换。

5. **记录您的数据集** - 编写详细的 `README`，描述研究设计、采集参数、已知问题和与 BIDS 的任何偏差。

6. **使用 scans.tsv 进行 run 级元数据** - 记录每个 run 的采集时间和质量注释：

```bash
# 示例 scans.tsv
filename	acq_time	quality_notes
sub-01_task-rest_run-01_bold.nii.gz	2024-01-15T10:30:00	good
sub-01_task-rest_run-02_bold.nii.gz	2024-01-15T10:45:00	good
```

## BIDS 扩展提案（BEP）

BEP 是社区驱动的提案，用于将 BIDS 扩展到新模态、衍生数据或元数据。完整列表（包括状态、负责人和链接）请参见 `references/beps.yml`（从 bids-website 获取）。BEP 特定的模式预览请访问 https://github.com/bids-standard/bids-schema/tree/main/BEPs。

**当前 BEP**（截至模式更新）：

| BEP | 标题 | 内容 | 状态 |
|-----|------|------|------|
| 004 | 磁化率加权成像 | 原始数据 | 寻求新负责人 |
| 011 | 结构预处理衍生数据 | 衍生数据 | 有 PR (#518) |
| 012 | 功能预处理衍生数据 | 衍生数据 | 有 PR (#519)，模式已实现 |

## 相关工具生态系统

| 工具 | 用途 |
|------|------|
| HeuDiConv | DICOM 到 BIDS 神经影像转换 |
| dcm2bids | 基于配置文件的 DICOM 到 BIDS 转换 |
| PyBIDS | Python BIDS 数据集查询和操作 |
| bids-validator | BIDS 数据集验证 |
| bidscoin | BIDS 数据集后期处理和报告生成 |
| QR | BIDS 查询报告生成 |

## 文档

- **BIDS 规范**: https://bids-specification.readthedocs.io/
- **BIDS 初学者指南**: https://bids-starter-kit.readthedocs.io/
- **PyBIDS 文档**: https://bids-standard.github.io/pybids/
- **bids-validator 文档**: https://bids-standard.github.io/bids-validator/
