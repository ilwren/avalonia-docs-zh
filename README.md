<p align="center">
  <img alt="Avalonia UI logo" src="static/img/purple-border-gradient-icon.png" width="75px" />
  <h1 align="center">Avalonia 文档（简体中文）</h1>
</p>

本仓库是 [Avalonia 官方文档站](https://docs.avaloniaui.net)（[AvaloniaUI/avalonia-docs](https://github.com/AvaloniaUI/avalonia-docs)）的**简体中文翻译分支**，包含站点代码与 Markdown 源文件。

---

## ⚠️ 免责声明：本仓库的中文内容由 AI 翻译

> **请务必先读这一段。**
>
> - 本仓库中的**全部中文译文（包括正文、标题、侧边栏标签以及 `api/` 下的 API 参考说明）均由 AI 自动翻译生成**，并经过脚本化校验，但**未经人工逐句审校**。
> - 翻译可能存在**错译、漏译、术语不统一、语气生硬或与最新英文原文不同步**的情况。技术细节、API 行为、命令行参数、版本号等内容，**一律以[英文原版文档](https://docs.avaloniaui.net)为准**。
> - 代码示例、XAML 片段、类型名、成员名、命名空间与方法签名**保持英文原样未作翻译**，仅翻译描述性文字。
> - 本仓库为**非官方**翻译，与 Avalonia 官方团队无从属关系，亦**不提供任何明示或默示的担保**。因使用本译文造成的任何后果，译者与贡献者不承担责任。
> - 如发现翻译问题，欢迎提交 Issue 或 Pull Request 指正；若是**文档内容本身**的问题，请到[上游仓库](https://github.com/AvaloniaUI/avalonia-docs/issues/new)反馈。

> **Disclaimer (English):** All Chinese text in this repository is **machine-translated by AI** and has **not** been reviewed sentence-by-sentence by a human translator. It may contain errors or be out of sync with the upstream English docs. Always refer to the [official English documentation](https://docs.avaloniaui.net) as the authoritative source. This is an **unofficial** translation, provided "as is" without warranty of any kind.

---

## 目录

- [免责声明](#️-免责声明本仓库的中文内容由-ai-翻译)
- [拉取项目源码](#拉取项目源码)
  - [克隆仓库](#克隆仓库)
  - [更新到最新](#更新到最新)
  - [同步上游英文原版](#同步上游英文原版)
- [本地运行](#本地运行)
  - [环境要求](#环境要求)
  - [安装依赖](#安装依赖)
  - [启动预览](#启动预览)
  - [构建静态站点](#构建静态站点)
- [翻译流水线](#翻译流水线)
- [参与贡献](#参与贡献)
  - [工作流](#工作流)
  - [写作约定](#写作约定)
- [API 参考的生成](#api-参考的生成)
- [反馈与问题](#反馈与问题)
- [致谢 💜](#致谢-)

## 拉取项目源码

本仓库的中文翻译位于分支 **`arena/01a0f56b-avalonia-docs-zh`**。

### 克隆仓库

```bash
# HTTPS（推荐）
git clone https://github.com/ilwren/avalonia-docs-zh.git
cd avalonia-docs-zh

# 切换到中文翻译分支
git checkout arena/01a0f56b-avalonia-docs-zh
```

一步到位，只拉取翻译分支（仓库较大，这样更快）：

```bash
git clone --branch arena/01a0f56b-avalonia-docs-zh --single-branch \
  https://github.com/ilwren/avalonia-docs-zh.git
cd avalonia-docs-zh
```

只要最新一次提交（浅克隆，体积最小，适合只想在本地跑一下文档站的人）：

```bash
git clone --branch arena/01a0f56b-avalonia-docs-zh --single-branch --depth 1 \
  https://github.com/ilwren/avalonia-docs-zh.git
cd avalonia-docs-zh
```

其他方式：

```bash
# SSH
git clone git@github.com:ilwren/avalonia-docs-zh.git

# GitHub CLI
gh repo clone ilwren/avalonia-docs-zh
```

### 更新到最新

```bash
# 在仓库目录下
git fetch origin
git pull --ff-only origin arena/01a0f56b-avalonia-docs-zh
```

本地有改动、无法快进时，可以先暂存：

```bash
git stash
git pull --ff-only origin arena/01a0f56b-avalonia-docs-zh
git stash pop
```

### 同步上游英文原版

把 Avalonia 官方仓库加为 `upstream`，即可随时对照或合并英文更新：

```bash
git remote add upstream https://github.com/AvaloniaUI/avalonia-docs.git
git fetch upstream

# 查看本地与上游英文版的差异
git diff upstream/main --stat
```

## 本地运行

### 环境要求

- **Node.js >= 18**（推荐 20 或更高）
- npm（随 Node.js 一起安装）
- Python 3.9+（仅在需要运行翻译流水线时才用得上）

### 安装依赖

```bash
npm install
```

严格按 lockfile 安装（CI 使用的方式）：

```bash
npm ci
```

### 启动预览

```bash
npm run start:light

# 刻意跳过 /api 页面，启动更快，也不容易触发「内存不足」崩溃。日常写作与校对推荐用这个。
```

```bash
npm start

# 预览整站（含 API 参考）。只有在需要查看 /api 页面时才用，它很吃内存。
```

### 构建静态站点

```bash
# 完整构建（含 API 参考，建议至少 12 GB 可用内存）
NODE_OPTIONS=--max-old-space-size=12288 npx docusaurus build

# 跳过 API 参考的快速构建
DOCS_SKIP_API=1 npx docusaurus build
```

构建产物位于 `build/` 目录，可用 `npm run serve` 本地预览。

## 翻译流水线

中文翻译不是手工逐文件改出来的，而是由 `scripts/i18n/` 下的一套工具链驱动的：切分 → 翻译记忆库 → 回填 → 校验。

```bash
# 抽取尚未翻译的文本片段
python3 scripts/i18n/i18n_cli.py extract --scope docs --path controls/input --by-file

# 把译文合并进翻译记忆库
python3 scripts/i18n/merge.py docs scripts/i18n/batch.json

# 将记忆库回填到 Markdown 源文件
python3 scripts/i18n/i18n_cli.py apply --scope all

# 校验占位符、代码围栏、JSX 标签是否与原文一致
python3 scripts/i18n/i18n_cli.py verify

# 逐篇做 MDX 语法编译校验
node scripts/i18n/check_mdx.mjs docs controls tools troubleshooting xpf api

# 查看翻译覆盖率
python3 scripts/i18n/i18n_cli.py stats
```

> `apply` 每次都从**基线提交**重新渲染译文，因此直接改 `.md` 文件的改动会在下次运行时被覆盖。
> 要让润色永久生效，请同步更新 `scripts/i18n/tm/docs.json`（或 `api.json`）中对应的记忆条目。
> 本 README 不走流水线，属于手工维护的文件。

设计说明与术语表见 [`scripts/i18n/README.md`](scripts/i18n/README.md) 和 [`scripts/i18n/glossary.md`](scripts/i18n/glossary.md)。
GitHub Actions 工作流 [`.github/workflows/build-zh-docs.yml`](.github/workflows/build-zh-docs.yml) 会在每次推送时校验翻译完整性并构建整站。

## 参与贡献

欢迎帮忙润色译文。请 fork 本仓库，然后针对 Markdown 或图片的改动提交 Pull Request。

### 工作流

推荐两种方式：

- 小修小补：直接用每个页面上的「Edit this page」按钮在 GitHub 上改 Markdown。
- 改动较大、或想在本地预览：把仓库克隆到本地，按[拉取项目源码](#拉取项目源码)和[本地运行](#本地运行)操作。

### 写作约定

- 每个 Markdown 文件的 front matter 都应包含 `id`、`title`、`description` 和 `doc-type`。

  ```yaml
  ---
  id: main-window
  title: 主窗口
  description: 为桌面、移动和浏览器平台设置并访问主窗口或主视图。
  doc-type: explanation
  ---
  ```

- 文件名和文件夹名使用 `kebab-case`。例如：
  - `/docs/get-started/create-your-first-project.md`
  - `/controls/input/buttons/togglebutton.md`

- 往仓库里加图片时，请放在 `static` 下的 `img` 子目录中。按主题新建或选用合适的文件夹，例如 `static\img\custom-controls\custom-flyout-demo.gif`。

  引用图片时路径和文件名**区分大小写**，约定使用 `kebab-case`。请用 `import` 引入图片以便及时发现失效链接，并把 `import` 放在文档靠前的位置方便维护；插入图片时使用 `<Image>` 组件。

  > 在 Markdown 文件中插入图片的示例代码：

  ```markdown
  import LayoutZonesDiagram from '/img/concepts/ui-concepts/layout/layout-zones.png';
  <Image light={LayoutZonesDiagram} maxWidth="400" alignment="center" alt="一张由四个重叠矩形组成的示意图，表示界面窗口的各个布局区域。" />
  ```

## API 参考的生成

`api/` 下的 API 参考页面由 `dotnet-apiref` 工具依据 `apiref.json` 的配置生成，生成结果已提交进仓库，因此 CI 和其他贡献者不必安装该工具也能构建站点。

### 手动重新生成

在本地重新生成 API 参考内容，需先安装 `dotnet-apiref` 工具，然后运行：

```bash
npm run apiref:materialise
```

该命令实际执行 `dotnet-apiref materialise --site .`：读取 `apiref.json`，拉取 NuGet 包，并把 API 文档文件写入站点。

> **注意：** 重新生成会用英文内容覆盖 `api/` 下已翻译的文件。覆盖后请运行 `python3 scripts/i18n/i18n_cli.py apply --scope api` 把译文重新回填。

### 自动重新生成（可选）

如果希望每次本地 `build` 或 `start` 之前都自动重新生成 API 参考，可以在 `package.json` 的 `scripts` 中加上这两个生命周期钩子：

```json
"prestart": "npm run apiref:materialise",
"prebuild": "npm run apiref:materialise"
```

**请勿提交这些钩子**，因为 CI 环境没有安装 `dotnet-apiref`，构建会失败。生成好的 API 参考文件已经在仓库里了。

## 反馈与问题

- **翻译问题**（错译、漏译、措辞别扭）：请在本仓库提 [Issue](https://github.com/ilwren/avalonia-docs-zh/issues/new) 或直接提 PR。
- **文档内容本身的问题**（英文原文有误、缺少说明、功能请求）：请到上游仓库提 [GitHub issue](https://github.com/AvaloniaUI/avalonia-docs/issues/new)。提之前麻烦先搜一下已有 issue，避免重复。
- 也欢迎加入 Avalonia 的 [Telegram 社区](https://t.me/Avalonia) 交流。

## 致谢 💜

感谢所有为 Avalonia UI 文档付出努力的贡献者。感谢你成为这个 ✨ 社区 ✨ 的一员！
