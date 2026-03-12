# Antigravity Awesome Skills 入门指南 (V7.0.0)

**新手？本指南将帮助您在5分钟内增强您的AI代理。**

> **💡 安装后不知道该做什么？** 查看[**完整使用指南**](usage.md)获取详细解释和示例！

---

## 🤔 什么是"技能"？

AI代理（如**Claude Code**、**Gemini**、**Cursor**）很智能，但它们缺乏关于您的工具的特定知识。
**技能**是专门的指导手册（markdown文件），可以教您的AI每次都完美地执行特定任务。

**类比：** 您的AI是一个出色的实习生。**技能**是SOP（标准操作程序），能让它们成为高级工程师。

---

## ⚡️ 快速开始："入门包"

不要为1,200+个技能而焦虑。您不需要一次性全部使用它们。
我们精心准备了**入门包**让您立即运行起来。

您**安装一次完整仓库**（npx或克隆）；入门包是精选列表，帮助您**按角色选择要使用的技能**（例如Web向导、黑客包）——它们不是不同的安装方式。

### 1. 安装仓库

**选项A — npx（最简单）：**

```bash
npx antigravity-awesome-skills
```

默认情况下克隆到`~/.gemini/antigravity/skills`。使用`--cursor`、`--claude`、`--gemini`、`--codex`或`--kiro`为特定工具安装，或使用`--path <dir>`自定义位置。运行`npx antigravity-awesome-skills --help`查看详情。

如果看到404错误，使用：`npx github:sickn33/antigravity-awesome-skills`

**选项B — git克隆：**

```bash
# 通用（适用于大多数代理）
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

### 2. 选择您的角色

找到与您角色匹配的包（参见[bundles.md](bundles.md)）：

| 角色                | 包名         | 包含内容                                     |
| :----------------- | :----------- | :------------------------------------------- |
| **Web开发者**      | `Web向导`   | React模式、Tailwind精通、前端设计            |
| **黑客**           | `黑客包`     | 渗透测试、安全审计、漏洞分析                |
| **AI开发者**       | `AI构建者`  | LangGraph、RAG、提示工程                    |
| **安全工程师**      | `安全专家`   | OWASP检查、代码审计、事件响应                |
| **全栈开发者**     | `全栈大师`  | API设计、数据库模式、部署流程                |
| **产品经理**       | `产品领导者` | 用户故事、路线图、市场分析                  |
| **DevOps工程师**    | `运维专家`   | Docker、Kubernetes、CI/CD、监控             |

### 3. 开始使用

只需在对话中自然地提及技能：

```bash
用户："使用 @react-patterns 构建一个带有身份验证的仪表板组件"
用户："使用 @security-audit 检查这个Node.js应用"
用户："使用 @prompt-engineer 为图像生成API优化提示"
```

您的AI会自动加载技能并遵循其指导。

---

## 🎯 技能使用场景

### 开发工作流示例

**构建SaaS MVP：**
```bash
# 第1步：架构规划
"使用 @brainstorming 设计微服务架构"

# 第2步：前端开发
"使用 @react-patterns 构建用户界面"

# 第3步：后端API
"使用 @api-design 创建RESTful端点"

# 第4步：安全审计
"使用 @security-audit 扫描漏洞"

# 第5步：部署
"使用 @k8s-deployment 部署到Kubernetes"
```

### 技能选择模式

| 场景                   | 推荐技能                                      |
| :--------------------- | :-------------------------------------------- |
| **编写文档**           | `@doc-coauthoring`, `@technical-writing`      |
| **代码审查**           | `@code-reviewer`, `@security-review`          |
| **性能优化**           | `@performance-analyzer`, `@optimization`       |
| **调试复杂问题**       | `@debugging`, `@root-cause-tracing`          |
| **API设计**           | `@api-design`, `@openapi-spec`               |
| **数据库设计**         | `@schema-design`, `@query-optimization`      |

---

## 🔧 高级用法

### 组合使用技能

技能可以组合使用：

```bash
"使用 @react-patterns 和 @tailwind-mastery 构建响应式组件，
然后用 @test-driven-development 编写测试"
```

### 上下文注入

为技能提供特定上下文：

```bash
"使用 @security-audit 检查这个电商API：
- 处理支付信息
- 需要GDPR合规
- 使用JWT认证"
```

### 技能发现

不知道用什么技能？询问您的AI：

```bash
"我需要优化这个React应用的性能，
有哪些相关的技能？"
```

---

## 💡 最佳实践

### 新手建议

1. **从小开始**：选择3-5个与您工作最相关的技能
2. **按需学习**：遇到问题时搜索相关技能
3. **逐步扩展**：随着使用深入了解更多技能

### 高级用户

1. **自定义技能**：基于现有模板创建专属技能
2. **工作流优化**：组合技能形成标准化流程
3. **团队共享**：在团队中推广有效技能组合

### 常见陷阱

**避免这些错误：**

❌ "我需要学习所有1200个技能"
✅ "我需要掌握当前任务相关的5个核心技能"

❌ "这个技能不够完美"
✅ "这个技能解决了80%的问题，我可以优化剩下的20%"

---

## 🆘 需要帮助？

### 快速问题检查

- **技能未找到？** → 确认安装路径正确
- **效果不理想？** → 尝试提供更具体的上下文
- **不知道用什么技能？** → 询问您的AI："我正在[任务]，有什么推荐的技能吗？"

### 社区支持

- 📖 [完整使用指南](usage.md) - 详细说明和示例
- 📋 [常见问题](faq.md) - 答疑解惑
- 🎯 [技能包指南](bundles.md) - 按角色组织
- 👥 [社区讨论](https://github.com/sickn33/antigravity-awesome-skills/discussions) - 与其他用户交流

### 技术支持

- 🐛 [报告问题](https://github.com/sickn33/antigravity-awesome-skills/issues) - 发现bug请报告
- 💡 [功能建议](https://github.com/sickn33/antigravity-awesome-skills/issues/new?template=feature_request.md) - 建议新功能
- 🤝 [贡献技能](../CONTRIBUTING.md) - 帮助改进项目

---

## 🎉 下一步

恭喜！您现在掌握了：

✅ 理解技能是什么以及如何工作  
✅ 安装了技能仓库  
✅ 选择了适合您角色的入门包  
✅ 学会了基本的技能使用方法  

**继续学习：**
- 📖 [完整使用指南](usage.md) - 深入了解所有功能
- 🎯 [技能包](bundles.md) - 探索更多专业技能组合
- 🔧 [本地配置](local-config.md) - 自定义您的设置

**开始您的第一个技能会话：**

```bash
"使用 @brainstorming 规划我的下一个项目"
```

祝您使用愉快！🚀