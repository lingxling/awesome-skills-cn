---
name: testing-qa
description: "全面的测试和 QA 工作流，涵盖单元测试、集成测试、E2E 测试、浏览器自动化和质量保证。"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# 测试/QA 工作流包

## 概述

全面的测试和质量保证工作流，涵盖单元测试、集成测试、E2E 测试、浏览器自动化和用于生产就绪软件的质量门控。

## 何时使用此工作流

当以下情况时使用此工作流：
- 建立测试基础设施
- 编写单元和集成测试
- 实施 E2E 测试
- 自动化浏览器测试
- 建立质量门控
- 执行代码审查

## 工作流阶段

### 阶段 1：测试策略

#### 要调用的技能
- `test-automator` - 测试自动化
- `test-driven-development` - TDD

#### 操作
1. 定义测试策略
2. 选择测试框架
3. 规划测试覆盖率
4. 建立测试基础设施
5. 配置 CI 集成

#### 复制粘贴提示
```
使用 @test-automator 来设计测试策略
```

```
使用 @test-driven-development 来实施 TDD 工作流
```

### 阶段 2：单元测试

#### 要调用的技能
- `javascript-testing-patterns` - Jest/Vitest
- `python-testing-patterns` - pytest
- `unit-testing-test-generate` - 测试生成
- `tdd-orchestrator` - TDD 编排

#### 操作
1. 编写单元测试
2. 建立测试夹具
3. 配置模拟
4. 测量覆盖率
5. 与 CI 集成

#### 复制粘贴提示
```
使用 @javascript-testing-patterns 来编写 Jest 测试
```

```
使用 @python-testing-patterns 来编写 pytest 测试
```

```
使用 @unit-testing-test-generate 来生成单元测试
```

### 阶段 3：集成测试

#### 要调用的技能
- `api-testing-observability-api-mock` - API 测试
- `e2e-testing-patterns` - 集成模式

#### 操作
1. 设计集成测试
2. 建立测试数据库
3. 配置 API 模拟
4. 测试服务交互
5. 验证数据流

#### 复制粘贴提示
```
使用 @api-testing-observability-api-mock 来测试 API
```

### 阶段 4：E2E 测试

#### 要调用的技能
- `playwright-skill` - Playwright 测试
- `e2e-testing-patterns` - E2E 模式
- `webapp-testing` - Web 应用测试

#### 操作
1. 设计 E2E 场景
2. 编写测试脚本
3. 配置测试数据
4. 建立并行执行
5. 实施视觉回归

#### 复制粘贴提示
```
使用 @playwright-skill 来创建 E2E 测试
```

```
使用 @e2e-testing-patterns 来设计 E2E 策略
```

### 阶段 5：浏览器自动化

#### 要调用的技能
- `browser-automation` - 浏览器自动化
- `webapp-testing` - 浏览器测试
- `screenshots` - 截图自动化

#### 操作
1. 建立浏览器自动化
2. 配置无头测试
3. 实施视觉测试
4. 捕获截图
5. 测试响应式设计

#### 复制粘贴提示
```
使用 @browser-automation 来自动化浏览器任务
```

```
使用 @screenshots 来捕获营销截图
```

### 阶段 6：性能测试

#### 要调用的技能
- `performance-engineer` - 性能工程
- `performance-profiling` - 性能分析
- `web-performance-optimization` - Web 性能

#### 操作
1. 设计性能测试
2. 建立负载测试
3. 测量响应时间
4. 识别瓶颈
5. 优化性能

#### 复制粘贴提示
```
使用 @performance-engineer 来测试应用性能
```

### 阶段 7：代码审查

#### 要调用的技能
- `code-reviewer` - AI 代码审查
- `code-review-excellence` - 审查最佳实践
- `find-bugs` - 缺陷检测
- `security-scanning-security-sast` - 安全扫描

#### 操作
1. 配置审查工具
2. 运行自动审查
3. 检查缺陷
4. 验证安全性
5. 批准更改

#### 复制粘贴提示
```
使用 @code-reviewer 来审查拉取请求
```

```
使用 @find-bugs 来检测代码缺陷
```

### 阶段 8：质量门控

#### 要调用的技能
- `lint-and-validate` - Linting
- `verification-before-completion` - 验证

#### 操作
1. 配置 linters
2. 建立格式化程序
3. 定义质量指标
4. 实施门控
5. 监控合规性

#### 复制粘贴提示
```
使用 @lint-and-validate 来检查代码质量
```

```
使用 @verification-before-completion 来验证更改
```

## 测试金字塔

```
        /       /  \    E2E 测试 (10%)
      /----     /      \  集成测试 (20%)
    /--------   /          \ 单元测试 (70%)
  /------------```

## 质量门控检查表

- [ ] 单元测试覆盖率 > 80%
- [ ] 所有测试通过
- [ ] 关键路径的 E2E 测试
- [ ] 性能基准已达成
- [ ] 安全扫描已通过
- [ ] 代码审查已批准
- [ ] Linting 清晰

## 相关工作流包

- `development` - 开发工作流
- `security-audit` - 安全测试
- `cloud-devops` - CI/CD 集成
- `ai-ml` - AI 测试

## 限制
- 仅当任务明确符合上述范围时，才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并要求澄清。
