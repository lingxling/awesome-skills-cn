---
name: conductor-setup
description: 配置 Rails 项目以使用 Conductor（平行编码代理）
allowed-tools: Bash(chmod *), Bash(bundle *), Bash(npm *), Bash(script/server)
context: fork
risk: critical
source: community
date_added: "2026-09-04"
metadata:
  author: Shpigford
  version: "1.0"
---

为 Conductor（Mac 应用程序用于平行编码代理）设置此 Rails 项目。

## 何时使用
- 您需要配置 Rails 项目，使其在 Conductor 工作区内正确运行。
- 该项目应支持具有隔离端口、Redis 设置和共享密钥的平行编码代理。
- 您希望为 Rails 存储库获得标准的 `conductor.json`、`bin/conductor-setup` 和 `script/server` 脚手架。

# 需要创建的内容

## 1. conductor.json（项目根目录）

在项目根目录创建 `conductor.json`（如果尚不存在）：

```json
{
  "scripts": {
    "setup": "bin/conductor-setup",
    "run": "script/server"
  }
}
```

## 2. bin/conductor-setup（可执行文件）

创建 `bin/conductor-setup`（如果尚不存在）：

```bash
#!/bin/bash
set -e

# 从存储库根目录链接 .env（秘密所在的地方，在工作树外）
[ -f "$CONDUCTOR_ROOT_PATH/.env" ] && ln -sf "$CONDUCTOR_ROOT_PATH/.env" .env

# 链接 Rails 主密钥
[ -f "$CONDUCTOR_ROOT_PATH/config/master.key" ] && ln -sf "$CONDUCTOR_ROOT_PATH/config/master.key" config/master.key

# 安装依赖项
bundle install
npm install
```

使用 `chmod +x bin/conductor-setup` 使其可执行。

## 3. script/server（可执行文件）

创建 `script` 目录（如果需要），然后创建 `script/server`（如果尚不存在）：

```bash
#!/bin/bash

# === 端口配置 ===
export PORT=${CONDUCTOR_PORT:-3000}
export VITE_RUBY_PORT=$((PORT + 1000))

# === Redis 隔离 ===
if [ -n "$CONDUCTOR_WORKSPACE_NAME" ]; then
  HASH=$(printf '%s' "$CONDUCTOR_WORKSPACE_NAME" | cksum | cut -d' ' -f1)
  REDIS_DB=$((HASH % 16))
  export REDIS_URL="redis://localhost:6379/${REDIS_DB}"
fi

exec bin/dev
```

使用 `chmod +x script/server` 使其可执行。

## 4. 更新 Rails 配置文件

对于以下每个文件，如果存在并包含 Redis 配置，请更新它们以使用 `ENV.fetch('REDIS_URL', ...)` 或 `ENV['REDIS_URL']` 及备用选项：

### config/initializers/sidekiq.rb
如果此文件存在并配置 Redis，请更新它以使用：
```ruby
redis_url = ENV.fetch('REDIS_URL', 'redis://localhost:6379/0')
```

### config/cable.yml
如果此文件存在，请将开发适配器更新为：
```yaml
development:
  adapter: redis
  url: <%= ENV.fetch('REDIS_URL', 'redis://localhost:6379/1') %>
```

### config/environments/development.rb
如果此文件为缓存配置 Redis，请更新为：
```ruby
config.cache_store = :redis_cache_store, { url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/0') }
```

### config/initializers/rack_attack.rb
如果此文件存在并配置 Redis 缓存存储，请更新为：
```ruby
Rack::Attack.cache.store = ActiveSupport::Cache::RedisCacheStore.new(url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/0'))
```

# 实现注意事项

- **不要覆盖现有文件**：在创建 conductor.json、bin/conductor-setup 和 script/server 之前检查它们是否存在。如果存在，跳过创建并告知用户。
- **Rails 配置更新**：仅修改与 Redis 相关的配置。如果文件不存在或不使用 Redis，请妥善跳过。
- **根据需要创建目录**：如果 `script/` 目录不存在，请创建它。

# 验证

创建文件后：
1. 确认所有 Conductor 文件存在且脚本可执行
2. 运行 `script/server` 以验证它启动时没有错误
3. 检查 Rails 配置是否正确引用 `ENV['REDIS_URL']` 或 `ENV.fetch('REDIS_URL', ...)`

## 限制
- 仅在任务清楚地符合上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
