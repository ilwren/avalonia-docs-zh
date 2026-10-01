---
id: mcp
title: Parcel MCP
sidebar_label: Parcel MCP
doc-type: how-to
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

## Parcel MCP 是什么？ {#what-is-parcel-mcp}

Parcel MCP 服务器让 AI 助手用上 Parcel 的打包能力。助手可以从 .NET 项目生成打包配置，也可以配置代码签名与公证，并为 Windows、macOS 和 Linux 构建安装包。

关于 MCP 的总体介绍，请见 [AI 工具](/tools/ai-tools/)。

## 前置条件 {#prerequisites}

配置 MCP 服务器之前，请确认你备齐了这些：

1. **已安装 Parcel .NET 工具。**请按[配置指南](/tools/parcel/setup)操作。
2. **有效的 Avalonia Plus 许可证密钥。**可在 [Avalonia 门户](https://portal.avaloniaui.net/)获取。

### 设置许可证密钥 {#setting-your-license-key}

MCP 服务器从 `AVALONIA_TOOLS_LICENSE_KEY` 环境变量读取许可证。许可证密钥可在 [Avalonia 门户](https://portal.avaloniaui.net/)获取。Parcel MCP 属于付费功能，Community 版不含此项。

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
若你的编辑器是从桌面快捷方式或应用菜单启动的，它可能读不到 shell 配置里的环境变量。当 MCP 服务器报告缺少许可证密钥时，请在 MCP 配置中加一个 `env` 块：

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
Parcel MCP 仅对完整的 [Avalonia Plus](https://avaloniaui.net/pricing) 许可证开放。
:::

## 配置 MCP 服务器 {#setting-up-the-mcp-server}

Parcel MCP 服务器以本地进程运行，命令是 `parcel mcp`。你不必手动跑它——配置好之后编辑器会自动把服务器拉起来。

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
2. 把 Parcel MCP 服务器加进 `claude_desktop_config.json`：

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

配置好 MCP 服务器后，测一下连接：

1. **确认服务器正在运行。**打开编辑器的 MCP 面板或状态指示器，确认 `parcel` 以已连接服务器的身份出现。在 VS Code 中，可从命令面板运行 **MCP: List Servers**。
2. **用一句提示词试一下。**问问你的 AI 助手：

```text
"List the available Parcel packaging tools."
```

若助手列出了一串能力清单，说明连接没问题。

## 排查问题 {#troubleshooting}

### 找不到 “parcel” 命令 {#parcel-command-not-found}

`parcel` 命令必须在系统 `PATH` 中。若装的是全局 .NET 工具，请在 macOS 和 Linux 上查看 `$HOME/.dotnet/tools`，在 Windows 上查看 `%USERPROFILE%\.dotnet\tools`；若相应目录不在 `PATH` 里，把它加进去。

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

若这些工具表现得不对劲，请确认你用的是最新版本：

```bash
dotnet tool update --global AvaloniaUI.Parcel
```

## Capabilities

配置好 MCP 服务器后，你的 AI 助手可以帮你：

### 项目配置 {#project-configuration}

- 从既有的 .NET 项目**生成 Parcel 配置**
- **配置应用属性**，比如包名、显示名、图标和应用包标识符
- 为多平台、多架构**设置构建目标**

### 配置代码签名 {#code-signing-setup}

- **Windows Azure Artifact Signing**——配置证书和签名参数
- **macOS 代码签名**——配置 P12 证书和描述文件
- **macOS 公证**——配置 Apple ID 和 App 专用密码

### 构建与打包 {#building-and-packaging}

- 为多个平台（Windows、macOS、Linux）**构建并打包**应用
- **生成** NSIS、MSIX、DMG、PKG、DEB、RPM 和 ZIP 格式的**安装包**
- **跨平台打包**，输出各运行时对应的产物

## 用法示例 {#usage-examples}

用自然语言说清你想做什么，AI 助手会自动调用相应的 MCP 工具：

**准备项目：**

```text
"Create a packaging config for my Avalonia project and set up macOS signing."
```

**打包：**

```text
"Package my app for macOS as a DMG with code signing enabled."
```

**管理配置：**

```text
"Update my app's display name and icon, then rebuild the Windows installer."
```

<Video src="/video/parcel/parcel_mcp.mp4" title="Parcel MCP server in action" aspectRatio="1492 / 958" maxWidth="100%" />

## 另请参阅 {#see-also}

- [AI 工具概述](/tools/ai-tools/)
- [Parcel 配置准备](/tools/parcel/setup)
- [Parcel 配置参考](/tools/parcel/configuration-reference)
- [DevTools MCP](/tools/developer-tools/mcp)
