---
name: "playwright"
description: "当任务需要通过 `playwright-cli` 或捆绑的包装脚本从终端自动化真实浏览器（导航、表单填写、快照、截图、数据提取、UI 流程调试）时使用。"
---


# Playwright CLI 技能

使用 `playwright-cli` 从终端驱动真实浏览器。更喜欢捆绑的包装脚本，以便即使未全局安装 CLI 也能工作。将此技能视为 CLI 优先的自动化。除非用户明确要求测试文件，否则不要转向 `@playwright/test`。

## 前置条件检查（必需）

在建议命令之前，检查 `npx` 是否可用（包装器依赖于它）：

```bash
command -v npx >/dev/null 2>&1
```

如果不可用，请暂停并要求用户安装 Node.js/npm（它提供 `npx`）。逐字提供这些步骤：

```bash
# 验证 Node/npm 已安装
node --version
npm --version

# 如果缺少，请安装 Node.js/npm，然后：
npm install -g @playwright/cli@latest
playwright-cli --help
```

一旦 `npx` 存在，请继续使用包装脚本。全局安装 `playwright-cli` 是可选的。

## 技能路径（设置一次）

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
```

用户范围的技能安装在 `$CODEX_HOME/skills` 下（默认：`~/.codex/skills`）。

## 快速开始

使用包装脚本：

```bash
"$PWCLI" open https://playwright.dev --headed
"$PWCLI" snapshot
"$PWCLI" click e15
"$PWCLI" type "Playwright"
"$PWCLI" press Enter
"$PWCLI" screenshot
```

如果用户更喜欢全局安装，这也是有效的：

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

## 核心工作流程

1. 打开页面。
2. 快照以获取稳定的元素引用。
3. 使用最新快照中的引用进行交互。
4. 在导航或重大 DOM 更改后重新快照。
5. 在有用时捕获工件（截图、pdf、跟踪）。

最小循环：

```bash
"$PWCLI" open https://example.com
"$PWCLI" snapshot
"$PWCLI" click e3
"$PWCLI" snapshot
```

## 何时再次快照

在以下情况后再次快照：

- 导航
- 单击实质上更改 UI 的元素
- 打开/关闭模态框或菜单
- 选项卡切换

引用可能会过时。当命令因缺少引用而失败时，请再次快照。

## 推荐模式

### 表单填写和提交

```bash
"$PWCLI" open https://example.com/form
"$PWCLI" snapshot
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" fill e2 "password123"
"$PWCLI" click e3
"$PWCLI" snapshot
```

### 使用跟踪调试 UI 流程

```bash
"$PWCLI" open https://example.com --headed
"$PWCLI" tracing-start
# ...交互...
"$PWCLI" tracing-stop
```

### 多选项卡工作

```bash
"$PWCLI" tab-new https://example.com
"$PWCLI" tab-list
"$PWCLI" tab-select 0
"$PWCLI" snapshot
```

## 包装脚本

包装脚本使用 `npx --package @playwright/cli playwright-cli`，因此 CLI 可以在没有全局安装的情况下运行：

```bash
"$PWCLI" --help
```

除非仓库已经标准化为全局安装，否则更喜欢包装脚本。

## 参考资料

仅打开您需要的内容：

- CLI 命令参考：`references/cli.md`
- 实用工作流程和故障排除：`references/workflows.md`

## 防护栏

- 在引用元素 id（如 `e12`）之前始终快照。
- 当引用看起来过时时重新快照。
- 除非需要，否则更喜欢显式命令而不是 `eval` 和 `run-code`。
- 当您没有新的快照时，使用占位符引用（如 `eX`）并说明原因；不要使用 `run-code` 绕过引用。
- 当视觉检查有帮助时使用 `--headed`。
- 在此仓库中捕获工件时，使用 `output/playwright/` 并避免引入新的顶级工件文件夹。
- 默认为 CLI 命令和工作流程，而不是 Playwright 测试规范。
