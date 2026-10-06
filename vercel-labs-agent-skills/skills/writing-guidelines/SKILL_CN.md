---
name: writing-guidelines
description: 审查文档/文章是否符合写作规范（Writing Guidelines）。当被要求"review my docs"、"check writing style"、"audit prose"、"review docs voice and tone"或"check this page against the writing handbook"时使用。
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# 写作规范

审查文件是否符合写作规范（Writing Guidelines）。

## 工作原理

1. 从下方的源URL获取最新的规范
2. 读取指定的文件（或提示用户提供文件/模式）
3. 对照获取到的规范检查所有规则
4. 以简洁的 `file:line` 格式输出发现的问题

## 规范来源

每次审查前获取最新的规范：

```
https://raw.githubusercontent.com/vercel-labs/writing-guidelines/main/command.md
```

使用WebFetch获取最新的规则。获取到的内容包含所有规则和输出格式说明。

## 用法

当用户提供一个文件或模式参数时：
1. 从上方的源URL获取规范
2. 读取指定的文件
3. 应用获取到的规范中的所有规则
4. 使用规范中指定的格式输出发现的问题

如果未指定文件，请询问用户要审查哪些文件。
