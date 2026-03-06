---
name: winui-app
description: 使用官方 Microsoft 指导、WinUI Gallery 模式、Windows App SDK 示例和 CommunityToolkit 组件，使用 C# 和 Windows App SDK 脚手架、开发和设计现代 WinUI 3 桌面应用程序。在创建全新应用程序、为 WinUI 准备机器、审查、重构、规划、故障排除、环境检查或设置 WinUI 3 XAML、控件、导航、窗口、主题、可访问性、响应性、性能、部署或相关 Windows 应用程序设计和开发工作时使用。
---

# WinUI App

使用此技能进行需要接地设置指导、应用程序脚手架、现代 Windows UX 决策或具体实现模式的 WinUI 3 和 Windows App SDK 工作。

## 必需流程

1. 将任务分类为环境/设置、新应用程序脚手架、设计、实现、审查或故障排除。
2. 如果任务是关于为 WinUI 准备机器、审计就绪性或创建全新应用程序，请在此技能中的捆绑设置和脚手架流程之前开始更广泛的设计、实现或故障排除工作：
   - 当请求是新应用程序时选择应用程序名称。
   - 当用户已经给出安全文件夹名称时，请使用他们给出的确切名称。
   - 如果用户没有给出名称，请从请求派生一个简短的 PascalCase 名称并说明您选择了什么。
   - 在用户当前工作区中创建项目，除非他们要求另一个位置。
   - 除非用户明确要求覆盖现有文件，否则不要使用 `--force`。
   - 从技能目录运行捆绑的 WinGet 配置，以便相对路径保持精确为 `config.yaml`：

```powershell
winget configure -f config.yaml --accept-configuration-agreements --disable-interactivity
```

   - 将配置视为旨在启用开发者模式、安装或更新 Visual Studio Community 2026，以及安装 WinUI 开发所需的 Managed Desktop、Universal 和 Windows App SDK C# 组件。
   - 在继续之前评估配置结果。成功时继续。如果失败，请检查输出而不是猜测。如果 `winui` 模板已可用且工具链可用，请记录部分失败并继续。如果仍然缺少先决条件，请停止并清楚地报告阻止程序。
   - 在脚手架之前验证模板可用：

```powershell
dotnet new list winui
```

   - 对于仅诊断的环境请求，请说明捆绑的脚手架可能会更改机器并在运行它之前获取确认。如果用户拒绝更改，请使用 `references/foundation-environment-audit-and-remediation.md` 中的手动验证指导，并在 `present`、`missing`、`uncertain` 和 `recommended optional tools` 下总结就绪性。
   - 对于全新应用程序，使用 `dotnet new winui -o <name>` 进行脚手架。仅当用户要求时才添加模板选项。支持的选项：`-f|--framework net10.0|net9.0|net8.0`、`-slnx|--use-slnx`、`-cpm|--central-pkg-mgmt`、`-mvvm|--use-mvvm`、`-imt|--include-mvvm-toolkit`、`-un|--unpackaged`、`-nsf|--no-solution-file`、`--force`。不要发明不支持的标志。如果用户要求打包行为，请传递 `--unpackaged false`。否则保持模板默认。
   - 通过确认预期的项目文件存在并对生成的 `.csproj` 运行 `dotnet build` 来验证新脚手架。
   - 通过其实际打包模型的正确路径启动新脚手架的应用程序，并确认有真实的顶级窗口而不是仅依赖启动器进程退出代码。
3. 阅读 `references/_sections.md`，然后仅加载与任务匹配的引用文件。
4. 在创建或重构应用程序之前使打包模型显式。默认对 Store 类产品工作流程和 Visual Studio 部署/F5 流程使用打包。当用户期望可重复的 CLI 构建和运行循环或每次更改后直接 `.exe` 启动时，默认为未打包。
5. 当任务是不透明的 XAML 编译器失败（如 `MSB3073` 或 `XamlCompiler.exe`）时，请阅读 `references/foundation-template-first-recovery.md` 并为所选打包模型简化回向当前 `dotnet new winui` 脚手架，而不是发明自定义恢复结构。
6. 对于创建或更改 WinUI 应用程序的任何工作，制作一个完整但最小的编辑集，然后构建应用程序并在响应用户之前运行它。即使用户没有明确要求验证，也默认这样做。如果运行的应用程序实例在仍有更多工作时锁定输出，请停止它，重新构建，重新启动并继续验证。当工作完成且启动验证成功时，请为用户保留最终验证的应用程序实例运行，除非他们明确要求您不要。
7. 将启动验证视为不完整，直到应用程序显示客观成功信号，如响应的顶级窗口、预期的窗口标题或其他清晰的启动行为。仅生成的进程本身是不够的。
8. 优先考虑 Microsoft Learn 以获取要求、API 期望和平台指导。
9. 优先考虑 WinUI Gallery 以获取具体控件使用、外壳组合和设计细节。
10. 优先考虑 WindowsAppSDK-Samples 以获取场景级别 API，如窗口、生命周期、通知、部署和自定义控件。
11. 首先构建向 WinUI 和 Fluent 指导。将原生 WinUI 外壳、控件、交互和控件 chrome 视为默认实现路径。
12. 对于分组的命令表面（如文档操作、编辑器格式化、视图切换或页面级工具栏），优先考虑原生 `CommandBar` 或其他标准 WinUI 命令表面，而不是使用 `Grid`、`StackPanel`、`Border` 或临时按钮分组构建自定义行。
13. 不要发明应用程序特定的控件、定制组件库或自定义 chrome 来替换标准 WinUI 行为，除非用户明确要求该定制、现有产品设计系统已需要它，或验证的平台差距没有干净的原生选项。
14. 需要定制时，首先组合、模板或重新设置内置 WinUI 控件和系统资源，然后再添加 CommunityToolkit 依赖项或创作新自定义控件。
15. 仅当内置 WinUI 控件或助手不能干净地覆盖需求时才使用 CommunityToolkit。
16. 默认支持浅色和深色模式。将单主题输出视为需要显式用户请求或现有产品约束的例外。
17. 构建或修订 UI 时，使用主题感知资源、系统画笔和 WinUI 样式挂钩，而不是硬编码仅浅色或仅深色的颜色。
18. 使滚动所有权显式用于集合布局。当页面已经垂直滚动时，不要假设嵌套的 `GridView` 或其他滚动拥有集合仍然可以正确渲染水平海报栏。
19. 不要在部分、列表或卡片周围添加额外的 `Border` 包装器，除非边框在做不同的工作，包含的控件或父表面尚未提供。避免"双卡片"组合，其中部分 `Border` 包装已经渲染为卡片的子项。
20. 将响应性视为外壳加页面问题，而不仅仅是控件调整大小问题。为导航、填充、内容密度和页脚/工具区域规划明确的宽、中和电话宽度行为，并在宽度缩小时简化或隐藏非必要 UI。

## 常见路由

| 请求 | 首先阅读 |
| --- | --- |
| 检查此 PC 是否可以构建 WinUI 应用程序 | `references/foundation-environment-audit-and-remediation.md` |
| 安装缺少的 WinUI 先决条件 | `references/foundation-environment-audit-and-remediation.md` |
| 启动新的打包或未打包应用程序 | `references/foundation-setup-and-project-selection.md` |
| 在保持锚定到模板脚手架的同时从不透明的 XAML 编译器或启动失败中恢复 | `references/foundation-template-first-recovery.md` |
| 构建、运行或验证 WinUI 应用程序实际启动 | `references/build-run-and-launch-verification.md` |
| 审查应用程序结构、页面、资源和绑定 | `references/foundation-winui-app-structure.md` |
| 选择外壳、导航、标题栏或多窗口模式 | `references/shell-navigation-and-windowing.md` |
| 选择控件或响应布局模式 | `references/controls-layout-and-adaptive-ui.md` |
| 应用 Mica、主题、字体排印、图标或 Fluent 样式 | `references/styling-theming-materials-and-icons.md` |
| 改善可访问性、键盘化或本地化 | `references/accessibility-input-and-localization.md` |
| 诊断响应性或 UI 线程性能 | `references/performance-diagnostics-and-responsiveness.md` |
| 决定是否使用 CommunityToolkit | `references/community-toolkit-controls-and-helpers.md` |
| 处理生命周期、通知或部署 | `references/windows-app-sdk-lifecycle-notifications-and-deployment.md` |
| 运行审查清单 | `references/testing-debugging-and-review-checklists.md` |

## 环境规则

- 不要猜测机器是否准备好进行 WinUI 开发。验证它。
- 对全新设置、补救和首次项目脚手架使用此技能中的捆绑设置和脚手架流程，而不是委托给另一个技能。
- 将此技能目录中的 `config.yaml` 视为捆绑的引导真实来源。
- 将不确定的环境信号视为不确定，而不是成功。
- 如果任务仅是审计且用户拒绝机器更改，请使用 `references/foundation-environment-audit-and-remediation.md` 中的手动验证指导，并使不确定信号显式，而不是暗示成功。
- 如果缺少 `config.yaml`，请清楚地说明并回退到官方 Microsoft 工作流程，而不是假装捆绑路径存在。
- 保持环境就绪性、打包选择和应用程序启动验证为单独的检查。通过一个并不能证明其他。
- 对模棱两可的启动结果失败关闭。如果应用程序没有清楚打开，请继续调试。
- 在创建或编辑 WinUI 应用程序后，不要在成功构建时停止。启动应用程序，确认客观启动行为，并在将控制权返回给用户之前留下最终验证的应用程序实例运行，除非他们明确说不要运行它。

## 引用规则

- 将 C# 视为主要路径。仅在差异实质性时才提及 C++ 或 C++/WinRT。
- 保留现有代码库的约定，而不是将通用示例结构强加于它。
- 将 WinUI 设计指导和原生控件视为准线。不要漂移到定制组件系统或标准控件的应用程序特定替换，除非用户明确要求它们或现有代码库已依赖它们。
- 除非用户明确要求单主题结果或产品已强制一个，否则对应用程序 UI 工作默认支持浅色和深色模式。
- 在添加 CommunityToolkit 依赖项、自定义控件或应用程序特定表面系统之前，优先考虑内置 WinUI 控件和系统样式挂钩。
- 将详细的控件、主题、外壳、滚动、响应性、打包和恢复指导放在匹配的引用文件中，而不是在此重复这些规则。
