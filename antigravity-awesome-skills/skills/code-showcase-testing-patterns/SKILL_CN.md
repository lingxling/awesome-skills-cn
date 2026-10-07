---
name: code-showcase-testing-patterns
description: Jest 测试模式、工厂函数、模拟策略和 TDD 工作流。在编写单元测试、创建测试工厂或遵循 TDD 红-绿-重构循环时使用。
risk: critical
source: https://github.com/ChrisWiles/claude-code-showcase/tree/main/.claude/skills/testing-patterns
source_repo: ChrisWiles/claude-code-showcase
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ChrisWiles/claude-code-showcase/blob/main/LICENSE
---

# 测试模式和工具
## 何时使用

当您需要 Jest 测试模式、工厂函数、模拟策略和 TDD 工作流时，使用此技能。在编写单元测试、创建测试工厂或遵循 TDD 红-绿-重构循环时使用。


## 测试哲学

**测试驱动开发（TDD）：**
- 先写失败的测试
- 实现最小代码以通过
- 绿色后重构
- 永远不要在没有失败测试的情况下编写生产代码

**行为驱动测试：**
- 测试行为，而不是实现
- 专注于公共 API 和业务需求
- 避免测试实现细节
- 使用描述性测试名称来描述行为

**工厂模式：**
- 创建 `getMockX(overrides?: Partial<X>)` 函数
- 提供合理的默认值
- 允许覆盖特定属性
- 保持测试 DRY 和可维护

## 测试工具

### 自定义渲染函数

创建一个自定义渲染函数，使用必需的提供程序包装组件：

```typescript
// src/utils/testUtils.tsx
import { render } from '@testing-library/react-native';
import { ThemeProvider } from './theme';

export const renderWithTheme = (ui: React.ReactElement) => {
  return render(
    <ThemeProvider>{ui}</ThemeProvider>
  );
};
```

**用法：**
```typescript
import { renderWithTheme } from 'utils/testUtils';
import { screen } from '@testing-library/react-native';

it('should render component', () => {
  renderWithTheme(<MyComponent />);
  expect(screen.getByText('Hello')).toBeTruthy();
});
```

## 工厂模式

### 组件属性工厂

```typescript
import { ComponentProps } from 'react';

const getMockMyComponentProps = (
  overrides?: Partial<ComponentProps<typeof MyComponent>>
) => {
  return {
    title: 'Default Title',
    count: 0,
    onPress: jest.fn(),
    isLoading: false,
    ...overrides,
  };
};

// 在测试中使用
it('should render with custom title', () => {
  const props = getMockMyComponentProps({ title: 'Custom Title' });
  renderWithTheme(<MyComponent {...props} />);
  expect(screen.getByText('Custom Title')).toBeTruthy();
});
```

### 数据工厂

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

const getMockUser = (overrides?: Partial<User>): User => {
  return {
    id: '123',
    name: 'John Doe',
    email: 'john@example.com',
    role: 'user',
    ...overrides,
  };
};

// 用法
it('should display admin badge for admin users', () => {
  const user = getMockUser({ role: 'admin' });
  renderWithTheme(<UserCard user={user} />);
  expect(screen.getByText('Admin')).toBeTruthy();
});
```

## 模拟模式

### 模拟模块

```typescript
// 模拟整个模块
jest.mock('utils/analytics');

// 使用工厂函数模拟
jest.mock('utils/analytics', () => ({
  Analytics: {
    logEvent: jest.fn(),
  },
}));

// 在测试中访问模拟
const mockLogEvent = jest.requireMock('utils/analytics').Analytics.logEvent;
```

### 模拟 GraphQL 钩子

```typescript
jest.mock('./GetItems.generated', () => ({
  useGetItemsQuery: jest.fn(),
}));

const mockUseGetItemsQuery = jest.requireMock(
  './GetItems.generated'
).useGetItemsQuery as jest.Mock;

// 在测试中
mockUseGetItemsQuery.mockReturnValue({
  data: { items: [] },
  loading: false,
  error: undefined,
});
```

## 测试结构

```typescript
describe('ComponentName', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('should render component with default props', () => {});
    it('should render loading state when loading', () => {});
  });

  describe('User interactions', () => {
    it('should call onPress when button is clicked', async () => {});
  });

  describe('Edge cases', () => {
    it('should handle empty data gracefully', () => {});
  });
});
```

## 查询模式

```typescript
// 元素必须存在
expect(screen.getByText('Hello')).toBeTruthy();

// 元素不应存在
expect(screen.queryByText('Goodbye')).toBeNull();

// 元素异步显示
await waitFor(() => {
  expect(screen.findByText('Loaded')).toBeTruthy();
});
```

## 用户交互模式

```typescript
import { fireEvent, screen } from '@testing-library/react-native';

it('should submit form on button click', async () => {
  const onSubmit = jest.fn();
  renderWithTheme(<LoginForm onSubmit={onSubmit} />);

  fireEvent.changeText(screen.getByLabelText('Email'), 'user@example.com');
  fireEvent.changeText(screen.getByLabelText('Password'), 'password123');
  fireEvent.press(screen.getByTestId('login-button'));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalled();
  });
});
```

## 应避免的反面模式

### 测试模拟行为而不是真实行为

```typescript
// 坏 - 测试模拟
expect(mockFetchData).toHaveBeenCalled();

// 好 - 测试实际行为
expect(screen.getByText('John Doe')).toBeTruthy();
```

### 不使用工厂

```typescript
// 坏 - 重复、不一致的测试数据
it('test 1', () => {
  const user = { id: '1', name: 'John', email: 'john@test.com', role: 'user' };
});
it('test 2', () => {
  const user = { id: '2', name: 'Jane', email: 'jane@test.com' }; // 缺少 role!
});

// 好 - 可重用的工厂
const user = getMockUser({ name: 'Custom Name' });
```

## 最佳实践

1. **始终为属性和数据使用工厂函数**
2. **测试行为，而不是实现**
3. **使用描述性测试名称**
4. **用 describe 块进行组织**
5. **在测试之间清除模拟**
6. **保持测试集中** - 每个测试一个行为

## 运行测试

```bash
# 运行所有测试
npm test

# 运行覆盖率
npm run test:coverage

# 运行特定文件
npm test ComponentName.test.tsx
```

## 与其他技能的集成

- **react-ui-patterns**：测试所有 UI 状态（加载、错误、空、成功）
- **systematic-debugging**：在修复之前编写重现 bug 的测试

## 限制

- 仅当任务清晰地匹配其上游源和本地项目上下文时，才使用此技能。
- 在应用更改之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例作为环境特定测试、安全审查或用户对破坏性或成本高昂操作的批准的替代品。
