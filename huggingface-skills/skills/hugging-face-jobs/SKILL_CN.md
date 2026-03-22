---
name: hugging-face-jobs
description: 当用户想要在 Hugging Face Jobs 基础设施上运行任何工作负载时使用此技能。涵盖 UV 脚本、基于 Docker 的作业、硬件选择、成本估算、使用令牌进行身份验证、机密管理、超时配置和结果持久化。专为通用计算工作负载设计,包括数据处理、推理、实验、批处理作业和任何基于 Python 的任务。应在涉及云计算、GPU 工作负载或用户提及在 Hugging Face 基础设施上运行作业而无需本地设置时调用。
license: 完整条款见 LICENSE.txt
---

# 在 Hugging Face Jobs 上运行工作负载

## 概述

在完全托管的 Hugging Face 基础设施上运行任何工作负载。无需本地设置 — 作业在云 CPU、GPU 或 TPU 上运行,并且可以将结果持久化到 Hugging Face Hub。

**常见用例:**
- **数据处理** - 转换、过滤或分析大型数据集
- **批处理推理** - 对数千个样本运行推理
- **实验和基准测试** - 可重现的 ML 实验
- **模型训练** - 微调模型(参见 `model-trainer` 技能以获取基于 TRL 的训练工作流程)
- **合成数据生成** - 使用 LLM 生成数据集
- **开发和测试** - 在没有本地 GPU 设置的情况下测试代码
- **计划作业** - 自动化重复性任务

**专门用于模型训练:** 参见 `model-trainer` 技能以获取基于 TRL 的训练工作流程。

## 何时使用此技能

当用户想要以下操作时使用此技能:
- 在云基础设施上运行 Python 工作负载
- 在没有本地 GPU/TPU 设置的情况下执行作业
- 大规模处理数据
- 运行批处理推理或实验
- 计划重复性任务
- 对任何工作负载使用 GPU/TPU
- 将结果持久化到 Hugging Face Hub

## 关键指令

协助作业时:

1. **始终使用 `hf_jobs()` MCP 工具** - 使用 `hf_jobs("uv", {...})` 或 `hf_jobs("run", {...})` 提交作业。`script` 参数直接接受 Python 代码。除非用户明确要求,否则不要保存到本地文件。将脚本内容作为字符串传递给 `hf_jobs()`。

2. **始终处理身份验证** - 与 Hub 交互的作业需要通过机密使用 `HF_TOKEN`。参见下面的令牌使用部分。

3. **提交后提供作业详细信息** - 提交后,提供作业 ID、监控 URL、预计时间,并注意用户可以稍后请求状态检查。

4. **设置适当的超时** - 默认 30 分钟对于长时间运行的任务可能不足。

## 先决条件检查表

开始任何作业之前,验证:

### ✅ **帐户和身份验证**
- Hugging Face 帐户,具有 [Pro](https://hf.co/pro)、[Team](https://hf.co/enterprise) 或 [Enterprise](https://hf.co/enterprise) 计划(Jobs 需要付费计划)
- 已身份验证登录: 使用 `hf_whoami()` 检查
- **用于 Hub 访问的 HF_TOKEN** ⚠️ 关键 - 对于任何 Hub 操作(推送模型/数据集、下载私有存储库等)都是必需的
- 令牌必须具有适当的权限(下载需要读取,上传需要写入)

### ✅ **令牌使用**(详细信息见令牌使用部分)

**何时需要令牌:**
- 将模型/数据集推送到 Hub
- 访问私有存储库
- 在脚本中使用 Hub API
- 任何经过身份验证的 Hub 操作

**如何提供令牌:**
```python
{
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # 推荐: 自动令牌
}
```

**⚠️ 关键:** `$HF_TOKEN` 占位符会自动替换为您的实际令牌。永远不要在脚本中硬编码令牌。

## 令牌使用指南

### 了解令牌

**什么是 HF 令牌?**
- Hugging Face Hub 的身份验证凭据
- 对于经过身份验证的操作(推送、私有存储库、API 访问)是必需的
- 在 `hf auth login` 后安全地存储在您的机器上

**令牌类型:**
- **读取令牌** - 可以下载模型/数据集、读取私有存储库
- **写入令牌** - 可以推送模型/数据集、创建存储库、修改内容
- **组织令牌** - 可以代表组织操作

### 何时需要令牌

**始终需要:**
- 将模型/数据集推送到 Hub
- 访问私有存储库
- 创建新存储库
- 修改现有存储库
- 以编程方式使用 Hub API

**不需要:**
- 下载公共模型/数据集
- 运行不与 Hub 交互的作业
- 读取公共存储库信息

### 如何向作业提供令牌

#### 方法 1: 自动令牌(推荐)

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 自动替换
})
```

**工作原理:**
- `$HF_TOKEN` 是一个占位符,会被您的实际令牌替换
- 使用您登录会话中的令牌(`hf auth login`)
- 最安全和最方便的方法
- 作为机密传递时,令牌在服务器端加密

**优点:**
- 代码中没有令牌暴露
- 使用您当前的登录会话
- 如果您重新登录会自动更新
- 与 MCP 工具无缝协作

#### 方法 2: 显式令牌(不推荐)

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "secrets": {"HF_TOKEN": "hf_abc123..."}  # ⚠️ 硬编码令牌
})
```

**何时使用:**
- 仅当自动令牌不起作用时
- 使用特定令牌进行测试
- 组织令牌(谨慎使用)

**安全问题:**
- 令牌在代码/日志中可见
- 如果令牌轮换必须手动更新
- 令牌暴露风险

#### 方法 3: 环境变量(安全性较低)

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "env": {"HF_TOKEN": "hf_abc123..."}  # ⚠️ 比机密安全性低
})
```

与机密的区别:
- `env` 变量在作业日志中可见
- `secrets` 在服务器端加密
- 对于令牌始终首选 `secrets`

### 在脚本中使用令牌

**在您的 Python 脚本中,令牌作为环境变量可用:**

```python
# /// script
# dependencies = ["huggingface-hub"]
# ///

import os
from huggingface_hub import HfApi

# 如果通过机密传递,令牌自动可用
token = os.environ.get("HF_TOKEN")

# 与 Hub API 一起使用
api = HfApi(token=token)

# 或让 huggingface_hub 自动检测
api = HfApi()  # 自动使用 HF_TOKEN 环境变量
```

**最佳实践:**
- 不要在脚本中硬编码令牌
- 使用 `os.environ.get("HF_TOKEN")` 访问
- 尽可能让 `huggingface_hub` 自动检测
- 在 Hub 操作之前验证令牌存在

### 令牌验证

**检查您是否已登录:**
```python
from huggingface_hub import whoami
user_info = whoami()  # 如果已身份验证则返回您的用户名
```

**验证作业中的令牌:**
```python
import os
assert "HF_TOKEN" in os.environ, "HF_TOKEN not found!"
token = os.environ["HF_TOKEN"]
print(f"Token starts with: {token[:7]}...")  # 应该以 "hf_" 开头
```

### 常见令牌问题

**错误: 401 Unauthorized**
- **原因:** 令牌缺失或无效
- **修复:** 在作业配置中添加 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
- **验证:** 检查 `hf_whoami()` 是否在本地工作

**错误: 403 Forbidden**
- **原因:** 令牌缺少所需权限
- **修复:** 确保令牌具有推送操作的写入权限
- **检查:** 在 https://huggingface.co/settings/tokens 检查令牌类型

**错误: Token not found in environment**
- **原因:** 未传递 `secrets` 或键名错误
- **修复:** 使用 `secrets={"HF_TOKEN": "$HF_TOKEN"}`(不是 `env`)
- **验证:** 脚本检查 `os.environ.get("HF_TOKEN")`

**错误: Repository access denied**
- **原因:** 令牌没有对私有存储库的访问权限
- **修复:** 使用具有访问权限的帐户的令牌
- **检查:** 验证存储库可见性和您的权限

### 令牌安全最佳实践

1. **永远不要提交令牌** - 使用 `$HF_TOKEN` 占位符或环境变量
2. **使用机密,而不是 env** - 机密在服务器端加密
3. **定期轮换令牌** - 定期生成新令牌
4. **使用最小权限** - 创建仅具有所需权限的令牌
5. **不要共享令牌** - 每个用户应该使用自己的令牌
6. **监控令牌使用情况** - 在 Hub 设置中检查令牌活动

### 完整令牌示例

```python
# 示例: 将结果推送到 Hub
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["huggingface-hub", "datasets"]
# ///

import os
from huggingface_hub import HfApi
from datasets import Dataset

# 验证令牌可用
assert "HF_TOKEN" in os.environ, "HF_TOKEN required!"

# 使用令牌进行 Hub 操作
api = HfApi(token=os.environ["HF_TOKEN"])

# 创建并推送数据集
data = {"text": ["Hello", "World"]}
dataset = Dataset.from_dict(data)
dataset.push_to_hub("username/my-dataset", token=os.environ["HF_TOKEN"])

print("✅ Dataset pushed successfully!")
""",
    "flavor": "cpu-basic",
    "timeout": "30m",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 安全地提供令牌
})
```

## 快速入门: 两种方法

### 方法 1: UV 脚本(推荐)

UV 脚本使用 PEP 723 内联依赖项,以实现干净、自包含的工作负载。

**MCP 工具:**
```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["transformers", "torch"]
# ///

from transformers import pipeline
import torch

# 您的工作负载在这里
classifier = pipeline("sentiment-analysis")
result = classifier("I love Hugging Face!")
print(result)
""",
    "flavor": "cpu-basic",
    "timeout": "30m"
})
```

**CLI 等效:**
```bash
hf jobs uv run my_script.py --flavor cpu-basic --timeout 30m
```

**Python API:**
```python
from huggingface_hub import run_uv_job
run_uv_job("my_script.py", flavor="cpu-basic", timeout="30m")
```

**优点:** 直接 MCP 工具使用、干净的代码、内联声明的依赖项、无需文件保存

**何时使用:** 所有工作负载的默认选择、自定义逻辑、任何需要 `hf_jobs()` 的场景

#### UV 脚本的自定义 Docker 镜像

默认情况下,UV 脚本使用 `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`。对于具有复杂依赖项的 ML 工作负载,使用预构建的镜像:

```python
hf_jobs("uv", {
    "script": "inference.py",
    "image": "vllm/vllm-openai:latest",  # 带有 vLLM 的预构建镜像
    "flavor": "a10g-large"
})
```

**CLI:**
```bash
hf jobs uv run --image vllm/vllm-openai:latest --flavor a10g-large inference.py
```

**优点:** 更快的启动、预安装的依赖项、针对特定框架优化

#### Python 版本

默认情况下,UV 脚本使用 Python 3.12。指定不同的版本:

```python
hf_jobs("uv", {
    "script": "my_script.py",
    "python": "3.11",  # 使用 Python 3.11
    "flavor": "cpu-basic"
})
```

**Python API:**
```python
from huggingface_hub import run_uv_job
run_uv_job("my_script.py", python="3.11")
```

#### 使用脚本

⚠️ **重要:** 根据您运行 Jobs 的方式,有 *两种*"脚本路径"场景:

- **使用 `hf_jobs()` MCP 工具(在此仓库中推荐)**: `script` 值必须是 **内联代码**(字符串)或 **URL**。本地文件系统路径(如 `"./scripts/foo.py"`)在远程容器中不存在。
- **使用 `hf jobs uv run` CLI**: 本地文件路径 **确实有效**(CLI 会上传您的脚本)。

**使用 `hf_jobs()` MCP 工具时的常见错误:**

```python
# ❌ 将失败(远程容器看不到您的本地路径)
hf_jobs("uv", {"script": "./scripts/foo.py"})
```

**使用 `hf_jobs()` MCP 工具的正确模式:**

```python
# ✅ 内联: 读取本地脚本文件并传递其 *内容*
from pathlib import Path
script = Path("hf-jobs/scripts/foo.py").read_text()
hf_jobs("uv", {"script": script})

# ✅ URL: 将脚本托管在可访问的地方
hf_jobs("uv", {"script": "https://huggingface.co/datasets/uv-scripts/.../raw/main/foo.py"})

# ✅ 来自 GitHub 的 URL
hf_jobs("uv", {"script": "https://raw.githubusercontent.com/huggingface/trl/main/trl/scripts/sft.py"})
```

**CLI 等效(支持本地路径):**

```bash
hf jobs uv run ./scripts/foo.py -- --your --args
```

#### 在运行时添加依赖项

添加 PEP 723 标头中未包含的额外依赖项:

```python
hf_jobs("uv", {
    "script": "inference.py",
    "dependencies": ["transformers", "torch>=2.0"],  # 额外依赖项
    "flavor": "a10g-small"
})
```

**Python API:**
```python
from huggingface_hub import run_uv_job
run_uv_job("inference.py", dependencies=["transformers", "torch>=2.0"])
```

### 方法 2: 基于 Docker 的作业

使用自定义 Docker 镜像和命令运行作业。

**MCP 工具:**
```python
hf_jobs("run", {
    "image": "python:3.12",
    "command": ["python", "-c", "print('Hello from HF Jobs!')"],
    "flavor": "cpu-basic",
    "timeout": "30m"
})
```

**CLI 等效:**
```bash
hf jobs run python:3.12 python -c "print('Hello from HF Jobs!')"
```

**Python API:**
```python
from huggingface_hub import run_job
run_job(image="python:3.12", command=["python", "-c", "print('Hello!')"], flavor="cpu-basic")
```

**优点:** 完整的 Docker 控制、使用预构建的镜像、运行任何命令
**何时使用:** 需要特定的 Docker 镜像、非 Python 工作负载、复杂环境

**使用 GPU 的示例:**
```python
hf_jobs("run", {
    "image": "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel",
    "command": ["python", "-c", "import torch; print(torch.cuda.get_device_name())"],
    "flavor": "a10g-small",
    "timeout": "1h"
})
```

**使用 Hugging Face Spaces 作为镜像:**

您可以使用来自 HF Spaces 的 Docker 镜像:
```python
hf_jobs("run", {
    "image": "hf.co/spaces/lhoestq/duckdb",  # Space 作为 Docker 镜像
    "command": ["duckdb", "-c", "SELECT 'Hello from DuckDB!'"],
    "flavor": "cpu-basic"
})
```

**CLI:**
```bash
hf jobs run hf.co/spaces/lhoestq/duckdb duckdb -c "SELECT 'Hello!'"
```

### 在 Hub 上查找更多 UV 脚本

`uv-scripts` 组织提供存储在 Hugging Face Hub 上的即用型 UV 脚本:

```python
# 发现可用的 UV 脚本集合
dataset_search({"author": "uv-scripts", "sort": "downloads", "limit": 20})

# 探索特定集合
hub_repo_details(["uv-scripts/classification"], repo_type="dataset", include_readme=True)
```

**热门集合:** OCR、分类、合成数据、vLLM、数据集创建

## 硬件选择

> **参考:** [HF Jobs 硬件文档](https://huggingface.co/docs/hub/en/spaces-config-reference) (更新于 07/2025)

| 工作负载类型 | 推荐硬件 | 用例 |
|---------------|---------------------|----------|
| 数据处理、测试 | `cpu-basic`、`cpu-upgrade` | 轻量级任务 |
| 小型模型、演示 | `t4-small` | <1B 模型、快速测试 |
| 中型模型 | `t4-medium`、`l4x1` | 1-7B 模型 |
| 大型模型、生产 | `a10g-small`、`a10g-large` | 7-13B 模型 |
| 超大型模型 | `a100-large` | 13B+ 模型 |
| 批处理推理 | `a10g-large`、`a100-large` | 高吞吐量 |
| 多 GPU 工作负载 | `l4x4`、`a10g-largex2`、`a10g-largex4` | 并行/大型模型 |
| TPU 工作负载 | `v5e-1x1`、`v5e-2x2`、`v5e-2x4` | JAX/Flax、TPU 优化 |

**所有可用类型:**
- **CPU:** `cpu-basic`、`cpu-upgrade`
- **GPU:** `t4-small`、`t4-medium`、`l4x1`、`l4x4`、`a10g-small`、`a10g-large`、`a10g-largex2`、`a10g-largex4`、`a100-large`
- **TPU:** `v5e-1x1`、`v5e-2x2`、`v5e-2x4`

**指南:**
- 从较小的硬件开始进行测试
- 根据实际需求扩展
- 对并行工作负载或大型模型使用多 GPU
- 对 JAX/Flax 工作负载使用 TPU
- 参见 `references/hardware_guide.md` 了解详细规格

## 关键: 保存结果

**⚠️ 临时环境 — 必须持久化结果**

Jobs 环境是临时的。作业结束时所有文件都会被删除。如果不持久化结果,**所有工作都将丢失**。

### 持久化选项

**1. 推送到 Hugging Face Hub(推荐)**

```python
# 推送模型
model.push_to_hub("username/model-name", token=os.environ["HF_TOKEN"])

# 推送数据集
dataset.push_to_hub("username/dataset-name", token=os.environ["HF_TOKEN"])

# 推送工件
api.upload_file(
    path_or_fileobj="results.json",
    path_in_repo="results.json",
    repo_id="username/results",
    token=os.environ["HF_TOKEN"]
)
```

**2. 使用外部存储**

```python
# 上传到 S3、GCS 等
import boto3
s3 = boto3.client('s3')
s3.upload_file('results.json', 'my-bucket', 'results.json')
```

**3. 通过 API 发送结果**

```python
# 将结果 POST 到您的 API
import requests
requests.post("https://your-api.com/results", json=results)
```

### Hub 推送所需的配置

**在作业提交中:**
```python
{
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # 启用身份验证
}
```

**在脚本中:**
```python
import os
from huggingface_hub import HfApi

# 令牌从机密自动可用
api = HfApi(token=os.environ.get("HF_TOKEN"))

# 推送您的结果
api.upload_file(...)
```

### 验证检查表

提交之前:
- [ ] 已选择结果持久化方法
- [ ] 如果使用 Hub,`secrets={"HF_TOKEN": "$HF_TOKEN"}`
- [ ] 脚本优雅地处理缺失的令牌
- [ ] 测试持久化路径有效

**参见:** `references/hub_saving.md` 了解详细的 Hub 持久化指南

## 超时管理

**⚠️ 默认值: 30 分钟**

作业在超时后自动停止。对于长时间运行的任务(如训练),始终设置自定义超时。

### 设置超时

**MCP 工具:**
```python
{
    "timeout": "2h"   # 2 小时
}
```

**支持的格式:**
- 整数/浮点数: 秒(例如,`300` = 5 分钟)
- 带后缀的字符串: `"5m"`(分钟)、`"2h"`(小时)、`"1d"`(天)
- 示例: `"90m"`、`"2h"`、`"1.5h"`、`300`、`"1d"`

**Python API:**
```python
from huggingface_hub import run_job, run_uv_job

run_job(image="python:3.12", command=[...], timeout="2h")
run_uv_job("script.py", timeout=7200)  # 2 小时,以秒为单位
```

### 超时指南

| 场景 | 推荐 | 说明 |
|----------|-------------|-------|
| 快速测试 | 10-30 分钟 | 验证设置 |
| 数据处理 | 1-2 小时 | 取决于数据大小 |
| 批处理推理 | 2-4 小时 | 大批量 |
| 实验 | 4-8 小时 | 多次运行 |
| 长时间运行 | 8-24 小时 | 生产工作负载 |

**始终添加 20-30% 缓冲** 用于设置、网络延迟和清理。

**超时时:** 作业立即被终止,所有未保存的进度丢失

## 成本估算

**一般指南:**

```
总成本 = (运行时间小时数) × (每小时成本)
```

**示例计算:**

**快速测试:**
- 硬件: cpu-basic($0.10/小时)
- 时间: 15 分钟(0.25 小时)
- 成本: $0.03

**数据处理:**
- 硬件: l4x1($2.50/小时)
- 时间: 2 小时
- 成本: $5.00

**批处理推理:**
- 硬件: a10g-large($5/小时)
- 时间: 4 小时
- 成本: $20.00

**成本优化提示:**
1. 从小处开始 - 在 cpu-basic 或 t4-small 上测试
2. 监控运行时间 - 设置适当的超时
3. 使用检查点 - 如果作业失败则恢复
4. 优化代码 - 减少不必要的计算
5. 选择合适的硬件 - 不要过度配置

## 监控和跟踪

### 检查作业状态

**MCP 工具:**
```python
# 列出所有作业
hf_jobs("ps")

# 检查特定作业
hf_jobs("inspect", {"job_id": "your-job-id"})

# 查看日志
hf_jobs("logs", {"job_id": "your-job-id"})

# 取消作业
hf_jobs("cancel", {"job_id": "your-job-id"})
```

**Python API:**
```python
from huggingface_hub import list_jobs, inspect_job, fetch_job_logs, cancel_job

# 列出您的作业
jobs = list_jobs()

# 仅列出正在运行的作业
running = [j for j in list_jobs() if j.status.stage == "RUNNING"]

# 检查特定作业
job_info = inspect_job(job_id="your-job-id")

# 查看日志
for log in fetch_job_logs(job_id="your-job-id"):
    print(log)

# 取消作业
cancel_job(job_id="your-job-id")
```

**CLI:**
```bash
hf jobs ps                    # 列出作业
hf jobs logs <job-id>         # 查看日志
hf jobs cancel <job-id>       # 取消作业
```

**记住:** 等待用户请求状态检查。避免重复轮询。

### 作业 URL

提交后,作业具有监控 URL:
```
https://huggingface.co/jobs/username/job-id
```

在浏览器中查看日志、状态和详细信息。

### 等待多个作业

```python
import time
from huggingface_hub import inspect_job, run_job

# 运行多个作业
jobs = [run_job(image=img, command=cmd) for img, cmd in workloads]

# 等待所有作业完成
for job in jobs:
    while inspect_job(job_id=job.id).status.stage not in ("COMPLETED", "ERROR"):
        time.sleep(10)
```

## 计划作业

使用 CRON 表达式或预定义计划在计划上运行作业。

**MCP 工具:**
```python
# 计划每小时运行的 UV 脚本
hf_jobs("scheduled uv", {
    "script": "your_script.py",
    "schedule": "@hourly",
    "flavor": "cpu-basic"
})

# 使用 CRON 语法计划
hf_jobs("scheduled uv", {
    "script": "your_script.py",
    "schedule": "0 9 * * 1",  # 每周一上午 9 点
    "flavor": "cpu-basic"
})

# 计划基于 Docker 的作业
hf_jobs("scheduled run", {
    "image": "python:3.12",
    "command": ["python", "-c", "print('Scheduled!')"],
    "schedule": "@daily",
    "flavor": "cpu-basic"
})
```

**Python API:**
```python
from huggingface_hub import create_scheduled_job, create_scheduled_uv_job

# 计划 Docker 作业
create_scheduled_job(
    image="python:3.12",
    command=["python", "-c", "print('Running on schedule!')"],
    schedule="@hourly"
)

# 计划 UV 脚本
create_scheduled_uv_job("my_script.py", schedule="@daily", flavor="cpu-basic")

# 使用 GPU 计划
create_scheduled_uv_job(
    "ml_inference.py",
    schedule="0 */6 * * *",  # 每 6 小时
    flavor="a10g-small"
)
```

**可用计划:**
- `@annually`、`@yearly` - 每年一次
- `@monthly` - 每月一次
- `@weekly` - 每周一次
- `@daily` - 每天一次
- `@hourly` - 每小时一次
- CRON 表达式 - 自定义计划(例如,`"*/5 * * * *"` 表示每 5 分钟)

**管理计划作业:**
```python
# MCP 工具
hf_jobs("scheduled ps")                              # 列出计划作业
hf_jobs("scheduled inspect", {"job_id": "..."})     # 检查详细信息
hf_jobs("scheduled suspend", {"job_id": "..."})     # 暂停
hf_jobs("scheduled resume", {"job_id": "..."})      # 恢复
hf_jobs("scheduled delete", {"job_id": "..."})      # 删除
```

**管理作业的 Python API:**
```python
from huggingface_hub import (
    list_scheduled_jobs,
    inspect_scheduled_job,
    suspend_scheduled_job,
    resume_scheduled_job,
    delete_scheduled_job
)

# 列出所有计划作业
scheduled = list_scheduled_jobs()

# 检查计划作业
info = inspect_scheduled_job(scheduled_job_id)

# 暂停(暂停)计划作业
suspend_scheduled_job(scheduled_job_id)

# 恢复计划作业
resume_scheduled_job(scheduled_job_id)

# 删除计划作业
delete_scheduled_job(scheduled_job_id)
```

## Webhooks: 在事件上触发作业

当 Hugging Face 存储库中发生更改时自动触发作业。

**Python API:**
```python
from huggingface_hub import create_webhook

# 创建在存储库更改时触发作业的 webhook
webhook = create_webhook(
    job_id=job.id,
    watched=[
        {"type": "user", "name": "your-username"},
        {"type": "org", "name": "your-org-name"}
    ],
    domains=["repo", "discussion"],
    secret="your-secret"
)
```

**工作原理:**
1. Webhook 侦听监视的存储库中的更改
2. 触发时,作业使用 `WEBHOOK_PAYLOAD` 环境变量运行
3. 您的脚本可以解析负载以了解发生了什么

**用例:**
- 上传新数据集时自动处理
- 模型更新时触发推理
- 代码更改时运行测试
- 在存储库活动上生成报告

**在脚本中访问 webhook 负载:**
```python
import os
import json

payload = json.loads(os.environ.get("WEBHOOK_PAYLOAD", "{}"))
print(f"Event type: {payload.get('event', {}).get('action')}")
```

参见 [Webhooks 文档](https://huggingface.co/docs/huggingface_hub/guides/webhooks) 了解更多详细信息。

## 常见工作负载模式

此仓库在 `hf-jobs/scripts/` 中提供即用型 UV 脚本。优先使用它们而不是发明新模板。

### 模式 1: 数据集 → 模型响应(vLLM) — `scripts/generate-responses.py`

**作用:** 加载 Hub 数据集(聊天 `messages` 或 `prompt` 列),应用模型聊天模板,使用 vLLM 生成响应,并将输出数据集 + 数据集卡片**推送**回 Hub。

**需要:** GPU + **写入**令牌(它推送数据集)。

```python
from pathlib import Path

script = Path("hf-jobs/scripts/generate-responses.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": [
        "username/input-dataset",
        "username/output-dataset",
        "--messages-column", "messages",
        "--model-id", "Qwen/Qwen3-30B-A3B-Instruct-2507",
        "--temperature", "0.7",
        "--top-p", "0.8",
        "--max-tokens", "2048",
    ],
    "flavor": "a10g-large",
    "timeout": "4h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

### 模式 2: CoT Self-Instruct 合成数据 — `scripts/cot-self-instruct.py`

**作用:** 通过 CoT Self-Instruct 生成合成提示/答案,可选地过滤输出(答案一致性/RIP),然后将生成的数据集 + 数据集卡片**推送**到 Hub。

**需要:** GPU + **写入**令牌(它推送数据集)。

```python
from pathlib import Path

script = Path("hf-jobs/scripts/cot-self-instruct.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": [
        "--seed-dataset", "davanstrien/s1k-reasoning",
        "--output-dataset", "username/synthetic-math",
        "--task-type", "reasoning",
        "--num-samples", "5000",
        "--filter-method", "answer-consistency",
    ],
    "flavor": "l4x4",
    "timeout": "8h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

### 模式 3: 流式数据集统计(Polars + HF Hub) — `scripts/finepdfs-stats.py`

**作用:** 直接从 Hub 扫描 parquet(无需 300GB 下载),计算时间统计,并(可选)将结果上传到 Hub 数据集存储库。

**需要:** CPU 通常足够;仅在传递 `--output-repo`(上传)时需要令牌。

```python
from pathlib import Path

script = Path("hf-jobs/scripts/finepdfs-stats.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": [
        "--limit", "10000",
        "--show-plan",
        "--output-repo", "username/finepdfs-temporal-stats",
    ],
    "flavor": "cpu-upgrade",
    "timeout": "2h",
    "env": {"HF_XET_HIGH_PERFORMANCE": "1"},
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

## 常见失败模式

### 内存不足(OOM)

**修复:**
1. 减少批次大小或数据块大小
2. 以较小的批次处理数据
3. 升级硬件: cpu → t4 → a10g → a100

### 作业超时

**修复:**
1. 检查日志以获取实际运行时间
2. 增加缓冲区增加超时: `"timeout": "3h"`
3. 优化代码以加快执行
4. 以块处理数据

### Hub 推送失败

**修复:**
1. 添加到作业: `secrets={"HF_TOKEN": "$HF_TOKEN"}`
2. 在脚本中验证令牌: `assert "HF_TOKEN" in os.environ`
3. 检查令牌权限
4. 验证存储库存在或可以创建

### 缺少依赖项

**修复:**
添加到 PEP 723 标头:
```python
# /// script
# dependencies = ["package1", "package2>=1.0.0"]
# ///
```

### 身份验证错误

**修复:**
1. 检查 `hf_whoami()` 是否在本地工作
2. 验证作业配置中的 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
3. 重新登录: `hf auth login`
4. 检查令牌是否具有所需权限

## 故障排除

**常见问题:**
- 作业超时 → 增加超时、优化代码
- 结果未保存 → 检查持久化方法、验证 HF_TOKEN
- 内存不足 → 减少批次大小、升级硬件
- 导入错误 → 将依赖项添加到 PEP 723 标头
- 身份验证错误 → 检查令牌、验证机密参数

**参见:** `references/troubleshooting.md` 了解完整的故障排除指南

## 资源

### 参考(在此技能中)
- `references/token_usage.md` - 完整的令牌使用指南
- `references/hardware_guide.md` - 硬件规格和选择
- `references/hub_saving.md` - Hub 持久化指南
- `references/troubleshooting.md` - 常见问题和解决方案

### 脚本(在此技能中)
- `scripts/generate-responses.py` - vLLM 批处理生成: 数据集 → 响应 → 推送到 Hub
- `scripts/cot-self-instruct.py` - CoT Self-Instruct 合成数据生成 + 过滤 → 推送到 Hub
- `scripts/finepdfs-stats.py` - Hub 上 `finepdfs-edu` parquet 的 Polars 流式统计(可选推送)

### 外部链接

**官方文档:**
- [HF Jobs 指南](https://huggingface.co/docs/huggingface_hub/guides/jobs) - 主要文档
- [HF Jobs CLI 参考](https://huggingface.co/docs/huggingface_hub/guides/cli#hf-jobs) - 命令行界面
- [HF Jobs API 参考](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api) - Python API 详细信息
- [硬件类型参考](https://huggingface.co/docs/hub/en/spaces-config-reference) - 可用硬件

**相关工具:**
- [UV 脚本指南](https://docs.astral.sh/uv/guides/scripts/) - PEP 723 内联依赖项
- [UV 脚本组织](https://huggingface.co/uv-scripts) - 社区 UV 脚本集合
- [HF Hub 身份验证](https://huggingface.co/docs/huggingface_hub/quick-start#authentication) - 令牌设置
- [Webhooks 文档](https://huggingface.co/docs/huggingface_hub/guides/webhooks) - 事件触发器

## 关键要点

1. **内联提交脚本** - `script` 参数直接接受 Python 代码;除非用户要求,否则无需文件保存
2. **作业是异步的** - 不要等待/轮询;让用户在准备好时检查
3. **始终设置超时** - 默认 30 分钟可能不足;设置适当的超时
4. **始终持久化结果** - 环境是临时的;没有持久化,所有工作都将丢失
5. **安全使用令牌** - 对于 Hub 操作始终使用 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
6. **选择合适的硬件** - 从小处开始,根据需求扩展(参见硬件指南)
7. **使用 UV 脚本** - 对于 Python 工作负载,默认使用 `hf_jobs("uv", {...})` 和内联脚本
8. **处理身份验证** - 在 Hub 操作之前验证令牌可用
9. **监控作业** - 提供作业 URL 和状态检查命令
10. **优化成本** - 选择合适的硬件,设置适当的超时

## 快速参考: MCP 工具 vs CLI vs Python API

| 操作 | MCP 工具 | CLI | Python API |
|-----------|----------|-----|------------|
| 运行 UV 脚本 | `hf_jobs("uv", {...})` | `hf jobs uv run script.py` | `run_uv_job("script.py")` |
| 运行 Docker 作业 | `hf_jobs("run", {...})` | `hf jobs run image cmd` | `run_job(image, command)` |
| 列出作业 | `hf_jobs("ps")` | `hf jobs ps` | `list_jobs()` |
| 查看日志 | `hf_jobs("logs", {...})` | `hf jobs logs <id>` | `fetch_job_logs(job_id)` |
| 取消作业 | `hf_jobs("cancel", {...})` | `hf jobs cancel <id>` | `cancel_job(job_id)` |
| 计划 UV | `hf_jobs("scheduled uv", {...})` | - | `create_scheduled_uv_job()` |
| 计划 Docker | `hf_jobs("scheduled run", {...})` | - | `create_scheduled_job()` |
