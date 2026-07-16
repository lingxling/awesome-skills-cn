---
name: cellxgene-census
description: 以编程方式查询 CZ CELLxGENE Census 中版本化的公开单细胞和空间转录组数据。当需要群体规模的细胞元数据、基因表达切片、Census 汇总计数、源 H5AD URI/下载、嵌入、空间 Census 数据，或跨物种、组织、疾病、检测方式和细胞类型的参考图谱比较时使用。分析自己本地的单细胞数据请使用 scanpy、anndata 或 scvi-tools。
allowed-tools: Read Write Edit Bash
license: MIT
compatibility: 需要 Python >=3.10,<3.13。示例针对 cellxgene-census 1.17.x 和 2025-11-08 稳定 LTS Census；空间工作流程需要 spatial extra 和 TileDB-SOMA >=1.15.5。查询公开 Census 数据无需身份验证。
metadata: {"version": "1.1", "skill-author": "K-Dense Inc."}
---

# CZ CELLxGENE Census

## 概述

CZ CELLxGENE Census 提供对来自 CZ CELLxGENE Discover 的全面、版本化标准化单细胞和空间转录组数据的编程访问。此技能使您能够高效查询和分析公开的 Census 发布版本，而无需先下载整个数据集。

Census 包括:
- 2025-11-08 稳定 LTS 发布版本中的 **2.17 亿+总细胞数**和 **1.25 亿+唯一细胞数**
- 2025-11-08 稳定 LTS 发布版本中的 **1,845 个数据集**
- 当前模式中的**人类、小鼠、狨猴、恒河猴和黑猩猩**数据
- **标准化元数据**(细胞类型、组织、疾病、供体)
- **原始基因表达**矩阵，以及源 H5AD 查找/下载辅助工具
- **预计算的汇总计数、嵌入和空间数据**
- **与 AnnData、Scanpy、TileDB-SOMA、TileDB-SOMA-ML 和其他分析工具集成**

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
uv pip install "cellxgene-census==1.17.*"
```

对于空间工作流程:
```bash
uv pip install "cellxgene-census[spatial]==1.17.*" "spatialdata[extra]>=0.2.5"
```

对于 PyTorch 模型训练，使用 TileDB-SOMA-ML。旧的 `cellxgene_census.experimental.ml` 加载器已弃用：

```bash
uv pip install "cellxgene-census==1.17.*" tiledbsoma-ml
```

## 核心工作流程模式

### 1. 打开 Census

始终使用上下文管理器以确保正确的资源清理:

```python
import cellxgene_census

# 打开最新稳定版本
with cellxgene_census.open_soma() as census:
    # 使用 census 数据

# 打开当前 LTS 版本以确保可重现性
with cellxgene_census.open_soma(census_version="2025-11-08") as census:
    # 使用 census 数据
```

**关键点:**
- 使用上下文管理器(`with` 语句)进行自动清理
- 指定 `census_version` 以确保可重现的分析
- `stable` 打开当前的 LTS Census 发布版本；`latest` 打开保留时间较短的最新每周发布版本

### 2. 探索 Census 信息

在查询表达数据之前,探索可用的数据集和元数据。

**访问摘要信息:**
```python
# 以 label/value 行形式获取摘要统计信息
summary = census["census_info"]["summary"].read().concat().to_pandas()
summary_values = summary.set_index("label")["value"]
print(f"总细胞数: {int(summary_values['total_cell_count']):,}")
print(f"唯一细胞数: {int(summary_values['unique_cell_count']):,}")

# 获取所有数据集
datasets = census["census_info"]["datasets"].read().concat().to_pandas()

# 按物种、细胞类型、组织、疾病和检测方式获取预计算的计数
summary_counts = census["census_info"]["summary_cell_counts"].read().concat().to_pandas()
tissue_counts = summary_counts[summary_counts["category"].eq("tissue_general")]
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
tissue_metadata = cellxgene_census.get_obs(
    census,
    "homo_sapiens",
    value_filter="is_primary_data == True",
    column_names=["tissue_general"],
)
tissue_counts = tissue_metadata["tissue_general"].value_counts()
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
- 在当前 LTS 发布版本中，`disease` 和 `disease_ontology_term_id` 可能包含以 ` || ` 分隔的多个值；在依赖精确相等筛选疾病队列前，先检查可用值

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
with census["census_data"]["homo_sapiens"].axis_query(
    measurement_name="RNA",
    obs_query=soma.AxisQuery(
        value_filter="tissue_general == 'brain' and is_primary_data == True"
    ),
    var_query=soma.AxisQuery(
        value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"
    ),
) as query:
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
import tiledbsoma as soma

# 示例: 计算平均表达
n_observations = 0
sum_values = 0.0

with census["census_data"]["homo_sapiens"].axis_query(
    measurement_name="RNA",
    obs_query=soma.AxisQuery(value_filter="tissue_general == 'brain' and is_primary_data == True"),
    var_query=soma.AxisQuery(value_filter="feature_name in ['FOXP2', 'TBR1', 'SATB2']"),
) as query:
    iterator = query.X("raw").tables()
    for batch in iterator:
        values = batch["soma_data"].to_numpy()
        n_observations += len(values)
        sum_values += values.sum()

mean_expression = sum_values / n_observations
```

### 5. 使用 PyTorch 进行机器学习

对于训练模型,使用 TileDB-SOMA-ML。旧的 `cellxgene_census.experimental.ml` PyTorch 加载器已弃用，计划移除。

```python
import tiledbsoma as soma
from tiledbsoma_ml import ExperimentDataset, experiment_dataloader

with cellxgene_census.open_soma() as census:
    experiment = census["census_data"]["homo_sapiens"]
    with experiment.axis_query(
        measurement_name="RNA",
        obs_query=soma.AxisQuery(
            value_filter="tissue_general == 'liver' and is_primary_data == True"
        ),
    ) as query:
        dataset = ExperimentDataset(
            query=query,
            layer_name="raw",
            obs_column_names=["cell_type"],
            batch_size=128,
            shuffle=True,
        )
        dataloader = experiment_dataloader(dataset)

        # 训练循环
        for epoch in range(num_epochs):
            dataset.set_epoch(epoch)
            for X, obs in dataloader:
                labels = obs["cell_type"]

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
train_dataset, test_dataset = dataset.random_split(0.8, 0.2, seed=42)
train_loader = experiment_dataloader(train_dataset, num_workers=2)
test_loader = experiment_dataloader(test_dataset, num_workers=2)
```

在 `ExperimentDataset` 上使用 `batch_size` 和 `shuffle`，而不是在 `torch.utils.data.DataLoader` 上；`experiment_dataloader()` 会拒绝 DataLoader 层面的 `batch_size`、`shuffle`、`sampler` 和 `batch_sampler` 参数。

### 6. 空间 Census 数据

对于支持的 Census 发布版本，空间数据存放在独立的 `census_spatial_sequencing` 集合中。查询 Visium 或 Slide-seq V2 数据时，请使用 spatial extra 和当前版本的 TileDB-SOMA：

```python
import cellxgene_census
import tiledbsoma as soma

with cellxgene_census.open_soma(census_version="2025-11-08") as census:
    spatial_experiment = census["census_spatial_sequencing"]["homo_sapiens"]
    with spatial_experiment.axis_query(
        measurement_name="RNA",
        obs_query=soma.AxisQuery(
            value_filter="dataset_id == '4cceac62-9513-42a4-90e5-2878dbb0192c'"
        ),
    ) as query:
        sdata = query.to_spatialdata(X_name="raw")
```

### 7. 与 Scanpy 集成

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

### 8. 多数据集集成

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

# 使用 AnnData 当前 API 连接
import anndata as ad
combined = ad.concat(adatas, label="tissue", keys=tissues)

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
census = cellxgene_census.open_soma(census_version="2025-11-08")
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

当前模式包含人类和小鼠以外的更多物种集合。可通过 `list(census["census_data"].keys())` 确认所选发布版本中可用的物种。

### 基因元数据(var)
- `feature_id`(Ensembl 基因 ID,例如 "ENSG00000161798")
- `feature_name`(基因符号,例如 "FOXP2")
- `feature_type`
- `feature_length`(基因长度,以碱基对为单位)
- `nnz`、`n_measured_obs`(用于检查稀疏度和覆盖率的可用性汇总信息)

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
- 空间 Census 访问模式
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
import tiledbsoma as soma
from tiledbsoma_ml import ExperimentDataset, experiment_dataloader

with cellxgene_census.open_soma() as census:
    experiment = census["census_data"]["homo_sapiens"]
    with experiment.axis_query(
        measurement_name="RNA",
        obs_query=soma.AxisQuery(value_filter="is_primary_data == True"),
    ) as query:
        dataset = ExperimentDataset(
            query=query,
            layer_name="raw",
            obs_column_names=["cell_type"],
            batch_size=128,
            shuffle=True,
        )
        dataloader = experiment_dataloader(dataset)

        for X, obs in dataloader:
            labels = obs["cell_type"]
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
