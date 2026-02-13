---
name: ui-ux-pro-max
description: "UI/UX设计智能。50种风格、21个调色板、50种字体配对、20种图表、9个技术栈（React、Next.js、Vue、Svelte、SwiftUI、React Native、Flutter、Tailwind、shadcn/ui）。操作：规划、构建、创建、设计、实现、审查、修复、改进、优化、增强、重构、检查UI/UX代码。项目：网站、着陆页、仪表板、管理面板、电子商务、SaaS、作品集、博客、移动应用、.html、.tsx、.vue、.svelte。元素：按钮、模态、导航栏、侧边栏、卡片、表格、表单、图表。风格：玻璃拟态、粘土拟态、极简主义、粗野主义、新拟态、便当网格、暗色模式、响应式、拟物化、扁平设计。主题：调色板、可访问性、动画、布局、排版、字体配对、间距、悬停、阴影、渐变。集成：shadcn/ui MCP用于组件搜索和示例。"
---

# UI/UX Pro Max - 设计智能

Web和移动应用程序的综合设计指南。包含50+种风格、97个调色板、57种字体配对、99条UX指南和9个技术栈的25种图表类型。具有基于优先级建议的可搜索数据库。

## 何时应用

在以下情况下参考这些指南：
- 设计新的UI组件或页面
- 选择调色板和排版
- 审查代码的UX问题
- 构建着陆页或仪表板
- 实现可访问性要求

## 按优先级分类的规则

| 优先级 | 类别 | 影响 | 领域 |
|----------|----------|--------|--------|
| 1 | 可访问性 | 关键 | `ux` |
| 2 | 触摸和交互 | 关键 | `ux` |
| 3 | 性能 | 高 | `ux` |
| 4 | 布局和响应式 | 高 | `ux` |
| 5 | 排版和颜色 | 中等 | `typography`, `color` |
| 6 | 动画 | 中等 | `ux` |
| 7 | 风格选择 | 中等 | `style`, `product` |
| 8 | 图表和数据 | 低 | `chart` |

## 快速参考

### 1. 可访问性（关键）

- `color-contrast` - 普通文本最小4.5:1对比度
- `focus-states` - 交互元素上可见的焦点环
- `alt-text` - 有意义图像的描述性alt文本
- `aria-labels` - 仅图标按钮的aria-label
- `keyboard-nav` - Tab顺序与视觉顺序匹配
- `form-labels` - 使用带有for属性的label

### 2. 触摸和交互（关键）

- `touch-target-size` - 最小44x44px触摸目标
- `hover-vs-tap` - 对主要交互使用点击/轻触
- `loading-buttons` - 在异步操作期间禁用按钮
- `error-feedback` - 在问题附近提供清晰的错误消息
- `cursor-pointer` - 为可点击元素添加cursor-pointer

### 3. 性能（高）

- `image-optimization` - 使用WebP、srcset、懒加载
- `reduced-motion` - 检查prefers-reduced-motion
- `content-jumping` - 为异步内容预留空间

### 4. 布局和响应式（高）

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - 移动端最小16px正文文本
- `horizontal-scroll` - 确保内容适合视口宽度
- `z-index-management` - 定义z-index比例（10、20、30、50）

### 5. 排版和颜色（中等）

- `line-height` - 正文文本使用1.5-1.75
- `line-length` - 限制每行65-75个字符
- `font-pairing` - 匹配标题/正文字体个性

### 6. 动画（中等）

- `duration-timing` - 微交互使用150-300ms
- `transform-performance` - 使用transform/opacity，而非width/height
- `loading-states` - 骨架屏或加载器

### 7. 风格选择（中等）

- `style-match` - 将风格与产品类型匹配
- `consistency` - 在所有页面使用相同风格
- `no-emoji-icons` - 使用SVG图标，而非表情符号

### 8. 图表和数据（低）

- `chart-type` - 将图表类型与数据类型匹配
- `color-guidance` - 使用可访问的调色板
- `data-table` - 为可访问性提供表格替代方案

## 如何使用

使用下面的CLI工具搜索特定领域。

---

## 先决条件

检查是否安装了Python：

```bash
python3 --version || python --version
```

如果未安装Python，根据用户的操作系统安装：

**macOS：**
```bash
brew install python3
```

**Ubuntu/Debian：**
```bash
sudo apt update && sudo apt install python3
```

**Windows：**
```powershell
winget install Python.Python.3.12
```

---

## 如何使用此技能

当用户请求UI/UX工作（设计、构建、创建、实现、审查、修复、改进）时，遵循此工作流程：

### 步骤1：分析用户需求

从用户请求中提取关键信息：
- **产品类型**：SaaS、电子商务、作品集、仪表板、着陆页等
- **风格关键词**：极简、俏皮、专业、优雅、暗色模式等
- **行业**：医疗保健、金融科技、游戏、教育等
- **技术栈**：React、Vue、Next.js或默认为`html-tailwind`

### 步骤2：生成设计系统（必需）

**始终以`--design-system`开始**以获取带有推理的综合建议：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

此命令：
1. 并行搜索5个领域（产品、风格、颜色、着陆、排版）
2. 应用`ui-reasoning.csv`中的推理规则以选择最佳匹配
3. 返回完整的设计系统：模式、风格、颜色、排版、效果
4. 包括要避免的反模式

**示例：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### 步骤2b：持久化设计系统（主+覆盖模式）

为了将设计系统保存以**跨会话分层检索**，添加`--persist`：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

这将创建：
- `design-system/MASTER.md` — 包含所有设计规则的全局单一事实来源
- `design-system/pages/` — 页面特定覆盖的文件夹

**使用页面特定覆盖：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

这也创建：
- `design-system/pages/dashboard.md` — 与主文件的页面特定偏差

**分层检索如何工作：**
1. 当构建特定页面（例如，"Checkout"）时，首先检查`design-system/pages/checkout.md`
2. 如果页面文件存在，其规则**覆盖**主文件
3. 如果不存在，仅使用`design-system/MASTER.md`

**上下文感知检索提示：**
```
我正在构建[页面名称]页面。请阅读design-system/MASTER.md。
还要检查design-system/pages/[page-name].md是否存在。
如果页面文件存在，优先考虑其规则。
如果不存在，仅使用主规则。
现在，生成代码...
```

### 步骤3：补充详细搜索（根据需要）

获得设计系统后，使用领域搜索获取其他详细信息：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**何时使用详细搜索：**

| 需求 | 领域 | 示例 |
|------|--------|---------|
| 更多风格选项 | `style` | `--domain style "glassmorphism dark"` |
| 图表推荐 | `chart` | `--domain chart "real-time dashboard"` |
| UX最佳实践 | `ux` | `--domain ux "animation accessibility"` |
| 替代字体 | `typography` | `--domain typography "elegant luxury"` |
| 着陆结构 | `landing` | `--domain landing "hero social-proof"` |

### 步骤4：技术栈指南（默认：html-tailwind）

获取实现特定的最佳实践。如果用户未指定技术栈，**默认为`html-tailwind`**。

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

可用技术栈：`html-tailwind`、`react`、`nextjs`、`vue`、`svelte`、`swiftui`、`react-native`、`flutter`、`shadcn`、`jetpack-compose`

---

## 搜索参考

### 可用领域

| 领域 | 用于 | 示例关键词 |
|--------|---------|------------------|
| `product` | 产品类型推荐 | SaaS、电子商务、作品集、医疗保健、美容、服务 |
| `style` | UI风格、颜色、效果 | 玻璃拟态、极简主义、暗色模式、粗野主义 |
| `typography` | 字体配对、Google字体 | 优雅、俏皮、专业、现代 |
| `color` | 按产品类型的调色板 | saas、ecommerce、healthcare、beauty、fintech、service |
| `landing` | 页面结构、CTA策略 | hero、hero-centric、testimonial、pricing、social-proof |
| `chart` | 图表类型、库推荐 | trend、comparison、timeline、funnel、pie |
| `ux` | 最佳实践、反模式 | animation、accessibility、z-index、loading |
| `react` | React/Next.js性能 | waterfall、bundle、suspense、memo、rerender、cache |
| `web` | Web界面指南 | aria、focus、keyboard、semantic、virtualize |
| `prompt` | AI提示、CSS关键词 | （风格名称） |

### 可用技术栈

| 技术栈 | 重点 |
|-------|-------|
| `html-tailwind` | Tailwind实用程序、响应式、a11y（默认） |
| `react` | 状态、hooks、性能、模式 |
| `nextjs` | SSR、路由、图像、API路由 |
| `vue` | 组合API、Pinia、Vue Router |
| `svelte` | Runes、stores、SvelteKit |
| `swiftui` | 视图、状态、导航、动画 |
| `react-native` | 组件、导航、列表 |
| `flutter` | 小部件、状态、布局、主题 |
| `shadcn` | shadcn/ui组件、主题、表单、模式 |
| `jetpack-compose` | Composables、修饰符、状态提升、重组 |

---

## 示例工作流程

**用户请求：** "Làm landing page cho dịch vụ chăm sóc da chuyên nghiệp"

### 步骤1：分析需求
- 产品类型：美容/水疗服务
- 风格关键词：优雅、专业、柔和
- 行业：美容/健康
- 技术栈：html-tailwind（默认）

### 步骤2：生成设计系统（必需）

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**输出：** 包含模式、风格、颜色、排版、效果和反模式的完整设计系统。

### 步骤3：补充详细搜索（根据需要）

```bash
# 获取动画和可访问性的UX指南
python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# 如果需要，获取替代排版选项
python3 skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### 步骤4：技术栈指南

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**然后：** 综合设计系统 + 详细搜索并实现设计。

---

## 输出格式

`--design-system`标志支持两种输出格式：

```bash
# ASCII框（默认）- 最适合终端显示
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - 最适合文档
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## 获得更好结果的技巧

1. **使用具体的关键词** - "healthcare SaaS dashboard" > "app"
2. **多次搜索** - 不同的关键词揭示不同的见解
3. **组合领域** - 风格 + 排版 + 颜色 = 完整的设计系统
4. **始终检查UX** - 搜索"animation"、"z-index"、"accessibility"以获取常见问题
5. **使用技术栈标志** - 获取实现特定的最佳实践
6. **迭代** - 如果第一次搜索不匹配，尝试不同的关键词

---

## 专业UI的通用规则

这些是经常被忽视的问题，使UI看起来不专业：

### 图标和视觉元素

| 规则 | 做 | 不要 |
|------|----|----- |
| **无表情符号图标** | 使用SVG图标（Heroicons、Lucide、Simple Icons） | 使用🎨 🚀 ⚙️等表情符号作为UI图标 |
| **稳定的悬停状态** | 在悬停时使用颜色/不透明度过渡 | 使用改变布局的缩放变换 |
| **正确的品牌徽标** | 从Simple Icons研究官方SVG | 猜测或使用错误的徽标路径 |
| **一致的图标大小** | 使用固定的viewBox（24x24）和w-6 h-6 | 随机混合不同的图标大小 |

### 交互和光标

| 规则 | 做 | 不要 |
|------|----|----- |
| **光标指针** | 为所有可点击/可悬停的卡片添加`cursor-pointer` | 在交互元素上保留默认光标 |
| **悬停反馈** | 提供视觉反馈（颜色、阴影、边框） | 没有指示元素是交互式的 |
| **平滑过渡** | 使用`transition-colors duration-200` | 瞬间状态变化或太慢（>500ms） |

### 浅色/暗色模式对比度

| 规则 | 做 | 不要 |
|------|----|----- |
| **玻璃卡片浅色模式** | 使用`bg-white/80`或更高不透明度 | 使用`bg-white/10`（太透明） |
| **浅色模式文本对比度** | 对文本使用`#0F172A`（slate-900） | 对正文文本使用`#94A3B8`（slate-400） |
| **浅色模式静音文本** | 最小使用`#475569`（slate-600） | 使用gray-400或更浅 |
| **边框可见性** | 在浅色模式中使用`border-gray-200` | 使用`border-white/10`（不可见） |

### 布局和间距

| 规则 | 做 | 不要 |
|------|----|----- |
| **浮动导航栏** | 添加`top-4 left-4 right-4`间距 | 将导航栏粘附到`top-0 left-0 right-0` |
| **内容填充** | 考虑固定导航栏高度 | 让内容隐藏在固定元素后面 |
| **一致的最大宽度** | 使用相同的`max-w-6xl`或`max-w-7xl` | 混合不同的容器宽度 |

---

## 交付前检查清单

在交付UI代码之前，验证这些项目：

### 视觉质量
- [ ] 没有使用表情符号作为图标（改用SVG）
- [ ] 所有图标来自一致的图标集（Heroicons/Lucide）
- [ ] 品牌徽标正确（从Simple Icons验证）
- [ ] 悬停状态不会导致布局偏移
- [ ] 直接使用主题颜色（bg-primary）而非var()包装器

### 交互
- [ ] 所有可点击元素都有`cursor-pointer`
- [ ] 悬停状态提供清晰的视觉反馈
- [ ] 过渡平滑（150-300ms）
- [ ] 键盘导航可见焦点状态

### 浅色/暗色模式
- [ ] 浅色模式文本具有足够的对比度（最小4.5:1）
- [ ] 玻璃/透明元素在浅色模式中可见
- [ ] 边框在两种模式下都可见
- [ ] 交付前测试两种模式

### 布局
- [ ] 浮动元素与边缘有适当的间距
- [ ] 没有内容隐藏在固定导航栏后面
- [ ] 在375px、768px、1024px、1440px处响应式
- [ ] 移动端没有水平滚动

### 可访问性
- [ ] 所有图像都有alt文本
- [ ] 表单输入有标签
- [ ] 颜色不是唯一的指示器
- [ ] 尊重`prefers-reduced-motion`
