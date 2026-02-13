---
name: web-design-guidelines
description: 审查UI代码是否符合Web界面指南。当被要求"审查我的UI"、"检查可访问性"、"审计设计"、"审查UX"或"根据最佳实践检查我的站点"时使用。
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web 界面指南

审查文件是否符合Web界面指南。

## 工作原理

1. 从下面的源URL获取最新指南
2. 读取指定文件（或提示用户输入文件/模式）
3. 根据获取的指南中的所有规则进行检查
4. 以简洁的`file:line`格式输出发现

## 指南来源

在每次审查之前获取最新指南：

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

使用WebFetch检索最新规则。获取的内容包含所有规则和输出格式说明。

## 用法

当用户提供文件或模式参数时：
1. 从上面的源URL获取指南
2. 读取指定文件
3. 应用获取的指南中的所有规则
4. 使用指南中指定的格式输出发现

如果未指定文件，询问用户要审查哪些文件。
