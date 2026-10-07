---
name: ai-coding-agent-guardrails
description: 为团队环境中的 AI 编码代理（Claude Code、Cursor、Codex、Copilot）构建安全防护，包括权限边界、密钥保护、代码审查关卡和安全的沙箱配置。
category: security
risk: safe
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: Requires the relevant security tooling (scanners, vault CLIs) and an
  authorized scope for any active assessment. Docs-only; helper scripts and templates
  not bundled.
metadata:
  author: devops-skills
  version: '1.0'
---

# AI Coding Agent Guardrails

保护工程团队中 AI 编码代理的使用安全。本技能涵盖权限边界、密钥保护、沙箱隔离、代码审查关卡以及针对 Claude Code、Cursor、Copilot 和 Codex 的审计追踪。

---

## 权限边界

### CLAUDE.md 配置

在仓库根目录创建一个 `CLAUDE.md`，以限制 Claude Code 的行为：

```markdown
# CLAUDE.md

## 限制

- 绝不读取或输出 .env、.env.*、secrets.yaml 的内容，或任何匹配 *.pem、*.key 的文件
- 绝不执行 `rm -rf`、`DROP TABLE`、`kubectl delete` 或 `terraform destroy` 命令
- 绝不直接推送到 main 或 master 分支
- 未经用户明确批准，绝不修改 infrastructure/、terraform/ 或 .github/workflows/ 目录中的文件
- 未先列出清单供审查，绝不安装新的依赖
- 绝不访问或显示 API 密钥、令牌、密码或连接字符串

## 允许的操作

- 读取并修改 src/、lib/ 和 tests/ 中的应用程序源码
- 使用 `npm test`、`pytest`、`go test` 运行测试套件
- 使用 `eslint`、`ruff`、`golangci-lint` 运行代码检查工具
- 创建前缀为 `ai/` 或 `agent/` 的新分支
- 在 docs/ 目录中创建和修改文件

## 代码标准

- 所有新函数必须包含文档字符串（docstring）或 JSDoc 注释
- 所有新代码必须具有相应的单元测试
- 遵循仓库中现有的代码风格和模式
- 文件最大长度：500 行。超过时建议拆分。
```

### 命令白名单

对于会执行 shell 命令的代理，定义一份明确的白名单：

```yaml
# .agent-permissions.yaml
agent_permissions:
  allowed_commands:
    - "npm test"
    - "npm run lint"
    - "npm run build"
    - "pytest"
    - "ruff check"
    - "go test ./..."
    - "git status"
    - "git diff"
    - "git log"
    - "git checkout -b"
    - "git add"
    - "git commit"
    - "ls"
    - "cat"
    - "head"
    - "tail"

  blocked_commands:
    - "rm -rf"
    - "curl"
    - "wget"
    - "ssh"
    - "scp"
    - "kubectl"
    - "terraform"
    - "aws"
    - "gcloud"
    - "az"
    - "docker push"
    - "npm publish"

  blocked_paths:
    - ".env*"
    - "**/*.pem"
    - "**/*.key"
    - "**/secrets/**"
    - "infrastructure/**"
    - ".github/workflows/**"

  allowed_paths:
    - "src/**"
    - "lib/**"
    - "tests/**"
    - "docs/**"
    - "package.json"
    - "pyproject.toml"
```

### 文件系统访问控制

使用文件系统权限在操作系统层面强制实施边界：

```bash
#!/bin/bash
# setup-agent-workspace.sh
# 为代理执行创建受限工作区

AGENT_USER="ai-agent"
REPO_DIR="/workspace/repo"

# 创建权限受限的代理用户
useradd --system --shell /bin/bash --no-create-home "$AGENT_USER"

# 设置所有权：开发者拥有一切，代理在大多数内容上仅有读权限
chown -R root:developers "$REPO_DIR"
chmod -R 750 "$REPO_DIR"

# 仅向代理授予对安全目录的写权限
setfacl -R -m u:${AGENT_USER}:rwx "${REPO_DIR}/src"
setfacl -R -m u:${AGENT_USER}:rwx "${REPO_DIR}/tests"
setfacl -R -m u:${AGENT_USER}:rwx "${REPO_DIR}/docs"

# 拒绝代理访问敏感文件
setfacl -m u:${AGENT_USER}:--- "${REPO_DIR}/.env"
setfacl -R -m u:${AGENT_USER}:--- "${REPO_DIR}/infrastructure"
setfacl -R -m u:${AGENT_USER}:--- "${REPO_DIR}/.github/workflows"

echo "Agent workspace permissions configured."
```

---

## 密钥保护

### 使用 git-secrets 的 Pre-commit Hook

```bash
#!/bin/bash
# install-secret-scanning.sh

# 安装 git-secrets
git clone https://github.com/awslabs/git-secrets.git /tmp/git-secrets
cd /tmp/git-secrets && make install

# 在仓库中初始化
cd /path/to/repo
git secrets --install

# 注册常见的密钥模式
git secrets --register-aws

# 为常见凭证格式添加自定义模式
git secrets --add '-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----'
git secrets --add 'AKIA[0-9A-Z]{16}'
git secrets --add 'ghp_[a-zA-Z0-9]{36}'
git secrets --add 'sk-[a-zA-Z0-9]{48}'
git secrets --add 'xox[baprs]-[0-9a-zA-Z-]{10,}'
git secrets --add 'password\s*[:=]\s*["\x27][^\s]{8,}'
git secrets --add 'api[_-]?key\s*[:=]\s*["\x27][^\s]{8,}'

# 添加允许的模式（排除误报）
git secrets --add --allowed 'EXAMPLE_KEY'
git secrets --add --allowed 'your-api-key-here'
```

### 代理输出扫描

在代理生成的输出进入版本控制之前对其进行扫描：

```python
#!/usr/bin/env python3
"""scan_agent_output.py - 扫描 AI 代理输出中泄露的密钥。"""

import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'(?i)aws_secret_access_key\s*[:=]\s*\S+', 'AWS Secret Key'),
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
    (r'gho_[a-zA-Z0-9]{36}', 'GitHub OAuth Token'),
    (r'sk-[a-zA-Z0-9]{48,}', 'OpenAI/Anthropic API Key'),
    (r'xox[baprs]-[0-9a-zA-Z\-]{10,}', 'Slack Token'),
    (r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----', 'Private Key'),
    (r'(?i)(password|passwd|pwd)\s*[:=]\s*["\x27][^\s]{4,}', 'Hardcoded Password'),
    (r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\x27][^\s]{8,}', 'API Key'),
    (r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}', 'JWT Token'),
    (r'(?i)database_url\s*[:=]\s*\S+', 'Database Connection String'),
]


def scan_file(filepath: str) -> list[dict]:
    findings = []
    content = Path(filepath).read_text(errors="ignore")
    for line_num, line in enumerate(content.splitlines(), 1):
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, line):
                findings.append({
                    "file": filepath,
                    "line": line_num,
                    "type": label,
                    "content": line.strip()[:120],
                })
    return findings


def main():
    files = sys.argv[1:]
    if not files:
        print("Usage: scan_agent_output.py <file1> [file2] ...")
        sys.exit(1)

    all_findings = []
    for f in files:
        all_findings.extend(scan_file(f))

    if all_findings:
        print(f"BLOCKED: {len(all_findings)} potential secret(s) detected:\n")
        for finding in all_findings:
            print(f"  [{finding['type']}] {finding['file']}:{finding['line']}")
            print(f"    {finding['content']}\n")
        sys.exit(1)

    print("OK: No secrets detected in agent output.")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

### Git Pre-commit Hook 集成

```bash
#!/bin/bash
# .git/hooks/pre-commit
# 阻止包含来自 AI 代理密钥的提交

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

echo "Scanning staged files for secrets..."

# 运行 git-secrets
git secrets --pre_commit_hook -- "$@"
GIT_SECRETS_EXIT=$?

# 对已暂存的文件运行自定义扫描器
python3 .tools/scan_agent_output.py $STAGED_FILES
SCANNER_EXIT=$?

if [ $GIT_SECRETS_EXIT -ne 0 ] || [ $SCANNER_EXIT -ne 0 ]; then
  echo ""
  echo "COMMIT BLOCKED: Secrets detected in staged files."
  echo "If this is a false positive, use: git commit"
  exit 1
fi
```

---

## 沙箱配置

### 用于代理执行的 Docker 沙箱

```dockerfile
# Dockerfile.agent-sandbox
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    git \
    nodejs \
    npm \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 的代理用户
RUN useradd -m -s /bin/bash agent && \
    mkdir -p /workspace && \
    chown agent:agent /workspace

# 降低权限能力
USER agent
WORKDIR /workspace

# 默认无网络——如需要可在运行时覆盖
# 无法访问 Docker socket
# 除挂载的卷之外，无法访问主机文件系统
```

```bash
#!/bin/bash
# run-agent-sandbox.sh
# 在一个锁定的容器内启动 AI 编码代理

REPO_DIR="$(pwd)"
CONTAINER_NAME="agent-sandbox-$$"

docker run \
  --name "$CONTAINER_NAME" \
  --rm \
  --network none \
  --read-only \
  --tmpfs /tmp:size=512m \
  --tmpfs /home/agent:size=256m \
  --memory 4g \
  --cpus 2 \
  --pids-limit 256 \
  --security-opt no-new-privileges:true \
  --security-opt seccomp=seccomp-agent.json \
  --cap-drop ALL \
  --cap-add DAC_OVERRIDE \
  -v "${REPO_DIR}/src:/workspace/src" \
  -v "${REPO_DIR}/tests:/workspace/tests:rw" \
  -v "${REPO_DIR}/docs:/workspace/docs:rw" \
  -v "${REPO_DIR}/package.json:/workspace/package.json:ro" \
  -e "NO_COLOR=1" \
  agent-sandbox:latest \
  "$@"
```

### 代理容器的 Seccomp 配置文件

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "comment": "seccomp-agent.json - Restrictive profile for AI coding agents",
  "syscalls": [
    {
      "names": [
        "read", "write", "open", "close", "stat", "fstat", "lstat",
        "poll", "lseek", "mmap", "mprotect", "munmap", "brk",
        "access", "pipe", "select", "sched_yield", "mremap",
        "dup", "dup2", "nanosleep", "getpid", "getuid", "getgid",
        "geteuid", "getegid", "getppid", "getpgrp", "setsid",
        "getgroups", "uname", "fcntl", "flock", "fsync",
        "getcwd", "chdir", "readlink", "chmod", "mkdir",
        "rmdir", "unlink", "rename", "symlink", "readlinkat",
        "openat", "mkdirat", "newfstatat", "unlinkat", "renameat",
        "faccessat", "pselect6", "ppoll", "set_robust_list",
        "get_robust_list", "epoll_create1", "epoll_ctl", "epoll_wait",
        "eventfd2", "pipe2", "dup3", "pread64", "pwrite64",
        "futex", "clock_gettime", "clock_getres", "exit_group",
        "wait4", "clone", "execve", "arch_prctl", "set_tid_address",
        "exit", "getdents64", "rt_sigaction", "rt_sigprocmask",
        "rt_sigreturn", "ioctl", "writev", "madvise", "getrandom"
      ],
      "action": "SCMP_ACT_ALLOW"
    },
    {
      "names": [
        "socket", "connect", "bind", "listen", "accept",
        "sendto", "recvfrom", "sendmsg", "recvmsg"
      ],
      "action": "SCMP_ACT_ERRNO",
      "comment": "Block all network syscalls"
    },
    {
      "names": ["ptrace", "process_vm_readv", "process_vm_writev"],
      "action": "SCMP_ACT_ERRNO",
      "comment": "Block debugging and process inspection"
    }
  ]
}
```

---


## 目录

- [代码审查关卡](references/details.md)
- [仓库配置](references/details.md)
- [安全规则](references/details.md)
- [文件限制](references/details.md)
- [代码质量](references/details.md)
- [Git 行为](references/details.md)
- [规则](references/details.md)
- [网络控制](references/details.md)
- [审计追踪](references/details.md)
- [团队策略](references/details.md)
- [测试代理输出](references/details.md)
- [快速参考](references/details.md)

## 何时使用

在以下情况下应用这些防护措施：

- 首次将 AI 编码代理引入工程团队
- 开发者正在使用 Claude Code、Cursor、Copilot 或 Codex 生成生产代码
- 代理可以访问包含密钥、基础设施配置或敏感业务逻辑的仓库
- 你的合规框架（SOC 2、ISO 27001、FedRAMP）要求对自动代码生成实施控制
- 自主或半自主代理在未经人工直接打字的情况下创建 Pull Request
- 你需要在多个代理和团队成员之间强制实施一致的安全策略

需要收紧防护措施的迹象：

- 代理已将密钥或凭证提交到版本控制中
- 代理生成的代码引入了直到管道后期才被发现的漏洞
- 没有清晰的审计追踪区分人工编写的代码和 AI 生成的代码
- 开发者在为"简单的"代理改动绕过代码审查
- 代理在与生产环境相连的环境中执行任意 shell 命令

---

## 局限性

- 仅在已获授权的范围内应用本指南；对破坏性步骤先在非生产环境中测试。
- 仅为文档导入：未附带上游脚本和模板。

### 示例

```bash
# 先只读：在执行任何主动操作之前先清点现状。
which <tool> && <tool> --help | head -n 20
```

> 改编自 [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills)（MIT 许可）；为符合上游合规性要求，新增了 frontmatter、"何时使用/局限性"以及安全边界部分。仅为文档导入：未附带辅助脚本和模板。
</content>
