---
name: airflow-dag-patterns
description: "使用运算符、传感器、测试和部署的最佳实践构建生产 Apache Airflow DAG。在创建数据管道、编排工作流或调度批处理作业时使用。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Apache Airflow DAG 模式

Apache Airflow 的生产就绪模式，包括 DAG 设计、运算符、传感器、测试和部署策略。

## 何时使用此技能

- 使用 Airflow 创建数据管道编排
- 设计 DAG 结构和依赖项
- 实现自定义运算符和传感器
- 在本地测试 Airflow DAG
- 在生产中设置 Airflow
- 调试失败的 DAG 运行

## 何时不使用此技能

- 您只需要一个简单的 cron 作业或 shell 脚本
- Airflow 不是工具堆栈的一部分
- 任务与工作流编排无关

## 说明

1. 确定数据源、计划和依赖项。
2. 设计具有清晰所有权和重试的幂等任务。
3. 使用可观测性和警报钩子实现 DAG。
4. 在分段中验证并记录操作手册。

请参阅 `resources/implementation-playbook.md` 了解详细模式、检查清单和模板。

## 安全

- 避免在未经批准的情况下更改生产 DAG 计划。
- 仔细测试回填和重试以防止数据重复。

## 资源

- `resources/implementation-playbook.md` 用于详细的模式、检查清单和模板。

## 限制
- 仅在任务与上述描述范围明确匹配时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并寻求澄清。
