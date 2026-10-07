---
name: ai-agent-security
description: 通过纵深防御控制措施，保护 AI 代理免受提示注入、工具滥用和数据泄露的侵害。
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
  version: '2.0'
---

# AI Agent Security

使用分层安全控制措施，保护代理式 AI 系统免受对抗性输入、不安全工具执行、数据泄露和权限滥用的侵害。

## 前提条件

- Python 3.10+ 用于护栏代码示例
- Docker 或 Podman 用于沙箱执行
- OpenTelemetry collector 用于审计日志
- 熟悉你的代理框架（LangChain、CrewAI、Autogen、自定义框架）
- 访问策略引擎（OPA/Cedar）以设置权限边界

## 威胁模型 —— 针对 AI 代理的 STRIDE

AI 代理引入了独特的威胁面。将 STRIDE 专门应用于代理式组件：

| 威胁 | 代理特定示例 | 控制措施 |
|--------|----------------------|---------|
| **仿冒（Spoofing）** | 攻击者构造模仿可信内部工具响应的输入 | 签名工具响应、HMAC 验证 |
| **篡改（Tampering）** | 提示注入在推理链中修改代理的推理过程 | 输入验证、提示加固 |
| **否认（Repudiation）** | 代理执行破坏性操作却没有留下审计记录 | 不可篡改的结构化日志 |
| **信息泄露（Information Disclosure）** | 代理在响应中泄露 PII、密钥或内部架构信息 | 输出过滤、内容分类器 |
| **拒绝服务（Denial of Service）** | 对抗性提示导致无限的工具循环或 token 耗尽 | 速率限制、token 预算、断路器 |
| **提权（Elevation of Privilege）** | 代理通过链式工具调用从只读升级到可写 | 按工具的 RBAC、最小权限范围 |

### 关键威胁类别

**提示注入（Prompt Injection）** —— 不受信任的内容（用户输入、网页抓取内容、文档内容）操纵代理的系统提示或推理链，使其执行非预期的操作。

**工具滥用（Tool Abuse）** —— 代理以设计者未曾预料到的顺序或参数调用工具，实现超出其预期范围的效果。

**数据泄露（Data Exfiltration）** —— 代理将敏感数据（凭证、PII、内部 IP）编码进其响应、工具调用或出站 HTTP 请求中。

**跨租户泄露（Cross-Tenant Leakage）** —— 在多租户部署中，某个租户会话的上下文通过共享内存、向量存储或缓存泄漏到另一个租户。

**权限提升（Privilege Escalation）** —— 代理将多个低权限工具调用串联起来，以实现高权限结果（例如：读取配置 -> 提取凭证 -> 调用管理员 API）。

## 输入验证

每一个传给代理的输入都必须在到达模型或任何工具之前经过清洗。这包括用户消息、被反馈回去的工具输出、以及检索到的文档。

### 提示注入检测

```python
import re
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ValidationResult:
    is_safe: bool
    risk_level: RiskLevel
    matched_rules: list[str]
    sanitized_input: str

INJECTION_PATTERNS = [
    (r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|rules)", "instruction_override"),
    (r"you\s+are\s+now\s+(a|an|the)\s+", "role_hijack"),
    (r"system\s*:\s*", "system_prompt_inject"),
    (r"<\|?(system|im_start|endoftext)\|?>", "control_token_inject"),
    (r"\[INST\]|\[\/INST\]|<<SYS>>", "template_inject"),
    (r"(?:execute|run|eval)\s*\(", "code_execution_attempt"),
    (r"(?:curl|wget|nc|ncat)\s+", "network_command_inject"),
    (r"(?:rm\s+-rf|mkfs|dd\s+if=|chmod\s+777)", "destructive_command"),
    (r"(?:\/etc\/passwd|\/etc\/shadow|\.env\b|\.ssh\/)", "path_traversal"),
    (r"(?:BEGIN\s+(?:RSA|DSA|EC)\s+PRIVATE\s+KEY)", "secret_exfil_attempt"),
]

def validate_agent_input(user_input: str, max_length: int = 4096) -> ValidationResult:
    """在传给代理之前验证并清洗输入。"""
    matched = []
    risk = RiskLevel.LOW

    # 长度检查
    if len(user_input) > max_length:
        matched.append("input_too_long")
        risk = RiskLevel.MEDIUM

    # 移除空字节和控制字符
    sanitized = user_input.replace("\x00", "")
    sanitized = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f]", "", sanitized)

    # 模式匹配
    for pattern, rule_name in INJECTION_PATTERNS:
        if re.search(pattern, sanitized, re.IGNORECASE):
            matched.append(rule_name)
            risk = RiskLevel.HIGH

    # 叠加注入检测（多个可疑模式）
    if len(matched) >= 3:
        risk = RiskLevel.CRITICAL

    is_safe = risk in (RiskLevel.LOW, RiskLevel.MEDIUM)

    return ValidationResult(
        is_safe=is_safe,
        risk_level=risk,
        matched_rules=matched,
        sanitized_input=sanitized[:max_length] if is_safe else "",
    )
```

### 内容分类中间件

在代理处理任何输入之前，使用轻量级分类器作为中间件：

```python
from functools import wraps
from typing import Callable

def input_guard(validator: Callable = validate_agent_input):
    """用于保护代理入口点免受不安全输入侵害的装饰器。"""
    def decorator(func):
        @wraps(func)
        async def wrapper(user_input: str, *args, **kwargs):
            result = validator(user_input)

            if result.risk_level == RiskLevel.CRITICAL:
                await log_security_event(
                    event="input_blocked",
                    risk=result.risk_level.value,
                    rules=result.matched_rules,
                    input_hash=hashlib.sha256(user_input.encode()).hexdigest(),
                )
                raise InputRejectedError(
                    f"Input blocked: matched {result.matched_rules}"
                )

            if result.risk_level == RiskLevel.HIGH:
                await log_security_event(
                    event="input_flagged",
                    risk=result.risk_level.value,
                    rules=result.matched_rules,
                )
                # 允许通过但标记以供审查
                kwargs["_security_flags"] = result.matched_rules

            return await func(result.sanitized_input, *args, **kwargs)
        return wrapper
    return decorator

# 用法
@input_guard()
async def handle_user_message(message: str, session_id: str, **kwargs):
    """通过代理处理一条经过验证的用户消息。"""
    flags = kwargs.get("_security_flags", [])
    if flags:
        # 路由到沙箱化执行路径
        return await agent.run_sandboxed(message, session_id)
    return await agent.run(message, session_id)
```

## 工具执行沙箱化

绝不要让代理直接在主机上执行工具。将每一次工具调用都隔离在沙箱中。

### Docker 沙箱配置

```yaml
# docker-compose.agent-sandbox.yml
version: "3.8"

services:
  agent-sandbox:
    image: agent-tools:latest
    read_only: true
    security_opt:
      - no-new-privileges:true
      - seccomp:seccomp-profile.json
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE   # 仅当工具需要网络时才添加
    tmpfs:
      - /tmp:size=64M,noexec,nosuid
    mem_limit: 512m
    cpus: "0.5"
    pids_limit: 64
    networks:
      - sandbox-net
    environment:
      - TOOL_TIMEOUT=30
      - MAX_OUTPUT_BYTES=65536
    volumes:
      - type: bind
        source: ./tool-workspace
        target: /workspace
        read_only: false
    dns:
      - 127.0.0.1           # 默认阻止外部 DNS

networks:
  sandbox-net:
    driver: bridge
    internal: true           # 无外部网络访问
```

### 使用 gVisor 运行时实现更强隔离

```bash
# 安装 gVisor runsc 运行时
curl -fsSL https://gvisor.dev/archive.key | sudo gpg --dearmor -o /usr/share/keyrings/gvisor-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/gvisor-archive-keyring.gpg] https://storage.googleapis.com/gvisor/releases release main" | \
  sudo tee /etc/apt/sources.list.d/gvisor.list
sudo apt-get update && sudo apt-get install -y runsc

# 配置 Docker 使用 gVisor
cat <<'EOF' | sudo tee /etc/docker/daemon.json
{
  "runtimes": {
    "runsc": {
      "path": "/usr/bin/runsc",
      "runtimeArgs": [
        "--network=none",
        "--directfs=false"
      ]
    }
  }
}
EOF
sudo systemctl restart docker

# 使用 gVisor 运行代理沙箱
docker run --runtime=runsc --rm \
  --read-only \
  --memory=512m \
  --cpus=0.5 \
  --pids-limit=64 \
  agent-tools:latest \
  python /tools/execute.py --tool="$TOOL_NAME" --args="$TOOL_ARGS"
```

### 工具白名单强制实施

```python
from dataclasses import dataclass, field

@dataclass
class ToolPolicy:
    name: str
    allowed_args: dict[str, type]     # 参数名 -> 期望类型
    max_calls_per_session: int = 10
    requires_approval: bool = False
    allowed_patterns: list[str] = field(default_factory=list)
    blocked_patterns: list[str] = field(default_factory=list)

TOOL_ALLOWLIST: dict[str, ToolPolicy] = {
    "read_file": ToolPolicy(
        name="read_file",
        allowed_args={"path": str},
        max_calls_per_session=20,
        allowed_patterns=[r"^/workspace/", r"^/data/public/"],
        blocked_patterns=[r"\.env$", r"\.key$", r"\.pem$", r"/etc/", r"/proc/"],
    ),
    "run_query": ToolPolicy(
        name="run_query",
        allowed_args={"sql": str, "database": str},
        max_calls_per_session=5,
        allowed_patterns=[r"^SELECT\s", r"^EXPLAIN\s"],
        blocked_patterns=[r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bINSERT\b", r"\bALTER\b"],
    ),
    "http_request": ToolPolicy(
        name="http_request",
        allowed_args={"url": str, "method": str},
        max_calls_per_session=10,
        requires_approval=True,
        allowed_patterns=[r"^https://api\.internal\."],
        blocked_patterns=[r"^https?://169\.254\.", r"^https?://metadata\.google\."],
    ),
    "execute_code": ToolPolicy(
        name="execute_code",
        allowed_args={"code": str, "language": str},
        max_calls_per_session=3,
        requires_approval=True,
        blocked_patterns=[r"import\s+subprocess", r"import\s+os", r"__import__", r"eval\(", r"exec\("],
    ),
}

class ToolGatekeeper:
    def __init__(self, allowlist: dict[str, ToolPolicy]):
        self.allowlist = allowlist
        self.call_counts: dict[str, int] = {}

    async def authorize(self, tool_name: str, args: dict) -> bool:
        if tool_name not in self.allowlist:
            await log_security_event(
                event="tool_denied_not_in_allowlist",
                tool=tool_name,
            )
            return False

        policy = self.allowlist[tool_name]

        # 检查调用计数
        count = self.call_counts.get(tool_name, 0)
        if count >= policy.max_calls_per_session:
            await log_security_event(
                event="tool_denied_rate_limit",
                tool=tool_name,
                count=count,
            )
            return False

        # 验证参数类型
        for arg_name, expected_type in policy.allowed_args.items():
            if arg_name in args and not isinstance(args[arg_name], expected_type):
                return False

        # 对所有字符串参数检查模式
        for arg_value in args.values():
            if not isinstance(arg_value, str):
                continue
            # 必须至少匹配一个允许的模式（如果有定义的话）
            if policy.allowed_patterns:
                if not any(re.search(p, arg_value, re.IGNORECASE) for p in policy.allowed_patterns):
                    return False
            # 不得匹配任何被阻止的模式
            if any(re.search(p, arg_value, re.IGNORECASE) for p in policy.blocked_patterns):
                await log_security_event(
                    event="tool_denied_blocked_pattern",
                    tool=tool_name,
                    arg_value_hash=hashlib.sha256(arg_value.encode()).hexdigest(),
                )
                return False

        self.call_counts[tool_name] = count + 1
        return True
```


## 目录

- [权限边界](references/details.md)
- [输出过滤](references/details.md)
- [审计日志](references/details.md)
- [速率限制与滥用防范](references/details.md)
- [终止开关与断路器](references/details.md)
- [红队检查清单](references/details.md)
- [事件响应手册](references/details.md)
- [故障排查](references/details.md)
- [最佳实践](references/details.md)
- [相关技能](references/details.md)

## 何时使用此技能

在以下情况下使用此技能：
- 构建会调用工具、API 或 shell 命令的 AI 代理
- 部署可访问生产数据库、云账户或内部服务的代理
- 加固多租户代理平台，防范跨租户数据泄露
- 为自主编码代理或 SRE 机器人添加护栏
- 为高风险代理操作设计审批流程
- 对代理式系统进行红队演练
- 响应涉及被攻陷或行为异常代理的事件

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
