---
name: agy-auto
description: "配置 agy-auto PreToolUse 安全门，以使用分层策略控制运行 Antigravity CLI (agy) 无人值守，而不是 --dangerously-skip-permissions。"
category: security
risk: critical
source: community
source_repo: onkarbadve/agy-auto
source_type: community
date_added: "2026-09-11"
author: onkarbadve
tags: [antigravity, agy, security, permissions, sandboxing, guardrails, cli]
license: "MIT"
license_source: "https://github.com/onkarbadve/agy-auto/blob/main/LICENSE"
tools: [antigravity]
---

# agy-auto — Antigravity 自动权限和安全门

## 概述

`agy-auto` 是 Google Antigravity CLI (`agy`) 的 PreToolUse 钩子和安全框架，它支持在不依赖 `--dangerously-skip-permissions` 的情况下进行安全的无人值守执行。它通过多层策略门控传递每个待处理的工具调用：确定性硬拒绝规则、工作区范围和只读操作的确定性快速允许、LLM 分类器回退（Gemini Flash Lite 或本地 llama.cpp）以及具有零环境权限的单次使用范围令牌批准。

## 何时使用此技能

- 当在无人值守或后台代理循环中运行 Antigravity CLI (`agy`) 时使用，并且您希望进行自动化工具权限控制而不暴露系统文件或凭证。
- 当您需要在 `agy` 工作流期间对 shell 命令、文件修改和网络出口进行粒度、可审计的控制时使用。
- 当设置安全的与 Antigravity 配对编程环境，防止提示注入攻击逃离工作区时使用。

## 工作原理

### 第 1 步：审查、固定和安装 agy-auto

> [!IMPORTANT]
> 因为 `agy-auto` 作为活跃的 PreToolUse 钩子安装在权限评估路径上，永远不要直接克隆可变分支到您的活跃插件目录。始终克隆到临时的准备区域文件夹，固定不可变的发布标签或提交 SHA，并在使钩子可执行之前检查代码库。

**选项 A：原生 Antigravity 插件（推荐）**
```bash
# 1. 克隆到临时审查目录并检出不可变发布标签
git clone https://github.com/onkarbadve/agy-auto.git /tmp/agy-auto-review
cd /tmp/agy-auto-review
git checkout v0.2.0-alpha

# 2. 在部署前检查 hook.sh 和 engine/ 文件
less hook.sh
python3 -m unittest -v tests/test_engine.py

# 3. 审查并验证后，复制到 Antigravity 插件目录并设置权限
mkdir -p ~/.gemini/config/plugins/agy-auto
cp -r . ~/.gemini/config/plugins/agy-auto/
chmod +x ~/.gemini/config/plugins/agy-auto/hook.sh
```

确保在 `~/.gemini/antigravity-cli/settings.json` 中配置了 `toolPermission: "always-proceed"`，以便钩子可以门控工具调用：
```json
{
  "toolPermission": "always-proceed"
}
```

**选项 B：通过安装程序进行全局钩子**
```bash
# 1. 克隆到隔离位置并固定发布版本
git clone https://github.com/onkarbadve/agy-auto.git ~/.local/share/agy-auto
cd ~/.local/share/agy-auto
git checkout v0.2.0-alpha

# 2. 审查并运行安装程序
chmod +x hook.sh
./install.sh                  # 在 hooks.json 中注册钩子，设置 always-proceed，运行烟雾测试
```

### 第 2 步：策略评估层

`agy-auto` 通过顺序层评估每个工具调用（首次匹配胜出）：

1. **硬拒绝**：立即阻止工作区外递归删除、凭证读取（`~/.ssh`、`.env`、云令牌）、git 历史重写（`push --force`、`rebase`）、包发布、系统文件写入（`/etc`、shell rc）和门控篡改。
2. **快速允许**：立即允许已解析的只读命令（`cat`、`grep`、`git status`）和工作区限制的写入，而无需调用 LLM。
3. **分类器**：模糊或灰色区域命令落入 LLM 分类器（Google Gemini 3.5 Flash Lite 免费层或本地 `llama.cpp` / Ollama 端点），该分类器针对对话上下文审查待处理调用，并在超时时故障关闭。
4. **范围化行动批准**：如果命令被拒绝或需要人工判断，引擎会发布严格绑定到 `(tool, normalized_cmd, cwd)` 的单次使用 6 字符操作令牌。您通过在聊天中回复 `> agy-approve <token>` 来批准它。会话化短语如"yes"或"proceed"被忽略，以防止环境权限泄露。

## 示例

### 示例 1：批准被阻止的命令

当未分类的命令被阻止时，`agy-auto` 输出一个令牌：
```text
tool call denied by pre-tool hook: [agy-auto/classifier] needs human approval: pip install requests. Reply '> agy-approve a1b2c3' in chat to proceed.
```
要为单次运行授权此特定命令，请直接在聊天中回复：
```text
> agy-approve a1b2c3
```

### 示例 2：配置本地模型后端

要使用 llama.cpp 或 Ollama 而不是云 API 完全离线运行 `agy-auto`，请编辑 `~/.gemini/config/agy-auto/policy.toml`：
```toml
[classifier]
endpoint = "http://127.0.0.1:8080/v1/chat/completions"
model = "qwen2.5-coder:7b"
timeout_s = 20
```

### 示例 3：运行无头调用

当以无头模式（`-p`）调用 `agy` 时，始终传递 `--add-dir` 以便 `agy-auto` 识别工作区边界：
```bash
agy --add-dir . -p "Run test suite and fix failing cases"
```

## 最佳实践

- ✅ 始终保持 `toolPermission: "always-proceed"` 启用，以便前工具钩子可以拦截和门控每个工具调用。
- ✅ 将自定义重复的开发工具（例如专门的编译器、格式化程序）添加到 `~/.gemini/config/agy-auto/policy.toml` 中的 `[fast_allow]` 以实现即时亚毫秒执行。
- ✅ 运行无头命令（`agy -p`）时传递 `--add-dir <path>`，以防止路径拒绝误报。
- ❌ 不要使用 `--dangerously-skip-permissions`；`agy-auto` 提供安全的自主执行，而无需移除安全护栏。
- ❌ 不要尝试会话化批准词（"approve"、"proceed"、"yes"）；批准严格要求短暂的操作令牌。

## 常见陷阱

- **问题：** 运行 `agy -p` 时命令失败，显示 `path is outside the workspace`。
  **解决方案：** 无头 `agy` 不会自动推断工作区根目录。传递 `--add-dir .`（例如 `agy --add-dir . -p "..."`）。
- **问题：** 分类器失败关闭，显示 `policy classifier unavailable (The read operation timed out)`。
  **解决方案：** 增加 `~/.gemini/config/agy-auto/policy.toml` 中的 `timeout_s`（尤其是在集成显卡上运行本地 LLM 时），或验证您的 `GEMINI_API_KEY`。
- **问题：** 对 `policy.toml` 或 `hook.sh` 的更改被 `[agy-auto/hard_deny]` 阻止。
  **解决方案：** `agy-auto` 强制进行自我保护，防止代理篡改安全门。直接从您自己的 shell 编辑策略文件。

## 限制

- `agy-auto` 只拦截通过工具调用（例如 `run_command`、`write_to_file`）执行的操作；它无法限制内部 LLM 网络推理或 Antigravity 自身的内部上下文收集文件读取。
- 需要在 Antigravity 设置中设置 `toolPermission: "always-proceed"` 以确保 PreToolUse 钩子拦截所有工具调用。
- Shell 解析很保守：无法静态解析的计算变量扩展的复杂管道将落入 LLM 分类器或需要手动令牌批准。

## 其他资源

- [agy-auto GitHub 存储库](https://github.com/onkarbadve/agy-auto)
- [Antigravity CLI 文档](https://github.com/google-gemini/antigravity-cli)
