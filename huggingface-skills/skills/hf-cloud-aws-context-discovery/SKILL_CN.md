---
name: hf-cloud-aws-context-discovery
description: 在开始任何 AWS 任务之初，先发现用户本地的 AWS 上下文（激活的 profile、区域、账户 ID、调用者身份）。在进行任何其他 AWS 工作之前使用此技能——部署到 SageMaker、创建资源、调用 AWS API，或任何涉及 AWS 账户的操作。尤其是在用户没有明确指定区域或 profile 时使用，比如当他们说"用我的 AWS 账户"、"部署到 AWS"、"用我的 profile"，或者即将发起任何 AWS CLI 或 SDK 调用时。永远不要猜测区域或账户 ID——始终先用此技能从本地配置中读取。
---

# AWS 上下文发现

在进行任何 AWS 工作之前，先读取用户本地的 AWS 配置。不要猜测区域，也不要向用户询问他们的配置已经能回答的问题。

## 要发现什么

在 AWS 工作开始时运行以下步骤，并在本次会话的剩余时间里记住这些结果。

### 1. 激活的 profile

`AWS_PROFILE` 环境变量，否则为 `default`。如果用户在提示中提到了某个 profile，以此为准。如果指定的 profile 在 `~/.aws/config` 中不存在，要清楚地指出这一点。

### 2. 区域

解析顺序——在第一个能得出结果的地方停下：
1. 用户在本次对话中明确指定的区域
2. `AWS_REGION` 环境变量
3. `AWS_DEFAULT_REGION` 环境变量
4. `~/.aws/config` 中激活 profile 上的 `region` 字段
5. 询问用户——但只有在前四项都失败之后才这样做

不要回退使用 `us-east-1` 或任何其他硬编码的默认值。

### 3. 凭据、账户 ID、调用者 ARN

```bash
aws sts get-caller-identity --profile <profile> --region <region>
```

一次调用，三个目的：确认凭据有效（如果无效则停止）；返回构造 ARN 所需的 `Account` ID；返回调用者的 `Arn`。

### 4. 识别 SSO / 假设角色（assumed-role）主体

`Arn` 字段告诉你这是哪种类型的主体。这个模式很重要，因为它决定了调用者能执行哪些 IAM 操作。

| ARN 模式 | 类型 | IAM 写入能力 |
|---|---|---|
| `arn:aws:iam::<acct>:user/<name>` | IAM 用户 | 取决于所附加的策略 |
| `arn:aws:sts::<acct>:assumed-role/AWSReservedSSO_<...>/<email>` | **SSO 假设角色** | 通常**没有**——无法创建/修改 IAM 角色 |
| `arn:aws:sts::<acct>:assumed-role/<role>/<session>` | 常规假设角色 | 取决于该角色 |

**如果调用者是 SSO**，要立即指出这一点，以免后续技能撞上 `iam:CreateRole` 并失败：

> 提示一下：你是通过 SSO 认证的（`AWSReservedSSO_<PermissionSet>_...`）。SSO 主体通常无法直接创建 IAM 角色。如果我们需要一个 SageMaker 执行角色，我会先查找是否有现成的——如果没有，你需要请负责管理你 AWS 权限的人创建一个。

这是此技能发挥最大作用的地方。现在就把这一点指出来，能把一个让人困惑的、部署中途才出现的错误，变成一次五秒钟的对话。

## 要运行的命令

```bash
# 有效的 profile 和区域（比解析配置文件更快）
aws configure list

# 验证凭据并获取身份信息
aws sts get-caller-identity
aws sts get-caller-identity --profile <profile-name>  # 如果指定了 profile
```

`aws configure list` 会处理环境变量的覆盖，并显示解析后的有效值。优先使用它，而不是自己去解析 `~/.aws/config`。如果你需要读取原始配置（例如列出所有 profile），`~/.aws/config` 和 `~/.aws/credentials` 是纯文本的 INI 文件——只读即可。

## 要反馈什么

一两行就好，不要写一大段：

> 正在使用 profile `my-profile`，区域 `eu-west-1`，账户 `123456789012`。你是通过 SSO 认证的，所以我们需要使用现有的 IAM 角色，而不能创建新的。

不要让用户去确认你刚从他们配置中读到的区域——他们配置了它，那本身就是确认。

如果出了问题（凭据过期、profile 不存在、哪里都找不到区域），停下来，把具体的错误清楚地呈现出来，再继续。
