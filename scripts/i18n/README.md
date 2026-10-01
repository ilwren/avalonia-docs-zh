# Avalonia 文档简体中文翻译流水线

本目录是 `avalonia-docs-zh` 的翻译基础设施。核心思路只有一句：

> **英文原文永远从基线提交读取，中文文档永远由「基线原文 + 翻译记忆库」渲染生成。**

因此整条流水线是**幂等**的 —— 重复执行不会把已译内容再翻一遍，也不会出现译文叠加、
半中半英互相覆盖的情况。想补译、想改译名、想同步上游更新，重跑一遍 `apply` 即可。

## 目录结构

```
scripts/i18n/
├── config.json       基线提交（base_ref）与目标语言
├── segmenter.py      Markdown / MDX 分段器（核心）
├── i18n_cli.py       extract / apply / stats / verify
├── merge.py          按序号把一批译文合并进记忆库
├── apply_ui.py       侧边栏分类与站点标题的译名回填
├── check_mdx.mjs     用 MDX 编译器逐篇校验语法
├── glossary.md       术语表与文风约定
└── tm/               翻译记忆库
    ├── docs.json     手写文档
    ├── api.json      API 参考
    └── ui.json       侧边栏 / 导航栏标签
```

## 日常工作流

```bash
# 1) 看看还缺哪些片段（按出现频次排序，优先译高频的性价比最高）
python3 scripts/i18n/i18n_cli.py extract --scope api --limit 300

# 1') 想整篇译完，就按文中顺序导出某个目录
python3 scripts/i18n/i18n_cli.py extract --scope docs --path docs/fundamentals --by-file

# 2) 照着 tm/<scope>.todo.json 里的序号写译文，存成 batch.json：
#    {"0": "……", "1": "……"}
python3 scripts/i18n/merge.py docs batch.json

# 3) 回填到工作区
python3 scripts/i18n/i18n_cli.py apply --scope all
python3 scripts/i18n/apply_ui.py

# 4) 自检
python3 scripts/i18n/i18n_cli.py verify
node scripts/i18n/check_mdx.mjs docs controls tools troubleshooting xpf api
python3 scripts/i18n/i18n_cli.py stats
```

## 为什么要有占位符

分段器会把**不该翻译的东西**全部替换成 `⟦0⟧`、`⟦1⟧` 这样的占位符再交给译者：

| 受保护内容 | 示例 |
| --- | --- |
| 行内代码 | `` `IsVisible` `` |
| JSX / HTML 标签 | `<span className="...">` |
| MDX 表达式 | `{props.version}` |
| 链接地址 | `](../input/inputelement.mdx)` |
| 点分标识符 | `Avalonia.Controls.Button` |
| 文件名 | `MainWindow.axaml` |
| HTML 实体 | `&gt;` |

这带来两个关键好处：

1. **结构不会被译坏。** 译者看到的是纯文字，碰不到标记；`merge.py` 还会逐条比对
   占位符集合与方括号数量，对不上直接拒绝合并。
2. **去重率极高。** 屏蔽之后，`Namespace: Avalonia.Controls` 和
   `Namespace: Avalonia.Media` 归一化成同一条记忆。自动生成的 API 参考因此只需
   **425 条**译文，就覆盖了 84% 的文本出现次数。

## 锚点保护

翻译标题会改变 Docusaurus 自动生成的 id，站内 `#锚点` 链接随之全部失效。
分段器在译完标题后会补上原始锚点：

```md
## See also          →   ## 另请参阅 {#see-also}
### Properties       →   ### 属性 {#properties}
### Properties       →   ### 属性 {#properties-1}   ← 复刻 github-slugger 的重复编号
```

## 同步上游更新

上游（AvaloniaUI/avalonia-docs）更新后：

1. 合并上游改动，把 `config.json` 里的 `base_ref` 指向新的英文基线提交；
2. `extract` 会自动列出新增 / 改动的片段（旧片段命中记忆库，不必重译）；
3. 补译增量，`apply` 回填。

## CI

`.github/workflows/build-zh-docs.yml` 会做四件事：

1. `verify` —— 译文结构校验（占位符、代码围栏、`<ApiRefPage>` 配对）；
2. 比对「记忆库渲染结果」与「仓库现有文档」是否一致，防止有人手改了译文却没回写记忆库；
3. `check_mdx.mjs` —— 3,500+ 篇逐一过 MDX 编译器；
4. `docusaurus build` 并校验产物中确实含中文。
