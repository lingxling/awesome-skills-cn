---
name: pyzotero
description: 使用pyzotero Python客户端与Zotero参考文献管理库进行交互。通过Zotero Web API v3检索、创建、更新和删除项目、集合、标签和附件。当以编程方式使用Zotero库、管理参考文献、导出引文、搜索库内容、上传PDF附件或构建与Zotero集成的研究自动化工作流时使用此技能。
allowed-tools: Read Write Edit Bash
license: MIT License
compatibility: Requires Python 3.10+ and pyzotero 1.13+. Web API access needs a Zotero API key. Optional CLI and MCP extras require Zotero 7 with local API access enabled.
required_environment_variables: [{"name": "ZOTERO_API_KEY", "prompt": "Zotero API key.", "required_for": "full functionality"}, {"name": "ZOTERO_LIBRARY_ID", "prompt": "Zotero library id.", "required_for": "full functionality"}, {"name": "ZOTERO_LIBRARY_TYPE", "prompt": "Zotero library type: 'user' or 'group' (default 'user').", "required_for": "optional features"}]
metadata: {"version": "1.1", "skill-author": "K-Dense Inc.", "openclaw": {"primaryEnv": "ZOTERO_API_KEY", "envVars": [{"name": "ZOTERO_API_KEY", "required": true, "description": "Zotero API key."}, {"name": "ZOTERO_LIBRARY_ID", "required": true, "description": "Zotero library id."}, {"name": "ZOTERO_LIBRARY_TYPE", "required": false, "description": "Zotero library type: 'user' or 'group' (default 'user')."}]}}
---






# Pyzotero

Pyzotero是[Zotero API v3](https://www.zotero.org/support/dev/web_api/v3/start)的Python包装器。使用它以编程方式管理Zotero库：读取项目和集合，创建和更新参考，上传附件，管理标签，以及导出引用。

## 身份验证设置

**所需凭证** — 从https://www.zotero.org/settings/keys获取：
- **User ID**：显示为"Your userID for use in API calls"
- **API Key**：在https://www.zotero.org/settings/keys/new创建
- **Library ID**：对于群组库，群组URL中`/groups/`后的整数

将凭证存储在环境变量或`.env`文件中：
```
ZOTERO_LIBRARY_ID=your_user_id
ZOTERO_API_KEY=your_api_key
ZOTERO_LIBRARY_TYPE=user  # 或 "group"
```

有关完整设置详细信息，请参见[references/authentication.md](references/authentication.md)。

## 安装

```bash
uv add pyzotero
# 或带有CLI支持：
uv add "pyzotero[cli]"
```

## 快速开始

```python
from pyzotero import Zotero

zot = Zotero(library_id='123456', library_type='user', api_key='ABC1234XYZ')

# 检索顶级项目（默认返回100个）
items = zot.top(limit=10)
for item in items:
    print(item['data']['title'], item['data']['itemType'])

# 按关键词搜索
results = zot.items(q='machine learning', limit=20)

# 检索所有项目（使用everything()获取完整结果）
all_items = zot.everything(zot.items())
```

## 核心概念

- 一个`Zotero`实例绑定到单个库（用户或群组）。所有方法都在此库上操作。
- 项目数据存储在`item['data']`中。访问字段如`item['data']['title']`、`item['data']['creators']`。
- Pyzotero默认返回100个项目（API默认是25个）。使用`zot.everything(zot.items())`获取所有项目。
- 写入方法成功时返回`True`或引发`ZoteroError`。

## 参考文件

| 文件 | 内容 |
|------|------|
| [references/authentication.md](references/authentication.md) | 凭证、库类型、本地模式 |
| [references/read-api.md](references/read-api.md) | 检索项目、集合、标签、群组 |
| [references/search-params.md](references/search-params.md) | 过滤、排序、搜索参数 |
| [references/write-api.md](references/write-api.md) | 创建、更新、删除项目 |
| [references/collections.md](references/collections.md) | 集合CRUD操作 |
| [references/tags.md](references/tags.md) | 标签检索和管理 |
| [references/files-attachments.md](references/files-attachments.md) | 文件检索和附件上传 |
| [references/exports.md](references/exports.md) | BibTeX、CSL-JSON、参考文献导出 |
| [references/pagination.md](references/pagination.md) | follow()、everything()、生成器 |
| [references/full-text.md](references/full-text.md) | 全文内容索引和检索 |
| [references/saved-searches.md](references/saved-searches.md) | 保存的搜索管理 |
| [references/cli.md](references/cli.md) | 命令行界面使用 |
| [references/error-handling.md](references/error-handling.md) | 错误和异常处理 |

## 常见模式

### 获取并修改项目
```python
item = zot.item('ITEMKEY')
item['data']['title'] = 'New Title'
zot.update_item(item)
```

### 从模板创建项目
```python
template = zot.item_template('journalArticle')
template['title'] = 'My Paper'
template['creators'][0] = {'creatorType': 'author', 'firstName': 'Jane', 'lastName': 'Doe'}
zot.create_items([template])
```

### 导出为BibTeX
```python
zot.add_parameters(format='bibtex')
bibtex = zot.top(limit=50)
# bibtex是bibtexparser BibDatabase对象
print(bibtex.entries)
```

### 本地模式（只读，不需要API密钥）
```python
zot = Zotero(library_id='123456', library_type='user', local=True)
items = zot.items()
```

### 本地 Zotero 7（CLI 或 MCP，不需要 API 密钥）

要搜索本地运行的 Zotero 桌面应用程序（包括全文 PDF 搜索），请使用 CLI 或 MCP 服务器而不是 Web API。两者都需要启用本地 API 访问的 Zotero 7。请参阅 [references/cli.md](references/cli.md) 和 [references/mcp.md](references/mcp.md)。