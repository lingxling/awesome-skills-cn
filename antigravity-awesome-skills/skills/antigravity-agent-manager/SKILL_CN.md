---
name: antigravity-agent-manager
description: "使用独立的 Antigravity 2.0 Agent Manager 和 Antigravity IDE 配置和编排并行代理。"
category: general
risk: critical
source: self
source_type: self
date_added: "2026-06-04"
author: community
tags: [agent-manager, orchestration, multi-agent, setup]
tools: [antigravity, gemini]
---

# Antigravity Agent Manager

## 概述

一份使用独立的 **Antigravity 2.0 Agent Manager**（白色图标）与 **Antigravity IDE**（黑色图标）并行编排多代理系统的操作手册。

从版本 2.0 开始，Google 将 Agent Manager 与主 IDE 界面分离，删除了"打开 Agent Manager"按钮。此技能概述了如何安装、配置和运营两个环境并排运行，以同时在前端和后端项目上指导多个 AI 代理。

## 何时使用此技能

- 当您需要协调多个前端、后端或 QA 代理同时在同一代码库上工作时使用。
- 当设置双窗口工作区（Antigravity IDE + Antigravity 2.0 Agent Manager）时使用。
- 用于解决冲突或已过时的教程步骤，这些步骤提及集成的"打开 Agent Manager"按钮。

## 工作原理

### 步骤 1：并行安装

1. **保留您当前的 Antigravity IDE**：不要卸载经典 IDE（黑色图标）。
2. **下载 Antigravity 2.0**：从官方 Antigravity 下载页面获取独立 Agent Manager 应用程序。
3. **安装**：运行安装程序。它将安装在您现有的 IDE 旁边，而不会覆盖它。您现在应该有两个：
   - **Antigravity IDE**（黑色图标）— 您的代码编辑器和手动开发工作区。
   - **Antigravity 2.0**（白色图标）— 您的多代理编排仪表板。

### 步骤 2：双工作区设置

1. 打开 **Antigravity IDE** 和 **Antigravity 2.0** 应用程序。
2. 在两个应用程序中加载相同的项目目录（例如，`C:/Users/erwinpzocikk/Dev/GroupProjects/intIntercatedraAdmin`）。
3. 在 Agent Manager（白色图标）中，配置您的代理池。分配专门的角色（例如，`frontend-agent`、`backend-agent`、`qa-validator`）。

### 步骤 3：协调代理执行

1. 在 Agent Manager 中，定义任务范围。为防止目录冲突和竞态条件：
   - 将 `backend-agent` 分配给服务器目录（例如，`/server` 或 `/api`）。
   - 将 `frontend-agent` 分配给前端目录（例如，`/client` 或 `/src`）。
2. 并行运行代理。
3. 使用 Antigravity IDE（黑色图标）实时监控文件更改、审查差异并执行手动微调。

## 示例

### 示例 1：在多代理项目中定义独立范围

配置 Agent Manager 仪表板时，在提示中指定目标文件或目录以防止代理碰撞：

**后端代理任务提示：**
```text
角色：后端开发人员代理
工作区目标：/server
任务：在 server/routes/students.js 中添加新的 POST /api/v1/students 端点，并更新 database/models/student.js。不要编辑 /server 目录外的文件。
```

**前端代理任务提示：**
```text
角色：前端 UI 代理
工作区目标：/client
任务：在 client/components/StudentForm.jsx 下构建学生注册表单。消费 /api/v1/students 端点。不要编辑 /client 目录外的文件。
```

### 示例 2：通过 Git 同步更改

由于代理并行编写代码，请在 IDE 终端中使用 git 同步其工作：

```bash
# 在 Antigravity IDE 终端中，检查代理编写的更改
git status

# 在提交前审查差异
git diff

# 提交稳定的检查点，以便两个代理与主分支保持同步
git add .
git commit -m "feat: synchronize parallel front-end and back-end agent changes"
```

## 最佳实践

- ✅ **应该做：** 同时在一侧运行两个应用程序。
- ✅ **应该做：** 在 Agent Manager 中为每个代理强制执行严格的文件夹级别边界（范围）。
- ✅ **应该做：** 在让代理执行大规模重写之前，使用 git 分支或提交来检查进度。
- ❌ **不应该做：** 让多个代理同时编辑同一个文件，因为这会导致写冲突和 git 合并冲突。
- ❌ **不应该做：** 在黑色图标 IDE 中搜索"打开 Agent Manager"按钮；改用独立的白色图标应用程序。

## 限制

- 此技能假定您在 Windows/macOS 上安装两个应用程序时具有本地管理员权限。
- 文件锁的协调依赖于标准 IDE 文件系统观察者。如果更改未反映，请重新加载 IDE 工作区（`Ctrl+R` 或开发人员重新加载）。

## 常见陷阱

- **问题：** 代理覆盖彼此的代码或被卡在写入锁中。
  **解决方案：** 隔离他们的工作区。如果他们必须编辑同一文件，按顺序编排他们（例如，首先运行后端代理，提交其更改，然后运行前端代理）。
- **问题：** Agent Manager 更改在 IDE 中不可见。
  **解决方案：** 验证两个应用程序指向完全相同的绝对文件路径。在 Windows 上，小心映射的驱动器或符号链接。

## 相关技能

- `@antigravity-workflows` - 指导代理通过顺序多代理执行。
- `@antigravity-skill-orchestrator` - 用于任务复杂性评估和常规技能路由。
- `@gitops-workflow` - 在团队环境中协调提交和分支合并。
