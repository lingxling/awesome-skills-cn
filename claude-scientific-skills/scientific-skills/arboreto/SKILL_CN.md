---
name: arboreto
description: 使用可扩展算法（GRNBoost2、GENIE3）从基因表达数据推断基因调控网络（GRN）。在分析转录组数据（bulk RNA-seq、单细胞RNA-seq）以识别转录因子-靶基因关系和调控相互作用时使用。支持大规模数据集的分布式计算。
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
---

# Arboreto

## 概述

Arboreto是一个计算库，用于使用并行化算法从基因表达数据推断基因调控网络（GRN），该算法可从单机扩展到多节点集群。

**核心能力**：根据跨观测（细胞、样本、条件）的表达模式，识别哪些转录因子（TF）调控哪些靶基因。

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
python scripts/basic_grn_inference.py expression_data.tsv output_network.tsv --tf-file tfs.txt --seed 777
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

**依赖项**：scipy、scikit-learn、numpy、pandas、dask、distributed

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
- 每个靶基因的前 N 个链接
- 重要性阈值（例如，> 0.5）
- 统计显著性检验（置换检验）

## 与 pySCENIC 集成

Arboreto 是 SCENIC 流程的核心组件，用于单细胞调控网络分析：

```python
# 步骤 1：使用 arboreto 进行 GRN 推断
from arboreto.algo import grnboost2
network = grnboost2(expression_data=sc_data, tf_names=tf_list)

# 步骤 2：使用 pySCENIC 进行调控因子识别和活性评分
# （下游分析请参阅 pySCENIC 文档）
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

    # 组合网络并过滤共识链接
    consensus = analyze_consensus(networks)
```

## 故障排除

**内存错误**：通过过滤低方差基因减少数据集大小，或使用分布式计算

**性能缓慢**：使用 GRNBoost2 代替 GENIE3，启用分布式客户端，过滤 TF 列表

**Dask 错误**：确保脚本中存在 `if __name__ == '__main__':` 保护

**空结果**：检查数据格式（基因作为列），验证 TF 名称与基因名称匹配
