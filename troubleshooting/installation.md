---
id: installation
title: 安装问题排查
description: 安装 .NET SDK、Avalonia 模板和配置 NuGet 包源时常见问题的解决办法。
doc-type: troubleshooting
---

本页汇总了安装 .NET SDK 或 Avalonia 项目模板时最常撞上的问题，并给出分步解决办法。

## 无法识别 .NET 程序 {#net-is-not-a-recognized-program}

若终端提示无法识别 `dotnet`，说明 .NET SDK 要么没装，要么不在系统 `PATH` 里。

### 第 1 步：确认 SDK 是否已安装 {#step-1-check-whether-the-sdk-is-installed}

运行下面的命令：

```bash
dotnet --list-sdks
```

若 .NET SDK 安装无误，会输出类似这样的内容：

```text
8.0.202 [C:\Program Files\dotnet\sdk]
```

若看到的是报错，请到 [.NET 官网](https://dotnet.microsoft.com/en-us/download/dotnet)下载并安装 .NET SDK。

### 第 2 步：重启终端 {#step-2-restart-your-terminal}

装好 SDK 后，关掉终端再打开（或开一个新的 shell 会话）。安装程序会更新系统 `PATH`，但已经开着的终端会话不会自动跟上这一变化。

### 第 3 步：核对 PATH（若问题依旧） {#step-3-verify-the-path-if-the-issue-persists}

若重启终端后仍识别不了 `dotnet`，请确认 SDK 的安装目录确实在你的 `PATH` 环境变量里。

常见的安装位置：

| OS      | 默认路径                          |
|---------|---------------------------------------|
| Windows | `C:\Program Files\dotnet`             |
| macOS   | `/usr/local/share/dotnet`             |
| Linux   | `/usr/share/dotnet` or `$HOME/.dotnet`|

在 **Windows** 上，打开**系统属性 > 环境变量**，确认上述路径出现在 `Path` 变量中。在 **macOS** 和 **Linux** 上，检查你的 shell 配置文件（比如 `~/.bashrc`、`~/.zshrc` 或 `~/.bash_profile`）里是否有导出 dotnet 目录的那一行。

:::tip
在 macOS 上，若你是用官方安装程序装的 .NET，命令却仍然找不到，可以试试运行：

```bash
export PATH="$PATH:/usr/local/share/dotnet"
```

把这一行加进 shell 配置文件，便可一劳永逸。
:::

### 第 4 步：检查是否装了多份 SDK {#step-4-check-for-multiple-sdk-installations}

若你装了多个 .NET SDK 版本，或用了多种安装方式（比如 macOS 上既用 Homebrew 又用官方安装程序），它们可能彼此冲突。运行：

```bash
which dotnet
```

确认返回的路径指向你心里那份安装。若不是，请调整 `PATH`，让正确的那份排在前面。

## 找不到 `Avalonia.Templates` 包 {#avaloniatemplates-package-cannot-be-found}

若 `dotnet new install Avalonia.Templates` 报 “not found” 失败，多半是你的 NuGet 包源配置里少了公共的 NuGet 源。

### 第 1 步：列出你的 NuGet 源 {#step-1-list-your-nuget-sources}

执行以下命令：

```bash
dotnet nuget list source
```

确认输出中包含下面这一项：

```text
nuget.org [Enabled]
https://api.nuget.org/v3/index.json
```

### 第 2 步：若缺失就把 NuGet 源加上 {#step-2-add-the-nuget-source-if-it-is-missing}

若列表里没有 `nuget.org`，把它加进去：

```bash
dotnet nuget add source https://api.nuget.org/v3/index.json -n nuget.org
```

然后重试安装模板：

```bash
dotnet new install Avalonia.Templates
```

### 第 3 步：重新启用被禁用的源 {#step-3-re-enable-a-disabled-source}

若 `nuget.org` 在列表里却显示为 `[Disabled]`，把它启用：

```bash
dotnet nuget enable source nuget.org
```

### 第 4 步：检查网络和防火墙设置 {#step-4-check-network-and-firewall-settings}

若源既在列表里又已启用，安装却仍然失败，请逐项排查：

- **企业代理或 VPN**：你的网络可能封了 `api.nuget.org`。请联系网络管理员，或换一个网络试试。
- **防火墙规则**：确认到 `api.nuget.org` 的出站 HTTPS 流量（443 端口）是放行的。
- **DNS 解析**：运行 `ping api.nuget.org` 确认该域名能正常解析。

### 第 5 步：清理 NuGet 缓存 {#step-5-clear-the-nuget-cache}

缓存数据损坏或过期偶尔也会让安装失败。清一下缓存再试：

```bash
dotnet nuget locals all --clear
dotnet new install Avalonia.Templates
```

## 模板装成功了，却看不到模板 {#template-install-succeeds-but-templates-do-not-appear}

若 `dotnet new install Avalonia.Templates` 报告成功，`dotnet new list` 却列不出任何 Avalonia 模板，多半是模板引擎的缓存出了岔子。

试试重新安装：

```bash
dotnet new uninstall Avalonia.Templates
dotnet new install Avalonia.Templates
```

若你用的是带 Avalonia 扩展的 Visual Studio，请注意该扩展自带一份模板。`dotnet new install` 这一步只有命令行或非 Visual Studio 的 IDE 工作流才需要。

## 安装过程中的权限错误 {#permission-errors-during-installation}

在 macOS 和 Linux 上，安装模板或 .NET SDK 时可能遇到权限错误。

- 不要用 `sudo` 搭配 `dotnet new install`。.NET 模板引擎把模板存在你的用户配置目录下，并不需要提权。
- 若你之前用 `sudo` 装过，模板缓存的属主可能成了 root。用下面的命令把属主改回来：

```bash
sudo chown -R $(whoami) ~/.templateengine
```

## 另请参阅 {#see-also}

- [Install Avalonia](/docs/get-started/install-avalonia)
- [配置你的 IDE](/docs/get-started/set-up-your-ide)
- [应用性能问题](/troubleshooting/app-performance-issues)
