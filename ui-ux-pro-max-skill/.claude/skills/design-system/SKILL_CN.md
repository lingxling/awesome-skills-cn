---
name: ckm:design-system
description: 令牌架构、组件规范和幻灯片生成。三层令牌（原始→语义→组件）、CSS变量、间距/排版比例、组件规范、战略性幻灯片创建。用于设计令牌、系统设计、品牌合规演示文稿。
argument-hint: "[组件或令牌]"
license: MIT
metadata:
  author: claudekit
  version: "1.0.0"
---

# 设计系统

令牌架构、组件规范、系统设计、幻灯片生成。

## 何时使用

- 设计令牌创建
- 组件状态定义
- CSS变量系统
- 间距/排版比例
- 设计到代码的交接
- Tailwind主题配置
- **幻灯片/演示文稿生成**

## 令牌架构

加载：`references/token-architecture.md`

### 三层结构

```
原始（原始值）
       ↓
语义（用途别名）
       ↓
组件（组件特定）
```

**示例：**
```css
/* 原始 */
--color-blue-600: #2563EB;

/* 语义 */
--color-primary: var(--color-blue-600);

/* 组件 */
--button-bg: var(--color-primary);
```

## 快速开始

**生成令牌：**
```bash
node scripts/generate-tokens.cjs --config tokens.json -o tokens.css
```

**验证使用：**
```bash
node scripts/validate-tokens.cjs --dir src/
```

## 参考

| 主题 | 文件 |
|------|------|
| 令牌架构 | `references/token-architecture.md` |
| 原始令牌 | `references/primitive-tokens.md` |
| 语义令牌 | `references/semantic-tokens.md` |
| 组件令牌 | `references/component-tokens.md` |
| 组件规范 | `references/component-specs.md` |
| 状态和变体 | `references/states-and-variants.md` |
| Tailwind集成 | `references/tailwind-integration.md` |

## 组件规范模式

| 属性 | 默认 | 悬停 | 激活 | 禁用 |
|------|------|------|------|------|
| 背景 | primary | primary-dark | primary-darker | muted |
| 文本 | white | white | white | muted-fg |
| 边框 | none | none | none | muted-border |
| 阴影 | sm | md | none | none |

## 脚本

| 脚本 | 用途 |
|------|------|
| `generate-tokens.cjs` | 从JSON令牌配置生成CSS |
| `validate-tokens.cjs` | 检查代码中的硬编码值 |
| `search-slides.py` | BM25搜索 + 上下文推荐 |
| `slide-token-validator.py` | 验证幻灯片HTML的令牌合规性 |
| `fetch-background.py` | 从Pexels/Unsplash获取图像 |

## 模板

| 模板 | 用途 |
|------|------|
| `design-tokens-starter.json` | 具有三层结构的入门JSON |

## 集成

**与品牌：** 从品牌颜色/排版中提取原始值
**与ui-styling：** 组件令牌 → Tailwind配置

**技能依赖：** brand、ui-styling
**主要代理：** ui-ux-designer、frontend-developer

## 幻灯片系统

使用设计令牌 + Chart.js + 上下文决策系统的品牌合规演示文稿。

### 事实来源

| 文件 | 用途 |
|------|------|
| `docs/brand-guidelines.md` | 品牌标识、声音、颜色 |
| `assets/design-tokens.json` | 令牌定义（原始→语义→组件） |
| `assets/design-tokens.css` | CSS变量（在幻灯片中导入） |
| `assets/css/slide-animations.css` | CSS动画库 |

### 幻灯片搜索（BM25）

```bash
# 基本搜索（自动检测域）
python scripts/search-slides.py "investor pitch"

# 域特定搜索
python scripts/search-slides.py "problem agitation" -d copy
python scripts/search-slides.py "revenue growth" -d chart

# 上下文搜索（高级系统）
python scripts/search-slides.py "problem slide" --context --position 2 --total 9
python scripts/search-slides.py "cta" --context --position 9 --prev-emotion frustration
```

### 决策系统CSV

| 文件 | 用途 |
|------|------|
| `data/slide-strategies.csv` | 15种幻灯片结构 + 情感弧线 + 火花线节拍 |
| `data/slide-layouts.csv` | 25种布局 + 组件变体 + 动画 |
| `data/slide-layout-logic.csv` | 目标 → 布局 + break_pattern标志 |
| `data/slide-typography.csv` | 内容类型 → 排版比例 |
| `data/slide-color-logic.csv` | 情感 → 颜色处理 |
| `data/slide-backgrounds.csv` | 幻灯片类型 → 图像类别（Pexels/Unsplash） |
| `data/slide-copy.csv` | 25种文案公式（PAS、AIDA、FAB） |
| `data/slide-charts.csv` | 25种图表类型，带有Chart.js配置 |

### 上下文决策流程

```
1. 解析目标/上下文
        ↓
2. 搜索slide-strategies.csv → 获取策略 + 情感节拍
        ↓
3. 对于每张幻灯片：
   a. 查询slide-layout-logic.csv → 布局 + break_pattern
   b. 查询slide-typography.csv → 类型比例
   c. 查询slide-color-logic.csv → 颜色处理
   d. 查询slide-backgrounds.csv → 如有需要的图像
   e. 应用slide-animations.css中的动画类
        ↓
4. 生成带有设计令牌的HTML
        ↓
5. 使用slide-token-validator.py验证
```

### 模式打破（Duarte火花线）

高级幻灯片交替使用情感以提高参与度：
```
"现状"（挫折） ↔ "可能的未来"（希望）
```

系统在1/3和2/3位置计算模式打破。

### 幻灯片要求

**所有幻灯片必须：**
1. 导入`assets/design-tokens.css` - 单一事实来源
2. 使用CSS变量：`var(--color-primary)`、`var(--slide-bg)`等
3. 使用Chart.js创建图表（不是仅CSS的条形图）
4. 包含导航（键盘箭头、点击、进度条）
5. 内容居中对齐
6. 专注于说服/转化

### Chart.js集成

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<canvas id="revenueChart"></canvas>
<script>
new Chart(document.getElementById('revenueChart'), {
    type: 'line',
    data: {
        labels: ['9月', '10月', '11月', '12月'],
        datasets: [{
            data: [5, 12, 28, 45],
            borderColor: '#FF6B6B',  // 使用品牌珊瑚色
            backgroundColor: 'rgba(255, 107, 107, 0.1)',
            fill: true,
            tension: 0.4
        }]
    }
});
</script>
```

### 令牌合规性

```css
/* 正确 - 使用令牌 */
background: var(--slide-bg);
color: var(--color-primary);
font-family: var(--typography-font-heading);

/* 错误 - 硬编码 */
background: #0D0D0D;
color: #FF6B6B;
font-family: 'Space Grotesk';
```

### 参考实现

包含所有功能的工作示例：
```
assets/designs/slides/claudekit-pitch-251223.html
```

### 命令

```bash
/slides:create "10-slide investor pitch for ClaudeKit Marketing"
```

## 最佳实践

1. 永远不要在组件中使用原始十六进制值 - 始终引用令牌
2. 语义层启用主题切换（明/暗）
3. 组件令牌启用每个组件的自定义
4. 使用HSL格式进行不透明度控制
5. 记录每个令牌的用途
6. **幻灯片必须导入design-tokens.css并仅使用var()**