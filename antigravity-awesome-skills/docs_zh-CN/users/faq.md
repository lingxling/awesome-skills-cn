# ❓ 常见问题解答 (FAQ)

**有疑问？** 您不是一个人！以下是关于Antigravity Awesome Skills最常见问题的答案。

---

## 🎯 一般问题

### 技能到底是什么？

技能是专门的指导文件，用于教AI助手如何处理特定任务。可以将它们看作是您的AI可以按需加载的专家知识模块。
**简单类比：** 就像您可能会咨询不同的专家（律师、医生、机械师）一样，这些技能让您的AI在需要时成为不同领域的专家。

### 我需要安装所有1,204+个技能吗？

**不需要！** 当您克隆仓库时，所有技能都可用，但您的AI只在您用`@skill-name`明确调用它们时才加载。
这就像拥有一座图书馆 - 所有书都在那里，但您只读需要的那些。
**专业提示：** 使用[入门包](bundles.md)只安装与您角色匹配的内容。

### 包和工作流有什么区别？

- **包**是按角色或领域分组的精选推荐。
- **工作流**是为具体结果编写的有序执行手册。

当您决定包含_哪些技能_时使用包。当您需要_逐步执行_时使用工作流。

从这里开始：

- [bundles.md](bundles.md)
- [workflows.md](workflows.md)

### 哪些AI工具支持这些技能？

- ✅ **Claude Code** (Anthropic CLI)
- ✅ **Gemini CLI** (Google)
- ✅ **Codex CLI** (OpenAI)
- ✅ **Cursor** (AI IDE)
- ✅ **Antigravity IDE**
- ✅ **OpenCode**
- ⚠️ **GitHub Copilot** (通过复制粘贴部分支持)

### 这些技能免费吗？

**是的！** 这个项目完全开源免费。所有技能都可以免费使用、修改和分发。

---

## 🔧 安装和设置

### 如何安装技能？

**选项1 - npx（推荐）：**
```bash
npx antigravity-awesome-skills
```

**选项2 - git克隆：**
```bash
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

详细说明请参见[入门指南](getting-started.md)。

### 安装到哪个位置？

**默认位置：**
- Antigravity: `~/.gemini/antigravity/skills/`
- 其他工具: `~/.agent/skills/`

**自定义位置：**
```bash
npx antigravity-awesome-skills --path /custom/path/skills
```

### Windows用户需要特殊设置吗？

是的，Windows用户需要：

1. **启用开发者模式**或以管理员身份运行
2. **使用正确的克隆命令：**
```bash
git clone -c core.symlinks=true https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

### 如何更新技能？

```bash
cd ~/.gemini/antigravity/skills  # 或您的安装路径
git pull
```

或重新运行安装程序：
```bash
npx antigravity-awesome-skills
```

---

## 💬 使用问题

### AI说找不到技能怎么办？

**检查清单：**
1. ✅ 确认安装路径正确
2. ✅ 确认技能文件存在
3. ✅ 确认语法正确（`@skill-name`）
4. ✅ 确认AI工具支持技能功能

**诊断命令：**
```bash
# 检查安装
ls ~/.gemini/antigravity/skills/

# 查看可用技能
ls ~/.gemini/antigravity/skills/*/SKILL.md | head -10
```

### 技能效果不理想怎么办？

**常见原因和解决方案：**

1. **缺少上下文**
   - ❌ "使用@api-design设计API"
   - ✅ "使用@api-design设计用户管理API，需要JWT认证"

2. **技能不匹配**
   - ❌ 用通用技能处理专门问题
   - ✅ 使用更具体的技能（如`@sql-injection-testing`而不是`@security-audit`）

3. **提示太模糊**
   - ❌ "优化这个代码"
   - ✅ "使用@performance-analyzer优化这个React组件的渲染性能"

### 可以同时使用多个技能吗？

**当然可以！** 事实上，组合使用是最佳实践：

```bash
"使用@react-patterns构建组件，然后用@test-driven-development编写测试"
```

### 如何知道该用哪个技能？

**方法1：直接询问**
```bash
"我需要优化数据库查询，有什么推荐技能？"
```

**方法2：浏览包**
查看[bundles.md](bundles.md)中您的角色相关技能。

**方法3：按任务查找**
- 安全相关 → `@security-audit`, `@pen-testing`, `@vulnerability-scanner`
- 性能优化 → `@performance-analyzer`, `@optimization`
- API开发 → `@api-design`, `@openapi-spec`
- 前端开发 → `@react-patterns`, `@tailwind-mastery`

---

## 🛠️ 高级问题

### 可以自定义技能吗？

**可以！** 详细步骤：

1. **复制现有技能模板**
2. **修改内容**以符合您的需求
3. **测试技能**确保工作正常
4. **贡献给社区**（可选）

详细指南请参见[贡献文档](../../CONTRIBUTING.md)。

### 技能可以离线使用吗？

**是的！** 一旦安装，所有技能都在本地，无需网络连接。

### 技能会访问外部API吗？

**通常不会。** 大部分技能是基于知识的指导。少数特殊技能（如web抓取）会使用外部API，但会在技能描述中明确说明。

### 如何贡献新技能？

**贡献流程：**
1. Fork仓库
2. 创建技能目录和SKILL.md文件
3. 遵循[技能模板](../contributors/skill-template.md)
4. 运行验证：`npm run validate`
5. 提交Pull Request

详细指南请参见[贡献指南](../../CONTRIBUTING.md)。

---

## 🔄 更新和维护

### 多久更新一次技能？

**不定期更新。** 当有：
- 新技能添加
- 现有技能改进
- 错误修复
- 安全更新

**如何保持更新：**
```bash
# 每周更新一次
cd ~/.gemini/antigravity/skills
git pull

# 或重新安装
npx antigravity-awesome-skills
```

### 如何报告技能问题？

**报告步骤：**
1. 在GitHub上创建[issue](https://github.com/sickn33/antigravity-awesome-skills/issues)
2. 详细描述问题
3. 提供示例
4. 标明技能名称

### 更新时会发生什么？

**安全更新：** 您的更改会被保留
**重大更新：** 可能需要手动合并

建议：如果您有自定义修改，请在更新前备份。

---

## 🎯 特定工具问题

### Claude Code特定问题

**语法：** `> 使用 @skill-name 做某事`

**常见问题：**
- 忘记`>`前缀
- 技能名称拼写错误
- 使用了错误的分隔符（应该是`@`，不是`#`）

### Gemini CLI特定问题

**语法：** 在消息中提及技能名称

**示例：**
```bash
"使用 security-audit 检查这个代码"
```

### Cursor特定问题

**语法：** `@skill-name`

**注意：** 确保在聊天窗口中使用，不是在代码编辑器中。

### GitHub Copilot特定问题

**限制：** 不直接支持，需要复制粘贴

**变通方法：**
1. 复制技能内容
2. 粘贴到Copilot聊天
3. 添加您的具体问题

---

## 📊 性能和规模

### 技能会影响AI响应速度吗？

**轻微影响。** 加载技能需要额外时间，但通常值得：

- **简单技能：** 几乎没有延迟
- **复杂技能：** 额外1-3秒
- **组合技能：** 按技能数量线性增加

### 有多少技能？

**当前统计：**
- 总技能数：1,204+
- 分类数：8个主要类别
- 语言：主要是英语
- 维护者：50+贡献者

### 技能有多大？

**大小范围：**
- 小技能：< 1KB
- 中等技能：1-10KB
- 大技能：> 10KB（通常包含代码示例）

**总仓库大小：** ~50MB

---

## 🔒 安全和隐私

### 技能会收集我的数据吗？

**不会。** 技能是静态markdown文件，不包含任何数据收集代码。

### 技能安全吗？

**审核过程：**
1. 社区审核
2. 自动化验证
3. 安全扫描
4. 手工检查

**报告安全问题：**
- 📧 security@antigravity-skills.org
- 🔒 [私有报告](https://github.com/sickn33/antigravity-awesome-skills/security/advisories)

### 企业环境可以使用吗？

**可以。** 建议：
1. 在私有环境中部署
2. 审核所有技能内容
3. 建立内部技能库
4. 定期更新

---

## 🆘 获取帮助

### 社区资源

- 📋 [GitHub讨论](https://github.com/sickn33/antigravity-awesome-skills/discussions) - 与用户交流
- 🐛 [问题报告](https://github.com/sickn33/antigravity-awesome-skills/issues) - 报告bug
- 💡 [功能建议](https://github.com/sickn33/antigravity-awesome-skills/issues/new?template=feature_request.md) - 建议改进
- 📖 [完整文档](https://github.com/sickn33/antigravity-awesome-skills/tree/main/docs) - 深入学习

### 联系方式

- 📧 Email: support@antigravity-skills.org
- 💬 Discord: [邀请链接](https://discord.gg/antigravity)
- 🐦 Twitter: @antigravity_ai

### 常用链接

- 📚 [入门指南](getting-started.md) - 新手必读
- 🎯 [技能包](bundles.md) - 按角色选择
- 🔧 [使用指南](usage.md) - 详细说明
- 🤝 [贡献指南](../../CONTRIBUTING.md) - 参与贡献

---

## 🎉 结语

我们希望这个FAQ解答了您的疑问！如果您有任何其他问题，请不要犹豫：

1. **搜索现有讨论** - 您的问题可能已被回答
2. **在GitHub上提问** - 社区很乐意帮助
3. **加入Discord** - 实时交流

记住，使用技能的最佳方式是：**开始简单，逐步深入，持续改进**。

祝您使用愉快！🚀