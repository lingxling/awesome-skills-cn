---
name: hf-cli
description: "Hugging Face Hub CLI (`hf`) 用于在 Hugging Face Hub 上下载、上传和管理存储库、模型、数据集和 Spaces。替代现已弃用的 `huggingface-cli` 命令。"
---

安装：`curl -LsSf https://hf.co/cli/install.sh | bash -s`。

Hugging Face Hub CLI 工具 `hf` 可用。重要：`hf` 命令替代了已弃用的 `huggingface-cli` 命令。

使用 `hf --help` 查看可用功能。注意，身份验证命令现在都在 `hf auth` 下，例如 `hf auth whoami`。

由 `huggingface_hub v1.6.0` 生成。运行 `hf skills add --force` 重新生成。

## 命令

- `hf download REPO_ID` — 从 Hub 下载文件。
- `hf env` — 打印环境信息。
- `hf sync` — 在本地目录和存储桶之间同步文件。
- `hf upload REPO_ID` — 上传文件或文件夹到 Hub。推荐用于单次提交上传。
- `hf upload-large-folder REPO_ID LOCAL_PATH` — 上传大型文件夹到 Hub。推荐用于可恢复的上传。
- `hf version` — 打印 hf 版本信息。

### `hf auth` — 管理身份验证（登录、登出等）。

- `hf auth list` — 列出所有存储的访问令牌。
- `hf auth login` — 使用来自 huggingface.co/settings/tokens 的令牌登录。
- `hf auth logout` — 从特定令牌登出。
- `hf auth switch` — 在访问令牌之间切换。
- `hf auth whoami` — 查看你登录的 huggingface.co 账户。

### `hf buckets` — 与存储桶交互的命令。

- `hf buckets cp SRC` — 复制单个文件到存储桶或从存储桶复制。
- `hf buckets create BUCKET_ID` — 创建新存储桶。
- `hf buckets delete BUCKET_ID` — 删除存储桶。
- `hf buckets info BUCKET_ID` — 获取存储桶信息。
- `hf buckets list` — 列出存储桶或存储桶中的文件。
- `hf buckets move FROM_ID TO_ID` — 将存储桶移动（重命名）到新名称或命名空间。
- `hf buckets remove ARGUMENT` — 从存储桶中删除文件。
- `hf buckets sync` — 在本地目录和存储桶之间同步文件。

### `hf cache` — 管理本地缓存目录。

- `hf cache ls` — 列出缓存的存储库或修订版。
- `hf cache prune` — 从缓存中删除分离的修订版。
- `hf cache rm TARGETS` — 删除缓存的存储库或修订版。
- `hf cache verify REPO_ID` — 验证来自缓存或本地目录的单个存储库修订版的校验和。

### `hf collections` — 与 Hub 上的集合交互。

- `hf collections add-item COLLECTION_SLUG ITEM_ID ITEM_TYPE` — 向集合添加项目。
- `hf collections create TITLE` — 在 Hub 上创建新集合。
- `hf collections delete COLLECTION_SLUG` — 从 Hub 中删除集合。
- `hf collections delete-item COLLECTION_SLUG ITEM_OBJECT_ID` — 从集合中删除项目。
- `hf collections info COLLECTION_SLUG` — 获取 Hub 上集合的信息。
- `hf collections ls` — 列出 Hub 上的集合。
- `hf collections update COLLECTION_SLUG` — 更新 Hub 上集合的元数据。
- `hf collections update-item COLLECTION_SLUG ITEM_OBJECT_ID` — 更新集合中的项目。

### `hf datasets` — 与 Hub 上的数据集交互。

- `hf datasets info DATASET_ID` — 获取 Hub 上数据集的信息。
- `hf datasets ls` — 列出 Hub 上的数据集。
- `hf datasets parquet DATASET_ID` — 列出数据集可用的 parquet 文件 URL。
- `hf datasets sql SQL` — 使用 DuckDB 对数据集 parquet URL 执行原始 SQL 查询。

### `hf discussions` — 管理 Hub 上的讨论和拉取请求。

- `hf discussions close REPO_ID NUM` — 关闭讨论或拉取请求。
- `hf discussions comment REPO_ID NUM` — 对讨论或拉取请求发表评论。
- `hf discussions create REPO_ID title` — 在存储库上创建新的讨论或拉取请求。
- `hf discussions diff REPO_ID NUM` — 显示拉取请求的差异。
- `hf discussions info REPO_ID NUM` — 获取讨论或拉取请求的信息。
- `hf discussions list REPO_ID` — 列出存储库上的讨论和拉取请求。
- `hf discussions merge REPO_ID NUM` — 合并拉取请求。
- `hf discussions rename REPO_ID NUM NEW_TITLE` — 重命名讨论或拉取请求。
- `hf discussions reopen REPO_ID NUM` — 重新打开已关闭的讨论或拉取请求。

### `hf endpoints` — 管理 Hugging Face 推理端点。

- `hf endpoints catalog` — 与推理端点目录交互。
- `hf endpoints delete NAME` — 永久删除推理端点。
- `hf endpoints deploy NAME repo framework accelerator instance_size instance_type region vendor` — 从 Hub 存储库部署推理端点。
- `hf endpoints describe NAME` — 获取现有端点的信息。
- `hf endpoints ls` — 列出给定命名空间的所有推理端点。
- `hf endpoints pause NAME` — 暂停推理端点。
- `hf endpoints resume NAME` — 恢复推理端点。
- `hf endpoints scale-to-zero NAME` — 将推理端点缩放到零。
- `hf endpoints update NAME` — 更新现有端点。

### `hf extensions` — 管理 hf CLI 扩展。

- `hf extensions exec NAME` — 执行已安装的扩展。
- `hf extensions install REPO_ID` — 从公共 GitHub 存储库安装扩展。
- `hf extensions list` — 列出已安装的扩展命令。
- `hf extensions remove NAME` — 移除已安装的扩展。

### `hf jobs` — 在 Hub 上运行和管理作业。

- `hf jobs cancel JOB_ID` — 取消作业
- `hf jobs hardware` — 列出作业可用的硬件选项
- `hf jobs inspect JOB_IDS` — 显示一个或多个作业的详细信息
- `hf jobs logs JOB_ID` — 获取作业的日志。
- `hf jobs ps` — 列出作业。
- `hf jobs run IMAGE COMMAND` — 运行作业。
- `hf jobs scheduled` — 在 Hub 上创建和管理计划作业。
- `hf jobs stats` — 获取作业的资源使用统计信息和指标
- `hf jobs uv` — 在 HF 基础设施上运行 UV 脚本（具有内联依赖项的 Python）。

### `hf models` — 与 Hub 上的模型交互。

- `hf models info MODEL_ID` — 获取 Hub 上模型的信息。
- `hf models ls` — 列出 Hub 上的模型。

### `hf papers` — 与 Hub 上的论文交互。

- `hf papers ls` — 列出 Hub 上的每日论文。

### `hf repos` — 管理 Hub 上的存储库。

- `hf repos branch` — 管理 Hub 上存储库的分支。
- `hf repos create REPO_ID` — 在 Hub 上创建新存储库。
- `hf repos delete REPO_ID` — 从 Hub 中删除存储库。这是不可逆的操作。
- `hf repos delete-files REPO_ID PATTERNS` — 从 Hub 上的存储库中删除文件。
- `hf repos duplicate FROM_ID` — 在 Hub 上复制存储库（模型、数据集或 Space）。
- `hf repos move FROM_ID TO_ID` — 将存储库从一个命名空间移动到另一个命名空间。
- `hf repos settings REPO_ID` — 更新存储库的设置。
- `hf repos tag` — 管理 Hub 上存储库的标签。

### `hf skills` — 管理 AI 助手的技能。

- `hf skills add` — 下载技能并为 AI 助手安装。
- `hf skills preview` — 将生成的 SKILL.md 打印到标准输出。

### `hf spaces` — 与 Hub 上的 spaces 交互。

- `hf spaces dev-mode SPACE_ID` — 在 Space 上启用或禁用开发模式。
- `hf spaces hot-reload SPACE_ID` — 热重载 Space 的任何 Python 文件，无需完全重建 + 重启。
- `hf spaces info SPACE_ID` — 获取 Hub 上 space 的信息。
- `hf spaces ls` — 列出 Hub 上的 spaces。

### `hf webhooks` — 管理 Hub 上的 webhook。

- `hf webhooks create watch` — 创建新 webhook。
- `hf webhooks delete WEBHOOK_ID` — 永久删除 webhook。
- `hf webhooks disable WEBHOOK_ID` — 禁用活动的 webhook。
- `hf webhooks enable WEBHOOK_ID` — 启用已禁用的 webhook。
- `hf webhooks info WEBHOOK_ID` — 以 JSON 格式显示单个 webhook 的完整详细信息。
- `hf webhooks list` — 列出当前用户的所有 webhook。
- `hf webhooks update WEBHOOK_ID` — 更新现有 webhook。仅更改提供的选项。

## 提示

- 使用 `hf <command> --help` 获取完整选项、用法和实际示例
- 在列表命令上使用 `--format json` 获取机器可读输出
- 使用 `-q` / `--quiet` 仅打印 ID
- 使用 `HF_TOKEN` 环境变量（推荐）或 `--token` 进行身份验证