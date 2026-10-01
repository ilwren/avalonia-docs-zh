---
id: mcp
title: Parcel MCP
sidebar_label: Parcel MCP
doc-type: how-to
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## What is Parcel MCP?

The Parcel MCP server lets AI assistants use Parcel packaging tools. Your assistant can create packaging configurations from .NET projects. It can also configure code signing and notarization, and build packages for Windows, macOS, and Linux.

关于 MCP 的总体介绍，请见 [AI 工具](/tools/ai-tools/)。

## 前置条件 {#prerequisites}

Before you configure the MCP server, make sure that you have these items:

1. **Parcel .NET tool installed.** Follow the [Setup guide](/tools/parcel/setup).
2. **有效的 Avalonia Plus 许可证密钥。**可在 [Avalonia 门户](https://portal.avaloniaui.net/)获取。

### 设置许可证密钥 {#setting-your-license-key}

The MCP server reads the license from the `AVALONIA_TOOLS_LICENSE_KEY` environment variable. Get your license key from the [Avalonia Portal](https://portal.avaloniaui.net/). Parcel MCP is a paid feature and is not included with the Community edition.

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
If you start your editor from a desktop shortcut or application menu, it might not read environment variables from your shell profile. If the MCP server reports a missing license key, add an `env` block to the MCP configuration:

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
Parcel MCP is only available with a full [Avalonia Plus](https://avaloniaui.net/pricing) license.
:::

## 配置 MCP 服务器 {#setting-up-the-mcp-server}

The Parcel MCP server runs as a local process. Its command is `parcel mcp`. You do not need to run this command manually. After configuration, your editor starts the server automatically.

在下面选择你用的编辑器：

<Tabs groupId="editor">
<TabItem value="vscode" label="VS Code">

**方式 A：命令面板**

1. 打开命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`）。
2. Run **MCP: Add Server**.
3. 服务器类型选 **stdio**。
4. 命令填 `parcel mcp`。
5. 服务器名称设为 `parcel`。
6. 选择把该服务器装到当前工作区还是全局。

**方式 B：手动配置**

把下列内容加进工作区根目录的 `.vscode/mcp.json`：

```json title=".vscode/mcp.json"
{
    "servers": {
        "parcel": {
            "type": "stdio",
            "command": "parcel",
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
        "parcel": {
            "type": "stdio",
            "command": "parcel",
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
3. 把命令设为 `parcel`，参数设为 `mcp`。
4. 服务器名称设为 `parcel`。

**方式 B：手动配置**

在项目目录中新建或编辑 `.idea/mcp.json`：

```json title=".idea/mcp.json"
{
    "servers": {
        "parcel": {
            "type": "stdio",
            "command": "parcel",
            "args": ["mcp"]
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
        "parcel": {
            "command": "parcel",
            "args": ["mcp"]
        }
    }
}
```

</TabItem>
<TabItem value="claude-code" label="Claude Code">

在终端里运行这条命令：

```bash
claude mcp add --scope user parcel -- parcel mcp
```

验证是否添加成功：

```bash
claude mcp list
```

</TabItem>
<TabItem value="claude-desktop" label="Claude Desktop">

1. 打开 **Settings** > **Developer**，点击 **Edit Config**。
2. Add the Parcel MCP server to `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "parcel": {
            "command": "parcel",
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

After you configure the MCP server, test the connection:

1. **确认服务器正在运行。**打开编辑器的 MCP 面板或状态指示器，确认 `parcel` 以已连接服务器的身份出现。在 VS Code 中，可从命令面板运行 **MCP: List Servers**。
2. **用一句提示词试一下。**问问你的 AI 助手：

```text
"List the available Parcel packaging tools."
```

If the assistant returns a list of capabilities, the connection works.

## 排查问题 {#troubleshooting}

### "parcel" command not found

The `parcel` command must be on the system `PATH`. For a global .NET tool installation, check for `$HOME/.dotnet/tools` on macOS and Linux. On Windows, check for `%USERPROFILE%\.dotnet\tools`. If the applicable directory is not in `PATH`, add it.

更多信息请见[排查 .NET 工具使用问题](https://learn.microsoft.com/en-us/dotnet/core/tools/troubleshoot-usage-issues#executable-file-not-found)。

### 检测不到许可证密钥 {#license-key-not-detected}

若 MCP 服务器起来了却报告许可证密钥缺失或无效：

- 在你启动编辑器的那个终端里运行 `echo $AVALONIA_TOOLS_LICENSE_KEY`（macOS/Linux）或 `echo %AVALONIA_TOOLS_LICENSE_KEY%`（Windows），**确认变量确实设上了**。
- **若你的编辑器是从图形界面快捷方式启动的**，它可能不会继承 shell 环境变量。请按上文[设置许可证密钥](#setting-your-license-key)一节所示，在 MCP 配置中加一个 `env` 块。

### 编辑器里看不到 MCP 服务器 {#mcp-server-does-not-appear-in-the-editor}

- 添加或修改 MCP 配置文件后，**请重启编辑器**。多数编辑器都要重启才能发现新的 MCP 服务器。
- **核对配置文件的位置。**每种编辑器都有各自约定的配置路径，请参照上文中你所用编辑器的配置说明。
- **检查 JSON 是否合法。**配置文件里的语法错误（漏逗号、多余的尾逗号、括号不配对）会悄无声息地让服务器加载不起来。

### Updating Parcel

If the tools do not work as expected, make sure that you use the latest version:

```bash
dotnet tool update --global AvaloniaUI.Parcel
```

## Capabilities

Once the MCP server is configured, your AI assistant can help with:

### 项目配置 {#project-configuration}

- **Create Parcel configurations** from existing .NET projects
- **Configure application properties** like package name, display name, icons, and bundle identifiers
- **Set up build targets** for multiple platforms and architectures

### Code signing setup

- **Windows Azure Artifact Signing** - Configure certificates and signing parameters
- **macOS Code Signing** - Set up P12 certificates and provisioning profiles
- **macOS Notarization** - Configure Apple ID and app-specific passwords

### Building and packaging

- **Build and package** applications for multiple platforms (Windows, macOS, Linux)
- **Generate packages** in NSIS, MSIX, DMG, PKG, DEB, RPM, and ZIP formats
- **Cross-platform packaging** with runtime-specific outputs

## 用法示例 {#usage-examples}

用自然语言说清你想做什么，AI 助手会自动调用相应的 MCP 工具：

**Project setup:**

```text
"Create a packaging config for my Avalonia project and set up macOS signing."
```

**Packaging:**

```text
"Package my app for macOS as a DMG with code signing enabled."
```

**Configuration management:**

```text
"Update my app's display name and icon, then rebuild the Windows installer."
```

<Video src="/video/parcel/parcel_mcp.mp4" title="Parcel MCP server in action" aspectRatio="1492 / 958" maxWidth="100%" />

## 另请参阅 {#see-also}

- [AI 工具概述](/tools/ai-tools/)
- [Parcel setup](/tools/parcel/setup)
- [Parcel configuration reference](/tools/parcel/configuration-reference)
- [DevTools MCP](/tools/developer-tools/mcp)
