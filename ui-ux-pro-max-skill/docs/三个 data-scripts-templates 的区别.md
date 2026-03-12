# 三处 data / scripts / templates 的区别

## 三处分别是什么

| 位置 | 作用 | 能删吗 |
|------|------|--------|
| **src/ui-ux-pro-max/** | **唯一源码**。所有 CSV、脚本、模板都在这里改，是“唯一真相来源”。 | ❌ 不能删，这是你要维护的那一份。 |
| **.claude/skills/ui-ux-pro-max/** | 给 **Cursor / Claude Code** 用的 Skill。AI 从这里读 SKILL.md 和运行 `scripts/search.py`。设计上这里的 data、scripts 应是**指向 src 的符号链接**，这样不用维护两份。 | ❌ 不能删（否则 Skill 不工作）；但可以改成只链到 src，不保留副本。 |
| **cli/assets/** | 给 **npm 包 uipro-cli** 打包用。用户执行 `npm i -g uipro-cli` 再 `uipro init` 时，安装的是这里打包进去的 data/scripts/templates。 | ❌ 不能删；发布前用脚本从 src 同步过来即可。 |

## 可以只保留一个吗？

- **不能**只保留一个“物理目录”：三处**用途不同**，都要存在。
- **可以**只维护**一份内容**：
  - 所有修改只在 **src/ui-ux-pro-max/** 里做。
  - .claude 里用**符号链接**指向 src → 不用在 .claude 里再维护 data/scripts。
  - 发布 CLI 前执行一次同步：把 src 拷到 cli/assets。

这样你日常只改 src，其它两处自动或按需跟上。

## 推荐工作流

1. 只改 **src/ui-ux-pro-max/data/**、**scripts/**、**templates/**。
2. .claude/skills 下的 data、scripts 用 symlink 指回 src（见下方「恢复符号链接」）。
3. 发布 npm 前执行：
   ```bash
   cp -r src/ui-ux-pro-max/data/* cli/assets/data/
   cp -r src/ui-ux-pro-max/scripts/* cli/assets/scripts/
   cp -r src/ui-ux-pro-max/templates/* cli/assets/templates/
   ```
