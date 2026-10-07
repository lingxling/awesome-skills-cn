---
name: agents-v2-py
description: "使用 Azure AI Projects SDK(ImageBasedHostedAgentDefinition)构建基于容器的 Foundry 智能体。在 Azure AI Foundry 中创建带自定义容器镜像的托管智能体时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

## 兼容性与维护

这是 `hosted-agents-v2-py` 的兼容性别名;当没有现有合约强制要求使用这个 ID 时,新的引用应使用那个 ID。完整的说明和支持文件仍保留在本地,以便现有安装能够继续离线使用。这是同一套共享流程,而非一项附加能力。
当现有的清单文件或客户端配置使用了此 ID 时,请保留这个可调用的 ID。
于 2026-09-05 在 AAS 中修改;保留原始元数据及许可声明。

# Azure AI 托管智能体(Python)

使用 Azure AI Projects SDK 中的 `ImageBasedHostedAgentDefinition` 构建基于容器的托管智能体。

## 安装

```bash
pip install 'azure-ai-projects>=2.0.0b3,<3' azure-identity
```

这些是预览阶段的 SDK v2 草稿示例。在正式部署前,请核实实际安装的版本以及当前的 Azure 托管智能体文档;一个宽泛的版本范围并不等同于一次集成测试。

## 环境变量

```bash
AZURE_AI_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
```

## 前提条件

创建托管智能体之前:

1. **容器镜像** —— 构建并推送到 Azure 容器注册表(ACR)
2. **ACR 拉取权限** —— 为你的项目的托管身份(managed identity)授予 ACR 上的 `AcrPull` 角色
3. **Capability Host** —— 账户级的 capability host,且 `enablePublicHostingEnvironment=true`
4. **SDK 版本** —— 确保 `azure-ai-projects>=2.0.0b3`

## 身份验证

针对目标租户/订阅使用经批准的 Azure 凭据流程;此草稿示例使用 `DefaultAzureCredential`:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

import os

credential = DefaultAzureCredential()
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=credential
)
```

## 核心工作流

### 1. 导入

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)
```

### 2. 创建托管智能体

```python
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

agent = client.agents.create_version(
    agent_name="my-hosted-agent",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[
            ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")
        ],
        cpu="1",
        memory="2Gi",
        image="myregistry.azurecr.io/my-agent:latest",
        tools=[{"type": "code_interpreter"}],
        environment_variables={
            "AZURE_AI_PROJECT_ENDPOINT": os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            "MODEL_NAME": "gpt-4o-mini"
        }
    )
)

print(f"Created agent: {agent.name} (version: {agent.version})")
```

### 3. 列出智能体版本

```python
versions = client.agents.list_versions(agent_name="my-hosted-agent")
for version in versions:
    print(f"Version: {version.version}, State: {version.state}")
```

### 4. 删除智能体版本

```python
client.agents.delete_version(
    agent_name="my-hosted-agent",
    version=agent.version
)
```

## ImageBasedHostedAgentDefinition 参数

| 参数 | 类型 | 是否必需 | 说明 |
|-----------|------|----------|-------------|
| `container_protocol_versions` | `list[ProtocolVersionRecord]` | 是 | 该智能体支持的协议版本 |
| `image` | `str` | 是 | 完整的容器镜像路径(registry/image:tag) |
| `cpu` | `str` | 否 | CPU 分配(例如 "1"、"2") |
| `memory` | `str` | 否 | 内存分配(例如 "2Gi"、"4Gi") |
| `tools` | `list[dict]` | 否 | 该智能体可用的工具 |
| `environment_variables` | `dict[str, str]` | 否 | 容器的环境变量 |

## 协议版本

`container_protocol_versions` 参数指定你的智能体支持哪些协议:

```python
from azure.ai.projects.models import ProtocolVersionRecord, AgentProtocol

# RESPONSES 协议 —— 标准智能体响应
container_protocol_versions=[
    ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")
]
```

**可用协议:**
| 协议 | 说明 |
|----------|-------------|
| `AgentProtocol.RESPONSES` | 用于智能体交互的标准响应协议 |

## 资源分配

为你的容器指定 CPU 和内存:

```python
definition=ImageBasedHostedAgentDefinition(
    container_protocol_versions=[...],
    image="myregistry.azurecr.io/my-agent:latest",
    cpu="2",      # 2 个 CPU 核心
    memory="4Gi"  # 4 GiB 内存
)
```

**示意性的资源规格;部署前请核实区域/SKU 限制:**
| 资源 | 最小值 | 最大值 | 默认值 |
|----------|-----|-----|---------|
| CPU | 0.5 | 4 | 1 |
| 内存 | 1Gi | 8Gi | 2Gi |

## 工具配置

为你的托管智能体添加工具:

### Code Interpreter(代码解释器)

```python
tools=[{"type": "code_interpreter"}]
```

### MCP 工具

```python
tools=[
    {"type": "code_interpreter"},
    {
        "type": "mcp",
        "server_label": "my-mcp-server",
        "server_url": "https://my-mcp-server.example.com"
    }
]
```

### 多个工具

```python
tools=[
    {"type": "code_interpreter"},
    {"type": "file_search"},
    {
        "type": "mcp",
        "server_label": "custom-tool",
        "server_url": "https://custom-tool.example.com"
    }
]
```

### 环境变量

向你的容器传递配置:

```python
environment_variables={
    "AZURE_AI_PROJECT_ENDPOINT": os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    "MODEL_NAME": "gpt-4o-mini",
    "LOG_LEVEL": "INFO",
    "CUSTOM_CONFIG": "value"
}
```

**最佳实践:** 绝不要硬编码密钥。使用环境变量或 Azure Key Vault。

## 完整示例

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)

def create_hosted_agent():
    """创建一个带自定义容器镜像的托管智能体。"""
    
    client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential()
    )
    
    agent = client.agents.create_version(
        agent_name="data-processor-agent",
        definition=ImageBasedHostedAgentDefinition(
            container_protocol_versions=[
                ProtocolVersionRecord(
                    protocol=AgentProtocol.RESPONSES,
                    version="v1"
                )
            ],
            image="myregistry.azurecr.io/data-processor:v1.0",
            cpu="2",
            memory="4Gi",
            tools=[
                {"type": "code_interpreter"},
                {"type": "file_search"}
            ],
            environment_variables={
                "AZURE_AI_PROJECT_ENDPOINT": os.environ["AZURE_AI_PROJECT_ENDPOINT"],
                "MODEL_NAME": "gpt-4o-mini",
                "MAX_RETRIES": "3"
            }
        )
    )
    
    print(f"Created hosted agent: {agent.name}")
    print(f"Version: {agent.version}")
    print(f"State: {agent.state}")
    
    return agent

if __name__ == "__main__":
    create_hosted_agent()
```

## 异步模式

```python
import os
from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)

async def create_hosted_agent_async():
    """异步创建一个托管智能体。"""
    
    async with DefaultAzureCredential() as credential:
        async with AIProjectClient(
            endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            credential=credential
        ) as client:
            agent = await client.agents.create_version(
                agent_name="async-agent",
                definition=ImageBasedHostedAgentDefinition(
                    container_protocol_versions=[
                        ProtocolVersionRecord(
                            protocol=AgentProtocol.RESPONSES,
                            version="v1"
                        )
                    ],
                    image="myregistry.azurecr.io/async-agent:latest",
                    cpu="1",
                    memory="2Gi"
                )
            )
            return agent
```

## 常见错误

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `ImagePullBackOff` | ACR 拉取权限被拒绝 | 为项目的托管身份授予 `AcrPull` 角色 |
| `InvalidContainerImage` | 未找到镜像 | 核实镜像路径和标签在 ACR 中确实存在 |
| `CapabilityHostNotFound` | 未配置 capability host | 创建账户级的 capability host |
| `ProtocolVersionNotSupported` | 协议版本无效 | 使用 `AgentProtocol.RESPONSES` 配合版本号 `"v1"` |

## 最佳实践

1. **为镜像打版本号** —— 在生产环境中使用具体的标签,而不是 `latest`
2. **最小化资源** —— 从最小的 CPU/内存起步,按需扩容
3. **环境变量** —— 用于所有配置,绝不硬编码
4. **错误处理** —— 用 try/except 包裹智能体创建逻辑
5. **清理** —— 删除未使用的智能体版本以释放资源

## 参考链接

- [Azure AI Projects SDK](https://pypi.org/project/azure-ai-projects/)
- [托管智能体文档](https://learn.microsoft.com/azure/ai-services/agents/how-to/hosted-agents)
- [Azure 容器注册表](https://learn.microsoft.com/azure/container-registry/)

## 何时使用
用于审查或创建明确请求的、基于容器的 Foundry 托管智能体。首先确认镜像摘要(digest)、订阅/租户、区域、服务可用性、权限和成本范围。创建智能体、授予角色以及删除版本都属于云端写操作,只能在用户授权的范围内执行。

## 审查示例
给定一个已固定版本的容器镜像和测试项目,先检查 SDK 的模型字段和注册表拉取权限,然后准备创建请求。只有在获得授权的情况下才进行部署,并记录下确切返回的版本号和观察到的健康状态。不要把删除无关版本当作日常清理操作来做。预期的结果是一份版本明确的凭证记录,而不是一次想当然的部署。

## 局限性
- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出当作特定环境验证、测试或专家审查的替代品。
- 如果所需的输入、权限、安全边界或成功标准缺失,应停下来并请求澄清。
