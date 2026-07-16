---
name: latchbio-integration
description: Latch plat用于m 用于 bio在用于matics w或kflows. Build pipel在es 使用 Latch SDK, @w或kflow/@task dec或at或s, deploy serverless w或kflows, LatchFile/LatchDir, Nextflow/Snakemake 在tegration.
license: Unknown
metadata: {"version": "1.0", "skill-author": "K-Dense Inc."}
---






# LatchBio 集成

## 概述

Latch 是一个用于构建和部署生物信息学工作流为无服务器流水线的 Python 框架。基于 Flyte 构建，使用 @workflow/@task 装饰器创建工作流，通过 LatchFile/LatchDir 管理云端数据，配置资源，并集成 Nextflow/Snakemake 流水线。

## 核心能力

Latch 平台提供四个主要功能领域：

### 1. 工作流创建与部署
- 使用 Python 装饰器定义无服务器工作流
- 支持原生 Python、Nextflow 和 Snakemake 流水线
- 使用 Docker 自动容器化
- 自动生成无代码用户界面
- 版本控制和可复现性

### 2. 数据管理
- 云存储抽象（LatchFile、LatchDir）
- 使用 Registry 进行结构化数据组织（Projects → Tables → Records）
- 通过链接和枚举实现类型安全的数据操作
- 本地与云端之间的自动文件传输
- 用于文件选择的 Glob 模式匹配

### 3. 资源配置
- 预配置的任务装饰器（@small_task、@large_task、@small_gpu_task、@large_gpu_task）
- 自定义资源规格（CPU、内存、GPU、存储）
- GPU 支持（K80、V100、A100）
- 超时和存储配置
- 成本优化策略

### 4. 验证工作流
- 生产就绪的预构建流水线
- 批量 RNA-seq、DESeq2、通路分析
- 用于蛋白质结构预测的 AlphaFold 和 ColabFold
- 单细胞工具（ArchR、scVelo、emptyDropsR）
- CRISPR 分析、系统发育学等

## 快速入门

### 安装与设置

```bash
# 安装 Latch SDK
uv pip install latch

# 登录 Latch
latch login

# 初始化新工作流
latch init my-workflow

# 将工作流注册到平台
latch register my-workflow
```

**前置条件：**
- Docker 已安装并运行
- Latch 账户凭据
- Python 3.8+

### 基本工作流示例

```python
from latch import workflow, small_task
from latch.types import LatchFile

@small_task
def process_file(input_file: LatchFile) -> LatchFile:
    """处理单个文件"""
    # 处理逻辑
    return output_file

@workflow
def my_workflow(input_file: LatchFile) -> LatchFile:
    """
    我的生物信息学工作流

    Args:
        input_file: 输入数据文件
    """
    return process_file(input_file=input_file)
```

## 何时使用此技能

遇到以下任何场景时应使用此技能：

**工作流开发：**
- "为 RNA-seq 分析创建 Latch 工作流"
- "将我的流水线部署到 Latch"
- "将我的 Nextflow 流水线转换为 Latch"
- "为我的工作流添加 GPU 支持"
- 使用 `@workflow`、`@task` 装饰器

**数据管理：**
- "在 Latch Registry 中组织我的测序数据"
- "如何使用 LatchFile 和 LatchDir？"
- "在 Latch 中设置样本追踪"
- 使用 `latch:///` 路径

**资源配置：**
- "为 Latch 上的 AlphaFold 配置 GPU"
- "我的任务内存不足"
- "如何优化工作流成本？"
- 使用任务装饰器

**验证工作流：**
- "在 Latch 上运行 AlphaFold"
- "使用 DESeq2 进行差异表达分析"
- "可用的预构建工作流"
- 使用 `latch.verified` 模块

## 详细文档

此技能包含按能力组织的综合参考文档：

### references/workflow-creation.md
**阅读此文档以了解：**
- 创建和注册工作流
- 任务定义和装饰器
- 支持 Python、Nextflow、Snakemake
- 启动计划和条件部分
- 工作流执行（CLI 和编程方式）
- 多步骤和并行流水线
- 注册问题故障排除

**关键主题：**
- `latch init` 和 `latch register` 命令
- `@workflow` 和 `@task` 装饰器
- LatchFile 和 LatchDir 基础
- 类型注解和文档字符串
- 带有预设参数的启动计划
- 条件 UI 部分

### references/data-management.md
**阅读此文档以了解：**
- 使用 LatchFile 和 LatchDir 进行云存储
- Registry 系统（Projects、Tables、Records）
- 链接记录和关系
- 枚举和类型化列
- 批量操作和事务
- 与工作流集成
- 账户和工作区管理

**关键主题：**
- `latch:///` 路径格式
- 文件传输和 glob 模式
- 创建和查询 Registry 表
- 列类型（string、number、file、link、enum）
- 记录 CRUD 操作
- 工作流-Registry 集成

### references/resource-configuration.md
**阅读此文档以了解：**
- 任务资源装饰器
- 自定义 CPU、内存、GPU 配置
- GPU 类型（K80、V100、A100）
- 超时和存储设置
- 资源优化策略
- 成本效益工作流设计
- 监控和调试

**关键主题：**
- `@small_task`、`@large_task`、`@small_gpu_task`、`@large_gpu_task`
- 带有精确规格的 `@custom_task`
- 多 GPU 配置
- 按工作负载类型选择资源
- 平台限制和配额

### references/verified-workflows.md
**阅读此文档以了解：**
- 预构建的生产工作流
- 批量 RNA-seq 和 DESeq2
- AlphaFold 和 ColabFold
- 单细胞分析（ArchR、scVelo）
- CRISPR 编辑分析
- 通路富集
- 与自定义工作流集成

**关键主题：**
- `latch.verified` 模块导入
- 可用的验证工作流
- 工作流参数和选项
- 结合验证和自定义步骤
- 版本管理

## 常见工作流模式

### 完整的 RNA-seq 流水线

```python
from latch import workflow, small_task, large_task
from latch.types import LatchFile, LatchDir

@small_task
def quality_control(fastq: LatchFile) -> LatchFile:
    """运行 FastQC"""
    return qc_output

@large_task
def alignment(fastq: LatchFile, genome: str) -> LatchFile:
    """STAR 比对"""
    return bam_output

@small_task
def quantification(bam: LatchFile) -> LatchFile:
    """featureCounts"""
    return counts

@workflow
def rnaseq_pipeline(
    input_fastq: LatchFile,
    genome: str,
    output_dir: LatchDir
) -> LatchFile:
    """RNA-seq 分析流水线"""
    qc = quality_control(fastq=input_fastq)
    aligned = alignment(fastq=qc, genome=genome)
    return quantification(bam=aligned)
```

### GPU 加速工作流

```python
from latch import workflow, small_task, large_gpu_task
from latch.types import LatchFile

@small_task
def preprocess(input_file: LatchFile) -> LatchFile:
    """准备数据"""
    return processed

@large_gpu_task
def gpu_computation(data: LatchFile) -> LatchFile:
    """GPU 加速分析"""
    return results

@workflow
def gpu_pipeline(input_file: LatchFile) -> LatchFile:
    """包含 GPU 任务的流水线"""
    preprocessed = preprocess(input_file=input_file)
    return gpu_computation(data=preprocessed)
```

### Registry 集成工作流

```python
from latch import workflow, small_task
from latch.registry.table import Table
from latch.registry.record import Record
from latch.types import LatchFile

@small_task
def process_and_track(sample_id: str, table_id: str) -> str:
    """处理样本并更新 Registry"""
    # 从 registry 获取样本
    table = Table.get(table_id=table_id)
    records = Record.list(table_id=table_id, filter={"sample_id": sample_id})
    sample = records[0]

    # 处理
    input_file = sample.values["fastq_file"]
    output = process(input_file)

    # 更新 registry
    sample.update(values={"status": "completed", "result": output})
    return "Success"

@workflow
def registry_workflow(sample_id: str, table_id: str):
    """与 Registry 集成的工作流"""
    return process_and_track(sample_id=sample_id, table_id=table_id)
```

## 最佳实践

### 工作流设计
1. 为所有参数使用类型注解
2. 编写清晰的文档字符串（显示在 UI 中）
3. 从标准任务装饰器开始，需要时扩展
4. 将复杂工作流分解为模块化任务
5. 实现适当的错误处理

### 数据管理
6. 使用一致的文件夹结构
7. 在批量录入前定义 Registry 模式
8. 使用链接记录表示关系
9. 在 Registry 中存储元数据以实现可追溯性

### 资源配置
10. 合理分配资源（不要过度分配）
11. 仅在算法支持时使用 GPU
12. 监控执行指标并优化
13. 尽可能设计并行执行

### 开发工作流
14. 在注册前使用 Docker 进行本地测试
15. 对工作流代码使用版本控制
16. 记录资源需求
17. 分析工作流以确定实际需求

## 故障排除

### 常见问题

**注册失败：**
- 确保 Docker 正在运行
- 使用 `latch login` 检查认证
- 验证 Dockerfile 中的所有依赖项
- 使用 `--verbose` 标志获取详细日志

**资源问题：**
- 内存不足：增加任务装饰器中的内存
- 超时：增加超时参数
- 存储问题：增加 ephemeral storage_gib

**数据访问：**
- 使用正确的 `latch:///` 路径格式
- 验证工作区中文件是否存在
- 检查共享工作区的权限

**类型错误：**
- 为所有参数添加类型注解
- 对文件/目录参数使用 LatchFile/LatchDir
- 确保工作流返回类型与实际返回匹配

## 其他资源

- **官方文档**：https://docs.latch.bio
- **GitHub 仓库**：https://github.com/latchbio/latch
- **Slack 社区**：加入 Latch SDK 工作区
- **API 参考**：https://docs.latch.bio/api/latch.html
- **博客**：https://blog.latch.bio

## 支持

如有问题或疑问：
1. 查看上述文档链接
2. 搜索 GitHub issues
3. 在 Slack 社区中提问
4. 联系 support@latch.bio
