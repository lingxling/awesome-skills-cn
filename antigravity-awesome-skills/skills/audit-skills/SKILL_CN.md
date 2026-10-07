---
name: audit-skills
description: "AI 技能和包的专家安全审计员。执行非侵入性静态分析，以识别恶意模式、数据泄露、系统稳定性风险，以及跨 Windows、macOS、Linux/Unix 和移动（Android/iOS）的混淆负载。"
category: security
risk: safe
source: community
date_added: "2026-03-07"
author: MAIOStudio
tags: [security, audit, skills, bundles, cross-platform]
tools: [claude, gemini, gpt, llama, mistral, etc]
---

# 审计技能（高级通用安全）

## 概述

AI 技能和包的专家安全审计员。执行非侵入性静态分析，以识别恶意模式、数据泄露、系统稳定性风险，以及跨 Windows、macOS、Linux/Unix 和移动（Android/iOS）的混淆负载。
2-4 句话是完美的。

## 何时使用此技能

- 需要审计 AI 技能和包中的安全漏洞时使用
- 进行跨平台安全分析时使用
- 用户询问验证技能合法性或执行安全审查时使用
- 扫描 AI 技能中的移动威胁时使用

## 工作原理

### 步骤 1：静态分析

执行非侵入性静态分析，以识别恶意模式、数据泄露、系统稳定性风险，以及混淆负载。

### 步骤 2：平台特定的威胁检测

分析代码中跨 Windows、macOS、Linux/Unix 和移动（Android/iOS）的平台特定安全问题。

#### 1. 权限、所有权和元数据操作
- **提升访问权限**: `sudo`, `chown`, `chmod`, `TakeOwnership`, `icacls`, `Set-ExecutionPolicy`。
- **元数据篡改**: `touch -t`, `setfile`（macOS）, `attrib`（Windows）, `Set-ItemProperty`, `chflags`。
- **风险**: 未授权访问、隐藏活动或使文件不可变。

#### 2. 文件/文件夹锁定和资源拒绝
- **模式**: `chmod 000`, `chattr +i`（不可变）, `attrib +r +s +h`, `Deny` ACEs in `icacls`。
- **全局操作**: 在 `%USERPROFILE%`、`/Users/` 或 `/etc/` 中锁定或隐藏文件夹。
- **风险**: 拒绝服务或数据锁定。

#### 3. 脚本执行和批处理调用
- **传统/批处理 Windows**: `.bat`, `.cmd`, `cmd.exe /c`, `vbs`, `cscript`, `wscript`。
- **Unix Shell**: `.sh`, `.bash`, `.zsh`, `chmod +x` 后跟执行。
- **PowerShell**: `.ps1`, `powershell -ExecutionPolicy Bypass -File ...`。
- **隐藏标志**: `-WindowStyle Hidden`, `-w hidden`, `-noprofile`。

#### 4. 危险安装/卸载和系统更改
- **Windows**: `msiexec /qn`, `choco uninstall`, `reg delete`。
- **Linux/Unix**: `apt-get purge`, `yum remove`, `rm -rf /usr/bin/...`。
- **macOS**: `brew uninstall`, 删除来自 `/Applications`。
- **风险**: 移除安全软件或创建未监控的安装路径。

#### 5. 移动应用和操作系统安全（Android/iOS）
- **Android 工具**: `adb shell`, `pm install`, `am start`, `apktool`, `dex2jar`, `keytool`。
- **Android 文件**: 操作 `AndroidManifest.xml`（权限）、`classes.dex` 或 `strings.xml`。
- **iOS 工具**: `xcodebuild`, `codesign`, `security find-identity`, `fastlane`, `xcrun`。
- **iOS 文件**: 操作 `Info.plist`、`Entitlements.plist` 或 `Provisioning Profiles`。
- **移动模式**: 越狱/root 检测旁路、移动源代码中硬编码的 API 密钥，或非移动技能中的敏感权限请求（相机、GPS、联系人）。
- **风险**: 恶意移动包注入、移动构建的凭据盗取或通过 ADB 的设备操纵。

#### 6. 信息披露和网络数据外泄
- **模式**: `curl`, `wget`, `Invoke-WebRequest`, `Invoke-RestMethod`, `scp`, `ftp`, `nc`, `socat`。
- **敏感数据**: `.env`, `.ssh`, `cookies.sqlite`, `Keychains`（macOS）, `Credentials`（Windows）, `keystore`（Android）。
- **内部网络**: 扫描内部 IP 或映射本地服务。

#### 7. 服务、进程和稳定性操纵
- **Windows**: `Stop-Service`, `taskkill /f`, `sc.exe delete`。
- **Unix/Mac**: `kill -9`, `pkill`, `systemctl disable/stop`, `launchctl unload`。
- **低级**: 直接磁盘访问（`dd`）、固件/BIOS 调用、内核模块管理。

#### 8. 混淆和持久化
- **编码**: `Base64`, `Hex`, `XOR` 循环, `atob()`。
- **持久化**: `reg add`（运行键）, `schtasks`, `crontab`, `launchctl`（macOS）, `systemd` 单元。
- **远程脚本管道**: 网络获取命令直接流入 shell 或 PowerShell 计算器。

#### 9. 合法性和范围（通用）
- **注册表对齐**: 与 `CATALOG.md` 交叉参考。
- **结构完整性**: 它是否遵循标准仓库布局？
- **健康范围**: "UI 设计"技能是否需要 `adb shell` 或 `sudo`？

### 步骤 3：报告

生成安全报告，包含评分（0-10）、平台目标识别、标记的操作、威胁分析和缓解建议。

## 示例

### 示例 1：安全审查

```markdown
"对此技能包执行安全审计"
```

### 示例 2：跨平台威胁分析

```markdown
"扫描此 AI 技能中的移动威胁"
```

## 最佳实践

- ✅ 执行非侵入性分析
- ✅ 检查权限提升模式
- ✅ 查找信息披露漏洞
- ✅ 分析跨平台威胁
- ❌ 审计期间不要执行潜在恶意代码
- ❌ 不要修改被审计的代码
- ❌ 不要忽视移动特定的安全问题

## 常见陷阱

- **问题:** 审计期间执行代码
  **解决方案:** 仅坚持使用静态分析方法

- **问题:** 遗漏跨平台威胁
  **解决方案:** 检查所有支持平台上的平台特定安全问题

- **问题:** 未能检测到混淆的负载
  **解决方案:** 查找编码模式，如 Base64、Hex、XOR 循环和 atob()

## 相关技能

- `@security-scanner` - 附加安全扫描功能

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
