---
name: apple-notes-search
description: "通过 apple-notes MCP 服务器,对用户自己的 Apple Notes 进行语义+关键词搜索以及关联发现。当用户想要从自己的笔记中查找、回忆或整合信息,或想要挖掘出非显而易见的桥接关联/相关笔记时使用。运行于 macOS,设备本地。"
risk: critical
source: community
source_repo: connerkward/mcp-apple-notes
source_type: community
date_added: "2026-06-16"
author: connerkward
tags: [apple-notes, search, mcp, macos, semantic-search, knowledge]
tools: [claude-code]
license: "MIT"
license_source: "https://github.com/connerkward/mcp-apple-notes/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "需要第三方 MCP 配置以及 macOS 完全磁盘访问权限；不要纳入插件安全包。"
    docs: SKILL.md
---

# Apple Notes 搜索与关联发现

`apple-notes` 是一个 MCP 服务器,用于对用户自己的 Apple Notes 进行语义搜索和
关联发现——混合搜索、Swanson-ABC 桥接、实体线索,以及对其所写一切内容的
带引用综合整理。嵌入计算、搜索、BM25、聚类和桥接发现都在**本地设备上**
运行；只有**综合整理生成**这一步会调用 LLM（本地或云端,由用户自行选择）。

本技能涵盖两部分：(1) 你必须引导用户完成的一次性设置,以及 (2) 由于该服务器
暴露了许多工具,该为哪项任务选用哪个工具。

## 何时使用本技能

- 当用户想要从自己的 Apple Notes 中**查找、回忆或检索**某些内容时使用
  （"search my notes for X"、"what did I write about X"、"did I ever note Y"）。
- 当用户想要在自己的笔记中挖掘**非显而易见的关联**时使用
  （"find bridges/connections across my notes"、"what links X and Y"、
  "show related notes"）。
- 当用户想要从自己的笔记中**综合整理出一个观点**时使用
  （"summarize what I think about X from my notes"、"pull together
  everything I've written on X"）。
- 也适用于 "index my Apple Notes"、标签/文件夹查询,以及 "what's connected
  to X"。
- **不要**用于创建提醒事项,也不要用于非 Apple Notes 的笔记系统。

## 首先：MCP 是否已连接？

如果 `apple-notes` 工具不可用,说明服务器尚未注册——请先完成下面的
**设置**步骤。如果工具已存在但搜索返回“尚未索引”或为空,请先运行
`index-notes`（参见排名注意事项）。

## 设置（引导用户完成——这是本技能真正的价值所在）

该服务器直接读取 Apple Notes 的 SQLite 存储,因此 **bun** 二进制文件需要
完全磁盘访问权限。步骤如下,按顺序执行：

1. **安装 bun**（如果尚未安装）：`brew install oven-sh/bun/bun`
2. **克隆仓库并安装依赖：**
   ```bash
   git clone https://github.com/connerkward/mcp-apple-notes
   cd mcp-apple-notes
   git checkout <reviewed-tag-or-commit>
   bun install
   ```
3. **为 bun 授予完全磁盘访问权限。** 运行 `which bun`,然后打开系统设置 →
   隐私与安全性 → 完全磁盘访问权限,点击 `+`,添加该确切的 `bun`
   二进制文件路径（通常是 `/opt/homebrew/bin/bun` 或 `/usr/local/bin/bun`）。
   如果没有此权限,服务器就无法读取 NoteStore.sqlite,所有调用都会因权限
   错误而失败。（`bun install` 的 postinstall 脚本会尝试自动打开该设置面板。）
4. **注册 MCP 服务器**（根据用户使用的客户端选择）：
   - Claude Code：`claude mcp add apple-notes -- bun /absolute/path/to/mcp-apple-notes/index.ts --stdio`
   - Claude Desktop：添加到 `claude_desktop_config.json`：
     ```json
     { "mcpServers": { "apple-notes": {
         "command": "/Users/<you>/.bun/bin/bun",
         "args": ["/Users/<you>/mcp-apple-notes/index.ts", "--stdio"] } } }
     ```
   - 作为 Claude Code 插件安装（同时打包了本技能）：
     `/plugin marketplace add connerkward/ckw-skills`,然后执行
     `/plugin install apple-notes@connerkward`。
5. **重启客户端**,然后让用户询问**"Index my Apple Notes"**（或调用
   `index-notes`）。约 1,800 条笔记的首次索引需要几秒钟。

## 工具对照表 — 什么任务用什么工具

| 工具 | 何时使用 |
|------|----------|
| `index-notes` | 首次运行,或强制重建索引。后台任务,有实时进度。 |
| `search-notes` | **默认搜索。** 混合语义 + BM25,并经过重排序。可选 `folder`、`modifiedAfter`、`modifiedBefore`。"What did I write about X." |
| `find-notes` | 精确子串匹配（类似 Apple Notes 自带搜索框）。当用户想要字面字符串而非语义匹配时使用。可选 `folder`、日期范围。 |
| `get-note` | 按标题获取某一条完整笔记（模糊匹配兜底）。 |
| `list-notes` | 按最近修改时间列出笔记。可选 `folder`、日期范围、`limit`。 |
| `list-folders` | 所有文件夹及笔记数量。 |
| `list-tags` / `search-by-tag` | `#标签` 清单 / 带有指定标签的笔记。 |
| `related-notes` | 通过共享标签、`[[wikilinks]]` 以及向量相似度找到与某条笔记相关的笔记。"Show me related notes." |
| `bridge-notes` | **Swanson-ABC 桥接**——非显而易见的关联：一对（A、C）本身不直接相似,但都与某个共同的中间项 B 紧密关联。"Find non-obvious connections across my notes." 可选 `folder`、`limit`。不调用 LLM。 |
| `feed` | 以 JSON 形式输出的、以证据为先的排序关联流（桥接 + 抽象对 + 实体线索）。可选 `limit`。 |
| `entity-notes` / `list-entities` | "Where else do I talk about Mercedes?" 实体标签 → 按提及权重排序的笔记。**需要可选的实体关系图数据库**（`~/.mcp-apple-notes/layered_graph.db`）；若不存在,这些工具会说明如何生成它。 |
| `get-tables` | 从笔记中提取用竖线/Tab 分隔的表格。 |
| `create-note` / `update-note` | 创建或编辑笔记。 |
| `check-changes` | 自上次索引以来笔记是否有变化？（不会触发重新索引） |
| `index-health` | 同步状态、最近索引时间、笔记数量。如果结果看起来陈旧,运行此工具。 |

对于 "synthesize what I think about X",综合整理功能位于**网页应用**端点
（使用 `bun index.ts` 运行时位于 `http://localhost:3741/` 的
`GET /api/synthesize?q=`）,它会写出带有内联 `[n]` 引用的、有依据的答案,
并链接回源笔记。

## 排名注意事项（当结果看起来不对时,说明以下内容）

- **首次搜索前要先索引。** 没有索引 → 结果为空/垂圾内容；运行
  `index-notes`。
- **自动重新索引：** 每次搜索都会进行约 1ms 的变化检测,如果笔记有变化,
  会触发**一个**后台增量索引任务——搜索会立即从当前索引返回结果,
  等任务完成后再自动追上。如果刚编辑的笔记未出现在结果中,这是追赶
  延迟所致；重新运行搜索即可。
- **得分：** `score = RRF(vector, BM25) × title_boost × recency_factor`。
- **时间性查询**（`recent`、`latest`、`today`）会自动切换为 1 天的
  新近度半衰期,权重为 70%；普通查询则保持相关性为主（90 天半衰期,
  权重 10%）。
- **综合整理是唯一需要云端能力的部分。** 它需要一个 LLM：可以是本地的
  LM Studio / Ollama（`SYNTH_BASE_URL=http://localhost:1234/v1
  SYNTH_MODEL=<model> OPENAI_API_KEY=local`,笔记留在本地设备上）,
  也可以是真正的 OpenAI（需要有余额的 `OPENAI_API_KEY`,默认使用
  `gpt-4o-mini`）。其他所有部分——嵌入、搜索、BM25、聚类、桥接、
  实体识别——都在设备本地运行。

## 示例

**用户请求：**

> Use @apple-notes-search for this task: Semantic + keyword search and connection-discovery across the user's own Apple Notes via the apple-notes MCP server.

## 局限性

- 仅支持 macOS 和 Apple Notes；不会搜索 Obsidian、Notion、Google Docs
  或其他笔记存储。
- MCP 服务器需要本地文件系统权限来读取 Apple Notes 数据,因此设置工作
  无法仅在远程 shell 中完成。
- 搜索质量依赖于一个新鲜的本地索引。最近编辑的笔记可能需要
  `check-changes`、`index-health`,或在后台索引追赶完成后重新运行搜索。
- 实体相关工具需要可选的分层关系图数据库；若没有该数据库,请改用
  混合搜索、精确搜索、相关笔记或桥接功能。

## 致谢

本项目 fork 自
[RafalWilinski/mcp-apple-notes](https://github.com/RafalWilinski/mcp-apple-notes);
该 fork 直接读取 SQLite + protobuf,并新增了桥接、实体、feed 以及综合
整理功能。作者为 [Conner K Ward](https://github.com/connerkward)。许可证：MIT。
