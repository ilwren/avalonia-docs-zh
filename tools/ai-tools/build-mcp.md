---
id: build-mcp
title: Build MCP
sidebar_label: Build MCP
doc-type: how-to
description: "配置 Build MCP 服务器，让你的 AI 编程助手能检索 Avalonia 的指南、教程和 API 参考，并获得分步的迁移指引。"
keywords:
  - mcp
  - model context protocol
  - ai assistant
  - documentation
  - copilot
  - claude
  - cursor
  - windsurf
  - gemini
  - ai tools
  - wpf migration
  - xpf
tags:
  - mcp
  - ai
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Build MCP 是什么？ {#what-is-build-mcp}

Build MCP 服务器让你的 AI 编程助手直接接触 Avalonia 文档和专家级开发指引。助手不必再依赖可能过时或残缺的训练数据，而是能实时检索指南、教程和 API 参考，加载 Avalonia 专属的编码规则，并借助预置提示词完成新建项目、照着截图还原界面之类的常见工作流。

Build MCP **免费使用**，既不需要许可证密钥，也不用在本地安装。它以远程服务器的形式运行，在任何兼容 MCP 的编辑器或命令行工具里几秒钟就能配好。

该服务器还提供迁移工具，引导助手把项目升级到最新的 Avalonia Developer Tools 包，并把 WPF 应用迁移到 Avalonia——既可以是彻底的原生移植，也可以借助 Avalonia XPF 实现近乎无改动的跨平台部署。

关于 MCP 的总体介绍，请见 [AI 工具](/tools/ai-tools/)。

## 可用的工具 {#available-tools}

Build MCP 服务器向你的 AI 助手开放了八个工具：

### 文档与规则 {#documentation-and-rules}

| 工具 | 说明 |
|------|-------------|
| `search_avalonia_docs` | 检索完整的 Avalonia 文档，涵盖 API 参考、教程、指南和迁移文档。“styling”“binding”“mvvm”等常见主题会自动走优化过的查询，结果更准。 |
| `lookup_avalonia_api` | 在 API 参考中查找某个具体的 Avalonia 类、属性、方法或事件。诸如 `TextBlock`、`Window.Show`、`StyledProperty` 这类定向查询就用它。 |
| `get_avalonia_expert_rules` | 返回一整套 Avalonia 开发规则，涵盖 AXAML 语法、属性系统、样式、数据绑定、MVVM 模式、自定义控件、布局、主题、资产、线程以及应当避开的常见错误。在开发会话一开始就调用它，助手写出的 Avalonia 代码才会正确而地道。 |

### 迁移 {#migration}

| 工具 | 说明 |
|------|-------------|
| `migrate_diagnostics` | 手把手指引你配置或迁移到当前的 Avalonia Developer Tools 包，内容包括移除已弃用的 `Avalonia.Diagnostics` 包、安装 `AvaloniaUI.DiagnosticsSupport`、更新 `Program.cs` 与 `App.axaml.cs`，以及替换过时的 API 调用。 |
| `analyze_wpf_project` | 把 WPF 应用迁移到 Avalonia 的入口。它会扫描项目的目标框架、WPF 引用、第三方控件套件（Telerik、DevExpress、Syncfusion、Infragistics、Actipro、SciChart、Xceed、ComponentOne）、MVVM 框架和 P/Invoke 用法，然后建议走 Avalonia XPF 还是原生 Avalonia 迁移，并据此交棒给 `migrate_to_xpf` 或 `migrate_to_avalonia`。 |
| `migrate_to_xpf` | 手把手指引你用 XPF 把 WPF 应用迁移到 Avalonia（近乎无改动地跨平台，现有的 WPF 代码、XAML 和第三方控件都原样保留）。内容包括 NuGet 源配置、SDK 切换、许可证密钥设置、版本冲突处理和排查问题。 |
| `migrate_to_avalonia` | 原生 Avalonia 完整迁移的分阶段作战手册。它给出指导原则（照搬而非重构、先跑起来再说、按纵向切片推进）、第 0 阶段验证、项目准备、文件迁移、构建/测试/迭代指引以及迁移后的收尾步骤。它不会一上来就把完整参考一股脑丢出来，而是按需通过 `lookup_wpf_to_avalonia_mapping` 取用针对性的映射表。 |
| `lookup_wpf_to_avalonia_mapping` | 返回单个主题的 WPF→Avalonia 映射，这样助手在移植时只加载当下用得着的那张表。可选主题：`namespaces`、`controls`、`custom-controls`、`properties`、`styling`、`bindings`、`templates`、`events`、`resources`、`layout`、`threading`、`windows`、`animations`、`mvvm`、`navigation`、`gotchas`。 |

## 可用的提示词 {#available-prompts}

除工具外，Build MCP 服务器还提供若干提示词，用来为特定工作流调校助手。MCP 提示词就是预先写好的指令，为某项任务铺好助手的上下文和行为方式。

:::note
对提示词的支持因客户端而异。Claude Desktop、Claude Code 和 Cursor 支持 MCP 提示词，其他编辑器未必会在界面上呈现。若你的编辑器不支持提示词，也可以直接让助手调用 `get_avalonia_expert_rules` 工具，效果是一样的。
:::

| 提示词 | 说明 |
|--------|-------------|
| `init` | 为既有项目开启一次 Avalonia 专家会话：加载开发规则、把回答风格调得简洁，并要求助手对每个技术问题都去查文档工具。 |
| `new` | 引导你创建一个新的 Avalonia 应用，涵盖模板选择（桌面端用 `avalonia.mvvm`，跨平台用 `avalonia.xplat`）、用 CommunityToolkit.Mvvm 创建项目、配置编译绑定以及安装开发者工具。可接受一个可选的 `app_name` 参数。 |
| `recreate-ui` | 为“照着截图或图片还原界面”搭起一套迭代式设计工作流。助手会写 AXAML，用 [DevTools MCP](/tools/developer-tools/mcp) 的 `attach-to-file` 工具预览，截图与目标图比对，如此反复打磨直到结果吻合。可接受一个可选的 `theme` 参数（`light` 或 `dark`）。DevTools MCP 集成需要 [Avalonia 许可证](https://avaloniaui.net/pricing)。 |

## 配置 MCP 服务器 {#setting-up-the-mcp-server}

Build MCP 用的是远程 URL 端点。你的编辑器通过 HTTP 连上服务器，本地无需安装任何东西。

在下面选择你用的编辑器或命令行工具：

<Tabs groupId="editor">
<TabItem value="vscode" label="VS Code">

**方式 A：命令面板**

1. 打开命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`）。
2. Run **MCP: Add Server**.
3. 服务器类型选 **HTTP**。
4. URL 填 `https://docs-mcp.avaloniaui.net/mcp`。
5. 服务器名称设为 `avalonia-docs`。
6. 选择把该服务器装到当前工作区还是全局。

**方式 B：手动配置**

把下列内容加进工作区根目录的 `.vscode/mcp.json`：

```json title=".vscode/mcp.json"
{
    "servers": {
        "avalonia-docs": {
            "type": "http",
            "url": "https://docs-mcp.avaloniaui.net/mcp"
        }
    }
}
```

</TabItem>
<TabItem value="visual-studio" label="Visual Studio">

Visual Studio 2022（17.x 及更高版本）通过 `mcp.json` 配置文件支持 MCP 服务器。

把下列内容加进解决方案目录下的 `.vscode/mcp.json`：

```json title=".vscode/mcp.json"
{
    "servers": {
        "avalonia-docs": {
            "type": "http",
            "url": "https://docs-mcp.avaloniaui.net/mcp"
        }
    }
}
```

:::tip
Visual Studio 读取的 `.vscode/mcp.json` 路径与 VS Code 相同。若你已为 VS Code 配置过，它在 Visual Studio 中自动就能用。
:::

</TabItem>
<TabItem value="rider" label="Rider">

JetBrains Rider 可通过 AI Assistant 插件和 GitHub Copilot 插件支持 MCP 服务器。

**方式 A：设置界面**

1. Open **Settings** > **Tools** > **AI Assistant** > **MCP Servers**.
2. 点击 **Add**，传输类型选 **Streamable HTTP**。
3. URL 填 `https://docs-mcp.avaloniaui.net/mcp`。
4. 服务器名称设为 `avalonia-docs`。

**方式 B：手动配置**

在项目目录中新建或编辑 `.idea/mcp.json`：

```json title=".idea/mcp.json"
{
    "servers": {
        "avalonia-docs": {
            "type": "http",
            "url": "https://docs-mcp.avaloniaui.net/mcp"
        }
    }
}
```

</TabItem>
<TabItem value="cursor" label="Cursor">

把下列内容加进项目目录下的 `.cursor/mcp.json`，若要全局配置则加进 `~/.cursor/mcp.json`：

```json title=".cursor/mcp.json"
{
    "mcpServers": {
        "avalonia-docs": {
            "url": "https://docs-mcp.avaloniaui.net/mcp"
        }
    }
}
```

</TabItem>
<TabItem value="windsurf" label="Windsurf">

把下列内容加进 `~/.codeium/windsurf/mcp_config.json`：

```json title="~/.codeium/windsurf/mcp_config.json"
{
    "mcpServers": {
        "avalonia-docs": {
            "serverUrl": "https://docs-mcp.avaloniaui.net/mcp"
        }
    }
}
```

</TabItem>
<TabItem value="claude-code" label="Claude Code">

在终端里运行这条命令：

```bash
claude mcp add --transport http avalonia-docs https://docs-mcp.avaloniaui.net/mcp
```

验证是否添加成功：

```bash
claude mcp list
```

</TabItem>
<TabItem value="claude-desktop" label="Claude Desktop">

1. 依次进入 **Customize** → **Connectors**。
2. 点击窗口顶部的 **+** 按钮，再点 **Add custom connector**。
3. 在 “Name” 一栏填入 “avalonia-docs”。
4. 在 “Remote MCP server URL” 一栏填入 `https://docs-mcp.avaloniaui.net/mcp`。
5. Click **Add**.
6. 可能需要重启 Claude Desktop。

</TabItem>
<TabItem value="gemini-cli" label="Gemini CLI">

把下列内容加进 `~/.gemini/settings.json`（或项目级的 `.gemini/settings.json`）：

```json title="~/.gemini/settings.json"
{
    "mcpServers": {
        "avalonia-docs": {
            "httpUrl": "https://docs-mcp.avaloniaui.net/mcp"
        }
    }
}
```

</TabItem>
</Tabs>

## 验证连接 {#verify-the-connection}

配置好 MCP 服务器后，按下面的步骤确认它确实在工作：

1. **确认服务器已列出。**打开编辑器的 MCP 面板或状态指示器，确认 `avalonia-docs` 以已连接服务器的身份出现。在 VS Code 中，可从命令面板运行 **MCP: List Servers**。
2. **用一句提示词试一下。**问问你的 AI 助手：

```text
"Search the Avalonia docs for how to set up data binding."
```

若助手返回了带来源链接的文档结果，就说明配置完成了。

## 排查问题 {#troubleshooting}

### 编辑器里看不到 MCP 服务器 {#mcp-server-does-not-appear-in-the-editor}

- 添加或修改 MCP 配置文件后，**请重启编辑器**。多数编辑器都要重启才能发现新的 MCP 服务器。
- **核对配置文件的位置。**每种编辑器都有各自约定的配置路径，请参照上文中你所用编辑器的配置说明。
- **检查 JSON 是否合法。**配置文件里的语法错误（漏逗号、多余的尾逗号、括号不配对）会悄无声息地让服务器加载不起来。

### 服务器出现了，但用不了工具 {#server-appears-but-tools-are-not-available}

- **确认你的编辑器支持 HTTP 传输。**某些较旧的编辑器版本只支持基于 STDIO 的 MCP 服务器，请把编辑器升级到最新版本。
- **检查网络连通性。**服务器托管在 `docs-mcp.avaloniaui.net`，请确认你的网络能访问这个域名。

### 结果似乎不是最新的 {#results-seem-outdated}

Build MCP 服务器索引的是已发布的 Avalonia 文档。若你发现内容陈旧，可能是文档站本身还没更新。可直接去 [docs.avaloniaui.net](https://docs.avaloniaui.net) 核对。

## 用法示例 {#usage-examples}

用自然语言说清你想做什么，AI 助手会自动调用相应的 MCP 工具：

**检索文档：**

```text
"Search the Avalonia docs for how to use TreeView with data binding."
```

**查阅 API 类型：**

```text
"Look up the Avalonia TextBlock control in the API reference."
```

**在会话开始时加载专家规则：**

```text
"Load the Avalonia expert rules so you can help me build my app correctly."
```

**创建新项目（使用 `new` 提示词）：**

```text
"Create a new Avalonia desktop app called WeatherTracker."
```

**照着截图还原界面（使用 `recreate-ui` 提示词）：**

```text
"Recreate this UI in Avalonia. Use the light theme."
```

这个提示词与 [DevTools MCP](/tools/developer-tools/mcp) 搭配效果最好，后者提供了用于实时预览 XAML 的 `attach-to-file` 工具。助手会写 AXAML、预览、截图，反复迭代直到结果贴合你的目标设计。DevTools MCP 需要 [Avalonia 许可证](https://avaloniaui.net/pricing)。

**迁移 WPF 应用：**

```text
"Analyze my WPF project and recommend the best migration path to Avalonia."
```

助手会调用 `analyze_wpf_project` 扫描你的项目，摸清目标框架、WPF 引用、第三方控件套件（Telerik、DevExpress、Syncfusion、Infragistics、Actipro、SciChart、Xceed、ComponentOne）、MVVM 框架和平台专属代码。根据扫描结果，它会在两条路径中推荐一条，并交棒给对应的工具：

- **Avalonia XPF**——近乎无改动地跨平台，现有的 WPF 代码、XAML 和第三方控件原样保留。助手会调用 `migrate_to_xpf`，带你走完 NuGet 配置、SDK 切换和许可证设置。
- **原生 Avalonia**——彻底迁移到现代的 Avalonia 控件与主题。助手会调用 `migrate_to_avalonia` 取得分阶段作战手册，然后在逐个文件移植时通过 `lookup_wpf_to_avalonia_mapping` 按主题取用针对性的映射表（控件、属性、样式、绑定、事件、模板、常见的坑等）。这样上下文始终聚焦——助手只加载当前这一节用得着的映射。

**配置 Avalonia Developer Tools：**

```text
"Help me set up the latest Avalonia Developer Tools in my project."
```

助手会调用 `migrate_diagnostics` 工具，引导你安装 `AvaloniaUI.DiagnosticsSupport`，并在存在已弃用的 `Avalonia.Diagnostics` 包时将其移除。

## 另请参阅 {#see-also}

- [AI 工具概述](/tools/ai-tools/)
- [DevTools MCP](/tools/developer-tools/mcp)
- [Parcel MCP](/tools/parcel/mcp)
