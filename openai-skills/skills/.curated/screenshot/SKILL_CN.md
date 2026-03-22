---
name: "screenshot"
description: "当用户明确要求桌面或系统截图（全屏、特定应用或窗口，或像素区域），或者当工具特定的捕获功能不可用且需要操作系统级别的捕获时使用。"
---


# 屏幕截图捕获

每次都遵循这些保存位置规则：

1) 如果用户指定路径，请保存在那里。
2) 如果用户要求截图但没有路径，请保存到操作系统默认的屏幕截图位置。
3) 如果 Codex 需要截图进行自己的检查，请保存到临时目录。

## 工具优先级

- 当可用时，更喜欢工具特定的屏幕截图功能（例如：用于 Figma 文件的 Figma MCP/技能，或用于浏览器和 Electron 应用的 Playwright/agent-browser 工具）。
- 当明确要求、用于全系统桌面捕获，或当工具特定的捕获无法获取您需要的内容时，使用此技能。
- 否则，将此技能视为没有更好集成捕获工具的桌面应用的默认设置。

## macOS 权限预检（减少重复提示）

在 macOS 上，在窗口/应用捕获之前运行一次预检辅助程序。它检查屏幕录制权限，解释为什么需要它，并在一个地方请求它。

辅助程序将 Swift 的模块缓存路由到 `$TMPDIR/codex-swift-module-cache`，以避免额外的沙盒模块缓存提示。

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh
```

为了避免多个沙盒批准提示，如果可能，请在一个命令中结合预检 + 捕获：

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

对于 Codex 检查运行，将输出保留在临时目录：

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

使用捆绑的脚本以避免重新推导特定于操作系统的命令。

## macOS 和 Linux（Python 辅助程序）

从仓库根目录运行辅助程序：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py
```

常见模式：

- 默认位置（用户要求"截图"）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py
```

- 临时位置（Codex 视觉检查）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp
```

- 明确位置（用户提供了路径或文件名）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --path output/screen.png
```

- 按应用名称捕获应用/窗口（仅 macOS；子字符串匹配可以；捕获所有匹配的窗口）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

- 应用内的特定窗口标题（仅 macOS）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex" --window-name "Settings"
```

- 捕获之前列出匹配的窗口 id（仅 macOS）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --list-windows --app "Codex"
```

- 像素区域（x,y,w,h）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --region 100,200,800,600
```

- 聚焦/活动窗口（仅捕获最前面的窗口；使用 `--app` 捕获所有窗口）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --active-window
```

- 特定窗口 id（使用 --list-windows 在 macOS 上发现 id）：

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --window-id 12345
```

该脚本为每次捕获打印一个路径。当多个窗口或显示匹配时，它每行打印多个路径（每个捕获一个）并添加后缀，如 `-w<windowId>` 或 `-d<display>`。按顺序使用图像查看器工具查看每个路径，并且仅在需要或请求时操作图像。

### 工作流程示例

- "看看 <App> 并告诉我你看到了什么"：捕获到临时目录，然后按顺序查看每个打印的路径。

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

- "来自 Figma 的设计与实现不匹配"：首先使用 Figma MCP/技能捕获设计，然后使用此技能捕获运行的应用程序（通常到临时目录），并在任何操作之前比较原始屏幕截图。

### 多显示器行为

- 在 macOS 上，当连接多个显示器时，全屏捕获为每个显示器保存一个文件。
- 在 Linux 和 Windows 上，全屏捕获使用虚拟桌面（所有显示器在一个图像中）；需要时使用 `--region` 隔离单个显示器。

### Linux 先决条件和选择逻辑

辅助程序自动选择第一个可用工具：

1) `scrot`
2) `gnome-screenshot`
3) ImageMagick `import`

如果都不可用，请要求用户安装其中一个并重试。

坐标区域需要 `scrot` 或 ImageMagick `import`。

`--app`、`--window-name` 和 `--list-windows` 仅限 macOS。在 Linux 上，使用 `--active-window` 或在可用时提供 `--window-id`。

## Windows（PowerShell 辅助程序）

运行 PowerShell 辅助程序：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1
```

常见模式：

- 默认位置：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1
```

- 临时位置（Codex 视觉检查）：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp
```

- 明确路径：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Path "C:\Temp\screen.png"
```

- 像素区域（x,y,w,h）：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -Region 100,200,800,600
```

- 活动窗口（要求用户首先聚焦它）：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -Mode temp -ActiveWindow
```

- 特定窗口句柄（仅在提供时）：

```powershell
powershell -ExecutionPolicy Bypass -File <path-to-skill>/scripts/take_screenshot.ps1 -WindowHandle 123456
```

## 直接操作系统命令（回退）

当您无法运行辅助程序时使用这些。

### macOS

- 全屏到特定路径：

```bash
screencapture -x output/screen.png
```

- 像素区域：

```bash
screencapture -x -R100,200,800,600 output/region.png
```

- 特定窗口 id：

```bash
screencapture -x -l12345 output/window.png
```

- 交互式选择或窗口选择：

```bash
screencapture -x -i output/interactive.png
```

### Linux

- 全屏：

```bash
scrot output/screen.png
```

```bash
gnome-screenshot -f output/screen.png
```

```bash
import -window root output/screen.png
```

- 像素区域：

```bash
scrot -a 100,200,800,600 output/region.png
```

```bash
import -window root -crop 800x600+100+200 output/region.png
```

- 活动窗口：

```bash
scrot -u output/window.png
```

```bash
gnome-screenshot -w -f output/window.png
```

## 错误处理

- 在 macOS 上，首先运行 `bash <path-to-skill>/scripts/ensure_macos_permissions.sh` 以在一个地方请求屏幕录制。
- 如果您看到"屏幕截图检查在沙盒中被阻止"、"无法从显示创建图像"或在沙盒运行中出现 Swift `ModuleCache` 权限错误，请使用提升权限重新运行命令。
- 如果 macOS 应用/窗口捕获返回不匹配，请运行 `--list-windows --app "AppName"` 并使用 `--window-id` 重试，并确保应用程序在屏幕上可见。
- 如果 Linux 区域/窗口捕获失败，请使用 `command -v scrot`、`command -v gnome-screenshot` 和 `command -v import` 检查工具可用性。
- 如果保存到操作系统默认位置因沙盒中的权限错误而失败，请使用提升权限重新运行命令。
- 始终在响应中报告保存的文件路径。
