---
name: avalonia-layout-zafiro
description: "使用 Zafiro.Avalonia 进行现代 Avalonia UI 布局的指南，强调共享样式、通用组件和避免 XAML 冗余。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 使用 Zafiro.Avalonia 进行 Avalonia 布局

> 掌握现代、干净和可维护的 Avalonia UI 布局。
> **专注于语义容器、共享样式和最小 XAML。**

## 🎯 选择性阅读规则

**仅阅读与布局挑战相关的文件！**

---

## 📑 内容地图

| 文件 | 说明 | 何时阅读 |
|------|-------------|--------------|
| `themes.md` | 主题组织和共享样式 | 设置或调整应用主题 |
| `containers.md` | 语义容器（`HeaderedContainer`、`EdgePanel`、`Card`） | 构造视图和布局 |
| `icons.md` | 使用 `IconExtension` 和 `IconOptions` 的图标 | 添加和自定义图标 |
| `behaviors.md` | `Xaml.Interaction.Behaviors` 和避免转换器 | 实现复杂交互 |
| `components.md` | 通用组件和避免嵌套 | 创建可重用的 UI 元素 |

---

## 🔗 相关项目（示范实现）

有关真实世界的示例，请参考 **Angor** 项目：
`/mnt/fast/Repos/angor/src/Angor/Avalonia/Angor.Avalonia.sln`

---

## ✅ 干净布局清单

- [ ] **使用了语义容器？**（例如，`HeaderedContainer` 而不是带有手动标题的 `Border`）
- [ ] **避免了冗余属性？** 在 `axaml` 文件中使用共享样式。
- [ ] **最小化了嵌套？** 使用 `EdgePanel` 或通用组件展平布局。
- [ ] **通过扩展使用图标？** 使用 `{Icon fa-name}` 和 `IconOptions` 进行样式设置。
- [ ] **行为优于代码隐藏？** 为 UI 逻辑使用 `Interaction.Behaviors`。
- [ ] **避免了转换器？** 优先使用 ViewModel 属性或行为，除非必要。

---

## ❌ 反面模式

**不要:**
- 在视图中使用硬编码的颜色或大小（字面值）。
- 创建 `Grid` 和 `StackPanel` 的深层嵌套。
- 跨多个元素重复视觉属性（使用样式）。
- 使用 `IValueConverter` 处理属于 ViewModel 的简单逻辑。

**要:**
- 为颜色和笔刷使用 `DynamicResource`。
- 将重复的布局提取到通用组件中。
- 利用 Zafiro.Avalonia 特定的面板，如 `EdgePanel`，处理常见的 UI 模式。

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务清楚地匹配上述范围时使用此技能。
- 不要将输出视为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并寻求澄清。
