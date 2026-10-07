---
name: async-python-patterns
description: "使用 asyncio、并发编程模式和 async/await 实现异步 Python 应用的综合指导，用于构建高性能、非阻塞系统。"
risk: safe
source: community
date_added: "2026-02-27"
---

# 异步 Python 模式

使用 asyncio、并发编程模式和 async/await 实现异步 Python 应用的综合指导，用于构建高性能、非阻塞系统。

## 何时使用此技能

- 构建异步 Web API（FastAPI、aiohttp、Sanic）
- 实现并发 I/O 操作（数据库、文件、网络）
- 使用并发请求创建 Web 爬虫
- 开发实时应用（WebSocket 服务器、聊天系统）
- 同时处理多个独立任务
- 构建具有异步通信的微服务
- 优化 I/O 绑定工作负载
- 实现异步后台任务和队列

## 何时不使用此技能

- 工作负载是 CPU 绑定的，具有最少的 I/O。
- 简单的同步脚本就足够了。
- 运行时环境无法支持 asyncio/事件循环使用。

## 说明

- 澄清工作负载特性（I/O 与 CPU）、目标和运行时约束。
- 使用取消规则选择并发模式（任务、gather、队列、池）。
- 添加超时、反压和结构化错误处理。
- 为异步代码路径包含测试和调试指导。
- 如果需要详细示例，打开 `resources/implementation-playbook.md`。

参考 `resources/implementation-playbook.md` 以获取详细的模式和示例。

## 资源

- `resources/implementation-playbook.md` 用于详细的模式和示例。

## 限制

- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
