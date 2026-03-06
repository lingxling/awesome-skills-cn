---
name: obsidian-cli
description: 使用 Obsidian CLI 与 Obsidian vaults 交互以读取、创建、搜索和管理笔记、任务、属性等。还支持插件和主题开发，具有重新加载插件、运行 JavaScript、捕获错误、截图和检查 DOM 的命令。当用户要求与他们的 Obsidian vault 交互、管理笔记、搜索 vault 内容、从命令行执行 vault 操作，或开发和调试 Obsidian 插件和主题时使用。
---

# Obsidian CLI

使用 `obsidian` CLI 与运行的 Obsidian 实例交互。需要 Obsidian 处于打开状态。

## 命令参考

运行 `obsidian help` 查看所有可用命令。这始终是最新的。完整文档：https://help.obsidian.md/cli

## 语法

**参数**使用 `=` 接受值。用空格引用值：

```bash
obsidian create name="我的笔记" content="你好世界"
```

**标志**是无值的布尔开关：

```bash
obsidian create name="我的笔记" silent overwrite
```

对于多行内容使用 `\n` 表示换行，使用 `\t` 表示制表符。

## 文件定位

许多命令接受 `file` 或 `path` 来定位文件。如果没有其中任何一个，则使用活动文件。

- `file=<name>` — 解析类似 wikilink（仅名称，不需要路径或扩展名）
- `path=<path>` — 从 vault 根目录开始的精确路径，例如 `folder/note.md`

## Vault 定位

命令默认针对最近聚焦的 vault。使用 `vault=<name>` 作为第一个参数来定位特定的 vault：

```bash
obsidian vault="我的 Vault" search query="测试"
```

## 常见模式

```bash
obsidian read file="我的笔记"
obsidian create name="新笔记" content="# 你好" template="模板" silent
obsidian append file="我的笔记" content="新行"
obsidian search query="搜索词" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] 新任务"
obsidian property:set name="状态" value="已完成" file="我的笔记"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="我的笔记"
```

在任何命令上使用 `--copy` 将输出复制到剪贴板。使用 `silent` 防止文件打开。在列表命令上使用 `total` 获取计数。

## 插件开发

### 开发/测试周期

对插件或主题进行代码更改后，遵循此工作流程：

1. **重新加载**插件以获取更改：
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **检查错误**——如果出现错误，修复并从步骤 1 重复：
   ```bash
   obsidian dev:errors
   ```
3. **视觉验证**——通过截图或 DOM 检查：
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **检查控制台输出**——查找警告或意外日志：
   ```bash
   obsidian dev:console level=error
   ```

### 其他开发者命令

在应用上下文中运行 JavaScript：

```bash
obsidian eval code="app.vault.getFiles().length"
```

检查 CSS 值：

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

切换移动模拟：

```bash
obsidian dev:mobile on
```

运行 `obsidian help` 查看其他开发者命令，包括 CDP 和调试器控件。
