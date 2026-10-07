---
name: ai-ml
description: "涵盖 LLM 应用开发、RAG 实现、代理架构、ML 管道和 AI 驱动功能的 AI 和机器学习工作流。"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# AI/ML 工作流包

## 概述

用于构建 LLM 应用、实现 RAG 系统、创建 AI 代理和开发机器学习管道的综合 AI/ML 工作流。此包协调用于生产 AI 开发的技能。

## 何时使用此工作流

在以下情况下使用此工作流：
- 构建由 LLM 驱动的应用
- 实现 RAG（检索增强生成）
- 创建 AI 代理
- 开发 ML 管道
- 向应用添加 AI 功能
- 设置 AI 可观测性

## 工作流阶段

### 阶段 1：AI 应用设计

#### 要调用的技能
- `ai-product` - AI 产品开发
- `ai-engineer` - AI 工程
- `ai-agents-architect` - 代理架构
- `llm-app-patterns` - LLM 模式

#### 行动
1. 定义 AI 用例
2. 选择合适的模型
3. 设计系统架构
4. 规划数据流
5. 定义成功指标

#### 复制粘贴提示
```
使用 @ai-product 设计 AI 驱动功能
```

```
使用 @ai-agents-architect 设计多代理系统
```

### 阶段 2：LLM 集成

#### 要调用的技能
- `llm-application-dev-ai-assistant` - AI 助手开发
- `llm-application-dev-langchain-agent` - LangChain 代理
- `llm-application-dev-prompt-optimize` - 提示工程
- `gemini-api-dev` - Gemini API

#### 行动
1. 选择 LLM 提供者
2. 设置 API 访问
3. 实现提示模板
4. 配置模型参数
5. 添加流支持
6. 实现错误处理

#### 复制粘贴提示
```
使用 @llm-application-dev-ai-assistant 构建对话 AI
```

```
使用 @llm-application-dev-langchain-agent 创建 LangChain 代理
```

```
使用 @llm-application-dev-prompt-optimize 优化提示
```

### 阶段 3：RAG 实现

#### 要调用的技能
- `rag-engineer` - RAG 工程
- `rag-implementation` - RAG 实现
- `embedding-strategies` - 嵌入选择
- `vector-database-engineer` - 向量数据库
- `similarity-search-patterns` - 相似度搜索
- `hybrid-search-implementation` - 混合搜索

#### 行动
1. 设计数据管道
2. 选择嵌入模型
3. 设置向量数据库
4. 实现分块策略
5. 配置检索
6. 添加重新排序
7. 实现缓存

#### 复制粘贴提示
```
使用 @rag-engineer 设计 RAG 管道
```

```
使用 @vector-database-engineer 设置向量搜索
```

```
使用 @embedding-strategies 选择最优嵌入
```

### 阶段 4：AI 代理开发

#### 要调用的技能
- `autonomous-agents` - 自主代理模式
- `autonomous-agent-patterns` - 代理模式
- `crewai` - CrewAI 框架
- `langgraph` - LangGraph
- `multi-agent-patterns` - 多代理系统
- `computer-use-agents` - 计算机使用代理

#### 行动
1. 设计代理架构
2. 定义代理角色
3. 实现工具集成
4. 设置内存系统
5. 配置协调
6. 添加人类在环系统

#### 复制粘贴提示
```
使用 @crewai 构建基于角色的多代理系统
```

```
使用 @langgraph 创建有状态 AI 工作流
```

```
使用 @autonomous-agents 设计自主代理
```

### 阶段 5：ML 管道开发

#### 要调用的技能
- `ml-engineer` - ML 工程
- `mlops-engineer` - MLOps
- `machine-learning-ops-ml-pipeline` - ML 管道
- `ml-pipeline-workflow` - ML 工作流
- `data-engineer` - 数据工程

#### 行动
1. 设计 ML 管道
2. 设置数据处理
3. 实现模型训练
4. 配置评估
5. 设置模型注册表
6. 部署模型

#### 复制粘贴提示
```
使用 @ml-engineer 构建机器学习管道
```

```
使用 @mlops-engineer 设置 MLOps 基础设施
```

### 阶段 6：AI 可观测性

#### 要调用的技能
- `langfuse` - Langfuse 可观测性
- `manifest` - Manifest 遥测
- `evaluation` - AI 评估
- `llm-evaluation` - LLM 评估

#### 行动
1. 设置追踪
2. 配置日志
3. 实现评估
4. 监控性能
5. 追踪成本
6. 设置警报

#### 复制粘贴提示
```
使用 @langfuse 设置 LLM 可观测性
```

```
使用 @evaluation 创建评估框架
```

### 阶段 7：AI 安全

#### 要调用的技能
- `prompt-engineering` - 提示安全
- `security-scanning-security-sast` - 安全扫描

#### 行动
1. 实现输入验证
2. 添加输出过滤
3. 配置速率限制
4. 设置访问控制
5. 监控滥用
6. 实现审计日志

## AI 开发检查清单

### LLM 集成
- [ ] API 密钥已保护
- [ ] 速率限制已配置
- [ ] 错误处理已实现
- [ ] 流支持已启用
- [ ] 令牌使用量已追踪

### RAG 系统
- [ ] 数据管道正常工作
- [ ] 嵌入已生成
- [ ] 向量搜索已优化
- [ ] 检索准确性已测试
- [ ] 缓存已实现

### AI 代理
- [ ] 代理角色已定义
- [ ] 工具已集成
- [ ] 内存正常工作
- [ ] 协调已测试
- [ ] 错误处理稳健

### 可观测性
- [ ] 追踪已启用
- [ ] 指标已收集
- [ ] 评估正在运行
- [ ] 警报已配置
- [ ] 仪表板已创建

## 质量关口

- [ ] 所有 AI 功能已测试
- [ ] 性能基准已达成
- [ ] 安全措施已就位
- [ ] 可观测性已配置
- [ ] 文档已完成

## 相关工作流包

- `development` - 应用开发
- `database` - 数据管理
- `cloud-devops` - 基础设施
- `testing-qa` - AI 测试

## 限制
- 仅在任务与上述描述范围明确匹配时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并寻求澄清。
