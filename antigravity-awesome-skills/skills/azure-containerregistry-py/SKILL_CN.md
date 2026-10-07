---
name: azure-containerregistry-py
description: Azure 容器注册表 SDK for Python。用于管理容器镜像、工件和存储库。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Container Registry SDK for Python

在 Azure 容器注册表中管理容器镜像、工件和存储库。

## 安装

```bash
pip install azure-containerregistry
```

## 环境变量

```bash
AZURE_CONTAINERREGISTRY_ENDPOINT=https://<registry-name>.azurecr.io
```

## 认证

### Entra ID（推荐）

```python
from azure.containerregistry import ContainerRegistryClient
from azure.identity import DefaultAzureCredential

client = ContainerRegistryClient(
    endpoint=os.environ["AZURE_CONTAINERREGISTRY_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

### 匿名访问（公共注册表）

```python
from azure.containerregistry import ContainerRegistryClient

client = ContainerRegistryClient(
    endpoint="https://mcr.microsoft.com",
    credential=None,
    audience="https://mcr.microsoft.com"
)
```

## 列出存储库

```python
client = ContainerRegistryClient(endpoint, DefaultAzureCredential())

for repository in client.list_repository_names():
    print(repository)
```

## 存储库操作

### 获取存储库属性

```python
properties = client.get_repository_properties("my-image")
print(f"Created: {properties.created_on}")
print(f"Modified: {properties.last_updated_on}")
print(f"Manifests: {properties.manifest_count}")
print(f"Tags: {properties.tag_count}")
```

### 更新存储库属性

```python
from azure.containerregistry import RepositoryProperties

client.update_repository_properties(
    "my-image",
    properties=RepositoryProperties(
        can_delete=False,
        can_write=False
    )
)
```

### 删除存储库

```python
client.delete_repository("my-image")
```

## 列出标签

```python
for tag in client.list_tag_properties("my-image"):
    print(f"{tag.name}: {tag.created_on}")
```

### 按顺序筛选

```python
from azure.containerregistry import ArtifactTagOrder

# 最近的优先
for tag in client.list_tag_properties(
    "my-image",
    order_by=ArtifactTagOrder.LAST_UPDATED_ON_DESCENDING
):
    print(f"{tag.name}: {tag.last_updated_on}")
```

## 清单操作

### 列出清单

```python
from azure.containerregistry import ArtifactManifestOrder

for manifest in client.list_manifest_properties(
    "my-image",
    order_by=ArtifactManifestOrder.LAST_UPDATED_ON_DESCENDING
):
    print(f"Digest: {manifest.digest}")
    print(f"Tags: {manifest.tags}")
    print(f"Size: {manifest.size_in_bytes}")
```

### 获取清单属性

```python
manifest = client.get_manifest_properties("my-image", "latest")
print(f"Digest: {manifest.digest}")
print(f"Architecture: {manifest.architecture}")
print(f"OS: {manifest.operating_system}")
```

### 更新清单属性

```python
from azure.containerregistry import ArtifactManifestProperties

client.update_manifest_properties(
    "my-image",
    "latest",
    properties=ArtifactManifestProperties(
        can_delete=False,
        can_write=False
    )
)
```

### 删除清单

```python
# 按摘要删除
client.delete_manifest("my-image", "sha256:abc123...")

# 按标签删除
manifest = client.get_manifest_properties("my-image", "old-tag")
client.delete_manifest("my-image", manifest.digest)
```

## 标签操作

### 获取标签属性

```python
tag = client.get_tag_properties("my-image", "latest")
print(f"Digest: {tag.digest}")
print(f"Created: {tag.created_on}")
```

### 删除标签

```python
client.delete_tag("my-image", "old-tag")
```

## 上传和下载工件

```python
from azure.containerregistry import ContainerRegistryClient

client = ContainerRegistryClient(endpoint, DefaultAzureCredential())

# 下载清单
manifest = client.download_manifest("my-image", "latest")
print(f"Media type: {manifest.media_type}")
print(f"Digest: {manifest.digest}")

# 下载 blob
blob = client.download_blob("my-image", "sha256:abc123...")
with open("layer.tar.gz", "wb") as f:
    for chunk in blob:
        f.write(chunk)
```

## 异步客户端

```python
from azure.containerregistry.aio import ContainerRegistryClient
from azure.identity.aio import DefaultAzureCredential

async def list_repos():
    credential = DefaultAzureCredential()
    client = ContainerRegistryClient(endpoint, credential)
    
    async for repo in client.list_repository_names():
        print(repo)
    
    await client.close()
    await credential.close()
```

## 清理旧镜像

```python
from datetime import datetime, timedelta, timezone

cutoff = datetime.now(timezone.utc) - timedelta(days=30)

for manifest in client.list_manifest_properties("my-image"):
    if manifest.last_updated_on < cutoff and not manifest.tags:
        print(f"Deleting {manifest.digest}")
        client.delete_manifest("my-image", manifest.digest)
```

## 客户端操作

| 操作 | 描述 |
|-----------|-------------|
| `list_repository_names` | 列出所有存储库 |
| `get_repository_properties` | 获取存储库元数据 |
| `delete_repository` | 删除存储库和所有镜像 |
| `list_tag_properties` | 列出存储库中的标签 |
| `get_tag_properties` | 获取标签元数据 |
| `delete_tag` | 删除特定标签 |
| `list_manifest_properties` | 列出存储库中的清单 |
| `get_manifest_properties` | 获取清单元数据 |
| `delete_manifest` | 按摘要删除清单 |
| `download_manifest` | 下载清单内容 |
| `download_blob` | 下载层 blob |

## 最佳实践

1. **在生产中使用 Entra ID** 进行认证
2. **按摘要删除**而不是标签以避免孤立镜像
3. **锁定生产镜像**（设置 can_delete=False）
4. **定期清理无标签清单**
5. **对高吞吐量操作使用异步客户端**
6. **按最后更新时间排序**以查找最新/旧镜像
7. **在删除前检查 manifest.tags**以避免删除带标签的镜像

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
