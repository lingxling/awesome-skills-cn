# CI 漂移修复指南

**问题**：失败的作业是由于在更新脚本运行后在 `README.md`、`skills_index.json` 或目录文件中检测到未提交的更改引起的。

**错误**：

```
❌ 检测到由 registry/readme/catalog 脚本产生的未提交更改。
```

**原因**：
像 `tools/scripts/generate_index.py`、`tools/scripts/update_readme.py` 和 `tools/scripts/build-catalog.js` 这样的脚本会修改 `README.md`、`skills_index.json`、`data/catalog.json`、`data/bundles.json`、`data/aliases.json` 和 `CATALOG.md`。工作流期望这些文件在脚本运行后没有更改。任何差异意味着提交的仓库与生成脚本产生的内容不同步。

**如何修复（每次都要这样做）：**

1. 在本地运行**完整的验证链**：

   ```bash
   npm run chain
   npm run catalog
   ```

2. 检查更改：

   ```bash
   git status
   git diff
   ```

3. 提交并推送任何更新：
   ```bash
   git add README.md skills_index.json data/catalog.json data/bundles.json data/aliases.json CATALOG.md
   git commit -m "chore: sync generated registry files"
   git push
   ```

**总结**：
始终提交并推送 registry、README 同步和 catalog 脚本产生的所有更改。这通过确保仓库和生成的工件与规范的 `tools/scripts/*` 管道保持同步，保持 CI 通过。
