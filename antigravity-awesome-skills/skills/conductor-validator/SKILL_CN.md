---
name: conductor-validator
description: '验证 Conductor 项目工件的完整性、一致性和正确性。在设置后、诊断问题时或在实现前使用以验证项目上下文。'
risk: safe
source: community
date_added: '2026-02-27'
---

# 检查 conductor 目录是否存在
ls -la conductor/

# 查找所有轨道目录
ls -la conductor/tracks/

# 检查必需的文件
ls conductor/index.md conductor/product.md conductor/tech-stack.md conductor/workflow.md conductor/tracks.md
```

## 使用此技能的场景

- 处理检查 conductor 目录是否存在的任务或工作流程
- 需要关于检查 conductor 目录是否存在的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与检查 conductor 目录是否存在无关
- 您需要超出此范围的不同域或工具

## 说明

- 澄清目标、约束和必需的输入。
- 应用相关的最佳实践并验证结果。
- 提供可执行的步骤和验证。
- 如果需要详细示例，打开 `resources/implementation-playbook.md`。

## 模式匹配

**tracks.md 中的状态标记：**

```
- [ ] 轨道名称  # 未开始
- [~] 轨道名称  # 进行中
- [x] 轨道名称  # 完成
```

**plan.md 中的任务标记：**

```
- [ ] 任务描述  # 待定
- [~] 任务描述  # 进行中
- [x] 任务描述  # 完成
```

**轨道 ID 模式：**

```
<type>_<name>_<YYYYMMDD>
示例：feature_user_auth_20250115
```

## 限制
- 仅在任务清楚地符合上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
