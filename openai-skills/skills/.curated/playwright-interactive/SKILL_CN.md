---
name: "playwright-interactive"
description: "通过 `js_repl` 进行持久的浏览器和 Electron 交互，用于快速迭代 UI 调试。"
---

# Playwright Interactive 技能

使用持久的 `js_repl` Playwright 会话来调试本地 Web 或 Electron 应用程序，在迭代过程中保持相同的句柄活动，并在不需要重新启动整个工具链的情况下运行功能加视觉 QA，除非进程所有权发生了变化。

## 先决条件

- 必须为此技能启用 `js_repl`。
- 如果缺少 `js_repl`，请在 `~/.codex/config.toml` 中启用它：

```toml
[features]
js_repl = true
```

- 您也可以使用 `--enable js_repl` 启动新会话（等效于 `-c features.js_repl=true`）。
- 启用 `js_repl` 后，启动新的 Codex 会话以便工具列表刷新。
- 目前，在禁用沙盒的情况下运行此工作流程：使用 `--sandbox danger-full-access` 启动 Codex（或 `sandbox_mode=danger-full-access` 的等效配置）。这是一个临时要求，因为沙盒内的 `js_repl` + Playwright 支持仍在完成中。
- 从您需要调试的同一项目目录运行设置。
- 将 `js_repl_reset` 视为恢复工具，而不是例程清理。重置内核会破坏您的 Playwright 句柄。

## 一次性设置

```bash
test -f package.json || npm init -y
npm install playwright
# 仅 Web，用于有头 Chromium 或移动模拟：
# npx playwright install chromium
# 仅 Electron，并且仅当目标工作区是应用程序本身时：
# npm install --save-dev electron
node -e "import('playwright').then(() => console.log('playwright import ok')).catch((error) => { console.error(error); process.exit(1); })"
```

如果您稍后切换到不同的工作区，请在那里重复设置。

## 核心工作流程

1. 在测试之前编写简短的 QA 清单：
   - 从三个来源构建清单：用户请求的要求、您实际实现的用户可见功能或行为，以及您期望在最终响应中做出的声明。
   - 出现在这三个来源中任何一个的内容都必须在签收之前映射到至少一个 QA 检查。
   - 列出您打算签收的用户可见声明。
   - 列出每个有意义的面向用户的控制、模式切换或实现的交互行为。
   - 列出每个控制或实现的行为可以导致的状态更改或视图更改。
   - 将此用作功能 QA 和视觉 QA 的共享覆盖列表。
   - 对于每个声明或控制状态对，注意预期的功能检查、必须进行视觉检查的特定状态以及您期望捕获的证据。
   - 如果要求在视觉上居中但是主观的，请将其转换为可观察的 QA 检查，而不是将其保留为隐式。
   - 添加至少 2 个探索性或非快乐路径场景，这些场景可能暴露脆弱的行为。
2. 运行引导单元一次。
3. 在持久的 TTY 会话中启动或确认任何必需的开发服务器。
4. 启动正确的运行时并保持重用相同的 Playwright 句柄。
5. 在每次代码更改后，对于仅渲染器更改重新加载，对于主进程/启动更改重新启动。
6. 使用正常用户输入运行功能 QA。
7. 运行单独的视觉 QA 传递。
8. 验证视口适配并捕获支持您的声明所需的屏幕截图。
9. 仅当任务实际完成时才清理 Playwright 会话。

## 引导（运行一次）

```javascript
var chromium;
var electronLauncher;
var browser;
var context;
var page;
var mobileContext;
var mobilePage;
var electronApp;
var appWindow;

try {
  ({ chromium, _electron: electronLauncher } = await import("playwright"));
  console.log("Playwright loaded");
} catch (error) {
  throw new Error(
    `Could not load playwright from current js_repl cwd. Run setup commands from this workspace first. Original error: ${error}`
  );
}
```

绑定规则：

- 对共享的顶级 Playwright 句柄使用 `var`，因为后面的 `js_repl` 单元会重用它们。
- 下面的设置单元故意是简短的快乐路径。如果句柄看起来过时，请将该绑定设置为 `undefined` 并重新运行单元，而不是到处添加恢复逻辑。
- 优先考虑每个您关心的表面一个命名句柄（`page`、`mobilePage`、`appWindow`），而不是从上下文重复重新发现页面。

共享的 Web 助手：

```javascript
var resetWebHandles = function () {
  context = undefined;
  page = undefined;
  mobileContext = undefined;
  mobilePage = undefined;
};

var ensureWebBrowser = async function () {
  if (browser && !browser.isConnected()) {
    browser = undefined;
    resetWebHandles();
  }

  browser ??= await chromium.launch({ headless: false });
  return browser;
};

var reloadWebContexts = async function () {
  for (const currentContext of [context, mobileContext]) {
    if (!currentContext) continue;
    for (const p of currentContext.pages()) {
      await p.reload({ waitUntil: "domcontentloaded" });
    }
  }
  console.log("Reloaded existing web tabs");
};
```

## 选择会话模式

对于 Web 应用程序，默认使用显式视口，并将原生窗口模式视为单独的验证传递。

- 对例程迭代、断点检查、可重现的屏幕截图、快照差异和模型辅助本地化使用显式视口。这是默认值，因为它在机器之间稳定，并避免了主机窗口管理器的可变性。
- 当您需要确定性的高 DPI 行为时，保持显式视口并添加 `deviceScaleFactor`，而不是直接切换到原生窗口模式。
- 对单独的有头传递使用原生窗口模式（`viewport: null`），当您需要验证启动的窗口大小、操作系统级别的 DPI 行为、浏览器 chrome 交互或可能依赖于主机显示配置的错误时。
- 对于 Electron，始终假设原生窗口行为。Electron 通过 Playwright 使用 `noDefaultViewport` 启动，因此将其视为真实的桌面窗口，并在调整任何内容之前检查启动时的大小和布局。
- 当签收依赖于布局断点和真实桌面行为时，执行两次传递：首先是确定性的 QA 的显式视口，然后是最终环境特定检查的原生窗口验证。
- 将切换模式视为上下文重置。不要为原生窗口传递重用视口模拟的 `context`，反之亦然；关闭旧的 `page` 和 `context`，然后为新模式创建一个新的。

## 启动或重用 Web 会话

桌面和移动 Web 会话共享相同的 `browser`、助手和 QA 流程。主要区别是您创建哪个上下文和页面对。

### 桌面 Web 上下文

将 `TARGET_URL` 设置为您正在调试的应用程序。对于本地服务器，优先考虑 `127.0.0.1` 而不是 `localhost`。

```javascript
var TARGET_URL = "http://127.0.0.1:3000";

if (page?.isClosed()) page = undefined;

await ensureWebBrowser();
context ??= await browser.newContext({
  viewport: { width: 1600, height: 900 },
});
page ??= await context.newPage();

await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded:", await page.title());
```

如果 `context` 或 `page` 过时，请设置 `context = page = undefined` 并重新运行单元。

### 移动 Web 上下文

当 `TARGET_URL` 已存在时重用它；否则直接设置移动目标。

```javascript
var MOBILE_TARGET_URL = typeof TARGET_URL === "string"
  ? TARGET_URL
  : "http://127.0.0.1:3000";

if (mobilePage?.isClosed()) mobilePage = undefined;

await ensureWebBrowser();
mobileContext ??= await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
});
mobilePage ??= await mobileContext.newPage();

await mobilePage.goto(MOBILE_TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded mobile:", await mobilePage.title());
```

如果 `mobileContext` 或 `mobilePage` 过时，请设置 `mobileContext = mobilePage = undefined` 并重新运行单元。

### 原生窗口 Web 传递

```javascript
var TARGET_URL = "http://127.0.0.1:3000";

await ensureWebBrowser();

await page?.close().catch(() => {});
await context?.close().catch(() => {});
page = undefined;
context = undefined;

browser ??= await chromium.launch({ headless: false });
context = await browser.newContext({ viewport: null });
page = await context.newPage();

await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded native window:", await page.title());
```

## 启动或重用 Electron 会话

当当前工作区是 Electron 应用程序且 `package.json` 将 `main` 指向正确的入口文件时，将 `ELECTRON_ENTRY` 设置为 `.`。如果您需要直接定位特定的主进程文件，请使用诸如 `./main.js` 之类的路径。

```javascript
var ELECTRON_ENTRY = ".";

if (appWindow?.isClosed()) appWindow = undefined;

if (!appWindow && electronApp) {
  await electronApp.close().catch(() => {});
  electronApp = undefined;
}

electronApp ??= await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

appWindow ??= await electronApp.firstWindow();

console.log("Loaded Electron window:", await appWindow.title());
```

如果 `js_repl` 尚未从 Electron 应用程序工作区运行，请在启动时显式传递 `cwd`。

如果应用程序进程看起来过时，请设置 `electronApp = appWindow = undefined` 并重新运行单元。

如果您已经有 Electron 会话但在主进程、预加载或启动更改后需要新进程，请在下一部分使用重新启动单元，而不是重新运行此单元。

## 在迭代期间重用会话

尽可能保持相同的会话活动。

Web 渲染器重新加载：

```javascript
await reloadWebContexts();
```

Electron 仅渲染器重新加载：

```javascript
await appWindow.reload({ waitUntil: "domcontentloaded" });
console.log("Reloaded Electron window");
```

主进程、预加载或启动更改后的 Electron 重新启动：

```javascript
await electronApp.close().catch(() => {});
electronApp = undefined;
appWindow = undefined;

electronApp = await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

appWindow = await electronApp.firstWindow();
console.log("Relaunched Electron window:", await appWindow.title());
```

如果您的启动需要显式 `cwd`，请在此处包含相同的 `cwd`。

默认姿态：

- 保持每个 `js_repl` 单元简短并专注于一个交互爆发。
- 重用现有的顶级绑定（`browser`、`context`、`page`、`electronApp`、`appWindow`），而不是重新声明它们。
- 如果您需要隔离，请在同一浏览器内创建新页面或新上下文。
- 对于 Electron，仅对主进程检查或专门构建的诊断使用 `electronApp.evaluate(...)`。
- 在原位修复助手错误；不要重置 REPL，除非内核实际损坏。

## 清单

### 会话循环

- 引导 `js_repl` 一次，然后在迭代过程中保持相同的 Playwright 句柄活动。
- 从当前工作区启动目标运行时。
- 进行代码更改。
- 使用该更改的正确路径重新加载或重新启动。
- 如果探索揭示了额外的控制、状态或可见声明，请更新共享 QA 清单。
- 重新运行功能 QA。
- 重新运行视觉 QA。
- 仅在当前状态是您正在评估的状态时才捕获最终工件。

### 重新加载决策

- 仅渲染器更改：重新加载现有页面或 Electron 窗口。
- 主进程、预加载或启动更改：重新启动 Electron。
- 关于进程所有权或启动代码的新不确定性：重新启动而不是猜测。

### 功能 QA

- 使用真实的用户控制进行签收：键盘、鼠标、点击、触摸或等效的 Playwright 输入 API。
- 验证至少一个端到端的关键流程。
- 确认该流程的可见结果，而不仅仅是内部状态。
- 对于实时或动画繁重的应用程序，在实际交互时间下验证行为。
- 通过共享 QA 清单工作，而不是临时点检查。
- 在签收之前至少覆盖一次每个明显的可见控制，而不仅仅是主要快乐路径。
- 对于清单中的可逆控制或有状态切换，测试完整循环：初始状态、更改状态和返回初始状态。
- 在脚本检查通过后，使用正常输入进行 30-90 秒的简短探索性传递，而不是仅遵循预期路径。
- 如果探索性传递揭示了新状态、控制或声明，请将其添加到共享 QA 清单并在签收之前覆盖它。
- `page.evaluate(...)` 和 `electronApp.evaluate(...)` 可以检查或暂存状态，但它们不算作签收输入。

### 视觉 QA

- 将视觉 QA 视为与功能 QA 分开。
- 使用在测试之前定义并在 QA 期间更新的相同共享 QA 清单；不要从不同的隐式列表开始视觉覆盖。
- 重申用户可见声明并明确验证每一个；不要假设功能传递证明视觉声明。
- 用户可见声明未签收，直到它已在旨在被感知的特定状态下被检查。
- 在滚动之前检查初始视口。
- 确认初始视图明显支持界面的主要声明；如果核心承诺的元素在那里不清楚可见，请将其视为错误。
- 检查所有必需的可见区域，而不仅仅是主要交互表面。
- 检查共享 QA 清单中已枚举的状态和模式，包括当任务是交互式的时至少一个有意义的交互后状态。
- 如果运动或过渡是体验的一部分，除了已确定的端点之外，还要检查至少一个过渡中状态。
- 如果标签、覆盖、注释、指南或高亮旨在跟踪更改的内容，请在相关状态更改后验证该关系。
- 对于动态或依赖交互的视觉效果，检查足够长的时间以判断稳定性、分层和可读性；不要依赖单个屏幕截图进行签收。
- 对于在加载或交互后可能变得更密集的界面，检查您在 QA 期间可以达到的最密集的现实状态，而不仅仅是空、加载或折叠状态。
- 如果产品定义了最小支持的视口或窗口大小，请在那里运行单独的视觉 QA 传递；否则，选择一个更小但仍然现实的大小并明确检查它。
- 区分存在与实现：如果预期的功能在技术上存在，但由于弱对比度、遮挡、裁剪或不稳定性而不清楚可见，请将其视为视觉失败。
- 如果在您正在评估的状态中，任何必需的可见区域被裁剪、切断、遮挡或推到视口之外，请将其视为错误，即使页面级别的滚动指标看起来可以接受。
- 查找裁剪、溢出、扭曲、布局不平衡、不一致的间距、对齐问题、难以辨认的文本、弱对比度、损坏的分层和尴尬的运动状态。
- 判断美学质量以及正确性。对于任务，UI 应该感觉有意、连贯且视觉上令人愉悦。
- 优先考虑视口屏幕截图进行签收。仅将整页捕获用作次要调试工件，并在区域需要更仔细检查时捕获聚焦的屏幕截图。
- 如果运动使屏幕截图模棱两可，请短暂等待 UI 稳定，然后捕获您实际评估的图像。
- 在签收之前，明确询问：此界面的哪些可见部分我尚未仔细检查？
- 在签收之前，明确询问：如果用户仔细查看，什么可见缺陷最可能使此结果尴尬？

### 签收

- 功能路径通过正常用户输入。
- 覆盖针对共享 QA 清单是明确的：注意哪些要求、实现的功能、控制、状态和声明已执行，并调用任何有意排除。
- 视觉 QA 传递覆盖了整个相关界面。
- 每个用户可见声明都有匹配的视觉检查和来自该声明相关的状态和视口或窗口大小的已审查屏幕截图工件。
- 视口适配检查通过了预期的初始视图和任何必需的最小支持视口或窗口大小。
- 如果产品在窗口中启动，启动时的大小、位置和初始布局在任何手动调整大小或重新定位之前已检查。
- UI 不仅功能正常；对于任务，它在视觉上是连贯的，并且在美学上不弱。
- 功能正确性、视口适配和视觉质量必须各自通过；一个并不意味着其他。
- 对交互产品完成了简短的探索性传递，响应提到了该传递覆盖了什么。
- 如果屏幕截图审查和数字检查在任何点不同意，请在签收之前调查差异；屏幕截图中的可见裁剪是需要解决的失败，而不是指标可以推翻的东西。
- 包括您检查并未发现的主要缺陷类别的简短否定确认。
- 已执行清理，或者您有意保持会话活动以进行进一步工作。

## 屏幕截图示例

如果您计划通过 `codex.emitImage(...)` 发出屏幕截图，默认情况下在下一部分中使用 CSS 标准化路径。这些是将由模型解释或用于基于坐标的后续操作的屏幕截图像范示例。将原始捕获保留为仅保真度敏感调试的例外；原始异常示例出现在标准化指导之后。

### 模型绑定的屏幕截图（默认）

如果您将通过 `codex.emitImage(...)` 发出屏幕截图以进行模型解释，请在发出之前将其标准化为您捕获的确切区域的 CSS 像素。如果回复稍后用于点击，这将使返回的坐标与 Playwright CSS 像素对齐，并且它还减少了图像有效负载大小和模型令牌成本。

默认情况下不要发出原始原生窗口屏幕截图。仅在您明确需要设备像素保真度（例如 Retina 或 DPI 工件调试、像素准确的渲染检查或另一个保真度敏感情况，其中原始像素比有效负载大小更重要）时才跳过标准化。对于仅本地且不会发出到模型的检查，原始捕获是可以的。

不要假设 `page.screenshot({ scale: "css" })` 在原生窗口模式（`viewport: null`）中就足够了。在 macOS Retina 显示屏上的 Chromium 中，有头原生窗口屏幕截图即使在请求 `scale: "css"` 时仍可能以设备像素大小返回。同样的警告适用于通过 Playwright 启动的 Electron 窗口，因为 Electron 使用 `noDefaultViewport` 运行，并且 `appWindow.screenshot({ scale: "css" })` 可能仍返回设备像素输出。

为 Web 页面和 Electron 窗口使用单独的标准化路径：

- Web：优先考虑直接使用 `page.screenshot({ scale: "css" })`。如果原生窗口 Chromium 仍返回设备像素输出，请在当前页面中使用 canvas 调整大小；不需要临时页面。
- Electron：不要使用 `appWindow.context().newPage()` 或 `electronApp.context().newPage()` 作为临时页面。Electron 上下文不能可靠地支持该路径。在主进程中使用 `BrowserWindow.capturePage(...)` 捕获，使用 `nativeImage.resize(...)` 调整大小，并直接发出这些字节。

共享助手和约定：

```javascript
var emitJpeg = async function (bytes) {
  await codex.emitImage({
    bytes,
    mimeType: "image/jpeg",
  });
};

var emitWebJpeg = async function (surface, options = {}) {
  await emitJpeg(await surface.screenshot({
    type: "jpeg",
    quality: 85,
    scale: "css",
    ...options,
  }));
};

var clickCssPoint = async function ({ surface, x, y, clip }) {
  await surface.mouse.click(
    clip ? clip.x + x : x,
    clip ? clip.y + y : y
  );
};

var tapCssPoint = async function ({ page, x, y, clip }) {
  await page.touchscreen.tap(
    clip ? clip.x + x : x,
    clip ? clip.y + y : y
  );
};
```

- 对 Web 使用 `page` 或 `mobilePage`，或对 Electron 使用 `appWindow` 作为 `surface`。
- 将 `clip` 视为来自渲染器中 `getBoundingClientRect()` 的 CSS 像素。
- 除非特别要求无损保真度，否则优先考虑 `quality: 85` 的 JPEG。
- 对于全图像捕获，直接使用返回的 `{ x, y }`。
- 对于裁剪的捕获，在点击时添加裁剪原点。

### Web CSS 标准化

显式视口上下文的首选 Web 路径，并且通常对于 Web 一般情况：

```javascript
await emitWebJpeg(page);
```

移动 Web 使用相同的路径；将 `mobilePage` 替换为 `page`：

```javascript
await emitWebJpeg(mobilePage);
```

如果模型返回 `{ x, y }`，请直接点击它：

```javascript
await clickCssPoint({ surface: page, x, y });
```

移动 Web 点击路径：

```javascript
await tapCssPoint({ page: mobilePage, x, y });
```

对于此标准路径中的 Web `clip` 屏幕截图或元素屏幕截图，`scale: "css"` 通常直接有效。在点击时添加区域原点。

- `await emitWebJpeg(page, { clip })`
- `await emitWebJpeg(mobilePage, { clip })`
- `await clickCssPoint({ surface: page, clip, x, y })`
- `await tapCssPoint({ page: mobilePage, clip, x, y })`
- `await clickCssPoint({ surface: page, clip: box, x, y })` 在 `const box = await locator.boundingBox()` 之后

当 `scale: "css"` 仍以设备像素大小返回时的 Web 原生窗口回退：

```javascript
var emitWebScreenshotCssScaled = async function ({ page, clip, quality = 0.85 } = {}) {
  var NodeBuffer = (await import("node:buffer")).Buffer;
  const target = clip
    ? { width: clip.width, height: clip.height }
    : await page.evaluate(() => ({
        width: window.innerWidth,
        height: window.innerHeight,
      }));

  const screenshotBuffer = await page.screenshot({
    type: "png",
    ...(clip ? { clip } : {}),
  });

  const bytes = await page.evaluate(
    async ({ imageBase64, targetWidth, targetHeight, quality }) => {
      const image = new Image();
      image.src = `data:image/png;base64,${imageBase64}`;
      await image.decode();

      const canvas = document.createElement("canvas");
      canvas.width = targetWidth;
      canvas.height = targetHeight;

      const ctx = canvas.getContext("2d");
      ctx.imageSmoothingEnabled = true;
      ctx.drawImage(image, 0, 0, targetWidth, targetHeight);

      const blob = await new Promise((resolve) =>
        canvas.toBlob(resolve, "image/jpeg", quality)
      );

      return new Uint8Array(await blob.arrayBuffer());
    },
    {
      imageBase64: NodeBuffer.from(screenshotBuffer).toString("base64"),
      targetWidth: target.width,
      targetHeight: target.height,
      quality,
    }
  );

  await emitJpeg(bytes);
};
```

对于全视口回退捕获，将返回的 `{ x, y }` 视为直接 CSS 坐标：

```javascript
await emitWebScreenshotCssScaled({ page });
await clickCssPoint({ surface: page, x, y });
```

对于裁剪的回退捕获，添加裁剪原点：

```javascript
await emitWebScreenshotCssScaled({ page, clip });
await clickCssPoint({ surface: page, clip, x, y });
```

### Electron CSS 标准化

对于 Electron，在主进程中标准化而不是打开临时的 Playwright 页面。下面的助手返回全内容区域或裁剪的 CSS 像素区域的 CSS 缩放字节。将 `clip` 视为内容区域 CSS 像素，例如从渲染器中的 `getBoundingClientRect()` 获取的值。

```javascript
var emitElectronScreenshotCssScaled = async function ({ electronApp, clip, quality = 85 } = {}) {
  const bytes = await electronApp.evaluate(async ({ BrowserWindow }, { clip, quality }) => {
    const win = BrowserWindow.getAllWindows()[0];
    const image = clip ? await win.capturePage(clip) : await win.capturePage();

    const target = clip
      ? { width: clip.width, height: clip.height }
      : (() => {
          const [width, height] = win.getContentSize();
          return { width, height };
        })();

    const resized = image.resize({
      width: target.width,
      height: target.height,
      quality: "best",
    });

    return resized.toJPEG(quality);
  }, { clip, quality });

  await emitJpeg(bytes);
};
```

全 Electron 窗口：

```javascript
await emitElectronScreenshotCssScaled({ electronApp });
await clickCssPoint({ surface: appWindow, x, y });
```

使用来自渲染器的 CSS 像素的裁剪 Electron 区域：

```javascript
var clip = await appWindow.evaluate(() => {
  const rect = document.getElementById("board").getBoundingClientRect();
  return {
    x: Math.round(rect.x),
    y: Math.round(rect.y),
    width: Math.round(rect.width),
    height: Math.round(rect.height),
  };
});

await emitElectronScreenshotCssScaled({ electronApp, clip });
await clickCssPoint({ surface: appWindow, clip, x, y });
```

### 原始屏幕截图异常示例

仅当原始像素比 CSS 坐标对齐更重要时才使用这些，例如 Retina 或 DPI 工件调试、像素准确的渲染检查或其他保真度敏感审查。

Web 桌面原始发出：

```javascript
await codex.emitImage({
  bytes: await page.screenshot({ type: "jpeg", quality: 85 }),
  mimeType: "image/jpeg",
});
```

Electron 原始发出：

```javascript
await codex.emitImage({
  bytes: await appWindow.screenshot({ type: "jpeg", quality: 85 }),
  mimeType: "image/jpeg",
});
```

在移动 Web 上下文已运行后的移动原始发出：

```javascript
await codex.emitImage({
  bytes: await mobilePage.screenshot({ type: "jpeg", quality: 85 }),
  mimeType: "image/jpeg",
});
```

## 视口适配检查（必需）

不要仅因为主要小部件可见就假设屏幕截图可以接受。在签收之前，明确验证预期的初始视图符合产品要求，同时使用屏幕截图审查和数字检查。

- 在签收之前定义预期的初始视图。对于可滚动页面，这是折上体验。对于类似应用程序的外壳、游戏、编辑器、仪表板或工具，这是完整的交互表面加上使用它所需的控制和状态。
- 将屏幕截图用作适配的主要证据。数字检查支持屏幕截图；它们不能推翻可见裁剪。
- 如果在预期初始视图中，任何必需的可见区域被裁剪、切断、遮挡或推到视口之外，签收失败，即使页面级别的滚动指标看起来可以接受。
- 当产品设计为滚动且初始视图仍然传达核心体验并暴露主要行动号召或必需的起始上下文时，滚动是可以接受的。
- 对于固定外壳界面，如果需要滚动以到达主要交互表面的一部分或必需控制，则滚动不是可接受的变通方法。
- 不要仅依赖文档滚动指标。固定高度外壳、内部窗格和隐藏溢出容器可以在页面级别滚动检查仍然看起来干净时裁剪所需的 UI。
- 检查区域边界，而不仅仅是文档边界。验证每个必需的可见区域在启动状态下适合视口。
- 对于 Electron 或桌面应用程序，在任何手动调整大小或重新定位之前，验证启动的窗口大小和位置以及渲染器的初始可见布局。
- 通过视口适配检查仅证明预期的初始视图可见而没有意外的裁剪或滚动。它不证明 UI 在视觉上正确或在美学上成功。

Web 或渲染器检查：

```javascript
console.log(await page.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  clientWidth: document.documentElement.clientWidth,
  clientHeight: document.documentElement.clientHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
  canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight,
})));
```

Electron 检查：

```javascript
console.log(await appWindow.evaluate(() => ({
  innerWidth: window.innerWidth,
  innerHeight: window.innerHeight,
  clientWidth: document.documentElement.clientWidth,
  clientHeight: document.documentElement.clientHeight,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
  canScrollX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  canScrollY: document.documentElement.scrollHeight > document.documentElement.clientHeight,
})));
```

当裁剪是现实的失败模式时，使用 `getBoundingClientRect()` 检查增强数字检查以获取您特定 UI 中的必需可见区域；仅文档级别的指标对于固定外壳是不够的。

## 开发服务器

对于本地 Web 调试，请在持久的 TTY 会话中保持应用程序运行。不要依赖来自短暂 shell 的一次性后台命令。

使用项目的正常启动命令，例如：

```bash
npm start
```

## 故障排除

- 浏览器启动或网络操作立即失败：确认会话是使用 `--sandbox danger-full-access` 启动的，并在需要时以该方式重新启动。
