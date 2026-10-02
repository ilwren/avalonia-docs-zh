---
id: installation
title: 安装 Avalonia Plus 开发者工具
sidebar_label: 安装
sidebar_position: 1
doc-type: tutorial
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

在本教程中，你将安装 Avalonia Plus 开发者工具，为项目添加诊断支持包，并验证应用与工具之间的连接。

## 前置条件 {#prerequisites}

### 开发者工具的环境要求 {#developer-tools-requirements}

| 要求 | Version/Details |
|------------|-----------------|
| .NET Runtime | 6.0 或更高 |
| Windows | 10 或更高 |
| macOS | 13 或更高 |
| Linux | X11，且兼容 glibc 2.27 或 musl 1.22.2 的发行版 |

运行该工具不需要管理员/sudo 权限。若你打算远程使用开发者工具，可能得为防火墙加一条例外规则。

### 诊断支持包的要求 {#diagnostics-support-requirements}

支持包需要 **Avalonia 11.2.0** 或更高版本，并构建在兼容 **.NET Standard 2.0** 的 API 之上。

该包同样适用于 Browser 和 Android/iOS 项目。

## Step 1: Installing AvaloniaUI Developer Tools

AvaloniaUI 开发者工具目前是一个原生的 [.NET 工具](https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools)，更新机制由 SDK 提供。
本指南演示的是全局安装。本地安装也可以，但有个限制：这样安装的工具只能在安装它的解决方案/项目所在目录或其子目录下使用。

<Tabs>
<TabItem value="net10" label=".NET 10+" default>

```bash
dotnet tool install --global AvaloniaUI.DeveloperTools
```

若你是从 .NET 8/9 的安装升级而来，应先用 `dotnet tool uninstall --global AvaloniaUI.DeveloperTools.Windows` 或 `avdt uninstall` 卸载旧版。

之后运行 `dotnet tool update` 命令即可更新开发者工具。

```bash
dotnet tool update --global AvaloniaUI.DeveloperTools
```

</TabItem>
<TabItem value="net8" label=".NET 8/9">

若你用的 .NET SDK 低于 10，就得按运行平台安装对应的专用包。

<details>
<summary>安装命令</summary>

**Windows:**

```bash
dotnet tool install --global AvaloniaUI.DeveloperTools.Windows
```

**macOS:**

```bash
dotnet tool install --global AvaloniaUI.DeveloperTools.macOS
```

**Linux:**

```bash
dotnet tool install --global AvaloniaUI.DeveloperTools.Linux
```

</details>

之后运行 `dotnet tool update` 命令即可更新开发者工具。

<details>
<summary>更新命令</summary>

**Windows:**

```bash
dotnet tool update --global AvaloniaUI.DeveloperTools.Windows
```

**macOS:**

```bash
dotnet tool update --global AvaloniaUI.DeveloperTools.macOS
```

**Linux:**

```bash
dotnet tool update --global AvaloniaUI.DeveloperTools.Linux
```

</details>

</TabItem>
</Tabs>

:::warning
在 macOS 或 Linux 上，安装位置未必会自动加进 PATH 环境变量，表现为运行 `avdt` 时报 “command not found”。

要解决这个问题，请把工具所在位置追加到 PATH 环境变量中。默认位置通常是 `$HOME/.dotnet/tools`。

更多信息请见[排查 .NET 工具使用问题](https://learn.microsoft.com/en-us/dotnet/core/tools/troubleshoot-usage-issues#global-tools)。
:::

## 第 2 步：安装诊断支持包 {#step-2-installing-diagnostics-support-package}

`Diagnostics Support` 包负责在用户应用与开发者工具进程之间架起连接的桥梁。

视你的应用架构而定，这个包既可以装在带 Program AppBuilder 的可执行项目里，也可以装在带 Application 的共享项目里。

两种情况下命令都一样：

```bash
dotnet add package AvaloniaUI.DiagnosticsSupport
```

:::note

旧的 `Avalonia.Diagnostics` 包可以放心移除，新的 `Developer Tools` 不再用它。

:::

## 第 3 步：配置你的项目 {#step-3-configuring-your-project}

装好 `DiagnosticsSupport` 包之后，你需要在 `Application` 类中把它启用：

```csharp
public override void Initialize()
{
    AvaloniaXamlLoader.Load(this);

#if DEBUG
    this.AttachDeveloperTools();
#endif
}
```

此外也可以在 AppBuilder 上使用 `.WithDeveloperTools()` 扩展方法。

这些方法还接受一个 `DeveloperToolsOptions` 选项类，可用来定制 `Diagnostics Support` 的配置。更多细节见 [DeveloperToolsOptions 参考](/tools/developer-tools/options)。

默认用的是 **29414** 端口，一般都空着可用。该端口可通过选项配置。

## 第 4 步：运行工具 {#step-4-run-the-tool}

目标应用跑起来之后，按 <kbd>F12</kbd> 建立连接。
`Diagnostics Support` 会自动启动 `Developer Tools` 可执行文件，并在两个进程之间发起连接。
在 `macOS` 上首次执行可能要等上几秒，这是 Gatekeeper 在做校验，之后再启动就快了。

## 第 5 步：激活工具 {#step-5-activate-the-tool}

开发者工具打开后，会让你输入为该工具授权时所用的 `AvaloniaUI Portal` 凭据。这是整个过程中唯一需要联网的环节，此后工具便可离线使用，直到许可证密钥会话到期为止。

![激活工具](/img/tools/dev-tools/tool-activation.png)

## 第 6 步：大功告成！ {#step-6-done}

激活之后，与应用的连接会恢复，工具窗口随之打开。 

## 另请参阅 {#see-also}

- [元素工具](/tools/developer-tools/elements-tool)文档
- 自定义 [DeveloperToolsOptions 配置](/tools/developer-tools/options)参考
- [模型上下文协议（MCP）](/tools/developer-tools/mcp)
- [Frequently Asked Questions](/tools/faq)
- [Settings](/tools/developer-tools/settings)
- [Shortcuts](/tools/developer-tools/shortcuts)
- [挂接浏览器或移动端应用](/tools/developer-tools/attaching-applications)
- [挂接到远程工具](/tools/developer-tools/attaching-to-the-remote-tool)
- [反馈问题](/troubleshooting/tools/developer-tools)