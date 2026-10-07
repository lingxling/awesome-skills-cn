---
name: architecture-decision-records
description: "用于创建、维护和管理架构决策记录(ADR)的全面模式,这些记录捕获了重大技术决策背后的背景和理由。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 架构决策记录

用于创建、维护和管理架构决策记录(ADR)的全面模式,这些记录捕获了重大技术决策背后的背景和理由。

## 何时使用此技能

- 做出重大架构决策时
- 记录技术选型时
- 记录设计权衡取舍时
- 新团队成员入职时
- 回顾历史决策时
- 建立决策流程时

## 何时不使用此技能

- 你只需要记录细微的实现细节
- 变更只是小补丁或日常维护
- 没有需要捕获的架构决策

## 使用说明

1. 捕获决策背景、约束条件和驱动因素。
2. 记录考虑过的各个选项及其权衡取舍。
3. 记录决策、理由和后果。
4. 关联相关的 ADR,并随时间更新状态。

## 核心概念

### 1. 什么是 ADR?

架构决策记录捕获了:
- **背景(Context)**: 为什么我们需要做出这个决策
- **决策(Decision)**: 我们决定了什么
- **后果(Consequences)**: 由此产生的结果

### 2. 何时编写 ADR

| 需要编写 ADR | 可以跳过 ADR |
|-----------|----------|
| 采用新框架 | 小版本升级 |
| 数据库技术选型 | 修复缺陷 |
| API 设计模式 | 实现细节 |
| 安全架构 | 日常维护 |
| 集成模式 | 配置变更 |

### 3. ADR 生命周期

```
已提议 → 已接受 → 已废弃 → 已被取代
              ↓
           已拒绝
```

## 模板

### 模板 1: 标准 ADR(MADR 格式)

```markdown
# ADR-0001: 使用 PostgreSQL 作为主数据库

## 状态

已接受

## 背景

我们需要为新的电子商务平台选择一个主数据库。该系统将处理:
- 约 10,000 个并发用户
- 具有层级分类的复杂产品目录
- 订单和支付的事务处理
- 产品的全文搜索
- 用于门店定位的地理空间查询

团队有 MySQL、PostgreSQL 和 MongoDB 的使用经验。我们需要金融交易
具备 ACID 合规性。

## 决策驱动因素

* 支付处理**必须具备 ACID 合规性**
* **必须支持复杂查询**以用于报表
* **应该支持全文搜索**以降低基础设施复杂度
* **应该有良好的 JSON 支持**以便灵活处理产品属性
* **团队的熟悉程度**可减少入职培训时间

## 已考虑的选项

### 选项 1: PostgreSQL
- **优点**: 符合 ACID、出色的 JSON 支持(JSONB)、内置全文
  搜索、支持地理空间的 PostGIS、团队有相关经验
- **缺点**: 复制配置比 MySQL 稍复杂

### 选项 2: MySQL
- **优点**: 团队非常熟悉、复制简单、社区庞大
- **缺点**: JSON 支持较弱、无内置全文搜索(需要
  Elasticsearch)、无扩展支持则没有地理空间能力

### 选项 3: MongoDB
- **优点**: 灵活的模式、原生 JSON、水平扩展
- **缺点**: (在决策时)多文档事务不支持 ACID,
  团队经验有限,需要严格的模式设计规范

## 决策

我们将使用 **PostgreSQL 15** 作为我们的主数据库。

## 理由

PostgreSQL 在以下方面提供了最佳平衡:
1. 对电子商务交易而言至关重要的 **ACID 合规性**
2. **内置能力**(全文搜索、JSONB、PostGIS)可降低
   基础设施复杂度
3. 团队**对 SQL 数据库的熟悉程度**降低了学习曲线
4. **成熟的生态系统**,具备出色的工具链和社区支持

复制方面的轻微复杂性被减少额外服务(无需单独的
Elasticsearch)所带来的收益所抵消。

## 后果

### 正面
- 单一数据库可处理事务、搜索和地理空间查询
- 降低运维复杂度(需要管理的服务更少)
- 对金融数据提供强一致性保证
- 团队可以利用现有的 SQL 专业知识

### 负面
- 需要学习 PostgreSQL 特有的功能(JSONB、全文搜索语法)
- 垂直扩展的限制可能会更早需要读副本
- 部分团队成员需要 PostgreSQL 相关培训

### 风险
- 全文搜索的扩展性可能不如专门的搜索引擎
- 缓解措施: 如有需要,设计上为后续添加 Elasticsearch 留出余地

## 实施说明

- 使用 JSONB 存储灵活的产品属性
- 使用 PgBouncer 实现连接池
- 设置流复制以实现读副本
- 使用 pg_trgm 扩展实现模糊搜索

## 相关决策

- ADR-0002: 缓存策略(Redis)—— 对数据库选型的补充
- ADR-0005: 搜索架构 —— 如果需要 Elasticsearch,可能会取代本决策

## 参考资料

- [PostgreSQL JSON 文档](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL 全文搜索](https://www.postgresql.org/docs/current/textsearch.html)
- 内部资料: `/docs/benchmarks/database-comparison.md` 中的性能基准测试
```

### 模板 2: 轻量级 ADR

```markdown
# ADR-0012: 前端开发采用 TypeScript

**状态**: 已接受
**日期**: 2024-01-15
**决策者**: @alice、@bob、@charlie

## 背景

我们的 React 代码库已经增长到 50 多个组件,与属性类型不匹配
和未定义错误相关的缺陷报告不断增加。PropTypes 只能提供
运行时检查。

## 决策

所有新的前端代码采用 TypeScript。对现有代码进行增量迁移。

## 后果

**好处**: 在编译时捕获类型错误,更好的 IDE 支持,自文档化
代码。

**坏处**: 团队有学习曲线,初期开发速度下降,构建复杂度增加。

**缓解措施**: 开展 TypeScript 培训课程,通过
`allowJs: true` 允许渐进式采用。
```

### 模板 3: Y-陈述格式(Y-Statement Format)

```markdown
# ADR-0015: API Gateway 选型

在**构建微服务架构**的背景下,
面对**集中化 API 管理、认证和速率限制的需求**,
我们决定选用 **Kong Gateway**
而不是 **AWS API Gateway 和自建 Nginx 方案**,
以实现**厂商独立性、插件可扩展性,以及团队对 Lua 的熟悉程度**,
并接受**我们需要自行管理 Kong 基础设施**这一代价。
```

### 模板 4: 用于弃用的 ADR

```markdown
# ADR-0020: 弃用 MongoDB,转向 PostgreSQL

## 状态

已接受(取代 ADR-0003)

## 背景

ADR-0003(2021 年)由于模式灵活性需求而选择了 MongoDB 用于用户资料存储。
自那以后:
- MongoDB 的多文档事务对我们的使用场景而言仍然存在问题
- 我们的模式已经稳定,很少变动
- 我们现在从其他服务中积累了 PostgreSQL 的专业知识
- 维护两种数据库增加了运维负担

## 决策

弃用 MongoDB,将用户资料迁移到 PostgreSQL。

## 迁移计划

1. **阶段 1**(第 1-2 周): 创建 PostgreSQL 模式,启用双写
2. **阶段 2**(第 3-4 周): 回填历史数据,验证一致性
3. **阶段 3**(第 5 周): 将读操作切换到 PostgreSQL,进行监控
4. **阶段 4**(第 6 周): 移除 MongoDB 写操作,下线 MongoDB

## 后果

### 正面
- 单一数据库技术降低了运维复杂度
- 用户数据具备 ACID 事务
- 团队可以专注于 PostgreSQL 专业知识

### 负面
- 迁移工作量(约 4 周)
- 迁移期间存在数据问题的风险
- 失去部分模式灵活性

## 经验教训

来自 ADR-0003 经验的记录:
- 模式灵活性的好处被高估了
- 维护多个数据库的运维成本被低估了
- 在技术决策中要考虑长期维护成本
```

### 模板 5: Request for Comments(RFC)风格

```markdown
# RFC-0025: 在订单管理中采用事件溯源

## 摘要

建议在订单管理领域采用事件溯源模式,以
提升可审计性、支持时间点查询,并支持业务分析。

## 动机

当前的挑战:
1. 审计要求需要完整的订单历史
2. 无法回答"在 X 时刻订单状态是什么?"这类查询
3. 分析团队需要事件流用于实时仪表盘
4. 为客服重建订单状态只能靠人工

## 详细设计

### 事件存储

```
OrderCreated { orderId, customerId, items[], timestamp }
OrderItemAdded { orderId, item, timestamp }
OrderItemRemoved { orderId, itemId, timestamp }
PaymentReceived { orderId, amount, paymentId, timestamp }
OrderShipped { orderId, trackingNumber, timestamp }
```

### 投影(Projections)

- **CurrentOrderState**: 用于查询的物化视图
- **OrderHistory**: 用于审计的完整时间线
- **DailyOrderMetrics**: 分析汇总

### 技术选型

- 事件存储: EventStoreDB(专门构建,处理投影)
- 考虑过的替代方案: Kafka + 自建投影服务

## 缺点

- 团队有学习曲线
- 相比 CRUD 复杂度增加
- 需要仔细设计事件(一旦存储则不可变)
- 存储增长(事件永不删除)

## 替代方案

1. **审计表**: 更简单,但无法支持时间点查询
2. **来自现有数据库的 CDC**: 复杂,不改变数据模型
3. **混合方案**: 仅对订单状态变化使用事件溯源

## 未解决的问题

- [ ] 事件模式版本管理策略
- [ ] 事件的保留策略
- [ ] 快照频率(出于性能考虑)

## 实施计划

1. 针对单一订单类型进行原型验证(2 周)
2. 团队事件溯源培训(1 周)
3. 完整实现与迁移(4 周)
4. 持续监控与优化

## 参考资料

- [Martin Fowler 的事件溯源](https://martinfowler.com/eaaDev/EventSourcing.html)
- [EventStoreDB 文档](https://www.eventstore.com/docs)
```

## ADR 管理

### 目录结构

```
docs/
├── adr/
│   ├── README.md           # 索引与指南
│   ├── template.md         # 团队的 ADR 模板
│   ├── 0001-use-postgresql.md
│   ├── 0002-caching-strategy.md
│   ├── 0003-mongodb-user-profiles.md  # [已废弃]
│   └── 0020-deprecate-mongodb.md      # 取代 0003
```

### ADR 索引(README.md)

```markdown
# 架构决策记录

本目录包含 [项目名称] 的架构决策记录(ADR)。

## 索引

| ADR | 标题 | 状态 | 日期 |
|-----|-------|--------|------|
| 0001 | 使用 PostgreSQL 作为主数据库 | 已接受 | 2024-01-10 |
| 0002 | 使用 Redis 的缓存策略 | 已接受 | 2024-01-12 |
| 0003 | 用户资料使用 MongoDB | 已废弃 | 2023-06-15 |
| 0020 | 弃用 MongoDB | 已接受 | 2024-01-15 |

## 创建新的 ADR

1. 将 `template.md` 复制为 `NNNN-title-with-dashes.md`
2. 填写模板
3. 提交 PR 进行审查
4. 批准后更新此索引

## ADR 状态

- **已提议**: 正在讨论中
- **已接受**: 已做出决策,正在实施
- **已废弃**: 不再相关
- **已被取代**: 已被另一个 ADR 替代
- **已拒绝**: 已考虑但未采纳
```

### 自动化(adr-tools)

```bash
# 安装 adr-tools
brew install adr-tools

# 初始化 ADR 目录
adr init docs/adr

# 创建新 ADR
adr new "Use PostgreSQL as Primary Database"

# 取代一个 ADR
adr new -s 3 "Deprecate MongoDB in Favor of PostgreSQL"

# 生成目录
adr generate toc > docs/adr/README.md

# 关联相关 ADR
adr link 2 "Complements" 1 "Is complemented by"
```

## 审查流程

```markdown
## ADR 审查清单

### 提交前
- [ ] 背景清楚地说明了问题
- [ ] 已考虑所有可行的选项
- [ ] 优缺点权衡均衡且诚实
- [ ] 已记录后果(正面和负面)
- [ ] 已关联相关 ADR

### 审查期间
- [ ] 至少有 2 名资深工程师审查
- [ ] 已咨询受影响的团队
- [ ] 已考虑安全影响
- [ ] 已记录成本影响
- [ ] 已评估可逆性

### 接受后
- [ ] 已更新 ADR 索引
- [ ] 已通知团队
- [ ] 已创建实施工单
- [ ] 已更新相关文档
```

## 最佳实践

### 应该做的
- **尽早编写 ADR** —— 在实现开始之前
- **保持简短** —— 最多 1-2 页
- **诚实对待权衡取舍** —— 包含真实的缺点
- **关联相关决策** —— 构建决策图谱
- **更新状态** —— 当被取代时予以废弃

### 不应该做的
- **不要修改已接受的 ADR** —— 编写新的 ADR 来取代它
- **不要跳过背景** —— 未来的读者需要背景信息
- **不要隐藏失败** —— 被拒绝的决策同样有价值
- **不要含糊其辞** —— 要有具体的决策、具体的后果
- **不要忘记实施** —— 没有行动的 ADR 就是浪费

## 资源

- [记录架构决策(Michael Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [MADR 模板](https://adr.github.io/madr/)
- [ADR GitHub 组织](https://adr.github.io/)
- [adr-tools](https://github.com/npryce/adr-tools)

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出当作特定环境验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准,请停止并寻求澄清。
