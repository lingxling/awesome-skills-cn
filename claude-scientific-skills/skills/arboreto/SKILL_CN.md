---
name: arboreto
description: 使用可扩展算法（GRNBoost2、GENIE3）从基因表达数据推断基因调控网络（GRNs）。当分析转录组学数据（bulk RNA-seq、单细胞RNA-seq）以识别转录因子-靶基因关系和调控相互作用时使用。支持大规模数据集的分布式计算。
license: BSD-3-Clause license
metadata:
  version: "1.0"
  skill-author: K-Dense Inc.
---






# Arboreto

## 概述

Arboreto 是来自 [Aerts Lab](https://github.com/aertslab/arboreto) 的 Python 库，用于从基因表达数据推断基因调控网络（GRN）。它使用 [Dask](https://distributed.dask.org/) 并行化树形集成回归算法（GRNBoost2、GENIE3），可在本地核心或远程集群上运行。

**核心能力**：根据跨观测（细胞、样本、条件）的表达模式，识别哪些转录因子（TF）调控哪些靶基因。

**上游**：PyPI **0.1.6** (2021-02-09, 最新)。文档：[arboreto.readthedocs.io](https://arboreto.readthedocs.io/en/latest/)。主要下游使用者：[pySCENIC](https://github.com/aertslab/pySCENIC)。

## 快速开始

安装 arboreto：
```bash
uv pip install arboreto
```

基本 GRN 推断：
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # 加载表达数据（基因作为列）
    expression_matrix = pd.read_csv('expression_data.tsv', sep='\t')

    # 推断调控网络
    network = grnboost2(expression_data=expression_matrix)

    # 保存结果（TF、target、importance）
    network.to_csv('network.tsv', sep='\t', index=False, header=False)
```

**关键**：始终使用 `if __name__ == '__main__':` 保护，因为 Dask 会生成新进程。

## 核心能力

### 1. 基本 GRN 推断

用于标准 GRN 推断工作流程，包括：
- 输入数据准备（Pandas DataFrame 或 NumPy 数组）
- 使用 GRNBoost2 或 GENIE3 运行推断
- 按转录因子过滤
- 输出格式和解释

**参见**：`references/basic_inference.md`

**使用现成脚本**：`scripts/basic_grn_inference.py` 用于标准推断任务：
```bash
python scripts/basic_grn_inference.py expression_data.tsv output_network.tsv --tf-file tfs.txt --seed 777 --limit 5000
```

### 2. 算法选择

Arboreto 提供两种算法：

**GRNBoost2（推荐）**：
- 基于快速梯度提升的推断
- 针对大型数据集（10k+ 观测）优化
- 大多数分析的默认选择

**GENIE3**：
- 基于随机森林的推断
- 原始多元回归方法
- 用于比较或验证

快速比较：
```python
from arboreto.algo import grnboost2, genie3

# 快速，推荐
network_grnboost = grnboost2(expression_data=matrix)

# 经典算法
network_genie3 = genie3(expression_data=matrix)
```

**有关详细算法比较、参数和选择指导**：`references/algorithms.md`

### 3. 分布式计算

将推断从本地多核扩展到集群环境：

**本地（默认）** - 自动使用所有可用核心：
```python
network = grnboost2(expression_data=matrix)
```

**自定义本地客户端** - 控制资源：
```python
from distributed import LocalCluster, Client

local_cluster = LocalCluster(n_workers=10, memory_limit='8GB')
client = Client(local_cluster)

network = grnboost2(expression_data=matrix, client_or_address=client)

client.close()
local_cluster.close()
```

**集群计算** - 连接到远程 Dask 调度器：
```python
from distributed import Client

client = Client('tcp://scheduler:8786')
network = grnboost2(expression_data=matrix, client_or_address=client)
```

**有关集群设置、性能优化和大规模工作流程**：`references/distributed_computing.md`

## 安装

```bash
uv pip install arboreto
```

Conda（Bioconda）：
```bash
conda install -c bioconda arboreto
```

**依赖项**（来自上游 `requirements.txt`）：`dask[complete]`、`distributed`、`numpy`、`pandas`、`scikit-learn`、`scipy`

**输入格式**：pandas DataFrame、密集 `numpy.ndarray` 或稀疏 `scipy.sparse.csc_matrix`（行 = 观测，列 = 基因）。对于数组/矩阵输入，请显式传递 `gene_names`。

## 常见用例

### 单细胞 RNA-seq 分析
```python
import pandas as pd
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # 加载单细胞表达矩阵（细胞 x 基因）
    sc_data = pd.read_csv('scrna_counts.tsv', sep='\t')

    # 推断细胞类型特异性调控网络
    network = grnboost2(expression_data=sc_data, seed=42)

    # 过滤高置信度链接
    high_confidence = network[network['importance'] > 0.5]
    high_confidence.to_csv('grn_high_confidence.tsv', sep='\t', index=False)
```

### 带 TF 过滤的 Bulk RNA-seq
```python
from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # 加载数据
    expression_data = pd.read_csv('rnaseq_tpm.tsv', sep='\t')
    tf_names = load_tf_names('human_tfs.txt')

    # 使用 TF 限制进行推断
    network = grnboost2(
        expression_data=expression_data,
        tf_names=tf_names,
        seed=123
    )

    network.to_csv('tf_target_network.tsv', sep='\t', index=False)
```

### 比较分析（多个条件）
```python
from arboreto.algo import grnboost2

if __name__ == '__main__':
    # 为不同条件推断网络
    conditions = ['control', 'treatment_24h', 'treatment_48h']

    for condition in conditions:
        data = pd.read_csv(f'{condition}_expression.tsv', sep='\t')
        network = grnboost2(expression_data=data, seed=42)
        network.to_csv(f'{condition}_network.tsv', sep='\t', index=False)
```

## 输出解释

Arboreto 返回一个包含调控链接的 DataFrame：

| 列 | 描述 |
|--------|-------------|
| `TF` | 转录因子（调控因子） |
| `target` | 靶基因 |
| `importance` | 调控重要性评分（越高 = 越强） |

**过滤策略**：
- 推断时使用 `limit=N`（全局返回前 N 个链接）
- 事后重要性阈值（例如，> 0.5）
- 通过 `groupby('target')` 获取每个靶基因的前几个链接
- 统计显著性检验（置换检验，外部工具）

## 与 pySCENIC 集成

Arboreto 为 [pySCENIC](https://github.com/aertslab/pySCENIC) 的 GRN 推断步骤提供支持。pySCENIC 0.11+ 将稀疏表达矩阵传递给 `grnboost2` / `genie3`；pySCENIC 0.12+ 默认使用 `arboreto_with_multiprocessing.py`（无 Dask）以保持兼容性 — 当需要 Dask 扩展时请使用独立版 arboreto。

```python
# 独立版：在 pySCENIC cisTarget 修剪之前推断共表达模块
from arboreto.algo import grnboost2

network = grnboost2(expression_data=expression_df, tf_names=tf_list, limit=5000)

# 下游：pySCENIC ctx 修剪、调控子定义、AUCell（参见 pySCENIC 文档）
```

将 AnnData 直接转换为 arboreto 使用的 DataFrame：

```python
expression_df = adata.to_df()  # cells x genes
```

## 可重现性

始终设置种子以获得可重现的结果：
```python
network = grnboost2(expression_data=matrix, seed=777)
```

运行多个种子进行稳健性分析：
```python
from distributed import LocalCluster, Client

if __name__ == '__main__':
    client = Client(LocalCluster())

    seeds = [42, 123, 777]
    networks = []

    for seed in seeds:
        net = grnboost2(expression_data=matrix, client_or_address=client, seed=seed)
        networks.append(net)

    # 共识：跨运行重复的链接（示例：每个 TF-靶基因对的平均重要性）
    import pandas as pd
    combined = pd.concat(networks)
    consensus = (
        combined.groupby(['TF', 'target'], as_index=False)['importance']
        .mean()
        .query('importance > 0.5')
    )
```

## 故障排除

**内存错误**：通过过滤低方差基因减少数据集大小，或使用分布式计算

**性能缓慢**：使用 GRNBoost2 代替 GENIE3，启用分布式客户端，过滤 TF 列表

**Dask 错误**：确保脚本中存在 `if __name__ == '__main__':` 保护（在具有基于 spawn 的多处理的 Windows/macOS 上需要）

**空结果**：检查数据格式（基因作为列），验证 TF 名称与表达矩阵中的列名匹配

**稀疏数据**：使用 `scipy.sparse.csc_matrix` 并传递匹配的 `gene_names`；自 arboreto 0.1.6 / pySCENIC 0.11 起支持
