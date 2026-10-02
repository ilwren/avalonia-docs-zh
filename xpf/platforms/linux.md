---
id: linux
title: Linux
---

## 支持的发行版 {#supported-distributions}

下列 Linux 发行版经过了全面测试，属于受支持之列：

* **Debian**：9 及以上版本
* **Ubuntu**：16.04 及以上版本
* **Fedora**：30 及以上版本

### 其他发行版 {#other-distributions}

除上面列出的之外，Avalonia XPF 在许多其他 Linux 发行版上同样跑得起来。若你用的发行版不在官方支持之列：

* Avalonia 支持团队可以帮你确认与所选发行版的兼容性
* 发行版专属的问题会按具体情况逐一处理
* 可能需要额外的配置或测试

:::note
若你打算部署到列表之外的发行版，请在开发早期就联系支持团队。
:::


## Installing .NET

许多发行版的软件仓库里都带有 .NET，但那些版本**不能用**——它们没有附带必需的 `Microsoft.NET.Sdk.WindowsDesktop` SDK。你必须从微软的软件源安装 .NET。

### Ubuntu

```bash
# Register the Microsoft package repository
wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

# Install the .NET SDK
sudo apt update
sudo apt install dotnet-sdk-8.0
```

### Debian

```bash
wget https://packages.microsoft.com/config/debian/$(cat /etc/debian_version | cut -d. -f1)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

sudo apt update
sudo apt install dotnet-sdk-8.0
```

### Fedora

```bash
sudo dnf install dotnet-sdk-8.0
```

Fedora 的默认仓库中就收录了微软的 .NET 软件包，它们与 XPF 兼容。

### 其他发行版 {#other-distributions-1}

其他发行版请把 [Microsoft 软件源](https://packages.microsoft.com/)加进包管理器，再从那里安装 .NET SDK。

### 修复装坏了的 .NET {#fixing-a-broken-net-installation}

若你此前是从发行版自带仓库（而非微软）装的 .NET，务必先彻底卸载干净，再从微软的源安装。两边的包混在一起会引发冲突，还会缺少 SDK 组件。

```bash
# 1. Remove the distribution's .NET packages
sudo apt remove 'dotnet*' 'aspnet*' 'netstandard*'   # Debian/Ubuntu
# or
sudo dnf remove 'dotnet*' 'aspnet*' 'netstandard*'   # Fedora

# 2. Remove any .NET install directories
sudo rm -rf /usr/share/dotnet
sudo rm -rf /usr/lib/dotnet

# 3. Remove the distribution's .NET package source to prevent it from being reinstalled
# On Ubuntu, check for and remove:
sudo rm /etc/apt/sources.list.d/*dotnet* 2>/dev/null
sudo rm /etc/apt/preferences.d/*dotnet* 2>/dev/null

# 4. Install .NET from the Microsoft feed (see instructions above)
```

:::danger
混装（一部分包来自发行版、一部分来自微软）会带来极难定位的构建失败。若 `dotnet --list-sdks` 的输出中看不到 `Microsoft.NET.Sdk.WindowsDesktop`，就说明你的安装不对劲。
:::

## 其他依赖 {#other-dependencies}

运行 XPF 需要下列原生库：`libICE`、`libSM`、`fontconfig` 和 `libgdiplus`。

### Debian / Ubuntu

```bash
sudo apt install libice6 libsm6 libfontconfig1 libgdiplus
```

### Fedora

```bash
sudo dnf install libICE libSM fontconfig libgdiplus
```

### RHEL / CentOS / Rocky Linux / AlmaLinux

```bash
sudo dnf install libICE libSM fontconfig
```

RHEL 的默认仓库里没有 `libgdiplus`，请从 EPEL 安装：

```bash
sudo dnf install epel-release
sudo dnf install libgdiplus
```

### 其他发行版 {#other-distributions-2}

请用你所在发行版的包管理器安装对应的软件包。各发行版的库名可能不同（比如 Debian 上的 `libice6` 对应 Fedora/RHEL 上的 `libICE`）。

## 为 Linux 发布 {#publishing-for-linux}

发布 XPF 应用请一律走命令行，不要用 Visual Studio。用 Visual Studio 发布可能产出不完整的输出，缺掉 `libSkiaSharp.so` 这类原生库。

```bash
dotnet publish -r linux-x64 -c Release
```

自包含部署：

```bash
dotnet publish -r linux-x64 -c Release --self-contained
```

:::caution
通过 Visual Studio 发布可能漏掉关键的原生依赖。若你遇到针对 `libSkiaSharp` 的 `DllNotFoundException` 或类似错误，请改用 CLI 发布。
:::

### ReadyToRun 下的原生库解析 {#native-library-resolution-with-readytorun}

启用 `PublishReadyToRun` 时，.NET 运行时解析原生库的方式可能有所不同。若应用在运行时找不到 `.so` 文件：

- 确认原生库与可执行文件在同一目录下
- 若原生库被挪了地方，请设置 `LD_LIBRARY_PATH` 把该目录包含进来
- 考虑改用自包含发布，它会把所有依赖放在一处

## 在 Linux 上调试 {#debugging-on-linux}

### 从 Windows（Visual Studio）调试 {#from-windows-visual-studio}

若要在 Windows 的 Visual Studio 中调试跑在 Linux 上的 XPF 应用：

1. 在命令行为 linux-x64 构建：
   ```bash
   dotnet publish -r linux-x64 -c Debug
   ```
2. 把输出复制到你的 Linux 机器或 WSL2 实例上
3. 在 Linux 上运行该应用
4. 在 Visual Studio 中选**调试 > 附加到进程**，连接类型选 WSL2 或 SSH，然后附加到正在运行的进程

### 从 VS Code 调试 {#from-vs-code}

用 VS Code 配合 C# DevKit 扩展，配一个 `launch.json` 以便通过 SSH 或 WSL2 远程调试。

### 从 JetBrains Rider 调试 {#from-jetbrains-rider}

Rider 原生支持通过 SSH 远程调试，并可借助 Gateway 功能支持 WSL2。

:::tip
搭配 XPF SDK 时，`net8.0-windows` 目标框架在非 Windows 平台上同样管用。为 Linux 构建时不必改动目标框架。
:::

## 托盘图标 {#tray-icons}

XPF 通过 StatusNotifierItem/AppIndicator 协议在 Linux 上支持系统托盘图标。

**GNOME** 默认不带托盘图标支持，请安装 [AppIndicator GNOME 扩展](https://extensions.gnome.org/extension/615/appindicator-support/)来启用。

**KDE Plasma** 原生支持托盘图标，无需额外配置。

## 老发行版上的文件对话框 {#file-dialogs-on-older-distributions}

在较老的 Linux 发行版上（比如 RHEL 8），GNOME 版本可能太旧，支持不了基于 DBus 的文件对话框协议，这会导致 `OpenFolderDialog.InitialDirectory` 等属性被忽略。

变通办法是在[自定义初始化](/xpf/configuration/customizing-initialization)中关掉 DBus 文件选取器：

```csharp
AppBuilder.Configure<AvaloniaUI.Xpf.Helpers.DefaultXpfAvaloniaApplication>()
    .UsePlatformDetect()
    .With(new X11PlatformOptions { UseDBusFilePicker = false })
    .WithAvaloniaXpf()
    .SetupWithLifetime(new ClassicDesktopStyleApplicationLifetime
    {
        ShutdownMode = ShutdownMode.OnExplicitShutdown
    });
```

这样会退回到 GTK 文件对话框，它在老系统上也支持 `InitialDirectory`。

## Win32 API shim 与原生 API 冲突 {#win32-api-shim-conflicts-with-native-apis}

若你的应用既调用了 Linux 原生 API（比如通过 `DllImport` 调 X11 函数），又启用了 Win32 API shim，shim 层可能把那些原生调用拦下来，从而引发 `EntryPointNotFoundException`。

解决办法是把调用 Linux 原生 API 的代码挪到一个单独的程序集里，并把它从 Win32 shim 中排除：

```csharp
AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable(asm =>
{
    // Skip the assembly containing native Linux API calls
    if (asm.GetName().Name == "MyLinuxNativeInterop")
        return true; // true = skip this assembly
    return false;
});
```

或者用 `WinApiShimSetup.AddLibrary` 只为特定程序集启用 shim，而不是用 `AutoEnable` 一刀切。

## 从 `systemd` 启动 {#launching-from-systemd}

在 X11 上以 systemd 服务的方式启动 XPF 应用时，可能出现竞态：应用抢在窗口管理器完全就绪之前就起来了，于是 `WindowStyle="None"` 被忽略，标题栏又冒了出来。

在 systemd 服务文件中加一段启动延迟：

```ini
[Service]
ExecStartPre=/bin/sleep 5
ExecStart=/path/to/your/application
```

## Linux 上的 WebView {#webview-on-linux}

在 Linux 上，XPF 通过 `NativeWebDialog`（来自 `Avalonia.Xpf.Controls.WebView` NuGet 包）提供网页内容嵌入。可内嵌的 `NativeWebView` 控件在 Linux 上不受支持。

`NativeWebDialog` 需要 webkit2gtk 4.1 版：

### Debian / Ubuntu

```bash
sudo apt install libwebkit2gtk-4.1-dev
```

### Fedora

```bash
sudo dnf install webkit2gtk4.1-devel
```

### RHEL / CentOS

```bash
sudo dnf install webkit2gtk4.1-devel
```

若你所用的 RHEL 版本里没有 `webkit2gtk4.1-devel`，不妨看看 EPEL 或更新的 AppStream 模块里有没有。

:::note
必须是 webkit2gtk 4.1 版。更老的版本（4.0）支持不了 `NativeWebDialog` 所需的全部功能。
:::

各种浏览器嵌入方案的对比请见[嵌入网页内容](/xpf/interop/web-content)。

## 显示服务器方面的考量 {#display-server-considerations}

### X11

X11 是多数 Linux 发行版的默认显示服务器。XPF 在 X11 上表现良好，不过有几点要留心：

- **窗口管理器的时序**：若在桌面会话很早的阶段启动 XPF 应用（比如从 systemd 服务启动），窗口管理器可能尚未完全就绪，导致 `WindowStyle="None"` 被忽略。变通办法请见[从 systemd 启动](#launching-from-systemd)。
- **窗口消息**：Win32 窗口消息（比如 `WM_ACTIVATEAPP`）由 shim 层模拟，但只覆盖所支持的第三方控件所需的那些，并非全部消息都会生成。若你的应用靠特定窗口消息做跨窗口通信，不妨改用 .NET 的 IPC 机制。
- **多显示器的怪癖**：窗口定位和 DPI 行为会因窗口管理器而异，请尽早在你的目标窗口管理器上实测。

### Wayland

Wayland 是较新的显示协议，近期版本的 Fedora 和 Ubuntu 默认都用它。XPF 通过 XWayland（X11 兼容层）支持 Wayland。

- **键盘隔离**：只有获得焦点的窗口才能收到键盘输入，没有办法把键盘输入定向到未获焦点的窗口。若你的应用需要在多个窗口之间隔离键盘输入（比如带多个输入设备的自助终端），那这是 Wayland 协议本身的限制。
- **窗口定位**：Wayland 不允许应用设定窗口的绝对位置，`Window.Left` 和 `Window.Top` 可能被合成器忽略。

## 已知限制 {#known-limitations}

- **UI 测试自动化**：Avalonia 目前在 Linux 上还不支持 AT-SPI2 无障碍协议。依赖无障碍 API 的自动化 UI 测试工具（比如 pywinauto 或 Appium）能做的事相当有限。
- **透明窗口的点击穿透**：与 macOS 上一样，XPF 在 Linux 上也不支持点穿窗口的透明区域。落在透明区域的鼠标点击会被该窗口捕获，不会传到下面的窗口。若要做叠加层，请把内容放进同一个窗口，而不是把若干透明窗口摞在一起。
- **Wayland 的键盘隔离**：在 Wayland 合成器上，只有获得焦点的窗口才能收到键盘输入，没有办法把键盘输入定向到未获焦点的窗口。
- **远程桌面下的透明度**：某些远程桌面工具（比如 MobaXterm）不支持 alpha 通道透明，透明窗口因此可能显示成白色背景。这是远程桌面工具的局限，与 XPF 无关。可以用原生 Linux 应用（比如开了透明的 Konsole）测一测，以确认透明度表现。
- **NativeControlHost**：`NativeControlHost`（用于嵌入 Linux 原生控件）在 Linux 上支持有限。若确需嵌入原生内容，不妨改用 Avalonia 的合成 API。
