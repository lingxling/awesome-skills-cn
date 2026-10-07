---
name: android-jetpack-compose-expert
description: "使用 Jetpack Compose 构建现代 Android UI 的专业指导，涵盖状态管理、导航、性能优化和 Material Design 3。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Android Jetpack Compose 专家指南

## 概述

使用 Jetpack Compose 构建生产级 Android 应用的完整指南。本技能涵盖架构模式、ViewModel 状态管理、类型安全导航和性能优化技术。

## 何时使用此技能

- 使用 Jetpack Compose 启动新的 Android 项目时。
- 将遗留 XML 布局迁移到 Compose 时。
- 实现复杂的 UI 状态管理和副作用时。
- 优化 Compose 性能（重新组合计数、稳定性）时。
- 设置类型安全导航时。

## 分步指南

### 1. 项目设置与依赖项

确保您的 `libs.versions.toml` 包含必要的 Compose BOM 和库。

```kotlin
[versions]
composeBom = "2024.02.01"
activityCompose = "1.8.2"

[libraries]
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
```

### 2. 状态管理模式（MVI/MVVM）

使用 `ViewModel` 和 `StateFlow` 来公开 UI 状态。避免暴露 `MutableStateFlow`。

```kotlin
// UI 状态定义
data class UserUiState(
    val isLoading: Boolean = false,
    val user: User? = null,
    val error: String? = null
)

// ViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(UserUiState())
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    fun loadUser() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val user = userRepository.getUser()
                _uiState.update { it.copy(user = user, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
}
```

### 3. 创建 Screen Composable

在"Screen"可组合函数中消费状态，并将数据向下传递到无状态组件。

```kotlin
@Composable
fun UserScreen(
    viewModel: UserViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    UserContent(
        uiState = uiState,
        onRetry = viewModel::loadUser
    )
}

@Composable
fun UserContent(
    uiState: UserUiState,
    onRetry: () -> Unit
) {
    Scaffold { padding ->
        Box(modifier = Modifier.padding(padding)) {
            when {
                uiState.isLoading -> CircularProgressIndicator()
                uiState.error != null -> ErrorView(uiState.error, onRetry)
                uiState.user != null -> UserProfile(uiState.user)
            }
        }
    }
}
```

## 示例

### 示例 1：类型安全导航

使用新的 Navigation Compose 类型安全功能（在最新版本中可用）。

```kotlin
// 定义目标
@Serializable
object Home

@Serializable
data class Profile(val userId: String)

// 设置 NavHost
@Composable
fun AppNavHost(navController: NavHostController) {
    NavHost(navController, startDestination = Home) {
        composable<Home> {
            HomeScreen(onNavigateToProfile = { id ->
                navController.navigate(Profile(userId = id))
            })
        }
        composable<Profile> { backStackEntry ->
            val profile: Profile = backStackEntry.toRoute()
            ProfileScreen(userId = profile.userId)
        }
    }
}
```

## 最佳实践

- ✅ **应该做：** 使用 `remember` 和 `derivedStateOf` 来最小化重新组合期间的不必要计算。
- ✅ **应该做：** 将 UI 状态中使用的数据类标记为 `@Immutable` 或 `@Stable`（如果它们包含 `List` 或其他不稳定类型），以启用聪明的重新组合跳过。
- ✅ **应该做：** 对由状态变化触发的一次性副作用（如显示 Snackbar）使用 `LaunchedEffect`。
- ❌ **不应该做：** 在可组合函数主体内直接执行昂贵的操作（如排序列表），而不使用 `remember`。
- ❌ **不应该做：** 将 `ViewModel` 实例传递给子组件。仅传递数据（状态）和 lambda 回调（事件）。

## 故障排除

**问题：** 无限重新组合循环。
**解决方案：** 检查您是否在组合中创建了新对象实例（如 `List` 或 `Modifier`）而没有 `remember`，或者您是否在组合阶段而不是副作用或回调中更新状态。使用 Layout Inspector 来调试重新组合计数。

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审核的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
