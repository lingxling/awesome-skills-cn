---
name: check-identity-pack
description: 在一组文件上运行 AFP 100 分或 AUSTRAC 安全港身份检查，并报告确切缺失的内容。当用户要求检查身份文件、验证某人的身份以进行入职或评估文件包是否满足澳大利亚身份要求时使用。
category: document-verification
risk: critical
source: community
source_repo: Sketchjar/stipple-agent-skills
source_type: community
date_added: "2026-08-31"
author: Sketchjar
tags: [document-verification, fact-checking, stipple, authenticity]
tools: [claude, cursor, gemini, codex]
license: "Apache-2.0"
license_source: "https://github.com/Sketchjar/stipple-agent-skills/blob/main/LICENSE"
---

# 检查身份文件包

在文件集上运行 AFP 100 分或 AUSTRAC 安全港身份检查。报告获得的分数、每个文件的状态以及**确切缺失的内容** — 以便用户可以仅请求不存在的文件并重新运行。使用 Stipple API（免费匿名层）。

## 何时使用

- 在澳大利亚为员工、租户、承包商或客户入职
- 需要 AFP 100 分或 AUSTRAC 安全港合规的 KYC 流
- "这些文件是否满足 100 分检查？"

## 说明

1. **获取文件。** 多个文件路径或 URL (PDF/图像)：护照、驾驶执照、医疗保险卡、银行对账单、公用事业单据等。

2. **选择方案：**
   - `afp_100_point` — 标准澳大利亚 100 分系统
   - `austrac_safe_harbour` — AUSTRAC 安全港身份验证

3. **运行检查。** POST 文件集（多部分、多个 `files` 部分）：

   ```bash
   curl -X POST "https://www.stipple.sh/v1/identity-check?scheme=afp_100_point" \
     -F "files=@passport.pdf" \
     -F "files=@medicare-card.jpg" \
     -F "files=@bank-statement.pdf" \
     -H "Authorization: Bearer $STIPPLE_API_KEY"
   ```

4. **解释响应。**

   - `status` — complete / incomplete / failed
   - `points_total` — 获得的分数（例如 95/100）
   - `checks[]` — 每个文件：检测到的类型、分值、状态
   - `missing[]` — **确切缺失的内容**（例如"过去 3 个月内当前住宅地址的证明"）

5. **报告并将差距列表放在最前面。** 这里的产品是*确切缺失的内容*列表 — 用户的入职 UX 可以循环它：仅请求缺少的内容、重新运行、完成。

6. **重要警告。** 身份检查回答*这是谁* — 它不回答*这个文件是真实的吗*。一份与名字匹配的伪造护照会得分。对于真实性，首先在每个文件上与 `verify-document` 技能配对。

## 输出格式

```
AFP 100-point check: incomplete

  points attained: 95/100
  - passport: 70 pts — ok
  - medicare_card: 25 pts — ok
  - drivers_licence: 40 pts — ok

  exactly what is missing:
    -> evidence of current residential address within last 3 months
```

## 限制和安全

- 此工作流将身份和地址文件上传到托管的第三方
  服务。在传输前获得用户的明确批准、最小化
  发送的文件和字段，并确认提供商对用于
  预期司法管辖区的当前保留、居住地、
  访问和删除条款。
- 分数结果是审查的辅助工具，不是法律 KYC/AML 判定。根据当前 AFP、AUSTRAC 和组织要求验证
  方案规则，并让合格的人类审查员对
  入职决定负责。
- 切勿将通过的分数视为文件真实或命名
  人员控制它的证明；在决定值得的地方
  运行独立的真实性和活跃度检查。

## 注意事项

- 每次检查花费 2 个学分；免费每周限额适用
- 分值：护照 70、公民证书 70、出生证明 70、驾驶执照 40、医疗保险卡 25、银行对账单 25、公用事业单据 25、理事会费率 25
- 检查将文件映射到方案并报告差距 — 它不验证文件真实性（使用 `verify-document` 实现）
- 免费密钥，位于 https://www.stipple.sh 用于超出匿名限额的计量
