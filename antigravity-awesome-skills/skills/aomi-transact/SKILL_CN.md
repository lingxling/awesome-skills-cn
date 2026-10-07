---
name: aomi-transact
description: "构建自然语言的加密货币/DeFi 代理和 EVM MCP 插件(Claude Code、Cursor、Codex、Gemini)。Aomi 将提示词转化为钱包签名的交易,支持 Ethereum、Base、Arbitrum、Optimism、Polygon、Linea —— 非托管、经过 fork 模拟验证。40+ 应用:Uniswap、Aave、Lido、Morpho、GMX、Hyperliquid、Polymarket。"
risk: critical
source: "aomi-labs/skills (MIT)"
source_repo: "aomi-labs/skills"
license: MIT
license_source: "https://github.com/aomi-labs/skills/blob/main/LICENSE"
date_added: "2026-05-06"
tags:
  - defi
  - wallet
  - account-abstraction
  - cli
  - eip-712
  - onchain
  - agent
  - intent
---

# Aomi Transact

> **仅限授权使用。** 此技能会代表用户签署并广播链上交易。用户必须明确请求每一个签名步骤。除非有明确的用户请求以及由 `aomi tx list` 列出的对应 `tx-N`,该技能不会运行 `aomi tx sign`。
>
> **签名门控。** 不要将 `aomi tx sign` 包含在可复制或可运行的多命令代码块中。在列出或模拟排队中的交易后停止,汇总交易 ID、链、金额、收款方、calldata 用途和模拟结果,然后请求用户给出像 `sign tx-1` 这样的明确签名指令。只有在获得那个单独的批准后才运行确切的签名命令。

## 概述

`aomi-transact` 是一套从自然语言提示词驱动 Aomi CLI([`@aomi-labs/client`](https://www.npmjs.com/package/@aomi-labs/client))的流程。用户输入类似 *"swap 1 ETH for USDC on Uniswap"* 的内容;代理选择正确的协议和合约,将 approve+swap 分阶段打包为一个批次,在一条分叉链上模拟执行,并返回一个排队中的钱包请求供用户签名。钱包只会看到已经通过模拟验证的 calldata。

该 CLI 以**账户抽象(account abstraction)优先**:默认情况下,它通过一个零配置的 Alchemy 代理进行签名(无需提供者凭据),在 Ethereum 主网上使用 EIP-7702,在 L2 上使用 ERC-4337。每次 `aomi <subcommand>` 调用都是启动、运行、退出 —— 没有长期运行的进程。

包含参考文档(`account-abstraction.md`、`apps.md`、`examples.md`、`session.md`、`troubleshooting.md`、`drain-vectors.md`)、模板(`aomi-workflow.sh`)和各主机元数据(`agents/openai.yaml`)的完整技能包存放在上游仓库 [`aomi-labs/skills`](https://github.com/aomi-labs/skills/tree/main/aomi-transact) 中。本条目只是规范的 SKILL.md —— 请克隆上游仓库以获取完整的技能包。

## 何时使用此技能

- 用户想通过终端与 Aomi 代理聊天。
- 用户想查询余额、价格、路由、报价或交易状态。
- 用户想构建、模拟、确认、签名或广播钱包请求。
- 用户想在签名前模拟一批待处理的交易。
- 用户想检查或切换应用、模型、链或会话。
- 用户想检查或更改账户抽象设置(EIP-7702 / ERC-4337)。
- 用户想签署 EIP-712 类型化数据载荷(链下协议、意图填充者)。

## 示例

### 只读——价格查询

```bash
aomi --prompt "what is the price of ETH?" --new-session
```

返回一个报价,不会排队任何钱包请求。使用 `aomi tx list` 确认没有待处理的内容。

### 单笔交易流程——Lido 质押

```bash
aomi chat "Stake 0.01 ETH with Lido to get stETH" \
  --public-key 0xUserAddress --chain 1 --new-session
aomi tx list
```

在 Lido stETH `0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84` 上调用 `submit(address(0))`,`value = 0.01 ETH`。无需 approve,单笔交易。到此停止,展示排队中的交易详情,并等待用户明确的签名指令。

### 多步骤批次——Uniswap V3 兑换

```bash
aomi chat "swap 1 USDC for WETH on Uniswap V3, send to my wallet" \
  --public-key 0xUserAddress --chain 1 --new-session
aomi tx list                        # tx-1 = approve, tx-2 = swap
aomi tx simulate tx-1 tx-2          # 多步骤时必须执行
```

模拟器会在一条分叉链上依次运行每笔交易,以便 swap 步骤能看到 approve 带来的状态变化。不要单独签名第 2 步 —— 那会导致回滚。在模拟后停止,汇总该批次,并等待用户明确指出两个交易 ID 的签名指令。

### 跨链——通过 CCTP 从 Ethereum 到 Base

```bash
aomi chat "Bridge 50 USDC from Ethereum to Base via CCTP. Recipient is my wallet." \
  --public-key 0xUserAddress --chain 1 --new-session
aomi tx list
aomi tx simulate tx-1 tx-2
```

在模拟后停止,等待用户明确批准签名指定的交易 ID。签名之后,来源链上的销毁(burn)会在 1-2 个区块内确认;目标链的铸造(mint)需要 Circle 的链下证明(约 13-19 分钟)。

## 限制

- **需要 `@aomi-labs/client` v0.1.30 或更新版本。** 旧版本缺少 `--aa`、`--aa-provider`、`--aa-mode` 和模拟门控。使用 `npm install -g @aomi-labs/client` 安装,或按需通过 `npx @aomi-labs/client@0.1.30 ...` 运行。
- **需要活跃的后端连接。** 此技能驱动的 CLI 会与 `api.aomi.dev` 通信。没有网络访问时,只有本地只读命令(`aomi tx list`、`aomi session log`)可用。
- **L2 上的账户抽象赞助不保证可用。** 在 v0.1.30 中,零配置代理路径在 Base/Arbitrum/Optimism 上不能可靠地赞助 gas。如果 EOA 在目标链上没有原生 gas,`aomi tx sign` 会返回 viem 的 `insufficient funds for transfer`(gas 不足)错误。要么给 EOA 充入少量原生 gas,要么配置一个带有赞助策略的真实 BYOK Alchemy/Pimlico 提供者。不要用 `--eoa` 重试 —— 那条路径同样需要 gas。
- **按会话摄取密钥。** 需要提供者 token 的应用(`binance`、`polymarket`、`dune` 等)必须由用户在自己的 shell 中或通过 `aomi secret add NAME=<value>` 自行配置凭据。该技能绝不会主动自行设置凭据。
- **资金转移向量会被防护拦截。** 代理会拒绝 `recipient`/`onBehalfOf`/`mintRecipient` 不等于 `msg.sender` 的 calldata。这是一项安全功能,不是缺陷 —— 应向用户展示该阻断,而不是重新组织提示词绕过它。
- **网络/RPC 故障。** 公共 RPC 可能会限流(`429`)或鉴权失败(`401`)。生产环境签名时,用户必须提供一个可靠且与链匹配的 RPC,通过 `--rpc-url` 传入。
- **实时交易上的滑点和截止时间。** 带截止时间的路由(Across、Khalani fillers)给出的报价可能在用户审查期间过期;代理会通过用新的截止时间重新构建来自我修复,但用户应重新检查 `aomi tx list` 以获取最新通过的批次。

## 最佳实践

- **在新任务的第一个命令上默认使用 `--new-session`。** 在任务进行中复用它会开启一段新对话,代理会丢失刚给出的报价。
- **始终在 `aomi tx sign` 之前运行 `aomi tx list`。** 绝不要假设某次聊天回复已经排队了一笔交易。
- **在签名多步骤批次之前始终运行 `aomi tx simulate tx-1 tx-2 ...`。** 单笔交易流程的模拟是可选的,但进行模拟永远不会是错的。
- **将签名命令排除在可运行示例之外。** 只有在用户给出单独的、明确指出确切排队中 `tx-N` ID 的批准之后,才展示或运行 `aomi tx sign`。
- **只签名 `Batch [...] passed` 的交易。** 跳过来自先前失败尝试的孤立交易(`failed at step N: 0x...`)。
- **将 `--rpc-url` 与排队交易的链匹配**,而不是会话链(`--chain`)——它们是相互独立的控制项。
- **绝不要回显凭据值。** 该技能只用用户名或推导出的地址来确认凭据设置成功。

## 授权声明

此技能能够签署并广播价值真实的链上交易。请仅在你拥有且信任的账户和网络上使用。该技能不托管资金;用户通过 `--public-key` 和底层钱包始终保有签名密钥的完全控制权。在运行 `aomi tx sign` 之前请审查每一笔排队中的 `tx-N`。

## 来源

- **上游**:[aomi-labs/skills](https://github.com/aomi-labs/skills) —— MIT 许可
- **作者**:[Aomi Labs](https://aomi.dev)
- **CLI**:npm 上的 [`@aomi-labs/client`](https://www.npmjs.com/package/@aomi-labs/client)
- **安全审查**:[aomi-transact/SECURITY.md](https://github.com/aomi-labs/skills/blob/main/aomi-transact/SECURITY.md) —— OWASP AST01–AST10 走查以及已捕获的扫描器报告

## 补充资源

如需完整技能包,包括各流程示例(CCTP 桥接、Aave 存入、Lido 质押、Uniswap 兑换)、账户抽象模式参考、资金转移向量表、故障排除指南和 bash 工作流模板,请参阅上游仓库:

- [账户抽象参考](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/account-abstraction.md)
- [应用目录(25+ 应用)](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/apps.md)
- [流程示例](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/examples.md)
- [资金转移向量参考](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/drain-vectors.md)
- [故障排除](https://github.com/aomi-labs/skills/blob/main/aomi-transact/references/troubleshooting.md)
- [aomi-workflow.sh 模板](https://github.com/aomi-labs/skills/blob/main/aomi-transact/templates/aomi-workflow.sh)
