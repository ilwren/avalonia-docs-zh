---
id: setup
title: 配置 Avalonia Parcel
description: 安装、配置并激活 Avalonia Parcel——用于在 Windows、macOS 和 Linux 上构建、签名并打包 Avalonia 应用的打包工具。
sidebar_label: 配置
sidebar_position: 1
doc-type: tutorial
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

Avalonia Parcel 是面向 Avalonia 应用的打包工具，既有图形界面（GUI）也有命令行界面（CLI）。你可以用它为 Windows、macOS 和 Linux 构建、签名并打包应用。

## 前置条件 {#prerequisites}

| 要求 | Version/Details |
|------------|-----------------|
| .NET Runtime | 6.0 或更高 |
| Windows | 10 或更高 |
| macOS | 13 或更高 |
| Linux | X11，且兼容 glibc 2.27 或 musl 1.22.2 的发行版 |

## Step 1: Install Avalonia Parcel

Avalonia Parcel 是一个 [.NET 工具](https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools)，用 .NET SDK 安装和更新即可。

本指南演示的是全局安装。你也可以本地安装，但那样只在安装它的那个项目里管用。

<Tabs>
<TabItem value="net10" label=".NET 10+" default>

```bash
dotnet tool install --global AvaloniaUI.Parcel
```

若你装过 .NET 8 或 .NET 9 版的 Parcel，请先运行 `dotnet tool uninstall --global AvaloniaUI.Parcel.Windows` 或 `parcel uninstall`。

用下面的命令更新 Parcel：

```bash
dotnet tool update --global AvaloniaUI.Parcel
```

</TabItem>
<TabItem value="net8" label=".NET 8/9">

若你用的 .NET SDK 版本低于 10，请安装对应你所在平台的包。

<details>
<summary>安装命令</summary>

**Windows:**

```bash
dotnet tool install --global AvaloniaUI.Parcel.Windows
```

**macOS:**

```bash
dotnet tool install --global AvaloniaUI.Parcel.macOS
```

**Linux:**

```bash
dotnet tool install --global AvaloniaUI.Parcel.Linux
```

</details>

用对应你所在平台的命令更新 Parcel。

<details>
<summary>更新命令</summary>

**Windows:**

```bash
dotnet tool update --global AvaloniaUI.Parcel.Windows
```

**macOS:**

```bash
dotnet tool update --global AvaloniaUI.Parcel.macOS
```

**Linux:**

```bash
dotnet tool update --global AvaloniaUI.Parcel.Linux
```

</details>

</TabItem>
</Tabs>

:::warning
在 macOS 或 Linux 上，安装程序未必会把安装目录加进 `PATH` 环境变量，这时运行 `parcel` 时 shell 会报 “command not found”。

把工具目录加进 `PATH`，默认目录通常是 `$HOME/.dotnet/tools`。

更多信息请见[排查 .NET 工具使用问题](https://learn.microsoft.com/en-us/dotnet/core/tools/troubleshoot-usage-issues#executable-file-not-found)。
:::

## 第 2 步：运行工具 {#step-2-run-the-tool}

装好之后，在终端里运行 Parcel：

```bash
parcel
```

这条命令会打开 Parcel 的图形界面，你可以在其中打开或新建 Parcel 项目。

你也可以对已有的 Parcel 项目执行 CLI 命令：

```bash
parcel pack ./SampleApp.parcel -r osx-x64 -p dmg -o ./artifacts
```

这条命令会按 Parcel 项目把应用打包并签名，然后生成一个 DMG 文件。

:::note
免费的社区许可证不含 CLI。
:::

## 第 3 步：激活工具 {#step-3-activate-the-tool}

Parcel 打开后，用持有该工具许可证的 Avalonia 门户账号登录。

对 CLI，可使用 `--license-key` 选项；也可以设置 `AVALONIA_TOOLS_LICENSE_KEY` 环境变量，或者先在 Parcel 图形界面中登录、让 CLI 复用那个会话。

## Further Reading

- [Parcel 命令行参考](/tools/parcel/command-line-reference)
- [Parcel 配置参考](/tools/parcel/configuration-reference)
- [模型上下文协议（MCP）](/tools/parcel/mcp)
- [Windows 打包](/tools/parcel/packaging-for-windows)
- [macOS 打包](/tools/parcel/packaging-for-macos)
- [Linux 打包](/tools/parcel/packaging-for-linux)
