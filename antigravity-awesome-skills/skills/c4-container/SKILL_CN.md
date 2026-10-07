---
name: c4-container
description: 专业 C4 容器级文档专家。
risk: none
source: community
date_added: '2026-02-27'
---

# C4 容器级：系统部署

## 何时使用此技能

- 处理 C4 容器级：系统部署任务或工作流时
- 需要关于 C4 容器级：系统部署的指导、最佳实践或检查清单时

## 何时不使用此技能

- 任务与 C4 容器级：系统部署无关时
- 你需要不同的域或超出此范围的工具时

## 说明

- 澄清目标、约束和所需的输入。
- 应用相关的最佳实践并验证结果。
- 提供可操作的步骤和验证。
- 如果需要详细示例，打开 `resources/implementation-playbook.md`。

## 容器

### [容器名称]

- **名称**：[容器名称]
- **描述**：[容器目的和部署的简短描述]
- **类型**：[Web 应用程序、API、数据库、消息队列等]
- **技术**：[主要技术：Node.js、Python、PostgreSQL、Redis 等]
- **部署**：[Docker、Kubernetes、云服务等]

## 目的

[详细描述此容器的功能以及它是如何部署的]

## 组件

此容器部署以下组件：

- [组件名称]：[描述]
  - 文档：c4-component-name.md

## 接口

### [API/接口名称]

- **协议**：[REST/GraphQL/gRPC/事件等]
- **描述**：[此接口提供的内容]
- **规范**：[指向 OpenAPI/Swagger/API 规范文件的链接]
- **端点**：
  - `GET /api/resource` - [描述]
  - `POST /api/resource` - [描述]

## 依赖

### 使用的容器

- [容器名称]：[它是如何被使用的、通信协议]

### 外部系统

- [外部系统]：[它是如何被使用的、集成类型]

## 基础设施

- **部署配置**：[指向 Dockerfile、K8s 清单等的链接]
- **缩放**：[水平/垂直缩放策略]
- **资源**：[CPU、内存、存储要求]

## 容器图

使用正确的 Mermaid C4Container 语法：

```mermaid
C4Container
    title Container Diagram for [System Name]

    Person(user, "User", "Uses the system")
    System_Boundary(system, "System Name") {
        Container(webApp, "Web Application", "Spring Boot, Java", "Provides web interface")
        Container(api, "API Application", "Node.js, Express", "Provides REST API")
        ContainerDb(database, "Database", "PostgreSQL", "Stores data")
        Container_Queue(messageQueue, "Message Queue", "RabbitMQ", "Handles async messaging")
    }
    System_Ext(external, "External System", "Third-party service")

    Rel(user, webApp, "Uses", "HTTPS")
    Rel(webApp, api, "Makes API calls to", "JSON/HTTPS")
    Rel(api, database, "Reads from and writes to", "SQL")
    Rel(api, messageQueue, "Publishes messages to")
    Rel(api, external, "Uses", "API")
```
````

**关键原则**（来自 [c4model.com](https://c4model.com/diagrams/container)）：

- 显示**高级技术选择**（这是技术细节应该出现的地方）
- 显示**职责如何分布**在各个容器中
- 包括**容器类型**：应用程序、数据库、消息队列、文件系统等
- 显示**容器之间的通信协议**
- 包括**外部系统**（容器与之交互的）

````

## API 规范模板

对于每个容器 API，创建 OpenAPI/Swagger 规范：

```yaml
openapi: 3.1.0
info:
  title: [Container Name] API
  description: [API description]
  version: 1.0.0
servers:
  - url: https://api.example.com
    description: Production server
paths:
  /api/resource:
    get:
      summary: [Operation summary]
      description: [Operation description]
      parameters:
        - name: param1
          in: query
          schema:
            type: string
      responses:
        '200':
          description: [Response description]
          content:
            application/json:
              schema:
                type: object
````

## 示例交互

- "基于部署定义将所有组件合成为容器"
- "将 API 组件映射到容器，并将其 API 记录为 OpenAPI 规范"
- "为微服务体系结构创建容器级文档"
- "将容器接口记录为 Swagger/OpenAPI 规范"
- "分析 Kubernetes 清单并创建容器文档"

## 关键区分

- **vs C4-Component agent**：将组件映射到部署单元；组件 agent 关注逻辑分组
- **vs C4-Context agent**：提供容器级详情；上下文 agent 创建高级系统图
- **vs C4-Code agent**：关注部署体系结构；代码 agent 记录各个代码元素

## 输出示例

合成容器时，提供：

- 清晰的容器边界及其部署原理
- 描述性的容器名称和部署特征
- 带有 OpenAPI/Swagger 规范的完整 API 文档
- 所有包含的组件的链接
- 显示部署体系结构的 Mermaid 容器图
- 部署配置（Dockerfile、K8s 清单等）的链接
- 基础设施要求和缩放考虑因素
- 跨所有容器的一致文档格式

## 限制
- 仅当任务明确与上述范围相符时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
