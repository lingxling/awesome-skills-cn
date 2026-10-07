---
name: api-documentation
description: "用于生成 OpenAPI 规范、创建开发者指南和维护全面 API 文档的 API 文档工作流。"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# API 文档工作流

## 概述

用于创建包括 OpenAPI/Swagger 规范、开发者指南、代码示例和交互式文档的全面 API 文档的专门工作流。

## 何时使用此工作流

在以下情况下使用此工作流：
- 创建 API 文档
- 生成 OpenAPI 规范
- 编写开发者指南
- 添加代码示例
- 设置 API 门户

## 工作流阶段

### 阶段 1：API 发现

#### 要调用的技能
- `api-documenter` - API 文档
- `api-design-principles` - API 设计

#### 操作
1. 库存端点
2. 文档请求/响应
3. 识别身份验证
4. 映射错误代码
5. 注明速率限制

#### 复制粘贴提示
```
使用 @api-documenter 来发现和文档 API 端点
```

### 阶段 2：OpenAPI 规范

#### 要调用的技能
- `openapi-spec-generation` - OpenAPI
- `api-documenter` - API 规范

#### 操作
1. 创建 OpenAPI 模式
2. 定义路径
3. 添加模式
4. 配置安全性
5. 添加示例

#### 复制粘贴提示
```
使用 @openapi-spec-generation 来创建 OpenAPI 规范
```

### 阶段 3：开发者指南

#### 要调用的技能
- `api-documentation-generator` - 文档
- `documentation-templates` - 模板

#### 操作
1. 创建入门指南
2. 编写身份验证指南
3. 文档常见模式
4. 添加故障排除
5. 创建常见问题解答

#### 复制粘贴提示
```
使用 @api-documentation-generator 来创建开发者指南
```

### 阶段 4：代码示例

#### 要调用的技能
- `api-documenter` - 代码示例
- `tutorial-engineer` - 教程

#### 操作
1. 创建示例请求
2. 编写 SDK 示例
3. 添加 curl 示例
4. 创建教程
5. 测试示例

#### 复制粘贴提示
```
使用 @api-documenter 来生成代码示例
```

### 阶段 5：交互式文档

#### 要调用的技能
- `api-documenter` - 交互式文档

#### 操作
1. 设置 Swagger UI
2. 配置 Redoc
3. 添加试用功能
4. 测试交互性
5. 部署文档

#### 复制粘贴提示
```
使用 @api-documenter 来设置交互式文档
```

### 阶段 6：文档网站

#### 要调用的技能
- `docs-architect` - 文档架构
- `wiki-page-writer` - 文档

#### 操作
1. 选择平台
2. 设计结构
3. 创建页面
4. 添加导航
5. 配置搜索

#### 复制粘贴提示
```
使用 @docs-architect 来设计 API 文档网站
```

### 阶段 7：维护

#### 要调用的技能
- `api-documenter` - 文档维护

#### 操作
1. 设置自动生成
2. 配置验证
3. 添加审查流程
4. 安排更新
5. 监控反馈

#### 复制粘贴提示
```
使用 @api-documenter 来设置自动文档生成
```

## 质量关卡

- [ ] OpenAPI 规范完成
- [ ] 开发者指南编写完成
- [ ] 代码示例正常运行
- [ ] 交互式文档功能正常
- [ ] 文档已部署

## 相关工作流捆绑

- `documentation` - 文档
- `api-development` - API 开发
- `development` - 开发

## 限制
- 仅在任务明确与上述描述的范围相匹配时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
