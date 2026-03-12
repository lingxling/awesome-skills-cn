# 📖 使用指南：如何实际使用这些技能

> **安装后感到困惑？** 本指南逐步指导您下一步该做什么。

---

## 🤔 "我刚安装了仓库。现在该做什么？"

好问题！以下是刚刚发生的事情以及下一步该怎么做：

### 您刚刚做了什么

当您运行`npx antigravity-awesome-skills`或克隆仓库时，您：

✅ **下载了1,204+个技能文件**到您的计算机（默认：`~/.gemini/antigravity/skills/`；如果使用`--path`则是`~/.agent/skills/`）  
✅ **使它们对您的AI助手可用**  
❌ **没有自动启用它们**（它们就在那里，等待使用）

可以把它想象成安装一个工具箱。您现在拥有所有工具，但您需要为每个工作**选择使用哪些工具**。

---

## 🎯 第1步：理解"包"（这不是另一个安装！）

**常见困惑：**"我需要单独下载每个技能吗？"

**答案：不需要！** 以下是包的实际含义：

### 包是什么

- ✅ **按角色组织的推荐技能列表**（例如：Web向导、黑客包）
- ✅ **帮助您选择技能**的精选起点
- ✅ **发现相关技能**的省时快捷方式

### 包不是什么

- ❌ 单独的安装或下载
- ❌ 不同的git命令
- ❌ 需要您"激活"的东西

### 如何使用包

1. **查看[bundles.md](bundles.md)**浏览可用包
2. **找到匹配您角色的包**
3. **从该包中选择3-5个技能**开始使用
4. **在与AI的对话中引用它们**

**示例：**
```bash
# 您是Web开发者？
查看"Web向导"包，从React Patterns、Tailwind Mastery等开始

# 您是安全工程师？
查看"安全专家"包，从Security Audit、Pen Testing等开始
```

---

## 🎯 第2步：理解技能引用语法

不同的AI工具有不同的语法，但概念相同：

### Claude Code
```bash
> 使用 @skill-name 处理这个...
```

### Gemini CLI
```bash
(用户消息) 使用 skill-name 来...
```

### Cursor
```bash
@skill-name (在聊天中)
```

### Antigravity IDE
```bash
(代理模式) 使用 skill... 
```

### OpenCode
```bash
opencode run @skill-name
```

**关键点：** 您需要明确告诉AI使用哪个技能。它不会自动"知道"要使用哪个。

---

## 🎯 第3步：您的第一个技能会话

让我们走一遍完整示例：

### 场景：您需要审核一个React应用的安全性

**❌ 错误方式：**
```bash
用户："检查这个React应用的安全性"
```
→ AI会使用通用知识，可能错过具体检查项

**✅ 正确方式：**
```bash
用户："使用 @security-audit 检查这个React应用的安全性"
```
→ AI会加载security-audit技能并遵循其专门的安全检查清单

### 完整对话示例

```bash
用户："使用 @security-audit 审核这个电商React应用：

src/components/PaymentForm.tsx
[组件代码...]

src/components/UserAuth.tsx  
[组件代码...]"

AI："正在使用Security Audit技能进行审核...

🔍 开始安全审核清单...

✅ 认证：使用JWT，实现正确
✅ 输入验证：React Hook Form + Yup验证
⚠️ XSS防护：缺少DOMPurify，建议添加
⚠️ CSRF保护：需要在API端点实现

详细建议：
1. 安装DOMPurify: npm install dompurify
2. 在PaymentForm中添加：import DOMPurify from 'dompurify'
..."
```

---

## 🎯 第4步：掌握高级用法

### 1. 上下文注入

给技能提供特定背景信息：

```bash
"使用 @api-design 设计用户管理API：

要求：
- 需要JWT认证
- 支持分页和搜索
- 必须GDPR合规
- 使用TypeScript"
```

### 2. 技能组合

一次使用多个技能：

```bash
"使用 @react-patterns 构建用户资料页面，
然后用 @test-driven-development 编写测试，
最后用 @performance-analyzer 优化性能"
```

### 3. 迭代优化

逐步改进：

```bash
# 第一次
"使用 @prompt-engineer 优化这个提示：'写一个登录页面'"

# 第二次  
"使用 @prompt-engineer 进一步优化，目标：
- 转化率更高
- 适合移动端
- 包含错误处理"
```

---

## 🎯 第5步：发现合适的技能

### 方法1：直接询问

```bash
"我需要优化PostgreSQL查询性能，有什么相关技能？"
```

### 方法2：浏览包

查看[bundles.md](bundles.md)找到您的角色相关技能。

### 方法3：搜索常用技能

| 任务类别 | 常用技能 |
| :------- | :-------- |
| **前端开发** | `@react-patterns`, `@tailwind-mastery`, `@frontend-design` |
| **安全** | `@security-audit`, `@pen-testing`, `@vulnerability-scanner` |
| **API开发** | `@api-design`, `@openapi-spec`, `@rest-best-practices` |
| **数据库** | `@schema-design`, `@query-optimization`, `@database-audit` |
| **部署** | `@docker-expert`, `@k8s-deployment`, `@ci-cd-pipeline` |
| **文档** | `@doc-coauthoring`, `@technical-writing`, `@api-documentation` |
| **测试** | `@test-driven-development`, `@testing-patterns`, `@e2e-testing` |
| **性能** | `@performance-analyzer`, `@optimization`, `@profiling` |

---

## 🔧 故障排除

### 问题1：AI说找不到技能

**原因：** 技能未安装在正确位置

**解决：**
```bash
# 检查安装位置
ls ~/.gemini/antigravity/skills/  # 或您的自定义路径

# 重新安装
npx antigravity-awesome-skills --path ~/.agent/skills
```

### 问题2：技能效果不理想

**原因：** 缺少具体上下文

**解决：**
```bash
# ❌ 模糊请求
"使用 @api-design 设计API"

# ✅ 具体请求  
"使用 @api-design 设计用户管理API，需要：
- JWT认证
- 分页支持
- RESTful设计
- 错误处理"
```

### 问题3：不知道用哪个技能

**解决：**
```bash
"我需要[任务描述]，有什么推荐的技能吗？"

# 示例
"我需要重构这个遗留代码，有什么推荐的技能吗？"
```

### 问题4：技能回答太泛泛

**原因：** 可能技能不适合这个具体场景

**解决：**
1. **尝试更具体的技能**（如用`@sql-injection-testing`而不是`@security-audit`）
2. **组合多个技能**
3. **提供更多上下文**

---

## 💡 专业技巧

### 1. 建立"技能栈"

像技术栈一样，为每个项目建立技能栈：

```bash
# SaaS项目技能栈
@react-patterns + @api-design + @security-audit + @docker-expert

# 移动应用技能栈  
@react-native-patterns + @mobile-testing + @performance-analyzer

# 数据项目技能栈
@python-patterns + @data-visualization + @ml-model-development
```

### 2. 创建"工作流模板"

为重复任务创建模板：

```bash
# 新功能开发模板
"使用 @brainstorming 设计功能架构 → 使用 @react-patterns 实现前端 → 使用 @api-design 创建后端 → 使用 @test-driven-development 编写测试 → 使用 @performance-analyzer 优化"

# 安全审计模板  
"使用 @security-audit 进行初步扫描 → 使用 @vulnerability-scanner 深度检查 → 使用 @pen-testing 渗透测试 → 使用 @incident-response 制定响应计划"
```

### 3. 渐进式复杂度

从简单到复杂：

```bash
# 第1级：基础使用
"使用 @skill-name 处理这个"

# 第2级：上下文注入
"使用 @skill-name 处理这个，要求：..."

# 第3级：技能组合
"使用 @skill1 和 @skill2 一起处理..."

# 第4级：工作流编排
"按顺序使用这些技能：@skill1 → @skill2 → @skill3"
```

---

## 🎯 实际案例研究

### 案例1：快速原型开发

**场景：** 需要2小时内构建一个简单的CRUD应用

**技能组合：**
```bash
"使用 @brainstorming 设计数据库模式 → 使用 @api-design 快速生成CRUD端点 → 使用 @react-patterns 创建基础UI → 使用 @tailwind-mastery 美化界面"
```

**结果：** 1.5小时完成功能完整的应用

### 案例2：安全加固现有系统

**场景：** 需要对生产系统进行全面安全评估

**技能组合：**
```bash
"使用 @security-audit 进行基础检查 → 使用 @vulnerability-scanner 扫描依赖 → 使用 @pen-testing 进行渗透测试 → 使用 @incident-response 制定安全计划"
```

**结果：** 发现并修复了17个安全漏洞

### 案例3：性能优化

**场景：** React应用加载缓慢

**技能组合：**
```bash
"使用 @performance-analyzer 识别瓶颈 → 使用 @optimization 优化关键路径 → 使用 @profiling 深度分析 → 使用 @code-simplifier 重写低效代码"
```

**结果：** 页面加载时间从4.2秒降到1.1秒

---

## 🆘 获取帮助

### 常见问题快速解答

**Q: 技能可以用在哪些AI工具上？**
A: Claude Code、Gemini、Cursor、Antigravity、OpenCode、Codex等

**Q: 可以同时使用多个技能吗？**  
A: 可以，鼓励组合使用以获得最佳效果

**Q: 技能会更新吗？**
A: 会，运行`git pull`更新仓库获取最新技能

**Q: 可以自定义技能吗？**
A: 可以，参见贡献指南

### 社区资源

- 📋 [常见问题](faq.md) - 更多答疑
- 🎯 [技能包指南](bundles.md) - 发现更多技能
- 👥 [GitHub讨论](https://github.com/sickn33/antigravity-awesome-skills/discussions) - 与用户交流
- 🐛 [问题报告](https://github.com/sickn33/antigravity-awesome-skills/issues) - 报告问题

---

## 🎉 恭喜！您现在是技能专家

您已掌握：

✅ **理解技能系统** - 知道技能是什么以及如何工作  
✅ **掌握引用语法** - 能在不同AI工具中使用技能  
✅ **学会高级技巧** - 上下文注入、技能组合、工作流编排  
✅ **了解最佳实践** - 建立技能栈、创建模板、渐进式复杂度  

**下一步：**
- 🎯 探索[技能包](bundles.md)发现更多专业技能组合
- 🔧 配置[本地环境](local-config.md)优化体验
- 🤝 加入[社区](https://github.com/sickn33/antigravity-awesome-skills/discussions)与其他用户交流

**开始您的技能之旅：**

```bash
"使用您最需要的技能开始第一个任务吧！"
```

祝您使用愉快！🚀