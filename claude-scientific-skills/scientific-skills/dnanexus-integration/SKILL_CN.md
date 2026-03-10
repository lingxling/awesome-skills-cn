---
name: dnanexus-integration
description: DNAnexus 云基因组学平台。构建应用/小程序、管理数据（上传/下载）、dxpy Python SDK、运行工作流、FASTQ/BAM/VCF，用于基因组学管道开发和执行。
license: Unknown
compatibility: 需要 DNAnexus 账户
metadata:
    skill-author: K-Dense Inc.
---

# DNAnexus 集成

## 概述

DNAnexus 是一个用于生物医学数据分析和基因组学的云平台。构建和部署应用/小程序、管理数据对象、运行工作流，并使用 dxpy Python SDK 进行基因组学管道开发和执行。

## 何时使用此技能

此技能应在以下情况下使用：
- 创建、构建或修改 DNAnexus 应用/小程序
- 上传、下载、搜索或组织文件和记录
- 运行分析、监控作业、创建工作流
- 编写使用 dxpy 与平台交互的脚本
- 设置 dxapp.json、管理依赖项、使用 Docker
- 处理 FASTQ、BAM、VCF 或其他生物信息学文件
- 管理项目、权限或平台资源

## 核心能力

此技能组织为五个主要领域，每个领域都有详细的参考文档：

### 1. 应用开发

**用途**：创建在 DNAnexus 平台上运行的可执行程序（应用/小程序）。

**关键操作**：
- 使用 `dx-app-wizard` 生成应用骨架
- 使用适当的入口点编写 Python 或 Bash 应用
- 处理输入/输出数据对象
- 使用 `dx build` 或 `dx build --app` 部署
- 在平台上测试应用

**常见用例**：
- 生物信息学管道（比对、变异调用）
- 数据处理工作流
- 质量控制和过滤
- 格式转换工具

**参考**：有关完整的应用结构和模式、Python 入口点装饰器、使用 dxpy 进行输入/输出处理、开发最佳实践以及常见问题和解决方案，请参阅 `references/app-development.md`。

### 2. 数据操作

**用途**：管理平台上的文件、记录和其他数据对象。

**关键操作**：
- 使用 `dxpy.upload_local_file()` 和 `dxpy.download_dxfile()` 上传/下载文件
- 使用元数据创建和管理记录
- 按名称、属性或类型搜索数据对象
- 在项目之间克隆数据
- 管理项目文件夹和权限

**常见用例**：
- 上传测序数据（FASTQ 文件）
- 组织分析结果
- 搜索特定样本或实验
- 跨项目备份数据
- 管理参考基因组和注释

**参考**：有关完整的文件和记录操作、数据对象生命周期（打开/关闭状态）、搜索和发现模式、项目管理和批处理操作，请参阅 `references/data-operations.md`。

### 3. 作业执行

**用途**：运行分析、监控执行和编排工作流。

**关键操作**：
- 使用 `applet.run()` 或 `app.run()` 启动作业
- 监控作业状态和日志
- 为并行处理创建子作业
- 构建和运行多步工作流
- 使用输出引用链接作业

**常见用例**：
- 在测序数据上运行基因组学分析
- 多个样本的并行处理
- 多步分析管道
- 监控长时间运行的计算
- 调试失败的作业

**参考**：有关完整的作业生命周期和状态、工作流创建和编排、并行执行模式、作业监控和调试以及资源管理，请参阅 `references/job-execution.md`。

### 4. Python SDK (dxpy)

**用途**：通过 Python 对 DNAnexus 平台进行编程访问。

**关键操作**：
- 使用数据对象处理程序（DXFile、DXRecord、DXApplet 等）
- 将高级函数用于常见任务
- 对高级操作进行直接 API 调用
- 在对象之间创建链接和引用
- 搜索和发现平台资源

**常见用例**：
- 数据管理自动化脚本
- 自定义分析管道
- 批处理工作流
- 与外部工具集成
- 数据迁移和组织

**参考**：有关完整的 dxpy 类参考、高级实用函数、API 方法文档、错误处理模式和常见代码模式，请参阅 `references/python-sdk.md`。

### 5. 配置和依赖项

**用途**：配置应用元数据和管理依赖项。

**关键操作**：
- 编写带有输入、输出和运行规范的 dxapp.json
- 安装系统包（execDepends）
- 捆绑自定义工具和资源
- 使用共享依赖项的资源
- 集成 Docker 容器
- 配置实例类型和超时

**常见用例**：
- 定义应用输入/输出规范
- 安装生物信息学工具（samtools、bwa 等）
- 管理 Python 包依赖项
- 使用复杂环境的 Docker 镜像
- 选择计算资源

**参考**：有关完整的 dxapp.json 规范、依赖项管理策略、Docker 集成模式、区域和资源配置以及示例配置，请参阅 `references/configuration.md`。

## 快速入门示例

### 上传和分析数据

```python
import dxpy

# 上传输入文件
input_file = dxpy.upload_local_file("sample.fastq", project="project-xxxx")

# 运行分析
job = dxpy.DXApplet("applet-xxxx").run({
    "reads": dxpy.dxlink(input_file.get_id())
})

# 等待完成
job.wait_on_done()

# 下载结果
output_id = job.describe()["output"]["aligned_reads"]["$dnanexus_link"]
dxpy.download_dxfile(output_id, "aligned.bam")
```

### 搜索和下载文件

```python
import dxpy

# 查找来自特定实验的 BAM 文件
files = dxpy.find_data_objects(
    classname="file",
    name="*.bam",
    properties={"experiment": "exp001"},
    project="project-xxxx"
)

# 下载每个文件
for file_result in files:
    file_obj = dxpy.DXFile(file_result["id"])
    filename = file_obj.describe()["name"]
    dxpy.download_dxfile(file_result["id"], filename)
```

### 创建简单应用

```python
# src/my-app.py
import dxpy
import subprocess

@dxpy.entry_point('main')
def main(input_file, quality_threshold=30):
    # 下载输入
    dxpy.download_dxfile(input_file["$dnanexus_link"], "input.fastq")

    # 处理
    subprocess.check_call([
        "quality_filter",
        "--input", "input.fastq",
        "--output", "filtered.fastq",
        "--threshold", str(quality_threshold)
    ])

    # 上传输出
    output_file = dxpy.upload_local_file("filtered.fastq")

    return {
        "filtered_reads": dxpy.dxlink(output_file)
    }

dxpy.run()
```

## 工作流决策树

使用 DNAnexus 时，遵循此决策树：

1. **需要创建新的可执行文件吗？**
   - 是 → 使用**应用开发**（references/app-development.md）
   - 否 → 继续到步骤 2

2. **需要管理文件或数据吗？**
   - 是 → 使用**数据操作**（references/data-operations.md）
   - 否 → 继续到步骤 3

3. **需要运行分析或工作流吗？**
   - 是 → 使用**作业执行**（references/job-execution.md）
   - 否 → 继续到步骤 4

4. **编写用于自动化的 Python 脚本吗？**
   - 是 → 使用**Python SDK**（references/python-sdk.md）
   - 否 → 继续到步骤 5

5. **配置应用设置或依赖项吗？**
   - 是 → 使用**配置**（references/configuration.md）

通常您需要结合多种能力（例如，应用开发 + 配置，或数据操作 + 作业执行）。

## 安装和身份验证

### 安装 dxpy

```bash
uv pip install dxpy
```

### 登录 DNAnexus

```bash
dx login
```

这将验证您的会话并设置对项目和数据的访问。

### 验证安装

```bash
dx --version
dx whoami
```

## 常见模式

### 模式 1：批处理

使用相同分析处理多个文件：

```python
# 查找所有 FASTQ 文件
files = dxpy.find_data_objects(
    classname="file",
    name="*.fastq",
    project="project-xxxx"
)

# 启动并行作业
jobs = []
for file_result in files:
    job = dxpy.DXApplet("applet-xxxx").run({
        "input": dxpy.dxlink(file_result["id"])
    })
    jobs.append(job)

# 等待所有完成
for job in jobs:
    job.wait_on_done()
```

### 模式 2：多步管道

链接多个分析：

```python
# 步骤 1：质量控制
qc_job = qc_applet.run({"reads": input_file})

# 步骤 2：比对（使用 QC 输出）
align_job = align_applet.run({
    "reads": qc_job.get_output_ref("filtered_reads")
})

# 步骤 3：变异调用（使用比对输出）
variant_job = variant_applet.run({
    "bam": align_job.get_output_ref("aligned_bam")
})
```

### 模式 3：数据组织

系统地组织分析结果：

```python
# 创建有组织的文件夹结构
dxpy.api.project_new_folder(
    "project-xxxx",
    {"folder": "/experiments/exp001/results", "parents": True}
)

# 带元数据上传
result_file = dxpy.upload_local_file(
    "results.txt",
    project="project-xxxx",
    folder="/experiments/exp001/results",
    properties={
        "experiment": "exp001",
        "sample": "sample1",
        "analysis_date": "2025-10-20"
    },
    tags=["validated", "published"]
)
```

## 最佳实践

1. **错误处理**：始终在 try-except 块中包装 API 调用
2. **资源管理**：为工作负载选择适当的实例类型
3. **数据组织**：使用一致的文件夹结构和元数据
4. **成本优化**：归档旧数据，使用适当的存储类别
5. **文档**：在 dxapp.json 中包含清晰的描述
6. **测试**：在生产使用前用各种输入类型测试应用
7. **版本控制**：对应用使用语义版本控制
8. **安全性**：永远不要在源代码中硬编码凭据
9. **日志记录**：包含用于调试的信息性日志消息
10. **清理**：删除临时文件和失败的作业

## 资源

此技能包含详细的参考文档：

### references/

- **app-development.md** - 构建和部署应用/小程序的完整指南
- **data-operations.md** - 文件管理、记录、搜索和项目操作
- **job-execution.md** - 运行作业、工作流、监控和并行处理
- **python-sdk.md** - 全面的 dxpy 库参考，包含所有类和函数
- **configuration.md** - dxapp.json 规范和依赖项管理

当您需要有关特定操作或复杂任务的详细信息时，请加载这些参考。

## 获取帮助

- 官方文档：https://documentation.dnanexus.com/
- API 参考：http://autodoc.dnanexus.com/
- GitHub 仓库：https://github.com/dnanexus/dx-toolkit
- 支持：support@dnanexus.com
