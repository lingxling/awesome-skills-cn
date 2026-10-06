---
name: plugin-creator
description: 为 Codex 创建并搭建插件目录脚手架，包含必需的 `.codex-plugin/plugin.json`、可选的插件文件夹/文件，以及可在发布或测试前编辑的基础占位内容。当 Codex 需要创建新的本地插件、添加可选的插件结构，或生成/更新仓库根目录的 `.agents/plugins/marketplace.json` 条目（用于插件排序和可用性元数据）时使用。
---

# 插件创建器

## 快速开始

1. 运行脚手架脚本：

```bash
  # 插件名称会被规范化为小写连字符形式（hyphen-case），且长度必须 <= 64 个字符。
  # 生成的文件夹名和 plugin.json 中的 name 始终相同。
# 从仓库根目录运行（或将 .agents/... 替换为本 SKILL 的绝对路径）。
# 默认创建在 <repo_root>/plugins/<plugin-name>。
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py <plugin-name>
```

2. 打开 `<plugin-path>/.codex-plugin/plugin.json`，替换其中的 `[TODO: ...]` 占位符。

3. 当插件需要出现在 Codex UI 的排序中时，生成或更新仓库的 marketplace 条目：

```bash
# marketplace.json 始终位于 <repo-root>/.agents/plugins/marketplace.json
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py my-plugin --with-marketplace
```

对于主目录本地（home-local）插件，将 `<home>` 视为根目录，使用：

```bash
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py my-plugin \
  --path ~/plugins \
  --marketplace-path ~/.agents/plugins/marketplace.json \
  --with-marketplace
```

4. 根据需要生成/调整可选的配套文件夹：

```bash
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py my-plugin --path <parent-plugin-directory> \
  --with-skills --with-hooks --with-scripts --with-assets --with-mcp --with-apps --with-marketplace
```

`<parent-plugin-directory>` 是将要创建插件文件夹 `<plugin-name>` 的目录（例如 `~/code/plugins`）。

## 此技能会创建什么

- 如果用户没有明确指定插件位置，在生成 marketplace 条目之前，先询问他们想要仓库本地（repo-local）插件还是主目录本地（home-local）插件。
- 在 `/<parent-plugin-directory>/<plugin-name>/` 创建插件根目录。
- 始终创建 `/<parent-plugin-directory>/<plugin-name>/.codex-plugin/plugin.json`。
- 用完整的 schema 结构、占位值以及完整的 `interface` 部分填充清单（manifest）。
- 当设置了 `--with-marketplace` 时，创建或更新 `<repo-root>/.agents/plugins/marketplace.json`。
  - 如果 marketplace 文件尚不存在，先写入顶层的 `name` 以及 `interface.displayName` 占位符，再添加第一个插件条目。
- `<plugin-name>` 按照 skill-creator 的命名规则进行规范化：
  - `My Plugin` → `my-plugin`
  - `My--Plugin` → `my-plugin`
  - 下划线、空格和标点符号会被转换为 `-`
  - 结果为小写、以连字符分隔，连续的连字符会被合并
- 支持可选地创建：
  - `skills/`
  - `hooks/`
  - `scripts/`
  - `assets/`
  - `.mcp.json`
  - `.app.json`

## Marketplace 工作流

- `marketplace.json` 始终位于 `<repo-root>/.agents/plugins/marketplace.json`。
- 对于主目录本地插件，采用相同的约定，以 `<home>` 作为根目录：
  `~/.agents/plugins/marketplace.json` 加上 `./plugins/<plugin-name>`。
- Marketplace 根元数据支持顶层的 `name` 以及可选的 `interface.displayName`。
- 将 `plugins[]` 中的插件顺序视为 Codex 中的渲染顺序。除非用户明确要求重新排序，否则只在末尾追加新条目。
- `displayName` 属于 marketplace 的 `interface` 对象，而不属于 `plugins[]` 中的各个条目。
- 每个生成的 marketplace 条目必须包含以下全部内容：
  - `policy.installation`
  - `policy.authentication`
  - `category`
- 新条目的默认值为：
  - `policy.installation: "AVAILABLE"`
  - `policy.authentication: "ON_INSTALL"`
- 仅当用户明确指定了其他允许的取值时，才覆盖默认值。
- `policy.installation` 的允许取值：
  - `NOT_AVAILABLE`
  - `AVAILABLE`
  - `INSTALLED_BY_DEFAULT`
- `policy.authentication` 的允许取值：
  - `ON_INSTALL`
  - `ON_USE`
- 将 `policy.products` 视为一种覆盖项。除非用户明确要求按产品进行限制，否则省略它。
- 生成的插件条目结构如下：

```json
{
  "name": "plugin-name",
  "source": {
    "source": "local",
    "path": "./plugins/plugin-name"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

- 只有在有意替换同名插件的现有 marketplace 条目时，才使用 `--force`。
- 如果 `<repo-root>/.agents/plugins/marketplace.json` 尚不存在，创建它，包含顶层的 `"name"`、包含 `"displayName"` 的 `"interface"` 对象以及一个 `plugins` 数组，然后添加新条目。

- 对于全新的 marketplace 文件，根对象应如下所示：

```json
{
  "name": "[TODO: marketplace-name]",
  "interface": {
    "displayName": "[TODO: Marketplace Display Name]"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": {
        "source": "local",
        "path": "./plugins/plugin-name"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

## 必需行为

- 外层文件夹名和 `plugin.json` 中的 `"name"` 始终是同一个规范化后的插件名。
- 不要删除必需的结构；保持 `.codex-plugin/plugin.json` 存在。
- 在有人或后续步骤明确填写之前，清单中的值保持为占位符。
- 如果在已有的插件路径内创建文件，只有在确实要覆盖时才使用 `--force`。
- 保留现有 marketplace 的 `interface.displayName`。
- 生成 marketplace 条目时，即使 `policy.installation`、`policy.authentication` 和 `category` 的值是默认值，也始终要写入它们。
- 仅当用户明确要求该覆盖项时，才添加 `policy.products`。
- 保持 marketplace 的 `source.path` 相对于仓库根目录，形式为 `./plugins/<plugin-name>`。

## 精确规范示例的参考

插件清单和 marketplace 条目的精确标准示例 JSON，请参阅：

- `references/plugin-json-spec.md`

## 验证

编辑 `SKILL.md` 之后，运行：

```bash
python3 <path-to-skill-creator>/scripts/quick_validate.py .agents/skills/plugin-creator
```
