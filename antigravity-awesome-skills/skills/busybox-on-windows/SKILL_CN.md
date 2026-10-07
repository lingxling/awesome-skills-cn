---
name: busybox-on-windows
description: "如何使用 Win32 版本的 BusyBox 在 Windows 上运行许多标准 UNIX 命令行工具。"
risk: safe
source: community
date_added: "2026-02-27"
---

BusyBox 是一个单二进制文件，实现了许多常见的 Unix 工具。

仅在 Windows 上使用此技能。如果你使用的是 UNIX，请停止。

仅当你在与本文档相同的目录中找不到 `busybox.exe` 文件时，才运行以下步骤。
这些是 PowerShell 命令，如果你有经典的 `cmd.exe` 终端，则必须使用 `powershell -Command "..."` 来运行它们。
1. 打印 CPU 类型：`Get-CimInstance -ClassName Win32_Processor | Select-Object Name, NumberOfCores, MaxClockSpeed`
2. 打印操作系统版本：`Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" | Select-Object ProductName, DisplayVersion, CurrentBuild`
3. 通过运行以下 PowerShell 命令之一下载合适的 BusyBox 版本：
   - 32 位 x86 (ANSI)：`$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox.exe -OutFile busybox.exe`
   - 64 位 x86 (ANSI)：`$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox64.exe -OutFile busybox.exe`
   - 64 位 x86 (Unicode)：`$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox64u.exe -OutFile busybox.exe`
   - 64 位 ARM (Unicode)：`$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox64a.exe -OutFile busybox.exe`

有用的命令：
- 帮助：`busybox.exe --list`
- 可用的 UNIX 命令：`busybox.exe --list`

用法：在 UNIX 命令前加上 `busybox.exe`，例如：`busybox.exe ls -1`

如果需要在另一个 CWD 下运行 UNIX 命令，则使用 `busybox.exe` 的绝对路径。

文档：https://frippery.org/busybox/
原始 BusyBox：https://busybox.net/

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 示例

**用户请求：**

> 使用 @busybox-on-windows 完成此任务：如何使用 Win32 版本的 BusyBox 在 Windows 上运行许多标准 UNIX 命令行工具。

## 限制
- 仅当任务清楚地符合上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
