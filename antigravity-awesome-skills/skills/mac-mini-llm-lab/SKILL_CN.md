---
name: mac-mini-llm-lab
description: 将 Mac mini 配置为具有远程访问、可观察性和电源安全操作的可靠本地 LLM
  服务器。在 Apple Silicon 上构建始终在线的私有 AI 推理服务器时使用。
category: devops
risk: critical
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: 需要相关的 OS/平台工具和注明的特权访问。仅文档；未捆绑辅助脚本和模板。
metadata:
  author: devops-skills
  version: '1.0'
---

# Mac mini LLM 实验室

将 Mac mini 转变为低噪声、始终在线的本地 AI 设备。

## 何时使用此技能

当以下情况时使用此技能：
- 建立专用的本地 LLM 推理服务器
- 构建私有 AI 开发环境
- 需要始终在线的模型服务，无需云成本
- 运行需要 Apple Silicon 统一内存的模型 (32-192GB)
- 为小团队创建家庭实验室 AI 服务器

## 前置条件

- 带有 Apple Silicon 的 Mac mini (M2/M3/M4，建议 16GB+ 统一内存)
- macOS Sonoma 14+ 或 Sequoia 15+
- 以太网连接（建议而不是 Wi-Fi）
- UPS 电源保护（可选但推荐）

## 初始系统设置

```bash
# 更新 macOS
softwareupdate --install --all

# 安装 Xcode 命令行工具
xcode-select --install

# 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 核心包
brew install tmux htop btop wget jq git neovim

# Python 环境 (用于 MLX 和自定义脚本)
brew install python@3.12 uv

# 监控
brew install prometheus node_exporter
```

## Ollama 设置

```bash
# 安装 Ollama
brew install ollama

# 根据您的 RAM 拉取模型
# 16GB Mac mini:
ollama pull llama3.1:8b
ollama pull nomic-embed-text
ollama pull codellama:7b

# 32GB Mac mini:
ollama pull llama3.1:8b
ollama pull qwen2.5:14b
ollama pull deepseek-coder-v2:16b
ollama pull nomic-embed-text

# 64GB+ Mac mini:
ollama pull llama3.1:70b
ollama pull qwen2.5:32b
ollama pull codellama:34b

# 验证 Metal 加速
ollama run llama3.1:8b --verbose
# 查找输出中的 "metal"
```

## MLX 框架 (Apple Silicon 原生)

MLX 在 Apple Silicon 上以出色的性能原生运行模型：

```bash
# 安装 MLX
uv pip install mlx mlx-lm

# 运行模型
python3 -c "
from mlx_lm import load, generate
model, tokenizer = load('mlx-community/Llama-3.1-8B-Instruct-4bit')
response = generate(model, tokenizer, prompt='Explain Docker in 3 sentences', max_tokens=200)
print(response)
"

# MLX 服务器 (OpenAI 兼容 API)
uv pip install mlx-lm[server]
mlx_lm.server --model mlx-community/Llama-3.1-8B-Instruct-4bit --port 8080
```

## 使用 launchd 自动启动

```xml
<!-- ~/Library/LaunchAgents/com.ollama.serve.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ollama.serve</string>
    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OLLAMA_HOST</key>
        <string>0.0.0.0</string>
        <key>OLLAMA_NUM_PARALLEL</key>
        <string>4</string>
        <key>OLLAMA_MAX_LOADED_MODELS</key>
        <string>2</string>
        <key>OLLAMA_FLASH_ATTENTION</key>
        <string>1</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ollama.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ollama.err</string>
</dict>
</plist>
```

```bash
# 加载服务
launchctl load ~/Library/LaunchAgents/com.ollama.serve.plist

# 检查状态
launchctl list | grep ollama

# 如果需要卸载
launchctl unload ~/Library/LaunchAgents/com.ollama.serve.plist
```

## 电源和可靠性

```bash
# 防止睡眠 (在 Mac mini 合盖时保持运行)
sudo pmset -a disablesleep 1
sudo pmset -a sleep 0

# 电源故障后自动重启
sudo pmset -a autorestart 1

# 计划周周期重启 (周日凌晨 4 点)
sudo pmset repeat shutdown MTWRFSU 03:55:00
sudo pmset repeat poweron MTWRFSU 04:00:00

# 检查电源设置
pmset -g
```

## 远程访问

### Tailscale (推荐)

```bash
# 安装 Tailscale 以便轻松安全的远程访问
brew install --cask tailscale

# 从菜单栏启用、验证
# 从任何地方访问您的 Mac mini: http://mac-mini:11434
```

### SSH 强化

```bash
# 启用远程登录
sudo systemsetup -setremotelogin on

# 编辑 SSH 配置
sudo nano /etc/ssh/sshd_config
# 添加:
# PasswordAuthentication no
# PubkeyAuthentication yes
# PermitRootLogin no
# AllowUsers yourusername

# 重启 SSH
sudo launchctl unload /System/Library/LaunchDaemons/ssh.plist
sudo launchctl load /System/Library/LaunchDaemons/ssh.plist
```

### 使用 Caddy 反向代理

```bash
brew install caddy

# Caddyfile
cat > /opt/homebrew/etc/Caddyfile << 'EOF'
llm.local:443 {
    tls internal
    reverse_proxy localhost:11434

    @api path /v1/*
    handle @api {
        reverse_proxy localhost:11434
    }
}

webui.local:443 {
    tls internal
    reverse_proxy localhost:3000
}
EOF

brew services start caddy
```

## Open WebUI 设置

```bash
# 通过 Docker 运行 Open WebUI
docker run -d \
  --name open-webui \
  -p 3000:8080 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e WEBUI_AUTH=true \
  -v open-webui:/app/backend/data \
  --restart unless-stopped \
  ghcr.io/open-webui/open-webui:main

# 或者先安装 Docker（如果不可用）
brew install --cask docker
```

## 监控

```bash
# 健康检查脚本
cat > ~/scripts/llm-health.sh << 'SCRIPT'
#!/bin/bash
# 检查 Ollama
if curl -sf http://localhost:11434/api/tags > /dev/null; then
    echo "$(date): Ollama OK"
    curl -s http://localhost:11434/api/ps | python3 -m json.tool
else
    echo "$(date): Ollama DOWN"
    # 重启
    launchctl kickstart -k gui/$(id -u)/com.ollama.serve
fi

# 系统统计
echo "CPU: $(top -l 1 -n 0 | grep 'CPU usage')"
echo "Memory: $(vm_stat | head -5)"
echo "Disk: $(df -h / | tail -1)"
echo "Thermal: $(sudo powermetrics --samplers smc -n 1 2>/dev/null | grep 'CPU die' || echo 'N/A')"
SCRIPT
chmod +x ~/scripts/llm-health.sh

# 每 5 分钟安排一次健康检查
# 添加到 crontab: crontab -e
# */5 * * * * ~/scripts/llm-health.sh >> ~/logs/llm-health.log 2>&1
```

### 按模型的内存使用

| 模型 | 所需 RAM | 令牌/秒 (M2) | 令牌/秒 (M4) |
|-------|-------------|-----------------|-----------------|
| llama3.1:8b (Q4) | ~5 GB | ~25 t/s | ~45 t/s |
| qwen2.5:14b (Q4) | ~9 GB | ~15 t/s | ~30 t/s |
| llama3.1:70b (Q4) | ~40 GB | ~5 t/s | ~10 t/s |
| nomic-embed-text | ~300 MB | N/A | N/A |
| codellama:13b | ~8 GB | ~18 t/s | ~35 t/s |

## 安全检查表

```bash
# 启用 FileVault 磁盘加密
sudo fdesetup enable

# 启用防火墙
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on

# 禁用不必要的共享服务
sudo launchctl disable system/com.apple.screensharing
sudo launchctl disable system/com.apple.AirPlayXPCHelper

# 设置强管理员密码
# 系统设置 > 用户和组

# 将 Ollama 限制为仅本地网络 (如果不使用 Tailscale)
# 在 launchd plist 中设置 OLLAMA_HOST=127.0.0.1
```

## 性能调优

```bash
# 增加文件描述符限制以处理并发请求
sudo launchctl limit maxfiles 65536 200000

# 检查统一内存压力
memory_pressure

# 监控 GPU 使用量 (Metal)
sudo powermetrics --samplers gpu_power -n 1

# 针对推理进行优化 (禁用模型目录上的 Spotlight 索引)
mdutil -i off ~/.ollama
```

## 故障排除

| 问题 | 解决方案 |
|-------|---------|
| 模型加载缓慢 | 第一次加载缓存到内存；后续加载很快 |
| 内存不足 | 使用更小的量化 (Q4_K_M)，减少 `OLLAMA_MAX_LOADED_MODELS` |
| Mac 睡眠 | 运行 `sudo pmset -a disablesleep 1` |
| Ollama 无法启动 | 检查 `launchctl list | grep ollama`，查看 `/tmp/ollama.err` |
| Wi-Fi 上速度缓慢 | 使用以太网；Wi-Fi 会为流式响应添加延迟 |
| 热节流 | 确保通风充足，检查 `powermetrics` |

## 相关技能

- ollama-stack (`ollama-stack`) — 具有 Docker Compose 和 LiteLLM 的软件堆栈
- ssh-configuration (`ssh-configuration`) — 安全远程访问
- vpn-setup (`vpn-setup`) — 通过 WireGuard/Tailscale 的远程访问

## 限制

- 基础设施命令可能会中断服务：在变更状态前确认目标主机/范围并进行备份/快照。
- 仅文档导入：上游脚本和模板未捆绑。
