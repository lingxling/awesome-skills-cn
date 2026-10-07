---
name: accesslint-scan
description: "审计实时页面的无障碍问题、精确定位每个 WCAG 违规、并返回选择器依据的修复工作清单，无编辑。"
risk: safe
source: "https://github.com/AccessLint/skills"
date_added: "2026-06-02"
---

审计实时页面并报告什么坏了及在哪里。定位；不要修复。如果 `$ARGUMENTS` 中没有 URL，请要求一个。

## 何时使用

- 当任务与此描述匹配时使用此技能：审计实时页面的无障碍问题、精确定位每个 WCAG 违规、并返回选择器依据的修复工作清单，无编辑。

## 1. 审计

```bash
PORT=$(npx -y @accesslint/chrome@latest ensure | node -e 'process.stdin.on("data",d=>process.stdout.write(""+JSON.parse(d).port))')
npx -y @accesslint/cli@latest "<url>" --port "$PORT" --format json
```

根据需要标记：`--selector`、`--wait-for "<selector>"`、`--include-aaa`、`--disable <rules>`。

## 2. 报告

按影响计数，然后每个违规一项：

- **位置** — 逐字选择器 + `file:line (symbol)` 如果 `source` 存在 — 绝不伪造。如果没有违规有 `source`，注意"源映射不可用 — 仅通过选择器定位"。
- **证据** — 对比度比、缺失属性、空名称
- **修复** — 机械改变或 `需要人工`

不要编辑。对于修复：应用机械修复然后重新运行以验证；对于大量工作移交给 `accesslint:audit`。

## 3. 清除

```bash
npx -y @accesslint/chrome@latest stop --all  # 如果 ensure 报告 "managed":false 则跳过
```

## 陷阱

- `ensure` 总是确定端口 — 永不硬编码 9222。
- CLI 退出 2 = 坏 URL 或页面从不加载；检查开发服务器。

## 限制条件

- 仅在任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
