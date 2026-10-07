---
name: browser-extension-reverse
description: "授权的 Chrome/Firefox 扩展逆向工程：清单分析、后台工作者、内容脚本以及基于扩展的凭证或数据泄露研究。"
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ 仅限授权使用**
> 此技能仅用于教育目的或授权的安全评估。
> 在使用此工具之前，你必须获得系统所有者的明确书面许可。
> 滥用此工具是非法的，严格禁止。

> **强制确认门控**
> 在运行任何探测、利用、更改、保留、提取数据或尝试对目标进行凭证访问的命令之前：
> 1. 要求用户说明确切的目标 URL、IP、帐户或资源。
> 2. 要求用户确认书面授权和允许的范围。
> 3. 显示确切的命令并解释其预期效果。
> 4. 等待当前对话中的明确确认。
>
> 没有该确认，保持只读并仅提供防御性指导。首选沙箱、一次性 VM 或受控实验室。

# 浏览器扩展逆向工程
## 何时使用

- 在授权审查中审计浏览器扩展的行为和权限。
- 调查扩展如何处理凭证或敏感页面数据。


## 适用场景

- Chrome/Edge MV2/MV3 扩展分析
- Firefox 扩展
- 恶意扩展 IOC、供应链扩展投毒调查
- 扩展实现的签名/加密/代理逻辑还原

## 工作流

### 1. 包体

```text
□ crx 解压 / 从 profile 取扩展目录
□ manifest.json：permissions、host_permissions、background、content_scripts
□ 评估过度权限（<all_urls>、webRequest、debugger）
```

### 2. 逻辑

```text
□ service_worker / background 入口
□ content_script 注入点与世界（isolated）
□ chrome.storage / IndexedDB 密钥
□ 与 `js-reverse` 相同：Observe 网络与消息传递（runtime.sendMessage）
```

### 3. 动态

```text
□ 开发者模式加载解压目录
□ chrome://extensions 检查错误
□ DevTools 附加 service worker
□ 必要时 Frida/浏览器 CDP（jshookmcp）
```

## 工具链

| 工具 | 用途 |
|------|------|
| 解压/jq | manifest |
| Chrome DevTools | worker 调试 |
| js-reverse 工具链 | 深度 JS |
| YARA | 恶意扩展规则 |

## 参考

- `references/extension-analysis.md`
- field-journal 扩展恢复相关条目
- `../js-reverse/` `../malware-analysis/`

## 路由上下文

**上游**: MASTER R30  
**下游**: 复杂混淆 JS → `js-reverse`；投毒调查 → supply-chain / malware

## 任务完成自检

- [ ] 是否列出权限面与入口脚本？
- [ ] 是否还原关键数据流？
- [ ] Checklist？

## 限制

- 扩展商店频繁更新；发现可能会过期。
- 动态分析需要与个人帐户隔离的配置文件。

> 改编自 [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT)。
