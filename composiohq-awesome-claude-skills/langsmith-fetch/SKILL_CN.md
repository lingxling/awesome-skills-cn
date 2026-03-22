---
name: langsmith-fetch
description: 通过从 LangSmith Studio 获取执行跟踪来调试 LangChain 和 LangGraph 代理。用于调试代理行为、调查错误、分析工具调用、检查内存操作或检查代理性能。自动获取最近的跟踪并分析执行模式。需要安装 langsmith-fetch CLI。
---

# LangSmith Fetch - 代理调试技能

通过在终端中直接从 LangSmith Studio 获取执行跟踪来调试 LangChain 和 LangGraph 代理。

## 何时使用此技能

当用户提到以下内容时自动激活：
- 🐛 "调试我的代理" 或 "出了什么问题？"
- 🔍 "显示我最近的跟踪" 或 "发生了什么？"
- ❌ "检查错误" 或 "为什么失败了？"
- 💾 "分析内存操作" 或 "检查 LTM"
- 📊 "审查代理性能" 或 "检查代币使用情况"
- 🔧 "调用了哪些工具？" 或 "显示执行流程"

## 先决条件

### 1. 安装 langsmith-fetch
```bash
pip install langsmith-fetch
```

### 2. 设置环境变量
```bash
export LANGSMITH_API_KEY="your_langsmith_api_key"
export LANGSMITH_PROJECT="your_project_name"
```

**验证设置：**
```bash
echo $LANGSMITH_API_KEY
echo $LANGSMITH_PROJECT
```

## 核心工作流程

### 工作流程 1：快速调试最近活动

**当用户询问：** "刚刚发生了什么？" 或 "调试我的代理"

**执行：**
```bash
langsmith-fetch traces --last-n-minutes 5 --limit 5 --format pretty
```

**分析并报告：**
1. ✅ 找到的跟踪数量
2. ⚠️ 任何错误或失败
3. 🛠️ 调用的工具
4. ⏱️ 执行时间
5. 💰 代币使用情况

**示例响应格式：**
```
在过去 5 分钟内找到 3 个跟踪：

跟踪 1：✅ 成功
- 代理：memento
- 工具：recall_memories, create_entities
- 持续时间：2.3s
- 代币：1,245

跟踪 2：❌ 错误
- 代理：cypher
- 错误："Neo4j 连接超时"
- 持续时间：15.1s
- 失败点：search_nodes 工具

跟踪 3：✅ 成功
- 代理：memento
- 工具：store_memory
- 持续时间：1.8s
- 代币：892

💡 发现问题：跟踪 2 因 Neo4j 超时而失败。建议检查数据库连接。
```

---

### 工作流程 2：深入分析特定跟踪

**当用户提供：** 跟踪 ID 或说 "调查那个错误"

**执行：**
```bash
langsmith-fetch trace <trace-id> --format json
```

**分析 JSON 并报告：**
1. 🎯 代理试图做什么
2. 🛠️ 调用了哪些工具（按顺序）
3. ✅ 工具结果（成功/失败）
4. ❌ 错误消息（如有）
5. 💡 根本原因分析
6. 🔧 建议的修复方案

**示例响应格式：**
```
深入分析 - 跟踪 abc123

目标：用户询问 "在 Neo4j 中查找所有项目"

执行流程：
1. ✅ search_nodes(query: "projects")
   → 找到 24 个节点

2. ❌ get_node_details(node_id: "proj_123")
   → 错误："节点未找到"
   → 这是失败点

3. ⏹️ 执行停止

根本原因：
search_nodes 工具返回的节点 ID 在数据库中已不存在，
可能是由于最近的删除操作。

建议的修复方案：
1. 在 get_node_details 工具中添加错误处理
2. 在搜索结果中过滤已删除的节点
3. 更新缓存失效策略

代币使用：1,842 代币（$0.0276）
执行时间：8.7 秒
```

---

### 工作流程 3：导出调试会话

**当用户说：** "保存此会话" 或 "导出跟踪"

**执行：**
```bash
# 创建带时间戳的会话文件夹
SESSION_DIR="langsmith-debug/session-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SESSION_DIR"

# 导出跟踪
langsmith-fetch traces "$SESSION_DIR/traces" --last-n-minutes 30 --limit 50 --include-metadata

# 导出线程（对话）
langsmith-fetch threads "$SESSION_DIR/threads" --limit 20
```

**报告：**
```
✅ 会话导出成功！

位置：langsmith-debug/session-20251224-143022/
- 跟踪：42 个文件
- 线程：8 个文件

您现在可以：
1. 查看单个跟踪文件
2. 与团队共享文件夹
3. 使用外部工具进行分析
4. 存档以备将来参考

会话大小：2.3 MB
```

---

### 工作流程 4：错误检测

**当用户询问：** "显示我错误" 或 "什么在失败？"

**执行：**
```bash
# 获取最近的跟踪
langsmith-fetch traces --last-n-minutes 30 --limit 50 --format json > recent-traces.json

# 搜索错误
grep -i "error\|failed\|exception" recent-traces.json
```

**分析并报告：**
1. 📊 发现的总错误数
2. ❌ 错误类型和频率
3. 🕐 错误发生的时间
4. 🎯 哪些代理/工具失败了
5. 💡 常见模式

**示例响应格式：**
```
错误分析 - 过去 30 分钟

总跟踪数：50
失败的跟踪：7（14% 失败率）

错误分解：
1. Neo4j 连接超时（4 次出现）
   - 代理：cypher
   - 工具：search_nodes
   - 首次出现：14:32
   - 最后出现：14:45
   - 模式：在峰值负载期间发生

2. 内存存储失败（2 次出现）
   - 代理：memento
   - 工具：store_memory
   - 错误："Pinecone 速率限制超出"
   - 发生时间：14:38, 14:41

3. 工具未找到（1 次出现）
   - 代理：sqlcrm
   - 尝试的工具："export_report"（不存在）
   - 发生时间：14:35

💡 建议：
1. 为 Neo4j 超时添加重试逻辑
2. 为 Pinecone 实现速率限制
3. 修复 sqlcrm 工具配置
```

---

## 常见用例

### 用例 1："代理无响应"

**用户说：** "我的代理什么都不做"

**步骤：**
1. 检查是否存在跟踪：
   ```bash
   langsmith-fetch traces --last-n-minutes 5 --limit 5
   ```

2. **如果未找到跟踪：**
   - 跟踪可能已禁用
   - 检查：环境中是否设置了 `LANGCHAIN_TRACING_V2=true`
   - 检查：是否设置了 `LANGCHAIN_API_KEY`
   - 验证代理是否实际运行

3. **如果找到跟踪：**
   - 检查错误
   - 检查执行时间（是否挂起？）
   - 验证工具调用是否完成

---

### 用例 2："调用了错误的工具"

**用户说：** "为什么它使用了错误的工具？"

**步骤：**
1. 获取特定跟踪
2. 查看执行时可用的工具
3. 检查代理选择工具的推理
4. 检查工具描述/说明
5. 建议提示或工具配置改进

---

### 用例 3："内存不工作"

**用户说：** "代理不记得事情"

**步骤：**
1. 搜索内存操作：
   ```bash
   langsmith-fetch traces --last-n-minutes 10 --limit 20 --format raw | grep -i "memory\|recall\|store"
   ```

2. 检查：
   - 内存工具是否被调用？
   - 回忆是否返回结果？
   - 记忆是否实际存储？
   - 检索的记忆是否被使用？

---

### 用例 4："性能问题"

**用户说：** "代理太慢了"

**步骤：**
1. 导出带元数据：
   ```bash
   langsmith-fetch traces ./perf-analysis --last-n-minutes 30 --limit 50 --include-metadata
   ```

2. 分析：
   - 每个跟踪的执行时间
   - 工具调用延迟
   - 代币使用情况（上下文大小）
   - 迭代次数
   - 最慢的操作

3. 识别瓶颈并建议优化

---

## 输出格式指南

### 美化格式（默认）
```bash
langsmith-fetch traces --limit 5 --format pretty
```
**用途：** 快速视觉检查，向用户展示

### JSON 格式
```bash
langsmith-fetch traces --limit 5 --format json
```
**用途：** 详细分析，语法高亮审查

### 原始格式
```bash
langsmith-fetch traces --limit 5 --format raw
```
**用途：** 传递给其他命令，自动化

---

## 高级功能

### 基于时间的过滤
```bash
# 特定时间戳之后
langsmith-fetch traces --after "2025-12-24T13:00:00Z" --limit 20

# 最近 N 分钟（最常见）
langsmith-fetch traces --last-n-minutes 60 --limit 100
```

### 包含元数据
```bash
# 获取额外上下文
langsmith-fetch traces --limit 10 --include-metadata

# 元数据包括：代理类型、模型、标签、环境
```

### 并发获取（更快）
```bash
# 加速大型导出
langsmith-fetch traces ./output --limit 100 --concurrent 10
```

---

## 故障排除

### "未找到匹配条件的跟踪"

**可能的原因：**
1. 时间范围内没有代理活动
2. 跟踪已禁用
3. 项目名称错误
4. API 密钥问题

**解决方案：**
```bash
# 1. 尝试更长的时间范围
langsmith-fetch traces --last-n-minutes 1440 --limit 50

# 2. 检查环境
echo $LANGSMITH_API_KEY
echo $LANGSMITH_PROJECT

# 3. 尝试获取线程
langsmith-fetch threads --limit 10

# 4. 验证代码中是否启用了跟踪
# 检查：LANGCHAIN_TRACING_V2=true
```

### "项目未找到"

**解决方案：**
```bash
# 查看当前配置
langsmith-fetch config show

# 设置正确的项目
export LANGSMITH_PROJECT="correct-project-name"

# 或永久配置
langsmith-fetch config set project "your-project-name"
```

### 环境变量不持久

**解决方案：**
```bash
# 添加到 shell 配置文件（~/.bashrc 或 ~/.zshrc）
echo 'export LANGSMITH_API_KEY="your_key"' >> ~/.bashrc
echo 'export LANGSMITH_PROJECT="your_project"' >> ~/.bashrc

# 重新加载 shell 配置
source ~/.bashrc
```

---

## 最佳实践

### 1. 定期健康检查
```bash
# 进行更改后快速检查
langsmith-fetch traces --last-n-minutes 5 --limit 5
```

### 2. 组织存储
```
langsmith-debug/
├── sessions/
│   ├── 2025-12-24/
│   └── 2025-12-25/
├── error-cases/
└── performance-tests/
```

### 3. 记录发现
当你发现错误时：
1. 导出有问题的跟踪
2. 保存到 `error-cases/` 文件夹
3. 在 README 中记录问题
4. 与团队共享跟踪 ID

### 4. 与开发集成
```bash
# 提交代码前
langsmith-fetch traces --last-n-minutes 10 --limit 5

# 如果发现错误
langsmith-fetch trace <error-id> --format json > pre-commit-error.json
```

---

## 快速参考

```bash
# 最常用的命令

# 快速调试
langsmith-fetch traces --last-n-minutes 5 --limit 5 --format pretty

# 特定跟踪
langsmith-fetch trace <trace-id> --format pretty

# 导出会话
langsmith-fetch traces ./debug-session --last-n-minutes 30 --limit 50

# 查找错误
langsmith-fetch traces --last-n-minutes 30 --limit 50 --format raw | grep -i error

# 带元数据
langsmith-fetch traces --limit 10 --include-metadata
```

---

## 资源

- **LangSmith Fetch CLI：** https://github.com/langchain-ai/langsmith-fetch
- **LangSmith Studio：** https://smith.langchain.com/
- **LangChain 文档：** https://docs.langchain.com/
- **此技能仓库：** https://github.com/OthmanAdi/langsmith-fetch-skill

---

## 给 Claude 的说明

- 在运行命令前始终检查是否安装了 `langsmith-fetch`
- 验证环境变量是否设置
- 使用 `--format pretty` 获得人类可读的输出
- 当需要解析和分析数据时使用 `--format json`
- 导出会话时，创建有组织的文件夹结构
- 始终提供清晰的分析和可操作的见解
- 如果命令失败，帮助排查配置问题

---

**版本：** 0.1.0
**作者：** Ahmad Othman Ammar Adi
**许可证：** MIT
**仓库：** https://github.com/OthmanAdi/langsmith-fetch-skill