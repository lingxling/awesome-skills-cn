---
name: changelog-generator
description: 通过分析提交历史、分类变更并将技术提交转换为清晰、对客户友好的发布说明，自动从 git 提交创建面向用户的 changelog。将数小时的手动 changelog 编写转变为几分钟的自动生成。
---

# 变更日志生成器

此技能将技术 git 提交转换为抛光的、用户友好的变更日志，您的客户和用户实际上会理解和欣赏。

## 何时使用此技能

- 为新版本准备发布说明
- 创建每周或每月产品更新摘要
- 为客户记录变更
- 为应用商店提交编写变更日志条目
- 生成更新通知
- 创建内部发布文档
- 维护公共变更日志/产品更新页面

## 此技能的功能

1. **扫描 Git 历史**：分析特定时间段或版本之间的提交
2. **分类变更**：将提交分组到逻辑类别（功能、改进、错误修复、破坏性变更、安全）
3. **技术 → 用户友好翻译**：将开发者提交转换为客户语言
4. **专业格式化**：创建干净、结构化的变更日志条目
5. **过滤噪音**：排除内部提交（重构、测试等）
6. **遵循最佳实践**：应用变更日志指南和您的品牌声音

## 如何使用

### 基本用法

从您的项目仓库：

```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

```
Create release notes for version 2.5.0
```

### 使用特定日期范围

```
Create a changelog for all commits between March 1 and March 15
```

### 使用自定义指南

```
Create a changelog for commits since v2.4.0, using my changelog 
guidelines from CHANGELOG_STYLE.md
```

## 示例

**用户**："Create a changelog for commits from the past 7 days"

**输出**：
```markdown
# 更新 - 2024 年 3 月 10 日那周

## ✨ 新功能

- **团队工作区**：为不同项目创建单独的工作区。邀请团队成员并保持一切井井有条。

- **键盘快捷键**：按 ? 查看所有可用的快捷键。无需触摸鼠标即可更快导航。

## 🔧 改进

- **更快的同步**：文件现在在设备之间同步速度提高 2 倍
- **更好的搜索**：搜索现在包括文件内容，而不仅仅是标题

## 🐛 修复

- 修复了大图像无法上传的问题
- 解决了计划帖子中的时区混淆
- 更正了通知徽章计数
```

**灵感来源**：Manik Aggarwal 在 Lenny's Newsletter 中的用例

## 提示

- 从您的 git 仓库根目录运行
- 为重点变更日志指定日期范围
- 使用您的 CHANGELOG_STYLE.md 获得一致的格式
- 在发布前查看并调整生成的变更日志
- 直接将输出保存到 CHANGELOG.md

## 相关用例

- 创建 GitHub 发布说明
- 编写应用商店更新描述
- 为用户生成电子邮件更新
- 创建社交媒体公告帖子