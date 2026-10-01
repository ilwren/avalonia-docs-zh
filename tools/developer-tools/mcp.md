---
id: mcp
title: DevTools MCP
sidebar_label: DevTools MCP
doc-type: how-to
description: "Set up the DevTools MCP server to let AI assistants inspect, debug, and modify your running Avalonia application."
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

## What is DevTools MCP?

The DevTools MCP server lets AI assistants connect to a running Avalonia application and interact with it directly. Your assistant can inspect the visual tree, search for elements by type or name, read and modify properties, capture screenshots, and send input events. It can also attach to the XAML previewer, making it a useful companion for iterating on layouts without leaving your editor.

关于 MCP 的总体介绍，请见 [AI 工具](/tools/ai-tools/)。

## 前置条件 {#prerequisites}

配置 MCP 服务器前，请先确认你具备：

1. **DevTools .NET tool** installed. Follow the [Getting Started](/tools/developer-tools/installation) guide.
2. **Valid Avalonia Plus license key.** You can get one from the [Avalonia portal](https://portal.avaloniaui.net/).

### Setting your license key

The MCP server reads your license from the `AVALONIA_TOOLS_LICENSE_KEY` environment variable. You can find your license key in the [Avalonia customer portal](https://portal.avaloniaui.net/). MCP is a paid feature and is not included with the Community license.

:::note
The `AVALONIA_TOOLS_LICENSE_KEY` variable is used from Avalonia 12.0.0. If you are on Avalonia 11.x.x or earlier versions, please use `ACCELERATE_LICENSE_KEY` instead.
:::

Set the key in your shell profile so it persists across sessions:

<Tabs>
<TabItem value="macos-linux" label="macOS / Linux">

Add this line to your shell profile (`~/.zshrc`, `~/.bashrc`, or equivalent):

```bash
export AVALONIA_TOOLS_LICENSE_KEY="your-license-key"
```

Then reload the profile or open a new terminal:

```bash
source ~/.zshrc
```

</TabItem>
<TabItem value="windows-powershell" label="Windows (PowerShell)">

Set a persistent environment variable for your user account:

```powershell
[System.Environment]::SetEnvironmentVariable('AVALONIA_TOOLS_LICENSE_KEY', 'your-license-key', 'User')
```

Restart any open terminals and editors to pick up the change.

</TabItem>
<TabItem value="windows-cmd" label="Windows (Command Prompt)">

```cmd
setx AVALONIA_TOOLS_LICENSE_KEY "your-license-key"
```

Restart any open terminals and editors to pick up the change.

</TabItem>
</Tabs>

:::caution[Editors launched from GUI shortcuts]
If you launch your editor from a desktop shortcut or application menu (rather than from a terminal), it may not inherit environment variables from your shell profile. If the MCP server reports a missing license key, you can set it directly in the MCP configuration by adding an `env` block:

```json
{
    "env": {
        "AVALONIA_TOOLS_LICENSE_KEY": "your-license-key"
    }
}
```

See the editor-specific setup instructions below for where to place this block.
:::

:::note
DevTools MCP is only available with an Avalonia Plus license or higher.
:::

## Prepare your application

The MCP server communicates with your Avalonia application through the `AvaloniaUI.DiagnosticsSupport` package. Without this package and the required startup call, the MCP server cannot discover or attach to your running app.

:::caution[Required for MCP connectivity]
This step is required for `attach-to-app` to work. If you skip it, the MCP server will repeatedly fail to connect with no clear error. The `attach-to-file` tool (XAML previewer) does not require a running application, but still requires the package to be installed.
:::

**1. Add the diagnostics support package to your project:**

```bash
dotnet add package AvaloniaUI.DiagnosticsSupport
```

**2. Enable developer tools in your application startup.**

Choose one of the following approaches:

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

For the full installation walkthrough, including platform-specific requirements and activation, see [Installing the Avalonia Plus developer tools](/tools/developer-tools/installation).

## 配置 MCP 服务器 {#setting-up-the-mcp-server}

DevTools provides an MCP server that runs as a local process. The underlying command is `avdt mcp`, but you do not need to run it manually. Your editor starts it automatically once configured.

:::note
The `AVALONIA_TOOLS_LICENSE_KEY` variable is used from Avalonia 12.0.0. If you are on Avalonia 11.x.x or earlier versions, please use `ACCELERATE_LICENSE_KEY` instead.
:::

Choose your editor below:

<Tabs groupId="editor">
<TabItem value="vscode" label="VS Code">

**Option A: One-click install**

[Install DevTools MCP for VS Code](https://vscode.dev/redirect/mcp/install?name=avalonia_devtools&config=%7b%22type%22%3a%22stdio%22%2c%22command%22%3a%22avdt%22%2c%22args%22%3a%5b%22mcp%22%5d%7d)

**Option B: Command palette**

1. 打开命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`）。
2. Run **MCP: Add Server**.
3. 服务器类型选 **stdio**。
4. 命令填 `avdt mcp`。
5. 服务器名称设为 `avalonia_devtools`。
6. 选择把该服务器装到当前工作区还是全局。

**Option C: Manual configuration**

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
2. Click **Add** and select **stdio** as the transport type.
3. Set the command to `avdt` with argument `mcp`.
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

**Option A: One-click install**

[Install DevTools MCP for Cursor](https://cursor.com/en/install-mcp?name=avalonia_devtools&config=eyJ0eXBlIjoic3RkaW8iLCJjb21tYW5kIjoiYXZkdCIsImFyZ3MiOlsibWNwIl19)

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

1. Open **Settings** > **Developer** and click **Edit Config**.
2. Add the DevTools MCP server to `claude_desktop_config.json`:

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

3. Save the file and restart Claude Desktop.

:::note
Claude Desktop does not inherit environment variables from your shell profile, so the license key must be set directly in the configuration as shown above.
:::

</TabItem>
</Tabs>

## 验证连接 {#verify-the-connection}

配置好 MCP 服务器后，按下面的步骤确认它确实在工作：

1. **Check the server is running.** Open your editor's MCP panel or status indicator and confirm `avalonia_devtools` appears as a connected server. In VS Code, run **MCP: List Servers** from the command palette.
2. **Start your Avalonia application** (or open a XAML file if using the previewer).
3. **用一句提示词试一下。**问问你的 AI 助手：

```text
"Connect to my running Avalonia app and show me the visual tree."
```

If the assistant returns the tree structure, setup is complete.

## 排查问题 {#troubleshooting}

### "avdt" command not found

The `avdt` command must be on your system PATH. If you installed it as a global .NET tool, check if `$HOME/.dotnet/tools` (macOS/Linux) or `%USERPROFILE%\.dotnet\tools` (Windows) is in your PATH. If not, add the directory to your PATH.

For more information, see [Troubleshooting .NET tool usage issues](https://learn.microsoft.com/en-us/dotnet/core/tools/troubleshoot-usage-issues#executable-file-not-found).

### License key not detected

If the MCP server starts but reports a missing or invalid license key:

- **Confirm the variable is set** by running `echo $AVALONIA_TOOLS_LICENSE_KEY` (macOS/Linux) or `echo %AVALONIA_TOOLS_LICENSE_KEY%` (Windows) in the same terminal where you launch your editor.
- **If your editor is launched from a GUI shortcut**, it may not inherit shell environment variables. Add an `env` block to your MCP configuration as shown in the [license key setup](#setting-your-license-key) section above.

### 编辑器里看不到 MCP 服务器 {#mcp-server-does-not-appear-in-the-editor}

- 添加或修改 MCP 配置文件后，**请重启编辑器**。多数编辑器都要重启才能发现新的 MCP 服务器。
- **核对配置文件的位置。**每种编辑器都有各自约定的配置路径，请参照上文中你所用编辑器的配置说明。
- **检查 JSON 是否合法。**配置文件里的语法错误（漏逗号、多余的尾逗号、括号不配对）会悄无声息地让服务器加载不起来。

### Server connects but cannot find the application

- **Verify your app has the diagnostics package installed.** The `AvaloniaUI.DiagnosticsSupport` NuGet package must be added to your project, and you must call `.WithDeveloperTools()` on your app builder or `this.AttachDeveloperTools()` in your `Application` class. See [Prepare your application](#prepare-your-application) above.
- **Ensure your Avalonia application is running** before asking the assistant to connect.
- If multiple Avalonia apps are running, the assistant will list them and ask which one to attach to.
- For XAML previewing, use `attach-to-file` instead of `attach-to-app`. This connects to the XAML previewer and does not require a running application.

### Cannot attach to a running application

This is the most common issue when first setting up the MCP server. The `attach-to-app` tool requires all of the following:

1. The `AvaloniaUI.DiagnosticsSupport` package is installed in your project.
2. `.WithDeveloperTools()` or `.AttachDeveloperTools()` is called at app startup.
3. The application is running and has fully started (past the splash screen or initialization phase).

If any of these are missing, the MCP server will fail to find your application. Pressing F12 in your app has no effect on MCP connectivity; that shortcut opens the standalone DevTools window, not the MCP connection.

### Updating DevTools

If tools behave unexpectedly, ensure you are running the latest version:

```bash
dotnet tool update -g avdt
```

## 可用的工具 {#available-tools}

### Connection

| 工具 | 说明 |
|------|-------------|
| `attach-to-app` | Connects to a running Avalonia app. If multiple apps are running, lists them for selection. |
| `attach-to-file` | Connects to the XAML previewer for a specified file. Recommended over `attach-to-app` for previewing XAML layouts. |
| `detach` | Disconnects from the current app or previewer session. |

### Inspection

| 工具 | 说明 |
|------|-------------|
| `tree` | Returns child elements of a node. Pass a null `nodeId` to get the root elements. |
| `ancestors` | Returns the parent chain from a node up to the root. |
| `search` | Finds elements by type name or `x:Name`. |
| `screenshot` | Captures a PNG screenshot of a specific UI element. |

### Properties and styles

| 工具 | 说明 |
|------|-------------|
| `props` | Returns all property values for a node. |
| `set-prop` | Sets a property value on a node. Use `null` or `unset` to clear a value. |
| `styles` | Returns applied styles and their setters for a node. |
| `pseudo-class` | Activates a pseudo-class on a node (for example, `:pointerover`). Omit the pseudo-class name to list available options. |

### Resources and assets

| 工具 | 说明 |
|------|-------------|
| `resources` | Returns resources defined in the application. Optionally scoped to a specific node. |
| `assets` | Lists embedded assets (images, fonts). Returns URLs for use with `open-asset`. |
| `open-asset` | Downloads an embedded asset by its URL (as returned by the `assets` tool). |

### Interaction

| 工具 | 说明 |
|------|-------------|
| `input` | Sends an input event (click, key press, etc.) to a UI element. |
| `action` | Performs a higher-level action on a UI element. |

## 用法示例 {#usage-examples}

用自然语言说清你想做什么，AI 助手会自动调用相应的 MCP 工具：

**Inspecting UI:**

```text
"Connect to my running app and show me the visual tree structure."
```

**Finding elements:**

```text
"Find all Button elements in my application."
```

**Debugging styles:**

```text
"What styles are applied to the MainWindow?"
```

**Taking screenshots:**

```text
"Take a screenshot of the login panel."
```

**Modifying properties at runtime:**

```text
"Set the Background of the sidebar panel to #F0F0F0."
```

**Iterating on UI design with screenshots:**

The following prompt demonstrates a complete design iteration workflow. The AI assistant writes XAML, previews it with `attach-to-file`, takes screenshots, and keeps refining until the result matches the target design:

```text
"Create an Avalonia application and recreate the attached UI. You can write XAML
and prefer MVVM-friendly code. Use the Avalonia MCP server to periodically confirm
if designs match. Design for the light theme. If the design doesn't match, you must
continue to iterate on it until it does. Use the Avalonia MVVM template and install
AvaloniaUI.DiagnosticsSupport and add .WithDeveloperTools() to the app builder to
enable MCP. Only use the attach-to-file tool. Don't call detach. You don't need to
rebuild the project on change."
```

This prompt works well because it:

- Tells the assistant to use `attach-to-file` (which connects to the XAML previewer without needing to rebuild).
- Includes the app instrumentation instructions (`DiagnosticsSupport` + `.WithDeveloperTools()`) directly in the prompt, so the assistant sets up the project correctly from the start.
- Creates a feedback loop where the assistant keeps iterating until the design matches.

## 另请参阅 {#see-also}

- [AI 工具概述](/tools/ai-tools/)
- [DevTools installation](/tools/developer-tools/installation)
- [Parcel MCP](/tools/parcel/mcp)
