---
name: azure-appconfiguration-py
description: Azure 应用配置 SDK for Python。用于集中配置管理、功能标志和动态设置。
risk: critical
source: community
date_added: '2026-02-27'
---

# Azure App Configuration SDK for Python

具有功能标志和动态设置的集中配置管理。

## 安装

```bash
pip install azure-appconfiguration
```

## 环境变量

```bash
AZURE_APPCONFIGURATION_CONNECTION_STRING=Endpoint=https://<name>.azconfig.io;Id=...;Secret=...
# 或使用 Entra ID：
AZURE_APPCONFIGURATION_ENDPOINT=https://<name>.azconfig.io
```

## 认证

### 连接字符串

```python
from azure.appconfiguration import AzureAppConfigurationClient

client = AzureAppConfigurationClient.from_connection_string(
    os.environ["AZURE_APPCONFIGURATION_CONNECTION_STRING"]
)
```

### Entra ID

```python
from azure.appconfiguration import AzureAppConfigurationClient
from azure.identity import DefaultAzureCredential

client = AzureAppConfigurationClient(
    base_url=os.environ["AZURE_APPCONFIGURATION_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## 配置设置

### 获取设置

```python
setting = client.get_configuration_setting(key="app:settings:message")
print(f"{setting.key} = {setting.value}")
```

### 通过标签获取

```python
# 标签允许特定于环境的值
setting = client.get_configuration_setting(
    key="app:settings:message",
    label="production"
)
```

### 设置配置

```python
from azure.appconfiguration import ConfigurationSetting

setting = ConfigurationSetting(
    key="app:settings:message",
    value="Hello, World!",
    label="development",
    content_type="text/plain",
    tags={"environment": "dev"}
)

client.set_configuration_setting(setting)
```

### 删除设置

```python
client.delete_configuration_setting(
    key="app:settings:message",
    label="development"
)
```

## 列出设置

### 所有设置

```python
settings = client.list_configuration_settings()
for setting in settings:
    print(f"{setting.key} [{setting.label}] = {setting.value}")
```

### 按键前缀筛选

```python
settings = client.list_configuration_settings(
    key_filter="app:settings:*"
)
```

### 按标签筛选

```python
settings = client.list_configuration_settings(
    label_filter="production"
)
```

## 功能标志

### 设置功能标志

```python
from azure.appconfiguration import ConfigurationSetting
import json

feature_flag = ConfigurationSetting(
    key=".appconfig.featureflag/beta-feature",
    value=json.dumps({
        "id": "beta-feature",
        "enabled": True,
        "conditions": {
            "client_filters": []
        }
    }),
    content_type="application/vnd.microsoft.appconfig.ff+json;charset=utf-8"
)

client.set_configuration_setting(feature_flag)
```

### 获取功能标志

```python
setting = client.get_configuration_setting(
    key=".appconfig.featureflag/beta-feature"
)
flag_data = json.loads(setting.value)
print(f"Feature enabled: {flag_data['enabled']}")
```

### 列出功能标志

```python
flags = client.list_configuration_settings(
    key_filter=".appconfig.featureflag/*"
)
for flag in flags:
    data = json.loads(flag.value)
    print(f"{data['id']}: {'enabled' if data['enabled'] else 'disabled'}")
```

## 只读设置

```python
# 设置为只读
client.set_read_only(
    configuration_setting=setting,
    read_only=True
)

# 移除只读
client.set_read_only(
    configuration_setting=setting,
    read_only=False
)
```

## 快照

### 创建快照

```python
from azure.appconfiguration import ConfigurationSnapshot, ConfigurationSettingFilter

snapshot = ConfigurationSnapshot(
    name="v1-snapshot",
    filters=[
        ConfigurationSettingFilter(key="app:*", label="production")
    ]
)

created = client.begin_create_snapshot(
    name="v1-snapshot",
    snapshot=snapshot
).result()
```

### 列出快照设置

```python
settings = client.list_configuration_settings(
    snapshot_name="v1-snapshot"
)
```

## 异步客户端

```python
from azure.appconfiguration.aio import AzureAppConfigurationClient
from azure.identity.aio import DefaultAzureCredential

async def main():
    credential = DefaultAzureCredential()
    client = AzureAppConfigurationClient(
        base_url=endpoint,
        credential=credential
    )
    
    setting = await client.get_configuration_setting(key="app:message")
    print(setting.value)
    
    await client.close()
    await credential.close()
```

## 客户端操作

| 操作 | 描述 |
|-----------|-------------|
| `get_configuration_setting` | 获取单个设置 |
| `set_configuration_setting` | 创建或更新设置 |
| `delete_configuration_setting` | 删除设置 |
| `list_configuration_settings` | 使用筛选器列出 |
| `set_read_only` | 锁定/解锁设置 |
| `begin_create_snapshot` | 创建时间点快照 |
| `list_snapshots` | 列出所有快照 |

## 最佳实践

1. **使用标签**进行环境分离（开发、暂存、生产）
2. **使用键前缀**进行逻辑分组（app:database:*、app:cache:*）
3. **使生产设置只读**以防止意外更改
4. **在部署前创建快照**以具有回滚功能
5. **在生产中使用 Entra ID** 而不是连接字符串
6. **在长时间运行的应用程序中定期刷新设置**
7. **使用功能标志**进行渐进式推出和 A/B 测试

## 何时使用

该技能适用于执行上述概述中描述的工作流程或操作。

## 限制

- 仅在任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
