---
name: hf-cli
description: "Hugging Face Hub CLI (`hf`) 用于在 Hugging Face Hub 上下载、上传和管理模型、数据集、spaces、存储桶、仓库、论文、作业等。当需要：处理认证；管理本地缓存；管理 Hugging Face 存储桶；在 Hugging Face 基础设施上运行或调度作业；管理 Hugging Face 仓库；讨论和拉取请求；浏览模型、数据集和 spaces；阅读、搜索或浏览学术论文；管理集合；查询数据集；配置 spaces；设置 webhook；或部署和管理 HF 推理端点时使用。当用户提到 'hf'、'huggingface'、'Hugging Face'、'huggingface-cli' 或 'hugging face cli'，或想要做任何与 Hugging Face 生态系统以及一般 AI 和 ML 相关的事情时，确保使用此技能。也用于云存储需求，如训练检查点、数据管道或代理跟踪。即使用户没有明确要求 CLI 命令，也要使用。替代现已弃用的 `huggingface-cli`。"
---

安装：`curl -LsSf https://hf.co/cli/install.sh | bash -s`。

Hugging Face Hub CLI 工具 `hf` 可用。重要：`hf` 命令替代了已弃用的 `huggingface-cli` 命令。

使用 `hf --help` 查看可用功能。注意，认证命令现在都在 `hf auth` 下，例如 `hf auth whoami`。

由 `huggingface_hub v1.17.0` 生成。运行 `hf skills add --force` 重新生成。

## 命令

- `hf download REPO_ID` — 从 Hub 下载文件。`[--type CHOICE --revision TEXT --include TEXT --exclude TEXT --cache-dir TEXT --local-dir TEXT --force-download --dry-run --max-workers INTEGER --format CHOICE]`
- `hf env` — 打印环境信息。`[--format CHOICE]`
- `hf sync` — 在本地目录和存储桶之间同步文件。`[--delete --ignore-times --ignore-sizes --plan TEXT --apply TEXT --dry-run --include TEXT --exclude TEXT --filter-from TEXT --existing --ignore-existing --verbose --format CHOICE]`
- `hf update` — 更新 `hf` CLI 到最新版本。`[--format CHOICE]`
- `hf upload REPO_ID` — 上传文件或文件夹到 Hub。推荐用于单次提交上传。`[--type CHOICE --revision TEXT --private --include TEXT --exclude TEXT --delete TEXT --commit-message TEXT --commit-description TEXT --create-pr --every FLOAT --format CHOICE]`
- `hf upload-large-folder REPO_ID LOCAL_PATH` — 上传大文件夹到 Hub。推荐用于可恢复上传。`[--type CHOICE --revision TEXT --private --include TEXT --exclude TEXT --num-workers INTEGER --no-report --no-bars --format CHOICE]`
- `hf version` — 打印 hf 版本信息。`[--format CHOICE]`

### `hf auth` — 管理认证（登录、登出等）。

- `hf auth list` — 列出所有存储的访问令牌。`[--format CHOICE]`
- `hf auth login` — 使用来自 huggingface.co/settings/tokens 的令牌登录。`[--add-to-git-credential --force --format CHOICE]`
- `hf auth logout` — 从特定令牌登出。`[--token-name TEXT --format CHOICE]`
- `hf auth switch` — 在访问令牌之间切换。`[--token-name TEXT --add-to-git-credential --format CHOICE]`
- `hf auth token` — 将当前访问令牌打印到 stdout。`[--format CHOICE]`
- `hf auth whoami` — 找出您登录的 huggingface.co 账户。`[--format CHOICE]`

### `hf buckets` — 与存储桶交互的命令。

- `hf buckets cp SRC` — 将文件复制到存储桶或从存储桶复制。`[--format CHOICE]`
- `hf buckets create BUCKET_ID` — 创建新存储桶。`[--private --region CHOICE --exist-ok --format CHOICE]`
- `hf buckets delete BUCKET_ID` — 删除存储桶。`[--yes --missing-ok --format CHOICE]`
- `hf buckets info BUCKET_ID` — 获取存储桶信息。`[--format CHOICE]`
- `hf buckets list` — 列出存储桶或存储桶中的文件。`[--human-readable --tree --recursive --search TEXT --format CHOICE]`
- `hf buckets move FROM_ID TO_ID` — 将存储桶移动（重命名）到新名称或命名空间。`[--format CHOICE]`
- `hf buckets remove ARGUMENT` — 从存储桶中删除文件。`[--recursive --yes --dry-run --include TEXT --exclude TEXT --format CHOICE]`
- `hf buckets sync` — 在本地目录和存储桶之间同步文件。`[--delete ... --format CHOICE]`

### `hf cache` — 管理本地缓存目录。

- `hf cache list` — 列出缓存的仓库或修订版。`[--cache-dir TEXT --revisions --filter TEXT --sort CHOICE --limit INTEGER --format CHOICE]`
- `hf cache prune` — 从缓存中删除分离的修订版。`[--cache-dir TEXT --yes --dry-run --format CHOICE]`
- `hf cache rm TARGETS` — 删除缓存的仓库或修订版。`[--cache-dir TEXT --yes --dry-run --format CHOICE]`
- `hf cache verify REPO_ID` — 验证来自缓存或本地目录的单个仓库修订版的校验和。`[--type CHOICE --revision TEXT --cache-dir TEXT --local-dir TEXT --fail-on-missing-files --fail-on-extra-files --format CHOICE]`

### `hf collections` — 与 Hub 上的集合交互。

- `hf collections add-item COLLECTION_SLUG ITEM_ID ITEM_TYPE` — 向集合添加项目。`[--note TEXT --exists-ok --format CHOICE]`
- `hf collections create TITLE` — 在 Hub 上创建新集合。`[--namespace TEXT --description TEXT --private --exists-ok --format CHOICE]`
- `hf collections delete COLLECTION_SLUG` — 从 Hub 中删除集合。`[--missing-ok --format CHOICE]`
- `hf collections delete-item COLLECTION_SLUG ITEM_OBJECT_ID` — 从集合中删除项目。`[--missing-ok --format CHOICE]`
- `hf collections info COLLECTION_SLUG` — 获取 Hub 上集合的信息。`[--format CHOICE]`
- `hf collections list` — 列出 Hub 上的集合。`[--owner TEXT --item TEXT --sort CHOICE --limit INTEGER --format CHOICE]`
- `hf collections update COLLECTION_SLUG` — 更新 Hub 上集合的元数据。`[--title TEXT --description TEXT --position INTEGER --private --theme TEXT --format CHOICE]`
- `hf collections update-item COLLECTION_SLUG ITEM_OBJECT_ID` — 更新集合中的项目。`[--note TEXT --position INTEGER --format CHOICE]`

### `hf datasets` — 与 Hub 上的数据集交互。

- `hf datasets card DATASET_ID` — 获取 Hub 上数据集的模型卡片（README）。`[--metadata --text --format CHOICE]`
- `hf datasets info DATASET_ID` — 获取 Hub 上数据集的信息。`[--revision TEXT --expand TEXT --format CHOICE]`
- `hf datasets leaderboard DATASET_ID` — 列出数据集排行榜上的模型分数。此命令帮助找到任务最佳模型或按基准分数比较模型。使用 'hf datasets ls --filter benchmark:official' 列出可用排行榜。`[--limit INTEGER --format CHOICE]`
- `hf datasets list` — 列出 Hub 上的数据集或数据集仓库中的文件。`[--search TEXT --author TEXT --filter TEXT --sort CHOICE --limit INTEGER --expand TEXT --human-readable --tree --recursive --revision TEXT --format CHOICE]`
- `hf datasets parquet DATASET_ID` — 列出数据集可用的 parquet 文件 URL。`[--subset TEXT --split TEXT --format CHOICE]`
- `hf datasets sql SQL` — 使用 DuckDB 对数据集 parquet URL 执行原始 SQL 查询。`[--format CHOICE]`

### `hf discussions` — 管理 Hub 上的讨论和拉取请求。

- `hf discussions close REPO_ID NUM` — 关闭讨论或拉取请求。`[--comment TEXT --yes --type CHOICE --format CHOICE]`
- `hf discussions comment REPO_ID NUM` — 对讨论或拉取请求发表评论。`[--body TEXT --body-file PATH --type CHOICE --format CHOICE]`
- `hf discussions create REPO_ID --title TEXT` — 在仓库上创建新讨论或拉取请求。`[--body TEXT --body-file PATH --pull-request --type CHOICE --format CHOICE]`
- `hf discussions diff REPO_ID NUM` — 显示拉取请求的差异。`[--type CHOICE --format CHOICE]`
- `hf discussions info REPO_ID NUM` — 获取讨论或拉取请求的信息。`[--type CHOICE --format CHOICE]`
- `hf discussions list REPO_ID` — 列出仓库上的讨论和拉取请求。`[--status CHOICE --kind CHOICE --author TEXT --limit INTEGER --type CHOICE --format CHOICE]`
- `hf discussions merge REPO_ID NUM` — 合并拉取请求。`[--comment TEXT --yes --type CHOICE --format CHOICE]`
- `hf discussions rename REPO_ID NUM NEW_TITLE` — 重命名讨论或拉取请求。`[--type CHOICE --format CHOICE]`
- `hf discussions reopen REPO_ID NUM` — 重新打开已关闭的讨论或拉取请求。`[--comment TEXT --yes --type CHOICE --format CHOICE]`

### `hf endpoints` — 管理 Hugging Face 推理端点。

- `hf endpoints catalog deploy --repo TEXT` — 从模型目录部署推理端点。`[--name TEXT --accelerator TEXT --namespace TEXT --format CHOICE]`
- `hf endpoints catalog list` — 列出可用的目录模型。`[--format CHOICE]`
- `hf endpoints delete NAME` — 永久删除推理端点。`[--namespace TEXT --yes --format CHOICE]`
- `hf endpoints deploy NAME --repo TEXT --framework TEXT --accelerator TEXT --instance-size TEXT --instance-type TEXT --region TEXT --vendor TEXT` — 从 Hub 仓库部署推理端点。`[--namespace TEXT --task TEXT --min-replica INTEGER --max-replica INTEGER --scale-to-zero-timeout INTEGER --scaling-metric CHOICE --scaling-threshold FLOAT --format CHOICE]`
- `hf endpoints describe NAME` — 获取现有端点的信息。`[--namespace TEXT --format CHOICE]`
- `hf endpoints list` — 列出给定命名空间的所有推理端点。`[--namespace TEXT --format CHOICE]`
- `hf endpoints pause NAME` — 暂停推理端点。`[--namespace TEXT --format CHOICE]`
- `hf endpoints resume NAME` — 恢复推理端点。`[--namespace TEXT --fail-if-already-running --format CHOICE]`
- `hf endpoints scale-to-zero NAME` — 将推理端点缩放到零。`[--namespace TEXT --format CHOICE]`
- `hf endpoints update NAME` — 更新现有端点。`[--namespace TEXT --repo TEXT --accelerator TEXT --instance-size TEXT --instance-type TEXT --framework TEXT --revision TEXT --task TEXT --min-replica INTEGER --max-replica INTEGER --scale-to-zero-timeout INTEGER --scaling-metric CHOICE --scaling-threshold FLOAT --format CHOICE]`

### `hf extensions` — 管理 hf CLI 扩展。

- `hf extensions exec NAME` — 执行已安装的扩展。
- `hf extensions install REPO_ID` — 从公共 GitHub 仓库安装扩展。`[--force --format CHOICE]`
- `hf extensions list` — 列出已安装的扩展命令。`[--format CHOICE]`
- `hf extensions remove NAME` — 移除已安装的扩展。`[--format CHOICE]`
- `hf extensions search` — 搜索 GitHub 上可用的扩展（标记为 'hf-extension' 主题）。`[--format CHOICE]`

### `hf jobs` — 在 Hub 上运行和管理作业。

- `hf jobs cancel JOB_ID` — 取消作业 `[--namespace TEXT --format CHOICE]`
- `hf jobs hardware` — 列出作业可用的硬件选项 `[--format CHOICE]`
- `hf jobs inspect JOB_IDS` — 显示一个或多个作业的详细信息 `[--namespace TEXT --format CHOICE]`
- `hf jobs logs JOB_ID` — 获取作业的日志。`[--follow --tail INTEGER --namespace TEXT --format CHOICE]`
- `hf jobs labels JOB_ID` — 更新作业的标签。替换所有现有标签。`[--label TEXT --clear --namespace TEXT --format CHOICE]`
- `hf jobs ps` — 列出作业。`[--all --namespace TEXT --filter TEXT --format TEXT --quiet]`
- `hf jobs run IMAGE COMMAND` — 运行作业。`[--env TEXT --secrets TEXT --label TEXT --volume TEXT --env-file TEXT --secrets-file TEXT --flavor CHOICE --timeout TEXT --detach --namespace TEXT]`
- `hf jobs scheduled delete SCHEDULED_JOB_ID` — 删除计划作业。`[--namespace TEXT --format CHOICE]`
- `hf jobs scheduled inspect SCHEDULED_JOB_IDS` — 显示一个或多个计划作业的详细信息 `[--namespace TEXT --format CHOICE]`
- `hf jobs scheduled labels SCHEDULED_JOB_ID` — 更新计划作业的标签。替换所有现有标签。`[--label TEXT --clear --namespace TEXT --format CHOICE]`
- `hf jobs scheduled ps` — 列出计划作业 `[--all --namespace TEXT --filter TEXT --format TEXT --quiet]`
- `hf jobs scheduled resume SCHEDULED_JOB_ID` — 恢复（取消暂停）计划作业。`[--namespace TEXT --format CHOICE]`
- `hf jobs scheduled run SCHEDULE IMAGE COMMAND` — 计划作业。`[--suspend --concurrency --env TEXT --secrets TEXT --label TEXT --volume TEXT --env-file TEXT --secrets-file TEXT --flavor CHOICE --timeout TEXT --namespace TEXT]`
- `hf jobs scheduled suspend SCHEDULED_JOB_ID` — 暂停（挂起）计划作业。`[--namespace TEXT --format CHOICE]`
- `hf jobs scheduled uv run SCHEDULE SCRIPT` — 在 HF 基础设施上运行 UV 脚本（本地文件或 URL）`[--suspend --concurrency --image TEXT --flavor CHOICE --env TEXT --secrets TEXT --label TEXT --volume TEXT --env-file TEXT --secrets-file TEXT --timeout TEXT --namespace TEXT --with TEXT --python TEXT]`
- `hf jobs stats` — 获取作业的资源使用统计和指标 `[--namespace TEXT --format CHOICE]`
- `hf jobs uv run SCRIPT` — 在 HF 基础设施上运行 UV 脚本（本地文件或 URL）`[--image TEXT --flavor CHOICE --env TEXT --secrets TEXT --label TEXT --volume TEXT --env-file TEXT --secrets-file TEXT --timeout TEXT --detach --namespace TEXT --with TEXT --python TEXT]`

### `hf models` — 与 Hub 上的模型交互。

- `hf models card MODEL_ID` — 获取 Hub 上模型的模型卡片（README）。`[--metadata --text --format CHOICE]`
- `hf models info MODEL_ID` — 获取 Hub 上模型的信息。`[--revision TEXT --expand TEXT --format CHOICE]`
- `hf models list` — 列出 Hub 上的模型或模型仓库中的文件。`[--search TEXT --author TEXT --filter TEXT --num-parameters TEXT --sort CHOICE --limit INTEGER --expand TEXT --human-readable --tree --recursive --revision TEXT --format CHOICE]`

### `hf papers` — 与 Hub 上的论文交互。

- `hf papers info PAPER_ID` — 获取 Hub 上论文的信息。`[--format CHOICE]`
- `hf papers list` — 列出 Hub 上的每日论文。`[--date TEXT --week TEXT --month TEXT --submitter TEXT --sort CHOICE --limit INTEGER --format CHOICE]`
- `hf papers read PAPER_ID` — 以 markdown 格式阅读论文。`[--format CHOICE]`
- `hf papers search QUERY` — 在 Hub 上搜索论文。`[--limit INTEGER --format CHOICE]`

### `hf repos` — 管理 Hub 上的仓库。

- `hf repos branch create REPO_ID BRANCH` — 为 Hub 上的仓库创建新分支。`[--revision TEXT --type CHOICE --exist-ok --format CHOICE]`
- `hf repos branch delete REPO_ID BRANCH` — 从 Hub 上的仓库删除分支。`[--type CHOICE --format CHOICE]`
- `hf repos create REPO_ID` — 在 Hub 上创建新仓库。`[--type CHOICE --space-sdk TEXT --private --public --protected --exist-ok --resource-group-id TEXT --region CHOICE --flavor CHOICE --storage CHOICE --sleep-time INTEGER --secrets TEXT --secrets-file TEXT --env TEXT --env-file TEXT --volume TEXT --format CHOICE]`
- `hf repos delete REPO_ID` — 从 Hub 中删除仓库。这是不可逆操作。`[--type CHOICE --missing-ok --yes --format CHOICE]`
- `hf repos delete-files REPO_ID PATTERNS` — 从 Hub 上的仓库删除文件。`[--type CHOICE --revision TEXT --commit-message TEXT --commit-description TEXT --create-pr --format CHOICE]`
- `hf repos duplicate FROM_ID` — 在 Hub 上复制仓库（模型、数据集或 Space）。`[--type CHOICE --private --public --protected --exist-ok --flavor CHOICE --storage CHOICE --sleep-time INTEGER --secrets TEXT --secrets-file TEXT --env TEXT --env-file TEXT --volume TEXT --format CHOICE]`
- `hf repos list` — 列出所有仓库（模型、数据集、spaces、存储桶）及存储信息。`[--namespace TEXT --type CHOICE --search TEXT --limit INTEGER --format CHOICE]`
- `hf repos move FROM_ID TO_ID` — 将仓库从一个命名空间移动到另一个命名空间。`[--type CHOICE --format CHOICE]`
- `hf repos settings REPO_ID` — 更新仓库的设置。`[--gated CHOICE --private --public --protected --type CHOICE --format CHOICE]`
- `hf repos tag create REPO_ID TAG` — 为仓库创建标签。`[--message TEXT --revision TEXT --type CHOICE --format CHOICE]`
- `hf repos tag delete REPO_ID TAG` — 删除仓库的标签。`[--yes --type CHOICE --format CHOICE]`
- `hf repos tag list REPO_ID` — 列出仓库的标签。`[--type CHOICE --format CHOICE]`

### `hf skills` — 管理 AI 助手的技能。

- `hf skills add` — 下载 Hugging Face 技能并为 AI 助手安装。`[--claude --global --dest PATH --force --format CHOICE]`
- `hf skills preview` — 将生成的 `hf-cli` SKILL.md 打印到 stdout。`[--format CHOICE]`
- `hf skills update` — 更新已安装的 Hugging Face 市场技能。`[--claude --global --dest PATH --format CHOICE]`

### `hf spaces` — 与 Hub 上的 spaces 交互。

- `hf spaces card SPACE_ID` — 获取 Hub 上 Space 的 Space 卡片（README）。`[--metadata --text --format CHOICE]`
- `hf spaces dev-mode SPACE_ID` — 在 Space 上启用或禁用开发模式。`[--stop --format CHOICE]`
- `hf spaces hardware` — 列出 Spaces 可用的硬件选项。`[--format CHOICE]`
- `hf spaces hot-reload SPACE_ID` — 热重载 Space 的任何 Python 文件，无需完全重建 + 重启。`[--local-file PATH --skip-checks --skip-summary --format CHOICE]`
- `hf spaces info SPACE_ID` — 获取 Hub 上 space 的信息。`[--revision TEXT --expand TEXT --format CHOICE]`
- `hf spaces list` — 列出 Hub 上的 spaces 或 space 仓库中的文件。`[--search TEXT --author TEXT --filter TEXT --sort CHOICE --limit INTEGER --expand TEXT --human-readable --tree --recursive --revision TEXT --format CHOICE]`
- `hf spaces logs SPACE_ID` — 获取 Space 的运行或构建日志。`[--build --follow --tail INTEGER --format CHOICE]`
- `hf spaces pause SPACE_ID` — 暂停 Space。`[--format CHOICE]`
- `hf spaces restart SPACE_ID` — 重启 Space。`[--factory-reboot --format CHOICE]`
- `hf spaces search QUERY` — 使用语义搜索在 Hub 上搜索 spaces。`[--filter TEXT --sdk TEXT --include-non-running --description --limit INTEGER --format CHOICE]`
- `hf spaces secrets add SPACE_ID` — 为 Space 添加或更新 secrets。`[--secrets TEXT --secrets-file TEXT --format CHOICE]`
- `hf spaces secrets delete SPACE_ID KEY` — 从 Space 中移除 secret。`[--yes --format CHOICE]`
- `hf spaces secrets list SPACE_ID` — 列出 Space 的 secrets。Secret 值是只写的，不会返回。`[--format CHOICE]`
- `hf spaces settings SPACE_ID` — 更新 Space 的设置。`[--sleep-time INTEGER --hardware CHOICE --format CHOICE]`
- `hf spaces ssh SPACE_ID` — SSH 到 Space 的 Dev Mode 容器。`[--identity-file PATH --dry-run --auto --format CHOICE]`
- `hf spaces variables add SPACE_ID` — 为 Space 添加或更新环境变量。`[--env TEXT --env-file TEXT --format CHOICE]`
- `hf spaces variables delete SPACE_ID KEY` — 从 Space 中移除环境变量。`[--yes --format CHOICE]`
- `hf spaces variables list SPACE_ID` — 列出 Space 的环境变量。`[--format CHOICE]`
- `hf spaces volumes delete SPACE_ID` — 从 Space 中删除所有卷。`[--yes --format CHOICE]`
- `hf spaces volumes list SPACE_ID` — 列出 Space 中挂载的卷。`[--format CHOICE]`
- `hf spaces volumes set SPACE_ID` — 为 Space 设置（替换）卷。`[--volume TEXT --format CHOICE]`

### `hf webhooks` — 管理 Hub 上的 webhook。

- `hf webhooks create --watch TEXT` — 创建新 webhook。`[--url TEXT --job-id TEXT --domain CHOICE --secret TEXT --format CHOICE]`
- `hf webhooks delete WEBHOOK_ID` — 永久删除 webhook。`[--yes --format CHOICE]`
- `hf webhooks disable WEBHOOK_ID` — 禁用活动 webhook。`[--format CHOICE]`
- `hf webhooks enable WEBHOOK_ID` — 启用已禁用的 webhook。`[--format CHOICE]`
- `hf webhooks info WEBHOOK_ID` — 显示单个 webhook 的完整详细信息。`[--format CHOICE]`
- `hf webhooks list` — 列出当前用户的所有 webhook。`[--format CHOICE]`
- `hf webhooks update WEBHOOK_ID` — 更新现有 webhook。仅更改提供的选项。`[--url TEXT --watch TEXT --domain CHOICE --secret TEXT --format CHOICE]`

## 通用选项

- `--format` — 输出格式：`--format json`（或 `--json`）或 `--format table`（默认）。
- `-q / --quiet` — 仅打印 ID（每行一个）。
- `--revision` — Git 修订 ID，可以是分支名称、标签或提交哈希。
- `--token` — 使用用户访问令牌。优先设置 `HF_TOKEN` 环境变量，而不是传递 `--token`。
- `--type` — 仓库类型（model、dataset 或 space）。

## 将仓库挂载为本地文件系统

要将 Hub 仓库或存储桶挂载为本地文件系统 — 无需下载、复制、等待 — 使用 `hf-mount`。文件按需获取。GitHub：https://github.com/huggingface/hf-mount

安装：`curl -fsSL https://raw.githubusercontent.com/huggingface/hf-mount/main/install.sh | sh`

一些命令示例：
- `hf-mount start repo openai-community/gpt2 /tmp/gpt2` — 挂载仓库（只读）
- `hf-mount start --hf-token $HF_TOKEN bucket myuser/my-bucket /tmp/data` — 挂载存储桶（读写）
- `hf-mount status` / `hf-mount stop /tmp/data` — 列出或卸载

## 提示

- 使用 `hf <command> --help` 获取完整选项、描述、用法和实际示例
- 使用 `HF_TOKEN` 环境变量（推荐）或 `--token` 进行认证
- 使用 `hf update` 更新 CLI（使用检测到的安装方法的正确命令）
