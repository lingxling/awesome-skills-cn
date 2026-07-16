---
name: pyopenms
description: 完整的质谱分析平台。用于蛋白质组学和代谢组学工作流——特征检测、肽段/蛋白质鉴定、无标记与同量异位标记定量、加合物/精确质量注释，以及复杂的LC-MS/MS流程。支持广泛的文件格式和算法。对于简单的谱图比对和小分子谱库匹配，请使用matchms。
license: 3 clause BSD license
allowed-tools: Read Write Edit Bash
compatibility: Requires Python 3.9+ and uv. Examples and scripts target pyOpenMS 3.5.0.
metadata: {"version": "2.0", "skill-author": "K-Dense Inc."}
---

# PyOpenMS

## 概述

PyOpenMS 为 OpenMS 库提供 Python 绑定，用于计算质谱分析，支持蛋白质组学和代谢组学数据的分析。可用它读写质谱文件格式、处理原始谱图、检测并定量特征、鉴定肽段和蛋白质，以及运行端到端的 LC-MS/MS 流程。

**本技能在 `scripts/` 目录中提供了开箱即用的脚本**，涵盖最常见的高层工作流。优先运行脚本，而不是自己编写新代码——每个脚本都是一个带参数的命令行工具，负责加载、处理和导出。只有在没有合适脚本时，才直接使用 Python API（并参考 `references/`）。

## 安装

```bash
uv pip install pyopenms
```

验证安装（注意：`__version__` 可正常使用，但内置二进制文件在导入时会打印一行内存状态提示，这是无害的）：

```python
import pyopenms as ms
print(ms.__version__)  # 3.5.0
```

## 脚本（从这里开始）

使用 `python scripts/<name>.py --help` 查看完整选项。所有脚本都接受标准的质谱文件格式，并按需写出 featureXML/consensusXML/CSV/mzTab/PNG。

### 检查与转换
| 脚本 | 作用 |
|--------|--------------|
| `inspect_ms_data.py` | 汇总任意 mzML/mzXML/featureXML/consensusXML/idXML 文件（计数、RT/m/z 范围、TIC、元数据）；可选逐谱图 CSV 输出。 |
| `convert_format.py` | 在 mzML/mzXML/MGF 之间转换，可选按 MS 级别、RT、强度进行过滤。 |
| `process_spectra.py` | 可配置的信号处理链：平滑（Gauss/SGolay）、质心化（PeakPickerHiRes）、归一化、信噪比与强度阈值。 |

### 特征检测与定量
| 脚本 | 作用 |
|--------|--------------|
| `detect_features_metabo.py` | 非靶向代谢组学特征查找：MassTraceDetection → ElutionPeakDetection → FeatureFindingMetabo。 |
| `detect_features_centroided.py` | 通过 FeatureFinderAlgorithmPicked 进行肽段/质心化特征检测。 |
| `align_link_quantify.py` | 多样本流程：检测（或加载）特征 → RT 对齐 → 一致性链接 → 定量矩阵 CSV。 |
| `consensus_to_matrix.py` | consensusXML → 宽格式强度矩阵 + 元数据，可选中位数/分位数归一化和长格式输出。 |

### 注释
| 脚本 | 作用 |
|--------|--------------|
| `detect_adducts.py` | 将同一中性质量的加合物/电荷变体分组（MetaboliteFeatureDeconvolution）。 |
| `accurate_mass_search.py` | 基于精确质量对特征进行 HMDB 注释（AccurateMassSearchEngine → mzTab/CSV）。 |
| `export_gnps_sirius.py` | 导出 GNPS FBMN 输入（MGF + 定量表）或 SIRIUS 的 `.ms` 文件。 |

### 鉴定
| 脚本 | 作用 |
|--------|--------------|
| `process_identifications.py` | 针对 FASTA 重新建立索引、估计 FDR/q 值、进行过滤（FDR/长度/每谱图最佳匹配），导出 idXML + CSV。 |

### 化学
| 脚本 | 作用 |
|--------|--------------|
| `mass_calculator.py` | 计算肽段或化学式的单同位素/平均质量、带电荷 m/z、化学式和同位素模式。 |
| `digest_protein.py` | 对 FASTA/序列进行计算机模拟蛋白酶消化 → 生成带质量和 m/z 的理论肽段。 |
| `theoretical_spectrum.py` | 为某个肽段生成带注释的理论碎片谱图（b/y/a/c/x/z 离子系列、中性丢失）。 |

### 靶向分析与可视化
| 脚本 | 作用 |
|--------|--------------|
| `extract_chromatograms.py` | 为目标 m/z 构建 TIC/BPC 及 XIC 色谱轨迹（CSV + 可选绘图）。 |
| `plot_ms_data.py` | 快速绘图：单张谱图、TIC、二维特征图、MS1 信号图。 |

### 常用脚本示例

```bash
# 检查文件
python scripts/inspect_ms_data.py sample.mzML --spectra-csv spectra.csv

# 非靶向代谢组学：单个样本的特征
python scripts/detect_features_metabo.py sample.mzML --out-csv features.csv

# 完整的多样本定量研究
python scripts/align_link_quantify.py s1.mzML s2.mzML s3.mzML --out-prefix study
python scripts/consensus_to_matrix.py study.consensusXML --out quant.csv --normalize median

# 肽段化学计算
python scripts/mass_calculator.py --peptide "PEPTIDEM(Oxidation)K" --charges 1 2 3 --isotopes 5
python scripts/digest_protein.py proteins.fasta --enzyme Trypsin --missed 2 --out peptides.csv

# 鉴定结果后处理
python scripts/process_identifications.py search.idXML --fasta db.fasta --fdr 0.01 --out filtered.idXML --csv hits.csv
```

## 3.5.0 关键 API 变化说明

以下内容相对于旧版 OpenMS 发生了变化——旧的教程和代码在新版本上会出错：

- **特征查找**：`FeatureFinder("centroided")` 已被**移除**。请使用
  `FeatureFinderAlgorithmPicked`（蛋白质组学/质心化数据）或
  `MassTraceDetection → ElutionPeakDetection → FeatureFindingMetabo` 流程
  （代谢组学）。参见 `detect_features_*.py`。
- **idXML 读写**：`IdXMLFile().load/store` 要求肽段 ID 使用
  `ms.PeptideIdentificationList()`（使用普通 Python `list` 会抛出 "can not handle type" 错误）。蛋白质 ID 仍然使用普通 list。
- **加合物去电荷**：对应的类是 `MetaboliteFeatureDeconvolution`，加合物使用
  `Elements:Charge:Probability` 语法（例如 `H:+:0.4`、`H-2O-1:0:0.05`）——而不是
  `[M+H]+` 这种方括号写法。
- **DataFrame 列名**：`FeatureMap.get_df()` 使用小写的 `rt`/`mz`（不是 `RT`）。
  `ConsensusMap` 提供 `get_intensity_df()` 和 `get_metadata_df()`。
- **内置数据说明**：pip wheel 包中附带了 `HMDBMappingFile.tsv`，但不包含
  `HMDB2StructMapping.tsv`；`accurate_mass_search.py` 会检测到这一点，并说明如何自行提供该文件。

## 核心数据结构

- **MSExperiment** – 谱图和色谱图的集合
- **MSSpectrum / MSChromatogram** – 单张谱图 / 单条色谱轨迹
- **Feature / FeatureMap** – 检测到的 LC-MS 峰 / 特征集合
- **ConsensusMap** – 跨样本链接的特征（即定量表）
- **PeptideIdentification / ProteinIdentification** – 搜索结果
- **AASequence / EmpiricalFormula** – 序列与化学式相关计算

**详情参见**：`references/data_structures.md`。

## 参数管理

大多数算法都暴露了一个 OpenMS `Param` 对象：

```python
algo = ms.FeatureFindingMetabo()
p = algo.getDefaults()
for key in p.keys():
    print(key.decode(), "=", p.getValue(key), "|", p.getDescription(key))
p.setValue("charge_lower_bound", 1)
algo.setParameters(p)
```

## 导出到 pandas

```python
fm = ms.FeatureMap(); ms.FeatureXMLFile().load("features.featureXML", fm)
df = fm.get_df()             # 列名包括小写的 rt、mz、intensity、charge、quality

cm = ms.ConsensusMap(); ms.ConsensusXMLFile().load("study.consensusXML", cm)
intensities = cm.get_intensity_df()   # 特征 x 样本
metadata = cm.get_metadata_df()       # rt、mz、charge、quality 等
```

## 与其他工具的集成

Pandas（DataFrame）、NumPy（峰值数组）、scikit-learn（机器学习）、Matplotlib/Seaborn
（绘图），以及通过导出对接的下游工具：GNPS（FBMN）、SIRIUS 和 mzTab。

## 资源

- 官方文档（3.5.0）：https://pyopenms.readthedocs.io/en/release-3.5.0/
- OpenMS：https://www.openms.org
- GitHub：https://github.com/OpenMS/OpenMS

## 参考文档

- `references/file_io.md` – 文件格式处理
- `references/signal_processing.md` – 信号处理算法
- `references/feature_detection.md` – 特征检测与链接
- `references/identification.md` – 肽段与蛋白质鉴定
- `references/metabolomics.md` – 代谢组学专用工作流
- `references/data_structures.md` – 核心对象与数据结构
