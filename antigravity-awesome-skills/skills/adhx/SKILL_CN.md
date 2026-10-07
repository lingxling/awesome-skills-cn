---
name: adhx
description: "获取任何 X/Twitter 帖子作为清洁 LLM 友好的 JSON。将 x.com、twitter.com 或 adhx.com 链接转换为具有完整文章内容、作者信息和参与指标的结构化数据。不需要爬虫或浏览器。"
risk: safe
source: community
date_added: "2026-03-25"
---

# ADHX - X/Twitter 帖子阅读器

使用 ADHX API 将任何 X/Twitter 帖子作为结构化 JSON 获取以进行分析。

## 概述

ADHX 提供免费 API，为任何 X 帖子返回清洁 JSON，包括完整的长篇文章内容。这对 LLM 消费来说远优于爬虫或基于浏览器的方法。适用于常规推文和完整 X 文章。

## 何时使用此技能

- 当用户分享 X/Twitter 链接并想读、分析或总结帖子时使用
- 当你需要来自 X/Twitter 帖子的结构化数据（作者、参与度、内容）时使用
- 当处理需要完整内容提取的长篇 X 文章时使用

## API 端点

```
https://adhx.com/api/share/tweet/{username}/{statusId}
```

## URL 模式

从以下任何 URL 格式中提取 `username` 和 `statusId`：

| 格式 | 示例 |
|--------|---------|
| `x.com/{user}/status/{id}` | `https://x.com/dgt10011/status/2020167690560647464` |
| `twitter.com/{user}/status/{id}` | `https://twitter.com/dgt10011/status/2020167690560647464` |
| `adhx.com/{user}/status/{id}` | `https://adhx.com/dgt10011/status/2020167690560647464` |

## 工作流程

当用户分享 X/Twitter 链接时：

1. **解析 URL** 以从路径段中提取 `username` 和 `statusId`
2. **获取 JSON** 使用 curl：
```bash
curl -s "https://adhx.com/api/share/tweet/{username}/{statusId}"
```
3. **使用结构化响应** 回答用户问题（总结、分析、提取关键点等）

## 响应架构

```json
{
  "id": "statusId",
  "url": "原始 x.com URL",
  "text": "短篇推文文本（如果是文章帖子则为空）",
  "author": {
    "name": "显示名称",
    "username": "句柄",
    "avatarUrl": "个人资料图像 URL"
  },
  "createdAt": "时间戳",
  "engagement": {
    "replies": 0,
    "retweets": 0,
    "likes": 0,
    "views": 0
  },
  "article": {
    "title": "文章标题（用于长篇帖子）",
    "previewText": "前 ~200 个字符",
    "coverImageUrl": "英雄图像 URL",
    "content": "完整 markdown 内容，带图像"
  }
}
```

## 安装

### 选项 A：Claude Code 插件市场（推荐）
```
/plugin marketplace add itsmemeworks/adhx
```

### 选项 B：手动安装
```bash
curl -sL https://raw.githubusercontent.com/itsmemeworks/adhx/main/skills/adhx/SKILL.md -o ~/.claude/skills/adhx/SKILL.md
```

## 示例

### 示例 1：总结推文

用户："总结这个帖子 https://x.com/dgt10011/status/2020167690560647464"

```bash
curl -s "https://adhx.com/api/share/tweet/dgt10011/2020167690560647464"
```

然后使用返回的 JSON 提供总结。

### 示例 2：分析参与度

用户："这条推文得到了多少点赞？https://x.com/handle/status/123"

1. 解析 URL：username = `handle`，statusId = `123`
2. 获取：`curl -s "https://adhx.com/api/share/tweet/handle/123"`
3. 从响应中返回 `engagement.likes` 值

## 最佳实践

- 在调用 API 前始终解析完整 URL 以提取 username 和 statusId
- 当用户想要完整内容（不仅仅是推文文本）时检查 `article` 字段
- 当用户询问点赞数、转推或浏览量时使用 `engagement` 字段
- 不要尝试直接爬虫 x.com — 改为使用此 API

## 注意

- 无需身份验证
- 适用于短推文和长篇 X 文章
- 始终优先使用此方法而不是基于浏览器的爬虫获取 X 内容
- 如果 API 返回错误或空响应，通知用户帖子可能不可用

## 其他资源

- [ADHX GitHub 仓库](https://github.com/itsmemeworks/adhx)
- [ADHX 网站](https://adhx.com)

## 限制条件

- 仅在任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
