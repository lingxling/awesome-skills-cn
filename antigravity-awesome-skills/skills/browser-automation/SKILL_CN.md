---
name: browser-automation
description: 使用观察的 UI 状态、语义定位器、界限等待、隔离的测试数据和明确的结果验证来构建可靠的浏览器检查。
risk: critical
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 浏览器自动化

使用用户已选择或在项目中安装的浏览器工具。Playwright、Puppeteer 和 Selenium 有不同的集成；根据实际需求而非不受支持的成功率声明进行选择。由 AAS 维护者于 2026-09-05 修改：删除了未验证的比较和绕过默认值，澄清了等待和证据限制。

将你控制的应用程序的测试与与现有已验证浏览器的交互分离。不要用新的未验证的会话替换后者，也不要提取凭据来使自动化测试工作。

## 详细指南

执行此技能之前读取[详细指南](references/detailed-guide.md)。它保留完整的程序和参考材料。将其安全、先决条件和验证要求视为强制性。对于专注的工作，加载相关部分；对于端到端工作，完全阅读指南。

## Playwright 测试示例
"""
import { test, expect } from '@playwright/test';

// 每个测试在隔离的浏览器上下文中运行
test('user can add item to cart', async ({ page }) => {
  // 新上下文 - 没有其他测试的 cookie、存储
  await page.goto('/products');
  await page.getByRole('button', { name: 'Add to Cart' }).click();
  await expect(page.getByTestId('cart-count')).toHaveText('1');
});

test('user can remove item from cart', async ({ page }) => {
  // 完全隔离 - 购物车为空
  await page.goto('/cart');
  await expect(page.getByText('Your cart is empty')).toBeVisible();
});
"""

## 好的示例（面向用户）
"""
// 按角色 - 最佳选择
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('link', { name: 'Sign up' }).click();
await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
await page.getByRole('textbox', { name: 'Search' }).fill('query');

// 按文本内容
await expect(page.getByText('Welcome back')).toBeVisible();
await page.getByText(/Order #\d+/).click();  // 支持正则表达式

// 按标签（表单）
await page.getByLabel('Email address').fill('user@example.com');
await page.getByLabel('Password').fill('secret');

// 按占位符
await page.getByPlaceholder('Search...').fill('query');

// 按测试 ID（当没有面向用户的选项时）
await page.getByTestId('submit-button').click();
"""

## 坏的示例（脆弱）
"""
// 不要 - CSS 选择器绑定到结构
await page.locator('.btn-primary.submit-form').click();
await page.locator('#header > div > button:nth-child(2)').click();

// 不要 - XPath 绑定到结构
await page.locator('//div[@class="form"]/button[1]').click();

// 不要 - 自动生成的选择器
await page.locator('[data-v-12345]').click();
"""

## 何时使用

使用来验证真实浏览器工作流、诊断 UI 计时故障或收集明确授权的页面数据。在选择定位器或操作前检查当前页面和可用工具 API。

## 工作示例和先决条件

输入：从本地 web 应用程序导出经过审查的 JSON 文件。运行应用程序、可用目标浏览器和合成表单值。观察导出控制、在点击前注册下载事件、检查下载的 JSON 并确认编辑输入会使旧预览无效。预期结果：一个包含已审查值的文件，没有隐藏的项目数据或网络提交。

当任务包括可用性时，使用明确的桌面/移动视口并检查键盘/焦点行为。锁定的桌面会使交互验证待处理；单元测试和无头探针是单独的证据。

## 限制

- 自动等待检查可操作性，而不是业务正确性或成功的后端写入。
- 屏幕截图、HTML、迹线和身份验证状态文件可能包含私人信息；仅捕获授权的作用域。
- 重试读取可能是安全的；重试检查、删除或发送消息可能会复制副作用。在重复前验证状态。
- 资源阻塞和模拟响应改变环境，无法建立未修改的生产行为。
- 示例需要项目的导入、运行器和设备路由；此技能未安装浏览器、服务或帐户。
