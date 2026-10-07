---
name: awt-e2e-testing
description: "AI 驱动的 E2E 网页测试——AI 编码工具的眼睛和手。声明式 YAML 场景、Playwright 执行、视觉匹配（OpenCV + OCR）、平台自动检测（Flutter/React/Vue）、学习数据库。安装：npx skills add ksgisang/awt-skill --skill awt -g"
risk: critical
source: "https://github.com/ksgisang/awt-skill"
date_added: "2026-09-04"
---

# AWT — AI 驱动的 E2E 测试（测试版）

> `npx skills add ksgisang/awt-skill --skill awt -g`

AWT 给 AI 编码工具提供了通过真实浏览器查看和与网页应用程序交互的能力。您的 AI 设计 YAML 测试场景；AWT 用 Playwright 执行它们。

## 何时使用
- 需要通过带有声明式 YAML 场景的真实浏览器进行 AI 辅助端到端测试。
- 测试流程依赖视觉匹配、OCR 或平台自动检测，而不是稳定的 DOM 选择器。
- 想要一个 E2E 工具链，既能执行测试又能为 AI 编码工作流解释失败。

## 现在有什么作用
- YAML 场景 → Playwright 与类人交互
- 视觉匹配：OpenCV 模板 + OCR（无需 CSS 选择器）
- 平台自动检测：Flutter、React、Next.js、Vue、Angular、Svelte
- 结构化的失败诊断和调查清单
- 学习数据库：SQLite 中的失败→修复模式
- 5 个 AI 提供商：Claude、OpenAI、Gemini、DeepSeek、Ollama
- 技能模式：无需额外的 AI API 密钥

## 链接
- 主仓库：https://github.com/ksgisang/AI-Watch-Tester
- 技能仓库：https://github.com/ksgisang/awt-skill
- 云演示：https://ai-watch-tester.vercel.app

使用 AI 编码工具的帮助构建——为了帮助 AI 编码工具更好地测试而设计。

由 AILoopLab 的独立开发者积极开发。欢迎反馈！

## 示例

**用户请求:**

> 为结账流程创建并运行声明式浏览器测试，包括视觉断言和清晰的失败报告。

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
