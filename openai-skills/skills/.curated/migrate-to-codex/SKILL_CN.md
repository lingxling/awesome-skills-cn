---
name: migrate-to-codex
description: 将支持的指令文件、skills、agents 和 MCP 配置迁移到 Codex 项目和全局文件中。
---

# 迁移到 Codex

## 自主性

继续进行直到所选迁移完全完成：运行迁移工具、检查报告、修复已迁移的 Codex 指令/skills/agents/MCP 配置，然后重新运行检查，不要停下来询问下一步的确认。如果用户已选择目标，在该目标中创建、编辑、替换或删除生成的 Codex 产物之前不要询问（`AGENTS.md`、`.codex/`、`.agents/` 或 `~/.codex/`）。保留 `.codex/config.toml` 或 `~/.codex/config.toml` 中不相关的现有 Codex 配置条目，如 `notify`、`projects`、`marketplaces` 或不相关的 MCP 服务器；除非它们验证失败或与迁移直接冲突，否则不要询问它们。不要编辑源 Claude Code 文件（`.claude/`、`~/.claude/`、`.mcp.json` 或 `.claude.json`）、不相关的项目代码、密钥或另一个仓库。

## 迁移顺序

对每个选定的全局或项目源按以下顺序运行迁移：

1. 首先使用 Codex 内置的 TODO/任务列表工具。除非用户明确要求，否则不要创建 `MIGRATION_TODOS.md` 或任何 TODO 文件。TODO 列表输入有一个 `plan` 数组，其项目各有 `step` 和 `status`；使用状态 `pending`、`in_progress` 和 `completed`。使 TODO 特定于选定的产物。使用字面的源 → Codex 目标标签，例如：
   - 检查 `.claude/commands` → Codex skills/prompts
   - 检查 `.claude/agents` → `.codex/agents`
   - 检查 `.mcp.json` → `.codex/config.toml` MCP 服务器
   - 检查 `.claude/settings.json` hooks → `.codex/hooks.json`
   - 迁移安全的选定产物 → Codex 文件
   - 验证生成的 `.codex/config.toml`
   - 验证生成的 `.codex/agents`
   - 报告已迁移的产物和需要手动审查的项目

2. 阅读 `references/differences.md`（如果其 `Docs last checked` 日期很旧，则刷新 Codex 文档）。

3. 写入前扫描和检查：
   - `--scan-only` 列出活动和非活动的源表面。
   - `--plan` 打印暂存的 Codex 产物路径和报告行。
   - `--doctor` 总结准备情况、手动审查工作和验证风险。

4. 按照 CLI 使用的相同顺序转换表面：
   - 指令：`CLAUDE.md` / `AGENTS.md` 转换为 `AGENTS.md`
   - 插件：将 Claude 插件树和市场报告为手动迁移工作
   - hooks：将支持的 Claude hooks 重写为 `.codex/hooks.json` 并启用 `[features].codex_hooks = true`
   - skills 和 commands：在 `.agents/skills/` 下写入 Codex skills
   - config：从 Claude 模型/沙盒设置和 MCP 服务器写入 `.codex/config.toml`，生成配置时包含 `personality = "friendly"`
   - subagents：在 `.codex/agents/` 下写入 Codex 自定义 agents

5. 试运行，然后写入选定的目标。仅当应该删除孤立的生成 skills 或 agents 时才使用 `--replace`。

6. 实际运行后检查终端输出和 `.codex/migrate-to-codex-report.txt`。

7. 按此顺序检查生成的产物：`AGENTS.md`、`.agents/skills/`、`.codex/config.toml`、`.codex/hooks.json`、`.codex/agents/`，然后是仅报告的插件项目。

8. 每次编辑后对每个目标运行 `--validate-target`。

9. 编辑后重新运行检查和 `--dry-run`。

10. 将最终迁移报告作为每个有行的范围的一个 markdown 表格返回。表格仅涵盖您执行的非原生后续迁移工作，如从斜杠命令创建的 skills、subagents、MCP 服务器、hooks、不支持的/本地插件说明和手动审查注意事项。仅当您在本后续运行中以编程方式原生导入了配置、指令、skills 或支持的插件时，才包含这些行的程序化原生导入行。

    如果只有一个范围有行，则仅渲染表格而不加标题。如果多个范围有行，则在每个表格前渲染一个标题。对于用户范围行使用 `**User Config**`。对于项目范围行，使用实际的项目文件夹名称作为标题，例如 `**northstar-support-portal**`；不要使用 `Current Project` 作为标题。不要在表格输出前或后添加散文。

    使用确切的列：

    **northstar-support-portal**

    | 状态 | 项目 | 备注 |
    | --- | --- | --- |
    | `已添加` | `斜杠命令` pr-review | 已转换为 Codex skill |
    | `已添加` | `Subagent` release-lead | 已添加为 Codex subagent |
    | `使用前检查` | `Hook` PreToolUse | 已转换，但某些 Claude hook 行为在 Codex 中有所不同 |
    | `未添加` | `Hook` Notification | Codex 没有等效的通知 hook |
    | `未添加` | `Plugin` team-macros | 插件需要手动设置 |

    `Status` 必须是 `Added`、`Check before using` 或 `Not Added`。当创建或更改了 Codex 面向的产物且不需要特殊审查时，使用 `Added`。当创建或更改了 Codex 面向的产物但迁移改变了语义、推断行为、将工具规则保留为指导或删除了不支持的行为时，使用 `Check before using`。当检测到源产物但未创建 Codex 面向的产物时，使用 `Not Added`。`Item` 在一个单元格中组合产物类型和具体项目名称。产物类型必须是单数：`Skill`、`Slash command`、`Subagent`、`MCP`、`Hook` 或 `Plugin`。将产物类型包装在内联代码中；在其后方写项目名称作为纯文本。`Notes` 始终是必需的；切勿留空。保持备注简短、纯文字和字面。避免内部实现术语，如运行时展开。优先使用短语，如 `已转换为 Codex skill`、`已添加为 Codex subagent`、`已添加到 Codex 配置`、`已转换为 Codex hook`、`已转换，但某些 Claude hook 行为在 Codex 中有所不同`、`Codex 没有等效的通知 hook`、`插件需要手动设置` 或 `插件市场需要手动设置`。

## 自我修复循环

继续循环直到所选迁移完成：

1. 运行 `--plan` 或 `--doctor`。
2. 使用 `--dry-run` 运行迁移。
3. 实际运行迁移。
4. 修复每个生成的 `## MANUAL MIGRATION REQUIRED` 块和每个可以在 Codex 产物内解决的 `manual_fix_required` 或 `skipped` 报告行。
5. 运行 `--validate-target`。
6. 重新运行迁移工具和验证器，直到报告和验证器没有剩余可操作的生成产物修复。

在此循环期间不要编辑源 Claude Code 文件、不相关的项目代码、密钥或另一个仓库。如果报告行需要源提供商更改或产品判断，请将生成的 Codex 产物保留清晰的手动指导，而不是更改源。

## 命令

选择迁移工具命令。

   ```bash
   MIGRATE_TO_CODEX='python3 .codex/skills/migrate-to-codex/scripts/migrate-to-codex.py'
   ```

写入前检查迁移。

   ```bash
   $MIGRATE_TO_CODEX --source ~/.claude/ --scan-only
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/ --plan
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/ --doctor
   ```

然后为全局和项目运行（先 dry-run，再不带 `--dry-run`）。

   ```bash
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/ --dry-run
   $MIGRATE_TO_CODEX --source ~/.claude/ --target ~/.codex/
   $MIGRATE_TO_CODEX --source ./.claude/ --target ./.codex/ --dry-run
   $MIGRATE_TO_CODEX --source ./.claude/ --target ./.codex/
   ```

编辑后对每个目标运行迁移后验证器。

   ```bash
   $MIGRATE_TO_CODEX --validate-target ~/.codex/
   $MIGRATE_TO_CODEX --validate-target ./.codex/
   ```

运行 `$MIGRATE_TO_CODEX --help` 获取标志（`--scan-only`、`--plan`、`--doctor`、`--validate-target`、默认值等）。更深入的表格和更多链接在 `references/differences.md` 中。
