---
name: lamindb
description: 在使用LaminDB时使用此技能，LaminDB是面向生物学数据集和模型的开源、谱系原生的湖仓（lakehouse）。涵盖设置、制品注册、查询/搜索、谱系跟踪、验证、通过Bionty进行的本体驱动注解、集合、分支、存储以及工作流集成。
license: Apache-2.0 license
metadata: {"version": "1.1", "skill-author": "K-Dense Inc."}
---

# LaminDB

## 概述

LaminDB是一个开源的、谱系原生的生物学湖仓。它使数据集和模型可查询、可追溯、经过验证、可重复，并符合FAIR（可发现、可访问、可互操作、可重用）标准，同时将数据以开放格式存储在本地文件系统、S3、GCS、Hugging Face、SQLite和Postgres中。

**核心价值主张：**
- **可查询性**：搜索和筛选制品、记录、运行、特征、模式和集合
- **可追溯性**：跟踪笔记本、脚本、函数和管道的输入、输出、参数、源代码和环境
- **验证**：使用模式管理DataFrame、AnnData、SpatialData、TileDB-SOMA、Parquet、Zarr及其他生物学格式
- **FAIR合规性**：使用Bionty支持的本体和自定义注册表标准化注解
- **变更管理**：使用项目、分支、空间、集合以及保存的笔记或计划来组织工作

## 何时使用此技能

在以下情况下使用此技能：

- **管理生物数据集**：scRNA-seq、批量RNA-seq、空间转录组学、流式细胞术、多模态数据、EHR数据
- **跟踪计算工作流程**：笔记本、脚本、函数、shell脚本、管道执行（Nextflow、Snakemake、Redun）
- **管理和验证数据**：模式验证、标准化、基于本体的注解
- **使用生物本体**：基因、蛋白质、细胞类型、组织、疾病、通路（通过Bionty）
- **构建数据湖仓**：跨多个数据集的统一查询接口
- **确保可重复性**：自动版本控制、谱系跟踪、环境捕获
- **集成ML管道**：连接Weights & Biases、MLflow、Hugging Face、Lightning、scVI-tools
- **部署数据基础设施**：设置本地或基于云的数据管理系统
- **在数据集上协作**：共享经过整理、带标准化元数据的注解数据

## 核心能力

LaminDB提供六个相互连接的能力领域，每个都在references文件夹中有详细文档。

### 1. 核心概念和数据谱系

**核心实体：**
- **Artifacts（制品）**：版本化数据集（DataFrame、AnnData、Parquet、Zarr等）
- **Records & ULabels（记录和ULabel）**：实验实体、类型化记录和简单标签
- **Collections（集合）**：版本化的、不可变的制品集
- **Runs & Transforms（运行和转换）**：计算谱系跟踪（什么代码产生了什么数据）
- **Features（特征）**：用于注解和查询的类型化元数据字段
- **Projects, Branches & Spaces（项目、分支和空间）**：项目分组、变更管理和访问边界

**关键工作流程：**
- 从文件或Python对象创建和版本化制品
- 使用`ln.track()`和`ln.finish()`跟踪笔记本/脚本执行
- 使用`@ln.flow()`和`@ln.step()`跟踪函数工作流
- 使用记录、ulabel、项目和类型化特征注解制品
- 使用`artifact.view_lineage()`可视化数据谱系图
- 按谱系查询（查找来自特定代码/输入的所有输出）

**参考：** `references/core-concepts.md` - 阅读此内容以了解制品、记录、运行、转换、特征、版本控制和谱系跟踪的详细信息。

### 2. 数据管理和查询

**查询能力：**
- 使用自动完成浏览注册表和查找
- 使用`get()`、`one()`、`one_or_none()`检索单个记录
- 使用比较运算符（`__gt`、`__lte`、`__contains`、`__startswith`）进行筛选
- 基于特征的查询，包括使用`Feature`对象的表达式风格查询
- 使用双下划线语法跨注册表遍历
- 跨注册表全文搜索
- 使用`ln.Q`对象进行高级逻辑查询（AND、OR、NOT）
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
- 使用`DataFrameCurator`、`AnnDataCurator`、`SpatialDataCurator`或`TiledbsomaExperimentCurator`进行验证
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
- Lightning：持久化检查点和训练元数据

**MLOps平台：**
- Weights & Biases：将实验与数据制品链接
- MLflow：跟踪模型和实验
- Hugging Face：跟踪模型微调
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
- 当前稳定基线版本：`lamindb==2.5.1`（发布于2026-06-01；需要Python >=3.10, <=3.14）
- 基本：`uv pip install 'lamindb==2.5.1'`
- 带附加组件：`uv pip install 'lamindb[gcp,zarr-v2,fcs]==2.5.1'`
- 仅最小命名空间：`uv pip install 'lamindb-core==2.5.1'`
- Bionty模块：已包含在LaminDB文档中，也可通过`uv pip install 'bionty==2.4.0'`单独安装
- 可选模块：对于wetlab或clinical模式模块，请固定已审核的发行版本，而不是安装浮动的最新版本

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
- 用于凭证和连接URL的命名环境变量

**部署模式：**
- 本地开发 → 云生产迁移
- 多区域部署
- 带有个人实例的共享存储

**参考：** `references/setup-deployment.md` - 阅读此内容以了解详细安装、配置、存储设置、数据库管理、安全最佳实践和故障排除。

## 安全默认设置

在协助进行LaminDB设置或集成时：

- 切勿显示、记录或传输实际的API密钥、云凭证、数据库密码或包含密钥的完整连接字符串。
- 优先使用IAM角色、工作负载身份、密钥管理器或诸如`LAMIN_DB_URL`、`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`和`GOOGLE_APPLICATION_CREDENTIALS`之类的命名环境变量；只检查某个命名变量是否存在，而不检查其值。
- 在保存来自REST API、外部数据库或用户提供文件的内容之前，使用明确的模式或管理器对其进行验证和清理。
- 为了实现可重复的安装，请固定软件包版本或使用锁定文件。仅当用户明确希望获取最新的上游版本时，才使用不固定版本的安装方式。

## 常见用例工作流程

### 用例1：使用本体验证的单细胞RNA-seq分析

```python
import lamindb as ln
import bionty as bt
import anndata as ad

# 开始跟踪笔记本/脚本运行
ln.track(params={"analysis": "scRNA-seq QC and annotation"})

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

# 链接本体驱动的注解以实现可查询性
cell_types = bt.CellType.from_values(adata.obs["cell_type"])
artifact.cell_types.add(*cell_types)

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
    artifact.features.set_values({
        "batch": i,
        "tissue": tissues[i],
        "condition": conditions[i]
    })

# 按注解特征跨所有实验查询
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
model_artifact.features.set_values({"wandb_run_id": wandb.run.id})

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

对于原生Nextflow项目，如果可用，优先使用`nf-lamin`插件和当前的`nextflow.config`模式；对于小型或自定义管道步骤，使用内联Python跟踪。

## 入门检查清单

要开始有效使用LaminDB：

1. **安装和设置**（`references/setup-deployment.md`）
   - 安装固定版本的LaminDB和所需的附加组件
   - 使用`lamin login`进行身份验证
   - 使用`lamin init --storage ...`初始化实例

2. **学习核心概念**（`references/core-concepts.md`）
   - 了解Artifacts、Records、Runs、Transforms
   - 练习创建和检索制品
   - 在工作流程中实现`ln.track()`/`ln.finish()`或`@ln.flow()`/`@ln.step()`

3. **掌握查询**（`references/data-management.md`）
   - 练习使用过滤器和排序浏览注册表
   - 学习基于特征的查询和表达式风格的筛选
   - 尝试流式传输大文件

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

7. **使用特征注解**：定义类型化特征，并使用`artifact.features.set_values()`实现可查询的元数据

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
