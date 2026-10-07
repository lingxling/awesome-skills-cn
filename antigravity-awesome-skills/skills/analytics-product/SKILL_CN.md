---
name: analytics-product
description: "产品分析 —— PostHog、Mixpanel、事件、转化漏斗(funnel)、群组(cohort)、留存、北极星指标、OKR 与产品看板。"
risk: none
source: community
date_added: '2026-03-06'
author: renat
tags:
- analytics
- product
- metrics
- posthog
- mixpanel
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# ANALYTICS-PRODUCT — 用数据做决策

## Overview

产品分析 —— PostHog、Mixpanel、事件、转化漏斗、群组、留存、北极星指标、OKR 与产品看板。适用于:配置事件追踪、创建转化漏斗、进行群组分析、留存分析、DAU/MAU、功能开关(feature flags)、A/B 测试、北极星指标、OKR、产品看板。

## When to Use This Skill

- 用于定义激活事件、调查漏斗流失,或在显式给定分母和时间窗口的情况下计算留存。
- 在埋点之前,先记录产品决策、数据来源、适用的用户同意情况、时区以及分析单位。

## Do Not Use This Skill When

- 任务与产品分析无关
- 有更简单、更专用的工具可以处理该请求
- 用户需要的是不涉及领域专长的通用协助

## How It Works

```
[对象]_[过去分词的动作]

正确示例:   user_signed_up, conversation_started, upgrade_completed
错误示例:    signup, click, conversion
```

## Analytics-Product — 用数据做决策

> "我们信赖上帝。其他人都必须拿数据来说话。"—— W. Edwards Deming

---

## 示意示例:某助手的事件

```python
AURI_EVENTS = {
    # 获客(Aquisicao)
    "user_signed_up":        {"props": ["source", "medium", "campaign"]},
    "onboarding_started":    {"props": ["step_count"]},
    "onboarding_completed":  {"props": ["time_to_complete", "steps_skipped"]},

    # 激活(Ativacao)
    "first_conversation":    {"props": ["intent", "response_time"]},
    "aha_moment_reached":    {"props": ["trigger", "session_number"]},
    "feature_discovered":    {"props": ["feature_name", "discovery_method"]},

    # 留存(Retencao)
    "conversation_started":  {"props": ["intent", "user_tier", "device"]},
    "conversation_completed":{"props": ["messages_count", "duration", "rating"]},
    "session_started":       {"props": ["days_since_last", "platform"]},

    # 营收(Receita)
    "upgrade_viewed":        {"props": ["trigger", "current_tier"]},
    "upgrade_started":       {"props": ["target_tier", "trigger"]},
    "upgrade_completed":     {"props": ["tier", "plan", "revenue"]},
    "subscription_canceled": {"props": ["reason", "tier", "tenure_days"]},
    "payment_failed":        {"props": ["attempt_count", "error_code"]},
}
```

## Posthog 实现(Python)

```python
from posthog import Posthog
import os

posthog = Posthog(
    project_api_key=os.environ["POSTHOG_API_KEY"],
    host=os.environ.get("POSTHOG_HOST", "https://app.posthog.com")
)

def track(user_id: str, event: str, properties: dict = None):
    posthog.capture(
        distinct_id=user_id,
        event=event,
        properties=properties or {}
    )

def identify(user_id: str, traits: dict):
    posthog.identify(
        distinct_id=user_id,
        properties=traits
    )

## 用法:

track("user_123", "conversation_started", {
    "intent": "business_advice",
    "device": "alexa",
    "user_tier": "pro"
})
```

---

## 示意性激活漏斗(假设数字)

```
访问落地页                    (100%)
    | [目标: 40%]
点击"试用"                     (40%)
    | [目标: 70%]
完成注册                        (28%)
    | [目标: 60%]
进行第一次对话                  (17%)  <- AHA 时刻
    | [目标: 50%]
次日回访                        (8.5%)
    | [目标: 40%]
一周内使用 3+ 天                (3.4%)
    | [目标: 20%]
转化为 Pro                      (0.7%)
```

## 优化漏斗

```
对于每一处流失率超出基准值的环节:
1. 识别:用户究竟在哪一步流失?
2. 理解:为什么?(会话录屏、问卷调查)
3. 假设:什么改动可能改善它?
4. 测试:用具有统计显著性的样本进行 A/B 测试
5. 衡量:预先确定时间窗口和样本,给出带置信区间的效应、数据质量和护栏指标
   不要因为一个有利的 p 值就提前结束;要排查 SRM(样本比例不匹配)和埋点丢失
6. 学习:即使失败了,也能更好地理解用户
```

---

## 群组分析(周留存)

```python
def calculate_cohort_retention(events_df):
    """
    events_df: DataFrame com colunas [user_id, event_date, event_name]
    (events_df:包含列 [user_id, event_date, event_name] 的 DataFrame)
    Retorna: matriz de retencao [cohort_week x week_number]
    (返回:留存矩阵 [群组周 x 周数])
    """
    import pandas as pd

    first_session = events_df[events_df.event_name == "session_started"] \
        .groupby("user_id")["event_date"].min() \
        .dt.to_period("W")

    sessions = events_df[events_df.event_name == "session_started"].copy()
    sessions["cohort"] = sessions["user_id"].map(first_session)
    sessions["weeks_since"] = (
        sessions["event_date"].dt.to_period("W") - sessions["cohort"]
    ).apply(lambda x: x.n)

    cohort_data = sessions.groupby(["cohort", "weeks_since"])["user_id"].nunique()
    cohort_sizes = cohort_data.unstack().iloc[:, 0]
    retention = cohort_data.unstack().divide(cohort_sizes, axis=0) * 100

    return retention
```

## 留存示意区间(并非市场基准)

这些数字没有来源或外部验证。仅作为格式示例使用;请替换为来自可比且成熟群组的实际观察基线。

| 周 | 区间 A | 区间 B | 区间 C | 区间 D |
|--------|---------|-----|-----|-----------|
| W1 | <20% | 20-35% | 35-50% | >50% |
| W4 | <10% | 10-20% | 20-30% | >30% |
| W8 | <5% | 5-12% | 12-20% | >20% |

---

## 北极星指标的示意假设

```
框架:
1. 什么能为用户创造真正的价值? -> 能带来洞见/行动的对话
2. 待验证的假设:每周进行 3+ 次对话的用户能获得持续性的价值
3. 如何衡量? -> "每周活跃对话用户"(Weekly Active Conversationalists, WAC)

北极星指标: WAC (Weekly Active Conversationalists)
定义: 一周内进行了 >= 3 次且每次时长 >= 2 分钟的对话的用户

第一年目标: 10,000 WAC
第二年目标: 100,000 WAC
```

## 北极星看板

草图:请根据项目情况调整 `db.query` 和 `calculate_wow_growth`。使用明确的窗口边界和统一的时区;在聚合结果中统计符合条件的用户数,而不是逐用户生成一行。

```python
def calculate_north_star(db, window_start, window_end):
    wac = db.query("""
        SELECT COUNT(*) as wac
        FROM (
            SELECT user_id
            FROM conversations
            WHERE created_at >= :window_start AND created_at < :window_end
              AND duration_seconds >= 120
            GROUP BY user_id
            HAVING COUNT(*) >= 3
        ) AS qualifying_users
    """, {"window_start": window_start, "window_end": window_end}).scalar()

    return {
        "wac": wac,
        "wow_growth": calculate_wow_growth(db, "wac"),
        "target": 10000,
        "progress": f"{wac/10000*100:.1f}%"
    }
```

---

## 使用 Posthog 的功能开关(Feature Flags)

使用所安装版本对应的 API。当前 SDK 提供 `evaluate_flags`;在旧版本中,`feature_enabled` 的参数顺序是 `(feature, user_id)`。出现错误或取不到值时,保留安全的控制流程。参见[官方 Python 文档](https://posthog.com/docs/libraries/python)。在获得授权及项目的用户同意规则确认之前,不要发送事件/识别请求。

```python
def is_feature_enabled(user_id: str, feature: str) -> bool:
    flags = posthog.evaluate_flags(user_id)
    return flags.is_enabled(feature) is True

if is_feature_enabled(user_id, "new-onboarding-v2"):
    show_new_onboarding()
else:
    show_old_onboarding()
```

## 统计显著性计算器

```python
from scipy import stats

def ab_test_significance(
    control_conversions: int,
    control_visitors: int,
    variant_conversions: int,
    variant_visitors: int,
    confidence: float = 0.95
) -> dict:
    counts = (control_conversions, control_visitors, variant_conversions, variant_visitors)
    if any(type(value) is not int or value < 0 for value in counts):
        raise ValueError("Contagens devem ser inteiros nao negativos")
        # (计数必须是非负整数)
    if not (0 < control_visitors and 0 < variant_visitors
            and control_conversions <= control_visitors
            and variant_conversions <= variant_visitors and 0 < confidence < 1):
        raise ValueError("Denominadores, conversoes ou confianca invalidos")
        # (分母、转化数或置信度无效)
    control_rate = control_conversions / control_visitors
    variant_rate = variant_conversions / variant_visitors
    lift = (variant_rate - control_rate) / control_rate * 100 if control_rate else None

    table = [
        [control_conversions, control_visitors - control_conversions],
        [variant_conversions, variant_visitors - variant_conversions]
    ]
    if any(sum(row) == 0 for row in zip(*table)):
        return {"status": "insufficient-variation", "recommendation": "No automatic decision"}
    _, p_value, _, expected = stats.chi2_contingency(table)
    if (expected < 5).any():
        return {"status": "sparse-counts", "recommendation": "Use a pre-specified exact method"}

    significant = p_value < (1 - confidence)

    return {
        "control_rate": f"{control_rate*100:.2f}%",
        "variant_rate": f"{variant_rate*100:.2f}%",
        "lift": f"{lift:+.1f}%" if lift is not None else None,
        "p_value": round(p_value, 4),
        "significant": significant,
        "absolute_difference_pp": (variant_rate - control_rate) * 100,
        "recommendation": "Review pre-specified effect, uncertainty and guardrails; no automatic deploy"
    }
```

---

## 6. 提示词建议(不会在客户端安装命令)

| 命令 | 操作 |
|---------|------|
| `/event-taxonomy` | 定义事件分类体系 |
| `/funnel-analysis` | 分析转化漏斗 |
| `/cohort-retention` | 按群组计算留存 |
| `/north-star` | 定义或审视北极星指标 |
| `/ab-test` | 计算 A/B 测试的显著性 |
| `/dashboard-setup` | 创建产品看板 |
| `/okr-template` | 产品 OKR 模板 |

## 可验证示例

合成输入:在一个封闭时间窗口内,用户 A 进行了三次 120 秒的对话,B 进行了两次,C 进行了四次 60 秒的对话。预期的 WAC 结果应为 **1**,而不是多行各为 1 的记录。在留存方面,应报告群组规模和可观测的"年龄";一个尚未结束的周不代表零留存。

对于一次实验,在计算检验之前应记录随机化单位、主要指标、时间窗口、最小效应量、停止规则和护栏指标。上面的显著性示例会拒绝无效的分母和过于稀疏的计数;它并不是一个上线决策机制。

## Limitations

- 以上目标、区间和助手事件均为假设性内容;不构成基准或用户行为的证明。
- 群组代码片段假定时间戳已经规范化且数据完整;未结束的周需要被屏蔽,没有用户的群组不应除以零。
- 单一的 p 值无法衡量产品价值,也不能消除偏差或替代置信区间与实验设计。
- SDK 可能将数据发送到外部服务。在启用追踪之前,请最小化属性、避免传输对话文本,并验证用户同意、数据驻留和保留期限。
- 数据库与界面示例依赖于项目自身的适配层;并不代表一个可直接使用的应用。
