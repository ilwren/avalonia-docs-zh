---
id: webview-environment
title: WebView 运行环境
---

## 概述 {#overview}

WebView 环境选项让你在底层浏览器引擎初始化之前对它做定制。开发者工具、隐私浏览、用户数据目录以及其他必须在创建时设定的平台专有特性，都得靠它来配置。

`EnvironmentRequested` 事件在 WebView 适配器创建之前触发，让你有机会按应用需要修改这些设置。

## 基本用法 {#basic-usage}

```csharp
var webView = new WebView();
webView.EnvironmentRequested += (sender, args) =>
{
    // Enable developer tools for all platforms
    args.EnableDevTools = true;
    
    // Platform-specific configuration
    switch (args)
    {
        case WindowsWebView2EnvironmentRequestedEventArgs webView2Args:
            webView2Args.IsInPrivateModeEnabled = true;
            break;
        case AppleWKWebViewEnvironmentRequestedEventArgs appleArgs:
            appleArgs.NonPersistentDataStore = true;
            break;
        case GtkWebViewEnvironmentRequestedEventArgs gtkArgs:
            gtkArgs.EphemeralDataManager = true;
            break;
    }
};
```

## 基类属性 {#base-class-properties}

### WebViewEnvironmentRequestedEventArgs

**属性：**

- `EnableDevTools`（bool）：控制用户能否通过右键菜单或快捷键打开 DevTools。所有平台均可用。

## 平台专有选项 {#platform-specific-options}

### Windows WebView2

**Key Properties:**

- `ExplicitEnvironment`：使用已有的 ICoreWebView2Environment COM 句柄
- `ProfileName`：设置自定义的浏览器配置文件名称
- `BrowserExecutableFolder`：指定 Edge 浏览器可执行文件的位置
- `UserDataFolder`：指定用户数据的存放位置
- `AdditionalBrowserArguments`：传入自定义的 Chromium 命令行开关
- `Language`：设置浏览器界面语言（BCP 47 格式）
- `IsInPrivateModeEnabled`：启用隐私浏览模式

**Example:**

```csharp
webView.EnvironmentRequested += (sender, args) =>
{
    if (args is WindowsWebView2EnvironmentRequestedEventArgs webView2)
    {
        webView2.ProfileName = "AvaloniaUser";
        webView2.UserDataFolder = Path.Combine(AppContext.BaseDirectory, "webview");
    }
};
```

### macOS/iOS (WKWebView)

**Key Properties:**

- `NonPersistentDataStore`：只在内存中存放数据
- `DataStoreIdentifier`：为持久化数据设置唯一标识
- `ApplicationNameForUserAgent`：定制 user agent 中的应用名称
- `UpgradeKnownHostsToHTTPS`：自动把 HTTP 升级为 HTTPS
- `LimitsNavigationsToAppBoundDomains`：限制只能导航到应用自己的域名

**Example:**

```csharp
webView.EnvironmentRequested += (sender, args) =>
{
    if (args is AppleWKWebViewEnvironmentRequestedEventArgs wkWebView)
    {
        wkWebView.NonPersistentDataStore = true;
        wkWebView.ApplicationNameForUserAgent = "Avalonia WebView Sample";
    }
};
```

### Linux (WPE WebKit)

[WPE WebKit](https://wpewebkit.org) 采用离屏渲染，再合成进 Avalonia 的视觉树。只要装了它的库，`NativeWebView` 就优先用它，否则改用 [WebKitGTK](#linux-gtk-webkit)。这个事件只在走 WPE 时才会引发，因此没装 WPE 的机器上它永远不触发。所需软件包见 [Linux 前置条件](/docs/app-development/embedding-web-content#linux)；另请注意 Ubuntu 根本没有打包 WPE。

**Key Properties:**

- `DataDirectory`：用于存放持久化网站数据的目录。为 `null` 时使用 WPE 的默认数据目录。
- `CacheDirectory`：用于存放网站缓存的目录。为 `null` 时使用 WPE 的默认缓存目录。
- `RenderingMode`：选择 WPE 渲染后端（`WpeRenderingMode`）。默认的 `Auto` 目前映射到 `Shm`（软件渲染，不需要 GPU）。`Egl` 和 `DmaBuf` 为将来预留，选中会抛出 `NotImplementedException`。该选择是进程全局的，会影响所有 `NativeWebView` 实例。
- `PreferWebKitGtkInstead`：为 `true` 时，即便 WPE 可用也仍旧使用 WebKitGTK 适配器。这是给装有 WPE 的机器准备的「退出选项」；没装 WPE 的机器本来就会走 WebKitGTK，不需要设置它。

**Example:**

```csharp
webView.EnvironmentRequested += (sender, args) =>
{
    if (args is LinuxWpeWebViewEnvironmentRequestedEventArgs wpeArgs)
    {
        wpeArgs.DataDirectory = Path.Combine(AppContext.BaseDirectory, "wpe-data");
        wpeArgs.CacheDirectory = Path.Combine(AppContext.BaseDirectory, "wpe-cache");
    }
};
```

### Linux (GTK WebKit)

WebKitGTK 是 Linux 上的基准后端。`NativeWebDialog` 一律使用它；而 `NativeWebView` 只在未安装 [WPE WebKit](#linux-wpe-webkit) 时使用它。用它不需要任何配置。

**Key Properties:**

- `ApplicationNameForUserAgent`：定制 user agent 中的应用名称
- `ExperimentalOffscreen`：渲染到由 Avalonia 合成的离屏 GTK 窗口，而不是把原生 X11 子窗口重新挂到父窗口上。这样 web 视图就能和其他控件共处同一个 Avalonia 窗口而不互相遮挡。
- `ForceX11GdkBackend`：在 GTK 初始化期间把 `GDK_BACKEND` 改写为 `x11`，之后恢复原值。该选项默认开启，于是 [Wayland](/docs/platform-specific-guides/linux#wayland) 会话无需任何配置即可工作；设为 `false` 可放弃这项环境变量改写。
- `EphemeralDataManager`：不持久化数据存储
- `BaseDataDirectory`：设置网站数据的基准目录
- `BaseCacheDirectory`：设置缓存的基准目录
- `SharedProcessModel`：所有 WebView 实例共用一个进程
- `DisableCache`：彻底关闭缓存以优化内存占用

**Example:**

```csharp
webView.EnvironmentRequested += (sender, args) =>
{
    if (args is GtkWebViewEnvironmentRequestedEventArgs gtkArgs)
    {
        gtkArgs.EphemeralDataManager = true;
        gtkArgs.EnableDevTools = true;
    }
};
```

## 另请参阅 {#see-also}

- [NativeWebView](/controls/web/nativewebview)
- [NativeWebDialog](/controls/web/nativewebdialog)
- [WebAuthenticationBroker](/controls/web/webauthenticationbroker)
- [嵌入网页内容](/docs/app-development/embedding-web-content)
- [FAQ](/tools/faq#webview)
