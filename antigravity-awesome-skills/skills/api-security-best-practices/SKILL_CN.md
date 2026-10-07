---
name: api-security-best-practices
description: "实现安全的 API 设计模式，包括身份验证、授权、输入验证、速率限制，以及针对常见 API 漏洞的防护"
risk: critical
source: community
date_added: "2026-02-27"
---

# API 安全最佳实践

审查从调用者身份认证、授权、经过验证的输入、存储，到可观测响应的
整条请求边界。保留应用程序实际的身份提供方和数据模型，而不是
引入第二套身份验证系统。

## 何时使用

在新增受保护端点、审查对象访问、替换过于宽松的请求解析逻辑，
或调查 API 滥用路径时使用本技能。对于一个具体的缺陷，应从出问题
的路由及其调用方入手；不要部署与之无关的安全基础设施。

## 输入与前提条件

记录路由、调用方/租户模型、身份提供方、令牌契约、运行时及锁定的
依赖版本、数据库 schema、代理拓扑结构，以及经授权的测试范围。
在测试环境中使用合成身份。已有任务授权可以延续使用；生产环境
扫描、账户写入和消息发送则需要其各自独立的授权。下方的 Node
示例是针对 Express、jsonwebtoken 和 Zod 的集成草图；应用/数据库
适配器是特意直接命名的，而非以完整可运行服务的形式呈现。在集成
前，请对照已安装的版本确认各 API 的行为。

## 1. 验证确切的令牌契约

优先使用既有的提供方/会话中间件。当服务自身拥有一套 HMAC JWT
契约时，要求使用强健的、由服务端所有的密钥、固定的算法、确切的
issuer 和 audience，以及必需的运行时声明。切勿在完成签名验证之前
就从已解码的令牌中推断权限。切勿接受由调用方自行选择的验证算法。

```javascript
const jwt = require('jsonwebtoken');

// 示意性的第一方访问令牌契约；并非第三方 OAuth 适配器。
const ACCESS_POLICY = {
  algorithms: ['HS256'], issuer: 'example-auth', audience: 'example-api'
};
function verifyAccessToken(token, signingKey) {
  const claims = jwt.verify(token, signingKey, ACCESS_POLICY);
  if (!claims || typeof claims !== 'object' ||
      typeof claims.sub !== 'string' || !claims.sub ||
      typeof claims.tenantId !== 'string' || !claims.tenantId ||
      !Number.isSafeInteger(claims.exp) || !Number.isSafeInteger(claims.iat) ||
      claims.exp <= claims.iat) {
    throw new Error('Invalid access claims');
  }
  return { subject: claims.sub, tenantId: claims.tenantId };
}
function readBearer(header) {
  if (typeof header !== 'string' || header.length > 8192) return null;
  const match = /^Bearer ([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)$/i.exec(header);
  return match ? match[1] : null;
}
```

签发访问令牌时使用相同的 issuer/audience/算法，并设置应用程序所
批准的较短过期时间。将验证失败处理为统一的通用 401，不要回显令牌
或异常信息。过期本身并不等同于撤销令牌；应根据实际的威胁模型来
定义撤销机制或短生命周期会话。使用非对称提供方密钥的服务需要该
提供方的 discovery/JWKS 验证和密钥轮换策略，而不是本例中的 HMAC
方案。切勿将访问令牌当作刷新令牌重复使用。

### 刷新会话

使用提供方支持的会话流程，或采用服务端不透明刷新令牌的设计：
仅存储摘要值、过期时间、用户/会话族以及撤销状态。在一个原子事务
中消费旧的活动令牌并创建替代令牌。并发重用不应签发两个后继令牌；
已定义的重用处理逻辑应撤销受影响的整个令牌族。签发新访问令牌时
应检查当前用户状态和权限。将刷新操作绑定到预期的客户端/会话，
并对基于 cookie 的请求进行 CSRF 防护。切勿记录令牌、以明文形式
将其存入数据库，或通过 URL 返回刷新令牌。在宣称该流程完成之前，
请测试并发刷新、过期、重放、撤销以及事务失败等情况。此处未附带
数据库事务适配器。

## 2. 对资源和操作进行授权

身份验证用于识别调用者；授权则用于决定对某个对象和租户执行的
确切操作。角色名称本身并不会自动授予跨租户访问权限。应在数据库
变更操作中应用所有者/租户断言，以避免"先检查后写入"的竞态，
并对可写属性使用允许列表。应按照产品的资源暴露策略，统一使用
404/403。

```javascript
// Prisma 风格的草图；id 和租户类型必须与你实际的 schema 相匹配。
async function deleteOwnedPost(prisma, postId, principal) {
  const result = await prisma.post.deleteMany({
    where: { id: postId, userId: principal.subject, tenantId: principal.tenantId }
  });
  return result.count === 1;
}
```

管理员路径需要一套明确、独立的策略和审计事件；不要给每一个所有者
检查都添加隐式的管理员绕行机制。请测试：一个合法用户访问另一用户
的对象、同一 ID 在另一租户下的情况、已删除的成员关系，以及批量
操作端点。

## 3. 只解析一次，然后使用经过验证的值

应拒绝部分数字解析结果(`12abc` 并不是 ID 12)、不安全的整数、
意外出现的属性以及超大的请求。使用参数化数据库查询。ORM 本身
并不提供业务层授权，也不会使不安全的原始 SQL 变得安全。

```javascript
function parsePositiveId(raw) {
  if (typeof raw !== 'string' || !/^[1-9][0-9]{0,15}$/.test(raw)) return null;
  const value = Number(raw);
  return Number.isSafeInteger(value) && value > 0 ? value : null;
}

const { z } = require('zod');
const profileUpdate = z.object({
  displayName: z.string().trim().min(1).max(100)
}).strict();
function validateBody(schema) {
  return (req, res, next) => {
    const parsed = schema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ error: 'Invalid request' });
    }
    req.validatedBody = parsed.data; // 默认值/转换结果必须传递给处理函数。
    next();
  };
}
// 处理函数使用 req.validatedBody，绝不使用原始 body 或任意展开(spread)的数据。
```

应在解析之前设置请求体大小限制。Zod 的形状验证只是其中一层：还
需要在事务中检查当前的所有权、允许的状态转换以及唯一性约束。对
HTML 内容，只允许使用维护良好的清洗器所界定的必需标签/属性，然后
通过目标环境安全的输出 API 进行渲染。对于普通评论，优先使用纯
文本；对字符串进行清洗并不意味着它在任何 JavaScript、URL 或 HTML
上下文中都是安全的。上游 API 响应同样应作为不可信输入进行验证。

对于出站 URL，要明确定义允许的协议/主机、重定向行为、解析后的 IP
范围、凭据策略、超时时间和响应大小。仅靠正则表达式或 URL 解析器
并不能防止 SSRF 或 DNS rebinding。文件上传同样需要类型/内容检查、
大小限制、隔离存储以及读取时的授权控制。

## 4. 控制滥用行为，但不要声称具备 DDoS 防护能力

使用现有的网关和维护良好的速率限制存储。应先完成身份验证，再从
已认证用户派生限流键，并且永远不要信任用户自行提供的等级信息。
对于匿名流量，应使用库所支持的、支持 IPv6 的 IP 键处理方式，并
将 Express 的 trust proxy 配置为实际可信的跳数；不要对所有调用者
一概盲目启用它。

对于分布式配额，应使用具备原子性的"计数器加过期"实现，并明确
定义存储故障时的行为。应避免手写的"先 INCR 后 EXPIRE"：两者之间
发生崩溃可能导致该键永久存在。应区分按用户配额、按 IP 的滥用控制、
并发限制以及上游服务预算。记录实际的窗口/重置语义，并发送准确的
Retry-After，而不是硬编码的整窗口值。除非配置了共享存储，否则
内存中的限制器仅作用于单个进程。

请测试并发请求、IPv4/IPv6、伪造的转发头、未知等级、身份缺失、
Redis 故障以及过期情况。应用层的速率限制无法吸收网络层面的饱和
流量。Helmet 配置的是 HTTP 响应头；它不是 DDoS 防护、访问控制，
也不能替代上游的容量控制措施。应针对实际的部署和子域策略推出
CSP/HSTS；不要盲目照搬预加载设置。

## 5. 密码、密钥与日志记录

尽可能使用既有的身份提供方。对于存储的密码，应使用维护良好的
密码哈希方案，并校准相关参数(新设计优先选用 Argon2id)。应检查
是否为已泄露/常见密码，并支持使用密码短语(passphrase)。不要强加
任意的大小写/符号组合规则，也不要静默截断过长的密码。旧版 bcrypt
对输入字节数有限制，在迁移时必须明确处理这一点；密码按字符计算
的长度和按 UTF-8 字节计算的长度是不同的。

将密钥保存在经批准的密钥管理机制中，在启动时检查必需的配置项
而不打印其值，并对已暴露的凭据进行轮换。日志中绝不应包含原始
令牌、密码、请求体或完整的数据库异常信息。应在适当的留存/访问
策略下，记录有边界限制的事件名称、请求关联信息以及安全的状态/
错误类别。经过清洗的错误不应返回被批量赋值过的用户对象。CORS
控制的是浏览器的跨源访问，它不是 API 身份验证，也不是 CSRF 防护。

## 实例演练：个人资料更新边界

以 `PATCH /users/:id`(字符串 ID)和可编辑的显示名称为例：

1. 在测试夹具中记录经过授权的调用方/租户以及当前端点行为。
2. 检查缺失/过期/受众错误的令牌在触及存储层之前是否返回 401。
3. 发送 `12abc`、一个不安全的整数、一个空名称以及一个额外的 `role`
   字段；预期返回 400 且不发生数据库变更。发送一个带填充字符的
   合法名称；确认只有经解析、裁剪过的值能到达按所有者和租户限定
   范围的更新逻辑中。
4. 尝试使用另一个用户的合法 ID 以及跨租户 ID；预期返回文档中所述
   的拒绝结果，且不发生任何变更。合法所有者的请求应只更新被允许
   的那个属性。
5. 触发配额/存储故障场景，并确认日志中不包含请求令牌或姓名信息。

应返回路由策略、复现出的失败场景、确切的测试命令/输出，以及尚存
的差距。这些是预期在目标应用程序中要执行的检查，而不是本仓库已
对某个已部署 API 完成测试的断言。

## 局限性

本指南不是完整的身份服务、认证过的安全审计或渗透测试。代码片段
省略了应用适配器和集成错误中间件。对解析器的单元测试并不能验证
数据库事务、代理行为或提供方会话。应明确报告任何未经测试的路由、
租户路径和失败模式。不要仅凭结构性检查通过，或凭借某个风险元数据
标签，就推断出一个干净的安全态势。

## 参考资料

- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [JWT best current practices, RFC 8725](https://www.rfc-editor.org/rfc/rfc8725)
- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Express production security](https://expressjs.com/en/advanced/best-practice-security.html)
- [Zod basic parsing](https://zod.dev/basics)
- 相关技能：`auth-implementation-patterns`、`api-patterns`、`systematic-debugging`。
