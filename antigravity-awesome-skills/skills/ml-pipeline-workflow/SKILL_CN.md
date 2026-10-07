---
name: ml-pipeline-workflow
description: "从数据准备到模型部署的完整端到端 MLOps 管道编排。"
risk: critical
source: community
date_added: "2026-02-27"
---

# ML 管道工作流

从数据准备到模型部署的完整端到端 MLOps 管道编排。

## 不要在以下情况下使用此技能

- 任务与 ml 管道工作流无关
- 您需要此范围之外的不同域或工具

## 说明

- 澄清目标、约束和所需的输入。
- 应用相关的最佳实践并验证结果。
- 提供可操作的步骤和验证。
- 如果需要详细示例，打开 `resources/implementation-playbook.md`。

## 概述

此技能为构建生产 ML 管道提供全面的指导，这些管道处理完整的生命周期：数据摄取 → 准备 → 训练 → 验证 → 部署 → 监控。

## 在以下情况时使用此技能

- 从头开始构建新的 ML 管道
- 为 ML 系统设计工作流编排
- 实施数据 → 模型 → 部署自动化
- 建立可重现的训练工作流
- 创建基于 DAG 的 ML 编排
- 将 ML 组件集成到生产系统中

## 此技能提供的内容

### 核心功能

1. **管道架构**
   - 端到端工作流设计
   - DAG 编排模式 (Airflow、Dagster、Kubeflow)
   - 组件依赖关系和数据流
   - 错误处理和重试策略

2. **数据准备**
   - 数据验证和质量检查
   - 特征工程管道
   - 数据版本控制和血统
   - 训练/验证/测试分割策略

3. **模型训练**
   - 训练作业编排
   - 超参数管理
   - 实验跟踪集成
   - 分布式训练模式

4. **模型验证**
   - 验证框架和指标
   - A/B 测试基础设施
   - 性能回归检测
   - 模型比较工作流

5. **部署自动化**
   - 模型服务模式
   - 金丝雀部署
   - 蓝绿部署策略
   - 回滚机制

### 参考文档

请查看 `references/` 目录以获取详细指南：
- **data-preparation.md** - 数据清理、验证和特征工程
- **model-training.md** - 训练工作流和最佳实践
- **model-validation.md** - 验证策略和指标
- **model-deployment.md** - 部署模式和服务架构

### 资产和模板

`assets/` 目录包含：
- **pipeline-dag.yaml.template** - 工作流编排的 DAG 模板
- **training-config.yaml** - 训练配置模板
- **validation-checklist.md** - 部署前验证检查表

## 使用模式

### 基本管道设置

```python
# 1. 定义管道阶段
stages = [
    "data_ingestion",
    "data_validation",
    "feature_engineering",
    "model_training",
    "model_validation",
    "model_deployment"
]

# 2. 配置依赖关系
# 有关完整示例，请查看 assets/pipeline-dag.yaml.template
```

### 生产工作流

1. **数据准备阶段**
   - 从源摄取原始数据
   - 运行数据质量检查
   - 应用特征转换
   - 对已处理的数据集进行版本控制

2. **训练阶段**
   - 加载版本化的训练数据
   - 执行训练作业
   - 跟踪实验和指标
   - 保存训练的模型

3. **验证阶段**
   - 运行验证测试套件
   - 与基线比较
   - 生成性能报告
   - 批准部署

4. **部署阶段**
   - 打包模型工件
   - 部署到服务基础设施
   - 配置监控
   - 验证生产流量

## 最佳实践

### 管道设计

- **模块化**：每个阶段应该是独立可测试的
- **幂等性**：重新运行阶段应该是安全的
- **可观察性**：在每个阶段记录指标
- **版本控制**：跟踪数据、代码和模型版本
- **故障处理**：实施重试逻辑和警报

### 数据管理

- 使用数据验证库 (Great Expectations、TFX)
- 使用 DVC 或类似工具对数据集进行版本控制
- 记录特征工程转换
- 维护数据血统跟踪

### 模型操作

- 分离训练和服务基础设施
- 使用模型注册表 (MLflow、Weights & Biases)
- 对新模型实施逐步推出
- 监控模型性能漂移
- 维护回滚功能

### 部署策略

- 从影子部署开始
- 将金丝雀版本用于验证
- 实施 A/B 测试基础设施
- 设置自动回滚触发器
- 监控延迟和吞吐量

## 集成点

### 编排工具

- **Apache Airflow**：基于 DAG 的工作流编排
- **Dagster**：基于资产的管道编排
- **Kubeflow Pipelines**：Kubernetes 原生 ML 工作流
- **Prefect**：现代数据流自动化

### 实验跟踪

- MLflow 用于实验跟踪和模型注册表
- Weights & Biases 用于可视化和协作
- TensorBoard 用于训练指标

### 部署平台

- AWS SageMaker 用于托管 ML 基础设施
- Google Vertex AI 用于 GCP 部署
- Azure ML 用于 Azure 云
- Kubernetes + KServe 用于云无关服务

## 渐进式信息披露

从基础开始，逐步增加复杂性：

1. **第 1 级**：简单线性管道（数据 → 训练 → 部署）
2. **第 2 级**：添加验证和监控阶段
3. **第 3 级**：实施超参数调整
4. **第 4 级**：添加 A/B 测试和逐步推出
5. **第 5 级**：多模型管道与集成策略

## 常见模式

### 批处理训练管道

```yaml
# 查看 assets/pipeline-dag.yaml.template
stages:
  - name: data_preparation
    dependencies: []
  - name: model_training
    dependencies: [data_preparation]
  - name: model_evaluation
    dependencies: [model_training]
  - name: model_deployment
    dependencies: [model_evaluation]
```

### 实时特征管道

```python
# 用于实时特征的流处理
# 与批处理训练相结合
# 查看 references/data-preparation.md
```

### 连续训练

```python
# 按计划进行自动重新训练
# 由数据漂移检测触发
# 查看 references/model-training.md
```

## 故障排除

### 常见问题

- **管道故障**：检查依赖关系和数据可用性
- **训练不稳定**：审查超参数和数据质量
- **部署问题**：验证模型工件和服务配置
- **性能下降**：监控数据漂移和模型指标

### 调试步骤

1. 检查每个阶段的管道日志
2. 验证边界处的输入/输出数据
3. 独立测试组件
4. 审查实验跟踪指标
5. 检查模型工件和元数据

## 后续步骤

设置管道后：

1. 探索**超参数调整**技能以进行优化
2. 学习**实验跟踪设置**以使用 MLflow/W&B
3. 审查**模型部署模式**以了解服务策略
4. 使用可观察性工具实施监控

## 相关技能

- **experiment-tracking-setup**：MLflow 和 Weights & Biases 集成
- **hyperparameter-tuning**：自动化超参数优化
- **model-deployment-patterns**：高级部署策略

## 限制
- 仅当任务明确符合上述范围时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
