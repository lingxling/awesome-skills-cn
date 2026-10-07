---
name: ai-security-hardening
description: 加固 AI/LLM 部署,抵御提示注入、数据泄露、模型盗取和供应链攻击。
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

# AI 安全加固

在生产环境中保护 LLM 和 AI 系统,抵御提示注入、越狱、数据泄露和供应链威胁。

## 何时使用此技能

在以下场景使用此技能:
- 部署处理敏感用户数据的 LLM 驱动应用
- 保护 AI Agent 免受提示注入攻击
- 实施输出过滤和内容审核
- 保护模型权重和 API 端点以防被盗取
- 为 AI 系统达成 SOC2 或 ISO 27001 合规要求

## AI 专属威胁模型

```
Threat                    Risk                          Control
─────────────────────────────────────────────────────────────────────
Prompt injection          System prompt override         Input sanitization, separate context
Data exfiltration         PII in model outputs           Output filtering, DLP scanning
Jailbreaking             Policy bypass                  Content moderation, guardrails
Model theft               Weight extraction via API      Rate limiting, access controls
Training data poisoning   Backdoored fine-tuned model    Dataset validation, provenance
Supply chain attack       Malicious model weights        Signature verification, scanning
Insecure output           XSS/SQLi from LLM response     Output encoding, parameterized queries
```

## 提示注入防御

```python
import re
from typing import Optional

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"you\s+are\s+now\s+",
    r"new\s+instructions?:",
    r"system\s+prompt",
    r"forget\s+everything",
    r"act\s+as\s+",
    r"jailbreak",
    r"dan\s+mode",
    r"<\s*system\s*>",
    r"\[INST\]",
]

def detect_prompt_injection(user_input: str) -> tuple[bool, Optional[str]]:
    """Return (is_suspicious, matched_pattern)."""
    normalized = user_input.lower().strip()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return True, pattern
    return False, None

def sanitize_user_input(user_input: str, max_length: int = 4000) -> str:
    """Sanitize input before passing to LLM."""
    # Truncate
    user_input = user_input[:max_length]

    # Remove null bytes and control characters
    user_input = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', user_input)

    # Check for injection
    suspicious, pattern = detect_prompt_injection(user_input)
    if suspicious:
        raise ValueError(f"Potential prompt injection detected: {pattern}")

    return user_input
```

## 使用 NeMo Guardrails 实现护栏

```python
# guardrails.yaml
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("./guardrails-config")
rails = LLMRails(config)

async def safe_llm_call(user_message: str) -> str:
    response = await rails.generate_async(
        messages=[{"role": "user", "content": user_message}]
    )
    return response["content"]
```

```yaml
# guardrails-config/config.yml
models:
  - type: main
    engine: openai
    model: gpt-4o-mini

rails:
  input:
    flows:
      - check jailbreak
      - check sensitive data
  output:
    flows:
      - check output for PII
      - check output for harmful content
```

## 输出过滤与 PII 清洗

```python
import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

PII_ENTITIES = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD",
                "US_SSN", "IBAN_CODE", "IP_ADDRESS", "LOCATION"]

def scrub_pii_from_output(text: str) -> str:
    """Remove PII from LLM output before returning to user."""
    results = analyzer.analyze(text=text, entities=PII_ENTITIES, language="en")
    if not results:
        return text
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized.text

def validate_output_safety(output: str) -> bool:
    """Check output doesn't contain prompt injection artifacts."""
    dangerous_patterns = [
        r"<\s*script\s*>",         # XSS
        r"javascript:",             # XSS
        r";\s*(DROP|DELETE|INSERT)",# SQLi
        r"\$\{.*\}",               # template injection
        r"`.*`",                   # command injection in some contexts
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, output, re.IGNORECASE):
            return False
    return True
```

## LLM 端点的 API 安全

```python
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import time
from collections import defaultdict

app = FastAPI()
security = HTTPBearer()

# Rate limiting (per API key)
request_counts = defaultdict(list)

def rate_limit(api_key: str, max_requests: int = 100, window_seconds: int = 60):
    now = time.time()
    requests = request_counts[api_key]
    # Remove old requests outside window
    request_counts[api_key] = [t for t in requests if now - t < window_seconds]
    if len(request_counts[api_key]) >= max_requests:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    request_counts[api_key].append(now)

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        rate_limit(payload["sub"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/v1/chat/completions")
async def chat(request: Request, token: dict = Depends(verify_token)):
    body = await request.json()

    # Input validation
    user_msg = body.get("messages", [{}])[-1].get("content", "")
    try:
        safe_input = sanitize_user_input(user_msg)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Call LLM and scrub output
    response = await call_llm(safe_input, token["scope"])
    response["choices"][0]["message"]["content"] = scrub_pii_from_output(
        response["choices"][0]["message"]["content"]
    )
    return response
```

## 模型权重安全

```bash
# Verify model weights with SHA-256 hash before loading
MODEL_DIR="./models/llama-3.1-8b"
EXPECTED_HASH="sha256:abc123..."

# Generate hash of downloaded model
actual_hash=$(find "$MODEL_DIR" -name "*.safetensors" | sort | xargs sha256sum | sha256sum)
echo "Model hash: $actual_hash"

# Compare (automate in CI/CD)
if [ "$actual_hash" != "$EXPECTED_HASH" ]; then
  echo "ERROR: Model hash mismatch — possible tampering!"
  exit 1
fi

# Scan model files for embedded malware (ModelScan)
pip install modelscan
modelscan scan -p "$MODEL_DIR"
```

## AI 服务的网络隔离

```yaml
# Kubernetes NetworkPolicy — isolate LLM API
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: llm-api-isolation
  namespace: ai-services
spec:
  podSelector:
    matchLabels:
      app: vllm
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: backend           # only backend can call LLM
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: monitoring        # metrics only
    ports:
    - protocol: TCP
      port: 9090
  # Block egress to internet — prevent data exfiltration
  # (allow only internal cluster traffic)
```

## 审计日志

```python
import structlog
from datetime import datetime, timezone

audit_log = structlog.get_logger("ai.audit")

def log_llm_interaction(
    user_id: str,
    session_id: str,
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    was_filtered: bool,
    injection_detected: bool,
):
    audit_log.info(
        "llm_interaction",
        timestamp=datetime.now(timezone.utc).isoformat(),
        user_id=user_id,
        session_id=session_id,
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        was_filtered=was_filtered,
        injection_detected=injection_detected,
        # DO NOT log prompt/completion content — PII risk
    )
```

## 常见问题

| 问题 | 原因 | 修复方法 |
|-------|-------|-----|
| 注入检测误报过多 | 正则表达式过于宽泛 | 调优检测规则;在高流量场景使用基于 ML 的分类器 |
| 模型输出中出现 PII | 模型在含 PII 的数据上训练 | 在输出层加入 Presidio 清洗 |
| API 密钥泄露 | 密钥出现在日志或响应中 | 在日志中屏蔽密钥;使用 vault 存储密钥 |
| 模型权重被篡改 | 下载的权重未经验证 | 始终校验 SHA-256;使用 `modelscan` |
| 速率限制被绕过 | 按 IP 而非按用户限流 | 对已认证用户 ID 而非 IP 进行限流 |

## 最佳实践

- 切勿记录原始提示或补全内容——它们可能包含 PII 或敏感数据。
- 将 LLM 输出视为不可信输入——在 HTML 中渲染前始终进行编码。
- 使用网络策略防止 LLM Pod 发起出站互联网调用。
- 每季度轮换 API 密钥;服务间认证使用短期有效的 JWT 令牌。
- 对任何从互联网下载的模型,在提供服务前先运行 `modelscan`。

## 相关技能

- hashicorp-vault (`hashicorp-vault`) - API 密钥的密钥管理
- [network-security] (../../network/) - 网络层控制
- linux-hardening (`linux-hardening`) - 主机加固
- agent-observability (`agent-observability`) - AI 审计日志
- llm-gateway (`llm-gateway`) - 集中式访问控制

## 限制

- 仅在授权范围内应用本指导;破坏性步骤先在非生产环境中测试。
- 仅导入文档:上游脚本和模板未随附。

### 示例

```bash
# Read-only first: inventory before any active step.
which <tool> && <tool> --help | head -n 20
```

> 改编自 [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills) (MIT);为符合上游合规要求,新增了 frontmatter、"何时使用"/"限制"部分及安全边界说明。仅导入文档:未随附辅助脚本和模板。
