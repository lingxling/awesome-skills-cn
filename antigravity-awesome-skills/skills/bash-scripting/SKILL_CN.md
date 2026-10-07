---
name: bash-scripting
description: 用于创建具有防御模式、错误处理和测试的生产就绪 shell 脚本的 Bash 脚本编写工作流。
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Bash 脚本编写工作流

## 概述

专业工作流，用于创建具有防御性编程模式、全面错误处理和自动化测试的健壮、生产就绪 Bash 脚本。

## 何时使用此工作流

在以下情况下使用此工作流：
- 创建自动化脚本
- 编写系统管理工具
- 构建部署脚本
- 开发备份解决方案
- 创建 CI/CD 脚本

## 工作流阶段

### 阶段 1：脚本设计

#### 调用的技能
- `bash-pro` - 专业脚本编写
- `bash-defensive-patterns` - 防御模式

#### 行动
1. 定义脚本目的
2. 识别输入/输出
3. 规划错误处理
4. 设计日志记录策略
5. 记录要求

#### 复制粘贴提示
```
使用 @bash-pro 设计生产就绪的 Bash 脚本
```

### 阶段 2：脚本结构

#### 调用的技能
- `bash-pro` - 脚本结构
- `bash-defensive-patterns` - 安全模式

#### 行动
1. 添加 shebang 和严格模式
2. 创建使用函数
3. 实现参数解析
4. 设置日志记录
5. 添加清理处理程序

#### 复制粘贴提示
```
使用 @bash-defensive-patterns 实现严格模式和错误处理
```

### 阶段 3：核心实现

#### 调用的技能
- `bash-linux` - Linux 命令
- `linux-shell-scripting` - Shell 脚本编写

#### 行动
1. 实现主要函数
2. 添加输入验证
3. 创建辅助函数
4. 处理边界情况
5. 添加进度指示

#### 复制粘贴提示
```
使用 @bash-linux 实现系统命令
```

### 阶段 4：错误处理

#### 调用的技能
- `bash-defensive-patterns` - 错误处理
- `error-handling-patterns` - 错误模式

#### 行动
1. 添加陷阱处理程序
2. 实现重试逻辑
3. 创建错误消息
4. 设置退出代码
5. 添加回滚功能

#### 复制粘贴提示
```
使用 @bash-defensive-patterns 添加全面的错误处理
```

### 阶段 5：日志记录

#### 调用的技能
- `bash-pro` - 日志记录模式

#### 行动
1. 创建日志记录函数
2. 添加日志级别
3. 实现时间戳
4. 配置日志轮转
5. 添加调试模式

#### 复制粘贴提示
```
使用 @bash-pro 实现结构化日志记录
```

### 阶段 6：测试

#### 调用的技能
- `bats-testing-patterns` - Bats 测试
- `shellcheck-configuration` - ShellCheck

#### 行动
1. 编写 Bats 测试
2. 运行 ShellCheck
3. 测试边界情况
4. 验证错误处理
5. 测试不同输入

#### 复制粘贴提示
```
使用 @bats-testing-patterns 编写脚本测试
```

```
使用 @shellcheck-configuration lint Bash 脚本
```

### 阶段 7：文档

#### 调用的技能
- `documentation-templates` - 文档

#### 行动
1. 添加脚本标头
2. 文档函数
3. 创建使用示例
4. 列表依赖项
5. 添加故障排除部分

#### 复制粘贴提示
```
使用 @documentation-templates 记录 Bash 脚本
```

## 脚本模板

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
error() { log "ERROR: $*" >&2; exit 1; }

usage() { cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]
Options:
    -h, --help      显示帮助
    -v, --verbose   详细输出
EOF
}

main() {
    log "Script started"
    # 实现
    log "Script completed"
}

main "$@"
```

## 质量检查点

- [ ] ShellCheck 通过
- [ ] Bats 测试通过
- [ ] 错误处理正常工作
- [ ] 日志记录可工作
- [ ] 文档完整

## 相关工作流包

- `os-scripting` - 操作系统脚本编写
- `linux-troubleshooting` - Linux 故障排除
- `cloud-devops` - DevOps 自动化

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出作为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
