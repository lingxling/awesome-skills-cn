---
name: aspnet-core
description: 使用 .NET Web 开发的当前官方指导构建、审查、重构或架构 ASP.NET Core Web 应用程序。在处理 Blazor Web Apps、Razor Pages、MVC、Minimal APIs、基于控制器的 Web API、SignalR、gRPC、中间件、依赖注入、配置、身份验证、授权、测试、性能、部署或 ASP.NET Core 升级时使用。
---

# ASP.NET Core

## 概述

选择正确的 ASP.NET Core 应用程序模型，正确组合主机和请求管道，并以 Microsoft 今天记录的框架风格实现功能。

加载适合任务的最小引用集。不要默认加载每个引用。

## 工作流程

1. 确认目标框架、SDK 和当前应用程序模型。
2. 首先打开 [references/stack-selection.md](references/stack-selection.md) 用于新应用程序或主要重构。
3. 接下来打开 [references/program-and-pipeline.md](references/program-and-pipeline.md) 用于 `Program.cs`、DI、配置、中间件、路由、日志和静态资产。
4. 只打开一个主要应用程序模型引用：
   - [references/ui-blazor.md](references/ui-blazor.md)
   - [references/ui-razor-pages.md](references/ui-razor-pages.md)
   - [references/ui-mvc.md](references/ui-mvc.md)
   - [references/apis-minimal-and-controllers.md](references/apis-minimal-and-controllers.md)
5. 仅在需要时添加跨领域引用：
   - [references/data-state-and-services.md](references/data-state-and-services.md)
   - [references/security-and-identity.md](references/security-and-identity.md)
   - [references/realtime-grpc-and-background-work.md](references/realtime-grpc-and-background-work.md)
   - [references/testing-performance-and-operations.md](references/testing-performance-and-operations.md)
6. 在将新平台 API 引入旧解决方案或在主要版本之间迁移之前，打开 [references/versioning-and-upgrades.md](references/versioning-and-upgrades.md)。
7. 当您需要与尚未被专注引用涵盖的任务对应的 Microsoft Learn 部分时，使用 [references/source-map.md](references/source-map.md)。

## 默认操作假设

- 优先使用最新的稳定 ASP.NET Core 和 .NET，除非仓库或用户请求固定了较旧的目标。
- 截至 2026 年 3 月，对于新的生产工作，优先使用 .NET 10 / ASP.NET Core 10。除非用户明确要求预览功能，否则将 ASP.NET Core 11 视为预览。
- 优先使用 `WebApplicationBuilder` 和 `WebApplication`。避免较旧的 `Startup` 和 `WebHost` 模式，除非代码库已使用它们或任务是迁移。
- 在添加第三方基础架构之前，优先使用内置 DI、选项/配置、日志、ProblemDetails、OpenAPI、健康检查、速率限制、输出缓存和 Identity。
- 保持功能切片内聚，以便页面、组件、端点、控制器、验证、服务、数据访问和测试易于跟踪。
- 尊重现有的应用程序模型。如果没有明确原因，不要将 Razor Pages 重写为 MVC 或将控制器重写为 Minimal APIs。

## 引用指南

- [references/_sections.md](references/_sections.md)：快速索引和阅读顺序。
- [references/stack-selection.md](references/stack-selection.md)：选择正确的 ASP.NET Core 应用程序模型和模板。
- [references/program-and-pipeline.md](references/program-and-pipeline.md)：构建 `Program.cs`、服务、中间件、路由、配置、日志和静态资产。
- [references/ui-blazor.md](references/ui-blazor.md)：构建 Blazor Web Apps，选择渲染模式，并正确使用组件、表单和 JS 互操作。
- [references/ui-razor-pages.md](references/ui-razor-pages.md)：使用处理程序、模型绑定和约定构建以页面为中心的服务器渲染应用程序。
- [references/ui-mvc.md](references/ui-mvc.md)：构建具有清晰关注点分离的控制器/视图应用程序。
- [references/apis-minimal-and-controllers.md](references/apis-minimal-and-controllers.md)：使用 Minimal APIs 或控制器构建 HTTP API，包括验证和响应模式。
- [references/data-state-and-services.md](references/data-state-and-services.md)：负责任地使用 EF Core、`DbContext`、选项、`IHttpClientFactory`、会话、临时数据和应用程序状态。
- [references/security-and-identity.md](references/security-and-identity.md)：应用身份验证、授权、Identity、机密、数据保护、CORS、CSRF 和 HTTPS 指导。
- [references/realtime-grpc-and-background-work.md](references/realtime-grpc-and-background-work.md)：使用 SignalR、gRPC 和托管服务。
- [references/testing-performance-and-operations.md](references/testing-performance-and-operations.md)：添加集成测试、浏览器测试、缓存、压缩、健康检查、速率限制和部署关注点。
- [references/versioning-and-upgrades.md](references/versioning-and-upgrades.md)：处理目标框架、重大更改、过时的 API 和迁移。
- [references/source-map.md](references/source-map.md)：将官方 ASP.NET Core 文档树映射到此技能中的引用。

## 执行说明

- 生成新代码时，从正确的 `dotnet new` 模板开始，并保持生成的结构可识别。
- 编辑现有解决方案时，首先遵循解决方案的约定，并使用这些引用以避免框架误用或过时的模式。
- 当任务提及"最新"时，在依赖内存之前在 Microsoft Learn 或 ASP.NET Core 文档仓库上验证功能。
