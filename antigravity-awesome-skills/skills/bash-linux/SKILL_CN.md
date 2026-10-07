---
name: bash-linux
description: Bash/Linux 终端模式。关键命令、管道、错误处理、脚本编写。在 macOS 或 Linux 系统上工作时使用。
risk: critical
source: community
date_added: "2026-02-27"
---

# Bash Linux 模式

> 用于 Linux/macOS 上 Bash 的基本模式。

---

## 1. 运算符语法

### 链接命令

| 运算符 | 含义 | 示例 |
|----------|---------|---------|
| `;` | 按顺序运行 | `cmd1; cmd2` |
| `&&` | 如果前一个成功则运行 | `npm install && npm run dev` |
| `\|\|` | 如果前一个失败则运行 | `npm test \|\| echo "Tests failed"` |
| `\|` | 管道输出 | `ls \| grep ".js"` |

---

## 2. 文件操作

### 基本命令

| 任务 | 命令 |
|------|---------|
| 列出所有文件 | `ls -la` |
| 查找文件 | `find . -name "*.js" -type f` |
| 文件内容 | `cat file.txt` |
| 前 N 行 | `head -n 20 file.txt` |
| 后 N 行 | `tail -n 20 file.txt` |
| 追踪日志 | `tail -f log.txt` |
| 搜索文件 | `grep -r "pattern" --include="*.js"` |
| 文件大小 | `du -sh *` |
| 磁盘使用 | `df -h` |

---

## 3. 进程管理

| 任务 | 命令 |
|------|---------|
| 列表进程 | `ps aux` |
| 按名称查找 | `ps aux \| grep node` |
| 按 PID 杀死 | `kill -9 <PID>` |
| 查找端口用户 | `lsof -i :3000` |
| 杀死端口 | `kill -9 $(lsof -t -i :3000)` |
| 后台运行 | `npm run dev &` |
| 任务列表 | `jobs -l` |
| 带到前景 | `fg %1` |

---

## 4. 文本处理

### 核心工具

| 工具 | 用途 | 示例 |
|------|---------|---------|
| `grep` | 搜索 | `grep -rn "TODO" src/` |
| `sed` | 替换 | `sed -i 's/old/new/g' file.txt` |
| `awk` | 提取列 | `awk '{print $1}' file.txt` |
| `cut` | 切割字段 | `cut -d',' -f1 data.csv` |
| `sort` | 排序行 | `sort -u file.txt` |
| `uniq` | 唯一行 | `sort file.txt \| uniq -c` |
| `wc` | 计数 | `wc -l file.txt` |

---

## 5. 环境变量

| 任务 | 命令 |
|------|---------|
| 查看所有 | `env` 或 `printenv` |
| 查看一个 | `echo $PATH` |
| 临时设置 | `export VAR="value"` |
| 在脚本中设置 | `VAR="value" command` |
| 添加到 PATH | `export PATH="$PATH:/new/path"` |

---

## 6. 网络

| 任务 | 命令 |
|------|---------|
| 下载 | `curl -O https://example.com/file` |
| API 请求 | `curl -X GET https://api.example.com` |
| POST JSON | `curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' URL` |
| 检查端口 | `nc -zv localhost 3000` |
| 网络信息 | `ifconfig` 或 `ip addr` |

---

## 7. 脚本模板

```bash
#!/bin/bash
set -euo pipefail  # 在错误、未定义变量、管道失败时退出

# 颜色（可选）
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 函数
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# 主程序
main() {
    log_info "Starting..."
    # 您的逻辑在这里
    log_info "Done!"
}

main "$@"
```

---

## 8. 常见模式

### 检查命令是否存在

```bash
if command -v node &> /dev/null; then
    echo "Node is installed"
fi
```

### 默认变量值

```bash
NAME=${1:-"default_value"}
```

### 逐行读取文件

```bash
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

### 循环文件

```bash
for file in *.js; do
    echo "Processing $file"
done
```

---

## 9. 与 PowerShell 的区别

| 任务 | PowerShell | Bash |
|------|------------|------|
| 列出文件 | `Get-ChildItem` | `ls -la` |
| 查找文件 | `Get-ChildItem -Recurse` | `find . -type f` |
| 环境变量 | `$env:VAR` | `$VAR` |
| 字符串连接 | `"$a$b"` | `"$a$b"`（相同） |
| Null 检查 | `if ($x)` | `if [ -n "$x" ]` |
| 管道 | 对象类型 | 文本类型 |

---

## 10. 错误处理

### 设置选项

```bash
set -e          # 错误时退出
set -u          # 未定义变量时退出
set -o pipefail # 管道失败时退出
set -x          # 调试：打印命令
```

### 清理的陷阱

```bash
cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/tempfile
}
trap cleanup EXIT
```

---

> **记住：** Bash 基于文本。使用 `&&` 进行成功链、`set -e` 保证安全，以及引用您的变量！

## 何时使用

此技能适用于执行上述概述中描述的工作流或操作。

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出作为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
