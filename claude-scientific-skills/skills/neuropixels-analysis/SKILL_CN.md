---
name: neuropixels-analysis
description: 使用 SpikeInterface 端到端分析 Neuropixels 细胞外记录。涵盖加载 SpikeGLX/Open Ephys/NWB 数据、预处理、漂移/运动校正、Kilosort4（及 CPU）spike 分类、质量指标，以及单位筛选（基于阈值、基于模型的 UnitRefine 以及 AI 辅助的可视化审查）。当处理 Neuropixels 1.0/2.0 记录、spike 分类或细胞外电生理学分析时使用。
license: MIT license
required_environment_variables: [{"name": "ANTHROPIC_API_KEY", "prompt": "For optional Claude API calls.", "required_for": "optional features"}]
metadata: {"version": "2.1", "skill-author": "K-Dense Inc.", "openclaw": {"primaryEnv": "ANTHROPIC_API_KEY", "envVars": [{"name": "ANTHROPIC_API_KEY", "required": false, "description": "For optional Claude API calls."}]}}
---

# Neuropixels数据分析

## 概述

用于分析 Neuropixels 高密度神经记录的工具包,采用来自 [SpikeInterface](https://spikeinterface.readthedocs.io/)、Allen 研究所和国际脑实验室(IBL)的最新最佳实践。它涵盖从原始数据到可发表的经筛选单位的完整工作流程。

所有示例均使用真实的 SpikeInterface API(`spikeinterface.full as si`）以及配套的筛选模块(`spikeinterface.curation as sc`）。此技能在 `scripts/` 中提供可运行的脚本,并在 `assets/` 中提供可复制编辑的模板,它们直接基于 SpikeInterface 实现此工作流程——除了[安装](#安装)部分列出的依赖项外,无需安装单独的软件包。

## 何时使用此技能

在以下情况下应使用此技能:
- 处理 Neuropixels 记录(`.ap.bin`、`.lf.bin`、`.meta` 文件)
- 从 SpikeGLX、Open Ephys 或 NWB 格式加载数据
- 预处理神经记录(滤波、共同参考、坏通道检测)
- 检测和校正运动/漂移
- 运行 spike sorting(Kilosort4、SpykingCircus2、Mountainsort5、Tridesclous2)
- 计算质量指标(SNR、ISI 违规、存在率、幅度截止)
- 筛选单位(基于阈值、基于模型或 AI 辅助)
- 创建可视化并导出到 Phy 或 NWB

## 支持的硬件和格式

| 探针 | 电极 | 通道 | 备注 |
|-------|-----------|----------|-------|
| Neuropixels 1.0 | 960 | 384 | 使用 `phase_shift` 进行 ADC 校正 |
| Neuropixels 2.0 (单探针) | 1280 | 384 | 更密集的几何结构 |
| Neuropixels 2.0 (4-shank) | 5120 | 384 | 多区域记录 |

| 格式 | 扩展名 | 读取器 |
|--------|-----------|--------|
| SpikeGLX | `.ap.bin`, `.lf.bin`, `.meta` | `si.read_spikeglx()` |
| Open Ephys | `.continuous`, `.oebin` | `si.read_openephys()` |
| NWB | `.nwb` | `si.read_nwb()` |

## 快速开始

### 导入并配置并行处理

```python
import spikeinterface.full as si

# 全局作业参数会被所有可并行化的步骤重用
si.set_global_job_kwargs(n_jobs=-1, chunk_duration="1s", progress_bar=True)
```

### 加载数据

```python
# 首先检查可用的流
stream_names, stream_ids = si.get_neo_streams("spikeglx", "/path/to/run_g0/")
print(stream_names)  # 例如 ['imec0.ap', 'imec0.lf', 'nidq']

# SpikeGLX(最常见) — 按名称选择 AP 流
recording = si.read_spikeglx("/path/to/run_g0/", stream_name="imec0.ap", load_sync_channel=False)

# Open Ephys
recording = si.read_openephys("/path/to/Record_Node_101/")

# 为快速迭代,截取前 60 秒
fs = recording.get_sampling_frequency()
recording_sub = recording.frame_slice(0, int(60 * fs))
```

### 完整管道(内置脚本)

该仓库提供了一个基于 SpikeInterface 构建的端到端管道:

```bash
python scripts/neuropixels_pipeline.py /path/to/spikeglx/data output/ --sorter kilosort4 --curation allen
```

它依次执行加载 → 预处理 → 漂移检查 → 可选运动校正 → 分类 → 后处理 → 质量指标 → 筛选 → 导出。请阅读下面的步骤以交互式运行或自定义该管道。

## 标准分析工作流程

### 1. 预处理

推荐的处理链,遵循 SpikeInterface 的 Neuropixels 操作指南(IBL 风格的条纹去除,包含通道移除 + 共同参考):

```python
rec = si.highpass_filter(recording, freq_min=400.0)
bad_channel_ids, channel_labels = si.detect_bad_channels(rec)
rec = rec.remove_channels(bad_channel_ids)
rec = si.phase_shift(rec)  # ADC 相位校正(Neuropixels 1.0)
rec = si.common_reference(rec, operator="median", reference="global")
```

保存预处理后的记录(Kilosort 需要二进制文件,并且这样也能加速重用):

```python
rec = rec.save(folder="preprocessed/", format="binary")
```

### 2. 检查和校正漂移

在分类之前,始终检查漂移:

```python
from spikeinterface.sortingcomponents.peak_detection import detect_peaks
from spikeinterface.sortingcomponents.peak_localization import localize_peaks

noise_levels = si.get_noise_levels(rec, return_in_uV=False)
peaks = detect_peaks(rec, method="locally_exclusive", noise_levels=noise_levels,
                     detect_threshold=5, radius_um=50.0)
peak_locations = localize_peaks(rec, peaks, method="center_of_mass")

# 可视化漂移光栅图
si.plot_drift_raster_map(peaks=peaks, peak_locations=peak_locations,
                         recording=rec, clim=(-50, 50))
```

如有需要则应用校正(预设：`rigid_fast`、`kilosort_like`、
`nonrigid_accurate`、`nonrigid_fast_and_accurate`、`dredge`、`dredge_fast`):

```python
rec_corrected = si.correct_motion(rec, preset="nonrigid_fast_and_accurate", folder="motion/")
```

### 3. Spike sorting

```python
# Kilosort4(推荐,需要 CUDA GPU)
sorting = si.run_sorter("kilosort4", rec_corrected, folder="ks4_output")

# CPU 替代方案(内部开发,无需外部安装)
sorting = si.run_sorter("spykingcircus2", rec_corrected, folder="sc2_output")
sorting = si.run_sorter("tridesclous2", rec_corrected, folder="tdc2_output")
sorting = si.run_sorter("mountainsort5", rec_corrected, folder="ms5_output")

# 外部 sorter 可以在容器中运行,无需本地安装
sorting = si.run_sorter("kilosort2_5", rec_corrected, folder="ks25_output", docker_image=True)

print(si.installed_sorters())
```

> 注意：`run_sorter` 使用 `folder=` 参数。旧的 `output_folder=` 已被弃用。

### 4. 后处理

```python
analyzer = si.create_sorting_analyzer(sorting, rec_corrected, sparse=True,
                                      format="binary_folder", folder="analyzer/")

analyzer.compute("random_spikes", method="uniform", max_spikes_per_unit=500)
analyzer.compute("waveforms", ms_before=1.0, ms_after=2.0)
analyzer.compute("templates", operators=["average", "std"])
analyzer.compute("noise_levels")
analyzer.compute("spike_amplitudes")
analyzer.compute("correlograms", window_ms=50.0, bin_ms=1.0)
analyzer.compute("unit_locations", method="monopolar_triangulation")
analyzer.compute("template_similarity")

metric_names = ["firing_rate", "presence_ratio", "snr", "isi_violation", "amplitude_cutoff"]
analyzer.compute("quality_metrics", metric_names=metric_names)
metrics = analyzer.get_extension("quality_metrics").get_data()
```

### 5. 基于指标阈值的筛选

```python
# Allen 风格的查询(注意：列名为 isi_violations_ratio)
query = "(amplitude_cutoff < 0.1) & (isi_violations_ratio < 0.5) & (presence_ratio > 0.9)"
good_unit_ids = metrics.query(query).index.values
```

要使用带有 `allen` / `ibl` / `strict` 预设的可复用多阈值逻辑,请使用内置的 `scripts/compute_metrics.py`。详情及 Bombcell / UnitMatch 工具请参阅 [references/AUTOMATED_CURATION.md](references/AUTOMATED_CURATION.md)。

### 6. 基于模型的筛选(UnitRefine)

SpikeInterface 可以通过 `spikeinterface.curation` 模块应用来自 Hugging Face 的预训练机器学习分类器。UnitRefine 模型是在真实的 Neuropixels 数据(V1、SC、ALM）上训练的:

```python
import spikeinterface.curation as sc

# 1) 噪声 vs 神经元
noise_labels = sc.model_based_label_units(
    sorting_analyzer=analyzer,
    repo_id="SpikeInterface/UnitRefine_noise_neural_classifier",
    trust_model=True,
)
neural = analyzer.remove_units(noise_labels[noise_labels["prediction"] == "noise"].index)

# 2) 对存留的单位进行单神经元(sua) vs 多神经元(mua)分类
sua_mua_labels = sc.model_based_label_units(
    sorting_analyzer=neural,
    repo_id="SpikeInterface/UnitRefine_sua_mua_classifier",
    trust_model=True,
)
```

每次调用都会返回一个包含每个单位的 `prediction` 和 `probability`(置信度）的 DataFrame。加载 `.skops` 模型需要 `trust_model=True`(或明确的 `trusted=[...]` 列表)——只加载来自您信任的来源的模型。在其他脑区/数据集上训练的模型可能无法直接迁移;应对照人工标注的子集进行验证。

### 7. AI 辅助筛选(用于不确定的单位)

当在 Cursor 或 Claude Code 等智能体环境中运行时,智能体可以直接检查波形/相关图并给出专家判断——无需 API 设置。生成图表并要求智能体评估隔离质量。

对于编程式的视觉模型访问,**从环境中读取 API 密钥——切勿在分析脚本中硬编码凭据**(它们会泄漏到版本控制和日志中):

```python
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])  # 在 shell 中设置,而不是在代码中
```

完整模式(渲染单位摘要图像、构建提示词以及解析响应)请参阅 [references/AI_CURATION.md](references/AI_CURATION.md)。

### 8. 导出结果

```python
# 只保留好的单位,然后导出
analyzer_clean = analyzer.select_units(good_unit_ids, folder="analyzer_clean/", format="binary_folder")

# 用于手动审查的 Phy
si.export_to_phy(analyzer_clean, output_folder="phy_export/",
                 compute_pc_features=True, compute_amplitudes=True)

# 图表报告
si.export_report(analyzer_clean, "report/", format="png")

# NWB
from spikeinterface.exporters import export_to_nwb
export_to_nwb(analyzer_clean, "output.nwb")

# 指标表
metrics.to_csv("quality_metrics.csv")
```

## 常见陷阱和最佳实践

1. **始终检查漂移**,在 spike sorting 之前——漂移 > 约 10 μm 会显著降低质量。
2. **对 Neuropixels 1.0 使用 `phase_shift`**,以校正 ADC 采样偏移。
3. **保存预处理后的记录**,使用 `rec.save(folder=...)` 以避免重新计算(Kilosort 也需要二进制文件)。
4. **对 Kilosort4 使用 GPU**——它比 CPU sorter 快得多。
5. **审查不确定的单位**——自动/基于模型的筛选是一个起点,而不是最终定论。
6. **结合多种方法**——对明确情况使用阈值,对边界单位使用模型/AI。
7. **记录阈值和模型仓库 ID**以确保可复现性。
8. **对关键实验导出到 Phy**——人工监督很有价值。

## 需要调整的关键参数

### 预处理
- `freq_min`：高通截止频率(300–400 Hz 典型)
- `detect_bad_channels`：返回 `(bad_channel_ids, channel_labels)`

### 运动校正
- `preset`：`nonrigid_fast_and_accurate`(平衡)、`nonrigid_accurate`(严重漂移)、`dredge`(最先进)

### Spike Sorting(Kilosort4)
- `batch_size`：每批样本数(默认 60000)
- `nblocks`：漂移块数(长且有漂移的记录应增加)
- `Th_universal` / `Th_learned`：检测阈值(越低=更多 spikes)

### 质量指标
- `snr`：信噪比截止(3–5 典型)
- `isi_violations_ratio`：不应期违规(0.01–0.5)
- `presence_ratio`：记录覆盖率(0.5–0.95)

## 内置资源

### scripts/explore_recording.py
快速检查记录(流、通道、时长、坏通道):
```bash
python scripts/explore_recording.py /path/to/data
```

### scripts/preprocess_recording.py
自动预处理:
```bash
python scripts/preprocess_recording.py /path/to/data --output preprocessed/
```

### scripts/run_sorting.py
运行spike sorting:
```bash
python scripts/run_sorting.py preprocessed/ --sorter kilosort4 --output sorting/
```

### scripts/compute_metrics.py
计算质量指标并应用筛选:
```bash
python scripts/compute_metrics.py sorting/ preprocessed/ --output metrics/ --curation allen
```

### scripts/export_to_phy.py
导出到Phy以进行手动筛选:
```bash
python scripts/export_to_phy.py metrics/analyzer --output phy_export/
```

### scripts/neuropixels_pipeline.py
完整的端到端管道(参见[快速开始](#完整管道内置脚本))。

### assets/analysis_template.py
完整的、可编辑的分析模板。复制并自定义:
```bash
cp assets/analysis_template.py my_analysis.py
# 编辑 PARAMETERS 部分,然后运行
python my_analysis.py
```

## 详细参考指南

| 主题 | 参考 |
|-------|-----------|
| 完整工作流程 | [references/standard_workflow.md](references/standard_workflow.md) |
| API参考(SpikeInterface) | [references/api_reference.md](references/api_reference.md) |
| 绘图指南 | [references/plotting_guide.md](references/plotting_guide.md) |
| 预处理 | [references/PREPROCESSING.md](references/PREPROCESSING.md) |
| Spike sorting | [references/SPIKE_SORTING.md](references/SPIKE_SORTING.md) |
| 运动校正 | [references/MOTION_CORRECTION.md](references/MOTION_CORRECTION.md) |
| 质量指标 | [references/QUALITY_METRICS.md](references/QUALITY_METRICS.md) |
| 自动化及基于模型的筛选 | [references/AUTOMATED_CURATION.md](references/AUTOMATED_CURATION.md) |
| AI辅助筛选 | [references/AI_CURATION.md](references/AI_CURATION.md) |
| 波形分析 | [references/ANALYSIS.md](references/ANALYSIS.md) |

## 安装

需要 Python ≥ 3.10。推荐使用 [uv](https://docs.astral.sh/uv/)。

```bash
# 核心包(SpikeInterface 内置了筛选/模型相关工具)
uv pip install "spikeinterface[full]" probeinterface neo

# Spike sorters
uv pip install kilosort          # Kilosort4(需要 CUDA GPU)
uv pip install spykingcircus     # SpykingCircus(旧版；SpykingCircus2 已内置于 SpikeInterface)
uv pip install mountainsort5     # Mountainsort5(CPU)

# 基于模型的筛选(UnitRefine)从 Hugging Face 下载
uv pip install "huggingface_hub" skops

# 可选：AI 辅助可视化筛选
uv pip install anthropic

# 可选：IBL 工具和 Bombcell
uv pip install ibl-neuropixel ibllib bombcell
```

为了保证可复现的环境,请固定版本(截至 2026-06 的当前版本：`spikeinterface==0.104.3`、
`kilosort==4.1.7`、`probeinterface==0.3.2`、`neo==0.14.4`)。不固定版本适合快速实验,但在生产管道中应固定版本。

## 项目结构

```
project/
├── raw_data/
│   └── recording_g0/
│       └── recording_g0_imec0/
│           ├── recording_g0_t0.imec0.ap.bin
│           └── recording_g0_t0.imec0.ap.meta
├── preprocessed/           # 保存的预处理记录
├── motion/                 # 运动估计结果
├── sorting_output/         # Spike sorter输出
├── analyzer/               # SortingAnalyzer(波形、指标)
├── phy_export/             # 用于手动筛选
├── ai_curation/            # AI分析报告
└── results/
    ├── quality_metrics.csv
    ├── curation_labels.json
    └── output.nwb
```

## 其他资源

- **SpikeInterface文档**: https://spikeinterface.readthedocs.io/
- **Neuropixels教程**: https://spikeinterface.readthedocs.io/en/stable/how_to/analyze_neuropixels.html
- **基于模型的筛选教程**: https://spikeinterface.readthedocs.io/en/stable/tutorials/curation/plot_1_automated_curation.html
- **UnitRefine 模型(Hugging Face)**: https://huggingface.co/SpikeInterface
- **Kilosort4 GitHub**: https://github.com/MouseLand/Kilosort
- **IBL Neuropixel工具**: https://github.com/int-brain-lab/ibl-neuropixel
- **Allen研究所ecephys**: https://github.com/AllenInstitute/ecephys_spike_sorting
- **Bombcell(自动QC)**: https://github.com/Julie-Fabre/bombcell
- **Awesome Neuropixels**: https://github.com/Julie-Fabre/awesome_neuropixels
