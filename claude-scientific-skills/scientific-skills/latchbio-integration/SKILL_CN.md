---
name: latchbio-integration
description: 用于生物信息学工作流程的Latch平台。使用Latch SDK构建工作流程、@workflow/@task装饰器、部署无服务器工作流程、LatchFile/LatchDir、Nextflow/Snakemake集成。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# LatchBio集成

## 概述

Latch是一个用于构建和部署生物信息学工作流程作为无服务器管道的Python框架。在Flyte上构建，使用@workflow/@task装饰器定义工作流程，使用LatchFile/LatchDir管理云数据，配置资源，并集成Nextflow/Snakemake管道。

## 核心能力

Latch平台提供四个主要功能领域：

### 1. 工作流程创建和部署
- 使用Python装饰器定义无服务器工作流程
- 支持原生Python、Nextflow和Snakemake管道
- 使用Docker自动容器化
- 自动生成的无代码用户界面
- 版本控制和可重复性

### 2. 数据管理
- 云存储抽象（LatchFile、LatchDir）
- 使用注册表的结构化数据组织（项目 → 表 → 记录）
- 使用链接和枚举的类型安全数据操作
- 本地和云之间的自动文件传输
- 用于文件选择的Glob模式匹配

### 3. 资源配置
- 预配置的任务装饰器（@small_task、@large_task、@small_gpu_task、@large_gpu_task）
- 自定义资源规范（CPU、内存、GPU、存储）
- GPU支持（K80、V100、A100）
- 超时和存储配置
- 成本优化策略

### 4. 验证工作流程
- 生产就绪的预构建管道
- 批量RNA-seq、DESeq2、通路分析
- AlphaFold和ColabFold用于蛋白质结构预测
- 单细胞工具（ArchR、scVelo、emptyDropsR）
- CRISPR分析、系统发育和更多

## 快速开始

### 安装和设置

```bash
# 安装Latch SDK
python3 -m uv pip install latch

# 登录到Latch
latch login

# 初始化新工作流程
latch init my-workflow

# 将工作流程注册到平台
latch register my-workflow
```

**先决条件：**
- Docker已安装并运行
- Latch账户凭据
- Python 3.8+

### 基本工作流程示例

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
    我的生物信息学工作流程

    Args:
        input_file: 输入数据文件
    """
    return process_file(input_file=input_file)
```

## 何时使用此技能

在遇到以下任何场景时应使用此技能：

**工作流程开发：**
- "为RNA-seq分析创建Latch工作流程"
- "将我的管道部署到Latch"
- "将我的Nextflow管道转换为Latch"
- "为我的工作流程添加GPU支持"
- 使用 `@workflow`、`@task` 装饰器

**数据管理：**
- "在Latch注册表中组织我的测序数据"
- "如何使用LatchFile和LatchDir？"
- "在Latch中设置样本跟踪"
- 使用 `latch:///` 路径

**资源配置：**
- "在Latch上为AlphaFold配置GPU"
- "我的任务内存不足"
- "如何优化工作流程成本？"
- 使用任务装饰器

**验证工作流程：**
- "在Latch上运行AlphaFold"
- "使用DESeq2进行差异表达"
- "可用的预构建工作流程"
- 使用 `latch.verified` 模块

## 详细文档

此技能包括按功能组织的全面参考文档：

### references/workflow-creation.md
**阅读此内容以了解：**
- 创建和注册工作流程
- 任务定义和装饰器
- 支持Python、Nextflow、Snakemake
- 启动计划和条件部分
- 工作流程执行（CLI和编程）
- 多步骤和并行管道
- 注册问题故障排除

**关键主题：**
- `latch init` 和 `latch register` 命令
- `@workflow` 和 `@task` 装饰器
- LatchFile和LatchDir基础
- 类型注解和文档字符串
- 带有预设参数的启动计划
- 条件UI部分

### references/data-management.md
**阅读此内容以了解：**
- 使用LatchFile和LatchDir进行云存储
- 注册表系统（项目、表、记录）
- 链接记录和关系
- 枚举和类型化列
- 批量操作和事务
- 与工作流程集成
- 账户和工作区管理

**关键主题：**
- `latch:///` 路径格式
- 文件传输和glob模式
- 创建和查询注册表
- 列类型（字符串、数字、文件、链接、枚举）
- 记录CRUD操作
- 工作流程-注册表集成

### references/resource-configuration.md
**阅读此内容以了解：**
- 任务资源装饰器
- 自定义CPU、内存、GPU配置
- GPU类型（K80、V100、A100）
- 超时和存储设置
- 资源优化策略
- 成本效益工作流程设计
- 监控和调试

**关键主题：**
- `@small_task`、`@large_task`、`@small_gpu_task`、`@large_gpu_task`
- `@custom_task` 带有精确规范
- 多GPU配置
- 按工作负载类型进行资源选择
- 平台限制和配额

### references/verified-workflows.md
**阅读此内容以了解：**
- 预构建生产工作流程
- 批量RNA-seq和DESeq2
- AlphaFold和ColabFold
- 单细胞分析（ArchR、scVelo）
- CRISPR编辑分析
- 通路富集
- 与自定义工作流程集成

**关键主题：**
- `latch.verified` 模块导入
- 可用的验证工作流程
- 工作流程参数和选项
- 结合验证和自定义步骤
- 版本管理

## 常见工作流程模式

### 完整RNA-seq管道

```python
from latch import workflow, small_task, large_task
from latch.types import LatchFile, LatchDir

@small_task
def quality_control(fastq: LatchFile) -> LatchFile:
    """运行FastQC"""
    return qc_output

@large_task
def alignment(fastq: LatchFile, genome: str) -> LatchFile:
    """STAR比对"""
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
    """RNA-seq分析管道"""
    qc = quality_control(fastq=input_fastq)
    aligned = alignment(fastq=qc, genome=genome)
    return quantification(bam=aligned)
```

### GPU加速工作流程

```python
from latch import workflow, small_task, large_gpu_task
from latch.types import LatchFile

@small_task
def preprocess(input_file: LatchFile) -> LatchFile:
    """准备数据"""
    return processed

@large_gpu_task
def gpu_computation(data: LatchFile) -> LatchFile:
    """GPU加速分析"""
    return results

@workflow
def gpu_pipeline(input_file: LatchFile) -> LatchFile:
    """带GPU任务的管道"""
    preprocessed = preprocess(input_file=input_file)
    return gpu_computation(data=preprocessed)
```

### 注册表集成工作流程

```python
from latch import workflow, small_task
from latch.registry.table import Table
from latch.registry.record import Record
from latch.types import LatchFile

@small_task
def process_and_track(sample_id: str, table_id: str) -> str:
    """处理样本并更新注册表"""
    # 从注册表获取样本
    table = Table.get(table_id=table_id)
    records = Record.list(table_id=table_id, filter={"sample_id": sample_id})
    sample = records[0]

    # 处理
    input_file = sample.values["fastq_file"]
    output = process(input_file)

    # 更新注册表
    sample.update(values={"status": "completed", "result": output})
    return "Success"

@workflow
def registry_workflow(sample_id: str, table_id: str):
    """与注册表集成的工作流程"""
    return process_and_track(sample_id=sample_id, table_id=table_id)
```

## 最佳实践

### 工作流程设计
1. 为所有参数使用类型注解
2. 编写清晰的文档字符串（出现在UI中）
3. 从标准任务装饰器开始，如需要则扩展
4. 将复杂工作流程分解为模块化任务
5. 实现适当的错误处理

### 数据管理
6. 使用一致的文件夹结构
7. 在批量输入之前定义注册表架构
8. 使用链接记录表示关系
9. 在注册表中存储元数据以实现可追溯性

### 资源配置
10. 正确调整资源大小（不要过度分配）
11. 仅在算法支持时使用GPU
12. 监控执行指标并优化
13. 尽可能设计并行执行

### 开发工作流程
14. 在注册之前使用Docker在本地测试
15. 对工作流程代码使用版本控制
16. 记录资源需求
17. 分析工作流程以确定实际需求

## 故障排除

### 常见问题

**注册失败：**
- 确保Docker正在运行
- 使用 `latch login` 检查身份验证
- 验证Dockerfile中的所有依赖项
- 使用 `--verbose` 标志获取详细日志

**资源问题：**
- 内存不足：在任务装饰器中增加内存
- 超时：增加超时参数
- 存储问题：增加ephemeral_storage_gib

**数据访问：**
- 使用正确的 `latch:///` 路径格式
- 验证文件存在于工作区中
- 检查共享工作区的权限

**类型错误：**
- 向所有参数添加类型注解
- 对文件/目录参数使用LatchFile/LatchDir
- 确保工作流程返回类型与实际返回匹配

## 其他资源

- **官方文档**：https://docs.latch.bio
- **GitHub存储库**：https://github.com/latchbio/latch
- **Slack社区**：加入Latch SDK工作区
- **API参考**：https://docs.latch.bio/api/latch.html
- **博客**：https://blog.latch.bio

## 支持

如有问题或疑问：
1. 查看上述文档链接
2. 搜索GitHub问题
3. 在Slack社区中提问
4. 联系support@latch.bio
