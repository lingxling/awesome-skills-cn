---
name: attack-chain
description: "授权的多阶段攻击路径规划和编排，跨越侦察、初始访问、权限提升、横向移动和报告。完整参与和跨阶段操作的入口点。"
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ 仅授权使用**
> 此技能仅用于教育目的或授权的安全评估。
> 在使用此工具前，你必须获得系统所有者的明确书面许可。
> 滥用此工具是违法的，严格禁止。

> **强制确认门**
> 在运行任何探测、利用、改变、持续、从目标提取数据或尝试凭证访问的命令前：
> 1. 要求用户说明确切的目标 URL、IP、帐户或资源。
> 2. 要求用户确认书面授权和允许的范围。
> 3. 显示确切的命令并解释其预期效果。
> 4. 在当前对话中等待明确确认。
>
> 没有该确认，保持只读并仅提供防御指导。优选沙箱、一次性 VM 或受控实验室。

# 攻击链编排技能
## 何时使用

- 授权参与跨越多个杀伤链阶段。
- 协调多个专家技能到一个连贯的攻击路径。

## 何时路由到本技能

以下场景**必须**先经过本技能做全链路规划，再分发到具体子技能执行：

| 场景 | 为什么需要编排 |
|------|--------------|
| "帮我做一次完整的渗透测试" | 需要规划从信息收集到报告的全流程 |
| "从外网打到域控" | 跨越边界突破→提权→横向→AD 多个阶段 |
| "HW 攻防演练" | 需要完整攻击链 + 隐蔽性 + 痕迹清理 |
| "评估这个目标的攻击面" | 需要多维度信息收集 + 路径规划 |
| "我拿到了一个 webshell，下一步怎么办" | 需要从当前据点规划后续路径 |
| "帮我规划攻击路径" | 明确需要路径编排 |
| "从这个漏洞能打到什么程度" | 需要评估漏洞的链式利用价值 |
| "Bug Bounty 持续监控" | 需要自动化多阶段流程 |
| "内网渗透全流程" | 横向移动 + 提权 + 域攻击组合 |
| "近源渗透方案" | 物理接入 + 内网渗透组合 |
| "供应链攻击路径" | 跨组织多跳攻击 |
| "钓鱼 + 后渗透" | 初始访问 + 后续利用组合 |

**单阶段任务不需要经过本技能**：
- 只做端口扫描 → 直接去 `pentest-tools/`
- 只做 SQL 注入 → 直接去 `pentest-tools/`
- 只做 APK 逆向 → 直接去 `apk-reverse/`
- 只做域渗透 → 直接去 `windows-ad/SKILL.md`

---

## 编排原则

### 本技能的角色

```
用户提出多阶段任务
    ↓
attack-chain/SKILL.md（本文件）
    ↓ 规划攻击路径、确定阶段顺序
    ↓ 评估每阶段所需工具和方法
    ↓
分发到具体子技能执行：
    ├── pentest-tools/     → 工具调用、漏洞利用
    ├── apk-reverse/       → 移动端渗透
    ├── js-reverse/        → Web 前端突破
    ├── reverse-engineering/ → 二进制分析
    ├── ida-reverse/       → 深度逆向
    └── browser-automation/ → 自动化操作
    ↓
每阶段完成后回到本技能评估下一步
    ↓
全部完成 → docs-generator 生成报告
```

### 路径规划决策树

```
拿到目标后：
1. 目标是什么？（Web/内网/云/移动/IoT）
2. 当前有什么？（外部视角/已有凭据/已有据点）
3. 最终目标是什么？（域控/数据/特定系统/证明影响）
4. 约束条件？（时间/隐蔽性/不可触碰的系统）
    ↓
根据以上信息规划最短路径
    ↓
一条路走不通 → 回到本技能重新规划备选路径
```

---

## 完整攻击链阶段

---

有关详细阶段方法、工具链和剧本，请参考：
- [攻击链阶段和剧本](references/phases.md)

## 红队行动铁律

### 三条底线

1. **所有操作必须获得书面授权**
2. **数据渗出需进行匿名化处理**
3. **清理所有攻击痕迹（包括内存驻留）**

### 行动纪律

- 每个操作前评估风险等级（低/中/高/严重）
- 高风险操作前通知项目经理
- 保持操作日志（时间、动作、结果）
- 发现高危漏洞立即上报，不扩大利用
- 不影响业务可用性（禁止 DoS）
- 不访问/下载真实用户数据

### 典型失败案例

| 失败原因 | 后果 | 教训 |
|---------|------|------|
| 未清除 Mimikatz 内存 dump | 蓝队溯源完整攻击路径 | 操作后立即清理 |
| C2 域名被威胁情报标记 | 首次连接即被拦截 | 使用新注册域名 + 域前置 |
| 钓鱼邮件触发 DLP 告警 | 蓝队提前预警 | 测试邮件网关规则 |
| 横向移动触发蜜罐 | 暴露攻击意图 | 先识别蜜罐再行动 |

---

## 工具速查表

### 信息收集
`subfinder` `amass` `httpx` `naabu` `katana` `gau` `dnsx` `nmap` `whatweb` `wpscan`

### 漏洞利用
`nuclei` `sqlmap` `sstimap` `xsstrike` `burpsuite` `metasploit`

### 权限提升
`winPEAS` `linpeas` `GodPotato` `PrintSpoofer` `watson`

### 横向移动
`mimikatz` `crackmapexec/netexec` `impacket` `bloodhound` `certipy` `coercer` `responder` `evil-winrm`

### C2 框架
`cobalt-strike` `sliver` `havoc` `mythic` `adaptixc2`

### 近源渗透
`fluxion` `aircrack-ng` `proxmark3` `rubber-ducky` `wifi-pineapple`

---

## 与本包其他技能的关系

| 需求 | 路由到 |
|------|--------|
| Web 漏洞深度利用 | `pentest-tools/SKILL.md` |
| 内网 AD 攻击详细步骤 | `windows-ad/SKILL.md` |
| 逆向分析恶意样本 | `reverse-engineering/SKILL.md` |
| APK 逆向（移动端渗透） | `apk-reverse/SKILL.md` |
| JS 前端签名绕过 | `js-reverse/SKILL.md` |
| 自动化群体渗透 | Pentest Swarm AI（`pentestswarm scan --swarm`） |
| AI 辅助渗透 | `mcp-kali-server` / `metasploitmcp` / `hexstrike-ai` |
| 报告生成 | `docs-generator/SKILL.md` |
| 攻击路径图 | `diagram-generator/SKILL.md` |

## 任务完成自检（声称完成前 MUST 通过）

- [ ] 我是否执行了工作流中的每一步（而不是只阅读）？
- [ ] 我是否基于 `tool-index` 使用了真实工具路径？
- [ ] 我是否产出了可复现证据（命令/脚本/截图/报告）？
- [ ] 我是否完成并回写了 RULES 要求的 Checklist 项？

## 限制

- 攻击阶段的执行需要按目标获得书面授权。
- 假设支持工具（侦察/利用工具包）已安装并在适用时获得许可。

> 改编自 [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT)。
