---
name: api-patterns
description: "API 设计原则和决策制定。REST 与 GraphQL 与 tRPC 选择、响应格式、版本控制、分页。"
risk: none
source: community
date_added: "2026-02-27"
---

# API 模式

> 与消费者和部署约束相关的 API 设计决策。
> **学会思考，而不是复制固定的模式。**

## 🎯 选择性阅读规则

**仅读取与请求相关的文件！** 检查内容地图，找到您需要的内容。

---

## 📑 内容地图

| 文件 | 描述 | 何时阅读 |
|------|-------------|--------------|
| `api-style.md` | REST 与 GraphQL 与 tRPC 决策树 | 选择 API 类型 |
| `rest.md` | 资源命名、HTTP 方法、状态代码 | 设计 REST API |
| `response.md` | 信封模式、错误格式、分页 | 响应结构 |
| `graphql.md` | 模式设计、何时使用、安全 | 考虑 GraphQL |
| `trpc.md` | TypeScript 单体仓库、类型安全 | TS 全栈项目 |
| `versioning.md` | URI/Header/Query 版本控制 | API 演变规划 |
| `auth.md` | JWT、OAuth、Passkey、API 密钥 | 身份验证模式选择 |
| `rate-limiting.md` | 令牌桶、滑动窗口 | API 保护 |
| `documentation.md` | OpenAPI/Swagger 最佳实践 | 文档 |
| `security-testing.md` | OWASP API Top 10、身份验证/授权测试 | 安全审计 |

---

## 🔗 相关技能

| 需要 | 技能 |
|------|-------|
| API 实现 | `@[skills/backend-architect]` |
| 数据结构 | `@[skills/database-design]` |
| 安全详情 | `@[skills/api-security-best-practices]` |

---

## ✅ 决策检查清单

在设计 API 之前：

- [ ] **询问用户关于 API 消费者？**
- [ ] **为此上下文选择了 API 风格？** (REST/GraphQL/tRPC)
- [ ] **定义了一致的响应格式？**
- [ ] **规划了版本控制策略？**
- [ ] **考虑了身份验证需求？**
- [ ] **规划了速率限制？**
- [ ] **定义了文档方法？**

---

## ❌ 反模式

**不要：**
- 默认为一切使用 REST
- 在 REST 端点中使用动词 (/getUsers)
- 返回不一致的响应格式
- 向客户端暴露内部错误
- 跳过速率限制

**要做：**
- 根据上下文选择 API 风格
- 询问客户端要求
- 彻底文档化
- 使用适当的状态代码

---

## 脚本

| 脚本 | 用途 | 命令 |
|--------|---------|---------|
| `scripts/api_validator.py` | 本地启发式源代码扫描（不是模式验证） | `python3 skills/api-patterns/scripts/api_validator.py <project_path>` |

## 何时使用

在定义新端点协议、为已知消费者选择 REST/GraphQL/tRPC 或更改分页、错误、身份验证或兼容性行为时使用。对于现有协议中的错误，请保留该协议，除非任务授权进行更改。

## 输入和程序

记录消费者和已部署的版本、预期有效负载大小、访问规则、兼容性义务和一个具体操作。读取地图中的相关文件、比较真实的选择，然后指定请求/响应示例和拒绝案例。在构建时共享的类型不能确保独立部署的客户端保持兼容。

## 工作示例

输入：公开订单列表在客户端浏览时更改。选择有界页面大小和基于稳定 `(created_at, id)` 顺序的游标。定义下一游标格式、授权筛选器和删除记录或无效游标的行为。测试两个相等的时间戳和页面之间的插入。预期：承诺的快照语义中没有重复的 ID；文档化新插入的行是否可以出现。

## 限制

- Python 帮助程序最多使用正则表达式和浅 JSON/YAML 检查扫描 15 个匹配的文件。其输出是分类提示，不是 OpenAPI 验证、授权审计或部署批准。
- GraphQL 查询形状、tRPC 推理和 HTTP 方法名称不强制资源授权或向后兼容性。
- 速率限制单独无法防止所有资源耗尽；大小、并发、时间和提供商成本界限取决于操作。
- 仅对授权的本地/测试目标执行安全检查，使用隔离的帐户和定义的范围。
