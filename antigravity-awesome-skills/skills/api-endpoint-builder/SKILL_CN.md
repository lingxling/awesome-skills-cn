---
name: api-endpoint-builder
description: "构建具有验证、错误处理、身份验证和文档的生产级 REST API 端点。遵循安全性和可扩展性的最佳实践。"
category: development
risk: safe
source: community
date_added: "2026-03-05"
---

# API 端点构建器

构建完整的、生产级的 REST API 端点，具有正确的验证、错误处理、身份验证和文档。

## 何时使用此技能

- 用户要求"创建 API 端点"或"构建 REST API"
- 构建新的后端功能
- 向现有 API 添加端点
- 用户提到"API"、"端点"、"路由"或"REST"
- 创建 CRUD 操作

## 您将构建什么

对于每个端点，您创建：
- 具有正确 HTTP 方法的路由处理器
- 输入验证（请求体、参数、查询）
- 身份验证/授权检查
- 业务逻辑
- 错误处理
- 响应格式化
- API 文档
- 测试（如果要求）

## 端点结构

### 1. 路由定义

```javascript
// Express 示例
router.post('/api/users', authenticate, validateUser, createUser);

// Fastify 示例
fastify.post('/api/users', {
  preHandler: [authenticate],
  schema: userSchema
}, createUser);
```

### 2. 输入验证

始终在处理前验证：

```javascript
const validateUser = (req, res, next) => {
  const { email, name, password } = req.body;
  
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: '需要有效的电子邮件' });
  }
  
  if (!name || name.length < 2) {
    return res.status(400).json({ error: '名称必须至少为 2 个字符' });
  }
  
  if (!password || password.length < 8) {
    return res.status(400).json({ error: '密码必须至少为 8 个字符' });
  }
  
  next();
};
```

### 3. 处理器实现

```javascript
const createUser = async (req, res) => {
  try {
    const { email, name, password } = req.body;
    
    // 检查用户是否存在
    const existing = await db.users.findOne({ email });
    if (existing) {
      return res.status(409).json({ error: '用户已存在' });
    }
    
    // 哈希密码
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // 创建用户
    const user = await db.users.create({
      email,
      name,
      password: hashedPassword,
      createdAt: new Date()
    });
    
    // 不返回密码
    const { password: _, ...userWithoutPassword } = user;
    
    res.status(201).json({
      success: true,
      data: userWithoutPassword
    });
    
  } catch (error) {
    console.error('创建用户错误:', error);
    res.status(500).json({ error: '内部服务器错误' });
  }
};
```

## 最佳实践

### HTTP 状态代码
- `200` - 成功（GET、PUT、PATCH）
- `201` - 已创建（POST）
- `204` - 无内容（DELETE）
- `400` - 错误请求（验证失败）
- `401` - 未授权（未认证）
- `403` - 禁止（未授权）
- `404` - 未找到
- `409` - 冲突（重复）
- `500` - 内部服务器错误

### 响应格式

一致的结构：

```javascript
// 成功
{
  "success": true,
  "data": { ... }
}

// 错误
{
  "error": "错误消息",
  "details": { ... } // 可选
}

// 列表带分页
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### 安全检查清单

- [ ] 受保护路由需要身份验证
- [ ] 授权检查（用户拥有资源）
- [ ] 所有字段的输入验证
- [ ] SQL 注入预防（使用参数化查询）
- [ ] 公开端点的速率限制
- [ ] 响应中无敏感数据（密码、令牌）
- [ ] CORS 配置正确
- [ ] 设置了请求大小限制

### 错误处理

```javascript
// 集中式错误处理器
app.use((err, req, res, next) => {
  console.error(err.stack);
  
  // 不要在生产环境中泄露错误详情
  const message = process.env.NODE_ENV === 'production' 
    ? '内部服务器错误' 
    : err.message;
  
  res.status(err.status || 500).json({ error: message });
});
```

## 常见模式

### CRUD 操作

```javascript
// 创建
POST /api/resources
Body: { name, description }

// 读取（列表）
GET /api/resources?page=1&limit=20

// 读取（单个）
GET /api/resources/:id

// 更新
PUT /api/resources/:id
Body: { name, description }

// 删除
DELETE /api/resources/:id
```

### 分页

```javascript
const getResources = async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const skip = (page - 1) * limit;
  
  const [resources, total] = await Promise.all([
    db.resources.find().skip(skip).limit(limit),
    db.resources.countDocuments()
  ]);
  
  res.json({
    success: true,
    data: resources,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  });
};
```

### 筛选和排序

```javascript
const getResources = async (req, res) => {
  const { status, sort = '-createdAt' } = req.query;
  
  const filter = {};
  if (status) filter.status = status;
  
  const resources = await db.resources
    .find(filter)
    .sort(sort)
    .limit(20);
  
  res.json({ success: true, data: resources });
};
```

## 文档模板

```javascript
/**
 * @route POST /api/users
 * @desc 创建新用户
 * @access 公开
 * 
 * @body {string} email - 用户电子邮件（必需）
 * @body {string} name - 用户名称（必需）
 * @body {string} password - 密码，最少 8 个字符（必需）
 * 
 * @returns {201} 用户创建成功
 * @returns {400} 验证错误
 * @returns {409} 用户已存在
 * @returns {500} 服务器错误
 * 
 * @example
 * POST /api/users
 * {
 *   "email": "user@example.com",
 *   "name": "John Doe",
 *   "password": "securepass123"
 * }
 */
```

## 测试示例

```javascript
describe('POST /api/users', () => {
  it('应该创建新用户', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      });
    
    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.email).toBe('test@example.com');
    expect(response.body.data.password).toBeUndefined();
  });
  
  it('应该拒绝无效的电子邮件', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'invalid',
        name: 'Test User',
        password: 'password123'
      });
    
    expect(response.status).toBe(400);
    expect(response.body.error).toContain('email');
  });
});
```

## 关键原则

- 在处理前验证所有输入
- 使用正确的 HTTP 状态代码
- 优雅地处理错误
- 切勿泄露敏感数据
- 保持响应一致
- 在需要时添加身份验证
- 文档化您的端点
- 为关键路径编写测试

## 相关技能

- `@security-auditor` - 安全审查
- `@test-driven-development` - 测试
- `@database-design` - 数据建模

## 限制
- 仅在任务明确与上述描述的范围相匹配时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
