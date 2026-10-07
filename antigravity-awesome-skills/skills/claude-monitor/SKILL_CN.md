---
name: claude-monitor
description: Claude Code 和本地系统性能监控。诊断运行缓慢问题，测量 CPU/RAM/磁盘，检查 API 延迟并生成系统健康报告。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- monitoring
- performance
- diagnostics
- system-health
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Claude Monitor — 性能诊断

## 概览

Claude Code 和本地系统性能监控。诊断运行缓慢问题，测量 CPU/RAM/磁盘，检查 API 延迟并生成系统健康报告。

## 何时使用此技能

- 用户提到"变慢"或相关话题
- 用户提到"运行缓慢"或相关话题
- 用户提到"卡顿"或相关话题
- 用户提到"滞后"或相关话题
- 用户提到"冻结"或相关话题
- 用户提到"claude 很慢"或相关话题

## 何时不使用此技能

- 任务与 claude monitor 无关
- 可以使用更简单、更具体的工具处理请求
- 用户需要不需要领域专业知识的通用帮助

## 工作原理

用于诊断和解决 Claude Code 和系统中的运行缓慢问题的技能。
确定瓶颈是本地（PC）还是远程（Claude API）并建议纠正措施。

## 何时使用

- 用户抱怨 Claude Code 运行缓慢或冻结
- 对话会话的切换加载缓慢
- Claude 的回应花费很长时间
- 使用 Claude Code 时 PC 似乎运行缓慢
- 任何关于性能、卡顿、运行缓慢的提及

## 1. 快速诊断 (Health_Check.Py)

始终作为第一步运行：

```bash
python C:\Users\renat\skills\claude-monitor\scripts\health_check.py
```

该脚本在约 3 秒内分析：
- **CPU**: 当前使用情况和每核心使用率。>80% = 可能的瓶颈
- **RAM**: 总计、已用、可用。>85% = 内存压力
- **浏览器**: 每个浏览器的进程和 RAM。>5GB 总计 = 超过标签页
- **Claude Code**: 进程和占用 RAM
- **磁盘**: 可用空间。<10% = 影响虚拟内存/性能
- **网络**: 到 Claude API 端点的延迟
- **诊断**: 自动分类问题并提供建议

## 2. 解释结果

该脚本返回包含 `diagnosis` 的 JSON：

- `bottleneck`: "cpu" | "ram" | "browsers" | "disk" | "network" | "claude_api" | "ok"
- `severity`: "critical" | "warning" | "ok"
- `suggestions`: 推荐操作列表
- `summary`: 中文摘要供显示给用户

**向用户显示 `summary`** 并提议执行建议。

## 3. 自动纠正措施

根据诊断，提供给用户：

#### 如果 CPU 使用率高 (>80%)：
- 列出消耗最多 CPU 的进程
- 建议关闭不必要的重型进程
- 检查 Windows Update 是否在后台运行

#### 如果浏览器占用大量资源 (>5GB RAM 或 >40 个进程)：
```bash
python C:\Users\renat\skills\claude-monitor\scripts\health_check.py --browsers-detail
```
显示每个浏览器的 RAM 并建议关闭哪些。**未得到用户明确许可，不要关闭任何进程。**

#### 如果磁盘满 (>85%)：
- 显示最大的文件夹
- 建议清理 Temp、浏览器缓存、回收站

#### 如果网络缓慢 (延迟 >500ms)：
- 测试与 api.anthropic.com 的连接
- 建议检查 VPN、代理或 WiFi 连接

## 4. 持续监控 (可选)

如果用户想要后台监控：

```bash
python C:\Users\renat\skills\claude-monitor\scripts\monitor.py --interval 30 --duration 300
```

参数：
- `--interval`: 每次采样之间的秒数 (默认: 30)
- `--duration`: 总持续时间（秒）(默认: 300 = 5 分钟)
- `--output`: 日志文件的路径 (默认: monitor_log.json)
- `--alert-cpu`: CPU 警报的阈值 (默认: 80)
- `--alert-ram`: RAM % 的警报阈值 (默认: 85)

监控器保存定期快照并在最后生成报告，包括：
- CPU 和 RAM 峰值
- 趋势（改进/恶化/稳定）
- 检测到的警报事件
- 最终建议

## 5. Claude API 基准测试 (可选)

要测试运行缓慢是否来自 API：

```bash
python C:\Users\renat\skills\claude-monitor\scripts\api_bench.py
```

测量本地 Claude Code 进程的响应时间（不进行 API 调用）。
与典型时间进行比较并指示是否在预期范围内。

## 参考阈值

| 指标 | 正常 | 警告 | 严重 |
|---------|-----|---------|----------|
| CPU % | <60% | 60-85% | >85% |
| RAM 使用 % | <70% | 70-85% | >85% |
| RAM 浏览器 | <3 GB | 3-6 GB | >6 GB |
| 浏览器进程 | <30 | 30-60 | >60 |
| 可用磁盘 | >15% | 10-15% | <10% |
| 网络延迟 | <200ms | 200-500ms | >500ms |

## 用户提示

呈现诊断时，包括以下上下文提示：

- **太多标签页 = 高 CPU/RAM**: 每个浏览器标签页都是一个单独的进程。
  50 个标签页 = 50 个进程竞争资源。
- **Claude Code 占用资源**: 它运行多个 Electron 进程。正常消耗 3-5 GB。
  但如果在多个会话下使用 >6 GB，考虑关闭旧会话。
- **会话切换缓慢**: 通常由高 CPU 或许多进程竞争引起。
  会话需要加载对话历史记录，如果 CPU 忙碌，会很慢。
- **磁盘接近满**: 影响虚拟内存（交换）的速度，可能导致
  普遍运行缓慢。

## 依赖关系

- Python 3.10+
- psutil（如果不可用，脚本会自动安装）
- 不需要 API 密钥

## 最佳实践

- 提供清晰、具体的项目和要求背景
- 在将建议应用于生产代码之前查看所有建议
- 与其他补充技能结合以进行全面分析

## 常见陷阱

- 将此技能用于超出其领域专业知识范围的任务
- 在不理解您特定背景的情况下应用建议
- 没有为准确分析提供足够的项目背景

## 限制
- 仅在任务与上述范围匹配时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果需要的输入、权限、安全边界或成功标准缺失，请停止并寻求澄清。
