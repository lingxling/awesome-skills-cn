---
name: matchms
description: 用于质谱数据处理的Python库。提供光谱匹配、光谱相似性计算、光谱预处理、光谱聚类和质谱数据分析功能。支持多种质谱格式，包括mzML、mzXML、mgf等。适用于代谢组学、蛋白质组学和质谱数据分析。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# Matchms

## 概述

Matchms是用于质谱数据处理的Python库。它提供了光谱匹配、光谱相似性计算、光谱预处理、光谱聚类和质谱数据分析功能。该库支持多种质谱格式，包括mzML、mzXML、mgf等，适用于代谢组学、蛋白质组学和质谱数据分析。

## 核心能力

### 1. 光谱匹配

- **精确质量匹配**：基于精确质量的光谱匹配
- **光谱相似性**：计算光谱相似性分数
- **数据库搜索**：在数据库中搜索匹配的光谱
- **候选排名**：对候选光谱进行排名

### 2. 光谱相似性计算

- **余弦相似性**：计算光谱的余弦相似性
- **修改后的余弦相似性**：考虑质量偏移的余弦相似性
- **Jaccard相似性**：计算光谱的Jaccard相似性
- **Dice相似性**：计算光谱的Dice相似性
- **其他相似性度量**：其他光谱相似性度量

### 3. 光谱预处理

- **归一化**：光谱强度归一化
- **峰值过滤**：过滤低强度峰值
- **质量过滤**：过滤特定质量范围的峰值
- **去噪**：光谱去噪
- **基线校正**：光谱基线校正

### 4. 光谱聚类

- **层次聚类**：层次聚类算法
- **K-means聚类**：K-means聚类算法
- **DBSCAN聚类**：DBSCAN聚类算法
- **光谱聚类**：基于相似性的光谱聚类

### 5. 质谱数据分析

- **光谱导入**：导入质谱数据
- **光谱导出**：导出质谱数据
- **光谱可视化**：可视化质谱数据
- **统计分析**：质谱数据统计分析

## 何时使用此技能

在以下情况下使用此技能：
- 进行质谱数据预处理
- 计算光谱相似性
- 进行光谱匹配
- 进行光谱聚类
- 分析质谱数据
- 进行代谢组学分析
- 进行蛋白质组学分析

## 安装

```bash
pip install matchms
```

## 使用示例

### 光谱相似性计算

```python
from matchms import Spectrum
from matchms.similarity import CosineGreedy

# 创建光谱
spectrum1 = Spectrum(mz=[100, 150, 200], intensities=[0.5, 1.0, 0.7])
spectrum2 = Spectrum(mz=[100, 150, 200], intensities=[0.6, 0.9, 0.8])

# 计算余弦相似性
cosine = CosineGreedy()
score = cosine(spectrum1, spectrum2)

print(f"余弦相似性: {score}")
```

### 光谱预处理

```python
from matchms import Spectrum
from matchms.filtering import normalize_intensities, select_by_intensity

# 创建光谱
spectrum = Spectrum(mz=[100, 150, 200, 250], intensities=[0.1, 0.5, 1.0, 0.3])

# 归一化强度
spectrum = normalize_intensities(spectrum)

# 选择高强度峰值
spectrum = select_by_intensity(spectrum, intensity_from=0.3)

print(f"归一化后的m/z: {spectrum.mz}")
print(f"归一化后的强度: {spectrum.intensities}")
```

### 光谱匹配

```python
from matchms import Spectrum
from matchms.similarity import CosineGreedy
from matchms.importing import load_from_mgf

# 加载光谱库
spectra = list(load_from_mgf("spectra.mgf"))

# 查询光谱
query = Spectrum(mz=[100, 150, 200], intensities=[0.5, 1.0, 0.7])

# 计算相似性
cosine = CosineGreedy()
scores = [cosine(query, spectrum) for spectrum in spectra]

# 排名
ranked = sorted(zip(spectra, scores), key=lambda x: x[1], reverse=True)

# 显示前5个匹配
for i, (spectrum, score) in enumerate(ranked[:5]):
    print(f"排名 {i+1}: 相似性 {score}")
```

### 光谱聚类

```python
from matchms import Spectrum
from matchms.similarity import CosineGreedy
from sklearn.cluster import DBSCAN

# 加载光谱
spectra = list(load_from_mgf("spectra.mgf"))

# 计算相似性矩阵
cosine = CosineGreedy()
n = len(spectra)
similarity_matrix = [[0]*n for _ in range(n)]

for i in range(n):
    for j in range(i+1, n):
        score = cosine(spectra[i], spectra[j])
        similarity_matrix[i][j] = score
        similarity_matrix[j][i] = score

# 转换为距离矩阵
distance_matrix = [[1-score for score in row] for row in similarity_matrix]

# 聚类
clustering = DBSCAN(eps=0.5, min_samples=2).fit(distance_matrix)
labels = clustering.labels_

print(f"聚类标签: {labels}")
```

### 光谱导入和导出

```python
from matchms.importing import load_from_mgf, load_from_mzml
from matchms.exporting import save_as_mgf

# 从mgf文件加载
spectra = list(load_from_mgf("input.mgf"))

# 从mzML文件加载
spectra = list(load_from_mzml("input.mzml"))

# 保存为mgf文件
save_as_mgf(spectra, "output.mgf")
```

## 支持的格式

### 输入格式
- **mgf**：Mascot通用格式
- **mzML**：质谱标记语言
- **mzXML**：质谱XML格式
- **其他格式**：其他质谱格式

### 输出格式
- **mgf**：Mascot通用格式
- **mzML**：质谱标记语言
- **其他格式**：其他质谱格式

## 最佳实践

1. **光谱预处理**：在进行相似性计算之前进行适当的光谱预处理
2. **相似性度量选择**：选择合适的相似性度量
3. **参数调整**：调整相似性度量的参数以获得最佳结果
4. **质量控制**：进行质量控制以确保数据质量
5. **批量处理**：使用批量处理提高效率
6. **并行计算**：使用并行计算加速处理

## 常见问题

**Q: 如何选择合适的相似性度量？**
A: 根据数据类型和分析目标选择合适的相似性度量。

**Q: 如何处理大型质谱数据集？**
A: 使用批量处理、并行计算或分布式计算。

**Q: 如何提高光谱匹配的准确性？**
A: 进行适当的光谱预处理、调整参数、使用多个相似性度量。

**Q: Matchms支持哪些质谱格式？**
A: 支持mgf、mzML、mzXML等多种格式。

## 资源

- **Matchms文档**：https://matchms.readthedocs.io
- **Matchms GitHub**：https://github.com/matchms/matchms
- **Matchms教程**：https://matchms.readthedocs.io/en/latest/tutorials.html
