---
name: ckm:ui-styling
description: 使用shadcn/ui组件（基于Radix UI + Tailwind）、Tailwind CSS实用优先样式和基于画布的视觉设计创建美观、可访问的用户界面。当构建用户界面、实现设计系统、创建响应式布局、添加可访问组件（对话框、下拉菜单、表单、表格）、自定义主题和颜色、实现深色模式、生成视觉设计和海报，或在应用程序中建立一致的样式模式时使用。
argument-hint: "[组件或布局]"
license: MIT
metadata:
  author: claudekit
  version: "1.0.0"
---

# UI样式技能

全面的技能，用于创建美观、可访问的用户界面，结合shadcn/ui组件、Tailwind CSS实用样式和基于画布的视觉设计系统。

## 参考

- shadcn/ui: https://ui.shadcn.com/llms.txt
- Tailwind CSS: https://tailwindcss.com/docs

## 何时使用此技能

当：
- 使用基于React的框架（Next.js、Vite、Remix、Astro）构建UI
- 实现可访问组件（对话框、表单、表格、导航）
- 使用实用优先CSS方法进行样式设计
- 创建响应式、移动优先布局
- 实现深色模式和主题自定义
- 使用一致的令牌构建设计系统
- 生成视觉设计、海报或品牌材料
- 通过即时视觉反馈进行快速原型设计
- 添加复杂的UI模式（数据表、图表、命令面板）

## 核心堆栈

### 组件层：shadcn/ui
- 通过Radix UI原语预构建的可访问组件
- 复制粘贴分发模型（组件存在于您的代码库中）
- 优先使用TypeScript，具有完整的类型安全
- 用于复杂UI的可组合原语
- 基于CLI的安装和管理

### 样式层：Tailwind CSS
- 实用优先CSS框架
- 构建时处理，零运行时开销
- 移动优先响应式设计
- 一致的设计令牌（颜色、间距、排版）
- 自动消除死代码

### 视觉设计层：画布
- 博物馆级视觉组合
- 哲学驱动的设计方法
- 复杂的视觉传达
- 最小文本，最大视觉冲击力
- 系统模式和精致美学

## 快速开始

### 组件 + 样式设置

**使用Tailwind安装shadcn/ui：**
```bash
npx shadcn@latest init
```

CLI提示框架、TypeScript、路径和主题偏好。这会配置shadcn/ui和Tailwind CSS。

**添加组件：**
```bash
npx shadcn@latest add button card dialog form
```

**使用实用样式的组件：**
```tsx
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export function Dashboard() {
  return (
    <div className="container mx-auto p-6 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <Card className="hover:shadow-lg transition-shadow">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Analytics</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">View your metrics</p>
          <Button variant="default" className="w-full">
            View Details
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
```

### 替代方案：仅Tailwind设置

**Vite项目：**
```bash
npm install -D tailwindcss @tailwindcss/vite
```

```javascript
// vite.config.ts
import tailwindcss from '@tailwindcss/vite'
export default { plugins: [tailwindcss()] }
```

```css
/* src/index.css */
@import "tailwindcss";
```

## 组件库指南

**全面的组件目录，包含使用模式、安装和组合示例。**

参见：`references/shadcn-components.md`

涵盖：
- 表单和输入组件（Button、Input、Select、Checkbox、Date Picker、表单验证）
- 布局和导航（Card、Tabs、Accordion、Navigation Menu）
- 覆盖层和对话框（Dialog、Drawer、Popover、Toast、Command）
- 反馈和状态（Alert、Progress、Skeleton）
- 显示组件（Table、Data Table、Avatar、Badge）

## 主题和自定义

**主题配置、CSS变量、深色模式实现和组件自定义。**

参见：`references/shadcn-theming.md`

涵盖：
- 使用next-themes设置深色模式
- CSS变量系统
- 颜色自定义和调色板
- 组件变体自定义
- 主题切换实现

## 可访问性模式

**ARIA模式、键盘导航、屏幕阅读器支持和可访问组件使用。**

参见：`references/shadcn-accessibility.md`

涵盖：
- Radix UI可访问性功能
- 键盘导航模式
- 焦点管理
- 屏幕阅读器公告
- 表单验证可访问性

## Tailwind实用程序

**用于布局、间距、排版、颜色、边框和阴影的核心实用类。**

参见：`references/tailwind-utilities.md`

涵盖：
- 布局实用程序（Flexbox、Grid、定位）
- 间距系统（内边距、外边距、间隙）
- 排版（字体大小、权重、对齐、行高）
- 颜色和背景
- 边框和阴影
- 用于自定义样式的任意值

## 响应式设计

**移动优先断点、响应式实用程序和自适应布局。**

参见：`references/tailwind-responsive.md`

涵盖：
- 移动优先方法
- 断点系统（sm、md、lg、xl、2xl）
- 响应式实用程序模式
- 容器查询
- 最大宽度查询
- 自定义断点

## Tailwind自定义

**配置文件结构、自定义实用程序、插件和主题扩展。**

参见：`references/tailwind-customization.md`

涵盖：
- @theme指令用于自定义令牌
- 自定义颜色和字体
- 间距和断点扩展
- 自定义实用程序创建
- 自定义变体
- 层组织（@layer base、components、utilities）
- 组件提取的Apply指令

## 视觉设计系统

**基于画布的设计理念、视觉传达原则和复杂组合。**

参见：`references/canvas-design-system.md`

涵盖：
- 设计理念方法
- 视觉传达而非文本
- 系统模式和组合
- 颜色、形式和空间设计
- 最小文本集成
- 博物馆级执行
- 多页设计系统

## 实用脚本

**用于组件安装和配置生成的Python自动化。**

### shadcn_add.py
添加带有依赖处理的shadcn/ui组件：
```bash
python scripts/shadcn_add.py button card dialog
```

### tailwind_config_gen.py
生成带有自定义主题的tailwind.config.js：
```bash
python scripts/tailwind_config_gen.py --colors brand:blue --fonts display:Inter
```

## 最佳实践

1. **组件组合**：从简单、可组合的原语构建复杂UI
2. **实用优先样式**：直接使用Tailwind类；仅为真正的重复提取组件
3. **移动优先响应式**：从移动样式开始，分层响应式变体
4. **可访问性优先**：利用Radix UI原语，添加焦点状态，使用语义HTML
5. **设计令牌**：使用一致的间距比例、调色板、排版系统
6. **深色模式一致性**：对所有主题元素应用深色变体
7. **性能**：利用自动CSS清除，避免动态类名
8. **TypeScript**：使用完整的类型安全以获得更好的开发体验
9. **视觉层次结构**：让组合引导注意力，有意使用间距和颜色
10. **专家工艺**：每个细节都很重要 - 将UI视为一种工艺

## 参考导航

**组件库**
- `references/shadcn-components.md` - 完整组件目录
- `references/shadcn-theming.md` - 主题和自定义
- `references/shadcn-accessibility.md` - 可访问性模式

**样式系统**
- `references/tailwind-utilities.md` - 核心实用类
- `references/tailwind-responsive.md` - 响应式设计
- `references/tailwind-customization.md` - 配置和扩展

**视觉设计**
- `references/canvas-design-system.md` - 设计理念和画布工作流程

**自动化**
- `scripts/shadcn_add.py` - 组件安装
- `scripts/tailwind_config_gen.py` - 配置生成

## 常见模式

**带验证的表单：**
```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
})

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(schema),
    defaultValues: { email: "", password: "" }
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-6">
        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl>
              <Input type="email" {...field} />
            </FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit" className="w-full">Sign In</Button>
      </form>
    </Form>
  )
}
```

**带有深色模式的响应式布局：**
```tsx
<div className="min-h-screen bg-white dark:bg-gray-900">
  <div className="container mx-auto px-4 py-8">
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardContent className="p-6">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
            Content
          </h3>
        </CardContent>
      </Card>
    </div>
  </div>
</div>
```

## 资源

- shadcn/ui文档：https://ui.shadcn.com
- Tailwind CSS文档：https://tailwindcss.com
- Radix UI：https://radix-ui.com
- Tailwind UI：https://tailwindui.com
- Headless UI：https://headlessui.com
- v0（AI UI生成器）：https://v0.dev