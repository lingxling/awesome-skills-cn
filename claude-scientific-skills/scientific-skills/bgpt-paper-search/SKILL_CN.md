---
name: bgpt-paper-search
description: 通过 BGPT MCP 服务器搜索科学论文并检索从全文研究中提取的结构化实验数据。每篇论文返回 25+ 个字段，包括方法、结果、样本量、质量评分和结论。用于文献综述、证据综合，以及查找摘要中没有的实验细节。
allowed-tools: Bash
license: MIT
metadata:
    skill-author: BGPT
    website: https://bgpt.pro/mcp
    github: https://github.com/connerlambden/bgpt-mcp
---

# BGPT 论文搜索

## 概述

BGPT 是一个远程 MCP 服务器，它搜索从全文研究中提取的原始实验数据构建的科学论文精选数据库。与返回标题和摘要的传统文献数据库不同，BGPT 返回来自论文实际内容的结构化数据 — 方法、定量结果、样本量、质量评估，以及每篇论文 25+ 个元数据字段。

## 何时使用此技能

当您需要以下功能时使用此技能：
- 搜索具有特定实验细节的科学论文
- 进行系统性或范围性文献综述
- 查找跨研究的定量结果、样本量或效应量
- 比较不同研究中使用的方法
- 寻找具有质量评分或证据分级的论文
- 需要来自全文论文的结构化数据（而不仅仅是摘要）
- 为元分析或临床指南构建证据表

## 设置

BGPT 是一个远程 MCP 服务器 — 无需本地安装。

### Claude 桌面版 / Claude Code

添加到您的 MCP 配置：

```json
{
  "mcpServers": {
    "bgpt": {
      "command": "npx",
      "args": ["mcp-remote", "https://bgpt.pro/mcp/sse"]
    }
  }
}
```

### npm（替代方法）

```bash
npx bgpt-mcp
```

## 使用

配置完成后，使用 BGPT MCP 服务器提供的 `search_papers` 工具：

```
Search for papers about: "CRISPR gene editing efficiency in human cells"
```

服务器返回结构化结果，包括：
- **标题、作者、期刊、年份、DOI**
- **方法**：实验技术、模型、协议
- **结果**：带有定量数据的关键发现
- **样本量**：受试者/样本数量
- **质量评分**：研究质量评估
- **结论**：作者结论和影响

## 定价

- **免费 tier**：每个网络 50 次搜索，无需 API 密钥
- **付费**：使用来自 [bgpt.pro/mcp](https://bgpt.pro/mcp) 的 API 密钥，每结果 $0.01