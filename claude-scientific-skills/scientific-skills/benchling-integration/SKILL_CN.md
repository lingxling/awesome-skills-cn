---
name: benchling-integration
description: Benchling R&D 平台集成。通过 API 访问注册表（DNA、蛋白质）、库存、ELN 条目、工作流程，构建 Benchling 应用，查询数据仓库，用于实验室数据管理自动化。
license: Unknown
compatibility: 需要 Benchling 账户和 API 密钥
metadata:
    skill-author: K-Dense Inc.
---

# Benchling 集成

## 概述

Benchling 是生命科学研发的云平台。通过 Python SDK 和 REST API 以编程方式访问注册表实体（DNA、蛋白质）、库存、电子实验室笔记本和工作流程。

## 何时使用此技能

此技能应在以下情况使用：
- 使用 Benchling 的 Python SDK 或 REST API
- 管理生物序列（DNA、RNA、蛋白质）和注册表实体
- 自动化库存操作（样本、容器、位置、转移）
- 创建或查询电子实验室笔记本条目
- 构建工作流程自动化或 Benchling 应用
- 在 Benchling 和外部系统之间同步数据
- 查询 Benchling 数据仓库进行分析
- 使用 AWS EventBridge 设置事件驱动的集成

## 核心能力

### 1. 身份验证和设置

**Python SDK 安装：**
```python
# 稳定版本
uv pip install benchling-sdk
# 或使用 Poetry
poetry add benchling-sdk
```

**身份验证方法：**

API 密钥身份验证（推荐用于脚本）：
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key")
)
```

OAuth 客户端凭据（用于应用）：
```python
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2

auth_method = ClientCredentialsOAuth2(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=auth_method
)
```

**关键点：**
- API 密钥从 Benchling 中的个人资料设置获取
- 安全存储凭据（使用环境变量或密码管理器）
- 所有 API 请求都需要 HTTPS
- 身份验证权限镜像 UI 中的用户权限

有关详细的身份验证信息，包括 OIDC 和安全最佳实践，请参阅 `references/authentication.md`。

### 2. 注册表和实体管理

注册表实体包括 DNA 序列、RNA 序列、AA 序列、自定义实体和混合物。SDK 提供类型化类用于创建和管理这些实体。

**创建 DNA 序列：**
```python
from benchling_sdk.models import DnaSequenceCreate

sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="My Plasmid",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        schema_id="ts_abc123",  # 可选
        fields=benchling.models.fields({"gene_name": "GFP"})
    )
)
```

**注册表注册：**

要在创建时直接注册实体：
```python
sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="My Plasmid",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        entity_registry_id="src_abc123",  # 要注册的注册表
        naming_strategy="NEW_IDS"  # 或 "IDS_FROM_NAMES"
    )
)
```

**重要：** 使用 `entity_registry_id` 或 `naming_strategy`，切勿同时使用两者。

**更新实体：**
```python
from benchling_sdk.models import DnaSequenceUpdate

updated = benchling.dna_sequences.update(
    sequence_id="seq_abc123",
    dna_sequence=DnaSequenceUpdate(
        name="Updated Plasmid Name",
        fields=benchling.models.fields({"gene_name": "mCherry"})
    )
)
```

未指定的字段保持不变，允许部分更新。

**列出和分页：**
```python
# 列出所有 DNA 序列（返回生成器）
sequences = benchling.dna_sequences.list()
for page in sequences:
    for seq in page:
        print(f"{seq.name} ({seq.id})")

# 检查总数
total = sequences.estimated_count()
```

**关键操作：**
- 创建：`benchling.<entity_type>.create()`
- 读取：`benchling.<entity_type>.get(id)` 或 `.list()`
- 更新：`benchling.<entity_type>.update(id, update_object)`
- 归档：`benchling.<entity_type>.archive(id)`

实体类型：`dna_sequences`、`rna_sequences`、`aa_sequences`、`custom_entities`、`mixtures`

有关综合 SDK 参考和高级模式，请参阅 `references/sdk_reference.md`。

### 3. 库存管理

在 Benchling 库存系统中管理物理样本、容器、盒子和位置。

**创建容器：**
```python
from benchling_sdk.models import ContainerCreate

container = benchling.containers.create(
    ContainerCreate(
        name="Sample Tube 001",
        schema_id="cont_schema_abc123",
        parent_storage_id="box_abc123",  # 可选
        fields=benchling.models.fields({"concentration": "100 ng/μL"})
    )
)
```

**管理盒子：**
```python
from benchling_sdk.models import BoxCreate

box = benchling.boxes.create(
    BoxCreate(
        name="Freezer Box A1",
        schema_id="box_schema_abc123",
        parent_storage_id="loc_abc123"
    )
)
```

**转移项目：**
```python
# 将容器转移到新位置
transfer = benchling.containers.transfer(
    container_id="cont_abc123",
    destination_id="box_xyz789"
)
```

**关键库存操作：**
- 创建容器、盒子、位置、板
- 更新库存项目属性
- 在位置之间转移项目
- 签入/签出项目
- 批量转移的批量操作

### 4. 笔记本和文档

与电子实验室笔记本（ELN）条目、方案和模板交互。

**创建笔记本条目：**
```python
from benchling_sdk.models import EntryCreate

entry = benchling.entries.create(
    EntryCreate(
        name="Experiment 2025-10-20",
        folder_id="fld_abc123",
        schema_id="entry_schema_abc123",
        fields=benchling.models.fields({"objective": "Test gene expression"})
    )
)
```

**将实体链接到条目：**
```python
# 在条目中添加对实体的引用
entry_link = benchling.entry_links.create(
    entry_id="entry_abc123",
    entity_id="seq_xyz789"
)
```

**关键笔记本操作：**
- 创建和更新实验室笔记本条目
- 管理条目模板
- 将实体和结果链接到条目
- 导出条目以供文档记录

### 5. 工作流程和自动化

使用 Benchling 的工作流程系统自动化实验室流程。

**创建工作流程任务：**
```python
from benchling_sdk.models import WorkflowTaskCreate

task = benchling.workflow_tasks.create(
    WorkflowTaskCreate(
        name="PCR Amplification",
        workflow_id="wf_abc123",
        assignee_id="user_abc123",
        fields=benchling.models.fields({"template": "seq_abc123"})
    )
)
```

**更新任务状态：**
```python
from benchling_sdk.models import WorkflowTaskUpdate

updated_task = benchling.workflow_tasks.update(
    task_id="task_abc123",
    workflow_task=WorkflowTaskUpdate(
        status_id="status_complete_abc123"
    )
)
```

**异步操作：**

某些操作是异步的并返回任务：
```python
# 等待任务完成
from benchling_sdk.helpers.tasks import wait_for_task

result = wait_for_task(
    benchling,
    task_id="task_abc123",
    interval_wait_seconds=2,
    max_wait_seconds=300
)
```

**关键工作流程操作：**
- 创建和管理工作流程任务
- 更新任务状态和分配
- 异步执行批量操作
- 监控任务进度

### 6. 事件和集成

使用 AWS EventBridge 订阅 Benchling 事件以进行实时集成。

**事件类型：**
- 实体创建、更新、归档
- 库存转移
- 工作流程任务状态更改
- 条目创建和更新
- 结果注册

**集成模式：**
1. 在 Benchling 设置中配置事件路由到 AWS EventBridge
2. 创建 EventBridge 规则以过滤事件
3. 将事件路由到 Lambda 函数或其他目标
4. 处理事件并更新外部系统

**用例：**
- 将 Benchling 数据同步到外部数据库
- 在工作流程完成时触发下游流程
- 在实体更改时发送通知
- 审计跟踪日志记录

有关事件架构和配置，请参阅 Benchling 事件文档。

### 7. 数据仓库和分析

通过数据仓库使用 SQL 查询历史 Benchling 数据。

**访问方法：**
Benchling 数据仓库提供对 Benchling 数据的 SQL 访问，用于分析和报告。使用提供的凭据通过标准 SQL 客户端连接。

**常见查询：**
- 聚合实验结果
- 分析库存趋势
- 生成合规报告
- 导出数据以进行外部分析

**与分析工具集成：**
- Jupyter 笔记本用于交互式分析
- BI 工具（Tableau、Looker、PowerBI）
- 自定义仪表板

## 最佳实践

### 错误处理

SDK 自动重试失败的请求：
```python
# 自动重试 429、502、503、504 状态代码
# 最多 5 次重试，具有指数退避
# 如需要，自定义重试行为
from benchling_sdk.retry import RetryStrategy

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key"),
    retry_strategy=RetryStrategy(max_retries=3)
)
```

### 分页效率

使用生成器进行内存高效分页：
```python
# 基于生成器的迭代
for page in benchling.dna_sequences.list():
    for sequence in page:
        process(sequence)

# 检查估计计数而不加载所有页面
total = benchling.dna_sequences.list().estimated_count()
```

### 架构字段助手

使用 `fields()` 助手处理自定义架构字段：
```python
# 将 dict 转换为 Fields 对象
custom_fields = benchling.models.fields({
    "concentration": "100 ng/μL",
    "date_prepared": "2025-10-20",
    "notes": "High quality prep"
})
```

### 前向兼容性

SDK 优雅地处理未知枚举值和类型：
- 保留未知枚举值
- 无法识别的多态类型返回 `UnknownType`
- 允许使用较新的 API 版本

### 安全考虑

- 切勿将 API 密钥提交到版本控制
- 使用环境变量存储凭据
- 如果密钥泄露，请轮换密钥
- 为应用授予最小必要权限
- 对多用户场景使用 OAuth

## 资源

### references/

详细的参考文档，用于深入信息：

- **authentication.md** - 综合身份验证指南，包括 OIDC、安全最佳实践和凭据管理
- **sdk_reference.md** - 详细的 Python SDK 参考，包含高级模式、示例和所有实体类型
- **api_endpoints.md** - REST API 端点参考，用于在没有 SDK 的情况下直接进行 HTTP 调用

根据需要加载这些参考以获取特定的集成要求。

### scripts/

此技能当前包含示例脚本，可以删除或替换为特定 Benchling 工作流程的自定义自动化脚本。

## 常见用例

**1. 批量实体导入：**
```python
# 从 FASTA 文件导入多个序列
from Bio import SeqIO

for record in SeqIO.parse("sequences.fasta", "fasta"):
    benchling.dna_sequences.create(
        DnaSequenceCreate(
            name=record.id,
            bases=str(record.seq),
            is_circular=False,
            folder_id="fld_abc123"
        )
    )
```

**2. 库存审计：**
```python
# 列出特定位置中的所有容器
containers = benchling.containers.list(
    parent_storage_id="box_abc123"
)

for page in containers:
    for container in page:
        print(f"{container.name}: {container.barcode}")
```

**3. 工作流程自动化：**
```python
# 更新工作流程的所有待处理任务
tasks = benchling.workflow_tasks.list(
    workflow_id="wf_abc123",
    status="pending"
)

for page in tasks:
    for task in page:
        # 执行自动检查
        if auto_validate(task):
            benchling.workflow_tasks.update(
                task_id=task.id,
                workflow_task=WorkflowTaskUpdate(
                    status_id="status_complete"
                )
            )
```

**4. 数据导出：**
```python
# 导出具有特定属性的所有序列
sequences = benchling.dna_sequences.list()
export_data = []

for page in sequences:
    for seq in page:
        if seq.schema_id == "target_schema_id":
            export_data.append({
                "id": seq.id,
                "name": seq.name,
                "bases": seq.bases,
                "length": len(seq.bases)
            })

# 保存到 CSV 或数据库
import csv
with open("sequences.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=export_data[0].keys())
    writer.writeheader()
    writer.writerows(export_data)
```

## 其他资源

- **官方文档：** https://docs.benchling.com
- **Python SDK 参考：** https://benchling.com/sdk-docs/
- **API 参考：** https://benchling.com/api/reference
- **支持：** [email protected]
