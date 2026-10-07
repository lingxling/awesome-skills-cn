---
name: android-cli
description: 使用 `android` 命令行工具编排 Android 开发任务,包括项目创建、部署、SDK 管理和环境诊断。
category: tools
risk: critical
source: self
source_type: self
date_added: "2026-06-15"
author: Owais
tags: [android, cli, adb, mobile, build, emulator]
tools: [claude, cursor, gemini, antigravity]
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "Installer guidance executes remote Android CLI setup scripts; keep out of plugin-safe bundles."
    docs: SKILL.md
---

# Android CLI 专家

本技能提供使用 `android` CLI 工具的说明。该工具包含用于创建项目、运行应用、与设备交互以及管理 CLI 环境的各种命令。

## 何时使用

- 当你需要从命令行创建、配置或分析 Android 项目时使用。
- 当你需要与正在运行的 Android 设备交互、向其部署应用或对其截图时使用。
- 当你需要管理 Android SDK 组件、版本或虚拟设备(模拟器)时使用。
- 当你需要检查 UI 布局或运行以 XML 指定的流程测试(journey tests)时使用。

## 安装

如果 `android` 工具不在 PATH 中,先将对应平台的安装程序下载到一个私有的临时目录中,检查其内容,然后仅在用户确认来源和内容之后才运行它:

```bash
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/android-cli.XXXXXX")" || exit 1
curl -fsSL https://dl.google.com/android/cli/latest/linux_x86_64/install.sh -o "$tmpdir/install.sh"
sed -n '1,160p' "$tmpdir/install.sh"
# After review and explicit user confirmation:
bash "$tmpdir/install.sh"
```

macOS 或 Windows 请使用对应的 `darwin_arm64/install.sh` 或 `windows_x86_64/install.cmd` URL。不要将可变的网络安装脚本直接管道传入 shell 执行。

## SDK 管理

要管理 Android SDK 和工具的安装,请使用 `sdk` 命令。例如:

- `android sdk install <package>[@<version>]...`: 安装指定的包。可以指定多个包,用空格分隔。`<version>` 默认为最新版本。例如: `android sdk install platforms/android-30@2 platforms/android-34`
- `android sdk update [<pkg-name>]`: 将指定的包或所有包更新到最新版本。
- `android sdk remove <pkg-name>`: 从本地 SDK 中移除一个包。
- `android sdk list --all`: 列出已安装和可用的 SDK 包。

## 项目创建

使用 `create` 命令从模板创建项目。

例如:
```bash
android create empty-activity --name="My App" --output=./my-app
```

## 与设备交互

关于与运行中设备交互的更多信息,请参见[这里](references/interact.md)。

## 运行流程测试(Journey Tests)

关于运行 journey 的更多信息,请参见[这里](references/journeys.md)。

## 文档搜索

`docs` 命令在 Android 知识库中搜索权威、高质量的 Android 开发者文档。
只需提供几个关键词,该工具就会返回包含 Android API 或库使用示例或指导的高质量文章。
当你需要获取关于如何完成 Android 特定任务的更多信息,或想了解更多关于 Android API、界面(surfaces)、库或设备的信息时,使用此工具。

获取关于 Android 概念的最新信息时,始终使用此工具。典型的良好使用场景包括:
  - 查找 API 的迁移指南。
  - 查找 API 的使用示例。
  - 查找关于 Android API 的最新信息。
  - 查找 Android 相关概念的最佳实践。

## 运行 APK

使用 `run` 命令运行 Android 应用。

## 管理模拟器

使用 `android emulator` 命令管理 Android 虚拟设备(AVD)。

## 捕获截图

使用 `android screen capture -o <file path>` 命令捕获已连接 Android 设备当前屏幕的图像并输出为文件。

## 管理技能

使用 `android skills` 命令管理 Android 的 antigravity agent 技能。

## 检查 UI 布局

使用 `android layout` 命令检查 Android 应用的 UI 布局。它会以 JSON 格式返回该 Android 应用的布局树。在调试 UI 错误时,这通常比截图更快。

## 更新 CLI

使用 `android update` 命令更新 Android CLI。

## 局限性

- 必须已安装 `android` CLI 且可在 `PATH` 中找到;否则请先安装,或使用上文的平台特定安装指引。
- 设备、模拟器、SDK 和文档相关命令可能依赖于本地 Android SDK 状态、网络访问和已连接的硬件。
- 将生成的命令视为对环境敏感的内容:在运行之前检查路径、包名、设备序列号以及安装/更新目标。

## Android 帮助输出

```text
Usage: android [-hV] [--sdk=PARAM] [COMMAND]
  -h, --help        Show this help message and exit.
      --sdk=PARAM   Path to the Android SDK
  -V, --version     Print version information and exit.
Commands:
  create    Create a new Android project
  describe  Analyzes an Android project to generate descriptive metadata.
  docs      Android documentation commands
  emulator  Emulator commands
  help      Shows the help of all commands
  info      Print environment information (SDK Location, etc.)
  init      Initializes the environment (eg. skills) for Android CLI.
  layout    Returns the layout tree of an application
  run       Deploy an Android Application
  screen    Commands to view the device
  sdk       Download and list SDK packages
  skills    Manage skills
  update    Update the Android CLI

create
          Usage: android create [-h] [--verbose] [--list] [--minSdk=api]
                                --name=applicationName [-o=dest-path] [template-name]
          Create a new Android project
                [template-name]      The template name
            -h, --help               Show this help message and exit.
                --minSdk=api         The 'minSdk' supported by the application (default
                                       is defined in the template)
                --name=applicationName
                                      The name of the application (e.g. 'My Application')
            -o, --output=dest-path   The destination project directory path (default is
                                       '.')
                --verbose            Enables verbose output
                --list               List all available templates

describe
          Usage: android describe [-hV] [--project_dir=PARAM]
          Analyzes an Android project to generate descriptive metadata.
          This command identifies and outputs the paths to JSON files that detail the
          project's structure, including build targets and their corresponding output
          artifact locations (e.g., APKs). This information enables other tools and
          commands to locate build artifacts efficiently.
            -h, --help                Show this help message and exit.
                --project_dir=PARAM   The project directory to describe
            -V, --version             Print version information and exit.

docs
          Usage: android docs [-h] [COMMAND]
          Android documentation commands
            -h, --help   Show this help message and exit.
          Commands:
            search  Search Android documentation
            fetch   Fetch Android documentation

emulator
          Usage: android emulator [-h] [COMMAND]
          Emulator commands
            -h, --help   Show this help message and exit.
          Commands:
            create  Creates a virtual device
            start   Launches the specified virtual device. This command will return when
                      the emulator is fully started and ready to use.
            stop    Stops the specified virtual device
            list    Lists available virtual devices
            remove  Delete a virtual device

help
          Usage: android help [COMMAND]
          Shows the help of all commands
                [COMMAND]   The command to show help for

info
          Usage: android info <field>
          Print environment information (SDK Location, etc.)
                <field>   The specific field to print the value of. If omitted print all.

init
          Usage: android init
          Initializes the environment (eg. skills) for Android CLI.

layout
          Usage: android layout [-dhp] [--device=PARAM] [-o=PARAM]
          Returns the layout tree of an application
            -d, --diff           Returns a flat list of the layout elements that have
                                   changed since the last invocation of ui-dump
                --device=PARAM   The device serial number
            -h, --help           Show this help message and exit.
            -o, --output=PARAM   Writes the layout tree to the specified file or
                                   directory. If omitted, prints the tree to standard
                                   output
            -p, --pretty         Pretty-prints the returned JSON

run
          Usage: android run [-h] [--debug] [--activity=PARAM] [--device=PARAM]
                             [--type=PARAM] [--apks=PARAM[,PARAM...]]...
          Deploy an Android Application
                --activity=PARAM   The activity name
                --apks=PARAM[,PARAM...]
                                   The paths to the APKs
                --debug            Run in debug mode
                --device=PARAM     The device serial number
            -h, --help             Show this help message and exit.
                --type=PARAM       The component type (ACTIVITY, SERVICE, etc.)

screen
          Usage: android screen [-h] [COMMAND]
          Commands to view the device
            -h, --help   Show this help message and exit.
          Commands:
            capture  Outputs the device screen to a PNG
            resolve  Target UI elements visually

sdk
          Usage: android sdk [COMMAND]
          Download and list SDK packages
          Commands:
            install  Install SDK packages
            update   Update one or all packages to the latest version
            remove   Remove a package from the SDK
            list     List installed and available SDK packages

skills
          Usage: android skills [COMMAND]
          Manage skills
          Commands:
            add     Install a skill
            remove  Remove a skill
            list    List available skills
            find    Find skills by keyword

update
          Usage: android update [--url=PARAM]
          Update the Android CLI
                --url=PARAM   The URL to download the update from
```
