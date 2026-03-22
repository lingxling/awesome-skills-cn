# AGENTS.md

本文件为在 `skills` CLI 代码库上工作的 AI 编程代理提供指导。

## 项目概述

`skills` 是开放代理技能生态系统的命令行工具。

## 命令

| 命令                       | 描述                                         |
| ----------------------------- | --------------------------------------------------- |
| `skills`                      | 显示包含可用命令的横幅                 |
| `skills add <pkg>`            | 从 git 仓库、URL 或本地路径安装技能 |
| `skills experimental_install` | 从 skills-lock.json 恢复技能                |
| `skills experimental_sync`    | 将技能从 node_modules 同步到代理目录       |
| `skills list`                 | 列出已安装的技能（别名：`ls`）                 |
| `skills check`                | 检查可用的技能更新                   |
| `skills update`               | 将所有技能更新到最新版本                |
| `skills init [name]`          | 创建新的 SKILL.md 模板                      |

别名：`skills a` 适用于 `add`。`skills i`、`skills install`（无参数）从 `skills-lock.json` 恢复。`skills ls` 适用于 `list`。`skills experimental_install` 从 `skills-lock.json` 恢复。`skills experimental_sync` 在 `node_modules` 中爬取技能。

## 架构

```
src/
├── cli.ts           # 主入口点，命令路由，init/check/update
├── cli.test.ts      # CLI 测试
├── add.ts           # 核心添加命令逻辑
├── add-prompt.test.ts # 添加提示行为测试
├── add.test.ts      # 添加命令测试
├── constants.ts      # 共享常量
├── find.ts           # 查找/搜索命令
├── list.ts          # 列出已安装技能命令
├── list.test.ts     # 列出命令测试
├── remove.ts         # 移除命令实现
├── remove.test.ts    # 移除命令测试
├── agents.ts        # 代理定义和检测
├── installer.ts     # 技能安装逻辑（符号链接/复制）+ listInstalledSkills
├── skills.ts        # 技能发现和解析
├── skill-lock.ts    # 全局锁文件管理 (~/.agents/.skill-lock.json)
├── local-lock.ts    # 本地锁文件管理 (skills-lock.json，已提交)
├── sync.ts          # 同步命令 - 在 node_modules 中爬取技能
├── source-parser.ts # 解析 git URL、GitHub 简写、本地路径
├── git.ts           # Git 克隆操作
├── telemetry.ts     # 匿名使用跟踪
├── types.ts         # TypeScript 类型
├── mintlify.ts      # Mintlify 技能获取（遗留）
├── plugin-manifest.ts # 插件清单发现支持
├── prompts/         # 交互式提示助手
│   └── search-multiselect.ts
├── providers/       # 远程技能提供者（GitHub、HuggingFace、Mintlify）
│   ├── index.ts
│   ├── registry.ts
│   ├── types.ts
│   ├── huggingface.ts
│   ├── mintlify.ts
│   └── wellknown.ts
├── init.test.ts     # Init 命令测试
└── test-utils.ts    # 测试工具

tests/
├── cross-platform-paths.test.ts # 跨平台路径规范化
├── full-depth-discovery.test.ts # --full-depth 技能发现测试
├── openclaw-paths.test.ts       # OpenClaw 特定路径测试
├── plugin-manifest-discovery.test.ts # 插件清单技能发现
├── sanitize-name.test.ts     # sanitizeName 测试（路径遍历防护）
├── skill-matching.test.ts    # filterSkills 测试（多词技能名称匹配）
├── source-parser.test.ts     # URL/路径解析测试
├── installer-symlink.test.ts # 符号链接安装测试
├── list-installed.test.ts    # 列出已安装技能测试
├── skill-path.test.ts        # 技能路径处理测试
├── wellknown-provider.test.ts # 知名提供者测试
├── xdg-config-paths.test.ts   # XDG 全局路径处理测试
└── dist.test.ts               # 构建分发测试
```

## 更新检查系统

### `skills check` 和 `skills update` 如何工作

1. 读取 `~/.agents/.skill-lock.json` 获取已安装的技能
2. 筛选具有 `skillFolderHash` 和 `skillPath` 的 GitHub 支持的技能
3. 对于每个技能，调用 `fetchSkillFolderHash(source, skillPath, token)`。可选的认证令牌来自 `GITHUB_TOKEN`、`GH_TOKEN` 或 `gh auth token` 以提高速率限制。
4. `fetchSkillFolderHash` 直接调用 GitHub Trees API（`/git/trees/<branch>?recursive=1` 用于 `main`，然后回退到 `master`）
5. 将最新的文件夹树 SHA 与锁文件 `skillFolderHash` 进行比较；不匹配意味着有可用更新
6. `skills update` 通过直接调用当前 CLI 入口点（`node <repo>/bin/cli.mjs add <source-tree-url> -g -y`）重新安装已更改的技能，以避免嵌套的 npm exec/npx 行为

### 锁文件兼容性

锁文件格式是 v3。关键字段：`skillFolderHash`（技能文件夹的 GitHub 树 SHA）。

如果读取的是较旧的锁文件版本，它将被清除。用户必须重新安装技能以填充新格式。

## 关键集成点

| 功能                    | 实现                                                |
| -------------------------- | ------------------------------------------------------------- |
| `skills add`               | `src/add.ts` - 完整实现                            |
| `skills experimental_sync` | `src/sync.ts` - 爬取 node_modules                            |
| `skills check`             | `src/cli.ts` + `src/skill-lock.ts` 中的 `fetchSkillFolderHash`  |
| `skills update`            | `src/cli.ts` 直接哈希比较 + 通过 `skills add` 重新安装 |

## 开发

```bash
# 安装依赖
pnpm install

# 构建
pnpm build

# 本地测试
pnpm dev add vercel-labs/agent-skills --list
pnpm dev experimental_sync
pnpm dev check
pnpm dev update
pnpm dev init my-skill

# 运行所有测试
pnpm test

# 运行特定测试文件
pnpm test tests/sanitize-name.test.ts
pnpm test tests/skill-matching.test.ts tests/source-parser.test.ts

# 类型检查
pnpm type-check

# 格式化代码
pnpm format

# 检查格式
pnpm format:check

# 验证和同步代理元数据/文档
pnpm run -C scripts validate-agents.ts
pnpm run -C scripts sync-agents.ts
```

## 代码风格

本项目使用 Prettier 进行代码格式化。**在提交更改之前始终运行 `pnpm format`** 以确保格式一致。

```bash
# 格式化所有文件
pnpm format

# 检查格式而不修复
pnpm format:check
```

如果代码格式不正确，CI 将失败。

## 发布

```bash
# 1. 在 package.json 中提升版本
# 2. 构建
pnpm build
# 3. 发布
npm publish
```

## 添加新代理

1. 将代理定义添加到 `src/agents.ts`
2. 运行 `pnpm run -C scripts validate-agents.ts` 进行验证
3. 运行 `pnpm run -C scripts sync-agents.ts` 更新 README.md 和 package 关键字
