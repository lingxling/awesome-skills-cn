---
name: aws-mcp-setup
description: "为文档搜索和 API 访问配置 AWS MCP 服务器。当设置 AWS MCP、配置 AWS 文档工具、排除 MCP 连接问题，或当用户提及 aws-mcp、awsdocs、uvx 设置或 MCP 服务器配置时使用。"
risk: critical
source: https://github.com/zxkane/aws-skills/tree/main/plugins/aws-common/skills/aws-mcp-setup
source_repo: zxkane/aws-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/zxkane/aws-skills/blob/main/LICENSE
---

# AWS MCP 服务器配置指南
## 何时使用

当需要为文档搜索和 API 访问配置 AWS MCP 服务器时使用此技能。在设置 AWS MCP、配置 AWS 文档工具、排除 MCP 连接问题，或当用户提及 aws-mcp、awsdocs、uvx 设置或 MCP 服务器配置时使用。涵盖完整 AWS MCP 服务器（包含...）和 AWS 文档 MCP 服务器。

## 概述

本指南帮助您为 AI 代理配置 AWS MCP 工具。有两个选项可用：

| 选项 | 要求 | 功能 |
|--------|--------------|--------------|
| **完整 AWS MCP 服务器** | Python 3.10+、uvx、AWS 凭据 | 执行 AWS API 调用 + 文档搜索 |
| **AWS 文档 MCP** | 无 | 仅文档搜索 |

## 步骤 1：检查现有配置

在配置前，使用任一方法检查 AWS MCP 工具是否已可用：

### 方法 A：检查可用工具（推荐）

在您的代理可用工具中查找这些工具名称模式：
- `mcp__aws-mcp__*` 或 `mcp__aws__*` → 配置了完整 AWS MCP 服务器
- `mcp__*awsdocs*__aws___*` → 配置了 AWS 文档 MCP

**如何检查**：运行 `/mcp` 命令列出所有活跃的 MCP 服务器。

### 方法 B：检查配置文件

代理工具使用分层配置（优先级：本地 → 项目 → 用户 → 企业）：

| 范围 | 文件位置 | 用例 |
|-------|---------------|----------|
| 本地 | `.claude.json`（在项目中） | 个人/试验性 |
| 项目 | `.mcp.json`（项目根目录） | 团队共享 |
| 用户 | `~/.claude.json` | 跨项目个人 |
| 企业 | 系统管理的目录 | 组织范围 |

检查这些文件中的 `mcpServers`，包含 `aws-mcp`、`aws` 或 `awsdocs` 密钥：

```bash
# 检查项目配置
cat .mcp.json 2>/dev/null | grep -E '"(aws-mcp|aws|awsdocs)"'

# 检查用户配置
cat ~/.claude.json 2>/dev/null | grep -E '"(aws-mcp|aws|awsdocs)"'

# 或使用 Claude CLI
claude mcp list
```

如果 AWS MCP 已配置，无需进一步设置。

## 步骤 2：选择配置方法

### 自动检测

运行这些命令来确定要使用的选项：

```bash
# 检查 uvx（需要 Python 3.10+）
which uvx || echo "uvx not available"

# 检查有效的 AWS 凭据
aws sts get-caller-identity || echo "AWS credentials not configured"
```

### 选项 A：完整 AWS MCP 服务器（推荐）

**何时使用**：uvx 可用且 AWS 凭据有效

**前置条件**:
- Python 3.10+ 和 `uv` 软件包管理器
- AWS 凭据已配置（通过配置文件、环境变量或 IAM 角色）

**必需的 IAM 权限**:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "aws-mcp:InvokeMCP",
      "aws-mcp:CallReadOnlyTool",
      "aws-mcp:CallReadWriteTool"
    ],
    "Resource": "*"
  }]
}
```

**配置**（添加到您的 MCP 设置）：
```json
{
  "mcpServers": {
    "aws-mcp": {
      "command": "uvx",
      "args": [
        "mcp-proxy-for-aws@latest",
        "https://aws-mcp.us-east-1.api.aws/mcp",
        "--metadata", "AWS_REGION=us-west-2"
      ]
    }
  }
}
```

**凭据配置选项**:

1. **AWS 配置文件**（推荐用于开发）：
   ```json
   "args": [
     "mcp-proxy-for-aws@latest",
     "https://aws-mcp.us-east-1.api.aws/mcp",
     "--profile", "my-profile",
     "--metadata", "AWS_REGION=us-west-2"
   ]
   ```

2. **环境变量**:
   ```json
   "env": {
     "AWS_ACCESS_KEY_ID": "...",
     "AWS_SECRET_ACCESS_KEY": "...",
     "AWS_REGION": "us-west-2"
   }
   ```

3. **IAM 角色**（用于 EC2/ECS/Lambda）：无需其他配置 - 使用实例凭据

**其他选项**:
- `--region <region>`：覆盖 AWS 区域
- `--read-only`：限制为只读工具
- `--log-level <level>`：设置日志级别（debug、info、warning、error）

**参考**：https://github.com/aws/mcp-proxy-for-aws

### 选项 B：AWS 文档 MCP 服务器（无认证）

**何时使用**:
- 没有 Python/uvx 环境
- 没有 AWS 凭据
- 仅需文档搜索（无 API 执行）

**配置**:
```json
{
  "mcpServers": {
    "awsdocs": {
      "type": "http",
      "url": "https://knowledge-mcp.global.api.aws"
    }
  }
}
```

## 步骤 3：验证

配置后，验证工具是否可用：

**对于完整 AWS MCP**:
- 查找工具：`mcp__aws-mcp__aws___search_documentation`、`mcp__aws-mcp__aws___call_aws`

**对于文档 MCP**:
- 查找工具：`mcp__awsdocs__aws___search_documentation`、`mcp__awsdocs__aws___read_documentation`

## 故障排除

| 问题 | 原因 | 解决方案 |
|-------|-------|----------|
| `uvx: command not found` | 未安装 uv | 使用 `pip install uv` 安装或使用选项 B |
| `AccessDenied` 错误 | 缺少 IAM 权限 | 在 IAM 策略中添加 aws-mcp:* 权限 |
| `InvalidSignatureException` | 凭据问题 | 检查 `aws sts get-caller-identity` |
| 工具未出现 | MCP 未启动 | 配置更改后重启您的代理 |

## 限制

- 仅当任务清楚地匹配其上游来源和本地项目背景时使用此技能。
- 在应用更改前验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例视为特定于环境的测试、安全审查或用户对破坏性或昂贵操作的批准的替代品。
