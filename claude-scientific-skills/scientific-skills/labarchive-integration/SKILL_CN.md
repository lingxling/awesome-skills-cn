---
name: labarchive-integration
description: 电子实验记录本API集成。访问笔记本、管理条目/附件、备份笔记本、与Protocols.io/Jupyter/REDCap集成，用于程序化ELN工作流程。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# LabArchives集成

## 概述

LabArchives是一个用于研究文档和数据管理的电子实验记录本平台。通过REST API以编程方式访问笔记本、管理条目和附件、生成报告，并与第三方工具集成。

## 何时使用此技能

在以下情况下应使用此技能：
- 使用LabArchives REST API进行笔记本自动化
- 以编程方式备份笔记本
- 创建或管理笔记本条目和附件
- 生成站点报告和分析
- 将LabArchives与第三方工具（Protocols.io、Jupyter、REDCap）集成
- 自动将数据上传到电子实验记录本
- 以编程方式管理用户访问和权限

## 核心能力

### 1. 身份验证和配置

设置LabArchives API集成的API访问凭据和区域端点。

**先决条件：**
- 带有API访问权限的企业LabArchives许可证
- LabArchives管理员提供的API访问密钥ID和密码
- 用户身份验证凭据（电子邮件和外部应用程序密码）

**配置设置：**

使用`scripts/setup_config.py`脚本创建配置文件：

```bash
python3 scripts/setup_config.py
```

这将创建具有以下结构的`config.yaml`文件：

```yaml
api_url: https://api.labarchives.com/api  # 或区域端点
access_key_id: YOUR_ACCESS_KEY_ID
access_password: YOUR_ACCESS_PASSWORD
```

**区域API端点：**
- 美国/国际：`https://api.labarchives.com/api`
- 澳大利亚：`https://auapi.labarchives.com/api`
- 英国：`https://ukapi.labarchives.com/api`

有关详细的身份验证说明和故障排除，请参阅`references/authentication_guide.md`。

### 2. 用户信息检索

获取后续API操作所需的用户ID（UID）和访问信息。

**工作流程：**

1. 使用登录凭据调用`users/user_access_info` API方法
2. 解析XML/JSON响应以提取用户ID（UID）
3. 使用UID通过`users/user_info_via_id`检索详细用户信息

**使用Python包装器的示例：**

```python
from labarchivespy.client import Client

# 初始化客户端
client = Client(api_url, access_key_id, access_password)

# 获取用户访问信息
login_params = {'login_or_email': user_email, 'password': auth_token}
response = client.make_call('users', 'user_access_info', params=login_params)

# 从响应中提取UID
import xml.etree.ElementTree as ET
uid = ET.fromstring(response.content)[0].text

# 获取详细用户信息
params = {'uid': uid}
user_info = client.make_call('users', 'user_info_via_id', params=params)
```

### 3. 笔记本操作

管理笔记本访问、备份和元数据检索。

**关键操作：**

- **列出笔记本**：检索用户可访问的所有笔记本
- **备份笔记本**：下载完整的笔记本数据，可选择包含附件
- **获取笔记本ID**：检索机构定义的笔记本标识符，以便与资助/项目管理系统集成
- **获取笔记本成员**：列出有权访问特定笔记本的所有用户
- **获取笔记本设置**：检索笔记本的配置和权限

**笔记本备份示例：**

使用`scripts/notebook_operations.py`脚本：

```bash
# 带有附件的备份（默认，创建7z归档）
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID

# 不带附件的备份，JSON格式
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID --json --no-attachments
```

**API端点格式：**
```
https://<api_url>/notebooks/notebook_backup?uid=<UID>&nbid=<NOTEBOOK_ID>&json=true&no_attachments=false
```

有关全面的API方法文档，请参阅`references/api_reference.md`。

### 4. 条目和附件管理

创建、修改和管理笔记本条目和文件附件。

**条目操作：**
- 在笔记本中创建新条目
- 向现有条目添加评论
- 创建条目部分/组件
- 向条目上传文件附件

**附件工作流程：**

使用`scripts/entry_operations.py`脚本：

```bash
# 向条目上传附件
python3 scripts/entry_operations.py upload --uid USER_ID --nbid NOTEBOOK_ID --entry-id ENTRY_ID --file /path/to/file.pdf

# 创建带文本内容的新条目
python3 scripts/entry_operations.py create --uid USER_ID --nbid NOTEBOOK_ID --title "实验结果" --content "今天实验的结果..."
```

**支持的文件类型：**
- 文档（PDF、DOCX、TXT）
- 图像（PNG、JPG、TIFF）
- 数据文件（CSV、XLSX、HDF5）
- 科学格式（CIF、MOL、PDB）
- 归档（ZIP、7Z）

### 5. 站点报告和分析

生成机构报告，关于笔记本使用、活动和合规性（企业功能）。

**可用报告：**
- 详细使用报告：用户活动指标和参与度统计
- 详细笔记本报告：笔记本元数据、成员列表和设置
- PDF/离线笔记本生成报告：导出跟踪以实现合规
- 笔记本成员报告：访问控制和协作分析
- 笔记本设置报告：配置和权限审核
- PDF/离线笔记本生成报告：导出跟踪以实现合规

**报告生成：**

```python
# 生成详细使用报告
response = client.make_call('site_reports', 'detailed_usage_report',
                           params={'start_date': '2025-01-01', 'end_date': '2025-10-20'})
```

### 6. 第三方集成

LabArchives与众多科学软件平台集成。该技能提供利用这些集成的程序化指导。

**支持的集成：**
- **Protocols.io**：将协议直接导出到LabArchives笔记本
- **GraphPad Prism**：导出分析和图形（8.0版及以上）
- **SnapGene**：直接分子生物学工作流程集成
- **Geneious**：生物信息学分析导出
- **Jupyter**：将Jupyter笔记本嵌入为条目
- **REDCap**：临床数据捕获集成
- **Qeios**：研究发布平台
- **SciSpace**：文献管理

**OAuth身份验证：**
LabArchives现在对所有新集成使用OAuth。旧集成可能使用API密钥身份验证。

有关详细的集成设置说明和用例，请参阅`references/integrations.md`。

## 常见工作流程

### 完整笔记本备份工作流程

1. 身份验证并获取用户ID
2. 列出所有可访问的笔记本
3. 遍历笔记本并备份每个
4. 使用时间戳元数据存储备份

```bash
# 完整备份脚本
python3 scripts/notebook_operations.py backup-all --email user@example.edu --password AUTH_TOKEN
```

### 自动化数据上传工作流程

1. 使用LabArchives API进行身份验证
2. 识别目标笔记本和条目
3. 上传实验数据文件
4. 向条目添加元数据评论
5. 生成活动报告

### 集成工作流程示例（Jupyter → LabArchives）

1. 将Jupyter笔记本导出为HTML或PDF
2. 使用entry_operations.py上传到LabArchives
3. 添加带有执行时间戳和环境信息的评论
4. 为便于检索标记条目

## Python包安装

安装`labarchives-py`包装器以简化API访问：

```bash
git clone https://github.com/mcmero/labarchives-py
cd labarchives-py
uv pip install .
```

或者，通过Python的`requests`库使用直接HTTP请求进行自定义实现。

## 最佳实践

1. **速率限制**：实施API调用之间的适当延迟以避免限流
2. **错误处理**：始终将API调用包装在try-except块中，并带有适当的日志记录
3. **身份验证安全**：将凭据存储在环境变量或安全配置文件中（绝不存储在代码中）
4. **备份验证**：笔记本备份后，验证文件完整性和完整性
5. **增量操作**：对于大型笔记本，使用分页和批处理
6. **区域端点**：为最佳性能使用正确的区域API端点
7. **记录所有操作**：跟踪所有API调用、响应时间和错误以进行调试

## 故障排除

**常见问题：**

- **401未授权**：验证访问密钥ID和密码正确；检查您的账户是否启用了API访问
- **404未找到**：确认笔记本ID（nbid）存在且用户具有访问权限
- **403禁止**：检查用户对所请求操作的权限
- **空响应**：确保提供了正确的参数（uid、nbid）
- **附件上传失败**：验证文件大小限制和格式兼容性

有关其他支持，请通过support@labarchives.com联系LabArchives。

## 资源

此技能包含支持LabArchives API集成的捆绑资源：

### scripts/

- `setup_config.py`：用于API凭据的交互式配置文件生成器
- `notebook_operations.py`：用于列出、备份和管理笔记本的实用程序
- `entry_operations.py`：用于创建条目和上传附件的工具

### references/

- `api_reference.md`：全面的API端点文档，包含参数和示例
- `authentication_guide.md`：详细的身份验证设置和配置说明
- `integrations.md`：第三方集成设置指南和用例
