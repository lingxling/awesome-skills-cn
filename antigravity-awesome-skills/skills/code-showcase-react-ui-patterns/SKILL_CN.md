---
name: code-showcase-react-ui-patterns
description: 用于加载状态、错误处理和数据获取的现代 React UI 模式。在构建 UI 组件、处理异步数据或管理 UI 状态时使用。
risk: critical
source: https://github.com/ChrisWiles/claude-code-showcase/tree/main/.claude/skills/react-ui-patterns
source_repo: ChrisWiles/claude-code-showcase
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ChrisWiles/claude-code-showcase/blob/main/LICENSE
---

# React UI 模式
## 何时使用

当您需要用于加载状态、错误处理和数据获取的现代 React UI 模式时，使用此技能。在构建 UI 组件、处理异步数据或管理 UI 状态时使用。


## 核心原则

1. **永远不要显示陈旧的 UI** - 仅在实际加载时显示加载微调器
2. **始终显示错误** - 用户必须知道何时出现问题
3. **乐观更新** - 让 UI 感觉即时
4. **渐进式展示** - 在内容可用时展示它
5. **优雅降级** - 部分数据比没有数据更好

## 加载状态模式

### 黄金法则

**仅当没有要显示的数据时，才显示加载指示器。**

```typescript
// 正确 - 仅在没有数据时显示加载
const { data, loading, error } = useGetItemsQuery();

if (error) return <ErrorState error={error} onRetry={refetch} />;
if (loading && !data) return <LoadingState />;
if (!data?.items.length) return <EmptyState />;

return <ItemList items={data.items} />;
```

```typescript
// 错误 - 即使我们有缓存数据也显示微调器
if (loading) return <LoadingState />; // 重新获取时闪烁!
```

### 加载状态决策树

```
是否有错误？
  → 是：显示错误状态及重试选项
  → 否：继续

是否正在加载且没有数据？
  → 是：显示加载指示器（微调器/骨架屏）
  → 否：继续

是否有数据？
  → 是，有项目：显示数据
  → 是，但为空：显示空状态
  → 否：显示加载（回退）
```

### 骨架屏 vs 微调器

| 使用骨架屏时 | 使用微调器时 |
|-------------------|------------------|
| 已知内容形状 | 未知内容形状 |
| 列表/卡片布局 | 模态框操作 |
| 初始页面加载 | 按钮提交 |
| 内容占位符 | 内联操作 |

## 错误处理模式

### 错误处理层级

```
1. 内联错误（字段级） → 表单验证错误
2. Toast 通知 → 可恢复的错误，用户可以重试
3. 错误横幅 → 页面级错误，数据仍然部分可用
4. 完整错误屏幕 → 不可恢复，需要用户操作
```

### 始终显示错误

**关键：永远不要静默吞掉错误。**

```typescript
// 正确 - 错误始终显示给用户
const [createItem, { loading }] = useCreateItemMutation({
  onCompleted: () => {
    toast.success({ title: 'Item created' });
  },
  onError: (error) => {
    console.error('createItem failed:', error);
    toast.error({ title: 'Failed to create item' });
  },
});

// 错误 - 错误被静默捕获，用户不知道
const [createItem] = useCreateItemMutation({
  onError: (error) => {
    console.error(error); // 用户看不到任何东西！
  },
});
```

### 错误状态组件模式

```typescript
interface ErrorStateProps {
  error: Error;
  onRetry?: () => void;
  title?: string;
}

const ErrorState = ({ error, onRetry, title }: ErrorStateProps) => (
  <div className="error-state">
    <Icon name="exclamation-circle" />
    <h3>{title ?? 'Something went wrong'}</h3>
    <p>{error.message}</p>
    {onRetry && (
      <Button onClick={onRetry}>Try Again</Button>
    )}
  </div>
);
```

## 按钮状态模式

### 按钮加载状态

```tsx
<Button
  onClick={handleSubmit}
  isLoading={isSubmitting}
  disabled={!isValid || isSubmitting}
>
  Submit
</Button>
```

### 在操作期间禁用

**关键：始终在异步操作期间禁用触发器。**

```tsx
// 正确 - 加载时禁用按钮
<Button
  disabled={isSubmitting}
  isLoading={isSubmitting}
  onClick={handleSubmit}
>
  Submit
</Button>

// 错误 - 用户可以多次点击
<Button onClick={handleSubmit}>
  {isSubmitting ? 'Submitting...' : 'Submit'}
</Button>
```

## 空状态

### 空状态要求

每个列表/集合都必须有一个空状态：

```tsx
// 错误 - 无空状态
return <FlatList data={items} />;

// 正确 - 显式空状态
return (
  <FlatList
    data={items}
    ListEmptyComponent={<EmptyState />}
  />
);
```

### 上下文相关的空状态

```tsx
// 搜索无结果
<EmptyState
  icon="search"
  title="No results found"
  description="Try different search terms"
/>

// 列表尚无项目
<EmptyState
  icon="plus-circle"
  title="No items yet"
  description="Create your first item"
  action={{ label: 'Create Item', onClick: handleCreate }}
/>
```

## 表单提交模式

```tsx
const MyForm = () => {
  const [submit, { loading }] = useSubmitMutation({
    onCompleted: handleSuccess,
    onError: handleError,
  });

  const handleSubmit = async () => {
    if (!isValid) {
      toast.error({ title: 'Please fix errors' });
      return;
    }
    await submit({ variables: { input: values } });
  };

  return (
    <form>
      <Input
        value={values.name}
        onChange={handleChange('name')}
        error={touched.name ? errors.name : undefined}
      />
      <Button
        type="submit"
        onClick={handleSubmit}
        disabled={!isValid || loading}
        isLoading={loading}
      >
        Submit
      </Button>
    </form>
  );
};
```

## 反面模式

### 加载状态

```typescript
// 错误 - 当数据存在时显示微调器（导致闪烁）
if (loading) return <Spinner />;

// 正确 - 仅在没有数据时显示加载
if (loading && !data) return <Spinner />;
```

### 错误处理

```typescript
// 错误 - 错误被吞掉
try {
  await mutation();
} catch (e) {
  console.log(e); // 用户不知道！
}

// 正确 - 错误被显示
onError: (error) => {
  console.error('operation failed:', error);
  toast.error({ title: 'Operation failed' });
}
```

### 按钮状态

```typescript
// 错误 - 提交时按钮未被禁用
<Button onClick={submit}>Submit</Button>

// 正确 - 禁用并显示加载
<Button onClick={submit} disabled={loading} isLoading={loading}>
  Submit
</Button>
```

## 清单

完成任何 UI 组件之前：

**UI 状态：**
- [ ] 错误状态已处理并显示给用户
- [ ] 加载状态仅在没有数据时显示
- [ ] 为集合提供了空状态
- [ ] 在异步操作期间禁用按钮
- [ ] 按钮在适当时显示加载指示器

**数据和变更：**
- [ ] 变更有 onError 处理器
- [ ] 所有用户操作都有反馈（toast/视觉）

## 与其他技能的集成

- **graphql-schema**：使用带有适当错误处理的变更模式
- **testing-patterns**：测试所有 UI 状态（加载、错误、空、成功）
- **formik-patterns**：应用表单提交模式

## 限制

- 仅当任务清晰地匹配其上游源和本地项目上下文时，才使用此技能。
- 在应用更改之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例作为环境特定测试、安全审查或用户对破坏性或成本高昂操作的批准的替代品。
