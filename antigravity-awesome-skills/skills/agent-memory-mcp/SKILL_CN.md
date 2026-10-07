---
name: agent-memory-mcp
description: "一个混合内存系统，为 AI 代理提供持久的、可搜索的知识管理（架构、模式、决策）。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 代理内存技能

此技能提供一个持久的、可搜索的内存库，它自动与项目文档同步。它作为 MCP 服务器运行，允许读取/写入/搜索长期内存。

## 前置条件

- Node.js (v18+)

## 设置

1. **检查仓库**：
   要求用户批准对命名仓库的网络访问，然后将
   固定版本克隆到临时目录，而不是活动的技能路径：

   ```bash
   review_dir="$(mktemp -d)"
   git clone --filter=blob:none https://github.com/webzler/agentMemory.git "$review_dir/agent-memory"
   git -C "$review_dir/agent-memory" checkout --detach 0409b7b7bb6fe443d0d4b6a6b1ee0d4df214f3cd
   git -C "$review_dir/agent-memory" ls-files
   ```

   阅读所有捆绑的文件并检查 `package.json`、锁文件、生命周期
   脚本、网络行为、凭证访问和文件系统范围。显示
   发现和精确提交，然后等待明确的用户批准。

2. **安装已审查的版本**：

   在批准后将审查的树复制到用户选择的位置。仅在
   已审查包脚本后安装锁定的依赖项：

   ```bash
   cd <approved-agent-memory-directory>
   npm ci
   npm run compile
   ```

3. **启动 MCP 服务器**：
   使用辅助脚本为您的当前项目激活内存库：

   ```bash
   npm run start-server <project_id> <absolute_path_to_target_workspace>
   ```

   _当前目录的示例：_

   ```bash
   npm run start-server my-project $(pwd)
   ```

## 功能（MCP 工具）

### `memory_search`

按查询、类型或标签搜索内存。

- **参数**：`query` (string)、`type?` (string)、`tags?` (string[])
- **用法**："查找所有身份验证模式" -> `memory_search({ query: "authentication", type: "pattern" })`

### `memory_write`

记录新知识或决策。

- **参数**：`key` (string)、`type` (string)、`content` (string)、`tags?` (string[])
- **用法**："保存此架构决策" -> `memory_write({ key: "auth-v1", type: "decision", content: "..." })`

### `memory_read`

通过密钥检索特定的内存内容。

- **参数**：`key` (string)
- **用法**："获取身份验证设计" -> `memory_read({ key: "auth-v1" })`

### `memory_stats`

查看内存使用分析。

- **用法**："显示内存统计信息" -> `memory_stats({})`

## 仪表板

此技能包括一个独立的仪表板来可视化内存使用情况。

```bash
npm run start-dashboard <absolute_path_to_target_workspace>
```

访问：`http://localhost:3333`

## 何时使用
此技能适用于执行概览中描述的工作流或操作。

## 限制条件
- 仅在任务明确与上述范围相匹配时才使用此技能。
- 不要将输出作为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并要求澄清。
- 在更改固定版本之前重新检查上游；提交固定可提高可重现性，但不是信任保证。
