---
name: azure-cosmos-py
description: Azure Cosmos DB SDK for Python（NoSQL API）。用于文档 CRUD、查询、容器和全球分布式数据。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure Cosmos DB SDK for Python

Azure Cosmos DB NoSQL API 的客户端库 — 全球分布式、多模型数据库。

## 安装

```bash
pip install azure-cosmos azure-identity
```

## 环境变量

```bash
COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
COSMOS_DATABASE=mydb
COSMOS_CONTAINER=mycontainer
```

## 认证

```python
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

credential = DefaultAzureCredential()
endpoint = "https://<account>.documents.azure.com:443/"

client = CosmosClient(url=endpoint, credential=credential)
```

## 客户端层次结构

| 客户端 | 目的 | 获取来源 |
|--------|---------|----------|
| `CosmosClient` | 账户级操作 | 直接实例化 |
| `DatabaseProxy` | 数据库操作 | `client.get_database_client()` |
| `ContainerProxy` | 容器/项目操作 | `database.get_container_client()` |

## 核心工作流

### 设置数据库和容器

```python
# 获取或创建数据库
database = client.create_database_if_not_exists(id="mydb")

# 获取或创建带分区键的容器
container = database.create_container_if_not_exists(
    id="mycontainer",
    partition_key=PartitionKey(path="/category")
)

# 获取现有
database = client.get_database_client("mydb")
container = database.get_container_client("mycontainer")
```

### 创建项目

```python
item = {
    "id": "item-001",           # 必需：在分区内唯一
    "category": "electronics",   # 分区键值
    "name": "Laptop",
    "price": 999.99,
    "tags": ["computer", "portable"]
}

created = container.create_item(body=item)
print(f"Created: {created['id']}")
```

### 读取项目

```python
# 读取需要 id 和分区键
item = container.read_item(
    item="item-001",
    partition_key="electronics"
)
print(f"Name: {item['name']}")
```

### 更新项目（替换）

```python
item = container.read_item(item="item-001", partition_key="electronics")
item["price"] = 899.99
item["on_sale"] = True

updated = container.replace_item(item=item["id"], body=item)
```

### 更新插入项目

```python
# 创建（如果不存在），替换（如果存在）
item = {
    "id": "item-002",
    "category": "electronics",
    "name": "Tablet",
    "price": 499.99
}

result = container.upsert_item(body=item)
```

### 删除项目

```python
container.delete_item(
    item="item-001",
    partition_key="electronics"
)
```

## 查询

### 基本查询

```python
# 在分区内查询（高效）
query = "SELECT * FROM c WHERE c.price < @max_price"
items = container.query_items(
    query=query,
    parameters=[{"name": "@max_price", "value": 500}],
    partition_key="electronics"
)

for item in items:
    print(f"{item['name']}: ${item['price']}")
```

### 跨分区查询

```python
# 跨分区（成本较高，谨慎使用）
query = "SELECT * FROM c WHERE c.price < @max_price"
items = container.query_items(
    query=query,
    parameters=[{"name": "@max_price", "value": 500}],
    enable_cross_partition_query=True
)

for item in items:
    print(item)
```

### 带投影的查询

```python
query = "SELECT c.id, c.name, c.price FROM c WHERE c.category = @category"
items = container.query_items(
    query=query,
    parameters=[{"name": "@category", "value": "electronics"}],
    partition_key="electronics"
)
```

### 读取所有项目

```python
# 读取分区中的所有项目
items = container.read_all_items()  # 跨分区
# 或使用分区键
items = container.query_items(
    query="SELECT * FROM c",
    partition_key="electronics"
)
```

## 分区键

**关键**：始终为高效操作包含分区键。

```python
from azure.cosmos import PartitionKey

# 单个分区键
container = database.create_container_if_not_exists(
    id="orders",
    partition_key=PartitionKey(path="/customer_id")
)

# 分层分区键（预览）
container = database.create_container_if_not_exists(
    id="events",
    partition_key=PartitionKey(path=["/tenant_id", "/user_id"])
)
```

## 吞吐量

```python
# 创建具有预配吞吐量的容器
container = database.create_container_if_not_exists(
    id="mycontainer",
    partition_key=PartitionKey(path="/pk"),
    offer_throughput=400  # RU/s
)

# 读取当前吞吐量
offer = container.read_offer()
print(f"Throughput: {offer.offer_throughput} RU/s")

# 更新吞吐量
container.replace_throughput(throughput=1000)
```

## 异步客户端

```python
from azure.cosmos.aio import CosmosClient
from azure.identity.aio import DefaultAzureCredential

async def cosmos_operations():
    credential = DefaultAzureCredential()
    
    async with CosmosClient(endpoint, credential=credential) as client:
        database = client.get_database_client("mydb")
        container = database.get_container_client("mycontainer")
        
        # 创建
        await container.create_item(body={"id": "1", "pk": "test"})
        
        # 读取
        item = await container.read_item(item="1", partition_key="test")
        
        # 查询
        async for item in container.query_items(
            query="SELECT * FROM c",
            partition_key="test"
        ):
            print(item)

import asyncio
asyncio.run(cosmos_operations())
```

## 错误处理

```python
from azure.cosmos.exceptions import CosmosHttpResponseError

try:
    item = container.read_item(item="nonexistent", partition_key="pk")
except CosmosHttpResponseError as e:
    if e.status_code == 404:
        print("Item not found")
    elif e.status_code == 429:
        print(f"Rate limited. Retry after: {e.headers.get('x-ms-retry-after-ms')}ms")
    else:
        raise
```

## 最佳实践

1. **始终为点读和查询指定分区键**
2. **使用参数化查询**以防止注入并改进缓存
3. **避免跨分区查询**（如果可能）
4. **对幂等写入使用 `upsert_item`**
5. **对高吞吐量场景使用异步客户端**
6. **设计分区键**以实现均匀的数据分布
7. **对单个文档检索使用 `read_item`** 而不是查询

## 参考文件

| 文件 | 内容 |
|------|----------|
| references/partitioning.md | 分区键策略、分层键、热分区检测和缓解 |
| references/query-patterns.md | 查询优化、聚合、分页、事务、变更源 |
| scripts/setup_cosmos_container.py | 用于创建具有分区、吞吐量和索引的容器的 CLI 工具 |

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
