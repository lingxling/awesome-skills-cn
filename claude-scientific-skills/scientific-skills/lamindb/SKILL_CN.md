---
name: lamindb
description: 用于生物学的开源数据框架。使数据可查询、可追溯、可重复和FAIR。管理生物数据集（scRNA-seq、空间、流式细胞术等）、跟踪计算工作流程、使用生物本体进行管理和验证数据、构建数据湖仓，或确保生物学研究中的数据谱系和可重复性。涵盖数据管理、注解、本体（基因、细胞类型、疾病、组织）、模式验证、与工作流程管理器（Nextflow、Snakemake）和MLOps平台（W&B、MLflow）的集成以及部署策略。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# LaminDB

## 概述

LaminDB是一个专为生物学设计的开源数据框架，旨在使数据可查询、可追溯、可重复和FAIR（可发现、可访问、可互操作、可重用）。它通过单个Python API提供了统一平台，结合了湖仓架构、谱系跟踪、特征存储、生物本体、LIMS（实验室信息管理系统）和ELN（电子实验记录本）功能。

**核心价值主张：**
- **可查询性**：通过元数据、特征和本体术语搜索和筛选数据集
- **可追溯性**：从原始数据通过分析到结果的自动谱系跟踪
- **可重复性**：数据、代码和环境的版本控制
- **FAIR合规性**：使用生物本体进行标准化注解

## 何时使用此技能

在以下情况下使用此技能：

- **管理生物数据集**：scRNA-seq、批量RNA-seq、空间转录组学、流式细胞术、多模态数据、EHR数据
- **跟踪计算工作流程**：笔记本、脚本、管道执行（Nextflow、Snakemake、Redun）
- **管理和验证数据**：模式验证、标准化、基于本体的注解
- **使用生物本体**：基因、蛋白质、细胞类型、组织、疾病、通路（通过Bionty）
- **构建数据湖仓**：跨多个数据集的统一查询接口
- **确保可重复性**：自动版本控制、谱系跟踪、环境捕获
- **集成ML管道**：连接Weights & Biases、MLflow、HuggingFace、scVI-tools
- **部署数据基础设施**：设置本地或基于云的数据管理系统
- **在数据集上协作**：共享管理的、带标准化元数据的注解数据

## 核心能力

LaminDB提供六个相互连接的能力领域，每个都在references文件夹中有详细文档。

### 1. 核心概念和数据谱系

**核心实体：**
- **Artifacts（制品）**：版本化数据集（DataFrame、AnnData、Parquet、Zarr等）
- **Records（记录）**：实验实体（样本、扰动、仪器）
- **Runs & Transforms（运行和转换）**：计算谱系跟踪（什么代码产生了什么数据）
- **Features（特征）**：用于注解和查询的类型化元数据字段

**关键工作流程：**
- 从文件或Python对象创建和版本化制品
- 使用`ln.track()`和`ln.finish()`跟踪笔记本/脚本执行
- 使用类型化特征注解制品
- 使用`artifact.view_lineage()`可视化数据谱系图
- 按谱系查询（查找来自特定代码/输入的所有输出）

**参考：** `references/core-concepts.md` - 阅读此内容以了解制品、记录、运行、转换、特征、版本控制和谱系跟踪的详细信息。

### 2. 数据管理和查询

**查询能力：**
- 使用自动完成浏览注册表和查找
- 使用`get()`、`one()`、`one_or_none()`检索单个记录
- 使用比较运算符（`__gt`、`__lte`、`__contains`、`__startswith`）进行筛选
- 基于特征的查询（按注解的元数据查询）
- 使用双下划线语法跨注册表遍历
- 跨注册表全文搜索
- 使用Q对象进行高级逻辑查询（AND、OR、NOT）
- 流式传输大数据集而不加载到内存中

**关键工作流程：**
- 使用过滤器和排序浏览制品
- 按特征、创建日期、创建者、大小等查询
- 分块或使用数组切片流式传输大文件
- 使用分层键组织数据
- 将制品分组到集合中

**参考：** `references/data-management.md` - 阅读此内容以了解全面的查询模式、筛选示例、流式传输策略和数据组织最佳实践。

### 3. 注解和验证

**管理过程：**
1. **验证**：确认数据集匹配所需模式
2. **标准化**：修复拼写错误、将同义词映射到规范术语
3. **注解**：将数据集链接到元数据实体以实现可查询性

**模式类型：**
- **灵活模式**：仅验证已知列，允许额外元数据
- **最小所需模式**：指定基本列，允许额外内容
- **严格模式**：对结构和值进行完全控制

**支持的数据类型：**
- DataFrame（Parquet、CSV）
- AnnData（单细胞基因组学）
- MuData（多模态）
- SpatialData（空间转录组学）
- TileDB-SOMA（可扩展数组）

**关键工作流程：**
- 定义特征和模式以进行数据验证
- 使用`DataFrameCurator`或`AnnDataCurator`进行验证
- 使用`.cat.standardize()`标准化值
- 使用`.cat.add_ontology()`映射到本体
- 保存具有模式链接的注解制品
- 按特征查询验证的数据集

**参考：** `references/annotation-validation.md` - 阅读此内容以了解详细管理工作流程、模式设计模式、处理验证错误和最佳实践。

### 4. 生物本体

**可用本体（通过Bionty）：**
- 基因（Ensembl）、蛋白质（UniProt）
- 细胞类型（CL）、细胞系（CLO）
- 组织（Uberon）、疾病（Mondo、DOID）
- 表型（HPO）、通路（GO）
- 实验因子（EFO）、发育阶段
- 生物体（NCBItaxon）、药物（DrugBank）

**关键工作流程：**
- 使用`bt.CellType.import_source()`导入公共本体
- 使用关键词或精确匹配搜索本体
- 使用同义词映射标准化术语
- 探索层次关系（父级、子级、祖先）
- 根据本体术语验证数据
- 使用本体记录注解数据集
- 创建自定义术语和层次
- 处理多生物体上下文（人类、小鼠等）

**参考：** `references/ontologies.md` - 阅读此内容以了解全面的本体操作、标准化策略、层次导航和注解工作流程。

### 5. 集成

**工作流程管理器：**
- Nextflow：跟踪管道过程和输出
- Snakemake：集成到Snakemake规则
- Redun：结合Redun任务跟踪

**MLOps平台：**
- Weights & Biases：将实验与数据制品链接
- MLflow：跟踪模型和实验
- HuggingFace：跟踪模型微调
- scVI-tools：单细胞分析工作流程

**存储系统：**
- 本地文件系统、AWS S3、Google Cloud Storage
- S3兼容（MinIO、Cloudflare R2）
- HTTP/HTTPS端点（只读）
- HuggingFace数据集

**数组存储：**
- TileDB-SOMA（带cellxgene支持）
- DuckDB用于Parquet文件的SQL查询

**可视化：**
- Vitessce用于交互式空间/单细胞可视化

**版本控制：**
- Git集成用于源代码跟踪

**参考：** `references/integrations.md` - 阅读此内容以了解集成模式、代码示例和第三方系统的故障排除。

### 6. 设置和部署

**安装：**
- 基本：`uv pip install lamindb`
- 带附加组件：`uv pip install 'lamindb[gcp,zarr,fcs]'`
- 模块：bionty、wetlab、clinical

**实例类型：**
- 本地SQLite（开发）
- 云存储 + SQLite（小团队）
- 云存储 + PostgreSQL（生产）

**存储选项：**
- 本地文件系统
- 带有可配置区域和权限的AWS S3
- Google Cloud Storage
- S3兼容端点（MinIO、Cloudflare R2）

**配置：**
- 云文件的缓存管理
- 多用户系统配置
- Git存储库同步
- 环境变量

**部署模式：**
- 本地开发 → 云生产迁移
- 多区域部署
- 带有个人实例的共享存储

**参考：** `references/setup-deployment.md` - 阅读此内容以了解详细安装、配置、存储设置、数据库管理、安全最佳实践和故障排除。

## 常见用例工作流程

### 用例1：使用本体验证的单细胞RNA-seq分析

```python
import lamindb as ln
import bionty as bt
import anndata as ad

# 开始跟踪
ln.track(params={"analysis": "scRNA-seq QC和注解"})

# 导入细胞类型本体
bt.CellType.import_source()

# 加载数据
adata = ad.read_h5ad("raw_counts.h5ad")

# 验证和标准化细胞类型
adata.obs["cell_type"] = bt.CellType.standardize(adata.obs["cell_type"])

# 使用模式进行管理
curator = ln.curators.AnnDataCurator(adata, schema)
curator.validate()
artifact = curator.save_artifact(key="scrna/validated.h5ad")

# 链接本体注解
cell_types = bt.CellType.from_values(adata.obs.cell_type)
artifact.feature_sets.add_ontology(cell_types)

ln.finish()
```

### 用例2：构建可查询的数据湖仓

```python
import lamindb as ln

# 注册多个实验
for i, file in enumerate(data_files):
    artifact = ln.Artifact.from_anndata(
        ad.read_h5ad(file),
        key=f"scrna/batch_{i}.h5ad",
        description=f"scRNA-seq批次{i}"
    ).save()

    # 使用特征注解
    artifact.features.add_values({
        "batch": i,
        "tissue": tissues[i],
        "condition": conditions[i]
    })

# 跨所有实验查询
immune_datasets = ln.Artifact.filter(
    key__startswith="scrna/",
    tissue="PBMC",
    condition="treated"
).to_dataframe()

# 加载特定数据集
for artifact in immune_datasets:
    adata = artifact.load()
    # 分析
```

### 用例3：使用W&B集成的ML管道

```python
import lamindb as ln
import wandb

# 初始化两个系统
wandb.init(project="drug-response", name="exp-42")
ln.track(params={"model": "random_forest", "n_estimators": 100})

# 从LaminDB加载训练数据
train_artifact = ln.Artifact.get(key="datasets/train.parquet")
train_data = train_artifact.load()

# 训练模型
model = train_model(train_data)

# 记录到W&B
wandb.log({"accuracy": 0.95})

# 在LaminDB中保存模型并带有W&B链接
import joblib
joblib.dump(model, "model.pkl")
model_artifact = ln.Artifact("model.pkl", key="models/exp-42.pkl").save()
model_artifact.features.add_values({"wandb_run_id": wandb.run.id})

ln.finish()
wandb.finish()
```

### 用例4：Nextflow管道集成

```python
# 在Nextflow进程脚本中
import lamindb as ln

ln.track()

# 加载输入制品
input_artifact = ln.Artifact.get(key="raw/batch_${batch_id}.fastq.gz")
input_path = input_artifact.cache()

# 处理（比对、定量等）
# ... Nextflow进程逻辑 ...

# 保存输出
output_artifact = ln.Artifact(
    "counts.csv",
    key="processed/batch_${batch_id}_counts.csv"
).save()

ln.finish()
```

## 入门检查清单

要开始有效使用LaminDB：

1. **安装和设置**（`references/setup-deployment.md`）
   - 安装LaminDB和所需的附加组件
   - 使用`lamin login`进行身份验证
   - 使用`lamin init --storage ...`初始化实例

2. **学习核心概念**（`references/core-concepts.md`）
   - 了解Artifacts、Records、Runs、Transforms
   - 练习创建和检索制品
   - 在工作流程中实现`ln.track()`和`ln.finish()`

3. **掌握查询**（`references/data-management.md`）
   - 练习使用过滤器和排序浏览注册表
   - 学习基于特征的查询
   - 尝试流式传输大文件
   - 实验不同的搜索模式

4. **设置验证**（`references/annotation-validation.md`）
   - 定义与研究领域相关的特征
   - 为数据类型创建模式
   - 练习管理工作流程
   - 尝试标准化和本体映射

5. **集成本体**（`references/ontologies.md`）
   - 导入相关的生物本体（基因、细胞类型等）
   - 验证现有注解
   - 使用本体术语标准化元数据
   - 探索层次关系

6. **连接工具**（`references/integrations.md`）
   - 与现有工作流程管理器集成
   - 链接ML平台进行实验跟踪
   - 配置云存储和计算
   - 测试跨系统工作流程

## 关键原则

使用LaminDB时遵循以下原则：

1. **跟踪所有内容**：在每次分析开始时使用`ln.track()`以自动捕获谱系

2. **尽早验证**：在进行广泛分析之前定义模式并验证数据

3. **使用本体**：利用公共生物本体进行标准化注解

4. **使用键组织**：使用分层键结构化制品键（例如，`project/experiment/batch/file.h5ad`）

5. **先查询元数据**：在加载大文件之前筛选和搜索

6. **版本化，不要重复**：使用内置版本控制而不是为修改创建新键

7. **使用特征注解**：定义类型化特征以实现可查询的元数据

8. **彻底记录**：为制品、模式和转换添加描述

9. **利用谱系**：使用`view_lineage()`了解数据来源

10. **本地开始，扩展到云**：使用SQLite进行本地开发，使用PostgreSQL部署到云

## 参考文件

此技能包括全面的参考文档，按能力组织：

- **`references/core-concepts.md`** - Artifacts、记录、运行、转换、特征、版本控制和谱系
- **`references/data-management.md`** - 查询、筛选、搜索、流式传输、组织数据
- **`references/annotation-validation.md`** - 模式设计、管理工作流程、验证策略
- **`references/ontologies.md`** - 生物本体管理、标准化、层次
- **`references/integrations.md`** - 工作流程管理器、MLOps平台、存储系统、工具
- **`references/setup-deployment.md`** - 安装、配置、部署、故障排除

根据任务需要阅读相关的参考文件。

## 其他资源

- **官方文档**：https://docs.lamin.ai
- **API参考**：https://docs.lamin.ai/api
- **GitHub存储库**：https://github.com/laminlabs/lamindb
- **教程**：https://docs.lamin.ai/tutorial
- **FAQ**：https://docs.lamin.ai/faq
