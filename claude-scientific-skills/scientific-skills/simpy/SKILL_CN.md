---
name: simpy
description: Python 中基于过程的离散事件模拟框架。当构建包含过程、队列、资源和基于时间的事件的系统模拟时使用此技能，例如制造系统、服务操作、网络流量、物流或任何实体随时间与共享资源交互的系统。
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# SimPy - 离散事件模拟

## 概述

SimPy 是一个基于标准 Python 的过程式离散事件模拟框架。使用 SimPy 建模系统，其中实体（客户、车辆、数据包等）相互交互并随时间竞争共享资源（服务器、机器、带宽等）。

**核心功能：**
- 使用 Python 生成器函数进行过程建模
- 共享资源管理（服务器、容器、存储）
- 事件驱动的调度和同步
- 与 wall-clock 时间同步的实时模拟
- 全面的监控和数据收集

## 何时使用此技能

当以下情况时使用 SimPy 技能：

1. **建模离散事件系统** - 事件以不规则间隔发生的系统
2. **资源竞争** - 实体竞争有限资源（服务器、机器、人员）
3. **队列分析** - 研究等待线、服务时间和吞吐量
4. **过程优化** - 分析制造、物流或服务过程
5. **网络模拟** - 数据包路由、带宽分配、延迟分析
6. **容量规划** - 确定所需性能的最佳资源水平
7. **系统验证** - 在实施前测试系统行为

**不适合：**
- 固定时间步长的连续模拟（考虑 SciPy ODE 求解器）
- 无资源共享的独立过程
- 纯数学优化（考虑 SciPy optimize）

## 快速入门

### 基本模拟结构

```python
import simpy

def process(env, name):
    """一个简单的等待和打印过程。"""
    print(f'{name} starting at {env.now}')
    yield env.timeout(5)
    print(f'{name} finishing at {env.now}')

# 创建环境
env = simpy.Environment()

# 启动过程
env.process(process(env, 'Process 1'))
env.process(process(env, 'Process 2'))

# 运行模拟
env.run(until=10)
```

### 资源使用模式

```python
import simpy

def customer(env, name, resource):
    """客户请求资源，使用它，然后释放。"""
    with resource.request() as req:
        yield req  # 等待资源
        print(f'{name} got resource at {env.now}')
        yield env.timeout(3)  # 使用资源
        print(f'{name} released resource at {env.now}')

env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

env.process(customer(env, 'Customer 1', server))
env.process(customer(env, 'Customer 2', server))
env.run()
```

## 核心概念

### 1. 环境

模拟环境管理时间和调度事件。

```python
import simpy

# 标准环境（尽可能快地运行）
env = simpy.Environment(initial_time=0)

# 实时环境（与 wall-clock 同步）
import simpy.rt
env_rt = simpy.rt.RealtimeEnvironment(factor=1.0)

# 运行模拟
env.run(until=100)  # 运行到时间 100
env.run()  # 运行直到没有事件剩余
```

### 2. 过程

过程使用 Python 生成器函数（带有 `yield` 语句的函数）定义。

```python
def my_process(env, param1, param2):
    """产生事件以暂停执行的过程。"""
    print(f'Starting at {env.now}')

    # 等待时间流逝
    yield env.timeout(5)

    print(f'Resumed at {env.now}')

    # 等待另一个事件
    yield env.timeout(3)

    print(f'Done at {env.now}')
    return 'result'

# 启动过程
env.process(my_process(env, 'value1', 'value2'))
```

### 3. 事件

事件是过程同步的基本机制。过程产生事件并在这些事件触发时恢复。

**常见事件类型：**
- `env.timeout(delay)` - 等待时间流逝
- `resource.request()` - 请求资源
- `env.event()` - 创建自定义事件
- `env.process(func())` - 作为事件的过程
- `event1 & event2` - 等待所有事件（AllOf）
- `event1 | event2` - 等待任何事件（AnyOf）

## 资源

SimPy 为不同场景提供多种资源类型。有关综合详细信息，请参阅 `references/resources.md`。

### 资源类型摘要

| 资源类型 | 用例 |
|---------------|----------|
| Resource | 有限容量（服务器、机器） |
| PriorityResource | 基于优先级的排队 |
| PreemptiveResource | 高优先级可以中断低优先级 |
| Container | 散装材料（燃料、水） |
| Store | Python 对象存储（FIFO） |
| FilterStore | 选择性项目检索 |
| PriorityStore | 优先级排序项目 |

### 快速参考

```python
import simpy

env = simpy.Environment()

# 基本资源（例如，服务器）
resource = simpy.Resource(env, capacity=2)

# 优先级资源
priority_resource = simpy.PriorityResource(env, capacity=1)

# 容器（例如，油箱）
fuel_tank = simpy.Container(env, capacity=100, init=50)

# 存储（例如，仓库）
warehouse = simpy.Store(env, capacity=10)
```

## 常见模拟模式

### 模式 1：客户-服务器队列

```python
import simpy
import random

def customer(env, name, server):
    arrival = env.now
    with server.request() as req:
        yield req
        wait = env.now - arrival
        print(f'{name} waited {wait:.2f}, served at {env.now}')
        yield env.timeout(random.uniform(2, 4))

def customer_generator(env, server):
    i = 0
    while True:
        yield env.timeout(random.uniform(1, 3))
        i += 1
        env.process(customer(env, f'Customer {i}', server))

env = simpy.Environment()
server = simpy.Resource(env, capacity=2)
env.process(customer_generator(env, server))
env.run(until=20)
```

### 模式 2：生产者-消费者

```python
import simpy

def producer(env, store):
    item_id = 0
    while True:
        yield env.timeout(2)
        item = f'Item {item_id}'
        yield store.put(item)
        print(f'Produced {item} at {env.now}')
        item_id += 1

def consumer(env, store):
    while True:
        item = yield store.get()
        print(f'Consumed {item} at {env.now}')
        yield env.timeout(3)

env = simpy.Environment()
store = simpy.Store(env, capacity=10)
env.process(producer(env, store))
env.process(consumer(env, store))
env.run(until=20)
```

### 模式 3：并行任务执行

```python
import simpy

def task(env, name, duration):
    print(f'{name} starting at {env.now}')
    yield env.timeout(duration)
    print(f'{name} done at {env.now}')
    return f'{name} result'

def coordinator(env):
    # 并行启动任务
    task1 = env.process(task(env, 'Task 1', 5))
    task2 = env.process(task(env, 'Task 2', 3))
    task3 = env.process(task(env, 'Task 3', 4))

    # 等待所有完成
    results = yield task1 & task2 & task3
    print(f'All done at {env.now}')

env = simpy.Environment()
env.process(coordinator(env))
env.run()
```

## 工作流指南

### 步骤 1：定义系统

确定：
- **实体**：什么在系统中移动？（客户、零件、数据包）
- **资源**：约束是什么？（服务器、机器、带宽）
- **过程**：活动是什么？（到达、服务、离开）
- **指标**：要测量什么？（等待时间、利用率、吞吐量）

### 步骤 2：实现过程函数

为每种过程类型创建生成器函数：

```python
def entity_process(env, name, resources, parameters):
    # 到达逻辑
    arrival_time = env.now

    # 请求资源
    with resource.request() as req:
        yield req

        # 服务逻辑
        service_time = calculate_service_time(parameters)
        yield env.timeout(service_time)

    # 离开逻辑
    collect_statistics(env.now - arrival_time)
```

### 步骤 3：设置监控

使用监控工具收集数据。有关综合技术，请参阅 `references/monitoring.md`。

```python
from scripts.resource_monitor import ResourceMonitor

# 创建并监控资源
resource = simpy.Resource(env, capacity=2)
monitor = ResourceMonitor(env, resource, "Server")

# 模拟后
monitor.report()
```

### 步骤 4：运行和分析

```python
# 运行模拟
env.run(until=simulation_time)

# 生成报告
monitor.report()
stats.report()

# 导出数据以进行进一步分析
monitor.export_csv('results.csv')
```

## 高级功能

### 过程交互

过程可以通过事件、过程产生和中断进行交互。有关详细模式，请参阅 `references/process-interaction.md`。

**关键机制：**
- **事件信号**：用于协调的共享事件
- **过程产生**：等待其他过程完成
- **中断**：强制恢复过程以进行抢占

### 实时模拟

将模拟与 wall-clock 时间同步，用于硬件在环或交互式应用程序。请参阅 `references/real-time.md`。

```python
import simpy.rt

env = simpy.rt.RealtimeEnvironment(factor=1.0)  # 1:1 时间映射
# factor=0.5 表示 1 模拟单位 = 0.5 秒（快 2 倍）
```

### 综合监控

监控过程、资源和事件。有关技术，请参阅 `references/monitoring.md`，包括：
- 状态变量跟踪
- 资源猴子补丁
- 事件跟踪
- 统计收集

## 脚本和模板

### basic_simulation_template.py

构建队列模拟的完整模板，包括：
- 可配置参数
- 统计收集
- 客户生成
- 资源使用
- 报告生成

**用法：**
```python
from scripts.basic_simulation_template import SimulationConfig, run_simulation

config = SimulationConfig()
config.num_resources = 2
config.sim_time = 100
stats = run_simulation(config)
stats.report()
```

### resource_monitor.py

可重用监控工具：
- `ResourceMonitor` - 跟踪单个资源
- `MultiResourceMonitor` - 监控多个资源
- `ContainerMonitor` - 跟踪容器级别
- 自动统计计算
- CSV 导出功能

**用法：**
```python
from scripts.resource_monitor import ResourceMonitor

monitor = ResourceMonitor(env, resource, "My Resource")
# ... 运行模拟 ...
monitor.report()
monitor.export_csv('data.csv')
```

## 参考文档

特定主题的详细指南：

- **`references/resources.md`** - 所有资源类型及示例
- **`references/events.md`** - 事件系统和模式
- **`references/process-interaction.md`** - 过程同步
- **`references/monitoring.md`** - 数据收集技术
- **`references/real-time.md`** - 实时模拟设置

## 最佳实践

1. **生成器函数**：在过程函数中始终使用 `yield`
2. **资源上下文管理器**：使用 `with resource.request() as req:` 进行自动清理
3. **可重现性**：设置 `random.seed()` 以获得一致的结果
4. **监控**：在整个模拟过程中收集数据，而不仅仅是在结束时
5. **验证**：将简单案例与分析解决方案进行比较
6. **文档**：注释过程逻辑和参数选择
7. **模块化设计**：分离过程逻辑、统计和配置

## 常见陷阱

1. **忘记 yield**：过程必须产生事件以暂停
2. **事件重用**：事件只能触发一次
3. **资源泄漏**：使用上下文管理器或确保释放
4. **阻塞操作**：避免在过程中使用 Python 阻塞调用
5. **时间单位**：保持时间单位解释的一致性
6. **死锁**：确保至少一个过程可以取得进展

## 示例用例

- **制造业**：机器调度、生产线、库存管理
- **医疗保健**：急诊室模拟、患者流程、人员分配
- **电信**：网络流量、数据包路由、带宽分配
- **交通运输**：交通流、物流、车辆路由
- **服务运营**：呼叫中心、零售结账、预约调度
- **计算机系统**：CPU 调度、内存管理、I/O 操作