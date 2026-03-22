---
name: cellxgene-census
description: 以编程方式查询 CELLxGENE Census(6100万+细胞)。当您需要来自最大策展单细胞图谱的组织、疾病或细胞类型的表达数据时使用。最适合人群规模查询、参考图谱比较。分析您自己的数据请使用 scanpy 或 scvi-tools。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# CZ CELLxGENE Census

## 概述

CZ CELLxGENE Census 提供对来自 CZ CELLxGENE Discover 的全面、版本化标准化单细胞基因组学数据的编程访问。此技能使您能够高效查询和分析数千个数据集中的数百万个细胞。

Census 包括:
- **6100万+细胞**,来自人类和小鼠
- **标准化元数据**(细胞类型、组织、疾病、供体)
- **原始基因表达**矩阵
- **预计算嵌入**和统计信息
- **与 PyTorch、scanpy 和其他分析工具集成**

## 何时使用此技能

在以下情况下使用此技能:
- 按细胞类型、组织或疾病查询单细胞表达数据
- 探索可用的单细胞数据集和元数据
- 在单细胞数据上训练机器学习模型
- 执行大规模跨数据集分析
- 将 Census 数据与 scanpy 或其他分析框架集成
- 计算数百万个细胞的统计信息
- 访问预计算嵌入或模型预测

## 安装和设置

安装 Census API:
```bash
uv pip install cellxgene-census
```

对于机器学习工作流程,安装额外依赖:
```bash
uv pip install cellxgene-census[experimental]
```

## 核心工作流程模式

### 1. 打开 Census

始终使用上下文管理器以确保正确的资源清理:

```python
import cellxgene_census

# 打开最新稳定版本
with cellxgene_census.open_soma() as census:
    # 使用 census 数据

# 打开特定版本以确保可重现性
with cellxgene_census.open_soma(census_version="2023-07-25") as census:
    # 使用 census 数据
```

**关键点:**
- 使用上下文管理器(`with` 语句)进行自动清理
- 指定 `census_version` 以确保可重现的分析
- 默认打开最新的"stable"版本

### 2. 探索 Census 信息

在查询表达数据之前,探索可用的数据集和元数据。

**访问摘要信息:**
```python
# 获取摘要统计信息
summary = census["census_info"]["summary"].read().concat().to_pandas()
print(f"总细胞数: {summary['total_cell_count'][0]}")

# 获取所有数据集
datasets = census["census_info"]["datasets"].read().concat().to_pandas()

# 按条件筛选数据集
covid_datasets = datasets[datasets["disease"].str.contains("COVID", na=False)]
```

**查询细胞元数据以了解可用数据:**
```python
# 获取组织中唯一的细胞类型
cell_metadata = cellxgene_census.get_obs(
    census,
    "homo_sapiens",
    value_filter="tissue_general == 'brain' and is_primary_data == True",
    column_names=["cell_type"]
)
unique_cell_types = cell_metadata["cell_type"].unique()
print(f"在脑中发现 {len(unique_cell_types)} 种细胞类型")

# 按组织统计细胞
tissue_counts = cell_metadata.groupby("tissue_general").size()
```

**重要提示:** 始终筛选 `is_primary_data == True` 以避免重复计数细胞,除非专门分析重复项。

### 3. 查询表达数据(小到中等规模)

对于返回 <10 万个细胞且适合内存的查询,使用 `get_anndata()`:

```python
# 使用细胞类型和组织筛选的基本查询
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",  # 或 "Mus musculus"
    obs_value_filter="cell_type == 'B cell' and tissue_general == 'lung' and is_primary_data == True",
    obs_column_names=["assay", "disease", "sex", "donor_id"],
)

# 使用多个筛选器查询特定基因
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19', 'FOXP3']",
    obs_value_filter="cell_type == 'T cell' and disease == 'COVID-19' and is_primary_data == True",
    obs_column_names=["cell_type", "tissue_general", "donor_id"],
)
```

**筛选语法:**
- 使用 `obs_value_filter` 进行细胞筛选
- 使用 `var_value_filter` 进行基因筛选
- 使用 `and`、`or` 组合条件
- 使用 `in` 表示多个值: `tissue in ['lung', 'liver']`
- 仅使用 `obs_column_names` 选择所需列

**单独获取元数据:**
```python
# 查询细胞元数据
cell_metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="disease == 'COVID-19' and is_primary_data == True",
    column_names=["cell_type", "tissue_general", "donor_id"]
)

# 查询基因元数据
gene_metadata = cellxgene_census.get_var(
    census, "homo_sapiens",
    value_filter="feature_name in ['CD4', 'CD8A']",
    column_names=["feature_id", "feature_name", "feature_length"]
)
```

### 4. 大规模查询(核外处理)

对于超出可用 RAM 的查询,使用 `axis_query()` 进行迭代处理:

```python
import tiledbsoma as soma

# 创建轴查询
query = census["census_data"]["homo_sapiens"].axis_query(
    measurement_name="RNA",
    obs_query=soma.AxisQuery(
        value_filter="tissue_general == 'brain' and is_primary_data == True"
    ),
    var_query=soma.AxisQuery(
        value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"
    )
)

# 分批迭代处理表达矩阵
iterator = query.X("raw").tables()
for batch in iterator:
    # batch 是 pyarrow.Table,包含列:
    # - soma_data: 表达值
    # - soma_dim_0: 细胞(obs)坐标
    # - soma_dim_1: 基因(var)坐标
    process_batch(batch)
```

**计算增量统计信息:**
```python
# 示例: 计算平均表达
n_observations = 0
sum_values = 0.0

iterator = query.X("raw").tables()
for batch in iterator:
    values = batch["soma_data"].to_numpy()
    n_observations += len(values)
    sum_values += values.sum()

mean_expression = sum_values / n_observations
```

### 5. 使用 PyTorch 进行机器学习

对于训练模型,使用实验性 PyTorch 集成:

```python
from cellxgene_census.experimental.ml import experiment_dataloader

with cellxgene_census.open_soma() as census:
    # 创建数据加载器
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="tissue_general == 'liver' and is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # 训练循环
    for epoch in range(num_epochs):
        for batch in dataloader:
            X = batch["X"]  # 基因表达张量
            labels = batch["obs"]["cell_type"]  # 细胞类型标签

            # 前向传播
            outputs = model(X)
            loss = criterion(outputs, labels)

            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

**训练/测试拆分:**
```python
from cellxgene_census.experimental.ml import ExperimentDataset

# 从实验创建数据集
dataset = ExperimentDataset(
    experiment_axis_query,
    layer_name="raw",
    obs_column_names=["cell_type"],
    batch_size=128,
)

# 拆分为训练和测试
train_dataset, test_dataset = dataset.random_split(
    split=[0.8, 0.2],
    seed=42
)
```

### 6. 与 Scanpy 集成

将 Census 数据与 scanpy 工作流程无缝集成:

```python
import scanpy as sc

# 从 Census 加载数据
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="cell_type == 'neuron' and tissue_general == 'cortex' and is_primary_data == True",
)

# 标准 scanpy 工作流程
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# 降维
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

# 可视化
sc.pl.umap(adata, color=["cell_type", "tissue", "disease"])
```

### 7. 多数据集集成

查询和集成多个数据集:

```python
# 策略 1: 分别查询多个组织
tissues = ["lung", "liver", "kidney"]
adatas = []

for tissue in tissues:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter=f"tissue_general == '{tissue}' and is_primary_data == True",
    )
    adata.obs["tissue"] = tissue
    adatas.append(adata)

# 连接
combined = adatas[0].concatenate(adatas[1:])

# 策略 2: 直接查询多个数据集
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="tissue_general in ['lung', 'liver', 'kidney'] and is_primary_data == True",
)
```

## 关键概念和最佳实践

### 始终筛选主数据
除非分析重复项,否则始终在查询中包含 `is_primary_data == True` 以避免多次计数细胞:
```python
obs_value_filter="cell_type == 'B cell' and is_primary_data == True"
```

### 指定 Census 版本以确保可重现性
始终在生产分析中指定 Census 版本:
```python
census = cellxgene_census.open_soma(census_version="2023-07-25")
```

### 加载前估算查询大小
对于大型查询,首先检查细胞数量以避免内存问题:
```python
# 获取细胞计数
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="tissue_general == 'brain' and is_primary_data == True",
    column_names=["soma_joinid"]
)
n_cells = len(metadata)
print(f"查询将返回 {n_cells:,} 个细胞")

# 如果太大(>10万),使用核外处理
```

### 使用 tissue_general 进行更广泛的分组
`tissue_general` 字段提供比 `tissue` 更粗略的类别,适用于跨组织分析:
```python
# 更广泛的分组
obs_value_filter="tissue_general == 'immune system'"

# 特定组织
obs_value_filter="tissue == 'peripheral blood mononuclear cell'"
```

### 仅选择所需列
通过仅指定所需的元数据列来最小化数据传输:
```python
obs_column_names=["cell_type", "tissue_general", "disease"]  # 不是所有列
```

### 检查基因特定查询的数据集存在性
分析特定基因时,验证哪些数据集测量了它们:
```python
presence = cellxgene_census.get_presence_matrix(
    census,
    "homo_sapiens",
    var_value_filter="feature_name in ['CD4', 'CD8A']"
)
```

### 两步工作流程: 先探索后查询
首先探索元数据以了解可用数据,然后查询表达:
```python
# 步骤 1: 探索可用内容
metadata = cellxgene_census.get_obs(
    census, "homo_sapiens",
    value_filter="disease == 'COVID-19' and is_primary_data == True",
    column_names=["cell_type", "tissue_general"]
)
print(metadata.value_counts())

# 步骤 2: 基于发现进行查询
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="disease == 'COVID-19' and cell_type == 'T cell' and is_primary_data == True",
)
```

## 可用的元数据字段

### 细胞元数据(obs)
筛选的关键字段:
- `cell_type`, `cell_type_ontology_term_id`
- `tissue`, `tissue_general`, `tissue_ontology_term_id`
- `disease`, `disease_ontology_term_id`
- `assay`, `assay_ontology_term_id`
- `donor_id`, `sex`, `self_reported_ethnicity`
- `development_stage`, `development_stage_ontology_term_id`
- `dataset_id`
- `is_primary_data`(布尔值: True = 唯一细胞)

### 基因元数据(var)
- `feature_id`(Ensembl 基因 ID,例如 "ENSG00000161798")
- `feature_name`(基因符号,例如 "FOXP2")
- `feature_length`(基因长度,以碱基对为单位)

## 参考文档

此技能包含详细的参考文档:

### references/census_schema.md
全面文档包括:
- Census 数据结构和组织
- 所有可用的元数据字段
- 值筛选语法和运算符
- SOMA 对象类型
- 数据纳入标准

**何时阅读:** 当您需要详细的架构信息、完整的元数据字段列表或复杂的筛选语法时。

### references/common_patterns.md
示例和模式包括:
- 探索性查询(仅元数据)
- 小到中等查询(AnnData)
- 大型查询(核外处理)
- PyTorch 集成
- Scanpy 集成工作流程
- 多数据集集成
- 最佳实践和常见陷阱

**何时阅读:** 实现特定查询模式、查找代码示例或排查常见问题时。

## 常见用例

### 用例 1: 探索组织中的细胞类型
```python
with cellxgene_census.open_soma() as census:
    cells = cellxgene_census.get_obs(
        census, "homo_sapiens",
        value_filter="tissue_general == 'lung' and is_primary_data == True",
        column_names=["cell_type"]
    )
    print(cells["cell_type"].value_counts())
```

### 用例 2: 查询标记基因表达
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19']",
        obs_value_filter="cell_type in ['T cell', 'B cell'] and is_primary_data == True",
    )
```

### 用例 3: 训练细胞类型分类器
```python
from cellxgene_census.experimental.ml import experiment_dataloader

with cellxgene_census.open_soma() as census:
    dataloader = experiment_dataloader(
        census["census_data"]["homo_sapiens"],
        measurement_name="RNA",
        X_name="raw",
        obs_value_filter="is_primary_data == True",
        obs_column_names=["cell_type"],
        batch_size=128,
        shuffle=True,
    )

    # 训练模型
    for epoch in range(epochs):
        for batch in dataloader:
            # 训练逻辑
            pass
```

### 用例 4: 跨组织分析
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="cell_type == 'macrophage' and tissue_general in ['lung', 'liver', 'brain'] and is_primary_data == True",
    )

    # 分析不同组织中的巨噬细胞差异
    sc.tl.rank_genes_groups(adata, groupby="tissue_general")
```

## 故障排除

### 查询返回的细胞太多
- 添加更具体的筛选器以减少范围
- 使用 `tissue` 而不是 `tissue_general` 以获得更精细的粒度
- 如果已知,按特定 `dataset_id` 筛选
- 对于大型查询,切换到核外处理

### 内存错误
- 使用更严格的筛选器减少查询范围
- 使用 `var_value_filter` 选择更少的基因
- 使用 `axis_query()` 进行核外处理
- 分批处理数据

### 结果中有重复细胞
- 始终在筛选器中包含 `is_primary_data == True`
- 检查是否故意跨多个数据集查询

### 未找到基因
- 验证基因名称拼写(区分大小写)
- 尝试使用 `feature_id` 代替 `feature_name` 的 Ensembl ID
- 检查数据集存在矩阵以查看是否测量了基因
- 某些基因可能在 Census 构建期间被过滤掉

### 版本不一致
- 始终显式指定 `census_version`
- 在所有分析中使用相同版本
- 查看版本特定更改的发行说明
