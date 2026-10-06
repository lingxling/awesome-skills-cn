# Details (moved from SKILL.md)

> Extended reference content for `openclaw-local-mac-mini`, kept under `references/` so the entrypoint stays within the audit budget.

## Networking

### Tailscale for Secure Remote Access

```bash
# Install Tailscale on the Mac mini
brew install --cask tailscale

# Authenticate and connect
open /Applications/Tailscale.app
# Or via CLI:
tailscale up --authkey tskey-auth-your-key-here

# Verify Tailscale IP
tailscale ip -4
# e.g., 100.64.x.x

# Access OpenClaw from any Tailscale device
curl http://100.64.x.x:3000/api/health

# Enable MagicDNS for friendly names
# Access via: http://openclaw-mini:3000
```

### Nginx Reverse Proxy (Optional)

```bash
# Install nginx via Homebrew
brew install nginx

# Configure reverse proxy
cat > /opt/homebrew/etc/nginx/servers/openclaw.conf << 'NGINX'
server {
    listen 80;
    server_name openclaw-mini openclaw-mini.local;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }

    # Rate limiting for API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINX

# Test and reload nginx
nginx -t
brew services restart nginx
```

### macOS Firewall

```bash
# Enable the application firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on

# Allow specific apps
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/node
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /opt/homebrew/bin/nginx

# Block all incoming except allowed
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setblockall on

# Verify
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```


## Monitoring

### Health Check Script

```bash
#!/usr/bin/env bash
# /Users/openclaw/openclaw/healthcheck.sh
set -euo pipefail

ENDPOINT="http://localhost:3000/api/health"
LOGFILE="/var/log/openclaw/healthcheck.log"
ALERT_EMAIL="admin@example.com"
MAX_FAILURES=3
FAILURE_COUNT_FILE="/tmp/openclaw-failures"

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

# Initialize failure counter
if [ ! -f "$FAILURE_COUNT_FILE" ]; then
  echo 0 > "$FAILURE_COUNT_FILE"
fi

if curl -sf --max-time 10 "$ENDPOINT" > /dev/null 2>&1; then
  echo "$(timestamp) OK" >> "$LOGFILE"
  echo 0 > "$FAILURE_COUNT_FILE"
else
  FAILURES=$(cat "$FAILURE_COUNT_FILE")
  FAILURES=$((FAILURES + 1))
  echo "$FAILURES" > "$FAILURE_COUNT_FILE"
  echo "$(timestamp) FAIL (count: $FAILURES)" >> "$LOGFILE"

  if [ "$FAILURES" -ge "$MAX_FAILURES" ]; then
    echo "$(timestamp) ALERT: OpenClaw down for $FAILURES checks" >> "$LOGFILE"
    # Attempt restart
    sudo launchctl stop com.openclaw.service
    sleep 2
    sudo launchctl start com.openclaw.service
    echo "$(timestamp) Service restarted" >> "$LOGFILE"
    echo 0 > "$FAILURE_COUNT_FILE"
  fi
fi
```

```bash
# Schedule health checks every 5 minutes via cron
crontab -e
# Add:
# */5 * * * * /Users/openclaw/openclaw/healthcheck.sh
```

### Resource Monitoring

```bash
# Monitor CPU and memory usage of OpenClaw
ps aux | grep -E 'node|docker' | grep -v grep

# Continuous monitoring with top (non-interactive)
top -l 1 -s 0 | grep -E 'node|docker'

# Disk usage check
df -h /Users/openclaw
du -sh /Users/openclaw/openclaw/data/

# Docker resource usage
docker stats --no-stream openclaw openclaw-redis openclaw-ollama

# macOS Activity Monitor from CLI
sudo powermetrics --samplers cpu_power,gpu_power -n 1
```

### Log Rotation

```bash
# /etc/newsyslog.d/openclaw.conf
# logfilename                        [owner:group]  mode  count  size  when  flags  [/pid_file]  [sig_num]
/var/log/openclaw/stdout.log         openclaw:staff  644   10     5120  *     JN
/var/log/openclaw/stderr.log         openclaw:staff  644   10     5120  *     JN
/var/log/openclaw/healthcheck.log    openclaw:staff  644   10     1024  *     JN
```

```bash
# Force log rotation
sudo newsyslog -F

# Or use a simple cron-based rotation
cat > /Users/openclaw/rotate-logs.sh << 'ROTATE'
#!/usr/bin/env bash
LOGDIR="/var/log/openclaw"
for log in "$LOGDIR"/*.log; do
  if [ -f "$log" ] && [ "$(stat -f%z "$log")" -gt 52428800 ]; then
    mv "$log" "${log}.$(date +%Y%m%d%H%M%S)"
    gzip "${log}."*
    touch "$log"
  fi
done
# Keep only last 10 rotated logs
ls -t "$LOGDIR"/*.gz 2>/dev/null | tail -n +11 | xargs rm -f
ROTATE
chmod +x /Users/openclaw/rotate-logs.sh
```


## Validation Checklist

- App starts after reboot without manual intervention (`launchctl list | grep openclaw`)
- Health check succeeds from local network (`curl -f http://<ip>:3000/api/health`)
- Health check succeeds via Tailscale (`curl -f http://100.64.x.x:3000/api/health`)
- Secrets are not committed and not world-readable (`ls -la .env`, check `.gitignore`)
- Access to admin interfaces is restricted to trusted users/devices
- Docker volumes persist across container restarts (`docker compose down && docker compose up -d`)
- Log rotation is active and disk usage stays bounded
- Automatic restart works after crash (kill the process and verify relaunch)


## Troubleshooting

| Symptom | Diagnostic | Fix |
|---|---|---|
| Slow responses | `top -l 1`, check model backend | Verify RAM/CPU pressure; use a smaller model or remote API |
| Boot failures | `sudo launchctl list`, check logs | Inspect `/var/log/openclaw/stderr.log`, fix working directory |
| Auth errors | Check `.env` or Keychain secrets | Re-check provider keys, scopes, and endpoint URLs |
| Random crashes | `log show --predicate 'process == "node"'` | Pin dependency versions, check for OOM in `dmesg` |
| Port 3000 in use | `lsof -i :3000` | Kill conflicting process or change PORT in `.env` |
| Docker won't start | `docker info`, `docker compose logs` | Ensure Docker Desktop/OrbStack is running |
| Ollama model slow | `docker stats openclaw-ollama` | Allocate more RAM to Docker, use quantized model |
| Tailscale unreachable | `tailscale status`, `ping 100.64.x.x` | Re-authenticate with `tailscale up`, check firewall |
| Disk full | `df -h`, `du -sh ~/openclaw/data/` | Prune Docker images (`docker system prune`), rotate logs |


## Related Skills

- ollama-stack (`ollama-stack`) - Local model serving patterns
- mac-mini-llm-lab (`mac-mini-llm-lab`) - Mac mini reliability and security baseline
- startup-it-troubleshooting (`startup-it-troubleshooting`) - Small-team operational triage

