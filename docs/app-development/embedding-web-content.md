---
id: embedding-web-content
title: 嵌入网页内容
description: 用 NativeWebView、NativeWebDialog 和 WebAuthenticationBroker 在 Avalonia 应用中嵌入网页内容。
doc-type: how-to
tags:
  - xpf
---

## 概述 {#overview}

Avalonia WebView 组件为你的应用带来原生的网页浏览能力。与那些需要打包 Chromium 的内嵌式 WebView 方案不同，它直接借助平台自带的网页渲染能力，因而应用体积更小、性能更好。

WebView 组件包含三个主要 API：

- [`NativeWebView`](/controls/web/nativewebview) —— 直接在应用界面中嵌入网页内容的控件
- [`NativeWebDialog`](/controls/web/nativewebdialog) —— 承载网页内容的独立对话框窗口
- [`WebAuthenticationBroker`](/controls/web/webauthenticationbroker) —— 处理 OAuth 等基于网页的认证流程的工具类

Avalonia 和 [Avalonia XPF](/xpf) 都能使用 WebView 组件。XPF 下的安装与用法请看下面的 [XPF 一节](#xpf)。

## 安装 {#installation}

把 WebView 包添加到你的项目：

```bash
dotnet add package Avalonia.Controls.WebView
```

## 基本用法 {#basic-usage}

### NativeWebView

:::note
在 Linux 上，`NativeWebView` 使用 [WPE WebKit](https://wpewebkit.org) 并以离屏方式渲染，请确保已安装 WPE 运行时库——参见 [Linux 环境要求](#linux)。若目标系统上没有 WPE，请改用 [`NativeWebDialog`](/controls/web/nativewebdialog)。
:::

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <NativeWebView Source="https://avaloniaui.net/"
                   NavigationCompleted="WebView_NavigationCompleted" />
</Window>
```

```csharp
private void WebView_NavigationCompleted(object? sender, WebViewNavigationCompletedEventArgs args)
{
    if (args.IsSuccess)
    {
        // Navigation completed successfully
    }
}
```

#### 双向执行 JavaScript {#bidirectional-javascript-execution}

有时你需要从 web view 控件中执行任意 JavaScript 代码。
`NativeWebView` 为此提供了 [`InvokeScript` 异步方法](/controls/web/nativewebview#invokescript)：

```csharp
webView.InvokeScript("console.log('Hello World')");
```

若需要从 JavaScript（网页）接收数据并在 C# 一侧处理，可以用 `NativeWebView.WebMessageReceived` 事件配合 `invokeCSharpAction` 这个 JS 辅助方法。

完整的双向通信示例：
```csharp
private async void NativeWebView_OnNavigationCompleted(object? sender, WebViewNavigationCompletedEventArgs e)
{
    await ((NativeWebView)sender!).InvokeScript(""" invokeCSharpAction("{'key': 10}") """);
}

private void NativeWebView_OnWebMessageReceived(object? sender, WebMessageReceivedEventArgs e)
{
    var message = e.Body;
    // message == "{'key': 10}"
}
```

![在 Avalonia 窗口中用 NativeWebView 控件显示网页内容](/img/webview.png)

### NativeWebDialog

```csharp
var dialog = new NativeWebDialog
{
    Title = "Avalonia Docs",
    CanUserResize = true,
    Source = new Uri("https://docs.avaloniaui.net/")
};

dialog.NavigationCompleted += (s, e) =>
{
    if (e.IsSuccess)
    {
        // Navigation completed successfully
    }
};

dialog.Show();
```

### WebAuthenticationBroker

```csharp
var authOptions = new WebAuthenticatorOptions(
    RequestUri: new Uri("https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&scope=openid"),
    RedirectUri: new Uri("http://localhost")
);

var result = await WebAuthenticationBroker.AuthenticateAsync(mainWindow, authOptions);

if (result.CallbackUri != null)
{
    // Process authentication result
    var code = HttpUtility.ParseQueryString(result.CallbackUri.Query)["code"];
}
```

把 `YOUR_CLIENT_ID` 换成你自己应用的客户端 ID。

## 平台前置条件 {#platform-prerequisites}

WebView 组件依赖用户机器上必须具备的原生网页渲染实现。

#### 小结 {#summary}

| 组件 | Windows | macOS | Linux | iOS | Android | 浏览器 |
|-----------|---------|-------|-------|-----|---------|---------|
| NativeWebView | ✓ | ✓ | ✓* | ✓ | ✓ | ✗ |
| NativeWebDialog | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| WebAuthenticationBroker | ✓** | ✓ | ✓** | ✓ | ✓*** | ✓**** |

\* 在 Linux 上，`NativeWebView` 在装有 WPE WebKit 时使用它，否则使用 WebKitGTK。两种后端各自需要哪些软件包，请参阅 [Linux](#linux)。
\** 采用 NativeWebDialog 实现
\*** Android 支持尚属实验性质
\**** 需要为重定向页面配置 CORS。在浏览器中运行该库还需要 .NET 10。

#### Windows

使用 Microsoft Edge WebView2，它：

- 在 Windows 11 上已预装
- 在 Windows 10 上可能需要另行安装

面向 Windows 10 用户，你可以把 WebView2 运行时一并打进安装程序：

- [WebView2 Runtime Download](https://developer.microsoft.com/en-us/microsoft-edge/webview2?form=MA13LH#download)
- [Distribution Guide](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution?tabs=dotnetcsharp)

#### macOS/iOS

使用 `WKWebView`，所有现代 macOS/iOS 设备上均已预装。

- 无需额外配置
- WebAuthenticationBroker 需要 macOS 10.15+ 或 iOS 12.0+

#### Linux

Linux 上有两种后端，系统会自动选择：

- **WebKitGTK** 是保底方案。`NativeWebDialog` 始终使用它；只要没装 WPE，`NativeWebView` 也会用它。无需任何配置。
- **[WPE WebKit](https://wpewebkit.org)** 是可选项，只要相关库存在，`NativeWebView` 就会优先采用。它以离屏（SHM）方式渲染，且不强依赖 GTK，因此无需原生窗口嵌入就能融入 Avalonia 的视觉树，在 X11 和 Wayland 会话下都能工作。

##### WebKitGTK

安装 GTK 3、WebKitGTK 4.1 和 libsoup 3。

Debian/Ubuntu:

```bash
sudo apt install libgtk-3-0 libwebkit2gtk-4.1-0 libsoup-3.0-0
```

Fedora：

```bash
sudo dnf install gtk3 webkit2gtk4.1 libsoup3
```

Arch：

```bash
sudo pacman -S gtk3 webkit2gtk-4.1 libsoup3
```

:::note
较老的发行版上 `libwebkit2gtk-4.0` 和 `libsoup-2.4` 同样可用，但推荐 `4.1` 和 `soup-3`。基于 GTK 4 构建的 WebKitGTK 6.0 不受支持。
:::

##### WPE WebKit（可选） {#wpe-webkit-optional}

Debian 13（trixie）及更新版本：

```bash
sudo apt install libwpewebkit-2.0-1
```

Fedora：

```bash
sudo dnf install dnf-plugins-core
sudo dnf copr enable philn/wpewebkit
sudo dnf install wpewebkit
```

Arch：

```bash
sudo pacman -S wpewebkit
```

:::note
Ubuntu 没有打包 WPE WebKit。它在 Ubuntu 22.10 中被移除（[LP #1981592](https://bugs.launchpad.net/ubuntu/+source/wpewebkit/+bug/1981592)）后再未回归，所以那里装不了 `libwpewebkit-2.0-1`。这不用管：`NativeWebView` 会自行回退到 WebKitGTK。
:::

##### X11 与 Wayland {#x11-and-wayland}

WPE 既不需要 X11 也不需要 GTK。WebKitGTK 则需要 x11 GDK 后端，在 Wayland 会话下可通过 XWayland 提供。

##### 查看当前装了什么 {#checking-what-is-installed}

`WebViewAdapterInfo.GetAdapterInfo` 会报告某个后端的库是否被找到，便于区分「库缺失」与「后端已加载但没在渲染」这两种情况：

```csharp
var gtk = WebViewAdapterInfo.GetAdapterInfo(WebViewAdapterType.WebKitGtk);
var wpe = WebViewAdapterInfo.GetAdapterInfo(WebViewAdapterType.WpeWebKit);

Console.WriteLine($"WebKitGTK: {gtk.IsInstalled} {gtk.Version} {gtk.UnavailableReason}");
Console.WriteLine($"WPE WebKit: {wpe.IsInstalled} {wpe.Version} {wpe.UnavailableReason}");
```

#### Android

需要 Android API 21 或更高版本。

## 与原生浏览器互操作 {#native-browser-interop}

Avalonia WebView 组件借助各平台原生的 web view，提供跨平台的网页内容渲染能力。
不过有时你需要访问一些平台专属 API，而 Avalonia WebView 的抽象层并未暴露它们。

本文介绍如何获取原生句柄，以及如何在各个受支持的平台上与底层浏览器实现互操作。

### 获取句柄 {#getting-handle}

要访问原生浏览器的功能，首先得从 WebView 控件拿到平台专属的句柄。

#### 对 WebView 控件 {#for-webview-controls}

在 WebView 实例上调用 `TryGetPlatformHandle()` 方法：

```csharp
if (myWebView.TryGetPlatformHandle() is IWindowsWebView2PlatformHandle handle)
{
    // Cast to platform-specific interface and use
}
```

#### 对 WebView 对话框 {#for-webview-dialogs}

在 WebView 对话框实例上调用 `TryGetWebViewPlatformHandle()` 方法：

```csharp
if (myWebViewDialog.TryGetWebViewPlatformHandle() is IWindowsWebView2PlatformHandle handle)
{
    // Cast to platform-specific interface and use
}
```

### Interop

#### Windows

Avalonia 在 Windows 上的 WebView 支持两种适配器：

- **WebView2**：基于 Chromium 的现代 Edge（推荐）
- **WebView1**：旧版 Edge（用于没有 WebView2 的老 Windows 10 环境的回退方案）

两种适配器都通过经典 COM 互操作工作。
*IDL* 定义文件可以在 `Microsoft.Web.WebView2` NuGet 包（WebView2）、Windows SDK（WebView1）或网上找到。

**推荐做法**：使用新的 [`[GeneratedComInterface]`](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/comwrappers-source-generation) 特性，获得快速且对裁剪/AOT 友好的 COM 互操作。

**Alternative Solutions**:

- [CsWin32 生成器](https://github.com/microsoft/CsWin32)
- [Legacy `[ComImport]`](https://learn.microsoft.com/en-us/dotnet/standard/native-interop/cominterop)

```csharp
public interface IWindowsWebView2PlatformHandle : IPlatformHandle
{
    /// Returns COM handle to the ICoreWebView2 [76ECEACB-0462-4D94-AC83-423A6793775E] COM interface
    IntPtr CoreWebView2 { get; }
    /// Returns COM handle to the ICoreWebView2 [4D00C0D1-9434-4EB6-8078-8697A560334F] COM interface
    IntPtr CoreWebView2Controller { get; }
}
```

```csharp
public interface IWindowsWebView1PlatformHandle : IPlatformHandle
{
    /// Returns COM handle to the IWebViewControl [3F921316-BC70-4BDA-9136-C94370899FAB] COM interface.
    IntPtr WebViewControl { get; }
}
```

#### MacOS/iOS

**推荐做法**：使用官方 .NET Xamarin.Native 的 macOS/iOS 绑定，获得强类型包装。通常写成 [NSObject.GetNSObject\<WKWebView\>(IntPtr, false)](https://learn.microsoft.com/en-us/dotnet/api/objcruntime.runtime.getnsobject?view=xamarin-ios-sdk-12#objcruntime-runtime-getnsobject-1(system-intptr-system-boolean))。

```csharp
var wkWebView = NSObject.GetNSObject<WKWebView>(handle.WKWebView, false);
```

**备选方案**：用 `objc_msgSend` P/Invoke 直接调用原生 API（控制力更强，但更难维护）。

```csharp
public interface IAppleWKWebViewPlatformHandle : IPlatformHandle
{
    IntPtr WKWebView { get; }
    IntPtr GetWKWebViewRetained();
}
```

#### Linux (WPE WebKit)

当 [`NativeWebView`](/controls/web/nativewebview) 跑在 WPE 后端上时，平台句柄会同时暴露 `WebKitWebView` GObject 和底层的 `wpe_view_backend` 结构体，可据此直接 P/Invoke 调用 [WPEWebKit API](https://github.com/WebPlatformForEmbedded/WPEWebKit)。

```csharp
public interface ILinuxWpePlatformHandle : IPlatformHandle
{
    /// Pointer to the WebKitWebView GObject instance.
    IntPtr WebKitWebView { get; }

    /// Pointer to the wpe_view_backend native struct.
    IntPtr WpeViewBackend { get; }
}
```

#### Linux (WebKitGTK)

[`NativeWebDialog`](/controls/web/nativewebdialog) 始终暴露 WebKitGTK 句柄；[`NativeWebView`](/controls/web/nativewebview) 只要运行在 WebKitGTK 后端上也会暴露。拿到的 `WebKitWebView` IntPtr 可直接用于 [WebKitGTK 官方参考](https://webkitgtk.org/reference/webkit2gtk/stable/index.html)中的 WebKit P/Invoke 调用。

```csharp
public interface IGtkWebViewPlatformHandle : IPlatformHandle
{
    IntPtr WebKitWebView { get; }
}
```

#### Android

使用官方 .NET Xamarin.Android 绑定，可以最省事地拿到托管包装。

用法详情请参阅 [Android.Webkit.WebView 文档](https://learn.microsoft.com/en-us/dotnet/api/android.webkit.webview.-ctor?view=net-android-35.0#android-webkit-webview-ctor(system-intptr-android-runtime-jnihandleownership))。

```csharp
public interface IAndroidWebViewPlatformHandle : IPlatformHandle
{
    IntPtr WebKitWebView { get; }
}
```

## XPF

[Avalonia XPF](/xpf) 应用同样可以使用 WebView 组件。上文介绍的所有 WebView 功能、API 和平台前置条件对 XPF 都适用，差异见下。

### 安装 {#installation-1}

首先，请按[说明](/xpf/version-info/versioning)装好 XPF 的 NuGet 源。

配好 NuGet 源之后，安装 `Avalonia.Xpf.Controls.WebView` 包：

```xml
<PackageReference Include="Avalonia.Xpf.Controls.WebView" Version="11.3.9" />
```

:::note
若有更新版本，请用最新版。可以在 IDE 的 NuGet 包窗口里查看。

在 Windows 上，若 WebView2 不可用，则会内嵌旧版 Internet Explorer。这在需要兼容老旧 Windows 版本时很有用。
:::

### 用法 {#usage}

在 XAML 文件中添加 XPF 命名空间，然后使用 `NativeWebView`：

```xml
<wpf:NativeWebView xmlns:wpf="clr-namespace:Avalonia.Xpf.Controls;assembly=Avalonia.Xpf.Controls.WebView"
                   Source="https://avaloniaui.net/" />
```

`Source` 属性支持绑定。其余所有 API（`NativeWebDialog`、`WebAuthenticationBroker`、JavaScript 互操作）的用法与上文各节完全一致。

为了让代码迁移更顺畅，你也可以在 Windows 上不用 XPF、直接在原生 WPF 中使用 `NativeWebView` 控件。这种情况下所有 API 成员和底层浏览器都是一样的，用同一个包即可。

## 另请参阅 {#see-also}

- [NativeWebView](/controls/web/nativewebview)
- [NativeWebDialog](/controls/web/nativewebdialog)
- [WebAuthenticationBroker](/controls/web/webauthenticationbroker)
- [WebView 环境选项](/controls/web/webview-environment)
- [FAQ](/tools/faq#webview)
