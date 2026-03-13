---
name: ckm:brand
description: 品牌声音、视觉识别、信息框架、资产管理、品牌一致性。用于品牌内容、语调、营销资产、品牌合规性、风格指南。
argument-hint: "[update|review|create] [args]"
metadata:
  author: claudekit
  version: "1.0.0"
---

# 品牌

品牌识别、声音、信息、资产管理和一致性框架。

## 使用场景

- 品牌声音定义和内容语调指导
- 视觉识别标准和风格指南开发
- 信息框架创建
- 品牌一致性审查和审计
- 资产组织、命名和审批
- 调色板管理和排版规范

## 快速开始

**向提示中注入品牌上下文：**
```bash
node scripts/inject-brand-context.cjs
node scripts/inject-brand-context.cjs --json
```

**验证资产：**
```bash
node scripts/validate-asset.cjs <asset-path>
```

**提取/比较颜色：**
```bash
node scripts/extract-colors.cjs --palette
node scripts/extract-colors.cjs <image-path>
```

## 品牌同步工作流

```bash
# 1. 编辑 docs/brand-guidelines.md（或使用 /brand update）
# 2. 同步到设计令牌
node scripts/sync-brand-to-tokens.cjs
# 3. 验证
node scripts/inject-brand-context.cjs --json | head -20
```

**同步的文件：**
- `docs/brand-guidelines.md` → 真实来源
- `assets/design-tokens.json` → 令牌定义
- `assets/design-tokens.css` → CSS 变量

## 子命令

| 子命令 | 描述 | 参考 |
|--------|------|------|
| `update` | 更新品牌识别并同步到所有设计系统 | `references/update.md` |

## 参考资料

| 主题 | 文件 |
|------|------|
| 声音框架 | `references/voice-framework.md` |
| 视觉识别 | `references/visual-identity.md` |
| 信息传递 | `references/messaging-framework.md` |
| 一致性 | `references/consistency-checklist.md` |
| 指南模板 | `references/brand-guideline-template.md` |
| 资产组织 | `references/asset-organization.md` |
| 颜色管理 | `references/color-palette-management.md` |
| 排版 | `references/typography-specifications.md` |
| Logo 使用 | `references/logo-usage-rules.md` |
| 审批清单 | `references/approval-checklist.md` |

## 脚本

| 脚本 | 目的 |
|------|------|
| `scripts/inject-brand-context.cjs` | 提取品牌上下文用于提示注入 |
| `scripts/sync-brand-to-tokens.cjs` | 同步 brand-guidelines.md → design-tokens.json/css |
| `scripts/validate-asset.cjs` | 验证资产命名、大小、格式 |
| `scripts/extract-colors.cjs` | 提取并与调色板比较颜色 |

## 模板

| 模板 | 目的 |
|------|------|
| `templates/brand-guidelines-starter.md` | 新品牌的完整入门模板 |

## 路由

1. 从 `$ARGUMENTS`（第一个单词）解析子命令
2. 加载对应的 `references/{subcommand}.md`
3. 使用剩余参数执行