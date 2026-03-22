---
name: protocolsio-integration
description: 与protocols.io API集成，用于管理科学实验方案。当需要使用protocols.io搜索、创建、更新或发布实验方案；管理实验步骤和材料；处理讨论和评论；组织工作空间；上传和管理文件；或将protocols.io功能集成到工作流中时使用此技能。适用于实验方案发现、协作实验方案开发、实验跟踪、实验室实验方案管理和科学文档编制。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
---

# Protocols.io 集成

## 概述

Protocols.io 是一个用于开发、共享和管理科学实验方案的综合平台。此技能提供与 protocols.io API v3 的完整集成，实现对实验方案、工作空间、讨论、文件管理和协作功能的程序化访问。

## 使用场景

在以下任何场景中使用此技能：

- **实验方案发现**：通过关键词、DOI或类别搜索现有实验方案
- **实验方案管理**：创建、更新或发布科学实验方案
- **步骤管理**：添加、编辑或组织实验步骤和程序
- **协作开发**：与团队成员共同处理共享实验方案
- **工作空间组织**：管理实验室或机构的实验方案库
- **讨论与反馈**：添加或回复实验方案评论
- **文件管理**：上传数据文件、图像或文档到实验方案
- **实验跟踪**：记录实验方案执行和结果
- **数据导出**：备份或迁移实验方案集合
- **集成项目**：构建与 protocols.io 交互的工具

## 核心功能

此技能在五个主要功能领域提供全面指导：

### 1. 认证与访问

使用访问令牌和OAuth流程管理API认证。包括客户端访问令牌（用于个人内容）和OAuth令牌（用于多用户应用）。

**关键操作：**
- 为OAuth流程生成授权链接
- 交换授权码以获取访问令牌
- 刷新过期令牌
- 管理速率限制和权限

**参考：** 阅读 `references/authentication.md` 获取详细的认证程序、OAuth实现和安全最佳实践。

### 2. 实验方案操作

从创建到发布的完整实验方案生命周期管理。

**关键操作：**
- 通过关键词、过滤器或DOI搜索和发现实验方案
- 检索包含所有步骤的详细实验方案信息
- 创建带有元数据和标签的新实验方案
- 更新实验方案信息和设置
- 管理实验步骤（创建、更新、删除、重新排序）
- 处理实验材料和试剂
- 发布带有DOI的实验方案
- 为快速访问添加实验方案书签
- 生成实验方案PDF

**参考：** 阅读 `references/protocols_api.md` 获取全面的实验方案管理指导，包括API端点、参数、常见工作流程和示例。

### 3. 讨论与协作

通过评论和讨论实现社区参与。

**关键操作：**
- 查看实验方案级和步骤级评论
- 创建新评论和线程回复
- 编辑或删除自己的评论
- 分析讨论模式和反馈
- 回应用户问题和问题

**参考：** 阅读 `references/discussions.md` 获取讨论管理、评论线程和协作工作流程。

### 4. 工作空间管理

在具有基于角色权限的团队工作空间中组织实验方案。

**关键操作：**
- 列出和访问用户工作空间
- 检索工作空间详细信息和成员列表
- 请求访问或加入工作空间
- 列出特定工作空间的实验方案
- 在工作空间内创建实验方案
- 管理工作空间权限和协作

**参考：** 阅读 `references/workspaces.md` 获取工作空间组织、权限管理和团队协作模式。

### 5. 文件操作

上传、组织和管理与实验方案相关的文件。

**关键操作：**
- 搜索工作空间文件和文件夹
- 上传带有元数据和标签的文件
- 下载文件并验证上传
- 将文件组织到文件夹层次结构中
- 更新文件元数据
- 删除和恢复文件
- 管理存储和组织

**参考：** 阅读 `references/file_manager.md` 获取文件上传程序、组织策略和存储管理。

### 6. 其他功能

包括个人资料、通知和导出的补充功能。

**关键操作：**
- 管理用户个人资料和设置
- 查询最近发布的实验方案
- 创建和跟踪实验记录
- 接收和管理通知
- 导出组织数据用于存档

**参考：** 阅读 `references/additional_features.md` 获取个人资料管理、出版物发现、实验跟踪和数据导出。

## 入门指南

### 步骤1：认证设置

在使用任何 protocols.io API 功能之前：

1. 获取访问令牌（CLIENT_ACCESS_TOKEN 或 OAUTH_ACCESS_TOKEN）
2. 阅读 `references/authentication.md` 获取详细的认证程序
3. 安全存储令牌
4. 在所有请求中包含：`Authorization: Bearer YOUR_TOKEN`

### 步骤2：确定您的用例

确定哪个功能领域满足您的需求：

- **处理实验方案？** → 阅读 `references/protocols_api.md`
- **管理团队实验方案？** → 阅读 `references/workspaces.md`
- **处理评论/反馈？** → 阅读 `references/discussions.md`
- **上传文件/数据？** → 阅读 `references/file_manager.md`
- **跟踪实验或个人资料？** → 阅读 `references/additional_features.md`

### 步骤3：实现集成

按照相关参考文件中的指导：

- 每个参考文件都包含详细的端点文档
- 指定API参数和请求/响应格式
- 提供常见用例和工作流程示例
- 包含最佳实践和错误处理指南

## 基础URL和请求格式

所有API请求使用基础URL：
```
https://protocols.io/api/v3
```

所有请求都需要Authorization头：
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

大多数端点支持JSON请求/响应格式，带有 `Content-Type: application/json`。

## 内容格式选项

许多端点支持 `content_format` 参数来控制实验方案内容的返回方式：

- `json`：Draft.js JSON格式（默认）
- `html`：HTML格式
- `markdown`：Markdown格式

作为查询参数包含：`?content_format=html`

## 速率限制

注意API速率限制：

- **标准端点**：每个用户每分钟100个请求
- **PDF端点**：5个请求/分钟（已登录），3个请求/分钟（未登录）

对速率限制错误（HTTP 429）实现指数退避。

## 常见工作流程

### 工作流程1：导入和分析实验方案

分析来自 protocols.io 的现有实验方案：

1. **搜索**：使用 `GET /protocols` 和关键词查找相关实验方案
2. **检索**：使用 `GET /protocols/{protocol_id}` 获取完整详细信息
3. **提取**：解析步骤、材料和元数据进行分析
4. **查看讨论**：检查 `GET /protocols/{id}/comments` 获取用户反馈
5. **导出**：如果需要离线参考，生成PDF

**参考文件**：`protocols_api.md`、`discussions.md`

### 工作流程2：创建和发布实验方案

创建新实验方案并发布带有DOI：

1. **认证**：确保您有有效的访问令牌（见 `authentication.md`）
2. **创建**：使用 `POST /protocols` 提供标题和描述
3. **添加步骤**：对每个步骤，使用 `POST /protocols/{id}/steps`
4. **添加材料**：在步骤组件中记录试剂
5. **审查**：验证所有内容完整准确
6. **发布**：使用 `POST /protocols/{id}/publish` 发布DOI

**参考文件**：`protocols_api.md`、`authentication.md`

### 工作流程3：协作实验室工作空间

设置团队实验方案管理：

1. **创建/加入工作空间**：访问或请求工作空间成员资格（见 `workspaces.md`）
2. **组织结构**：为实验室实验方案创建文件夹层次结构（见 `file_manager.md`）
3. **创建实验方案**：使用 `POST /workspaces/{id}/protocols` 创建团队实验方案
4. **上传文件**：添加实验数据和图像
5. **启用讨论**：团队成员可以评论并提供反馈
6. **跟踪实验**：使用实验记录记录实验方案执行

**参考文件**：`workspaces.md`、`file_manager.md`、`protocols_api.md`、`discussions.md`、`additional_features.md`

### 工作流程4：实验文档

跟踪实验方案执行和结果：

1. **执行实验方案**：在实验室执行实验方案
2. **上传数据**：使用文件管理器API上传结果（见 `file_manager.md`）
3. **创建记录**：使用 `POST /protocols/{id}/runs` 记录执行
4. **链接文件**：在实验记录中引用上传的数据文件
5. **记录修改**：记录任何实验方案偏差或优化
6. **分析**：审查多个运行以评估可重复性

**参考文件**：`additional_features.md`、`file_manager.md`、`protocols_api.md`

### 工作流程5：实验方案发现和引用

在研究中查找和引用实验方案：

1. **搜索**：使用 `GET /publications` 查询已发布的实验方案
2. **过滤**：使用类别和关键词过滤器查找相关实验方案
3. **审查**：阅读实验方案详细信息和社区评论
4. **添加书签**：使用 `POST /protocols/{id}/bookmarks` 保存有用的实验方案
5. **引用**：在出版物中使用实验方案DOI（适当归因）
6. **导出PDF**：生成格式化的PDF用于离线参考

**参考文件**：`protocols_api.md`、`additional_features.md`

## Python请求示例

### 基本实验方案搜索

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# 搜索CRISPR实验方案
response = requests.get(
    "https://protocols.io/api/v3/protocols",
    headers=headers,
    params={
        "filter": "public",
        "key": "CRISPR",
        "page_size": 10,
        "content_format": "html"
    }
)

protocols = response.json()
for protocol in protocols["items"]:
    print(f"{protocol['title']} - {protocol['doi']}")
```

### 创建新实验方案

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 创建实验方案
data = {
    "title": "CRISPR-Cas9基因编辑实验方案",
    "description": "CRISPR基因编辑综合实验方案",
    "tags": ["CRISPR", "基因编辑", "分子生物学"]
}

response = requests.post(
    "https://protocols.io/api/v3/protocols",
    headers=headers,
    json=data
)

protocol_id = response.json()["item"]["id"]
print(f"创建的实验方案：{protocol_id}")
```

### 上传文件到工作空间

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# 上传文件
with open("data.csv", "rb") as f:
    files = {"file": f}
    data = {
        "folder_id": "root",
        "description": "实验结果",
        "tags": "experiment,data,2025"
    }

    response = requests.post(
        "https://protocols.io/api/v3/workspaces/12345/files/upload",
        headers=headers,
        files=files,
        data=data
    )

file_id = response.json()["item"]["id"]
print(f"上传的文件：{file_id}")
```

## 错误处理

为API请求实现健壮的错误处理：

```python
import requests
import time

def make_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # 速率限制
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                continue
            elif response.status_code >= 500:  # 服务器错误
                time.sleep(2 ** attempt)  # 指数退避
                continue
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

    raise Exception("超过最大重试次数")
```

## 参考文件

根据您的任务加载适当的参考文件：

- **`authentication.md`**：OAuth流程、令牌管理、速率限制
- **`protocols_api.md`**：实验方案CRUD、步骤、材料、发布、PDF
- **`discussions.md`**：评论、回复、协作
- **`workspaces.md`**：团队工作空间、权限、组织
- **`file_manager.md`**：文件上传、文件夹、存储管理
- **`additional_features.md`**：个人资料、出版物、实验、通知

要加载参考文件，在需要特定功能时从 `references/` 目录读取文件。

## 最佳实践

1. **认证**：安全存储令牌，永远不要在代码或版本控制中存储
2. **速率限制**：实现指数退避并尊重速率限制
3. **错误处理**：适当处理所有HTTP错误代码
4. **数据验证**：在API调用前验证输入
5. **文档**：彻底记录实验步骤
6. **协作**：使用评论和讨论进行团队沟通
7. **组织**：保持一致的命名和标签约定
8. **版本控制**：在进行更新时跟踪实验方案版本
9. **归因**：使用DOI正确引用实验方案
10. **备份**：定期导出重要的实验方案和工作空间数据

## 其他资源

- **官方API文档**：https://apidoc.protocols.io/
- **Protocols.io平台**：https://www.protocols.io/
- **支持**：联系protocols.io支持获取API访问和技术问题
- **社区**：参与protocols.io社区获取最佳实践

## 故障排除

**认证问题：**
- 验证令牌有效且未过期
- 检查Authorization头格式：`Bearer YOUR_TOKEN`
- 确保适当的令牌类型（CLIENT vs OAUTH）

**速率限制：**
- 为429错误实现指数退避
- 监控请求频率
- 考虑缓存频繁请求

**权限错误：**
- 验证工作空间/实验方案访问权限
- 检查工作空间中的用户角色
- 确保实验方案不是私人的，如果在没有权限的情况下访问

**文件上传失败：**
- 检查文件大小是否符合工作空间限制
- 验证文件类型是否支持
- 确保multipart/form-data编码正确

有关详细的故障排除指南，请参考涵盖每个功能领域的特定参考文件。