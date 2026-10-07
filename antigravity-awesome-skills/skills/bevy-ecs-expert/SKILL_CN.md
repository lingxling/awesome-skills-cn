---
name: bevy-ecs-expert
description: 掌握 Rust 中 Bevy 的实体组件系统 (ECS)，涵盖系统、查询、资源和并行调度。
risk: safe
source: community
date_added: "2026-02-27"
---

# Bevy ECS 专家

## 概述

使用 Bevy 的面向数据的 ECS 架构构建高性能游戏逻辑的指南。学习如何构建系统、优化查询、管理资源和利用并行执行。

## 何时使用此技能

- 在 Rust 中使用 Bevy 引擎开发游戏时使用。
- 当设计需要并行运行的游戏系统时使用。
- 当通过最小化缓存未命中来优化游戏性能时使用。
- 当将面向对象的逻辑重构为面向数据的 ECS 模式时使用。

## 分步指南

### 1. 定义组件

对数据使用简单的结构。派生 `Component` 和 `Reflect`。

```rust
#[derive(Component, Reflect, Default)]
#[reflect(Component)]
struct Velocity {
    x: f32,
    y: f32,
}

#[derive(Component)]
struct Player;
```

### 2. 编写系统

系统是查询组件的常规 Rust 函数。

```rust
fn movement_system(
    time: Res<Time>,
    mut query: Query<(&mut Transform, &Velocity), With<Player>>,
) {
    for (mut transform, velocity) in &mut query {
        transform.translation.x += velocity.x * time.delta_seconds();
        transform.translation.y += velocity.y * time.delta_seconds();
    }
}
```

### 3. 管理资源

使用 `Resource` 处理全局数据（分数、游戏状态）。

```rust
#[derive(Resource)]
struct GameState {
    score: u32,
}

fn score_system(mut game_state: ResMut<GameState>) {
    game_state.score += 10;
}
```

### 4. 调度系统

将系统添加到 `App` 构建器，如果需要定义执行顺序。

```rust
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .init_resource::<GameState>()
        .add_systems(Update, (movement_system, score_system).chain())
        .run();
}
```

## 示例

### 示例 1：使用需求组件生成实体

```rust
use bevy::prelude::*;

#[derive(Component, Reflect, Default)]
#[require(Velocity, Sprite)]
struct Player;

#[derive(Component, Default)]
struct Velocity {
    x: f32,
    y: f32,
}

fn setup(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn((
        Player,
        Velocity { x: 10.0, y: 0.0 },
        Sprite::from_image(asset_server.load("player.png")), 
    ));
}
```

### 示例 2：查询过滤器

使用 `With` 和 `Without` 高效地过滤实体。

```rust
fn enemy_behavior(
    query: Query<&Transform, (With<Enemy>, Without<Dead>)>,
) {
    for transform in &query {
        // 只有活跃的敌人在这里处理
    }
}
```

## 最佳实践

- ✅ **要做：** 使用 `Query` 过滤器（`With`、`Without`、`Changed`）来减少迭代计数。
- ✅ **要做：** 当只读访问足够时优先使用 `Res` 而不是 `ResMut`，允许并行执行。
- ✅ **要做：** 使用 `Bundle` 原子地生成复杂实体。
- ❌ **不要：** 在组件内存储重型逻辑；将其保持为纯数据。
- ❌ **不要：** 在组件内使用 `RefCell` 或内部可变性；让 ECS 处理借用。

## 故障排除

**问题：** 系统恐慌出现"冲突"错误。
**解决方案：** 您可能试图在两个并行运行的系统中可变地访问相同的组件。使用 `.chain()` 对其进行排序或分割逻辑。

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出作为特定于环境的验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
