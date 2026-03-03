---
name: hugging-face-cli
description: 使用 `hf` CLI 执行 Hugging Face Hub 操作。当用户需要下载模型/数据集/Spaces、将文件上传到 Hub 存储库、创建存储库、管理本地缓存或在 HF 基础设施上运行计算作业时使用。涵盖身份验证、文件传输、存储库创建、缓存操作和云计算。
---

# Hugging Face CLI

`hf` CLI 提供对 Hugging Face Hub 的直接终端访问,用于下载、上传和管理存储库、缓存和计算资源。

## 快速命令参考

| 任务 | 命令 |
|------|---------|
| 登录 | `hf auth login` |
| 下载模型 | `hf download <repo_id>` |
| 下载到文件夹 | `hf download <repo_id> --local-dir ./path` |
| 上传文件夹 | `hf upload <repo_id> . .` |
| 创建存储库 | `hf repo create <name>` |
| 创建标签 | `hf repo tag create <repo_id> <tag>` |
| 删除文件 | `hf repo-files delete <repo_id> <files>` |
| 列出缓存 | `hf cache ls` |
| 从缓存中删除 | `hf cache rm <repo_or_revision>` |
| 列出模型 | `hf models ls` |
| 获取模型信息 | `hf models info <model_id>` |
| 列出数据集 | `hf datasets ls` |
| 获取数据集信息 | `hf datasets info <dataset_id>` |
| 列出 Spaces | `hf spaces ls` |
| 获取 Space 信息 | `hf spaces info <space_id>` |
| 列出端点 | `hf endpoints ls` |
| 运行 GPU 作业 | `hf jobs run --flavor a10g-small <image> <cmd>` |
| 环境信息 | `hf env` |

## 核心命令

### 身份验证
```bash
hf auth login                    # 交互式登录
hf auth login --token $HF_TOKEN  # 非交互式
hf auth whoami                   # 检查当前用户
hf auth list                     # 列出存储的令牌
hf auth switch                   # 在令牌之间切换
hf auth logout                   # 登出
```

### 下载
```bash
hf download <repo_id>                              # 完整存储库到缓存
hf download <repo_id> file.safetensors             # 特定文件
hf download <repo_id> --local-dir ./models         # 到本地目录
hf download <repo_id> --include "*.safetensors"    # 按模式过滤
hf download <repo_id> --repo-type dataset          # 数据集
hf download <repo_id> --revision v1.0              # 特定版本
```

### 上传
```bash
hf upload <repo_id> . .                            # 当前目录到根目录
hf upload <repo_id> ./models /weights              # 文件夹到路径
hf upload <repo_id> model.safetensors              # 单个文件
hf upload <repo_id> . . --repo-type dataset        # 数据集
hf upload <repo_id> . . --create-pr                # 创建 PR
hf upload <repo_id> . . --commit-message="msg"     # 自定义消息
```

### 存储库管理
```bash
hf repo create <name>                              # 创建模型存储库
hf repo create <name> --repo-type dataset          # 创建数据集
hf repo create <name> --private                    # 私有存储库
hf repo create <name> --repo-type space --space_sdk gradio  # Gradio space
hf repo delete <repo_id>                           # 删除存储库
hf repo move <from_id> <to_id>                     # 将存储库移动到新命名空间
hf repo settings <repo_id> --private true          # 更新存储库设置
hf repo list --repo-type model                     # 列出存储库
hf repo branch create <repo_id> release-v1         # 创建分支
hf repo branch delete <repo_id> release-v1         # 删除分支
hf repo tag create <repo_id> v1.0                  # 创建标签
hf repo tag list <repo_id>                         # 列出标签
hf repo tag delete <repo_id> v1.0                  # 删除标签
```

### 从存储库删除文件
```bash
hf repo-files delete <repo_id> folder/             # 删除文件夹
hf repo-files delete <repo_id> "*.txt"             # 使用模式删除
```

### 缓存管理
```bash
hf cache ls                      # 列出缓存的存储库
hf cache ls --revisions          # 包含单个修订版本
hf cache rm model/gpt2           # 删除缓存的存储库
hf cache rm <revision_hash>      # 删除缓存的修订版本
hf cache prune                   # 删除分离的修订版本
hf cache verify gpt2             # 从缓存验证校验和
```

### 浏览 Hub
```bash
# 模型
hf models ls                                        # 列出热门趋势模型
hf models ls --search "MiniMax" --author MiniMaxAI  # 搜索模型
hf models ls --filter "text-generation" --limit 20  # 按任务过滤
hf models info MiniMaxAI/MiniMax-M2.1               # 获取模型信息

# 数据集
hf datasets ls                                      # 列出热门趋势数据集
hf datasets ls --search "finepdfs" --sort downloads # 搜索数据集
hf datasets info HuggingFaceFW/finepdfs             # 获取数据集信息

# Spaces
hf spaces ls                                        # 列出热门趋势 spaces
hf spaces ls --filter "3d" --limit 10               # 过滤 3D 建模 spaces
hf spaces info enzostvs/deepsite                    # 获取 space 信息
```

### 作业(云计算)
```bash
hf jobs run python:3.12 python script.py           # 在 CPU 上运行
hf jobs run --flavor a10g-small <image> <cmd>      # 在 GPU 上运行
hf jobs run --secrets HF_TOKEN <image> <cmd>       # 使用 HF 令牌
hf jobs ps                                         # 列出作业
hf jobs logs <job_id>                              # 查看日志
hf jobs cancel <job_id>                            # 取消作业
```

### 推理端点
```bash
hf endpoints ls                                     # 列出端点
hf endpoints deploy my-endpoint \
  --repo openai/gpt-oss-120b \
  --framework vllm \
  --accelerator gpu \
  --instance-size x4 \
  --instance-type nvidia-a10g \
  --region us-east-1 \
  --vendor aws
hf endpoints describe my-endpoint                   # 显示端点详细信息
hf endpoints pause my-endpoint                      # 暂停端点
hf endpoints resume my-endpoint                     # 恢复端点
hf endpoints scale-to-zero my-endpoint              # 缩放到零
hf endpoints delete my-endpoint --yes               # 删除端点
```
**GPU 类型:** `cpu-basic`, `cpu-upgrade`, `cpu-xl`, `t4-small`, `t4-medium`, `l4x1`, `l4x4`, `l40sx1`, `l40sx4`, `l40sx8`, `a10g-small`, `a10g-large`, `a10g-largex2`, `a10g-largex4`, `a100-large`, `h100`, `h100x8`

## 常见模式

### 下载并在本地使用模型
```bash
# 下载到本地目录以进行部署
hf download meta-llama/Llama-3.2-1B-Instruct --local-dir ./model

# 或使用缓存并获取路径
MODEL_PATH=$(hf download meta-llama/Llama-3.2-1B-Instruct --quiet)
```

### 发布模型/数据集
```bash
hf repo create my-username/my-model --private
hf upload my-username/my-model ./output . --commit-message="Initial release"
hf repo tag create my-username/my-model v1.0
```

### 与本地同步 Space
```bash
hf upload my-username/my-space . . --repo-type space \
  --exclude="logs/*" --delete="*" --commit-message="Sync"
```

### 检查缓存使用情况
```bash
hf cache ls                      # 查看所有缓存的存储库和大小
hf cache rm model/gpt2           # 从缓存中删除存储库
```

## 关键选项

- `--repo-type`: `model`(默认)、`dataset`、`space`
- `--revision`: 分支、标签或提交哈希
- `--token`: 覆盖身份验证
- `--quiet`: 仅输出必要信息(路径/URL)

## 参考

- **完整命令参考**: 参见 [references/commands.md](references/commands.md)
- **工作流程示例**: 参见 [references/examples.md](references/examples.md)
