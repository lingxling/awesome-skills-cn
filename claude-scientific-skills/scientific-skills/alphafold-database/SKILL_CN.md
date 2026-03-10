---
name: alphafold-database
description: 访问 AlphaFold 2 亿多个 AI 预测的蛋白质结构。通过 UniProt ID 检索结构，下载 PDB/mmCIF 文件，分析置信度指标（pLDDT、PAE），用于药物发现和结构生物学。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# AlphaFold 数据库

## 概述

AlphaFold DB 是由 DeepMind 和 EMBL-EBI 维护的超过 2 亿个蛋白质的 AI 预测 3D 蛋白质结构的公共存储库。访问具有置信度指标的结构预测，下载坐标文件，检索批量数据集，并将预测集成到计算工作流程中。

## 何时使用此技能

在以下场景中使用此技能处理 AI 预测的蛋白质结构：

- 通过 UniProt ID 或蛋白质名称检索蛋白质结构预测
- 下载 PDB/mmCIF 坐标文件进行结构分析
- 分析预测置信度指标（pLDDT、PAE）以评估可靠性
- 通过 Google Cloud Platform 访问批量蛋白质组数据集
- 将预测结构与实验数据进行比较
- 执行基于结构的药物发现或蛋白质工程
- 为缺乏实验结构的蛋白质构建结构模型
- 将 AlphaFold 预测集成到计算流水线中

## 核心功能

### 1. 搜索和检索预测

**使用 Biopython（推荐）：**

Biopython 库提供了检索 AlphaFold 结构的最简单接口：

```python
from Bio.PDB import alphafold_db

# 获取 UniProt 登录号的所有预测
predictions = list(alphafold_db.get_predictions("P00520"))

# 下载结构文件（mmCIF 格式）
for prediction in predictions:
    cif_file = alphafold_db.download_cif_for(prediction, directory="./structures")
    print(f"已下载: {cif_file}")

# 直接获取 Structure 对象
from Bio.PDB import MMCIFParser
structures = list(alphafold_db.get_structural_models_for("P00520"))
```

**直接 API 访问：**

使用 REST 端点查询预测：

```python
import requests

# 获取 UniProt 登录号的预测元数据
uniprot_id = "P00520"
api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
response = requests.get(api_url)
prediction_data = response.json()

# 提取 AlphaFold ID
alphafold_id = prediction_data[0]['entryId']
print(f"AlphaFold ID: {alphafold_id}")
```

**使用 UniProt 查找登录号：**

首先搜索 UniProt 以查找蛋白质登录号：

```python
import urllib.parse, urllib.request

def get_uniprot_ids(query, query_type='PDB_ID'):
    """查询 UniProt 以获取登录号 ID"""
    url = 'https://www.uniprot.org/uploadlists/'
    params = {
        'from': query_type,
        'to': 'ACC',
        'format': 'txt',
        'query': query
    }
    data = urllib.parse.urlencode(params).encode('ascii')
    with urllib.request.urlopen(urllib.request.Request(url, data)) as response:
        return response.read().decode('utf-8').splitlines()

# 示例：查找蛋白质名称的 UniProt ID
protein_ids = get_uniprot_ids("hemoglobin", query_type="GENE_NAME")
```

### 2. 下载结构文件

AlphaFold 为每个预测提供多种文件格式：

**可用的文件类型：**

- **模型坐标** (`model_v4.cif`)：mmCIF/PDBx 格式的原子坐标
- **置信度分数** (`confidence_v4.json`)：每个残基的 pLDDT 分数（0-100）
- **预测对齐误差** (`predicted_aligned_error_v4.json`)：残基对置信度的 PAE 矩阵

**下载 URL：**

```python
import requests

alphafold_id = "AF-P00520-F1"
version = "v4"

# 模型坐标（mmCIF）
model_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{version}.cif"
response = requests.get(model_url)
with open(f"{alphafold_id}.cif", "w") as f:
    f.write(response.text)

# 置信度分数（JSON）
confidence_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_{version}.json"
response = requests.get(confidence_url)
confidence_data = response.json()

# 预测对齐误差（JSON）
pae_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-predicted_aligned_error_{version}.json"
response = requests.get(pae_url)
pae_data = response.json()
```

**PDB 格式（替代方案）：**

```python
# 下载为 PDB 格式而不是 mmCIF
pdb_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-model_{version}.pdb"
response = requests.get(pdb_url)
with open(f"{alphafold_id}.pdb", "wb") as f:
    f.write(response.content)
```

### 3. 使用置信度指标

AlphaFold 预测包括对解释至关重要的置信度估计：

**pLDDT（每个残基的置信度）：**

```python
import json
import requests

# 加载置信度分数
alphafold_id = "AF-P00520-F1"
confidence_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_v4.json"
confidence = requests.get(confidence_url).json()

# 提取 pLDDT 分数
plddt_scores = confidence['confidenceScore']

# 解释置信度水平
# pLDDT > 90: 非常高置信度
# pLDDT 70-90: 高置信度
# pLDDT 50-70: 低置信度
# pLDDT < 50: 非常低置信度

high_confidence_residues = [i for i, score in enumerate(plddt_scores) if score > 90]
print(f"高置信度残基: {len(high_confidence_residues)}/{len(plddt_scores)}")
```

**PAE（预测对齐误差）：**

PAE 表示对残基对之间相对位置的置信度：

```python
import numpy as np
import matplotlib.pyplot as plt

# 加载 PAE 矩阵
pae_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-predicted_aligned_error_{version}.json"
pae = requests.get(pae_url).json()

# 可视化 PAE 矩阵
pae_matrix = np.array(pae['distance'])
plt.figure(figsize=(10, 8))
plt.imshow(pae_matrix, cmap='viridis_r', vmin=0, vmax=30)
plt.colorbar(label='PAE (Å)')
plt.title(f'预测对齐误差: {alphafold_id}')
plt.xlabel('残基')
plt.ylabel('残基')
plt.savefig(f'{alphafold_id}_pae.png', dpi=300, bbox_inches='tight')

# 低 PAE 值（<5 Å）表示可信的相对定位
# 高 PAE 值（>15 Å）表明不确定的域排列
```

### 4. 通过 Google Cloud 进行批量数据访问

对于大规模分析，使用 Google Cloud 数据集：

**Google Cloud Storage：**

```bash
# 安装 gsutil
uv pip install gsutil

# 列出可用数据
gsutil ls gs://public-datasets-deepmind-alphafold-v4/

# 下载整个蛋白质组（按分类学 ID）
gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-9606-*.tar .

# 下载特定文件
gsutil cp gs://public-datasets-deepmind-alphafold-v4/accession_ids.csv .
```

**BigQuery 元数据访问：**

```python
from google.cloud import bigquery

# 初始化客户端
client = bigquery.Client()

# 查询元数据
query = """
SELECT
  entryId,
  uniprotAccession,
  organismScientificName,
  globalMetricValue,
  fractionPlddtVeryHigh
FROM `bigquery-public-data.deepmind_alphafold.metadata`
WHERE organismScientificName = 'Homo sapiens'
  AND fractionPlddtVeryHigh > 0.8
LIMIT 100
"""

results = client.query(query).to_dataframe()
print(f"找到 {len(results)} 个高置信度的人类蛋白质")
```

**按物种下载：**

> ⚠️ **安全说明**：下面的示例使用 `shell=True` 是为了简单起见。在生产环境中，首选使用 `subprocess.run()` 和参数列表来防止命令注入漏洞。请参阅 [Python subprocess 安全性](https://docs.python.org/3/library/subprocess.html#security-considerations)。

```python
import subprocess
import shlex

def download_proteome(taxonomy_id, output_dir="./proteomes"):
    """下载物种的所有 AlphaFold 预测"""
    # 验证 taxonomy_id 是整数以防止注入
    if not isinstance(taxonomy_id, int):
        raise ValueError("taxonomy_id 必须是整数")

    pattern = f"gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-{taxonomy_id}-*_v4.tar"
    # 使用列表形式而不是 shell=True 以确保安全
    subprocess.run(["gsutil", "-m", "cp", pattern, f"{output_dir}/"], check=True)

# 下载 E. coli 蛋白质组（分类学 ID: 83333）
download_proteome(83333)

# 下载人类蛋白质组（分类学 ID: 9606）
download_proteome(9606)
```

### 5. 解析和分析结构

使用 BioPython 处理下载的 AlphaFold 结构：

```python
from Bio.PDB import MMCIFParser, PDBIO
import numpy as np

# 解析 mmCIF 文件
parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v4.cif")

# 提取坐标
coords = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:  # 仅 Alpha 碳
                coords.append(residue['CA'].get_coord())

coords = np.array(coords)
print(f"结构有 {len(coords)} 个残基")

# 计算距离
from scipy.spatial.distance import pdist, squareform
distance_matrix = squareform(pdist(coords))

# 识别接触（< 8 Å）
contacts = np.where((distance_matrix > 0) & (distance_matrix < 8))
print(f"接触数: {len(contacts[0]) // 2}")
```

**提取 B 因子（pLDDT 值）：**

AlphaFold 将 pLDDT 分数存储在 B 因子列中：

```python
from Bio.PDB import MMCIFParser

parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v4.cif")

# 从 B 因子中提取 pLDDT
plddt_scores = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:
                plddt_scores.append(residue['CA'].get_bfactor())

# 识别高置信度区域
high_conf_regions = [(i, score) for i, score in enumerate(plddt_scores, 1) if score > 90]
print(f"高置信度残基: {len(high_conf_regions)}")
```

### 6. 批量处理多个蛋白质

高效处理多个预测：

```python
from Bio.PDB import alphafold_db
import pandas as pd

uniprot_ids = ["P00520", "P12931", "P04637"]  # 多个蛋白质
results = []

for uniprot_id in uniprot_ids:
    try:
        # 获取预测
        predictions = list(alphafold_db.get_predictions(uniprot_id))

        if predictions:
            pred = predictions[0]

            # 下载结构
            cif_file = alphafold_db.download_cif_for(pred, directory="./batch_structures")

            # 获取置信度数据
            alphafold_id = pred['entryId']
            conf_url = f"https://alphafold.ebi.ac.uk/files/{alphafold_id}-confidence_v4.json"
            conf_data = requests.get(conf_url).json()

            # 计算统计信息
            plddt_scores = conf_data['confidenceScore']
            avg_plddt = np.mean(plddt_scores)
            high_conf_fraction = sum(1 for s in plddt_scores if s > 90) / len(plddt_scores)

            results.append({
                'uniprot_id': uniprot_id,
                'alphafold_id': alphafold_id,
                'avg_plddt': avg_plddt,
                'high_conf_fraction': high_conf_fraction,
                'length': len(plddt_scores)
            })
    except Exception as e:
        print(f"处理 {uniprot_id} 时出错: {e}")

# 创建摘要 DataFrame
df = pd.DataFrame(results)
print(df)
```

## 安装和设置

### Python 库

```bash
# 安装 Biopython 用于结构访问
uv pip install biopython

# 安装 requests 用于 API 访问
uv pip install requests

# 用于可视化和分析
uv pip install numpy matplotlib pandas scipy

# 用于 Google Cloud 访问（可选）
uv pip install google-cloud-bigquery gsutil
```

### 3D-Beacons API 替代方案

AlphaFold 也可以通过 3D-Beacons 联合 API 访问：

```python
import requests

# 通过 3D-Beacons 查询
uniprot_id = "P00520"
url = f"https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{uniprot_id}.json"
response = requests.get(url)
data = response.json()

# 筛选 AlphaFold 结构
af_structures = [s for s in data['structures'] if s['provider'] == 'AlphaFold DB']
```

## 常见用例

### 结构蛋白质组学
- 下载完整的蛋白质组预测进行分析
- 识别蛋白质中的高置信度结构区域
- 将预测结构与实验数据进行比较
- 为蛋白质家族构建结构模型

### 药物发现
- 检索靶蛋白结构用于对接研究
- 分析结合位点构象
- 在预测结构中识别可药物口袋
- 比较同源物之间的结构

### 蛋白质工程
- 使用 pLDDT 识别稳定/不稳定区域
- 在高置信度区域设计突变
- 使用 PAE 分析域架构
- 建模蛋白质变体和突变

### 进化研究
- 比较物种之间的直系同源结构
- 分析结构特征的保守性
- 研究域进化模式
- 识别功能重要区域

## 关键概念

**UniProt 登录号**：蛋白质的主要标识符（例如，"P00520"）。查询 AlphaFold DB 时需要。

**AlphaFold ID**：内部标识符格式：`AF-[UniProt 登录号]-F[片段号]`（例如，"AF-P00520-F1"）。

**pLDDT（预测局部距离差异测试）**：每个残基的置信度度量（0-100）。较高的值表示更可信的预测。

**PAE（预测对齐误差）**：表示残基对之间相对位置置信度的矩阵。低值（<5 Å）表明可信的相对定位。

**数据库版本**：当前版本是 v4。文件 URL 包括版本后缀（例如，`model_v4.cif`）。

**片段号**：大蛋白质可能被分成多个片段。片段号出现在 AlphaFold ID 中（例如，F1、F2）。

## 置信度解释指南

**pLDDT 阈值：**
- **>90**：非常高置信度 - 适合详细分析
- **70-90**：高置信度 - 通常可靠的主链结构
- **50-70**：低置信度 - 谨慎使用，柔性区域
- **<50**：非常低置信度 - 可能无序或不可靠

**PAE 指南：**
- **<5 Å**：域的可信相对定位
- **5-10 Å**：排列的中等置信度
- **>15 Å**：不确定的相对位置，域可能是可移动的

## 资源

### references/api_reference.md

全面的 API 文档，涵盖：
- 完整的 REST API 端点规范
- 文件格式详细信息和数据架构
- Google Cloud 数据集结构和访问模式
- 高级查询示例和批处理策略
- 速率限制、缓存和最佳实践
- 常见问题故障排除

有关详细的 API 信息、批量下载策略或处理大型数据集时，请参阅此参考。

## 重要说明

### 数据使用和归属

- AlphaFold DB 在 CC-BY-4.0 许可下免费提供
- 引用：Jumper et al. (2021) Nature 和 Varadi et al. (2022) Nucleic Acids Research
- 预测是计算模型，不是实验结构
- 在下游分析之前始终评估置信度指标

### 版本管理

- 当前数据库版本：v4（截至 2024-2025 年）
- 文件 URL 包括版本后缀（例如，`_v4.cif`）
- 定期检查数据库更新
- 旧版本可能会随时间被弃用

### 数据质量考虑

- 高 pLDDT 不能保证功能准确性
- 低置信度区域可能在体内无序
- PAE 表示相对域置信度，而不是绝对定位
- 预测缺少配体、翻译后修饰和辅因子
- 不预测多链复合物（仅单链）

### 性能提示

- 使用 Biopython 进行简单的单蛋白质访问
- 使用 Google Cloud 进行批量下载（比单个文件快得多）
- 在本地缓存下载的文件以避免重复下载
- BigQuery 免费层：每月处理 1 TB 数据
- 考虑大规模下载的网络带宽

## 其他资源

- **AlphaFold DB 网站**：https://alphafold.ebi.ac.uk/
- **API 文档**：https://alphafold.ebi.ac.uk/api-docs
- **Google Cloud 数据集**：https://cloud.google.com/blog/products/ai-machine-learning/alphafold-protein-structure-database
- **3D-Beacons API**：https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/
- **AlphaFold 论文**：
  - Nature (2021): https://doi.org/10.1038/s41586-021-03819-2
  - Nucleic Acids Research (2024): https://doi.org/10.1093/nar/gkad1011
- **Biopython 文档**：https://biopython.org/docs/dev/api/Bio.PDB.alphafold_db.html
- **GitHub 存储库**：https://github.com/google-deepmind/alphafold
