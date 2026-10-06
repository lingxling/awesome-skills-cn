---
name: openclaw-local-mac-mini
description: Set up OpenClaw locally and run it reliably on a Mac mini for private,
  always-on local agent workflows.
category: devops
risk: critical
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: Requires the relevant OS/platform tooling and privileged access where
  noted. Docs-only; helper scripts and templates not bundled.
metadata:
  author: devops-skills
  version: '1.0'
---

# OpenClaw Local + Mac mini Setup

Use this skill when you want to run [OpenClaw](https://github.com/openclaw/openclaw) on a developer laptop or promote it to a stable Mac mini host. Covers cloning and bootstrapping, Docker Compose configuration, Mac mini hardware optimization, networking, monitoring, and production-grade launchd services.

## Prerequisites

- macOS 13 (Ventura) or later on Apple Silicon (M1/M2/M4 Mac mini recommended)
- Docker Desktop for Mac or OrbStack installed
- Git, Node.js (v18+), and a package manager (npm or pnpm)
- API keys for your chosen LLM provider (OpenAI, Anthropic, or local Ollama)
- At least 16 GB RAM (32 GB recommended for local model serving)

## Local Setup (Any Dev Machine)

### Clone and Bootstrap

```bash
# Clone the repository
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Review the upstream README for current prerequisites
cat README.md

# Copy the example environment file
cp .env.example .env

# Edit .env with your provider keys and configuration
# At minimum, set the model provider and API key
cat > .env << 'ENV'
# LLM Provider Configuration
OPENAI_API_KEY=sk-your-openai-key-here
# Or for Anthropic:
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# Or for local Ollama:
# OLLAMA_BASE_URL=http://localhost:11434

# Application settings
NODE_ENV=development
PORT=3000
HOST=0.0.0.0
LOG_LEVEL=info

# Database (if applicable)
DATABASE_URL=sqlite:./data/openclaw.db
ENV
```

### Install Dependencies and Run

```bash
# Install dependencies
npm install
# Or with pnpm:
# pnpm install

# Run database migrations if needed
npm run db:migrate

# Start the development server
npm run dev

# Verify startup
curl -s http://localhost:3000/api/health | jq .
# Expected: {"status":"ok","version":"..."}
```

### Validate the Setup

```bash
# Check the API health endpoint
curl -f http://localhost:3000/api/health

# Check the UI loads
curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/
# Expected: 200

# Run built-in tests if available
npm test
```

## Docker Compose Setup

### docker-compose.yml

```yaml
version: "3.8"

services:
  openclaw:
    build:
      context: .
      dockerfile: Dockerfile
    image: openclaw:latest
    container_name: openclaw
    restart: unless-stopped
    ports:
      - "3000:3000"
    env_file:
      - .env
    environment:
      - NODE_ENV=production
      - HOST=0.0.0.0
      - PORT=3000
    volumes:
      - openclaw-data:/app/data
      - ./config:/app/config:ro
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 1G
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "5"

  # Optional: Redis for caching/queues
  redis:
    image: redis:7-alpine
    container_name: openclaw-redis
    restart: unless-stopped
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  # Optional: Ollama for local model serving
  ollama:
    image: ollama/ollama:latest
    container_name: openclaw-ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama-models:/root/.ollama
    deploy:
      resources:
        limits:
          memory: 16G
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  openclaw-data:
  redis-data:
  ollama-models:
```

### Running with Docker Compose

```bash
# Build and start all services
docker compose up -d --build

# Check service status
docker compose ps

# View logs
docker compose logs -f openclaw
docker compose logs -f --tail=100 ollama

# Pull a model into Ollama (if using local models)
docker exec openclaw-ollama ollama pull llama3:8b
docker exec openclaw-ollama ollama list

# Restart a single service
docker compose restart openclaw

# Stop everything
docker compose down

# Stop and remove volumes (full reset)
docker compose down -v
```

## Mac mini Production Setup

### macOS Hardening and Baseline

```bash
# Enable automatic security updates
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled -bool true
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload -bool true
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate CriticalUpdateInstall -bool true

# Enable FileVault disk encryption
sudo fdesetup enable

# Disable sleep (headless server should never sleep)
sudo pmset -a sleep 0
sudo pmset -a disksleep 0
sudo pmset -a displaysleep 0

# Enable auto-restart after power failure
sudo pmset -a autorestart 1

# Disable screen saver
defaults -currentHost write com.apple.screensaver idleTime 0

# Set hostname
sudo scutil --set ComputerName "openclaw-mini"
sudo scutil --set HostName "openclaw-mini"
sudo scutil --set LocalHostName "openclaw-mini"

# Verify power settings
pmset -g
```

### Dedicated User Account

```bash
# Create a dedicated service user
sudo sysadminctl -addUser openclaw -fullName "OpenClaw Service" -password "temp-change-me" -admin

# Switch to the service user for setup
su - openclaw

# Clone and configure OpenClaw in the user's home
cd ~
git clone https://github.com/openclaw/openclaw.git
cd openclaw
cp .env.example .env
# Edit .env with production values
```

### Secrets Management

```bash
# Store API keys in macOS Keychain instead of plaintext .env
security add-generic-password -a openclaw -s "OPENAI_API_KEY" -w "sk-your-key-here"
security add-generic-password -a openclaw -s "ANTHROPIC_API_KEY" -w "sk-ant-your-key-here"

# Retrieve a secret from Keychain in scripts
OPENAI_API_KEY=$(security find-generic-password -a openclaw -s "OPENAI_API_KEY" -w)
export OPENAI_API_KEY

# Helper script to load secrets from Keychain
cat > /Users/openclaw/openclaw/load-secrets.sh << 'SCRIPT'
#!/usr/bin/env bash
export OPENAI_API_KEY=$(security find-generic-password -a openclaw -s "OPENAI_API_KEY" -w 2>/dev/null)
export ANTHROPIC_API_KEY=$(security find-generic-password -a openclaw -s "ANTHROPIC_API_KEY" -w 2>/dev/null)
SCRIPT
chmod 700 /Users/openclaw/openclaw/load-secrets.sh
```

### launchd Service Configuration

```xml
<!-- /Library/LaunchDaemons/com.openclaw.service.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.service</string>

    <key>UserName</key>
    <string>openclaw</string>

    <key>WorkingDirectory</key>
    <string>/Users/openclaw/openclaw</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>source ./load-secrets.sh && /usr/local/bin/node ./dist/server.js</string>
    </array>

    <key>EnvironmentVariables</key>
    <dict>
        <key>NODE_ENV</key>
        <string>production</string>
        <key>PORT</key>
        <string>3000</string>
        <key>HOST</key>
        <string>0.0.0.0</string>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>

    <key>ThrottleInterval</key>
    <integer>10</integer>

    <key>StandardOutPath</key>
    <string>/var/log/openclaw/stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/var/log/openclaw/stderr.log</string>

    <key>SoftResourceLimits</key>
    <dict>
        <key>NumberOfFiles</key>
        <integer>65536</integer>
    </dict>
</dict>
</plist>
```

```bash
# Create log directory
sudo mkdir -p /var/log/openclaw
sudo chown openclaw:staff /var/log/openclaw

# Load the service
sudo launchctl load -w /Library/LaunchDaemons/com.openclaw.service.plist

# Verify it is running
sudo launchctl list | grep openclaw
curl -f http://localhost:3000/api/health

# Stop/start/restart the service
sudo launchctl stop com.openclaw.service
sudo launchctl start com.openclaw.service

# Unload the service (disable)
sudo launchctl unload /Library/LaunchDaemons/com.openclaw.service.plist

# View logs
tail -f /var/log/openclaw/stdout.log
tail -f /var/log/openclaw/stderr.log
```

### Docker Compose via launchd

```xml
<!-- /Library/LaunchDaemons/com.openclaw.docker.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.docker</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/docker</string>
        <string>compose</string>
        <string>-f</string>
        <string>/Users/openclaw/openclaw/docker-compose.yml</string>
        <string>up</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/var/log/openclaw/docker-stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/var/log/openclaw/docker-stderr.log</string>
</dict>
</plist>
```


## Contents

- [Networking](references/details.md)
- [Monitoring](references/details.md)
- [Validation Checklist](references/details.md)
- [Troubleshooting](references/details.md)
- [Related Skills](references/details.md)

## When to Use

- Running OpenClaw as a private, always-on local AI agent
- Setting up a dedicated Mac mini as a home-lab AI server
- Deploying OpenClaw with Docker Compose for reproducible environments
- Optimizing macOS for headless server operation
- Monitoring a local AI service for uptime and performance

## Limitations

- Infrastructure commands can disrupt services: confirm target host/scope and have backups/snapshots before mutating state.
- Docs-only import: upstream scripts and templates not bundled.

