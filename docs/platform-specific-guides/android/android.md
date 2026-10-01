---
id: android
title: 用 Avalonia 开发 Android 应用
description: 搭建 Android 开发环境以构建 Avalonia 应用，包括安装 SDK 和工作负载。
doc-type: how-to
---

## 搭建开发环境 {#setting-up-your-developer-environment}

按下面几步用命令行安装所需的工具：

-  先确认你装的 .NET SDK 版本可用。Avalonia 支持的最低版本是 6.0.2.00。

:::info
你可以查看[可用的 .NET SDK 版本](https://dotnet.microsoft.com/en-us/download/dotnet)。
:::

-  你也许得先卸掉旧版的 _Android 工作负载_。执行以下命令即可：

```bash
dotnet workload uninstall android
```

-  安装 _Android 工作负载_。执行以下命令：

```bash
dotnet workload install android
```

:::info
上述命令可能需要加 _sudo_ 运行。
:::

:::caution[Linux 用户：请使用微软官方的 .NET SDK]
`dotnet workload` 命令需要微软官方的 .NET SDK。Linux 发行版仓库里的 .NET 包（比如 Arch Linux 的 AUR、Ubuntu 的 `dotnet-sdk` apt 包或 Fedora 的 `dotnet` dnf 包）可能不带工作负载支持。若 `dotnet workload install android` 报错 `NETSDK1139`，请从[微软 .NET 下载页](https://dotnet.microsoft.com/download)安装 SDK，或使用[安装脚本](https://learn.microsoft.com/dotnet/core/tools/dotnet-install-script)：

```bash
curl -sSL https://dot.net/v1/dotnet-install.sh | bash /dev/stdin --channel 10.0
```
:::

### 安装 Android SDK {#install-the-android-sdk}

安装 Android SDK 的办法有好几种，挑一个与你开发环境相符的即可。

如果你用 Visual Studio，请参阅 [Android SDK 安装指南](https://docs.microsoft.com/en-us/xamarin/android/get-started/installation/android-sdk)。

如果你用 JetBrains Rider，请参阅 [Rider 文档](https://www.jetbrains.com/help/rider/Introduction.html)。

另一种办法是安装 [Android 命令行工具](https://developer.android.com/studio#command-tools)。

这套工具自带一个命令行版的 SDK 管理器，可用来安装 SDK。装好 Android SDK 后，请把 sdk 的路径加入 PATH 环境变量——在 Linux 上可以直接在 bash 里设置，或写进 profile 的 .bashrc 文件。

```bash
export ANDROID_HOME=/path/to/sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

你也可以在构建、运行或部署 dotnet Android 项目时，于 `dotnet` 命令中设置 `AndroidSdkDirectory` 变量，直接指明 Android SDK 的位置：

```bash
dotnet build ... /p:AndroidSdkDirectory=/path/to/sdk
```

请用你平台上的包管理器装好 JDK 11 或更高版本。若你已按上文用 Visual Studio 或 JetBrains Rider 配置过，这一步就已经做好了。

还有一个正在开发中的工具叫 _MAUI Check_，能自动替你装齐所有必需的 SDK 和工具：

```bash
dotnet tool install -g Redth.Net.Maui.Check
maui-check
```

完成上述 _Android_ 开发环境配置后，你就能构建 _Android_ 应用，并在本机的模拟器中运行它们了。

## 另请参阅 {#see-also}

- [在 Android 上部署](/docs/deployment/android)（模拟器、真机与发布）
- [在 Linux 的 Visual Studio Code 中配置 Android 调试](/tools/visual-studio-code/configure-vscode-debug-linux)
