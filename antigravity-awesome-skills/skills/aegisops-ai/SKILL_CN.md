---
name: aegisops-ai
description: "自治 DevSecOps 和 FinOps 防护措施。编排 Gemini 3 Flash 来审计 Linux Kernel 补丁、Terraform 成本漂移和 K8s 合规性。"
risk: safe
source: community
author: Champbreed
date_added: "2026-03-24"
---

# /aegisops-ai — 自治治理编排器

AegisOps-AI 是一个专业级的"活络管道"，
它将高级 AI 推理直接集成到
SDLC 中。它充当系统级安全、云基础设施成本
和 Kubernetes 合规性的智能网关。

## 目标

通过以下方式自动化高风险安全和财务审计：
1. 在 Linux Kernel 补丁中识别基于逻辑的漏洞（UAF、Stale 
State）。
2. 检测 Terraform 计划中的大规模"沉默灾难"成本漂移。
3. 将自然语言安全意图转化为强化的 K8s 清单。

## 何时使用
- **Kernel 补丁评审：**审计基于 C 的 Git 差异以实现内存安全。
- **IaC 应用前审计：**分析 `terraform plan` 输出以防止账单飙升。
- **集群强化：**为部署生成"最小权限" securityContexts。
- **CI/CD 质量门控：**通过 GitHub Actions 阻止不合规的合并。

## 何时不使用

- **Web 应用逻辑：**不用于标准 Web 漏洞（XSS、SQLi）；使用专用 SAST 扫描仪。
- **非 C 内存分析：**补丁分析器针对 C 逻辑进行了优化；避免将其用于 Python 或 JS 等高级语言。
- **直接资源变更：**这是一个*审计工具*，不是部署工具。它不执行 `terraform apply` 或 `kubectl apply`。
- **事后分析：**要分析*为什么*之前的 AI 会话失败，请改用 `/analyze-project`。

---
## 🤖 生成式 AI 集成

AegisOps-AI 利用 **Google GenAI SDK** 来实现用于自治安全和财务审计的"推理路径"：

* **神经补丁分析：**对 Linux Kernel 补丁进行语义代码审查，超越简单的模式匹配来理解复杂的内存状态逻辑。
* **智能成本综合：**通过财务推理模型处理原始 Terraform 计划差异，以检测高风险资源升级和"沉默"财务漂移。
* **自然语言政策映射：**将人类安全意图转化为语法正确的、强化的 Kubernetes `securityContext` 配置。

## 🧭 核心模块

### 1. 🐧 Kernel 补丁审查器（`patch_analyzer.py`）

* **问题：**Linux Kernel 内存安全的手动审查耗时且容易出错。
* **解决方案：**Gemini 3 对原始 Git 差异执行"深度推理"审计，在几秒钟内检测关键内存损坏漏洞（UAF、Stale State）。
* **关键输出：** `analysis_results.json`

### 2. 💰 FinOps 和云审计器（`cost_auditor.py`）

* **问题：**基础设施即代码（IaC）更改可能导致意外的"沉默灾难"和大规模云账单飙升。
* **解决方案：**分析 `terraform plan` 输出以识别成本异常——例如从 `t3.micro` 意外升级到高性能 GPU 实例。
* **关键输出：** `infrastructure_audit_report.json`

### 3. ☸️ K8s 政策强化器（`k8s_policy_generator.py`）

* **问题：**在 Kubernetes 中实现"最小权限"安全上下文很复杂且经常被忽视。
* **解决方案：**将自然语言安全要求转化为生产就绪、强化的 YAML 清单（只读根文件系统、非 root 强制执行等）。
* **关键输出：** `hardened_deployment.yaml`

## 🛠️ 设置和环境

### 1. 克隆仓库

```bash
git clone https://github.com/Champbreed/AegisOps-AI.git
cd AegisOps-AI
```
## 2. 设置

```bash
python3 -m venv venv
source venv/bin/activate
pip install google-genai python-dotenv
```
### 3. API 配置

在根目录中创建一个 `.env` 文件来安全地
存储您的凭证：

```bash
printf 'GEMINI_API_KEY=%s\n' "$GEMINI_API_KEY" > .env
```
## 🏁 操作仪表板

按顺序执行所有代理的完整套件并生成所有安全报告：

```bash
python3 main.py
```
### 模式：过度授权容器

* **指标：** `allowPrivilegeEscalation: true` 或 root 用户执行。
* **调查：**将安全意图（例如"仅非 root"）传递给 K8s Hardener 模块。

---

## 💡 最佳实践

* **上下文至关重要：**在 Git 差异周围提供至少 5 行上下文以获得更准确的神经推理。
* **持续门控：**在每次基础设施更改之前运行 FinOps 审计，而不是之后。
* **手动签署：**使用 AI 发现作为高保真信号，但在 Kernel 级合并中保持人类参与。

---

## 🔒 安全和安全说明

* **密钥管理：**在生产中对 `GEMINI_API_KEY` 使用 CI/CD 秘密。
* **最小权限：**首先在暂存环境中测试"强化"清单，以确保没有功能回归。

## 链接

+ - **仓库**：https://github.com/Champbreed/AegisOps-AI
+ - **文档**：https://github.com/Champbreed/AegisOps-AI#readme

## 限制条件
- 仅在任务明确与上述范围相匹配时才使用此技能。
- 不要将输出作为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并要求澄清。
