# 发布流程

这是维护者的仓库发布操作手册。历史发布记录在[`CHANGELOG.md`](../../CHANGELOG.md)中；本文档记录可重复的流程。

## 前置条件

- 工作目录是干净的，或者您已经明确隔离了发布更改。
- `package.json`包含您打算发布的版本。
- 生成的注册表文件已同步。
- README统计、徽章和致谢是最新的。

## 发布检查清单

### 1. 运行操作验证套件：

```bash
npm run validate
npm run validate:references
npm run sync:all
npm run test
npm run app:build
```

### 2. 可选的强化检查：

```bash
npm run validate:strict
```

将其用作诊断信号。它有助于发现历史质量债务，但目前还不是整个仓库的发布阻止因素。

### 3. 更新版本号：

```bash
# 更新package.json中的版本
npm version patch|minor|major

# 或手动更新为特定版本
npm version 1.2.3
```

### 4. 生成变更日志：

```bash
npm run changelog
```

审查生成的变更日志，确保：
- 所有重要更改都已记录
- 版本号正确
- 破坏性变更已标记
- 新功能已突出显示

### 5. 更新文档：

```bash
npm run readme
npm run catalog
```

验证：
- README中的技能数量正确
- 新技能已分类
- 示例代码可运行
- 链接有效

### 6. 运行完整测试套件：

```bash
npm run test:ci
```

确保：
- 所有测试通过
- 代码覆盖率达标
- 安全检查通过
- 性能基准稳定

### 7. 创建发布分支：

```bash
git checkout -b release/vX.X.X
```

### 8. 提交所有更改：

```bash
git add .
git commit -m "chore: prepare release v$VERSION"
```

### 9. 创建标签：

```bash
git tag -a v$VERSION -m "Release v$VERSION"
```

### 10. 推送更改和标签：

```bash
git push origin main
git push origin release/vX.X.X
git push origin v$VERSION
```

## 发布后操作

### 1. 合并发布分支：

```bash
git checkout main
git merge release/vX.X.X
git push origin main
```

### 2. 发布到NPM：

```bash
npm publish
```

### 3. 创建GitHub Release：

- 访问 [GitHub Releases页面](https://github.com/sickn33/antigravity-awesome-skills/releases)
- 点击"Create a new release"
- 选择刚推送的标签
- 粘贴变更日志内容
- 添加发布说明
- 点击"Publish release"

### 4. 更新网站和文档：

```bash
npm run deploy:docs
npm run deploy:web
```

### 5. 社区公告：

#### Discord公告：
```text
🎉 Antigravity Awesome Skills v$VERSION 已发布！

主要更新：
• [关键更新1]
• [关键更新2]
• [关键更新3]

获取更新：npx antigravity-awesome-skills

详情：[GitHub Release链接]
```

#### Twitter公告：
```text
🚀 Antigravity Awesome Skills v$VERSION 发布了！

[最激动人心的新功能]

立即更新：npx antigravity-awesome-skills

#AI #Skills #ClaudeCode #Gemini
```

#### 博客文章：
- 撰写详细的发布说明
- 包含新功能示例
- 添加迁移指南
- 分享最佳实践

## 紧急发布流程

### 何时需要紧急发布：

- 关键安全漏洞修复
- 生产环境破坏性bug
- 重大安装问题

### 紧急发布步骤：

1. **立即修复**
   ```bash
   git checkout -b hotfix/issue-description
   # 实施修复
   npm test
   ```

2. **快速验证**
   ```bash
   npm run validate:quick
   ```

3. **发布修复**
   ```bash
   npm version patch
   git tag v$VERSION
   git push origin v$VERSION
   npm publish
   ```

4. **通知社区**
   - Discord紧急通知
   - GitHub Issue说明
   - Twitter安全公告

## 版本控制策略

### 语义化版本控制

遵循[SemVer](https://semver.org/)规范：

- **主版本号（MAJOR）**：不兼容的API更改
- **次版本号（MINOR）**：向后兼容的功能添加
- **修订号（PATCH）**：向后兼容的问题修复

### 版本号格式

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

示例：
- `1.0.0` - 稳定发布
- `1.0.0-alpha.1` - Alpha版本
- `1.0.0-beta.2` - Beta版本
- `1.0.0-rc.3` - 候选版本

### 发布周期

- **主版本**：每3-6个月
- **次版本**：每月
- **修订版本**：根据需要（bug修复）

## 质量门禁

### 发布前检查

**必须通过：**
- [ ] 所有自动化测试通过
- [ ] 代码覆盖率 > 80%
- [ ] 安全扫描无高危漏洞
- [ ] 性能测试无回归
- [ ] 文档生成成功
- [ ] 技能验证通过

**可选通过：**
- [ ] 严格验证通过
- [ ] 手动QA验证
- [ ] 社区反馈收集

### 发布后监控

**监控指标：**
- NPM下载量
- GitHub Stars
- 社区反馈
- 错误报告
- 性能指标

**告警阈值：**
- 下载量下降 > 20%
- 错误率上升 > 5%
- 社区投诉 > 10条

## 回滚程序

### 何时回滚

- 安装失败率 > 10%
- 关键功能破坏
- 安全问题发现
- 用户大量投诉

### 回滚步骤

1. **立即停止推广**
   - 撤下发布说明
   - 更新Discord状态
   - 暂停Twitter宣传

2. **创建回滚分支**
   ```bash
   git checkout -b rollback/v$VERSION
   git revert $MERGE_COMMIT
   ```

3. **发布回滚版本**
   ```bash
   npm version patch
   git tag v$ROLLBACK_VERSION
   npm publish
   ```

4. **社区通知**
   ```text
   🚨 v$VERSION 紧急回滚
   
   问题：[问题描述]
   解决：[回滚版本 v$ROLLBACK_VERSION]
   
   建议：暂缓更新或使用 --version $ROLLBACK_VERSION
   ```

## 工具和自动化

### 发布脚本

```bash
#!/bin/bash
# release.sh - 自动化发布脚本

set -e

VERSION=$(node -p "require('./package.json').version")
echo "🚀 发布版本 v$VERSION"

# 运行检查
npm run validate
npm run test

# 更新文档
npm run readme
npm run catalog

# 创建发布
git add .
git commit -m "chore: release v$VERSION"
git tag -a v$VERSION -m "Release v$VERSION"

# 推送
git push origin main
git push origin v$VERSION

# 发布到NPM
npm publish

echo "✅ 发布成功 v$VERSION"
```

### 持续集成配置

**GitHub Actions工作流：**
```yaml
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm test
      - run: npm publish
```

## 贡献者认可

### 发布致谢

在每个发布中感谢贡献者：

```markdown
## 贡献者

特别感谢本版本的贡献者：
- @username - [主要贡献]
- @username2 - [主要贡献]
- @username3 - [主要贡献]

以及所有报告问题和反馈的用户！
```

### 奖励机制

- 🏆 **月度贡献者** - Discord特别角色
- 🎁 **发布贡献者** - 项目商品
- 📝 **技术写作奖** - 优秀文档奖
- 🌟 **新星奖** - 新贡献者鼓励

## 文档和培训

### 维护者培训

**新维护者入职：**
1. 阅读完整的维护者文档
2. 观摩一次完整的发布流程
3. 在监督下进行一次发布
4. 独立执行发布（有回滚支持）

### 技能文档

**必备文档：**
- 发布流程检查清单
- 紧急响应程序
- 工具使用指南
- 常见问题解答

**可选文档：**
- 高级故障排除
- 性能优化指南
- 社区管理最佳实践

---

## 🎉 成功发布指标

### 发布成功标志

- ✅ 所有自动化检查通过
- ✅ 社区反馈积极
- ✅ 下载量稳步增长
- ✅ 错误率在可接受范围内
- ✅ 文档完整准确

### 持续改进

每次发布后进行：
- 📊 性能分析
- 📋 用户反馈收集
- 🔄 流程优化
- 📚 文档更新
- 🎯 目标调整

---

这个发布流程确保Antigravity Awesome Skills的质量、稳定性和社区满意度。通过遵循这些指导方针，我们能够为用户提供可靠、高质量的技能生态。

如果您有任何问题或建议，请随时联系维护团队。🚀