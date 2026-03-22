---
name: "develop-web-game"
description: "当 Codex 正在构建或迭代 Web 游戏（HTML/JS）并且需要可靠的开发 + 测试循环时使用：实现小更改、运行基于 Playwright 的测试脚本（包含短输入突发和有意暂停）、检查截图/文本、并使用 render_game_to_text 审查控制台错误。"
---

# 开发 Web 游戏

以小步骤构建游戏并在每次更改后进行验证。将每次迭代视为：实现 → 行动 → 暂停 → 观察 → 调整。

## 技能路径（设置一次）

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export WEB_GAME_CLIENT="$CODEX_HOME/skills/develop-web-game/scripts/web_game_playwright_client.js"
export WEB_GAME_ACTIONS="$CODEX_HOME/skills/develop-web-game/references/action_payloads.json"
```

用户范围的技能安装在 `$CODEX_HOME/skills` 下（默认：`~/.codex/skills`）。

## 工作流程

1. **选择目标。** 定义要实现的单个功能或行为。
2. **实现小更改。** 做出推动游戏前进的最小更改。
3. **确保集成点。** 提供单个画布和 `window.render_game_to_text`，以便测试循环可以读取状态。
4. **添加 `window.advanceTime(ms)`。** 强烈优先使用确定性的步骤钩子，以便 Playwright 脚本可以可靠地推进帧；没有它，自动化测试可能会不稳定。
5. **初始化 progress.md。** 如果 `progress.md` 存在，首先读取它并确认原始用户提示记录在顶部（前缀为 `Original prompt:`）。还要记录前一个智能体留下的任何 TODO 和建议。如果缺失，创建它并在顶部写入 `Original prompt: <prompt>`，然后再追加更新。
6. **验证 Playwright 可用性。** 确保 `playwright` 可用（本地依赖或全局安装）。如果不确定，首先检查 `npx`。
7. **运行 Playwright 测试脚本。** 每次有意义的更改后必须运行 `$WEB_GAME_CLIENT`；不要发明新客户端，除非有需要。
8. **使用负载参考。** 基于 `$WEB_GAME_ACTIONS` 构建操作以避免猜测键。
9. **检查状态。** 每次突发后捕获截图和文本状态。
10. **检查截图。** 打开最新的截图，验证预期的视觉效果，修复任何问题，并重新运行脚本。重复直到正确。
11. **验证控件和状态（多步骤焦点）。** 彻底练习所有重要的交互。对于每个，思考它所暗示的完整多步骤序列（原因 → 中间状态 → 结果）并验证整个链路端到端工作。确认 `render_game_to_text` 反映屏幕上显示的相同状态。如果有任何偏差，修复并重新运行。
    重要交互示例：移动、跳跃、射击/攻击、交互/使用、选择/确认/取消菜单、暂停/恢复、重启，以及请求定义的任何特殊能力或谜题操作。多步骤示例：射击敌人应该减少其生命值；当生命值达到 0 时它应该消失并更新分数；收集钥匙应该解锁门并允许关卡进度。
12. **检查错误。** 审查控制台错误并在继续之前修复第一个新问题。
13. **在场景之间重置。** 验证不同功能时避免交叉测试状态。
14. **以小增量迭代。** 一次更改一个变量（帧、输入、时序、位置），然后重复步骤 7–13 直到稳定。

示例命令（需要操作）：

```
node "$WEB_GAME_CLIENT" --url http://localhost:5173 --actions-file "$WEB_GAME_ACTIONS" --click-selector "#start-btn" --iterations 3 --pause-ms 250
```

示例操作（内联 JSON）：

```json
{
  "steps": [
    { "buttons": ["left_mouse_button"], "frames": 2, "mouse_x": 120, "mouse_y": 80 },
    { "buttons": [], "frames": 6 },
    { "buttons": ["right"], "frames": 8 },
    { "buttons": ["space"], "frames": 4 }
  ]
}
```

## 测试检查清单

测试为请求添加的任何新功能以及您的逻辑更改可能影响的任何区域。识别问题，修复它们，并重新运行测试以确认它们已解决。

要测试的示例：
- 主要移动/交互输入（例如，移动、跳跃、射击、确认/选择）。
- 胜/负或成功/失败转换。
- 分数/生命值/资源更改。
- 边界条件（碰撞、墙壁、屏幕边缘）。
- 如果存在菜单/暂停/开始流程。
- 与请求相关的任何特殊操作（增益、连招、能力、谜题、计时器）。

## 要审查的测试工件

- Playwright 运行的最新截图。
- 最新的 `render_game_to_text` JSON 输出。
- 控制台错误日志（在继续之前修复第一个新错误）。

您必须实际打开并目视检查 Playwright 脚本运行后的最新截图，而不仅仅是生成它们。确保屏幕上应该可见的所有内容实际上都可见。超越开始屏幕并捕获涵盖所有新添加功能的游戏截图。将截图视为真相的来源；如果有任何内容缺失，则构建中也缺失。如果您怀疑无头/WebGL 捕获问题，请在有头模式下重新运行 Playwright 脚本并重新检查。修复并在紧凑循环中重新运行，直到截图和文本状态看起来正确。验证修复后，重新测试所有重要的交互和控件，确认它们有效，并确保您的更改没有引入回归。如果确实引入了回归，修复它们并在循环中重新运行所有内容，直到交互、文本状态和控件都按预期工作。彻底测试控件；损坏的游戏是不可接受的。

## 核心游戏指南

### 画布 + 布局
- 优先使用在窗口中居中的单个画布。

### 视觉效果
- 保持屏幕上的文本最少；在开始/菜单屏幕上显示控件，而不是在游戏过程中覆盖它们。
- 除非设计要求，否则避免过于黑暗的场景。使关键元素易于看到。
- 在画布本身上绘制背景，而不是依赖 CSS 背景。

### 文本状态输出（render_game_to_text）
暴露一个 `window.render_game_to_text` 函数，该函数返回一个简洁的 JSON 字符串，表示当前游戏状态。文本应包含足够的信息以在没有视觉效果的情况下玩游戏。

最小模式：

```js
function renderGameToText() {
  const payload = {
    mode: state.mode,
    player: { x: state.player.x, y: state.player.y, r: state.player.r },
    entities: state.entities.map((e) => ({ x: e.x, y: e.y, r: e.r })),
    score: state.score,
  };
  return JSON.stringify(payload);
}
window.render_game_to_text = renderGameToText;
```

保持负载简洁并偏向于屏幕上的交互元素。优先考虑当前可见的实体而不是完整的历史记录。

包含清晰的坐标系统说明（原点和轴方向），并编码所有玩家相关的状态：玩家位置/速度、活动障碍物/敌人、可收集物、计时器/冷却、分数以及做出正确决策所需的任何模式/状态标志。避免大型历史记录；仅包含当前相关和可见的内容。

### 时间步进钩子

提供一个确定性的时间步进钩子，以便 Playwright 客户端可以受控增量推进游戏。暴露 `window.advanceTime(ms)`（或转发到游戏更新循环的薄包装器）并在存在时让游戏循环使用它。

Playwright 测试脚本使用此钩子在自动化测试期间确定性地推进帧。

最小模式：

```js
window.advanceTime = (ms) => {
  const steps = Math.max(1, Math.round(ms / (1000 / 60)));
  for (let i = 0; i < steps; i++) update(1 / 60);
  render();
};
```

### 全屏切换
- 使用单个键（优先 `f`）切换全屏开/关。
- 允许 `Esc` 退出全屏。
- 当全屏切换时，调整画布/渲染大小，以便视觉效果和输入映射保持正确。

## 进度跟踪

创建一个 `progress.md` 文件（如果不存在），并在进行过程中追加 TODO、说明、陷阱和松散的结尾，以便另一个智能体可以无缝接手。

如果 `progress.md` 文件已经存在，首先读取它，包括顶部的原始用户提示（您可能正在继续另一个智能体的工作）。不要覆盖原始提示；保留它。

每次有意义的更改块（添加功能、发现错误、测试运行或做出决策）后更新 `progress.md`。

在您的工作结束时，在 `progress.md` 中为下一个智能体留下 TODO 和建议。

## Playwright 前置条件

- 如果项目已经有它，优先使用本地 `playwright` 依赖。
- 如果不确定 Playwright 是否可用，检查 `npx`：
  ```
  command -v npx >/dev/null 2>&1
  ```
- 如果 `npx` 缺失，安装 Node/npm 然后全局安装 Playwright：
  ```
  npm install -g @playwright/mcp@latest
  ```
- 不要切换到 `@playwright/test`，除非明确要求；坚持使用客户端脚本。

## 脚本

- `$WEB_GAME_CLIENT`（安装默认：`$CODEX_HOME/skills/develop-web-game/scripts/web_game_playwright_client.js`）— 基于 Playwright 的操作循环，具有虚拟时间步进、屏幕截图捕获和控制台错误缓冲。您必须通过 `--actions-file`、`--actions-json` 或 `--click` 传递操作突发。

## 参考

- `$WEB_GAME_ACTIONS`（安装默认：`$CODEX_HOME/skills/develop-web-game/references/action_payloads.json`）— 示例操作负载（键盘 + 鼠标，每帧捕获）。使用这些来构建您的突发。
