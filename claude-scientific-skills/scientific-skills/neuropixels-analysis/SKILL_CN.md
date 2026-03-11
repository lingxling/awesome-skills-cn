---
name: neuropixels-analysis
description: Neuropixels神经记录分析。加载SpikeGLX/OpenEphys数据、预处理、运动校正、Kilosort4 spike sorting、质量指标、Allen/IBL筛选、AI辅助视觉分析,用于Neuropixels 1.0/2.0细胞外电生理。当处理神经记录、spike sorting、细胞外电生理,或用户提到Neuropixels、SpikeGLX、Open Ephys、Kilosort、质量指标或单位筛选时使用。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Neuropixels数据分析

## 概述

用于分析Neuropixels高密度神经记录的综合工具包,采用SpikeInterface、Allen研究所和国际脑实验室(IBL)的最新最佳实践。支持从原始数据到可发表筛选单位的完整工作流程。

## 何时使用此技能

在以下情况下应使用此技能:
- 处理Neuropixels记录(.ap.bin, .lf.bin, .meta文件)
- 从SpikeGLX、Open Ephys或NWB格式加载数据
- 预处理神经记录(滤波、CAR、坏通道检测)
- 检测和校正记录中的运动/漂移
- 运行spike sorting(Kilosort4、SpykingCircus2、Mountainsort5)
- 计算质量指标(SNR、ISI违规、存在率)
- 使用Allen/IBL标准筛选单位
- 创建神经数据的可视化
- 将结果导出到Phy或NWB

## 支持的硬件和格式

| 探针 | 电极 | 通道 | 备注 |
|-------|-----------|----------|-------|
| Neuropixels 1.0 | 960 | 384 | 需要phase_shift校正 |
| Neuropixels 2.0 (单探针) | 1280 | 384 | 更密集的几何结构 |
| Neuropixels 2.0 (4-shank) | 5120 | 384 | 多区域记录 |

| 格式 | 扩展名 | 读取器 |
|--------|-----------|--------|
| SpikeGLX | `.ap.bin`, `.lf.bin`, `.meta` | `si.read_spikeglx()` |
| Open Ephys | `.continuous`, `.oebin` | `si.read_openephys()` |
| NWB | `.nwb` | `si.read_nwb()` |

## 快速开始

### 基本导入和设置

```python
import spikeinterface.full as si
import neuropixels_analysis as npa

# 配置并行处理
job_kwargs = dict(n_jobs=-1, chunk_duration='1s', progress_bar=True)
```

### 加载数据

```python
# SpikeGLX(最常见)
recording = si.read_spikeglx('/path/to/data', stream_id='imec0.ap')

# Open Ephys(许多实验室常用)
recording = si.read_openephys('/path/to/Record_Node_101/')

# 检查可用流
streams, ids = si.get_neo_streams('spikeglx', '/path/to/data')
print(streams)  # ['imec0.ap', 'imec0.lf', 'nidq']

# 使用数据子集进行测试
recording = recording.frame_slice(0, int(60 * recording.get_sampling_frequency()))
```

### 完整管道(一条命令)

```python
# 运行完整分析管道
results = npa.run_pipeline(
    recording,
    output_dir='output/',
    sorter='kilosort4',
    curation_method='allen',
)

# 访问结果
sorting = results['sorting']
metrics = results['metrics']
labels = results['labels']
```

## 标准分析工作流程

### 1. 预处理

```python
# 推荐的预处理链
rec = si.highpass_filter(recording, freq_min=400)
rec = si.phase_shift(rec)  # Neuropixels 1.0必需
bad_ids, _ = si.detect_bad_channels(rec)
rec = rec.remove_channels(bad_ids)
rec = si.common_reference(rec, operator='median')

# 或使用我们的包装器
rec = npa.preprocess(recording)
```

### 2. 检查和校正漂移

```python
# 检查漂移(始终执行此操作!)
motion_info = npa.estimate_motion(rec, preset='kilosort_like')
npa.plot_drift(rec, motion_info, output='drift_map.png')

# 如需要则应用校正
if motion_info['motion'].max() > 10:  # 微米
    rec = npa.correct_motion(rec, preset='nonrigid_accurate')
```

### 3. Spike Sorting

```python
# Kilosort4(推荐,需要GPU)
sorting = si.run_sorter('kilosort4', rec, folder='ks4_output')

# CPU替代方案
sorting = si.run_sorter('tridesclous2', rec, folder='tdc2_output')
sorting = si.run_sorter('spykingcircus2', rec, folder='sc2_output')
sorting = si.run_sorter('mountainsort5', rec, folder='ms5_output')

# 检查可用的sorter
print(si.installed_sorters())
```

### 4. 后处理

```python
# 创建分析器并计算所有扩展
analyzer = si.create_sorting_analyzer(sorting, rec, sparse=True)

analyzer.compute('random_spikes', max_spikes_per_unit=500)
analyzer.compute('waveforms', ms_before=1.0, ms_after=2.0)
analyzer.compute('templates', operators=['average', 'std'])
analyzer.compute('spike_amplitudes')
analyzer.compute('correlograms', window_ms=50.0, bin_ms=1.0)
analyzer.compute('unit_locations', method='monopolar_triangulation')
analyzer.compute('quality_metrics')

metrics = analyzer.get_extension('quality_metrics').get_data()
```

### 5. 筛选

```python
# Allen研究所标准(保守)
good_units = metrics.query("""
    presence_ratio > 0.9 and
    isi_violations_ratio < 0.5 and
    amplitude_cutoff < 0.1
""").index.tolist()

# 或使用自动筛选
labels = npa.curate(metrics, method='allen')  # 'allen', 'ibl', 'strict'
```

### 6. AI辅助筛选(用于不确定的单位)

当在Claude Code中使用此技能时,Claude可以直接分析波形图并提供专家筛选决策。对于编程API访问:

```python
from anthropic import Anthropic

# 设置API客户端
client = Anthropic()

# 视觉分析不确定的单位
uncertain = metrics.query('snr > 3 and snr < 8').index.tolist()

for unit_id in uncertain:
    result = npa.analyze_unit_visually(analyzer, unit_id, api_client=client)
    print(f"Unit {unit_id}: {result['classification']}")
    print(f"  Reasoning: {result['reasoning'][:100]}...")
```

**Claude Code集成**: 在Claude Code中运行时,要求Claude直接检查波形/相关图 - 无需API设置。

### 7. 生成分析报告

```python
# 生成包含可视化的综合HTML报告
report_dir = npa.generate_analysis_report(results, 'output/')
# 打开report.html,包含摘要统计、图表和单位表

# 将格式化摘要打印到控制台
npa.print_analysis_summary(results)
```

### 8. 导出结果

```python
# 导出到Phy以进行手动审查
si.export_to_phy(analyzer, output_folder='phy_export/',
                 compute_pc_features=True, compute_amplitudes=True)

# 导出到NWB
from spikeinterface.exporters import export_to_nwb
export_to_nwb(rec, sorting, 'output.nwb')

# 保存质量指标
metrics.to_csv('quality_metrics.csv')
```

## 常见陷阱和最佳实践

1. **始终检查漂移**在spike sorting之前 - 漂移 > 10μm显著影响质量
2. **使用phase_shift**用于Neuropixels 1.0探针(2.0不需要)
3. **保存预处理数据**以避免重新计算 - 使用`rec.save(folder='preprocessed/')`
4. **使用GPU**进行Kilosort4 - 它比CPU替代方案快10-50倍
5. **手动审查不确定的单位** - 自动筛选是一个起点
6. **将指标与AI结合** - 对明确情况使用指标,对边界单位使用AI
7. **记录您的阈值** - 不同的分析可能需要不同的标准
8. **导出到Phy**用于关键实验 - 人工监督很有价值

## 需要调整的关键参数

### 预处理
- `freq_min`: 高通截止频率(300-400 Hz典型)
- `detect_threshold`: 坏通道检测灵敏度

### 运动校正
- `preset`: 'kilosort_like'(快速)或'nonrigid_accurate'(更适合严重漂移)

### Spike Sorting(Kilosort4)
- `batch_size`: 每批样本数(30000默认)
- `nblocks`: 漂移块数(长记录增加)
- `Th_learned`: 检测阈值(越低=更多spikes)

### 质量指标
- `snr_threshold`: 信噪比截止(3-5典型)
- `isi_violations_ratio`: 不应期违规(0.01-0.5)
- `presence_ratio`: 记录覆盖率(0.5-0.95)

## 打包资源

### scripts/preprocess_recording.py
自动预处理脚本:
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

### assets/analysis_template.py
完整分析模板。复制并自定义:
```bash
cp assets/analysis_template.py my_analysis.py
# 编辑参数并运行
python my_analysis.py
```

### reference/standard_workflow.md
详细的逐步工作流程,每个阶段都有解释。

### reference/api_reference.md
按模块组织的快速函数参考。

### reference/plotting_guide.md
用于出版质量图表的综合可视化指南。

## 详细参考指南

| 主题 | 参考 |
|-------|-----------|
| 完整工作流程 | [references/standard_workflow.md](reference/standard_workflow.md) |
| API参考 | [references/api_reference.md](reference/api_reference.md) |
| 绘图指南 | [references/plotting_guide.md](reference/plotting_guide.md) |
| 预处理 | [references/PREPROCESSING.md](reference/PREPROCESSING.md) |
| Spike sorting | [references/SPIKE_SORTING.md](reference/SPIKE_SORTING.md) |
| 运动校正 | [references/MOTION_CORRECTION.md](reference/MOTION_CORRECTION.md) |
| 质量指标 | [references/QUALITY_METRICS.md](reference/QUALITY_METRICS.md) |
| 自动筛选 | [references/AUTOMATED_CURATION.md](reference/AUTOMATED_CURATION.md) |
| AI辅助筛选 | [references/AI_CURATION.md](reference/AI_CURATION.md) |
| 波形分析 | [references/ANALYSIS.md](reference/ANALYSIS.md) |

## 安装

```bash
# 核心包
pip install spikeinterface[full] probeinterface neo

# Spike sorters
pip install kilosort          # Kilosort4(需要GPU)
pip install spykingcircus     # SpykingCircus2(CPU)
pip install mountainsort5     # Mountainsort5(CPU)

# 我们的工具包
pip install neuropixels-analysis

# 可选: AI筛选
pip install anthropic

# 可选: IBL工具
pip install ibl-neuropixel ibllib
```

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
- **Kilosort4 GitHub**: https://github.com/MouseLand/Kilosort
- **IBL Neuropixel工具**: https://github.com/int-brain-lab/ibl-neuropixel
- **Allen研究所ecephys**: https://github.com/AllenInstitute/ecephys_spike_sorting
- **Bombcell(自动QC)**: https://github.com/Julie-Fabre/bombcell
- **SpikeAgent(AI筛选)**: https://github.com/SpikeAgent/SpikeAgent
