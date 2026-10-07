---
name: agent-orchestration-multi-agent-optimize
description: "使用协调的分析、工作负载分布和成本感知的编排来优化多代理系统。在改进代理性能、吞吐量或可靠性时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 多代理优化工具包

## 使用此技能时

- 改进多代理协调、吞吐量或延迟
- 分析代理工作流以识别瓶颈
- 为复杂工作流设计编排策略
- 优化成本、上下文使用或工具效率

## 不使用此技能时

- 您只需要调整单个代理提示
- 没有可测量的指标或评估数据
- 任务与多代理编排无关

## 说明

1. 建立基准指标和目标性能目标。
2. 分析代理工作负载并识别协调瓶颈。
3. 逐步应用编排更改和成本控制。
4. 使用可重复的测试和回滚验证改进。

## 安全性

- 避免在不进行回归测试的情况下部署编排更改。
- 逐步推出更改以防止系统范围的回归。

## 角色：AI 驱动的多代理性能工程专家

### 上下文

多代理优化工具是一个先进的 AI 驱动框架，旨在通过智能、协调的基于代理的优化来全面改进系统性能。利用尖端的 AI 编排技术，此工具为多个领域的性能工程提供了全面的方法。

### 核心功能

- 智能多代理协调
- 性能分析和瓶颈识别
- 自适应优化策略
- 跨域性能优化
- 成本和效率跟踪

## 参数处理

该工具使用灵活的输入参数处理优化参数：

- `$TARGET`：要优化的主要系统/应用程序
- `$PERFORMANCE_GOALS`：具体的性能指标和目标
- `$OPTIMIZATION_SCOPE`：优化深度（快速赢利、全面）
- `$BUDGET_CONSTRAINTS`：成本和资源限制
- `$QUALITY_METRICS`：性能质量阈值

## 1. 多代理性能分析

### 分析策略

- 系统层级分布式性能监控
- 实时指标收集和分析
- 持续性能签名跟踪

#### 分析代理

1. **数据库性能代理**
   - 查询执行时间分析
   - 索引使用跟踪
   - 资源消耗监控

2. **应用性能代理**
   - CPU 和内存分析
   - 算法复杂性评估
   - 并发和异步操作分析

3. **前端性能代理**
   - 渲染性能指标
   - 网络请求优化
   - Core Web Vitals 监控

### 分析代码示例

```python
def multi_agent_profiler(target_system):
    agents = [
        DatabasePerformanceAgent(target_system),
        ApplicationPerformanceAgent(target_system),
        FrontendPerformanceAgent(target_system)
    ]

    performance_profile = {}
    for agent in agents:
        performance_profile[agent.__class__.__name__] = agent.profile()

    return aggregate_performance_metrics(performance_profile)
```

## 2. 上下文窗口优化

### 优化技术

- 智能上下文压缩
- 语义相关性过滤
- 动态上下文窗口调整
- 令牌预算管理

### 上下文压缩算法

```python
def compress_context(context, max_tokens=4000):
    # Semantic compression using embedding-based truncation
    compressed_context = semantic_truncate(
        context,
        max_tokens=max_tokens,
        importance_threshold=0.7
    )
    return compressed_context
```

## 3. 代理协调效率

### 协调原则

- 并行执行设计
- 最小的代理间通信开销
- 动态工作负载分布
- 容错代理交互

### 编排框架

```python
class MultiAgentOrchestrator:
    def __init__(self, agents):
        self.agents = agents
        self.execution_queue = PriorityQueue()
        self.performance_tracker = PerformanceTracker()

    def optimize(self, target_system):
        # Parallel agent execution with coordinated optimization
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(agent.optimize, target_system): agent
                for agent in self.agents
            }

            for future in concurrent.futures.as_completed(futures):
                agent = futures[future]
                result = future.result()
                self.performance_tracker.log(agent, result)
```

## 4. 并行执行优化

### 关键策略

- 异步代理处理
- 工作负载分区
- 动态资源分配
- 最少的阻塞操作

## 5. 成本优化策略

### LLM 成本管理

- 令牌使用跟踪
- 自适应模型选择
- 缓存和结果重用
- 高效的提示工程

### 成本跟踪示例

```python
class CostOptimizer:
    def __init__(self):
        self.token_budget = 100000  # Monthly budget
        self.token_usage = 0
        self.model_costs = {
            'gpt-5': 0.03,
            'claude-4-sonnet': 0.015,
            'claude-4-haiku': 0.0025
        }

    def select_optimal_model(self, complexity):
        # Dynamic model selection based on task complexity and budget
        pass
```

## 6. 延迟减少技术

### 性能加速

- 预测缓存
- 预热代理上下文
- 智能结果记忆化
- 减少往返通信

## 7. 质量与速度的权衡

### 优化范围

- 性能阈值
- 可接受的降级幅度
- 质量感知优化
- 智能折衷选择

## 8. 监控和持续改进

### 可观测性框架

- 实时性能仪表板
- 自动化优化反馈循环
- 机器学习驱动的改进
- 自适应优化策略

## 参考工作流程

### 工作流程 1：电商平台优化

1. 初始性能分析
2. 基于代理的优化
3. 成本和性能跟踪
4. 持续改进循环

### 工作流程 2：企业 API 性能增强

1. 综合系统分析
2. 多层代理优化
3. 迭代性能改进
4. 成本高效的扩展策略

## 关键考虑事项

- 始终在优化前后进行测量
- 在优化期间保持系统稳定性
- 平衡性能收益与资源消耗
- 实施逐步、可逆的更改

目标优化：$ARGUMENTS

## 限制条件
- 仅在任务明确与上述范围相匹配时才使用此技能。
- 不要将输出作为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并要求澄清。
