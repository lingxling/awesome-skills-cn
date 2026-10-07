---
name: azure-storage-blob-py
description: 用于 Python 的 Azure Blob 存储 SDK。用于上传、下载、列出 Blob、管理容器和 Blob 生命周期。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Blob 存储 SDK（Python）

用于 Azure Blob 存储的客户端库 — 非结构化数据的对象存储。

## 安装

```bash
pip install azure-storage-blob azure-identity
```

## 环境变量

```bash
AZURE_STORAGE_ACCOUNT_NAME=<your-storage-account>
# Or use full URL
AZURE_STORAGE_ACCOUNT_URL=https://<account>.blob.core.windows.net
```

## 身份验证

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()
account_url = "https://<account>.blob.core.windows.net"

blob_service_client = BlobServiceClient(account_url, credential=credential)
```

## 客户端层次结构

| 客户端 | 用途 | 获取方式 |
|--------|---------|----------|
| `BlobServiceClient` | 帐户级操作 | 直接实例化 |
| `ContainerClient` | 容器操作 | `blob_service_client.get_container_client()` |
| `BlobClient` | 单个 Blob 操作 | `container_client.get_blob_client()` |

## 核心工作流

### 创建容器

```python
container_client = blob_service_client.get_container_client("mycontainer")
container_client.create_container()
```

### 上传 Blob

```python
# From file path
blob_client = blob_service_client.get_blob_client(
    container="mycontainer",
    blob="sample.txt"
)

with open("./local-file.txt", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

# From bytes/string
blob_client.upload_blob(b"Hello, World!", overwrite=True)

# From stream
import io
stream = io.BytesIO(b"Stream content")
blob_client.upload_blob(stream, overwrite=True)
```

### 下载 Blob

```python
blob_client = blob_service_client.get_blob_client(
    container="mycontainer",
    blob="sample.txt"
)

# To file
with open("./downloaded.txt", "wb") as file:
    download_stream = blob_client.download_blob()
    file.write(download_stream.readall())

# To memory
download_stream = blob_client.download_blob()
content = download_stream.readall()  # bytes

# Read into existing buffer
stream = io.BytesIO()
num_bytes = blob_client.download_blob().readinto(stream)
```

### 列出 Blob

```python
container_client = blob_service_client.get_container_client("mycontainer")

# List all blobs
for blob in container_client.list_blobs():
    print(f"{blob.name} - {blob.size} bytes")

# List with prefix (folder-like)
for blob in container_client.list_blobs(name_starts_with="logs/"):
    print(blob.name)

# Walk blob hierarchy (virtual directories)
for item in container_client.walk_blobs(delimiter="/"):
    if item.get("prefix"):
        print(f"Directory: {item['prefix']}")
    else:
        print(f"Blob: {item.name}")
```

### 删除 Blob

```python
blob_client.delete_blob()

# Delete with snapshots
blob_client.delete_blob(delete_snapshots="include")
```

## 性能调优

```python
# Configure chunk sizes for large uploads/downloads
blob_client = BlobClient(
    account_url=account_url,
    container_name="mycontainer",
    blob_name="large-file.zip",
    credential=credential,
    max_block_size=4 * 1024 * 1024,  # 4 MiB blocks
    max_single_put_size=64 * 1024 * 1024  # 64 MiB single upload limit
)

# Parallel upload
blob_client.upload_blob(data, max_concurrency=4)

# Parallel download
download_stream = blob_client.download_blob(max_concurrency=4)
```

## SAS 令牌

```python
from datetime import datetime, timedelta, timezone
from azure.storage.blob import generate_blob_sas, BlobSasPermissions

sas_token = generate_blob_sas(
    account_name="<account>",
    container_name="mycontainer",
    blob_name="sample.txt",
    account_key="<account-key>",  # Or use user delegation key
    permission=BlobSasPermissions(read=True),
    expiry=datetime.now(timezone.utc) + timedelta(hours=1)
)

# Use SAS token
blob_url = f"https://<account>.blob.core.windows.net/mycontainer/sample.txt?{sas_token}"
```

## Blob 属性和元数据

```python
# Get properties
properties = blob_client.get_blob_properties()
print(f"Size: {properties.size}")
print(f"Content-Type: {properties.content_settings.content_type}")
print(f"Last modified: {properties.last_modified}")

# Set metadata
blob_client.set_blob_metadata(metadata={"category": "logs", "year": "2024"})

# Set content type
from azure.storage.blob import ContentSettings
blob_client.set_http_headers(
    content_settings=ContentSettings(content_type="application/json")
)
```

## 异步客户端

```python
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient

async def upload_async():
    credential = DefaultAzureCredential()
    
    async with BlobServiceClient(account_url, credential=credential) as client:
        blob_client = client.get_blob_client("mycontainer", "sample.txt")
        
        with open("./file.txt", "rb") as data:
            await blob_client.upload_blob(data, overwrite=True)

# Download async
async def download_async():
    async with BlobServiceClient(account_url, credential=credential) as client:
        blob_client = client.get_blob_client("mycontainer", "sample.txt")
        
        stream = await blob_client.download_blob()
        data = await stream.readall()
```

## 最佳实践

1. **使用 DefaultAzureCredential** 而不是连接字符串
2. **使用上下文管理器**用于异步客户端
3. **显式设置 `overwrite=True`** 重新上传时
4. **使用 `max_concurrency`** 用于大文件传输
5. **优先使用 `readinto()`** 而不是 `readall()` 以提高内存效率
6. **使用 `walk_blobs()`** 进行分层列表
7. **为网络提供的 Blob 设置适当的内容类型**

## 使用场景

本技能适用于执行上述概述中描述的工作流或操作。

## 限制条件

- 仅在任务明确符合上述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
