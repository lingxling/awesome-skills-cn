---
name: case-review
description: "逆向工程或评估案例包的质量门审查：范围就绪情况、证据-发现-路径可追踪性、工作项覆盖、时间线一致性和工件哈希。"
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
# 证据图审查
## 何时使用

- 在提交分析报告前，验证可追踪性和完整性。
- 审计结论是否由记录的证据支持。


当逆向工程、取证、CTF 或授权安全案例需要可防守的交付时使用此技能。它审计现有的 `work/<case>/` 包，而不更改案例或接触目标。

## 范围

此技能涵盖：

- 范围元数据和目标活动就绪情况
- 证据记录结构和可复现字段
- 工作项和时间线条目对证据的引用
- 报告 Markdown 中的结构化发现和路径
- 对案例本地工件的可选 SHA-256 验证
- 用于报告交付的 Markdown 或 JSON 审查结果

它不得执行侦察、利用、动态检测或目标更改。这些操作属于路由分析技能，需要案例范围门。

## 工具依赖

| 工具 | 必需 | 目的 | 自动引导 |
|------|----------|---------|---------------|
| Python 3.9+ | 是 | 运行只读案例审查脚本 | 否，使用平台 Python 安装 |

不需要网络访问或第三方包。

## 工作流

### 阶段 1：接收

针对现有案例目录运行审查：

```bash
python3 skills/case-review/scripts/review_case.py work/<case> --format markdown
```

确认 `scope.md`、`timeline.md`、`workitems.md` 和 `evidence/` 存在。非严格审查会报告范围警告，而严格审查会将警告视为交付阻塞程序。

## 建议下一步（选一个编号）

1. 修复 scope.md 中的授权、范围或 network_profile 字段
2. 继续检查 Evidence 记录的可复现命令和来源
3. 导出当前 review 结果并附到阶段性报告
4. 换 JSON 输出接入 CI 或其他审查工具
5. 暂停，先确认审查范围

### 阶段 2：可追踪性

审查检查：

- 不存在的证据 ID
- 没有 `evidence_ids` 的发现
- 没有允许的 `path_type` 或证据引用的路径
- 指向未知证据的工作项和时间线条目
- 未链接的证据记录
- 置信度低的已验证发现

离线观察只有在其 `notes` 字段明确记录离线限制时，才能使用 `repro_command: n/a`。

当另一个工具需要稳定字段时使用 JSON：

```bash
python3 skills/case-review/scripts/review_case.py work/<case> --format json
```

## 建议下一步（选一个编号）

1. 补写缺失的 Evidence，并保留原始命令
2. 将候选 Finding 绑定到 Evidence 后重新审查
3. 为调用链或攻击链补充 P-id 和 Path 步骤
4. 生成 Markdown handoff summary
5. 换回 PRIMARY skill 继续分析

### 阶段 3：固定性验证

当证据记录同时包含 `content_hash` 和 `artifact_path` 时，验证案例本地工件：

```bash
python3 skills/case-review/scripts/review_case.py work/<case> --verify-hashes --strict
```

脚本接受 `sha256:<64 hex characters>` 并检查工件是否保留在案例根目录内。哈希不匹配是硬故障。

PowerShell 证据帮助程序可以在追加记录时记录哈希：

```powershell
powershell -File skills/scripts/append-evidence.ps1 -CaseRoot work\<case> -Id E-001 -Title "Sample hash" -ReproCommand "sha256sum evidence/sample.bin" -ArtifactPath "evidence\sample.bin"
```

## 建议下一步（选一个编号）

1. 修复 hash mismatch 或替换已污染的工作副本
2. 为未固定的原始文件补充 SHA-256 和 artifact_path
3. 继续进入报告生成阶段
4. 导出 JSON 结果供 CI 保存
5. 暂停并请求人工复核

### 阶段 4：交付

在最终报告或专家交付前使用严格模式：

```bash
python3 skills/case-review/scripts/review_case.py work/<case> --strict --format markdown > work/<case>/report/case-review.md
```

该命令对案例是只读的，除非明确使用 shell 重定向来保存其输出。审查不是法律建议，不取代组织证据处理程序。

## 建议下一步（选一个编号）

1. 将通过的 review 结果交给 `docs-generator/` 生成正式报告
2. 回到 PRIMARY skill 补齐新的分析证据
3. 归档 Markdown 和 JSON review 结果
4. 暂停并请求人工复核

## 语言行为合约

- 内部推理、工具选择和阶段控制：英文。
- 用户可见的消息、部分标签、报告和下一步菜单：中文，除非用户要求另一种语言。
- 默认双语标签将中文放在前面，英文放在后面，用 `/` 分隔。

## 引导边界

此技能没有第三方依赖。如果 Python 3 不可用，唯一允许的恢复操作是当为当前平台注册了 Python 功能时的存储库引导路径。如果未注册这样的功能，停止并报告缺失的运行时。不要猜测可执行文件路径、下载包或从此技能内部执行手动安装。

## 路由上下文

**上游入口**：任何已生成案例包的逆向、取证、CTF 或授权安全技能。

**下游出口**：用于正式报告的 `docs-generator/`，或当图不完整时的原始 PRIMARY 技能。

**相关模块**：`ops/evidence-finding-path.md`、`ops/timeline-workitem.md`、`digital-forensics/`、`reverse-engineering/` 和 `docs-generator/`。

## 参考资源

- [NIST SP 800-86: Guide to Integrating Forensic Techniques into Incident Response](https://csrc.nist.gov/pubs/sp/800/86/final)
- [SWGDE Best Practices for Computer Forensic Acquisitions](https://www.swgde.org/documents/published-complete-listing/17-f-002-2-1/)
- [SWGDE Best Practices for Archiving Digital and Multimedia Evidence](https://www.swgde.org/documents/published-complete-listing/19-f-003-best-practices-for-archiving-digital-and-multimedia-evidence/)

## 任务完成自检

- [ ] 我是否审查了 scope.md、timeline.md、workitems.md 和 evidence/？
- [ ] 所有 Finding 是否引用了现存 Evidence？
- [ ] 所有 Path 是否包含合法 path_type 和 Evidence 引用？
- [ ] 是否执行了 hash verification，或记录了未执行原因？
- [ ] 是否以 strict 模式重新运行并保存了 review 结果？

## 限制

- 期望结构化案例布局（范围、证据、发现）；临时便笺需要预先组织。
- 审查文档质量，而非发现的技术正确性。

> 改编自 [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT)。
