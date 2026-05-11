---
name: autoskill
description: 通过 screenpipe 观察用户屏幕，检测重复的研究工作流，将其与现有的 scientific-agent-skills 进行匹配，并为尚未覆盖的模式起草新的技能（或组合现有技能的编排方案）。当用户要求分析其近期工作并基于实际行为提出技能时使用。需要在本地端口 3030 上运行 screenpipe 守护进程（https://github.com/screenpipe/screenpipe）—— 该技能没有其他数据来源，如果 screenpipe 不可达将拒绝运行。所有检测均在本地运行；只有脱敏后的聚类摘要会发送给 LLM。
allowed-tools: Read Write Edit Bash
license: MIT 许可证
metadata:
    skill-author: K-Dense Inc.
    requires: screenpipe
---

# autoskill

> **需要正在运行的 [screenpipe](https://github.com/screenpipe/screenpipe) 守护进程。** 该技能没有备用数据源 —— 它仅从本地 screenpipe HTTP API（默认 `http://localhost:3030`）读取数据。如果守护进程未运行，`run()` 将抛出 `ScreenpipeUnreachable` 并提供安装说明。

> **网络访问与环境变量。** 该技能会向以下端点发起经过身份验证的 HTTP 请求：(a) 用户本地回环地址上的 screenpipe 守护进程，以及 (b) 用户配置的 LLM 后端 —— 可选 `http://localhost:1234/v1`（LM Studio，默认）、`https://api.anthropic.com`（可选 Claude）或用户提供的 BYOK Foundry 网关。该技能读取三个环境变量 —— `SCREENPIPE_TOKEN`、`ANTHROPIC_API_KEY`、`FOUNDRY_API_KEY` —— 每个变量仅用于对其名称所对应的单一端点进行身份验证。没有其他网络目的地，没有遥测，不会向任何第三方传输数据。

## 概述

将用户自己的工作流历史 —— 由本地 [screenpipe](https://github.com/screenpipe/screenpipe) 守护进程被动捕获 —— 转化为新技能。该技能按需调用：用户指定一个时间窗口来触发它，它查询 screenpipe 的本地 HTTP API，对重复的工作流模式进行聚类，将每个模式与本仓库中的现有技能进行比较，并生成一个供用户审查、编辑和晋升的提案暂存文件夹。

## 何时使用此技能

当用户提出以下请求时，调用此技能：
- "分析我过去 4 小时 / 一天 / 一周的工作，并提出新技能。"
- "看看我一直在做什么，告诉我还有哪些没有被覆盖。"
- "根据我最近的工作流起草一个技能。"
- "为我重复的工作流找到组合方案。"

**不要** 在以下情况调用它：关于 screenpipe 本身的一次性问题、实时屏幕查询，或未经用户明确请求时 —— 该技能会分析敏感的本地内容，必须保持由用户显式触发。

## 隐私策略

- **Screenpipe 在捕获时处理应用/窗口过滤。** 将 `references/screenpipe-config.yaml` 复制到用户的 screenpipe 配置中以安装起始拒绝列表。敏感应用（密码管理器、即时通讯、银行）从一开始就不会被 OCR。
- **原始 OCR 数据永远不会离开本机。** `scripts/fetch_window.py` 通过本地回环 HTTP 拉取数据。`scripts/cluster.py` 将时间线缩减为应用/时长/标题摘要。`scripts/redact.py` 会在任何聚类摘要到达 LLM 之前，作为纵深防御措施，剥离电子邮件、API 密钥、Bearer 令牌和电话号码。
- **LLM 后端默认为 `local`。** 推荐配置是运行 `Gemma-4-31B-it` 的 [LM Studio](https://lmstudio.ai/) —— 具备强大的推理能力，模型大小适合大多数工作站 GPU，且数据永远不会离开您的机器。云端后端（`claude`、`foundry`）为可选，并在 `config.yaml` 中提供文档，供明确需要的用户使用。无论选择哪种后端，检测和嵌入始终在本地运行。
- **试运行模式**（`--plan`）会在任何 LLM 调用之前，打印将要分析的确切时间线。
- **本地主机的 TLS**（可选，用于企业策略）：请参阅 `references/https-proxy.md` 了解 Caddy 配置方案。

## 前置条件

### 1. Screenpipe 守护进程

可以安装官方发行版或从源码构建。无论哪种方式，守护进程默认都会将 HTTP 绑定到 `localhost:3030`。

**从源码构建**（推荐，如果您想要没有桌面 GUI 的 CLI 守护进程）：

```bash
git clone --depth 1 https://github.com/mediar-ai/screenpipe.git
cd screenpipe
cargo build -p screenpipe-engine --release
# 系统依赖（macOS）：cmake + 完整 Xcode.app（不仅仅是 Command Line Tools）。
#   brew install cmake
#   # 如果 xcodebuild 插件报错：sudo xcodebuild -runFirstLaunch
./target/release/screenpipe doctor   # 确认权限 + ffmpeg
./target/release/screenpipe record --disable-audio --use-pii-removal
```

首次运行会提示 macOS 屏幕录制权限。授予权限后重新启动。

### 2. Screenpipe API 令牌

本地 API 现在需要 Bearer 身份验证。获取您的令牌并导出：

```bash
export SCREENPIPE_TOKEN=$(screenpipe auth token)
```

（或者直接在 `config.yaml` 中设置 `screenpipe.token` —— 推荐使用环境变量，因为它可以避免将密钥存入版本控制。）

### 3. Python 环境

通过仓库根目录下的 `pipenv`：

```bash
pipenv install httpx pyyaml sentence-transformers
```

嵌入模型（`sentence-transformers/all-MiniLM-L6-v2`，约 80 MB）会在首次运行时下载。

### 4. 本地 LLM（默认路径）—— LM Studio

- 安装 [LM Studio](https://lmstudio.ai/)。
- 下载 `Gemma-4-31B-it`（或其他强大的推理模型；在 `config.yaml` 中调整 `local.model`）。
- 通过 CLI 加载以实现无头使用（无需 GUI）：

```bash
lms load gemma-4-31b-it --context-length 131072 --gpu max -y
lms status   # 确认服务器在 :1234 上运行
```

### 5. 云端 LLM 后端（可选，需主动选择）

仅当您明确选择不使用本地后端时：
- `claude`：设置 `ANTHROPIC_API_KEY`，在 `config.yaml` 中将 `backend` 切换为 `claude`。
- `foundry`：设置 `FOUNDRY_API_KEY`，将 `backend` 切换为 `foundry`，并将 `foundry.endpoint` 设置为您的企业网关 URL。

## 架构

```
screenpipe 守护进程（用户安装）
        │  HTTP on localhost:3030
        ▼
scripts/fetch_window.py    → 标准化时间线事件
scripts/redact.py          → 正则表达式清洗（纵深防御）
scripts/cluster.py         → 会话 + 聚类（仅限本地）
scripts/match_skills.py    → 与现有 135 个技能的 top-k 匹配（本地嵌入）
scripts/synthesize.py      → LLM 判断：复用 / 组合 / 全新
        │
        ▼
~/.autoskill/proposed/<timestamp>/        （默认；可通过 --out 覆盖）
  ├── report.md
  ├── composition-recipes/<name>/SKILL.md
  └── new-skills/<name>/SKILL.md

scripts/promote.py         → 用户批准的提案 → scientific-skills/<name>/
```

## 工作流

该技能在 `scripts/autoskill.py` 提供了一个统一的 CLI，包含三个子命令：

```bash
python scripts/autoskill.py doctor   --config config.yaml --skills-dir ../
python scripts/autoskill.py run      --start ... --end ... --config config.yaml
python scripts/autoskill.py promote  --proposed ~/.autoskill/proposed/<ts> --skills-dir ../ --name <skill>
```

### 0. 使用 `doctor` 进行预检

在完整运行之前，一次性验证所有依赖项：

```bash
python scripts/autoskill.py doctor \
  --config scientific-skills/autoskill/config.yaml \
  --skills-dir scientific-skills
```

报告涵盖 `config`（后端选择有效）、`skills_dir`（存在）、`screenpipe`（可达且已认证）和 `llm`（LM Studio 正在运行或 API 密钥存在）。任何失败都会返回非零退出码，并将有问题的行标记为 `error`。

### 1. 运行流水线

```bash
export SCREENPIPE_TOKEN=$(screenpipe auth token)
python scripts/autoskill.py run \
  --start "2026-04-17T00:00:00Z" \
  --end   "2026-04-17T23:59:59Z" \
  --config scientific-skills/autoskill/config.yaml \
  --skills-dir scientific-skills
```

提案默认输出到 `~/.autoskill/proposed/<timestamp>/`，将实验性输出保留在技能仓库之外。传递 `--out PATH` 以覆盖默认路径。

内部流程：
1. **获取** —— `fetch_window` 对 screenpipe 的 `/search` 端点进行分页查询，将事件规范化为 `{ts, app, window_title, text, content_type}`。
2. **脱敏** —— `redact` 从 OCR 文本和窗口标题中清除电子邮件、API 密钥、Bearer 令牌和电话号码，作为 screenpipe 自身 PII 移除功能之上的纵深防御。
3. **聚类** —— `segment_sessions` 按空闲间隙（默认 10 分钟）分割会话并丢弃短会话；`cluster_sessions` 按应用签名对会话进行分组，并保留大小达到 `min_cluster_size`（默认 2）的聚类。
4. **匹配** —— `load_skill_descriptions` 从 `scientific-skills/` 中的每个 `SKILL.md` 读取 frontmatter；`top_k_matches` 使用本地 `sentence-transformers` 嵌入（余弦相似度）将每个聚类与所有技能进行排名。
5. **合成** —— `synthesize` 提示配置的 LLM 后端将每个聚类分类为 `reuse`、`compose` 或 `novel`，并在适当时输出 SKILL.md 正文。
6. **报告** —— 写入 `<out_dir>/<ts>/report.md`，以及为每个提案输出 `new-skills/<name>/SKILL.md` 或 `composition-recipes/<name>/SKILL.md`。

添加 `--dry-run` 可在聚类后停止；这将跳过 LLM（以及 sentence-transformers 的加载），仅写入 `plan.md` 以供检查。

### 2. 审查与晋升

打开 `~/.autoskill/proposed/<ts>/report.md`，就地编辑草稿，删除任何不需要的内容。然后：

```bash
python scripts/autoskill.py promote \
  --proposed ~/.autoskill/proposed/2026-04-17T14-30-00 \
  --skills-dir scientific-skills \
  --name zotero-pubmed-helper
```

`promote` 将目录移动到 `scientific-skills/<name>/`，如果技能已存在则拒绝覆盖。如果未找到提案或目标已存在，则以非零状态退出并返回友好的错误信息。

## 配置

有关完整结构，请参阅 `config.yaml`。默认值（本地优先）：

```yaml
backend: local
local:
  endpoint: http://localhost:1234/v1   # LM Studio 的开发者服务器
  model: Gemma-4-31B-it

screenpipe:
  url: http://localhost:3030           # 或通过 Caddy 使用 https://screenpipe.local

cluster:
  min_session_minutes: 5
  idle_gap_minutes: 10
  min_cluster_size: 2
```

要选择使用云端后端：

```yaml
backend: claude                         # 或 foundry
claude:
  model: claude-opus-4-7
```

## 组合方案与新技能

- **compose**：LLM 判断认为通过组合现有技能即可覆盖该工作流。生成的 SKILL.md 有意保持精简 —— 仅包含 frontmatter 和一个按顺序调用现有技能的"工作流"部分。发现该技能的同一代理运行时随后可以端到端地调用它。
- **novel**：没有现有技能的组合能够覆盖它。会起草一份更完整的 SKILL.md，仍然遵循仓库规范（frontmatter、概述、何时使用、工作流）。用户在晋升前应始终审查新技能草稿。

## 测试

该技能由 `tests/` 中的一个小型 pytest 套件覆盖。每个脚本都通过依赖注入（模拟 HTTP 传输、存根后端、存根嵌入器）进行隔离单元测试：

```bash
cd scientific-skills/autoskill
python -m pytest tests/ -v
```

## 与本仓库中其他技能的组合

autoskill 的嵌入索引覆盖了所有 135 个同级技能。看起来像科学写作的工作流会匹配 `scientific-writing` / `literature-review` / `citation-management`；图表工作会匹配 `scientific-schematics` / `generate-image` / `infographics`；幻灯片准备会匹配 `scientific-slides` / `pptx`；等等。当一个聚类与两个或三个同级技能的得分都很高时，生成的组合方案会明确命名它们，以便用户未来的代理调用使用本仓库中已经记录优化的路径。
