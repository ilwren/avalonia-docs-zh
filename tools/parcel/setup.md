---
id: setup
title: Setting up Avalonia Parcel
description: Install, configure, and activate Avalonia Parcel, the packaging tool for building, signing, and packaging Avalonia applications on Windows, macOS, and Linux.
sidebar_label: 配置
sidebar_position: 1
doc-type: tutorial
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

Avalonia Parcel is a packaging tool for Avalonia applications. It provides a graphical user interface (GUI) and a command-line interface (CLI). You can use Parcel to build, sign, and package applications for Windows, macOS, and Linux.

## 前置条件 {#prerequisites}

| 要求 | Version/Details |
|------------|-----------------|
| .NET Runtime | 6.0 或更高 |
| Windows | 10 或更高 |
| macOS | 13 或更高 |
| Linux | X11，且兼容 glibc 2.27 或 musl 1.22.2 的发行版 |

## Step 1: Install Avalonia Parcel

Avalonia Parcel is a [.NET tool](https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools). Use the .NET SDK to install and update it.

This guide shows how to install Parcel globally. You can install it locally, but a local installation works only in the project where you install it.

<Tabs>
<TabItem value="net10" label=".NET 10+" default>

```bash
dotnet tool install --global AvaloniaUI.Parcel
```

If you installed Parcel for .NET 8 or .NET 9, first run `dotnet tool uninstall --global AvaloniaUI.Parcel.Windows` or `parcel uninstall`.

Use the following command to update Parcel:

```bash
dotnet tool update --global AvaloniaUI.Parcel
```

</TabItem>
<TabItem value="net8" label=".NET 8/9">

If you use a .NET SDK version earlier than 10, install the package for your platform.

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

Use the command for your platform to update Parcel.

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
On macOS or Linux, the installer might not add the installation directory to the `PATH` environment variable. In this case, the shell reports a "command not found" error when you run `parcel`.

Add the tool directory to `PATH`. The default directory is usually `$HOME/.dotnet/tools`.

更多信息请见[排查 .NET 工具使用问题](https://learn.microsoft.com/en-us/dotnet/core/tools/troubleshoot-usage-issues#executable-file-not-found)。
:::

## Step 2: Run the tool

After installation, run Parcel from a terminal:

```bash
parcel
```

This command opens the Parcel GUI. In the GUI, you can open or create Parcel projects.

You can also run CLI commands on an existing Parcel project:

```bash
parcel pack ./SampleApp.parcel -r osx-x64 -p dmg -o ./artifacts
```

This command uses the Parcel project to bundle and sign the application. It then creates a DMG file.

:::note
CLI is not available in the free community license.
:::

## Step 3: Activate the tool

When Parcel opens, sign in with the Avalonia Portal account that has the tool license.

For the CLI, use the `--license-key` option. Alternatively, set the `AVALONIA_TOOLS_LICENSE_KEY` environment variable, or sign in through the Parcel GUI and reuse that session.

## Further Reading

- [Parcel command line reference](/tools/parcel/command-line-reference)
- [Parcel configuration reference](/tools/parcel/configuration-reference)
- [模型上下文协议（MCP）](/tools/parcel/mcp)
- [Windows packaging](/tools/parcel/packaging-for-windows)
- [macOS packaging](/tools/parcel/packaging-for-macos)
- [Linux packaging](/tools/parcel/packaging-for-linux)
