---
name: cis-benchmarks
description: 审计和补救 CIS 基准测试违规。
category: security
risk: critical
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: 需要相关的安全工具（扫描器、保管库 CLI）和任何活跃评估的授权范围。仅文档；助手脚本和模板未打包。
metadata:
  author: devops-skills
  version: '1.0'
---

# CIS 基准测试

实现和审计 CIS 安全基准测试。

## 何时使用此技能

在以下情况下使用此技能：
- 评估安全合规性
- 实现安全基线
- 满足监管要求
- 将系统强化到标准

## 评估工具

### OpenSCAP

```bash
# Install
apt install openscap-scanner scap-security-guide

# Run CIS benchmark scan
oscap xccdf eval \
  --profile xccdf_org.ssgproject.content_profile_cis \
  --results results.xml \
  --report report.html \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml
```

### Lynis

```bash
# Install
apt install lynis

# Run audit
lynis audit system

# Generate report
lynis audit system --report-file /tmp/lynis-report.dat
```

### InSpec

```ruby
# cis-profile/controls/ssh.rb
control 'cis-ssh-1' do
  impact 1.0
  title 'Ensure SSH root login is disabled'
  
  describe sshd_config do
    its('PermitRootLogin') { should eq 'no' }
  end
end

control 'cis-ssh-2' do
  impact 0.7
  title 'Ensure SSH password authentication is disabled'
  
  describe sshd_config do
    its('PasswordAuthentication') { should eq 'no' }
  end
end
```

```bash
# Run InSpec
inspec exec cis-profile -t ssh://user@target
```

### Kubernetes CIS

```bash
# kube-bench
docker run --rm -v /etc:/etc:ro -v /var:/var:ro \
  aquasec/kube-bench:latest run --targets node

# Check specific sections
kube-bench run --targets master --check 1.1,1.2
```

## 补救工作流

```yaml
workflow:
  1_scan:
    - Run automated assessment
    - Generate baseline report
    
  2_analyze:
    - Review findings
    - Identify false positives
    - Prioritize by risk
    
  3_remediate:
    - Apply fixes
    - Document exceptions
    - Verify changes
    
  4_validate:
    - Re-run assessment
    - Confirm remediation
    - Generate compliance report
```

## 最佳实践

- 强化前建立基线
- 记录例外情况
- 自动化评估
- 跟踪随时间的合规性
- 定期重新评估
- 版本控制配置

## 相关技能

- linux-hardening (`linux-hardening`) - Linux 安全性
- vulnerability-scanning (`vulnerability-scanning`) - 安全扫描

## 限制

- 仅在授权范围内应用指导；在生产环境外首先测试破坏性步骤。
- 仅文档导入：上游脚本和模板未打包。

### 示例

```bash
# Read-only first: inventory before any active step.
which <tool> && <tool> --help | head -n 20
```

> 改编自 [BagelHole/DevOps-Security-Agent-Skills](https://github.com/BagelHole/DevOps-Security-Agent-Skills) (MIT)；添加了前置事项、何时使用/限制和安全边界以满足上游合规。仅文档导入：助手脚本和模板未打包。
