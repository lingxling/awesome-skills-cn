---
name: knap
description: 使用 Knap CLI 基于模板和结构化数据渲染 Markdown。当用户要求应用 Knap 模板、将 JSON 或 CSV 数据转换为笔记、批量生成 Markdown 文件，或将 Defuddle 输出格式化为笔记时使用。
---

# Knap

使用 Knap CLI 渲染包含变量、过滤器和逻辑的 Markdown 模板。

如果尚未安装：`npm install -g knap`（需要 Node.js 20 或更高版本）。也可以使用 `npx knap`。

运行 `knap --help` 查看可用的命令和选项。通过 CLI 的离线参考文档了解模板语言：

```bash
knap help syntax
knap help filters
knap help filter date
knap help tags
knap help tag for
```

先通过列表找到名称，再针对单个条目请求帮助，以查看语法、参数以及附带预期输出的示例。

## 用法

使用 JSON 变量渲染模板：

```bash
knap render template.md --data article.json -o note.md
```

以内联方式提供模板和数据：

```bash
knap render -t '# {{ title | trim }}' --data-json '{"title":"Hello"}'
```

覆盖某个变量，或通过管道传入 JSON 数据：

```bash
knap render template.md --data article.json --set 'title=Custom title'
cat article.json | knap render template.md --data -
```

数据必须是一个 JSON 对象；它的属性会成为模板变量。`--set` 会用字符串覆盖字面意义上的顶层键。对于嵌套对象、数组、数字和布尔值，请使用 JSON。

模板来源（文件、`-t` 或 stdin）和数据来源（`--data` 或 `--data-json`）各选一个。只能有一个输入读取 stdin。如果既没有模板文件也没有 `-t`，Knap 会从 stdin 读取模板。

输出默认写到 stdout。`-o` 会在渲染成功后创建父目录并覆盖目标文件。出错时以状态码 `1` 退出；诊断信息输出到 stderr。成功的输出也可能伴随警告。

## 模板

使用 `{{ variable }}` 表示值，`|` 表示过滤器，`{% ... %}` 表示逻辑。例如，将以下内容保存为 `template.md`：

```knap
---
{{ title | yaml_property:"title" }}
{{ tags | yaml_property:"tags" }}
---
# {{ title | trim }}
{% if author %}
By {{ author }}
{% endif %}

{{ content }}
```

对完整的 frontmatter 属性使用 `yaml_property`，这样值会被正确地加引号和缩进。CLI 包含标准过滤器，但不提供 Web Clipper 的浏览器变量、选择器、提示词或依赖 DOM 的 HTML 过滤器。请通过 JSON 提供变量。

渲染前先检查模板：

```bash
knap validate template.md
```

验证会在不使用数据、不输出文件的情况下检查语法、过滤器名称和静态过滤器参数。它不检查变量是否存在、运行时的值或动态参数；要检查运行时行为，请使用真实数据进行渲染。诊断信息输出到 stderr，并包含相关的帮助命令。

## Defuddle 管道

将网页提取为带 Markdown 内容的 JSON，然后渲染为笔记：

```bash
defuddle parse https://example.com/article --md --json \
  | knap render template.md --data - -o note.md
```

Defuddle 的 JSON 属性（例如 `title` 和 `content`）会直接成为模板变量。

## 批量渲染

为每个 CSV 行、每个 JSON 数组对象或文件夹中的每个 JSON 文件各创建一个文件：

```bash
knap batch template.md --data articles.csv --output-dir notes \
  --filename '{{ title | safe_name }}.md'
```

对于数组，使用 `--data articles.json`；对于包含 JSON 对象的文件夹，使用 `--data ./articles`。CSV 表头会成为变量名，值保持为字符串。通过管道传入的数据默认按 JSON 处理；对于管道传入的 CSV，请添加 `--format csv`。

使用 `--dry-run` 可以在不写入文件的情况下进行验证并列出输出路径。目标文件已存在时需要 `--overwrite`，即使在试运行时也是如此。同一批次内输出文件名重复会报错，即使使用了 `--overwrite`。

文件名模板必须生成一个带扩展名的单一文件名，不能包含目录。对于由数据派生的名称，请使用 `safe_name`。如果没有 `--filename`，Knap 会保留源 JSON 文件的基本名称，或者将 CSV 行和数组元素按 `1.md`、`2.md` 等依次编号。
