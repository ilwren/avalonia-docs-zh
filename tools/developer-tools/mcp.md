---
id: mcp
title: DevTools MCP
sidebar_label: DevTools MCP
doc-type: how-to
description: "配置 DevTools MCP 服务器，让 AI 助手能检视、调试并修改你正在运行的 Avalonia 应用。"
keywords:
  - mcp
  - model context protocol
  - ai assistant
  - devtools
  - copilot
  - claude
  - cursor
  - ai tools
tags:
  - mcp
  - ai
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## DevTools MCP 是什么？ {#what-is-devtools-mcp}

DevTools MCP 服务器让 AI 助手连上正在运行的 Avalonia 应用并直接与之交互。助手可以检视视觉树，按类型或名称查找元素，读取和修改属性，截图，还能发送输入事件。它也能挂接到 XAML 预览器，让你不必离开编辑器就能反复打磨布局。

关于 MCP 的总体介绍，请见 [AI 工具](/tools/ai-tools/)。

## 前置条件 {#prerequisites}

配置 MCP 服务器前，请先确认你具备：

1. 已安装 **DevTools .NET 工具**。请按[快速上手](/tools/developer-tools/installation)指南操作。
2. **有效的 Avalonia Plus 许可证密钥。**可在 [Avalonia 门户](https://portal.avaloniaui.net/)获取。

### 设置许可证密钥 {#setting-your-license-key}

MCP 服务器从 `AVALONIA_TOOLS_LICENSE_KEY` 环境变量读取你的许可证。许可证密钥可在 [Avalonia 客户门户](https://portal.avaloniaui.net/)中找到。MCP 属于付费功能，Community 许可证不含此项。

:::note
`AVALONIA_TOOLS_LICENSE_KEY` 变量自 Avalonia 12.0.0 起启用。若你用的是 Avalonia 11.x.x 或更早版本，请改用 `ACCELERATE_LICENSE_KEY`。
:::

把密钥写进 shell 配置，这样跨会话也能一直生效：

<Tabs>
<TabItem value="macos-linux" label="macOS / Linux">

把这一行加进你的 shell 配置文件（`~/.zshrc`、`~/.bashrc` 或同类文件）：

```bash
export AVALONIA_TOOLS_LICENSE_KEY="your-license-key"
```

然后重新加载配置，或者开一个新终端：

```bash
source ~/.zshrc
```

</TabItem>
<TabItem value="windows-powershell" label="Windows (PowerShell)">

为你的用户账户设置一个持久的环境变量：

```powershell
[System.Environment]::SetEnvironmentVariable('AVALONIA_TOOLS_LICENSE_KEY', 'your-license-key', 'User')
```

重启所有已打开的终端和编辑器，让改动生效。

</TabItem>
<TabItem value="windows-cmd" label="Windows (Command Prompt)">

```cmd
setx AVALONIA_TOOLS_LICENSE_KEY "your-license-key"
```

重启所有已打开的终端和编辑器，让改动生效。

</TabItem>
</Tabs>

:::caution[从图形界面快捷方式启动的编辑器]
如果你的编辑器是从桌面快捷方式或应用菜单启动的（而非从终端启动），它可能不会继承 shell 配置里的环境变量。若 MCP 服务器报告缺少许可证密钥，可以在 MCP 配置中加一个 `env` 块直接设置：

```json
{
    "env": {
        "AVALONIA_TOOLS_LICENSE_KEY": "your-license-key"
    }
}
```

这个块该放在哪儿，请见下文针对各编辑器的配置说明。
:::

:::note
DevTools MCP 仅对 Avalonia Plus 及以上许可证开放。
:::

## 准备你的应用 {#prepare-your-application}

MCP 服务器通过 `AvaloniaUI.DiagnosticsSupport` 包与你的 Avalonia 应用通信。没有这个包和必需的启动调用，MCP 服务器既发现不了也挂接不上你运行中的应用。

:::caution[MCP 连通性的必备条件]
这一步是 `attach-to-app` 能跑起来的前提。省了它，MCP 服务器会反复连接失败，还给不出清晰的错误。`attach-to-file` 工具（XAML 预览器）虽然不需要应用在运行，但同样要求装上这个包。
:::

**1. 为项目添加诊断支持包：**

```bash
dotnet add package AvaloniaUI.DiagnosticsSupport
```

**2. 在应用启动时启用开发者工具。**

下面两种做法任选其一：

<Tabs>
<TabItem value="appbuilder" label="App builder (Program.cs)">

```csharp
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .WithDeveloperTools();
```

</TabItem>
<TabItem value="application" label="Application class (App.axaml.cs)">

```csharp
public override void Initialize()
{
    AvaloniaXamlLoader.Load(this);

#if DEBUG
    this.AttachDeveloperTools();
#endif
}
```

</TabItem>
</Tabs>

完整的安装流程（含各平台的具体要求和激活步骤）请见[安装 Avalonia Plus 开发者工具](/tools/developer-tools/installation)。

## 配置 MCP 服务器 {#setting-up-the-mcp-server}

DevTools 提供的 MCP 服务器以本地进程运行。底层命令是 `avdt mcp`，但你不必手动去跑它——配置好之后编辑器会自动把它拉起来。

:::note
`AVALONIA_TOOLS_LICENSE_KEY` 变量自 Avalonia 12.0.0 起启用。若你用的是 Avalonia 11.x.x 或更早版本，请改用 `ACCELERATE_LICENSE_KEY`。
:::

在下面选择你用的编辑器：

<Tabs groupId="editor">
<TabItem value="vscode" label="VS Code">

**方式 A：一键安装**

[为 VS Code 安装 DevTools MCP](https://vscode.dev/redirect/mcp/install?name=avalonia_devtools&config=%7b%22type%22%3a%22stdio%22%2c%22command%22%3a%22avdt%22%2c%22args%22%3a%5b%22mcp%22%5d%7d)

**方式 B：命令面板**

1. 打开命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`）。
2. Run **MCP: Add Server**.
3. 服务器类型选 **stdio**。
4. 命令填 `avdt mcp`。
5. 服务器名称设为 `avalonia_devtools`。
6. 选择把该服务器装到当前工作区还是全局。

**方式 C：手动配置**

把下列内容加进工作区根目录的 `.vscode/mcp.json`：

```json title=".vscode/mcp.json"
{
    "servers": {
        "avalonia_devtools": {
            "type": "stdio",
            "command": "avdt",
            "args": ["mcp"]
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
        "avalonia_devtools": {
            "type": "stdio",
            "command": "avdt",
            "args": ["mcp"]
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
2. 点击 **Add**，传输类型选 **stdio**。
3. 把命令设为 `avdt`，参数设为 `mcp`。
4. 服务器名称设为 `avalonia_devtools`。

**方式 B：手动配置**

在项目目录中新建或编辑 `.idea/mcp.json`：

```json title=".idea/mcp.json"
{
    "servers": {
        "avalonia_devtools": {
            "type": "stdio",
            "command": "avdt",
            "args": ["mcp"]
        }
    }
}
```

</TabItem>
<TabItem value="cursor" label="Cursor">

**方式 A：一键安装**

[为 Cursor 安装 DevTools MCP](https://cursor.com/en/install-mcp?name=avalonia_devtools&config=eyJ0eXBlIjoic3RkaW8iLCJjb21tYW5kIjoiYXZkdCIsImFyZ3MiOlsibWNwIl19)

**方式 B：手动配置**

把下列内容加进项目目录下的 `.cursor/mcp.json`，若要全局配置则加进 `~/.cursor/mcp.json`：

```json title=".cursor/mcp.json"
{
    "mcpServers": {
        "avalonia_devtools": {
            "command": "avdt",
            "args": ["mcp"]
        }
    }
}
```

</TabItem>
<TabItem value="claude-code" label="Claude Code">

在终端里运行这条命令：

```bash
claude mcp add --scope user avalonia_devtools -- avdt mcp
```

验证是否添加成功：

```bash
claude mcp list
```

</TabItem>
<TabItem value="claude-desktop" label="Claude Desktop">

1. 打开 **Settings** > **Developer**，点击 **Edit Config**。
2. 把 DevTools MCP 服务器加进 `claude_desktop_config.json`：

```json
{
    "mcpServers": {
        "avalonia_devtools": {
            "command": "avdt",
            "args": ["mcp"],
            "env": {
                "AVALONIA_TOOLS_LICENSE_KEY": "your-license-key"
            }
        }
    }
}
```

3. 保存文件并重启 Claude Desktop。

:::note
Claude Desktop 不会从你的 shell 配置里继承环境变量，所以许可证密钥必须像上面那样直接写进配置。
:::

</TabItem>
</Tabs>

## 验证连接 {#verify-the-connection}

配置好 MCP 服务器后，按下面的步骤确认它确实在工作：

1. **确认服务器正在运行。**打开编辑器的 MCP 面板或状态指示器，确认 `avalonia_devtools` 以已连接服务器的身份出现。在 VS Code 中，可从命令面板运行 **MCP: List Servers**。
2. **启动你的 Avalonia 应用**（若用的是预览器，则打开一个 XAML 文件）。
3. **用一句提示词试一下。**问问你的 AI 助手：

```text
"Connect to my running Avalonia app and show me the visual tree."
```

若助手返回了树形结构，就说明配置完成了。

## 排查问题 {#troubleshooting}

### 找不到 “avdt” 命令 {#avdt-command-not-found}

`avdt` 命令必须在系统 PATH 中。若你是作为全局 .NET 工具安装的，请检查 `$HOME/.dotnet/tools`（macOS/Linux）或 `%USERPROFILE%\.dotnet\tools`（Windows）是否在 PATH 里；若不在，把该目录加进去。

更多信息请见[排查 .NET 工具使用问题](https://learn.microsoft.com/en-us/dotnet/core/tools/troubleshoot-usage-issues#executable-file-not-found)。

### 检测不到许可证密钥 {#license-key-not-detected}

若 MCP 服务器起来了却报告许可证密钥缺失或无效：

- 在你启动编辑器的那个终端里运行 `echo $AVALONIA_TOOLS_LICENSE_KEY`（macOS/Linux）或 `echo %AVALONIA_TOOLS_LICENSE_KEY%`（Windows），**确认变量确实设上了**。
- **若你的编辑器是从图形界面快捷方式启动的**，它可能不会继承 shell 环境变量。请按上文[设置许可证密钥](#setting-your-license-key)一节所示，在 MCP 配置中加一个 `env` 块。

### 编辑器里看不到 MCP 服务器 {#mcp-server-does-not-appear-in-the-editor}

- 添加或修改 MCP 配置文件后，**请重启编辑器**。多数编辑器都要重启才能发现新的 MCP 服务器。
- **核对配置文件的位置。**每种编辑器都有各自约定的配置路径，请参照上文中你所用编辑器的配置说明。
- **检查 JSON 是否合法。**配置文件里的语法错误（漏逗号、多余的尾逗号、括号不配对）会悄无声息地让服务器加载不起来。

### 服务器连上了，却找不到应用 {#server-connects-but-cannot-find-the-application}

- **确认你的应用装了诊断包。**项目中必须添加 `AvaloniaUI.DiagnosticsSupport` NuGet 包，并在 app builder 上调用 `.WithDeveloperTools()`，或在 `Application` 类中调用 `this.AttachDeveloperTools()`。请见上文[准备你的应用](#prepare-your-application)。
- 在让助手连接之前，**先确保你的 Avalonia 应用已经在运行**。
- 若同时跑着多个 Avalonia 应用，助手会把它们列出来，问你要挂接哪一个。
- 预览 XAML 请用 `attach-to-file` 而非 `attach-to-app`。它连的是 XAML 预览器，不需要应用处于运行状态。

### 挂接不上正在运行的应用 {#cannot-attach-to-a-running-application}

这是初次配置 MCP 服务器时最常见的问题。`attach-to-app` 工具要求下列条件全部满足：

1. 项目中已安装 `AvaloniaUI.DiagnosticsSupport` 包。
2. 应用启动时调用了 `.WithDeveloperTools()` 或 `.AttachDeveloperTools()`。
3. 应用正在运行并已完全启动（过了启动画面或初始化阶段）。

只要有一条没满足，MCP 服务器就找不到你的应用。在应用里按 F12 对 MCP 连接没有任何帮助——那个快捷键打开的是独立的 DevTools 窗口，不是 MCP 连接。

### Updating DevTools

若工具表现得不对劲，请确认你用的是最新版本：

```bash
dotnet tool update -g avdt
```

## 可用的工具 {#available-tools}

### Connection

| 工具 | 说明 |
|------|-------------|
| `attach-to-app` | 连上正在运行的 Avalonia 应用。若同时跑着多个，会列出来让你选。 |
| `attach-to-file` | 为指定文件连上 XAML 预览器。预览 XAML 布局时推荐用它，而不是 `attach-to-app`。 |
| `detach` | 断开当前的应用或预览器会话。 |

### Inspection

| 工具 | 说明 |
|------|-------------|
| `tree` | 返回某个节点的子元素。传入 null 的 `nodeId` 可取得根元素。 |
| `ancestors` | 返回从某个节点一路向上直到根的父级链。 |
| `search` | 按类型名或 `x:Name` 查找元素。 |
| `screenshot` | 把指定 UI 元素截成 PNG 图片。 |

### 属性与样式 {#properties-and-styles}

| 工具 | 说明 |
|------|-------------|
| `props` | 返回某个节点的所有属性值。 |
| `set-prop` | 设置节点上某个属性的值。用 `null` 或 `unset` 可清除取值。 |
| `styles` | 返回作用于某个节点的样式及其 setter。 |
| `pseudo-class` | 在节点上激活某个伪类（比如 `:pointerover`）。不写伪类名则会列出可选项。 |

### 资源与资产 {#resources-and-assets}

| 工具 | 说明 |
|------|-------------|
| `resources` | 返回应用中定义的资源，也可限定在某个节点的范围内。 |
| `assets` | 列出嵌入的资产（图片、字体），返回可配合 `open-asset` 使用的 URL。 |
| `open-asset` | 按 URL 下载嵌入的资产（URL 由 `assets` 工具返回）。 |

### Interaction

| 工具 | 说明 |
|------|-------------|
| `input` | 向某个 UI 元素发送输入事件（点击、按键等）。 |
| `action` | 在某个 UI 元素上执行更高层级的操作。 |

## 用法示例 {#usage-examples}

用自然语言说清你想做什么，AI 助手会自动调用相应的 MCP 工具：

**Inspecting UI:**

```text
"Connect to my running app and show me the visual tree structure."
```

**查找元素：**

```text
"Find all Button elements in my application."
```

**调试样式：**

```text
"What styles are applied to the MainWindow?"
```

**截图：**

```text
"Take a screenshot of the login panel."
```

**在运行时修改属性：**

```text
"Set the Background of the sidebar panel to #F0F0F0."
```

**借助截图打磨界面设计：**

下面这段提示词演示了一套完整的设计迭代流程。AI 助手写 XAML，用 `attach-to-file` 预览，截图，再不断改进，直到结果贴合目标设计：

```text
"Create an Avalonia application and recreate the attached UI. You can write XAML
and prefer MVVM-friendly code. Use the Avalonia MCP server to periodically confirm
if designs match. Design for the light theme. If the design doesn't match, you must
continue to iterate on it until it does. Use the Avalonia MVVM template and install
AvaloniaUI.DiagnosticsSupport and add .WithDeveloperTools() to the app builder to
enable MCP. Only use the attach-to-file tool. Don't call detach. You don't need to
rebuild the project on change."
```

这段提示词之所以好使，是因为它：

- 明确让助手用 `attach-to-file`（它连的是 XAML 预览器，不必重新构建）。
- 把应用的接入步骤（`DiagnosticsSupport` + `.WithDeveloperTools()`）直接写进了提示词，助手一上来就能把项目配置对。
- 构成了一个反馈闭环，助手会一轮轮迭代直到设计吻合。

## 另请参阅 {#see-also}

- [AI 工具概述](/tools/ai-tools/)
- [安装 DevTools](/tools/developer-tools/installation)
- [Parcel MCP](/tools/parcel/mcp)
