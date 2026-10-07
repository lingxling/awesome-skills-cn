---
name: add-app-clip
description: 为 Expo 应用添加 iOS App Clip 目标。当用户提到 App Clip、AASA、apple-app-site-association、appclips、智能应用横幅（smart app banner），或想要发布一个与主应用并行、通过 URL 唤起的轻量级 iOS Clip 时使用。
risk: critical
source: https://github.com/expo/skills/tree/main/plugins/expo/skills/add-app-clip
source_repo: expo/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/expo/skills/blob/main/LICENSE
---

# 为 Expo 应用添加 App Clip
## 何时使用

当你需要为 Expo 应用添加 iOS App Clip 目标时使用本技能。当用户提到 App Clip、AASA、apple-app-site-association、appclips、智能应用横幅（smart app banner），或想要发布一个与主应用并行、通过 URL 唤起的轻量级 iOS Clip 时使用。


为 Expo 项目添加 iOS App Clip 目标。该 Clip 位于 `targets/clip/`，与主应用一同发布，并通过 Apple App Site Association（AASA）文件，由应用域名上的 URL 唤起。

主应用的 bundle ID 为 `com.<username>.<app-name>`，Clip 的 bundle ID 会自动派生为 `<parent>.clip`（例如 `com.bacon.may20.clip`）。

## 1. 设置 `bundleIdentifier` 和 `appleTeamId`

如果缺少这些配置，`bun create target` 会给出警告。将其添加到 `app.json`：

```json
{
  "expo": {
    "ios": {
      "bundleIdentifier": "com.<username>.<app-name>",
      "appleTeamId": "XX57RJ5UTD"
    }
  }
}
```

## 2. 添加 App Clip 目标

```sh
bun create target clip
```

该命令会安装 [`@bacons/apple-targets`](https://github.com/EvanBacon/expo-apple-targets)，将其加入 `app.json` 的 `plugins` 数组，并写入：

- `targets/clip/expo-target.config.js` —— 该目标的 config plugin
- `targets/clip/Info.plist` —— Clip 的 Info.plist
- `targets/clip/AppDelegate.swift`、`Assets.xcassets` 等

选择一个合适的图标，或复用应用中已定义的图标——可通过 `bunx expo config` 在 `icon` 或 `ios.icon` 键下查看。

## 3. 配置 Associated Domains

主应用和 Clip 都需要配置 Associated Domains 权限（entitlement），指向托管 AASA 文件的域名。

在 `app.json` 中，同时添加 `applinks:`（主应用）和 `appclips:`（Clip 唤起）条目：

```json
{
  "expo": {
    "ios": {
      "associatedDomains": [
        "applinks:may20.expo.app",
        "appclips:may20.expo.app"
      ]
    }
  }
}
```

在 `targets/clip/expo-target.config.js` 中声明 Clip 的 entitlement：

```js
/** @type {import('@bacons/apple-targets/app.plugin').ConfigFunction} */
module.exports = (config) => ({
  type: "clip",
  icon: "https://github.com/expo.png",
  entitlements: {
    "com.apple.developer.associated-domains": ["appclips:may20.expo.app"],
  },
});
```

> 如果跳过此步骤，`expo prebuild` 会输出：`Apple App Clip may require the associated domains entitlement but none were found`。

## 4. 注册 bundle ID 并创建 App Store 条目

```sh
bunx setup-safari
```

该命令会登录 Apple Developer 账号，注册 `com.bacon.may20`，创建 App Store Connect 条目，并输出：

- 一份初始的 `apple-app-site-association` JSON
- 包含 iTunes app id 的 `<meta name="apple-itunes-app">` 标签
- Team ID、iTunes ID 和 Bundle ID

## 5. 托管 AASA 文件

当 iOS 获取 `https://<your-domain>/.well-known/apple-app-site-association` 并找到匹配的 `appclips` 条目时，App Clip 就会被唤起。

```sh
mkdir -p public/.well-known
touch public/.well-known/apple-app-site-association
```

粘贴 `setup-safari` 输出的 JSON，但要为 Clip 的完整 app ID（`<TeamID>.<ClipBundleID>`）**添加一个 `appclips` 块**。`setup-safari` 的输出只涵盖主应用：

```json
{
  "applinks": {
    "details": [
      {
        "appIDs": ["XX57RJ5UTD.com.bacon.may20"],
        "components": [{ "/": "*", "comment": "Matches all routes" }]
      }
    ]
  },
  "appclips": {
    "apps": ["XX57RJ5UTD.com.bacon.may20.clip"]
  },
  "activitycontinuation": {
    "apps": ["XX57RJ5UTD.com.bacon.may20"]
  },
  "webcredentials": {
    "apps": ["XX57RJ5UTD.com.bacon.may20"]
  }
}
```

注意事项：

- 该文件**没有扩展名**，且除了按原样提供之外**没有 `Content-Type` 要求**。Expo Router 的静态导出会原样提供 `public/` 中的文件。
- `appclips` 块使得该域名上的 URL 能够启动 Clip。
- `webcredentials` 用于在网站、主应用和 App Clip 之间共享凭据。
- `activitycontinuation` 是可选的，用于在移动端和桌面端之间共享链接。必须配合 expo-router 的 `Head` 使用——参见 https://docs.expo.dev/router/advanced/apple-handoff/
- 记法与禁用路由的详细说明：https://sosumi.ai/documentation/xcode/supporting-associated-domains

## 6. 添加智能应用横幅（Smart App Banner）meta 标签

创建 `src/app/+html.tsx`（Expo Router 的 HTML 外壳），并添加 `setup-safari` 输出的标签。如果带版本的模板尚不存在，请先创建：

```sh
bunx expo customize src/app/+html.tsx
```

将 meta 标签添加到 `<head>` 中：

```tsx
import { ScrollViewStyleReset } from "expo-router/html";

export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="apple-itunes-app" content="app-id=6771566491" />
        <ScrollViewStyleReset />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

若要让网站显示 App Clip 卡片而不是安装卡片，请使用：

```html
<meta
  name="apple-itunes-app"
  content="app-id=6771566491, app-clip-bundle-id=com.bacon.may20.clip, app-clip-display=card"
/>
```

## 7. 部署网站

AASA 文件必须先上线，iOS 才会信任该关联。使用 [EAS Hosting](https://docs.expo.dev/eas/hosting/)：

```sh
bunx expo export -p web
eas deploy --prod
```

这会将站点（包括 `/.well-known/apple-app-site-association`）发布到 `https://<slug>.expo.app`。验证：

```sh
curl https://may20.expo.app/.well-known/apple-app-site-association
```

## 8. 同步权限

在 prebuild 之后检查主应用的权限：

```sh
npx expo config --type introspect
```

查看 `infoPlist` 对象——将权限键同步到 App Clip 的 `Info.plist` 中，以便在 Clip 中使用相应的 API。

在 Clip 的目标配置中设置 `deploymentTarget: "17.6"`——App Clip 在 iOS 17.6 中有更高的最小体积限制。

如果应用使用推送通知或定位服务，请将以下内容添加到 App Clip 的 `Info.plist` 以请求必要的权限：

```xml
<key>NSAppClip</key>
<dict>
  <key>NSAppClipRequestEphemeralUserNotification</key>
  <false/>
  <key>NSAppClipRequestLocationConfirmation</key>
  <true/>
</dict>
```

## 9. 构建并提交到 TestFlight

```sh
bunx testflight
```

该命令将会：

1. 若缺少 `eas.json`，则生成一个。
2. 为**两个**目标（主应用 + Clip）设置凭据。每个目标有各自的 provisioning profile，但可以共用同一个 Distribution Certificate。
3. 同步 capabilities——注意 Clip 目标处的 `Enabled: Associated Domains`。
4. 构建、上传并安排 TestFlight 提交。

## 10. 配置 App Clip 元数据

将现有的 App Store 元数据拉取到本地：

```sh
eas metadata:pull
```

在 `store.config.json` 中添加 `apple.appClip`。最多可以有 3 个调用 URL 从网页启动该 Clip：

```json
{
  "configVersion": 0,
  "apple": {
    "appClip": {
      "defaultExperience": {
        "action": "PLAY",
        "releaseWithAppStoreVersion": true,
        "reviewDetail": {
          "invocationUrls": ["https://may20.expo.app/", null, null]
        },
        "info": {
          "en-US": {
            "subtitle": "Instantly native with Expo",
            "headerImage": "store/apple/app-clip/en-US/asc-app-clip.png"
          }
        }
      }
    }
  }
}
```

`headerImage` 必须是 1800x1200 的 PNG，且不含透明度。

推送回商店：

```sh
eas metadata:push
```

Apple 推荐的 App Clip 元数据指南：https://sosumi.ai/documentation/appclip/configuring-the-launch-experience-of-your-app-clip

## 最终成果

- 主应用目标：`com.bacon.may20`
- App Clip 目标：`com.bacon.may20.clip`，位于 `targets/clip/`
- AASA 托管在 `https://may20.expo.app/.well-known/apple-app-site-association`
- 每个 Web 路由都带有智能应用横幅 meta 标签
- 每个路由都与其对应的原生页面相关联
- 主应用的 TestFlight 构建，其中嵌入了该 Clip

一旦 Apple 从该域名上的 URL 唤起 Clip，iOS 就会打开 `targets/clip/` 的入口点，并加载 React Native 应用。

## 原生检测（可选）

若要让 JS 检测自己是否运行在 App Clip 内，并向用户展示完整应用的安装提示，请创建一个本地 Expo 模块（`bunx create-expo-module --local`），并暴露 `navigator.appClip.prompt()`。

Swift 模块、TypeScript 接口及用法请参见 [./references/native-module.md](./references/native-module.md)。

## 参考资料

- ./references/native-module.md —— 用于检测 App Clip 上下文并展示 SKOverlay 安装提示的本地 Expo 模块

## 局限性

- 仅在任务明确符合其上游产品或 API 范围时使用本技能。
- 在进行更改之前，请对照当前官方文档核实命令、API 行为、定价、配额、凭据和部署影响。
- 不要将生成的示例视为针对具体环境的测试、安全审查，或对破坏性/高成本操作的用户批准的替代品。
