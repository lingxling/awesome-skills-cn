---
name: tiledbvcf
description: 使用 TileDB 高效存储和检索基因组变异数据。支持可扩展的 VCF/BCF 数据导入、增量样本添加、压缩存储、并行查询以及用于群体基因组学的导出功能。
license: MIT license
metadata:
    skill-author: Jeremy Leipzig
---

# TileDB-VCF

## 概述

TileDB-VCF 是一个高性能 C++ 库，提供 Python 和命令行界面，用于高效存储和检索基因组变异调用数据。它基于 TileDB 的稀疏数组技术构建，支持 VCF/BCF 文件的可扩展导入、无需昂贵合并操作的增量样本添加，以及对本地或云端存储的变异数据的高效并行查询。

## 何时使用此技能

当您需要以下功能时，应使用此技能：
- 学习 TileDB-VCF 概念和工作流程
- 原型设计基因组学分析和管道
- 处理中小型数据集（< 1000 个样本）
- 需要向现有数据集增量添加新样本
- 需要高效查询多个样本的特定基因组区域
- 处理云端存储的变异数据（S3、Azure、GCS）
- 需要导出大型 VCF 数据集的子集
- 为队列研究构建变异数据库
- 教育项目和方法开发
- 变异数据操作的性能至关重要

## 快速开始

### 安装

**首选方法：Conda/Mamba**
```bash
# 如果您使用 M1 Mac，请输入以下两行
CONDA_SUBDIR=osx-64
conda config --env --set subdir osx-64

# 创建 conda 环境
conda create -n tiledb-vcf "python<3.10"
conda activate tiledb-vcf

# Mamba 是 conda 的更快、更可靠的替代品
conda install -c conda-forge mamba

# 安装 TileDB-Py 和 TileDB-VCF，以及其他有用的库
mamba install -y -c conda-forge -c bioconda -c tiledb tiledb-py tiledbvcf-py pandas pyarrow numpy
```

**替代方法：Docker 镜像**
```bash
docker pull tiledb/tiledbvcf-py     # Python 接口
docker pull tiledb/tiledbvcf-cli    # 命令行接口
```

### 基本示例

**创建并填充数据集：**
```python
import tiledbvcf

# 创建新数据集
ds = tiledbvcf.Dataset(uri="my_dataset", mode="w",
                      cfg=tiledbvcf.ReadConfig(memory_budget=1024))

# 导入 VCF 文件（必须是带索引的单样本文件）
# 要求：
# - VCF 必须是单样本（非多样本）
# - 必须有索引：.csi（bcftools）或 .tbi（tabix）
ds.ingest_samples(["sample1.vcf.gz", "sample2.vcf.gz"])
```

**查询变异数据：**
```python
# 打开现有数据集进行读取
ds = tiledbvcf.Dataset(uri="my_dataset", mode="r")

# 查询特定区域和样本
df = ds.read(
    attrs=["sample_name", "pos_start", "pos_end", "alleles", "fmt_GT"],
    regions=["chr1:1000000-2000000", "chr2:500000-1500000"],
    samples=["sample1", "sample2", "sample3"]
)
print(df.head())
```

**导出到 VCF：**
```python
import os

# 导出两个 VCF 样本
ds.export(
    regions=["chr21:8220186-8405573"],
    samples=["HG00101", "HG00097"],
    output_format="v",
    output_dir=os.path.expanduser("~"),
)
```

## 核心功能

### 1. 数据集创建和导入

创建 TileDB-VCF 数据集并从多个 VCF/BCF 文件增量导入变异数据。这适用于构建群体基因组学数据库和队列研究。

**要求：**
- **仅支持单样本 VCF**：不支持多样本 VCF
- **需要索引文件**：VCF/BCF 文件必须有索引（.csi 或 .tbi）

**常见操作：**
- 创建具有优化数组模式的新数据集
- 并行导入单个或多个 VCF/BCF 文件
- 增量添加新样本，无需重新处理现有数据
- 配置内存使用和压缩设置
- 处理各种 VCF 格式和 INFO/FORMAT 字段
- 恢复中断的导入过程
- 导入期间验证数据完整性


### 2. 高效查询和过滤

通过基因组区域、样本和变异属性进行高性能查询。这适用于关联研究、变异发现和群体分析。

**常见操作：**
- 查询特定基因组区域（单个或多个）
- 按样本名称或样本组过滤
- 提取特定变异属性（位置、等位基因、基因型、质量）
- 高效访问 INFO 和 FORMAT 字段
- 组合空间和基于属性的过滤
- 流式处理大型查询结果
- 跨样本或区域执行聚合


### 3. 数据导出和互操作性

以各种格式导出数据，用于下游分析或与其他基因组学工具集成。这适用于共享数据集、创建分析子集或为其他管道提供输入。

**常见操作：**
- 导出到标准 VCF/BCF 格式
- 生成带有选定字段的 TSV 文件
- 创建样本/区域特定的子集
- 维护数据来源和元数据
- 无损数据导出，保留所有注释
- 压缩输出格式
- 大型数据集的流式导出


### 4. 群体基因组学工作流程

TileDB-VCF 在需要高效访问多个样本和基因组区域的变异数据的大规模群体基因组学分析中表现出色。

**常见工作流程：**
- 全基因组关联研究 (GWAS) 数据准备
- 稀有变异负担测试
- 群体分层分析
- 跨群体的等位基因频率计算
- 大型队列的质量控制
- 变异注释和过滤
- 跨群体比较分析


## 关键概念

### 数组模式和数据模型

**TileDB-VCF 数据模型：**
- 变异存储为稀疏数组，基因组坐标为维度
- 样本存储为属性，允许高效的样本特定查询
- INFO 和 FORMAT 字段以原始数据类型保留
- 自动压缩和分块以实现最佳存储

**模式配置：**
```python
# 具有特定瓦片范围的自定义模式
config = tiledbvcf.ReadConfig(
    memory_budget=2048,  # MB
    region_partition=(0, 3095677412),  # 全基因组
    sample_partition=(0, 10000)  # 最多 10k 样本
)
```

### 坐标系和区域

**重要：** TileDB-VCF 使用 **1 基基因组坐标**，遵循 VCF 标准：
- 位置是 1 基的（第一个碱基是位置 1）
- 范围两端都包含
- 区域 "chr1:1000-2000" 包括位置 1000-2000（总共 1001 个碱基）

**区域指定格式：**
```python
# 单个区域
regions = ["chr1:1000000-2000000"]

# 多个区域
regions = ["chr1:1000000-2000000", "chr2:500000-1500000"]

# 整个染色体
regions = ["chr1"]

# BED 风格（0 基，半开区间，内部转换）
regions = ["chr1:999999-2000000"]  # 等效于 1 基的 chr1:1000000-2000000
```

### 内存管理

**性能考虑：**
1. **根据可用系统内存设置适当的内存预算**
2. **对非常大的结果集使用流式查询**
3. **分区大型导入以避免内存耗尽**
4. **为重复的区域访问配置瓦片缓存**
5. **对多个文件使用并行导入**
6. **通过组合附近区域优化区域查询**

### 云存储集成

TileDB-VCF 无缝支持云存储：
```python
# S3 数据集
ds = tiledbvcf.Dataset(uri="s3://bucket/dataset", mode="r")

# Azure Blob 存储
ds = tiledbvcf.Dataset(uri="azure://container/dataset", mode="r")

# Google Cloud Storage
ds = tiledbvcf.Dataset(uri="gcs://bucket/dataset", mode="r")
```

## 常见陷阱

1. **导入期间内存耗尽**：对大型 VCF 文件使用适当的内存预算和批处理
2. **低效的区域查询**：组合附近区域而不是进行许多单独的查询
3. **缺少样本名称**：确保 VCF 头部中的样本名称与查询样本规范匹配
4. **坐标系混淆**：记住 TileDB-VCF 使用 1 基坐标，如 VCF 标准
5. **大型结果集**：对返回数百万变异的查询使用流式处理或分页
6. **云权限**：确保云存储访问的适当认证
7. **并发访问**：多个写入器对同一数据集的访问可能导致损坏 - 使用适当的锁定

## CLI 使用

TileDB-VCF 提供命令行界面，包含以下子命令：

**可用子命令：**
- `create` - 创建空的 TileDB-VCF 数据集
- `store` - 将样本导入到 TileDB-VCF 数据集
- `export` - 从 TileDB-VCF 数据集导出数据
- `list` - 列出 TileDB-VCF 数据集中存在的所有样本名称
- `stat` - 打印关于 TileDB-VCF 数据集的高级统计信息
- `utils` - 用于处理 TileDB-VCF 数据集的工具
- `version` - 打印版本信息并退出

```bash
# 创建空数据集
tiledbvcf create --uri my_dataset

# 导入样本（需要带索引的单样本 VCF）
tiledbvcf store --uri my_dataset --samples sample1.vcf.gz,sample2.vcf.gz

# 导出数据
tiledbvcf export --uri my_dataset \
  --regions "chr1:1000000-2000000" \
  --sample-names "sample1,sample2"

# 列出所有样本
tiledbvcf list --uri my_dataset

# 显示数据集统计信息
tiledbvcf stat --uri my_dataset
```

## 高级功能

### 等位基因频率分析
```python
# 计算等位基因频率
af_df = tiledbvcf.read_allele_frequency(
    uri="my_dataset",
    regions=["chr1:1000000-2000000"],
    samples=["sample1", "sample2", "sample3"]
)
```

### 样本质量控制
```python
# 执行样本 QC
qc_results = tiledbvcf.sample_qc(
    uri="my_dataset",
    samples=["sample1", "sample2"]
)
```

### 自定义配置
```python
# 高级配置
config = tiledbvcf.ReadConfig(
    memory_budget=4096,
    tiledb_config={
        "sm.tile_cache_size": "1000000000",
        "vfs.s3.region": "us-east-1"
    }
)
```


## 资源

## 获取帮助

### 开源 TileDB-VCF 资源

**开源文档：**
- TileDB 学院：https://cloud.tiledb.com/academy/
- 群体基因组学指南：https://cloud.tiledb.com/academy/structure/life-sciences/population-genomics/
- TileDB-VCF GitHub：https://github.com/TileDB-Inc/TileDB-VCF

### TileDB-Cloud 资源

**对于大规模/生产基因组学：**
- TileDB-Cloud 平台：https://cloud.tiledb.com
- TileDB 学院（所有文档）：https://cloud.tiledb.com/academy/

**入门：**
- 免费账户注册：https://cloud.tiledb.com
- 联系：sales@tiledb.com 了解企业需求

## 扩展到 TileDB-Cloud

当您的基因组学工作负载超出单节点处理能力时，TileDB-Cloud 为生产基因组学管道提供企业级功能。

**注意**：本节基于可用文档涵盖 TileDB-Cloud 功能。有关完整的 API 详细信息和当前功能，请参考官方 TileDB-Cloud 文档和 API 参考。

### 设置 TileDB-Cloud

**1. 创建账户并获取 API 令牌**
```bash
# 在 https://cloud.tiledb.com 注册
# 在账户设置中生成 API 令牌
```

**2. 安装 TileDB-Cloud Python 客户端**
```bash
# 基本安装
pip install tiledb-cloud

# 带基因组学特定功能
pip install tiledb-cloud[life-sciences]
```

**3. 配置认证**
```bash
# 设置带有 API 令牌的环境变量
export TILEDB_REST_TOKEN="your_api_token"
```

```python
import tiledb.cloud

# 认证通过 TILEDB_REST_TOKEN 自动进行
# 代码中不需要显式登录
```

### 从开源迁移到 TileDB-Cloud

**大规模导入**
```python
# TileDB-Cloud：分布式 VCF 导入
import tiledb.cloud.vcf

# 使用专门的 VCF 导入模块
# 注意：确切的 API 需要 TileDB-Cloud 文档
# 这表示可用功能结构
tiledb.cloud.vcf.ingestion.ingest_vcf_dataset(
    source="s3://my-bucket/vcf-files/",
    output="tiledb://my-namespace/large-dataset",
    namespace="my-namespace",
    acn="my-s3-credentials",
    ingest_resources={"cpu": "16", "memory": "64Gi"}
)
```

**分布式查询处理**
```python
# TileDB-Cloud：跨分布式存储的 VCF 查询
import tiledb.cloud.vcf
import tiledbvcf

# 定义数据集 URI
dataset_uri = "tiledb://TileDB-Inc/gvcf-1kg-dragen-v376"

# 从数据集中获取所有样本
ds = tiledbvcf.Dataset(dataset_uri, tiledb_config=cfg)
samples = ds.samples()

# 定义要查询的属性和范围
attrs = ["sample_name", "fmt_GT", "fmt_AD", "fmt_DP"]
regions = ["chr13:32396898-32397044", "chr13:32398162-32400268"]

# 执行读取，以分布式方式执行
df = tiledb.cloud.vcf.read(
    dataset_uri=dataset_uri,
    regions=regions,
    samples=samples,
    attrs=attrs,
    namespace="my-namespace",  # 指定要收费的账户
)
df.to_pandas()
```

### 企业功能

**数据共享和协作**
```python
# TileDB-Cloud 通过基于命名空间的权限和组管理提供企业数据共享功能

# 通过 TileDB-Cloud URI 访问共享数据集
dataset_uri = "tiledb://shared-namespace/population-study"

# 通过共享笔记本和计算资源进行协作
# (具体 API 需要 TileDB-Cloud 文档)
```

**成本优化**
- **无服务器计算**：仅为实际计算时间付费
- **自动扩展**：根据工作负载自动向上/向下扩展
- ** Spot 实例**：为批处理作业使用成本优化的计算
- **数据分层**：自动热/冷存储管理

**安全和合规**
- **端到端加密**：数据在传输和静止时加密
- **访问控制**：细粒度权限和审计日志
- **HIPAA/SOC2 合规**：企业安全标准
- **VPC 支持**：在私有云环境中部署

### 迁移检查清单

✅ **如果您有以下情况，迁移到 TileDB-Cloud：**
- [ ] 数据集 > 1000 个样本
- [ ] 需要处理 > 100GB 的 VCF 数据
- [ ] 需要分布式计算
- [ ] 多个团队成员需要访问
- [ ] 需要企业安全/合规
- [ ] 想要成本优化的无服务器计算
- [ ] 需要 24/7 生产正常运行时间

### 开始使用 TileDB-Cloud

1. **免费开始**：TileDB-Cloud 提供用于评估的免费层级
2. **迁移支持**：TileDB 团队提供迁移协助
3. **培训**：访问基因组学特定的教程和示例
4. **专业服务**：定制部署和优化

**后续步骤：**
- 访问 https://cloud.tiledb.com 创建账户
- 查看 https://cloud.tiledb.com/academy/ 上的文档
- 联系 sales@tiledb.com 了解企业需求