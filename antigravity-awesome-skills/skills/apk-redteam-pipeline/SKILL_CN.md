---
name: apk-redteam-pipeline
description: 端到端的 Android APK 红队流程
category: security
risk: offensive
source: https://github.com/elementalsouls/Claude-BugHunter
source_repo: elementalsouls/Claude-BugHunter
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/elementalsouls/Claude-BugHunter/blob/main/LICENSE
compatibility: 需要针对目标范围的明确书面授权,以及该技术所需的相关测试工具。仅为文档;未捆绑辅助脚本和命令。
sources: authorized-engagement
report_count: 1
---
> **⚠️ 仅限授权使用**
> 本 skill 仅用于教育目的或经授权的安全评估。
> 在使用本工具之前,你必须获得系统所有者明确的书面许可。
> 滥用本工具是非法且严格禁止的。

> **强制确认关卡**
> 在运行任何会探测、利用、更改目标、在目标上持久化、从目标提取数据或尝试获取凭据的命令之前:
> 1. 要求用户陈述确切的目标 URL、IP、账号或资源。
> 2. 要求用户确认书面授权以及被允许的范围。
> 3. 展示确切的命令,并解释其预期效果。
> 4. 在当前对话中等待明确的确认。
>
> 没有这个确认,就保持只读状态,只提供防御性指导。优先使用沙箱、可丢弃的虚拟机或受控实验环境。

## 何时使用本 skill

当以下情况出现时触发:
- 侦察发现目标开发者名下有 1 个以上移动应用(Play Store 开发者页面)
- 某个 web 应用直接托管 `*.apk` 文件(例如在某次评估中在某个子域名上发现的 `Recruitz.apk`)
- 从窃密日志(stealer log)中泄露出 APK 包 ID(例如 `com.<brand>.app`、`com.<brand>.<sub-brand>` 这类窃密转储格式中的模式)
- 面向客户的应用、经销商/合作伙伴门户,或员工移动端配套应用在授权范围内
- Bug bounty 项目将 Android 列为授权范围

不要用于:
- 仅限 iOS 的目标(不同的流程——IPA 逆向、MobSF、frida-ios-dump)
- 已经由 JS bundle 分析覆盖的 React Native / Flutter web 应用
- 仅限服务端的评估

---

## 阶段 0 —— 清点组织所拥有的全部应用

### Play Store 开发者页面抓取
```bash
# 根据目标的品牌名找到开发者页面
curl -sk -A "Mozilla/5.0" "https://play.google.com/store/apps/developer?id=<Brand+Name>" -o /tmp/dev.html

# 提取包 ID
grep -oE 'id=[a-zA-Z0-9._]+' /tmp/dev.html | sort -u
```

示例输出(已匿名化——对于一个多品牌集团来说,7 个包很常见):
```
com.events.<brand>build
com.<corp>.<sub-brand-1>
com.<corp>.<sub-brand-2>
com.<corp>.<flagship>
com.<corp>.<product-line-1>
com.<corp>.<product-line-2>
com.<corp>.<sub-brand-3>
```

### 与窃密日志交叉比对
窃密日志格式包含类似 `*@com.<corp>.<app>` 的包名——如果你有一份泄露的转储,可以从 `creds_userpass.txt` 中提取这些内容。

### 品牌排列猜测(多品牌集团常见模式)
```
com.<brand>.app
com.<brand>.mobile  
com.<brand>.android
com.<brand>connect.app
in.<brand>.dealer
in.co.<brand>.app
```

---

## 阶段 1 —— APK 获取

### 首选:APKPure 直接下载(无需认证)
```bash
# 跟随 302 重定向到实际下载地址
curl -sk -L --max-time 60 \
  "https://d.apkpure.net/b/APK/<package_id>?version=latest" \
  -o "<package_id>.apk"

# 或者通过旧版 d-XX.winudf.com 镜像链(我们见过这种方式有效)
```

### 备选:APKMirror 搜索
```bash
curl -sk -A "Mozilla/5.0" "https://www.apkmirror.com/?post_type=app_release&searchtype=apk&s=<brand>" \
  | grep -oE 'href="[^"]+\.apk[^"]*"' | sort -u
```

### 第三选择:APKPure 网页搜索
```bash
curl -sk "https://apkpure.com/search?q=<brand>" | grep -oE 'data-dt-app="[^"]+"'
```

### XAPK 与 APK 的区别
- `.xapk` = 一个包含多个 split APK 的 zip 包(base + config.armeabi-v7a + config.en 等)
- 先解压外层,再解压内层的 `base.apk` 或 `<package>.apk`
- 有些 apkpure 下载会返回缺失 EOCD 签名的截断 XAPK——这是 CDN 限速的症状;换个 IP 重试,或者使用比 `unzip` 更宽容的 `7z x`

```bash
# 标准 unzip(适用于干净的 APK)
unzip -o <package>.apk -d extracted_<package>/

# 针对截断/已修复的 XAPK
7z x -y <package>.apk -o"extracted_<package>"

# 针对嵌套的 XAPK
for inner in extracted_<package>/*.apk; do
  mkdir -p "extracted_<package>/$(basename "$inner" .apk)"
  unzip -o "$inner" -d "extracted_<package>/$(basename "$inner" .apk)"
done
```

---

## 阶段 2 —— DEX 反编译(jadx)

```bash
# 安装
brew install jadx          # macOS
# 或
wget https://github.com/skylot/jadx/releases/latest/download/jadx-1.5.x.zip

# 反编译
jadx -d decompiled_<package>/ <package>.apk

# 针对包含多个 APK 的 XAPK
for inner in extracted_<package>/*.apk; do
  jadx -d decompiled_<package>_$(basename "$inner" .apk)/ "$inner"
done
```

如果只想快速做一次"仅字符串"的扫描,不做完整反编译:
```bash
find extracted_<package> -name "classes*.dex" -exec strings -8 {} \; > strings_<package>.txt
```

---

## 阶段 3 —— 敏感信息 grep(60 种模式目录)

```bash
# URL grep —— 自有域名引用
grep -oE 'https?://[a-zA-Z0-9.-]+\.(target1|target2|target3)\.(com|io|net|in)[a-zA-Z0-9./_?=&%-]*' strings_<package>.txt | sort -u

# 内部 IP / 端口 URL
grep -oE 'https?://(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|127\.)[0-9.]+(:[0-9]+)?[a-zA-Z0-9./_?=&-]*' strings_<package>.txt

# 云凭据
grep -oE 'AKIA[A-Z0-9]{16}'                            # AWS Access Key
grep -oE 'aws_secret_access_key[\s:=]+[A-Za-z0-9/+=]{40}' # AWS Secret
grep -oE 'AIza[A-Za-z0-9_-]{35}'                       # Google API key
grep -oE 'ya29\.[A-Za-z0-9_-]+'                        # Google OAuth refresh token
grep -oE 'gh[ps]_[A-Za-z0-9]{36}'                      # GitHub PAT
grep -oE 'glpat-[A-Za-z0-9_-]{20}'                     # GitLab PAT
grep -oE 'xox[pbar]-[A-Za-z0-9-]+'                     # Slack token
grep -oE 'sk-[A-Za-z0-9]{48}'                          # OpenAI API key
grep -oE 'sk-ant-[A-Za-z0-9_-]{90,}'                   # Anthropic API key
grep -oE 'AC[a-f0-9]{32}'                              # Twilio Account SID
grep -oE 'sk_live_[A-Za-z0-9]{24}'                     # Stripe live key
grep -oE 'pk_live_[A-Za-z0-9]{24}'                     # Stripe publishable
grep -oE 'mailgun-[A-Za-z0-9-]{40}'                    # Mailgun
grep -oE 'SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}'    # SendGrid

# JWT(任意算法)
grep -oE 'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*' strings_<package>.txt

# Firebase
grep -oE '"(api_key|project_id|database_url|storage_bucket|client_id|mobilesdk_app_id|google_app_id|gcm_defaultSenderId)"\s*:\s*"[^"]+"' \
  extracted_<package>/res/values/strings.xml \
  extracted_<package>/google-services.json \
  decompiled_<package>/resources/AndroidManifest.xml 2>/dev/null

# OAuth client secret
grep -oE 'client_secret["\s:=]+[A-Za-z0-9_-]{24,}' strings_<package>.txt

# 硬编码密码(启发式方法——误报较多,需人工复核)
grep -oE '"password"\s*:\s*"[^"]+"|password\s*=\s*"[^"]+"' decompiled_<package>/sources/**/*.java 2>/dev/null
```

### 真实发现示例(已匿名化——来自一次授权评估)
```
# 面向客户的 APK 里硬编码了这种形式的 URL:
https://api.<client>.example/<path-token>/<resource-token>?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.<payload>.<sig>

# 解码后的 JWT payload: {"sid":<int>,"iat":<unix-ts>,"exp":<unix-ts>}
# 大约 8 年前就已过期——但路径 token + 30 个 /v1/* 端点仍是有用的情报
```

---

## 阶段 4 —— Pinned 证书提取

```bash
# 在 assets/ 中查找 .cer / .der / .pem 文件
find extracted_<package>/assets -iname "*.cer" -o -iname "*.der" -o -iname "*.pem" -o -iname "*.crt" 2>/dev/null

# 或在 network_security_config.xml 中查找
find extracted_<package> -name "network_security_config.xml" -exec cat {} \;

# 对每个证书,提取 subject + SAN(可能揭示新的内部 API 主机)
for cert in $(find extracted_<package>/assets -iname "*.cer"); do
  echo "=== $cert ==="
  openssl x509 -in "$cert" -noout -subject -issuer -dates 2>/dev/null
  openssl x509 -in "$cert" -noout -text 2>/dev/null | grep -E 'Subject:|DNS:|Issuer:|Validity'
done
```

### 真实案例示例
一次授权评估中,一个面向客户的 APK 包含 `assets/api_<service>_<domain>_com.cer`——揭示了一个在被动侦察中尚未浮现的 `api.<service>.<domain>.example` 资产。

---

## 阶段 5 —— 导出组件枚举

AndroidManifest.xml 列出了各个组件。导出的组件(尤其是带有 `android:exported="true"` 或通过 intent-filter 隐式导出的)可以被其他应用触发——这是潜在的 intent 注入攻击面。

```bash
# 如需解码二进制 AndroidManifest
apktool d <package>.apk -o decoded_<package>/    # apktool 解码二进制 manifest

# 或直接从 jadx 输出中读取
cat decompiled_<package>/resources/AndroidManifest.xml | grep -E '<(activity|service|receiver|provider)' | head -50

# 筛选导出的组件
grep -E 'android:exported="true"' decompiled_<package>/resources/AndroidManifest.xml
```

对每个导出的组件,检查:
- 它是否接收会流入 WebView 的 extras(intent → WebView → XSS / file://)
- 它是否接收 URI extras(潜在的通过 deep link 实现的 SSRF)
- 它是否把 extras 传递给其他 Activity(intent 重定向)

---

## 阶段 6 —— Firebase / 云服务配置检查

```bash
# google-services.json —— 完整的 Firebase 配置
find extracted_<package> -name "google-services.json" -exec cat {} \; | python3 -m json.tool

# 关注:
#   project_id   → 可以猜测 Firestore / RTDB URL: https://<project_id>.firebaseio.com/.json
#   storage_bucket → 可以猜测 GCS bucket: gs://<bucket>
#   web_api_key  → 可用于枚举 Firebase 租户配置

# 测试 Firestore 是否可被公开读取
curl -s "https://firestore.googleapis.com/v1/projects/<project_id>/databases/(default)/documents/users"

# 测试 Realtime DB 是否可被公开读取
curl -s "https://<project_id>.firebaseio.com/.json"

# 测试 Storage Bucket 是否可被公开列出
curl -s "https://firebasestorage.googleapis.com/v0/b/<bucket>/o"
```

---

## 阶段 7 —— 运行时注入(Frida)

用于静态分析不够用的情况——你想在运行时dump token、绕过证书 pinning,或追踪 API 调用。

### 设置
```bash
pip install --break-system-packages frida-tools objection
adb devices  # 确保设备/模拟器已连接
# 把 frida-server 推送到设备上(需要 root,或使用已 root 的模拟器,如 Genymotion / x86_64 AVD)
```

### 证书 pinning 绕过(通用)
```javascript
// frida-script-pinning-bypass.js
Java.perform(function() {
    // OkHttp
    try {
        var CertificatePinner = Java.use('okhttp3.CertificatePinner');
        CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function() {
            console.log('[+] OkHttp pinning bypassed for: ' + arguments[0]);
            return;
        };
    } catch (e) {}
    // HttpsURLConnection
    try {
        var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
        TrustManagerImpl.verifyChain.implementation = function(chain) {
            console.log('[+] TrustManagerImpl verifyChain bypassed');
            return chain;
        };
    } catch (e) {}
});
```
```bash
frida -U -l frida-script-pinning-bypass.js -f <package_id> --no-pause
```

### 挂钩 HTTP 请求
```javascript
Java.perform(function() {
    var OkHttpClient = Java.use('okhttp3.OkHttpClient');
    var Request = Java.use('okhttp3.Request');
    var Call = Java.use('okhttp3.Call');
    
    OkHttpClient.newCall.implementation = function(req) {
        var url = req.url().toString();
        var headers = req.headers().toString();
        console.log('[REQ] ' + url);
        console.log('[HDRS] ' + headers);
        return this.newCall(req);
    };
});
```

### 通过 objection 快速提取 token
```bash
objection --gadget com.target.app explore
# 在交互环境内:
android hooking watch class_method <class>.<method> --dump-args --dump-return
```

---

## 阶段 8 —— 网络流量捕获(通过 mitmproxy)

用于在绕过 pinning 之后进行更深入的 API 发现。

```bash
# 在主机上运行 mitmproxy
mitmproxy --listen-port 8080

# 把 Android 设备的代理配置为 host:8080
# 在设备上安装 mitmproxy CA 证书:
#   - 在设备上从 http://mitm.it 拉取,或
#   - 在已 root 的设备上推送到 /system/etc/security/cacerts/

# 在流量经过 mitmproxy 的同时使用 Frida 的 pinning 绕过脚本
# 所有 API 调用都会在 mitmproxy UI 中可见
```

---

## 决策树 —— 发现各种结果后该怎么做

| 发现 | 下一步 |
|---|---|
| 有效 JWT(未过期) | 针对 API 主机进行测试——它是否授予访问权限?尝试 sid 篡改 |
| 已过期 JWT | 检查路径 token / API 端点结构——对 VPN 后渗透有用的情报 |
| AWS access key | 用 `awscli` 测试:`aws sts get-caller-identity`——很多泄露的 key 仍然拥有权限 |
| Firebase project_id + web_api_key | 测试公开的 Firestore/RTDB/Storage 读取 |
| Google API key(AIza*) | 针对 `https://www.googleapis.com/customsearch/v1` 等进行测试——看该 key 激活了哪个 API |
| 硬编码的 HTTP URL(http://) | 若缺乏证书 pinning,可能存在通过降级实现的 MITM |
| 内部主机的 pinned 证书 | 新资产发现——该主机是真实存在的 |
| 带 WebView 的导出 Activity | 测试 intent 注入 → URL 加载滥用 |
| 堆栈跟踪痕迹(Stack Overflow URL) | 识别开发者提出的问题 → 推断架构 |
| 硬编码凭据 | 立即进行喷射测试(遵守相关 skill 中的任何上限约束) |

---

## 反模式

- **不要只 grep "password"**——大多数敏感信息都有具体的高信噪比模式(AKIA、AIza、eyJ 等)。通用词汇 grep 会产生太多噪音。
- **不要跳过 XAPK 的 split APK**——config.armeabi split 和 config.<lang> split 有时包含不同的代码路径。
- **不要认为已过期的 JWT 就是"死情报"**——路径结构、端点列表和签名算法仍然有用。上面那个过期 8 年的 JWT 示例就说明了这一点。
- **不要只逆向最新版本**——(通过 APKMirror 的版本历史)旧版本 APK 有时会包含在新版本中已删除、但服务端仍然有效的敏感信息。
- **即使应用看起来"简单",也不要忽略 Firebase**——Firebase 规则配置错误(Firestore 公开可读)极其常见。
- **不要在生产设备上运行 Frida**——只在已 root 的模拟器或测试设备上运行。

---

## 工具安装(一次性)

```bash
brew install jadx p7zip
pip install --break-system-packages frida-tools objection
# Genymotion 或 AVD,用于已 root 的 Android 模拟器
```

为方便下载 APK,可以添加一个 `download-apk` shell 函数:
```bash
download-apk() {
  local pkg="$1"
  curl -sk -L --max-time 60 "https://d.apkpure.net/b/APK/$pkg?version=latest" -o "$pkg.apk"
  echo "Downloaded $(wc -c < "$pkg.apk") bytes"
  file "$pkg.apk"
}
```

---

## 与相邻 skill 的衔接

- `offensive-osint` —— Play Store / APKMirror 枚举是更广泛 OSINT 的一部分
- `hunt-cloud-misconfig` —— Firebase 公开可读正是本 skill 发现之后的专长领域
- `hunt-api-misconfig` —— 一旦你有了算法和样例 token,就可以进行 JWT 篡改
- `evidence-hygiene` —— 提取出的敏感信息在纳入报告前需要脱敏
- `redteam-mindset` —— APK 逆向应在评估第一天就进行,而不是事后才补做

---

## 真实发现模板(已匿名化——授权评估)

**发现:面向客户的 APK 中硬编码了 JWT 和 30+ 个内部 API 端点**

- 主题:遗留移动端构建中的硬编码产物暴露了内部 API 表面
- 观察:对 `com.<client>.<app>` 的反编译揭示了嵌入的 JWT(大约 8 年前已过期)以及针对 `api2.<client>.example`(仅对外部而言是内部专用)的 30+ 个 `/v1/*` 端点路径
- 描述:APK 附带了开发构建产物。路径 token 属于"隐藏式安全"(security-by-obscurity);API 端点清单是侦察级别的情报。
- 影响:在通过凭据泄露获得 VPN 立足点之后,攻击者无需逆向二进制即可拥有完整的 API 表面地图。通过 SSRF/LFI 恢复 HS256 密钥后,将能够任意伪造 token。
- 建议:轮换 HS256 密钥,迁移到 RS256,从构建中移除硬编码 URL,审计组织内所有 APK。
- 证据:提取的字符串、解码的 JWT、端点清单

---

## 相关 Skill 与链路

- **`cloud-iam-deep`** —— APK 敏感信息提取经常能得到有效的 AWS/GCP/Azure 凭据。链路原语:jadx 字符串 grep 产出 AWS Access Key ID + Secret → `cloud-iam-deep` 的 `aws sts get-caller-identity` → 角色/策略枚举 → IAM 权限提升路径(24 种已记录的 AWS 提权模式之一)→ 云平面接管。同样的流程也适用于从 APK 资源中提取的 GCP service-account JSON 和 Azure 共享访问签名 token。
- **`hunt-api-misconfig`** —— APK 端点清单免费给你提供了 API 表面;mass-assignment、JWT 和 CORS 漏洞是典型情况。链路原语:APK 揭示 `/v1/users/me` 和 `/v1/admin/users` → `hunt-api-misconfig` 对 `/v1/users/me` 进行 mass-assignment 探测(`{is_admin:true}`)→ 管理员角色提权 → 获得 `/v1/admin/users` 的访问权限。
- **`hunt-rce`** —— 从 APK 中提取的硬编码 JWT 签名密钥(HS256)能够实现任意 token 伪造。链路原语:APK 字符串得到 HS256 密钥 → 伪造管理员 token → 访问管理员 API → 如果该 API 存在 eval/模板/sink → 升级为针对服务器的 `hunt-rce`。另外:若应用是本地安装的,带 intent 注入 sink 的导出组件可能触达 `Runtime.exec`。
- **`offensive-osint`** —— APK 只是更广泛组织侦察图谱中的一个节点;可与数据泄露语料库和证书透明度日志配合使用。链路原语:APK 揭示内部 API 主机名 `api2.example.com` → `offensive-osint` 的证书透明度查询 → 发现同级子域名 → 扩大攻击面。
- **`redteam-report-template`** —— APK 发现需要清晰地说明"二进制泄露了什么",因为客户工程师常常会把移动端静态分析发现当作"混淆问题"而不予重视。链路原语:已验证的发现(提取出的 token/URL/密钥)→ `triage-validation` 的 7-Question Gate(具体是:"该凭据今天是否仍然能够通过认证?")→ `redteam-report-template` 打包,附带明确的二进制版本和提取复现步骤。

## 限制

- 仅限授权范围:在任何探测、利用或凭据访问命令之前,上面的确认关卡是强制性的。
- 仅为文档导入:上游的辅助脚本、命令、引擎和研究资产未被捆绑;需要时请从源仓库重新安装相应工具。
- 在报告之前验证每一项发现(参见 `triage-validation`);通过 `report-writing` 进行报告。优先使用沙箱、可丢弃的虚拟机或受控实验环境。

### 示例

```bash
# 只读的第一步;在进行任何主动操作之前确认范围。
cat scope.txt  # 来自授权评估简报的目标列表
```

> 改编自 [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)(MIT);为符合上游合规要求,添加了 frontmatter、"何时使用/限制"以及安全边界。仅为文档导入:可执行的辅助工具、命令、引擎和研究资产未被捆绑。
