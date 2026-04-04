---
name: defuddle
description: 使用 Defuddle CLI 从网页提取干净的 Markdown 内容，移除杂乱内容和导航以节省令牌。当用户提供 URL 来阅读或分析在线文档、文章、博客文章或任何标准网页时使用，而不是 WebFetch。不要用于以 .md 结尾的 URL — 这些已经是 Markdown，直接使用 WebFetch。
---

# Defuddle

使用 Defuddle CLI 从网页提取干净的可读内容。对于标准网页，优先使用它而不是 WebFetch——它会移除导航、广告和杂乱内容，减少令牌使用。

如果未安装：`npm install -g defuddle`

## 用法

始终使用 `--md` 进行 markdown 输出：

```bash
defuddle parse <url> --md
```

保存到文件：

```bash
defuddle parse <url> --md -o content.md
```

提取特定元数据：

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## 输出格式

| 标志 | 格式 |
|------|--------|
| `--md` | Markdown（默认选择） |
| `--json` | JSON，包含 HTML 和 markdown |
| (无) | HTML |
| `-p <name>` | 特定元数据属性 |
