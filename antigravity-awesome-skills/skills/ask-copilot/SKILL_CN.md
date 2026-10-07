---
name: ask-copilot
description: "在非交互模式下使用 GitHub Copilot CLI 提问、审查代码或生成片段，无需手动交互。"
category: development
risk: critical
source: self
source_repo: cshara1/antigravity-awesome-skills
source_type: self
date_added: "2026-07-08"
author: cshara1
tags: [copilot, github, cli, review, prompt]
tools: [claude, cursor, gemini]
---

# 询问 Copilot

## 概览

此技能允许代理以非交互（无头）模式与 GitHub Copilot CLI (`copilot`) 交互。当用户明确想要来自 GitHub Copilot 模型的次要建议、代码审查、解释或代码生成时使用此技能。

当技能是此代码库的原始版本且不需要 README 外部来源信用时，使用 `source: self` 和 `source_type: self`。

Copilot 是外部服务。将提示、文件路径、片段、代码库内容、命令输出和生成建议视为可能离开本地环境的数据。

## 何时使用此技能

- **仅用户请求**：**仅当**用户明确要求"咨询 Copilot"、"询问 Copilot"、"与 Copilot 审查"或明确要求使用 Copilot 的第二意见时使用此技能。
- **不自动调用**：为了遵守隐私政策，代理不得在没有明确用户同意的情况下自动调用此技能来自行第二意见或检查。

## 工作原理

### 步骤 1：请求明确的用户同意

在执行任何引用本地文件、代码库路径、片段、命令输出、秘密邻近配置或私有项目上下文的命令前，你**必须**获得明确的用户同意以向 GitHub Copilot 发送该材料。

在允许 Copilot 运行工具、执行 shell 命令、编辑文件、安装包或变更工作区前请求单独的批准。

### 步骤 2：使用最少允许标志执行

为防止 TUI 锁定，使用无头标志执行 `copilot` 命令。不要为例行 Q&A 或审查使用 `--yolo`、`--allow-all-tools` 或 `--allow-all-paths` 等笼统绕过。

- **用于只读 / 常规 Q&A**：仅在提示中发送用户批准、经过编辑的文本。不要授予 Copilot 宽泛的本地路径访问权限；当提示已包含批准的上下文时不需要。
- **用于受信任的变更任务**：如果 CLI 支持，优选范围权限标志。仅在用户明确授权 Copilot 为特定任务执行工具和变更工作区后使用笼统变更绕过。

### 步骤 3：使用会话管理（可选）

为维持对话上下文，使用 `--name` 和 `--resume` 标志，或在后续调用上传递 `--session-id`。

## 示例

### 示例 1：常规问题（只读）

不需要代码库路径访问或变更权限。
```bash
copilot -p "解释如何在 TypeScript 中实现去抖动函数" -s
```

### 示例 2：代码审查（批准的文件摘录）

始终在执行前与用户确认确切的文件和摘录。将路径保留在带引号的变量中；从静态指令加上批准的摘录构建提示。Shell 不会重新计算命令替换输出，因此审查文件中的元字符保持为提示文本而不是 shell 语法：
```bash
review_file="path/to/file.ts"
test -f "$review_file" || { echo "File not found: $review_file" >&2; exit 1; }
copilot -p "$(printf '%s\n\n' 'Review this approved excerpt for potential memory leaks:'; sed -n '1,220p' -- "$review_file")" -s
```

不要通过将用户控制的提示文本、路径、问题内容或文件名插入 shell 源来构造 shell 命令。仅使用固定命令结构、带引号的变量和批准的文件内容。

### 示例 3：命名会话管理

```bash
copilot -p "Remember this session label for follow-up questions." -s --name "my-session-name"
copilot -p "总结此会话中的先前建议。" -s --resume "my-session-name"
```

## 最佳实践

- ✅ **应该**：在将任何项目文件上传到第三方端点前请求用户同意。
- ✅ **应该**：仅发送批准的、经过编辑的摘录；将 Copilot 排除在更广泛的工作区之外。
- ✅ **应该**：将不受信任的值保留在带引号的变量或命令输入中，从不在 shell 源中。
- ✅ **应该**：使用 `-s`（静默）来抑制元数据和统计，仅留下干净输出。
- ❌ **不应该**：在没有用户明确要求的情况下自动为背景第二意见触发此技能。
- ❌ **不应该**：在没有明确批准的情况下向 Copilot 发送文件、日志、环境详情或私有代码库上下文。
- ❌ **不应该**：为审查使用 `--allow-all-paths`，或在 `copilot -p "..."` 内插入不受信任的文本。
- ❌ **不应该**：在后台任务中运行 `copilot` 而不使用权限绕过标志，因为它会挂起等待交互输入。

## 限制

- 此技能不会替代环境特定验证、测试或专家审查。
- 如果缺少必需的输入、权限或安全边界，请停止并要求澄清。
- Copilot 响应可能不完整、过时或错误；在使用前在本地验证任何建议代码。

## 安全性和安全性说明

- `--yolo` 标志绕过所有权限提示并允许 Copilot CLI 运行任意 shell 命令和变更工作区文件。它必须被视为高风险选项，永远不要默认使用。
- 始终检查发送的代码/文件不包含敏感凭证、API 密钥或私有环境变量。
- 当仅需要小上下文样本时，优选经过编辑的片段而不是完整文件。
- `--allow-all-paths` 授予 Copilot 比狭隘审查所需更宽泛的本地可见性；它不是只读最小权限标志。

## 常见陷阱

- **问题**：终端挂起或命令超时。
  **解决方案**：确保 `-p`（或 `--prompt`）和所需的最窄非交互权限标志都存在于命令参数中。没有所需的权限标志，CLI 可能会提示确认并挂起无头流程。

## 相关技能

- `@cli-assistant` - 如何一般与 CLI 工具交互。
