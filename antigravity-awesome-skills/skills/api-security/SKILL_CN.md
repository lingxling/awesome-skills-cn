---
name: api-security
description: "REST、GraphQL、WebSocket 和 SOAP API 的授权安全评估：发现、身份验证和授权缺陷（BOLA/IDOR、JWT/OAuth）、速率限制测试和结构化的多阶段方法。"
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ 仅限授权使用**
> 此技能仅用于教育目的或授权的安全评估。
> 在使用此工具之前，您必须获得系统所有者的明确书面权限。
> 滥用此工具是非法的，严格禁止。

> **强制确认门**
> 在运行任何探测、利用、更改、持久化、从目标提取数据或尝试凭据访问的命令之前：
> 1. 要求用户说明确切的目标 URL、IP、帐户或资源。
> 2. 要求用户确认书面授权和允许的范围。
> 3. 显示确切的命令并解释其预期影响。
> 4. 等待当前对话中的明确确认。
>
> 没有该确认，保持只读状态并仅提供防御性指导。建议使用沙盒、可弃置的虚拟机或受控实验室。

# API 安全测试
## 何时使用

- 授权的评估涵盖 API 端点，您需要从发现到报告的结构化工作流。
- 在批准的范围内测试 API 身份验证、授权或速率限制行为。


## 适用场景

- REST API 安全测试（OpenAPI/Swagger 驱动或盲测）
- GraphQL 安全审计（内省、批查询、别名过载）
- WebSocket 安全测试
- JWT / OAuth 2.0 认证测试
- BOLA/IDOR/BFLA 授权漏洞检测
- API 限速绕过与 DoS 测试

## 10 阶段测试流程

### 阶段 1: API 发现与侦察

```text
主动发现：
□ Vespasian: 无头浏览器爬取 → 自动生成 OpenAPI 3.0 / GraphQL SDL 规范
□ Entropy --discover: 从 robots.txt + JS 文件提取端点
□ Kiterunner / ffuf: 爆破未文档化的端点路径
□ 检查常见路径: /swagger.json, /openapi.json, /graphql, /api-docs

GraphQL 内省（三级尝试）：
  1. 标准内省查询
  2. 精简查询（绕过 WAF 全量封禁）
  3. 仅查 __schema { types { name } }（最小探测）
```

### 阶段 2: 认证测试

```text
JWT 分析（jwt_tool / Burp）：
□ alg:none 攻击: 修改头部为 "alg":"none"，清空签名
□ 密钥混淆: RS256 公钥 → HS256 对称密钥
□ 弱 HMAC 密钥爆破: jwt_tool -C -d wordlist.txt
□ 过期/声明篡改: 修改 exp/iat/sub/role 声明
□ kid 注入: ../../etc/passwd → HMAC 签名绕过

OAuth 2.0：
□ redirect_uri 操控 → 授权码泄漏
□ CSRF via state 参数缺失
□ Token 在 Referer 头泄漏
□ PKCE 缺失检测

GraphQL 认证：
□ mutation 通过 GET 请求绕过认证（CSRF）
□ 批查询认证绕过
```

### 阶段 3: 授权测试（BOLA/IDOR/BFLA）

```text
BOLA（对象级授权绕过）：
□ 遍历数字 ID: /user/1 → /user/2 → /user/3
□ 遍历 UUID
□ 遍历用户名/邮箱
□ Burp Autorize: 双会话重放对比

BFLA（功能级授权绕过）：
□ 普通用户执行管理员 API
□ HTTP 方法切换: GET → PUT → PATCH → DELETE
□ API 版本降级: /v2/admin → /v1/admin
□ 批量操作注入: {"users": [1,2,3]} → {"users": [1,2,3,admin_id]}

工具: Burp Autorize, AuthMatrix, Entropy (malicious_insider persona)
```

### 阶段 4: GraphQL 专项

```text
内省泄漏 → 信息暴露检测
别名过载 → 100+ 别名 DoS
批查询 → 10+ 同时查询 DoS
字段重复 → __typename × 500
指令过载 → 递归 @skip/@include
循环查询 → 深度嵌套内省递归
字段建议 → 错误消息信息泄漏
GraphiQL/Playground 暴露 → IDE 公开风险
GET 突变 → CSRF 风险
追踪/调试模式 → 元数据泄漏

工具: FireTail, Escape DAST, api.sh (Phases 1-3)
```

### 阶段 5: REST 输入验证

```text
□ HTTP 方法切换: GET→POST→PUT→DELETE→OPTIONS→PATCH
□ Content-Type 篡改: JSON→XML→multipart
□ NoSQL 注入: {"username": {"$gt": ""}}
□ SSRF via URL 参数: webhook URL/头像 URL/导入 URL
□ XXE in XML 端点
□ 参数污染: /api?role=user&role=admin
□ 批量赋值: 向请求体添加 is_admin: true
```

### 阶段 6: 业务逻辑与差分测试

```text
□ Entropy compare: diff v1 vs v2 API → 状态码变化/字段删除/延迟回归
□ 多角色工作流测试: admin/user/readonly 权限矩阵
□ 优惠券/积分/价格操控
□ 竞态条件: 并发请求测试 TOCTOU
```

### 阶段 7: WebSocket 测试

```text
□ 端点发现
□ 消息注入（注入 payload、原型污染）
□ 超大消息处理
□ 类型混淆
□ 跨站点 WebSocket 劫持（CSWH）
```

### 阶段 8: 限速与 DoS

```text
□ 限速绕过 via 头部: X-Forwarded-For, X-Real-IP
□ 路径变体: /api/ → /api → /Api/ → /API/
□ Slowloris 低带宽耗尽
□ GraphQL 批查询深度嵌套 DoS
□ IP 轮换测试（ProxyCat 代理池）
```

### 阶段 9: 数据暴露

```text
□ 响应过度暴露: 对比 API 返回 vs UI 展示
□ 分页枚举: ?page=1&limit=10000
□ 错误消息信息泄漏: 堆栈跟踪/内部路径/SQL 错误
□ GraphQL 嵌套遍历访问越权数据
□ OpenAPI 规范暴露敏感端点
```

### 阶段 10: CI/CD 集成

```text
□ Entropy --ci --watch: spec 变更时自动重跑
□ Escape DAST: 按严重度阈值自动阻断构建
□ 发现持久化为回归测试
□ StackHawk（开发者优先、ZAP 内核）
```

## 工具链

| 工具 | 用途 | 获取 |
|------|------|------|
| Vespasian | 流量 → OpenAPI/GraphQL 规范 | GitHub: praetorian-inc/vespasian |
| Entropy | LLM 生成攻击场景，5 personas | GitHub: arjinexe/entropy-chaos |
| Escape DAST | 业务逻辑安全测试 | escape.tech |
| api.sh | 8 阶段全协议攻击管道 | GitHub: Sharon-Needles/api |
| FireTail | GraphQL 12 专项测试 | firetail.ai |
| jwt_tool | JWT 全面测试 | GitHub: ticarpi/jwt_tool |
| Burp Autorize | 双会话授权对比 | Burp BApp Store |

## 参考

- `references/rest-graphql-testing.md` — REST + GraphQL 深度测试
- `references/jwt-oauth-testing.md` — JWT + OAuth 安全测试


## 任务完成自检（声称完成前 MUST 通过）

- [ ] 我是否执行了工作流中的每一步（而不是只阅读）？
- [ ] 我是否基于 `tool-index` 使用了真实工具路径？
- [ ] 我是否产出了可复现证据（命令/脚本/截图/报告）？
- [ ] 我是否完成并回写了 RULES 要求的 Checklist 项？

## 限制

- 仅对您明确授权测试的 API 运行。
- 某些检查具有侵入性；如果可用，建议在非生产镜像上进行。

> 改编自 [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT)。
