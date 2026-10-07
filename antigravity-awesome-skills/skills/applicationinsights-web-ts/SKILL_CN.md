---
name: applicationinsights-web-ts
description: "使用 Application Insights JavaScript SDK (@microsoft/applicationinsights-web) 为浏览器/网页应用添加监测。"
risk: critical
source: https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts
source_repo: microsoft/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/microsoft/skills/blob/main/LICENSE
---

# TypeScript 版 Application Insights JavaScript SDK（Web 端）
## 何时使用

当你需要使用 Application Insights JavaScript SDK (@microsoft/applicationinsights-web) 为浏览器/网页应用添加监测时使用此技能。适用于真实用户监测（RUM）——页面浏览、点击、AJAX/fetch 依赖、异常、自定义事件，以及与后端关联的浏览器端 GenAI agent 追踪……


面向浏览器应用的真实用户监测（RUM），使用 `@microsoft/applicationinsights-web`。自动收集页面浏览、AJAX/fetch 依赖、未处理异常，以及(配合 Click Analytics 插件)点击行为。支持自定义事件、指标,以及遵循 OpenTelemetry GenAI 语义约定并通过 W3C Trace Context 与后端 span 关联的 **GenAI agent 追踪**。

> **与 `azure-monitor-opentelemetry-ts` 不同**，后者面向 Node.js 服务端应用。本技能面向**浏览器/网页**代码(以及 React Native)。

## 实施前

在 `microsoft-docs` MCP 中搜索当前的 API 模式:

- 查询: "Application Insights JavaScript SDK setup"
- 查询: "Application Insights JavaScript SDK configuration"
- 查询: "Application Insights JavaScript framework extensions React Angular"
- 验证包版本: `npm view @microsoft/applicationinsights-web version`

## 软件包

| 软件包 | 用途 |
| --- | --- |
| `@microsoft/applicationinsights-web` | 核心 RUM SDK(页面浏览、AJAX、异常)。 |
| `@microsoft/applicationinsights-clickanalytics-js` | 自动收集点击遥测数据。 |
| `@microsoft/applicationinsights-react-js` | React 插件(路由监测、hooks、HOC、ErrorBoundary)。 |
| `@microsoft/applicationinsights-react-native` | React Native 插件(原生崩溃、会话)。 |
| `@microsoft/applicationinsights-angularplugin-js` | Angular 插件(路由事件、ErrorHandler)。 |
| `@microsoft/applicationinsights-debugplugin-js` | 仅用于开发的遥测检查器。 |
| `@microsoft/applicationinsights-perfmarkmeasure-js` | User Timing (`performance.mark/measure`) 集成。 |

## 安装

```bash
npm i --save @microsoft/applicationinsights-web
# 可选插件(只安装你会用到的):
npm i --save @microsoft/applicationinsights-clickanalytics-js
npm i --save @microsoft/applicationinsights-react-js @microsoft/applicationinsights-react-native @microsoft/applicationinsights-angularplugin-js
```

类型定义随软件包一起提供——无需单独安装 `@types/...`。

## 连接字符串

浏览器端 SDK 在初始化时需要连接字符串。**该字符串以明文形式发送给客户端**——浏览器端遥测不支持 Microsoft Entra ID 认证。如果你需要将其与后端遥测隔离，请为浏览器端 RUM 使用启用本地认证的独立 App Insights 资源。

```bash
# Vite / CRA / Next.js —— 通过公共环境变量前缀暴露给客户端
VITE_APPINSIGHTS_CONNECTION_STRING="InstrumentationKey=...;IngestionEndpoint=https://...;LiveEndpoint=https://..."
NEXT_PUBLIC_APPINSIGHTS_CONNECTION_STRING="InstrumentationKey=..."
```

## 快速开始(npm)

```typescript
import { ApplicationInsights } from "@microsoft/applicationinsights-web";

export const appInsights = new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,
    enableAutoRouteTracking: true,        // SPA 路由变化 -> 页面浏览
    enableCorsCorrelation: true,          // 将 Request-Id / traceparent 传播到跨源 AJAX
    enableRequestHeaderTracking: true,
    enableResponseHeaderTracking: true,
    distributedTracingMode: 2,            // DistributedTracingModes.AI_AND_W3C —— 发出 traceparent 以供后端关联
    autoTrackPageVisitTime: true,
    disableFetchTracking: false,          // fetch() 默认会被自动监测
    excludeRequestFromAutoTrackingPatterns: [/livemetrics\.azure\.com/i]
  }
});

appInsights.loadAppInsights();
appInsights.trackPageView();
```

调用 `loadAppInsights()` 一次且尽早调用(在你想要追踪的用户交互发生之前)。然后在初次加载时调用 `trackPageView()`——当 `enableAutoRouteTracking` 开启时,后续路由变化会自动追踪。

## 快速开始(SDK Loader 脚本)

当你希望 SDK 自动更新且无需构建流程时推荐使用。将其作为 `<head>` 中的**第一个** `<script>` 粘贴:

```html
<script type="text/javascript" src="https://js.monitor.azure.com/scripts/b/ai.3.gbl.min.js" crossorigin="anonymous"></script>
<script type="text/javascript">
  var appInsights = window.appInsights || function (cfg) {
    /* 参见: https://learn.microsoft.com/azure/azure-monitor/app/javascript-sdk
       使用上面 Microsoft Learn 页面中的最新代码片段——它包含
       备用 CDN 故障转移(cr)、SDK 加载失败报告,以及
       队列垫片,确保 SDK 就绪前的调用不会丢失。*/
  }({ src: "https://js.monitor.azure.com/scripts/b/ai.3.gbl.min.js",
      crossOrigin: "anonymous",
      cfg: { connectionString: "YOUR_CONNECTION_STRING" } });
</script>
```

Loader-only API(在 SDK 加载前会被排队): `trackEvent`、`trackPageView`、`trackException`、`trackTrace`、`trackDependencyData`、`trackMetric`、`trackPageViewPerformance`、`startTrackPage`、`stopTrackPage`、`startTrackEvent`、`stopTrackEvent`、`addTelemetryInitializer`、`setAuthenticatedUserContext`、`clearAuthenticatedUserContext`、`flush`。

## 核心追踪 API

```typescript
// 页面浏览(禁用了 enableAutoRouteTracking 的 SPA)
appInsights.trackPageView({ name: "Checkout", uri: "/checkout", properties: { cartSize: 3 } });

// 自定义事件(用户操作、业务事件)
appInsights.trackEvent({ name: "PurchaseCompleted" }, { orderId: "ord_123", amountUsd: 49.95 });

// 异常(已捕获的错误)
try {
  await pay(order);
} catch (err) {
  appInsights.trackException({ exception: err as Error, severityLevel: 3, properties: { orderId: order.id } });
}

// 追踪(日志,严重性 0=Verbose, 1=Info, 2=Warning, 3=Error, 4=Critical)
appInsights.trackTrace({ message: "Cart hydrated from local storage", severityLevel: 1 });

// 自定义指标(数值)
appInsights.trackMetric({ name: "checkout.duration_ms", average: 1234 });

// 依赖(手动追踪的出站调用——fetch/XHR 会被自动追踪)
appInsights.trackDependencyData({
  id: crypto.randomUUID(),
  name: "GET /api/orders",
  duration: 87, success: true, responseCode: 200,
  data: "https://api.example.com/api/orders", target: "api.example.com", type: "Fetch"
});

// 用户身份(每个已认证会话仅设置一次——这些值属于 PII;不要传递邮箱)
appInsights.setAuthenticatedUserContext("user-id-123", "tenant-456", /*storeInCookie*/ true);
appInsights.clearAuthenticatedUserContext(); // 退出登录时

// 卸载前强制发送
appInsights.flush();
```

## 遥测初始化器(富化与过滤)

在每个数据包发送前运行。返回 `false` 以丢弃。

```typescript
import type { ITelemetryItem } from "@microsoft/applicationinsights-web";

appInsights.addTelemetryInitializer((item: ITelemetryItem) => {
  item.tags ??= {};
  item.tags["ai.cloud.role"] = "web-shop";
  item.tags["ai.cloud.roleInstance"] = window.location.hostname;
  item.data ??= {};
  item.data["app.version"] = import.meta.env.VITE_APP_VERSION;
  item.data["app.build"] = import.meta.env.VITE_BUILD_SHA;

  // 丢弃嘈杂的健康检查页面浏览
  if (item.baseType === "PageviewData" && item.baseData?.uri?.endsWith("/healthz")) return false;

  // 清理查询字符串中的密钥
  if (item.baseData?.uri) {
    item.baseData.uri = item.baseData.uri.replace(/([?&](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/token|sig|key)=)[^&]+/gi, "$1REDACTED");
  }
});
```

## Click Analytics

```typescript
import { ClickAnalyticsPlugin } from "@microsoft/applicationinsights-clickanalytics-js";

const clickPlugin = new ClickAnalyticsPlugin();
const appInsights = new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,
    extensions: [clickPlugin],
    extensionConfig: {
      [clickPlugin.identifier]: {
        autoCapture: true,
        dataTags: { useDefaultContentNameOrId: true, customDataPrefix: "data-ai-" },
        urlCollectHash: false,
        behaviorValidator: (b: string) => /^[a-z0-9_]+$/.test(b) ? b : ""
      }
    }
  }
});
appInsights.loadAppInsights();
```

使用 `data-ai-*` 属性标记元素;点击会被作为带父级内容元数据的自定义事件发出。

## SPA 路由追踪

- **内置方式:** 设置 `enableAutoRouteTracking: true`。会挂钩 `history.pushState/replaceState` 和 `popstate`。
- **React Router:** 使用 `@microsoft/applicationinsights-react-js` 的 `withAITracking` HOC(参见 [references/framework-extensions.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/framework-extensions.md))。
- **手动方式:** 在路由组件的 `useEffect` 中,当路由变化时调用 `appInsights.trackPageView({ name, uri })`。禁用 `enableAutoRouteTracking` 以避免重复计数。

## 分布式追踪(关联后端)

设置 `distributedTracingMode: 2`(`DistributedTracingModes.AI_AND_W3C`)。SDK 会在出站的 `fetch`/`XHR` 请求中添加 `traceparent`(以及旧版 `Request-Id`)。使用 **OpenTelemetry** 监测的后端(例如 `@azure/monitor-opentelemetry`)会自动链接到浏览器的 operation_Id。

对于跨源调用,还需设置 `enableCorsCorrelation: true`,并在 API 上的**CORS 暴露头**中添加调用方的来源。

## GenAI Agent 追踪(OTel 语义约定)

当浏览器调用 AI agent(函数调用、工具使用、从客户端直接调用模型)时,发出 App Insights 的**依赖(Dependency)**遥测数据,其属性遵循 OpenTelemetry 的 **GenAI 语义约定**,以便在 App Insights / Log Analytics 中与后端 agent span 一起查询。

**先设置选用环境变量**,以便后端监测使用相同的 schema 版本:

```bash
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
```

### 必需的属性键(直接使用 OTel 名称)

| Span / 操作 | 必需的属性 |
| --- | --- |
| `invoke_agent {agent.name}` | `gen_ai.operation.name=invoke_agent`、`gen_ai.provider.name`、`gen_ai.agent.name`、`gen_ai.agent.id`(已知时) |
| `create_agent {agent.name}` | `gen_ai.operation.name=create_agent`、`gen_ai.provider.name`、`gen_ai.agent.name`、`gen_ai.request.model` |
| `chat {model}` | `gen_ai.operation.name=chat`、`gen_ai.provider.name`、`gen_ai.request.model`、`gen_ai.response.model`、`gen_ai.usage.input_tokens`、`gen_ai.usage.output_tokens` |
| `execute_tool {tool.name}` | `gen_ai.operation.name=execute_tool`、`gen_ai.tool.name`、`gen_ai.tool.type`(`function` \| `extension` \| `datastore`)、`gen_ai.tool.call.id` |

`gen_ai.provider.name` 常见值: `openai`、`azure.ai.openai`、`azure.ai.inference`、`anthropic`、`aws.bedrock`、`gcp.gemini`、`gcp.vertex_ai`、`cohere`、`mistral_ai`、`groq`、`deepseek`、`perplexity`、`x_ai`、`ibm.watsonx.ai`。

> **敏感内容需显式启用。** `gen_ai.system_instructions`、`gen_ai.input.messages`、`gen_ai.output.messages`、`gen_ai.tool.call.arguments`、`gen_ai.tool.call.result` 默认属于**需显式启用(Opt-In)**。请用运行时开关对其进行门控,未经批准的数据处理流程不要在生产环境中使用它们。

### 模式: invoke_agent + 嵌套的工具/模型 span

```typescript
import { ApplicationInsights, SeverityLevel } from "@microsoft/applicationinsights-web";

type GenAiAttrs = Record<string, string | number | boolean | undefined>;

function startGenAiSpan(name: string, attrs: GenAiAttrs) {
  const id = crypto.randomUUID();
  const start = performance.now();
  const baseProps: GenAiAttrs = { "gen_ai.span.id": id, ...attrs };
  return {
    end(success: boolean, extra: GenAiAttrs = {}, error?: Error) {
      const duration = Math.round(performance.now() - start);
      const properties = { ...baseProps, ...extra };
      appInsights.trackDependencyData({
        id, name, duration, success,
        responseCode: error ? 500 : 200,
        type: "GenAI",
        target: String(attrs["gen_ai.provider.name"] ?? "genai"),
        properties: properties as Record<string, string>
      });
      if (error) {
        appInsights.trackException({
          exception: error,
          severityLevel: SeverityLevel.Error,
          properties: { ...properties, "error.type": error.name } as Record<string, string>
        });
      }
    }
  };
}

// Agent 调用
const agentSpan = startGenAiSpan("invoke_agent ResearchAssistant", {
  "gen_ai.operation.name": "invoke_agent",
  "gen_ai.provider.name": "azure.ai.openai",
  "gen_ai.agent.name": "ResearchAssistant",
  "gen_ai.agent.id": "asst_5j66UpCpwteGg4YSxUnt7lPY",
  "gen_ai.request.model": "gpt-4o-mini",
  "server.address": "myresource.openai.azure.com"
});

try {
  // 嵌套的 chat completion span
  const chat = startGenAiSpan("chat gpt-4o-mini", {
    "gen_ai.operation.name": "chat",
    "gen_ai.provider.name": "azure.ai.openai",
    "gen_ai.request.model": "gpt-4o-mini"
  });
  const res = await callAzureOpenAi(/* ... */);
  chat.end(true, {
    "gen_ai.response.model": res.model,
    "gen_ai.response.id": res.id,
    "gen_ai.response.finish_reasons": JSON.stringify(res.choices.map(c => c.finish_reason)),
    "gen_ai.usage.input_tokens": res.usage.prompt_tokens,
    "gen_ai.usage.output_tokens": res.usage.completion_tokens,
    "gen_ai.output.type": "text"
  });

  // 嵌套的工具执行 span
  const tool = startGenAiSpan("execute_tool getWeather", {
    "gen_ai.operation.name": "execute_tool",
    "gen_ai.tool.name": "getWeather",
    "gen_ai.tool.type": "function",
    "gen_ai.tool.call.id": "call_abc123"
  });
  const toolResult = await runGetWeather({ location: "SF" });
  tool.end(true);

  agentSpan.end(true, {
    "gen_ai.usage.input_tokens": res.usage.prompt_tokens,
    "gen_ai.usage.output_tokens": res.usage.completion_tokens
  });
} catch (err) {
  agentSpan.end(false, { "error.type": (err as Error).name }, err as Error);
}
```

浏览器的 `traceparent` 会自动附加到出站的 `fetch`(当 `distributedTracingMode: 2` 时),因此下游的 Azure OpenAI / agent 后端 span 会挂在 App Insights 中同一个 operation_Id 之下。

完整的属性参考、常见值和内容捕获指南,请参见 [references/agent-traces.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/agent-traces.md)。

### KQL: 在 App Insights 中查询 GenAI 追踪

```kusto
dependencies
| where type == "GenAI"
| extend op   = tostring(customDimensions["gen_ai.operation.name"]),
         agent = tostring(customDimensions["gen_ai.agent.name"]),
         model = tostring(customDimensions["gen_ai.request.model"]),
         tin   = toint(customDimensions["gen_ai.usage.input_tokens"]),
         tout  = toint(customDimensions["gen_ai.usage.output_tokens"])
| summarize calls=count(), p95_ms=percentile(duration, 95),
            avg_in=avg(tin), avg_out=avg(tout) by op, agent, model, bin(timestamp, 5m)
```

## React (TypeScript)

完整的 React、React Native、Angular、Next.js 和 Vite 配方请参见 [references/framework-extensions.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/framework-extensions.md)。

```typescript
import { ApplicationInsights } from "@microsoft/applicationinsights-web";
import { ReactPlugin, withAITracking } from "@microsoft/applicationinsights-react-js";
import { createBrowserHistory } from "history";

const reactPlugin = new ReactPlugin();
const browserHistory = createBrowserHistory();

export const appInsights = new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,
    extensions: [reactPlugin],
    extensionConfig: { [reactPlugin.identifier]: { history: browserHistory } }
  }
});
appInsights.loadAppInsights();

export const TrackedCheckout = withAITracking(reactPlugin, Checkout, "Checkout");
```

## React Native

```typescript
import { ApplicationInsights } from "@microsoft/applicationinsights-web";
import { ReactNativePlugin } from "@microsoft/applicationinsights-react-native";

const rnPlugin = new ReactNativePlugin();
const appInsights = new ApplicationInsights({
  config: {
    connectionString: process.env.EXPO_PUBLIC_APPINSIGHTS_CONNECTION_STRING,
    extensions: [rnPlugin],
    disableFetchTracking: false
  }
});
appInsights.loadAppInsights();
```

## 性能 —— Web Vitals

自动收集: 通过 `PerformanceTiming` / `PerformanceNavigationTiming` 获取页面加载耗时。要添加 Core Web Vitals:

```typescript
import { onCLS, onLCP, onINP, type Metric } from "web-vitals";

function send(m: Metric) {
  appInsights.trackMetric(
    { name: `web_vitals.${m.name.toLowerCase()}`, average: m.value },
    { rating: m.rating, navigationType: m.navigationType, id: m.id }
  );
}
onCLS(send); onLCP(send); onINP(send);
```

## Cookie 与隐私

```typescript
new ApplicationInsights({ config: {
  connectionString,
  isCookieUseDisabled: true,         // 强制禁用所有 cookie
  cookieCfg: { enabled: true, domain: ".example.com", path: "/", expiry: 365 }
}});
```

要动态遵循用户同意:

```typescript
appInsights.getCookieMgr().setEnabled(userGaveConsent);
appInsights.config.disableTelemetry = !userGaveConsent;
```

## 采样

服务端采集采样(推荐)在 App Insights 资源上配置。SDK 端采样可减少网络使用:

```typescript
new ApplicationInsights({ config: { connectionString, samplingPercentage: 50 } });
```

通过遥测初始化器实现按类型采样: 根据 `item.baseType` 用 `return false` 丢弃。

## 离线 / 卸载时发送

SDK 使用 `sendBeacon`(默认 `onunloadDisableBeacon: false`)在 `pagehide` / `unload` 时进行刷送。对于 SPA,在有破坏性的跳转(登出、硬刷新)之前也应调用 `appInsights.flush()`。

## 常见陷阱

1. **不要初始化两次。** 在不同的打包中重复导入该模块会产生重复的页面浏览数据。使用单一的共享模块导出。
2. **在第一次用户输入前初始化**,以避免丢失早期的点击/异常。
3. **连接字符串是公开的** —— 切勿将同一个 App Insights 资源复用于后端密钥。
4. **`enableAutoRouteTracking` + 手动 `trackPageView`** = 重复记录。只能选其一。
5. **CORS 分布式追踪**要求 API 允许 `Request-Id`、`Request-Context`、`traceparent`、`tracestate` 请求头,并暴露 `Request-Context` 响应头。
6. **GenAI 敏感内容**(`gen_ai.input.messages` 等)需显式启用 —— 在没有明确的运行时开关和经批准的数据处理流程前切勿记录。
7. **Agent 的 token 用量在 `chat` span 上,而不是 `invoke_agent`** —— 只有在已知的情况下才将聚合用量复制到父级 agent span。
8. **React StrictMode** 在开发环境下会对 effect 双重调用 —— 用模块级单例保护 `loadAppInsights()`。

## 打包体积

完整的 web SDK 压缩后约 110 KB(gzip 后约 36 KB)。对于严格的体积预算,使用 **Loader 脚本**方式,使 SDK 异步加载、不占用关键路径,或对未使用的插件进行 tree-shake。

## 关键类型

```typescript
import {
  ApplicationInsights,
  SeverityLevel,
  DistributedTracingModes,
  type IConfiguration,
  type IConfig,
  type ITelemetryItem,
  type ITelemetryPlugin,
  type ICustomProperties,
  type IPageViewTelemetry,
  type IEventTelemetry,
  type IExceptionTelemetry,
  type ITraceTelemetry,
  type IMetricTelemetry,
  type IDependencyTelemetry
} from "@microsoft/applicationinsights-web";
```

## 最佳实践

1. **单例实例**,从单一模块导出。
2. **尽早初始化**,在应用入口处,路由设置之前。
3. **使用遥测初始化器**附加 `app.version`、`tenantId`,并清理 PII / 查询字符串密钥。
4. **设置 `distributedTracingMode: 2`**,并确保你的 API 能接受/暴露 W3C trace context 头。
5. **对于 GenAI**,严格遵循 OTel 的 `gen_ai.*` 属性名称 —— 它们可以在浏览器和后端遥测之间统一查询。
6. **将敏感内容捕获**(`gen_ai.input.messages` / `gen_ai.output.messages`)置于构建时或运行时的显式开关之后。
7. **在登出 / 敏感跳转时刷送**,以免正在传输的遥测数据被丢弃。

## 参考资料

- [references/agent-traces.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/agent-traces.md) —— 完整提炼的 OTel GenAI 语义约定(agent / model / tool span、属性、内容捕获)。
- [references/framework-extensions.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/framework-extensions.md) —— React、React Native、Angular、Next.js、Vite 配方。
- [references/configuration.md](https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-typescript/skills/applicationinsights-web-ts/references/configuration.md) —— 完整的 `IConfiguration` 参考和调优指南。
- Microsoft Learn: <https://learn.microsoft.com/azure/azure-monitor/app/javascript-sdk>
- ApplicationInsights-JS 源码: <https://github.com/microsoft/ApplicationInsights-JS>
- OTel GenAI 语义约定: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>

## 局限性

- 仅在任务明确匹配其上游来源与本地项目场景时使用此技能。
- 在应用变更前验证命令、生成的代码、依赖、凭据以及外部服务行为。
- 不要将示例当作针对特定环境测试、安全审查,或针对破坏性/高成本操作用户批准的替代品。
