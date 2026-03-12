# Antigravity 工作流

> 工作流手册，以更少的摩擦协调多个技能。

## 什么是工作流？

工作流是一个指导性的、逐步执行路径，将多个技能组合起来实现一个具体目标。

- **包**告诉您哪些技能与某个角色相关。
- **工作流**告诉您如何按顺序使用这些技能来完成实际目标。

如果包是您的工具箱，工作流就是您的执行手册。

---

## 如何使用工作流

1. 安装一次仓库（`npx antigravity-awesome-skills`）。
2. 选择符合您即时目标的工作流。
3. 按顺序执行步骤，并在每个步骤中调用的列出的技能。
4. 在每个步骤保留输出成果（计划、决策、测试、验证证据）。

当您需要更广泛的覆盖范围时，可以将工作流与[bundles.md](bundles.md)中的包结合使用。

---

## 工作流：发布SaaS MVP

构建并发布一个最小化但面向生产的SaaS产品。

### 步骤1：产品架构设计
**技能：** [`@brainstorming`](../../skills/brainstorming/)

**任务：** "使用 @brainstorming 设计SaaS MVP架构，包括：
- 核心功能识别
- 技术栈选择
- 数据库设计
- API端点规划
- 安全考虑"

**产出：** 架构设计文档和功能列表

---

### 步骤2：UI/UX设计
**技能：** [`@frontend-design`](../../skills/frontend-design/)

**任务：** "使用 @frontend-design 为核心功能设计用户界面，包括：
- 用户注册/登录流程
- 主要功能页面布局
- 响应式设计
- 无障碍考虑"

**产出：** UI设计规范和线框图

---

### 步骤3：安全架构
**技能：** [`@security-audit`](../../skills/security-audit/)

**任务：** "使用 @security-audit 为SaaS设计安全架构，包括：
- 身份验证和授权
- 数据保护
- API安全
- 合规要求（GDPR等）"

**产出：** 安全设计文档和威胁模型

---

### 步骤4：数据库设计
**技能：** [`@schema-design`](../../skills/schema-design/)

**任务：** "使用 @schema-design 设计数据库模式，包括：
- 用户和权限表
- 核心业务数据表
- 索引策略
- 数据迁移计划"

**产出：** 完整的数据库模式和迁移脚本

---

### 步骤5：API开发
**技能：** [`@api-design`](../../skills/api-design/)

**任务：** "使用 @api-design 开发RESTful API，包括：
- 认证端点
- 核心功能CRUD操作
- 错误处理
- API文档生成"

**产出：** 完整的API实现和OpenAPI文档

---

### 步骤6：前端开发
**技能：** [`@react-patterns`](../../skills/react-patterns/)

**任务：** "使用 @react-patterns 构建前端应用，包括：
- 组件架构
- 状态管理
- 路由设计
- 性能优化"

**产出：** 生产就绪的前端应用

---

### 步骤7：测试策略
**技能：** [`@test-driven-development`](../../skills/test-driven-development/)

**任务：** "使用 @test-driven-development 为SaaS实施测试，包括：
- 单元测试
- 集成测试
- 端到端测试
- 性能测试"

**产出：** 完整的测试套件和CI/CD配置

---

### 步骤8：部署配置
**技能：** [`@docker-expert`](../../skills/docker-expert/)

**任务：** "使用 @docker-expert 配置生产部署，包括：
- 容器化配置
- Docker Compose编排
- 环境变量管理
- 健康检查"

**产出：** 部署配置和基础设施即代码

---

### 步骤9：性能优化
**技能：** [`@performance-analyzer`](../../skills/performance-analyzer/)

**任务：** "使用 @performance-analyzer 优化SaaS性能，包括：
- 数据库查询优化
- 前端资源优化
- 缓存策略
- 监控设置"

**产出：** 性能优化报告和监控仪表板

---

### 步骤10：发布准备
**技能：** [`@deployment-pipeline`](../../skills/deployment-pipeline/)

**任务：** "使用 @deployment-pipeline 准备生产发布，包括：
- 发布流程设计
- 回滚策略
- 监控告警
- 用户文档"

**产出：** 生产就绪的发布计划

---

## 工作流：Web应用安全审计

对现有Web应用进行全面安全评估。

### 步骤1：初步侦察
**技能：** [`@reconnaissance`](../../skills/reconnaissance/)

**任务：** "使用 @reconnaissance 收集目标信息，包括：
- 技术栈识别
- 子域名枚举
- 端口扫描
- 公开信息收集"

**产出：** 目标信息收集报告

---

### 步骤2：漏洞扫描
**技能：** [`@vulnerability-scanner`](../../skills/vulnerability-scanner/)

**任务：** "使用 @vulnerability-scanner 进行自动扫描，包括：
- 依赖漏洞检查
- 配置安全检查
- 已知漏洞扫描
- 错误配置检测"

**产出：** 自动扫描结果报告

---

### 步骤3：手动渗透测试
**技能：** [`@pen-testing`](../../skills/pen-testing/)

**任务：** "使用 @pen-testing 进行手动测试，包括：
- SQL注入测试
- XSS漏洞测试
- CSRF测试
- 认证绕过测试"

**产出：** 手动渗透测试报告

---

### 步骤4：API安全测试
**技能：** [`@api-security-testing`](../../skills/api-security-testing/)

**任务：** "使用 @api-security-testing 测试API安全，包括：
- 认证授权测试
- 输入验证测试
- 速率限制测试
- 敏感数据泄露测试"

**产出：** API安全测试报告

---

### 步骤5：业务逻辑测试
**技能：** [`@business-logic-testing`](../../skills/business-logic-testing/)

**任务：** "使用 @business-logic-testing 测试业务逻辑，包括：
- 权限提升测试
- 价格操纵测试
- 工作流程绕过
- 数据完整性测试"

**产出：** 业务逻辑安全报告

---

### 步骤6：社会工程测试
**技能：** [`@social-engineering-testing`](../../skills/social-engineering-testing/)

**任务：** "使用 @social-engineering-testing 进行社会工程测试，包括：
- 钓鱼邮件测试
- 员工安全意识测试
- 物理安全测试（如适用）
- 安全培训效果评估"

**产出：** 社会工程测试报告

---

### 步骤7：报告和建议
**技能：** [`@security-reporting`](../../skills/security-reporting/)

**任务：** "使用 @security-reporting 生成综合报告，包括：
- 风险等级评估
- 漏洞详细说明
- 修复建议
- 安全加固指南"

**产出：** 完整的安全审计报告

---

## 工作流：AI应用开发

开发一个完整的AI驱动应用。

### 步骤1：AI策略规划
**技能：** [`@ai-strategy`](../../skills/ai-strategy/)

**任务：** "使用 @ai-strategy 规划AI应用，包括：
- AI模型选择
- 数据需求分析
- 性能指标定义
- 伦理考虑"

**产出：** AI策略文档

---

### 步骤2：数据工程
**技能：** [`@data-engineering`](../../skills/data-engineering/)

**任务：** "使用 @data-engineering 准备数据，包括：
- 数据收集策略
- 清洗和预处理
- 数据管道构建
- 数据质量管理"

**产出：** 数据管道和预处理脚本

---

### 步骤3：模型开发
**技能：** [`@model-development`](../../skills/model-development/)

**任务：** "使用 @model-development 开发AI模型，包括：
- 模型架构设计
- 训练流程实现
- 模型评估
- 超参数调优"

**产出：** 训练好的模型和评估报告

---

### 步骤4：提示工程
**技能：** [`@prompt-engineer`](../../skills/prompt-engineer/)

**任务：** "使用 @prompt-engineer 优化AI交互，包括：
- 提示模板设计
- 上下文管理
- 输出格式控制
- 错误处理"

**产出：** 提示模板和对话管理系统

---

### 步骤5：RAG系统构建
**技能：** [`@rag-engineer`](../../skills/rag-engineer/)

**任务：** "使用 @rag-engineer 构建RAG系统，包括：
- 向量数据库设置
- 检索策略设计
- 生成增强
- 评估指标"

**产出：** 完整的RAG系统

---

### 步骤6：应用集成
**技能：** [`@ai-integration`](../../skills/ai-integration/)

**任务：** "使用 @ai-integration 集成AI到应用，包括：
- API端点设计
- 错误处理机制
- 缓存策略
- 监控设置"

**产出：** 生产就绪的AI应用

---

## 工作流：全栈项目重构

重构遗留的全栈应用。

### 步骤1：代码审计
**技能：** [`@code-audit`](../../skills/code-audit/)

**任务：** "使用 @code-audit 审计现有代码，包括：
- 代码质量评估
- 性能瓶颈识别
- 安全漏洞检查
- 技术债务分析"

**产出：** 代码审计报告

---

### 步骤2：重构规划
**技能：** [`@refactoring-planning`](../../skills/refactoring-planning/)

**任务：** "使用 @refactoring-planning 制定重构计划，包括：
- 优先级排序
- 风险评估
- 时间线规划
- 资源分配"

**产出：** 重构执行计划

---

### 步骤3：数据库重构
**技能：** [`@database-refactoring`](../../skills/database-refactoring/)

**任务：** "使用 @database-refactoring 重构数据库，包括：
- 模式优化
- 索引重建
- 查询优化
- 迁移脚本"

**产出：** 优化后的数据库和迁移脚本

---

### 步骤4：后端重构
**技能：** [`@backend-refactoring`](../../skills/backend-refactoring/)

**任务：** "使用 @backend-refactoring 重构后端，包括：
- 架构现代化
- 代码清理
- 性能优化
- 测试补全"

**产出：** 重构后的后端代码

---

### 步骤5：前端重构
**技能：** [`@frontend-refactoring`](../../skills/frontend-refactoring/)

**任务：** "使用 @frontend-refactoring 重构前端，包括：
- 组件重构
- 状态管理优化
- 性能提升
- 用户体验改进"

**产出：** 重构后的前端代码

---

### 步骤6：测试验证
**技能：** [`@testing-verification`](../../skills/testing-verification/)

**任务：** "使用 @testing-verification 验证重构，包括：
- 回归测试
- 性能对比
- 安全验证
- 用户验收测试"

**产出：** 验证测试报告

---

## 💡 工作流最佳实践

### 📋 使用原则

1. **按顺序执行：** 不要跳过步骤，每个步骤都依赖前一步的产出
2. **保存成果：** 每个步骤的输出都是下一步的重要输入
3. **迭代改进：** 根据实际情况调整工作流
4. **团队协作：** 分配不同步骤给不同专业角色

### 🔄 自定义工作流

**创建自定义工作流：**
1. 明确目标和成果
2. 选择合适的技能组合
3. 设计步骤顺序
4. 定义每个步骤的产出要求
5. 测试和优化

### 🎯 工作流选择指南

| 项目类型 | 推荐工作流 | 关键技能 |
| :------- | :----------- | :------- |
| **新SaaS产品** | Ship a SaaS MVP | 架构、安全、部署 |
| **安全审计** | Web应用安全审计 | 渗透测试、漏洞扫描 |
| **AI项目** | AI应用开发 | 模型开发、RAG工程 |
| **代码重构** | 全栈项目重构 | 代码审计、重构策略 |
| **移动应用** | 移动应用开发 | React Native、移动安全 |

---

## 🆘 获取帮助

### ❓ 常见问题

**Q: 可以跳过某些步骤吗？**
A: 不建议。每个步骤都为后续步骤提供必要基础。

**Q: 工作流需要多长时间？**
A: 根据项目复杂度，从几天到几个月不等。

**Q: 可以并行执行步骤吗？**
A: 部分步骤可以并行，但需确保依赖关系。

### 📚 更多资源

- 📋 [技能包](bundles.md) - 按角色选择技能
- 📖 [使用指南](usage.md) - 详细使用说明
- ❓ [常见问题](faq.md) - 答疑解惑
- 🤝 [社区讨论](https://github.com/sickn33/antigravity-awesome-skills/discussions) - 经验分享

---

## 🎉 开始使用工作流

现在您有了完整的工作流指南：

1. **选择工作流**符合您的项目需求
2. **按步骤执行**每个阶段的任务
3. **保存每个产出**用于后续步骤
4. **团队协作**提高效率

**立即开始：**

```bash
"根据我的项目需求，使用最合适的工作流开始工作！"
```

祝您项目成功！🚀