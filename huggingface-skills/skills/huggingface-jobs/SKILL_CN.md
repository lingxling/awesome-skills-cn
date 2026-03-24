---
name: huggingface-jobs
description: 当用户想要在 Hugging Face Jobs 基础设施上运行任何工作负载时使用此技能。涵盖 UV 脚本、基于 Docker 的作业、硬件选择、成本估算、令牌认证、密钥管理、超时配置和结果持久化。专为通用计算工作负载设计，包括数据处理、推理、实验、批处理作业和任何基于 Python 的任务。应在涉及云计算、GPU 工作负载或用户提到在 Hugging Face 基础设施上运行作业而无需本地设置的任务中调用。
license: 完整条款见 LICENSE.txt
---

# 在 Hugging Face Jobs 上运行工作负载

## 概述

在完全托管的 Hugging Face 基础设施上运行任何工作负载。无需本地设置——作业在云 CPU、GPU 或 TPU 上运行，并可以将结果持久化到 Hugging Face Hub。

**常见用例：**
- **数据处理** - 转换、过滤或分析大型数据集
- **批量推理** - 对数千个样本运行推理
- **实验和基准测试** - 可重现的 ML 实验
- **模型训练** - 微调模型（具体训练见 `model-trainer` 技能）
- **合成数据生成** - 使用 LLM 生成数据集
- **开发和测试** - 无需本地 GPU 设置即可测试代码
- **计划作业** - 自动化重复任务

**专门用于模型训练：** 请参阅 `model-trainer` 技能了解基于 TRL 的训练工作流程。

## 何时使用此技能

当用户想要以下情况时使用此技能：
- 在云基础设施上运行 Python 工作负载
- 无需本地 GPU/TPU 设置即可执行作业
- 大规模处理数据
- 运行批量推理或实验
- 计划重复任务
- 对任何工作负载使用 GPU/TPU
- 将结果持久化到 Hugging Face Hub

## 关键指令

在协助处理作业时：

1. **始终使用 `hf_jobs()` MCP 工具** - 使用 `hf_jobs("uv", {...})` 或 `hf_jobs("run", {...})` 提交作业。`script` 参数直接接受 Python 代码。除非用户明确要求，否则不要保存到本地文件。将脚本内容作为字符串传递给 `hf_jobs()`。

2. **始终处理认证** - 与 Hub 交互的作业需要通过密钥提供 `HF_TOKEN`。请参阅下面的令牌使用部分。

3. **提交后提供作业详细信息** - 提交后，提供作业 ID、监控 URL、预计时间，并注意用户可以稍后请求状态检查。

4. **设置适当的超时** - 默认 30 分钟对于长时间运行的任务可能不足。

## 先决条件检查清单

在开始任何作业之前，验证：

### ✅ **账户和认证**
- 具有 [Pro](https://hf.co/pro)、[Team](https://hf.co/enterprise) 或 [Enterprise](https://hf.co/enterprise) 计划的 Hugging Face 账户（作业需要付费计划）
- 已认证登录：使用 `hf_whoami()` 检查
- **用于 Hub 访问的 HF_TOKEN** ⚠️ 关键 - 任何 Hub 操作（推送模型/数据集、下载私有仓库等）都需要
- 令牌必须具有适当的权限（下载需要读取权限，上传需要写入权限）

### ✅ **令牌使用**（详情见令牌使用部分）

**何时需要令牌：**
- 将模型/数据集推送到 Hub
- 访问私有仓库
- 在脚本中使用 Hub API
- 任何需要认证的 Hub 操作

**如何提供令牌：**
```python
# hf_jobs MCP 工具 — $HF_TOKEN 会自动替换为真实令牌：
{"secrets": {"HF_TOKEN": "$HF_TOKEN"}}

# HfApi().run_uv_job() — 必须传递实际令牌：
from huggingface_hub import get_token
secrets={"HF_TOKEN": get_token()}
```

**⚠️ 关键：** `$HF_TOKEN` 占位符仅由 `hf_jobs` MCP 工具自动替换。使用 `HfApi().run_uv_job()` 时，必须通过 `get_token()` 传递真实令牌。传递字面字符串 `"$HF_TOKEN"` 会导致 9 个字符的无效令牌和 401 错误。

## 令牌使用指南

### 了解令牌

**什么是 HF 令牌？**
- Hugging Face Hub 的认证凭据
- 需要认证操作（推送、私有仓库、API 访问）
- 在 `hf auth login` 后安全地存储在您的机器上

**令牌类型：**
- **读取令牌** - 可以下载模型/数据集，读取私有仓库
- **写入令牌** - 可以推送模型/数据集，创建仓库，修改内容
- **组织令牌** - 可以代表组织操作

### 何时需要令牌

**始终需要：**
- 将模型/数据集推送到 Hub
- 访问私有仓库
- 创建新仓库
- 修改现有仓库
- 以编程方式使用 Hub API

**不需要：**
- 下载公共模型/数据集
- 运行不与 Hub 交互的作业
- 读取公共仓库信息

### 如何向作业提供令牌

#### 方法 1：自动令牌（推荐）

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 自动替换
})
```

**工作原理：**
- `$HF_TOKEN` 是一个占位符，会被您的实际令牌替换
- 使用您登录会话中的令牌（`hf auth login`）
- 最安全、最方便的方法
- 令牌作为密钥传递时在服务器端加密

**优势：**
- 代码中不暴露令牌
- 使用您当前的登录会话
- 如果重新登录会自动更新
- 与 MCP 工具无缝配合

#### 方法 2：显式令牌（不推荐）

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "secrets": {"HF_TOKEN": "hf_abc123..."}  # ⚠️ 硬编码令牌
})
```

**何时使用：**
- 仅当自动令牌不起作用时
- 使用特定令牌进行测试
- 组织令牌（谨慎使用）

**安全问题：**
- 令牌在代码/日志中可见
- 如果令牌轮换必须手动更新
- 令牌暴露风险

#### 方法 3：环境变量（安全性较低）

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "env": {"HF_TOKEN": "hf_abc123..."}  # ⚠️ 比密钥安全性低
})
```

**与密钥的区别：**
- `env` 变量在作业日志中可见
- `secrets` 在服务器端加密
- 对于令牌始终优先使用 `secrets`

### 在脚本中使用令牌

**在您的 Python 脚本中，令牌作为环境变量可用：**

```python
# /// script
# dependencies = ["huggingface-hub"]
# ///

import os
from huggingface_hub import HfApi

# 如果通过密钥传递，令牌自动可用
token = os.environ.get("HF_TOKEN")

# 与 Hub API 一起使用
api = HfApi(token=token)

# 或者让 huggingface_hub 自动检测
api = HfApi()  # 自动使用 HF_TOKEN 环境变量
```

**最佳实践：**
- 不要在脚本中硬编码令牌
- 使用 `os.environ.get("HF_TOKEN")` 访问
- 尽可能让 `huggingface_hub` 自动检测
- 在 Hub 操作之前验证令牌存在

### 令牌验证

**检查是否已登录：**
```python
from huggingface_hub import whoami
user_info = whoami()  # 如果已认证，返回您的用户名
```

**在作业中验证令牌：**
```python
import os
assert "HF_TOKEN" in os.environ, "未找到 HF_TOKEN！"
token = os.environ["HF_TOKEN"]
print(f"令牌以：{token[:7]}... 开头")  # 应该以 "hf_" 开头
```

### 常见令牌问题

**错误：401 Unauthorized**
- **原因：** 令牌缺失或无效
- **修复：** 将 `secrets={"HF_TOKEN": "$HF_TOKEN"}` 添加到作业配置
- **验证：** 检查 `hf_whoami()` 在本地是否工作

**错误：403 Forbidden**
- **原因：** 令牌缺少所需权限
- **修复：** 确保令牌具有推送操作的写入权限
- **检查：** 在 https://huggingface.co/settings/tokens 检查令牌类型

**错误：环境中未找到令牌**
- **原因：** 未传递 `secrets` 或密钥名称错误
- **修复：** 使用 `secrets={"HF_TOKEN": "$HF_TOKEN"}`（而不是 `env`）
- **验证：** 脚本检查 `os.environ.get("HF_TOKEN")`

**错误：仓库访问被拒绝**
- **原因：** 令牌无权访问私有仓库
- **修复：** 使用有访问权限的账户的令牌
- **检查：** 验证仓库可见性和您的权限

### 令牌安全最佳实践

1. **永远不要提交令牌** - 使用 `$HF_TOKEN` 占位符或环境变量
2. **使用密钥而不是 env** - 密钥在服务器端加密
3. **定期轮换令牌** - 定期生成新令牌
4. **使用最小权限** - 创建仅具有所需权限的令牌
5. **不要共享令牌** - 每个用户应使用自己的令牌
6. **监控令牌使用** - 在 Hub 设置中检查令牌活动

### 完整令牌示例

```python
# 示例：将结果推送到 Hub
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["huggingface-hub", "datasets"]
# ///

import os
from huggingface_hub import HfApi
from datasets import Dataset

# 验证令牌可用
assert "HF_TOKEN" in os.environ, "需要 HF_TOKEN！"

# 使用令牌进行 Hub 操作
api = HfApi(token=os.environ["HF_TOKEN"])

# 创建并推送数据集
data = {"text": ["Hello", "World"]}
dataset = Dataset.from_dict(data)
dataset.push_to_hub("username/my-dataset", token=os.environ["HF_TOKEN"])

print("✅ 数据集推送成功！")
""",
    "flavor": "cpu-basic",
    "timeout": "30m",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 安全提供令牌
})
```

## 快速开始：两种方法

### 方法 1：UV 脚本（推荐）

UV 脚本使用 PEP 723 内联依赖项，实现简洁、自包含的工作负载。

**MCP 工具：**
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

**CLI 等效命令：**
```bash
hf jobs uv run my_script.py --flavor cpu-basic --timeout 30m
```

**Python API：**
```python
from huggingface_hub import run_uv_job
run_uv_job("my_script.py", flavor="cpu-basic", timeout="30m")
```

**优势：** 直接使用 MCP 工具，代码简洁，依赖项内联声明，无需保存文件

**何时使用：** 所有工作负载的默认选择、自定义逻辑、任何需要 `hf_jobs()` 的场景

#### UV 脚本的自定义 Docker 镜像

默认情况下，UV 脚本使用 `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`。对于具有复杂依赖项的 ML 工作负载，使用预构建镜像：

```python
hf_jobs("uv", {
    "script": "inference.py",
    "image": "vllm/vllm-openai:latest",  # 预构建的 vLLM 镜像
    "flavor": "a10g-large"
})
```

**CLI：**
```bash
hf jobs uv run --image vllm/vllm-openai:latest --flavor a10g-large inference.py
```

**优势：** 更快的启动、预安装的依赖项、针对特定框架优化

#### Python 版本

默认情况下，UV 脚本使用 Python 3.12。指定不同的版本：

```python
hf_jobs("uv", {
    "script": "my_script.py",
    "python": "3.11",  # 使用 Python 3.11
    "flavor": "cpu-basic"
})
```

**Python API：**
```python
from huggingface_hub import run_uv_job
run_uv_job("my_script.py", python="3.11")
```

#### 处理脚本

⚠️ **重要：** 根据您运行 Jobs 的方式，有*两个*"脚本路径"故事：

- **使用 `hf_jobs()` MCP 工具（在此仓库中推荐）**：`script` 值必须是**内联代码**（字符串）或 **URL**。本地文件系统路径（如 `"./scripts/foo.py"`）在远程容器内不存在。
- **使用 `hf jobs uv run` CLI**：本地文件路径**可以工作**（CLI 会上传您的脚本）。

**使用 `hf_jobs()` MCP 工具的常见错误：**

```python
# ❌ 将失败（远程容器看不到您的本地路径）
hf_jobs("uv", {"script": "./scripts/foo.py"})
```

**使用 `hf_jobs()` MCP 工具的正确模式：**

```python
# ✅ 内联：读取本地脚本文件并传递其*内容*
from pathlib import Path
script = Path("hf-jobs/scripts/foo.py").read_text()
hf_jobs("uv", {"script": script})

# ✅ URL：托管脚本到可访问的位置
hf_jobs("uv", {"script": "https://huggingface.co/datasets/uv-scripts/.../raw/main/foo.py"})

# ✅ 来自 GitHub 的 URL
hf_jobs("uv", {"script": "https://raw.githubusercontent.com/huggingface/trl/main/trl/scripts/sft.py"})
```

**CLI 等效命令（支持本地路径）：**

```bash
hf jobs uv run ./scripts/foo.py -- --your --args
```

#### 运行时添加依赖项

添加 PEP 723 标头之外的额外依赖项：

```python
hf_jobs("uv", {
    "script": "inference.py",
    "dependencies": ["transformers", "torch>=2.0"],  # 额外依赖
    "flavor": "a10g-small"
})
```

**Python API：**
```python
from huggingface_hub import run_uv_job
run_uv_job("inference.py", dependencies=["transformers", "torch>=2.0"])
```

### 方法 2：基于 Docker 的作业

使用自定义 Docker 镜像和命令运行作业。

**MCP 工具：**
```python
hf_jobs("run", {
    "image": "python:3.12",
    "command": ["python", "-c", "print('Hello from HF Jobs!')"],
    "flavor": "cpu-basic",
    "timeout": "30m"
})
```

**CLI 等效命令：**
```bash
hf jobs run python:3.12 python -c "print('Hello from HF Jobs!')"
```

**Python API：**
```python
from huggingface_hub import run_job
run_job(image="python:3.12", command=["python", "-c", "print('Hello!')"], flavor="cpu-basic")
```

**优势：** 完全的 Docker 控制、使用预构建镜像、运行任何命令
**何时使用：** 需要特定的 Docker 镜像、非 Python 工作负载、复杂环境

**GPU 示例：**
```python
hf_jobs("run", {
    "image": "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel",
    "command": ["python", "-c", "import torch; print(torch.cuda.get_device_name())"],
    "flavor": "a10g-small",
    "timeout": "1h"
})
```

**使用 Hugging Face Spaces 作为镜像：**

您可以使用来自 HF Spaces 的 Docker 镜像：
```python
hf_jobs("run", {
    "image": "hf.co/spaces/lhoestq/duckdb",  # Space 作为 Docker 镜像
    "command": ["duckdb", "-c", "SELECT 'Hello from DuckDB!'"],
    "flavor": "cpu-basic"
})
```

**CLI：**
```bash
hf jobs run hf.co/spaces/lhoestq/duckdb duckdb -c "SELECT 'Hello!'"
```

### 在 Hub 上查找更多 UV 脚本

`uv-scripts` 组织提供存储在 Hugging Face Hub 上作为数据集的现成 UV 脚本：

```python
# 发现可用的 UV 脚本集合
dataset_search({"author": "uv-scripts", "sort": "downloads", "limit": 20})

# 探索特定集合
hub_repo_details(["uv-scripts/classification"], repo_type="dataset", include_readme=True)
```

**流行集合：** OCR、classification、synthetic-data、vLLM、dataset-creation

## 硬件选择

> **参考：** [HF Jobs 硬件文档](https://huggingface.co/docs/hub/en/spaces-config-reference)（2025 年 7 月更新）

| 工作负载类型 | 推荐硬件 | 用例 |
|---------------|---------------------|----------|
| 数据处理、测试 | `cpu-basic`、`cpu-upgrade` | 轻量级任务 |
| 小型模型、演示 | `t4-small` | <1B 模型、快速测试 |
| 中型模型 | `t4-medium`、`l4x1` | 1-7B 模型 |
| 大型模型、生产 | `a10g-small`、`a10g-large` | 7-13B 模型 |
| 超大型模型 | `a100-large` | 13B+ 模型 |
| 批量推理 | `a10g-large`、`a100-large` | 高吞吐量 |
| 多 GPU 工作负载 | `l4x4`、`a10g-largex2`、`a10g-largex4` | 并行/大型模型 |
| TPU 工作负载 | `v5e-1x1`、`v5e-2x2`、`v5e-2x4` | JAX/Flax、TPU 优化 |

**所有可用规格：**
- **CPU：** `cpu-basic`、`cpu-upgrade`
- **GPU：** `t4-small`、`t4-medium`、`l4x1`、`l4x4`、`a10g-small`、`a10g-large`、`a10g-largex2`、`a10g-largex4`、`a100-large`
- **TPU：** `v5e-1x1`、`v5e-2x2`、`v5e-2x4`

**指南：**
- 从较小的硬件开始进行测试
- 根据实际需求扩展
- 对并行工作负载或大型模型使用多 GPU
- 对 JAX/Flax 工作负载使用 TPU
- 详见 `references/hardware_guide.md` 了解详细规格

## 关键：保存结果

**⚠️ 临时环境——必须持久化结果**

作业环境是临时的。作业结束时所有文件都会被删除。如果结果未持久化，**所有工作都将丢失**。

### 持久化选项

**1. 推送到 Hugging Face Hub（推荐）**

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
# POST 结果到您的 API
import requests
requests.post("https://your-api.com/results", json=results)
```

### Hub 推送的必需配置

**在作业提交中：**
```python
# hf_jobs MCP 工具：
{"secrets": {"HF_TOKEN": "$HF_TOKEN"}}  # 自动替换

# HfApi().run_uv_job()：
from huggingface_hub import get_token
secrets={"HF_TOKEN": get_token()}  # 必须传递真实令牌
```

**在脚本中：**
```python
import os
from huggingface_hub import HfApi

# 令牌从密钥自动可用
api = HfApi(token=os.environ.get("HF_TOKEN"))

# 推送您的结果
api.upload_file(...)
```

### 验证检查清单

提交之前：
- [ ] 已选择结果持久化方法
- [ ] 如果使用 Hub，令牌在密钥中（MCP：`"$HF_TOKEN"`，Python API：`get_token()`）
- [ ] 脚本优雅地处理缺失的令牌
- [ ] 测试持久化路径是否工作

**详见：** `references/hub_saving.md` 了解详细的 Hub 持久化指南

## 超时管理

**⚠️ 默认：30 分钟**

作业在超时后自动停止。对于训练等长时间运行的任务，始终设置自定义超时。

### 设置超时

**MCP 工具：**
```python
{
    "timeout": "2h"   # 2 小时
}
```

**支持的格式：**
- 整数/浮点数：秒（例如，`300` = 5 分钟）
- 带后缀的字符串：`"5m"`（分钟）、`"2h"`（小时）、`"1d"`（天）
- 示例：`"90m"`、`"2h"`、`"1.5h"`、`300`、`"1d"`

**Python API：**
```python
from huggingface_hub import run_job, run_uv_job

run_job(image="python:3.12", command=[...], timeout="2h")
run_uv_job("script.py", timeout=7200)  # 2 小时，以秒为单位
```

### 超时指南

| 场景 | 推荐 | 备注 |
|----------|-------------|-------|
| 快速测试 | 10-30 分钟 | 验证设置 |
| 数据处理 | 1-2 小时 | 取决于数据大小 |
| 批量推理 | 2-4 小时 | 大批量 |
| 实验 | 4-8 小时 | 多次运行 |
| 长时间运行 | 8-24 小时 | 生产工作负载 |

**始终添加 20-30% 的缓冲时间**用于设置、网络延迟和清理。

**超时时：** 作业立即终止，所有未保存的进度丢失

## 成本估算

**一般指南：**

```
总成本 =（运行小时数）×（每小时成本）
```

**示例计算：**

**快速测试：**
- 硬件：cpu-basic（$0.10/小时）
- 时间：15 分钟（0.25 小时）
- 成本：$0.03

**数据处理：**
- 硬件：l4x1（$2.50/小时）
- 时间：2 小时
- 成本：$5.00

**批量推理：**
- 硬件：a10g-large（$5/小时）
- 时间：4 小时
- 成本：$20.00

**成本优化技巧：**
1. 从小开始 - 在 cpu-basic 或 t4-small 上测试
2. 监控运行时间 - 设置适当的超时
3. 使用检查点 - 如果作业失败则恢复
4. 优化代码 - 减少不必要的计算
5. 选择正确的硬件 - 不要过度配置

## 监控和跟踪

### 检查作业状态

**MCP 工具：**
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

**Python API：**
```python
from huggingface_hub import list_jobs, inspect_job, fetch_job_logs, cancel_job

# 列出您的作业
jobs = list_jobs()

# 仅列出运行中的作业
running = [j for j in list_jobs() if j.status.stage == "RUNNING"]

# 检查特定作业
job_info = inspect_job(job_id="your-job-id")

# 查看日志
for log in fetch_job_logs(job_id="your-job-id"):
    print(log)

# 取消作业
cancel_job(job_id="your-job-id")
```

**CLI：**
```bash
hf jobs ps                    # 列出作业
hf jobs logs <job-id>         # 查看日志
hf jobs cancel <job-id>       # 取消作业
```

**记住：** 等待用户请求状态检查。避免重复轮询。

### 作业 URL

提交后，作业具有监控 URL：
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
    while inspect_job(job.id).status.stage != "FINISHED":
        time.sleep(30)
```

## 故障排除

### 作业失败

**常见原因：**
- 缺少依赖项
- 脚本中的语法错误
- 令牌问题（401/403 错误）
- 超时
- 内存不足

**调试步骤：**
1. 检查日志：`hf_jobs("logs", {"job_id": "your-job-id"})`
2. 验证令牌：`hf_whoami()`
3. 在本地测试脚本
4. 增加超时
5. 升级硬件规格

### 作业卡住

**可能原因：**
- 无限循环
- 等待用户输入
- 网络问题

**解决方案：**
- 取消作业：`hf_jobs("cancel", {"job_id": "your-job-id"})`
- 添加超时
- 添加日志以跟踪进度

### 内存错误

**症状：**
- OOM（内存不足）错误
- 作业崩溃

**解决方案：**
- 升级到更大的硬件规格
- 减少批量大小
- 使用量化模型
- 优化数据加载

### 网络问题

**症状：**
- 无法下载模型
- 无法连接到 Hub

**解决方案：**
- 检查令牌权限
- 验证网络连接
- 使用预构建镜像
- 在脚本中添加重试逻辑

## 参考文档

### 本技能
- **[硬件指南](./references/hardware_guide.md)** - 详细的硬件规格和选择
- **[Hub 保存](./references/hub_saving.md)** - 推送模型、数据集和工件
- **[令牌使用](./references/token_usage.md)** - 认证和令牌管理
- **[故障排除](./references/troubleshooting.md)** - 常见问题和解决方案

### 官方 Hugging Face Jobs
- 官方文档：https://huggingface.co/docs/hub/en/jobs
- CLI 参考：`hf jobs --help`
- Python API：https://huggingface.co/docs/huggingface_hub/en/guides/jobs
