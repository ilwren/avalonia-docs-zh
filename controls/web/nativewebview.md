---
id: nativewebview
title: NativeWebView
---

## 概述 {#overview}

`NativeWebView` 是一个控件，为 Avalonia 和 WPF 应用提供原生网页浏览器实现。它封装了各平台的网页控件，对外提供一套统一的浏览 API。

## 属性 {#properties}

### Source

```csharp
public Uri Source { get; set; }
```

WebView 中所显示顶层文档的 URI。设置该属性等同于调用 `Navigate()`。

默认值：`about:blank`

### CanGoBack

```csharp
public bool CanGoBack { get; }
```

指示 WebView 能否在导航历史中回到上一页。

### CanGoForward

```csharp
public bool CanGoForward { get; }
```

指示 WebView 能否在导航历史中前往下一页。

## 事件 {#events}

### AdapterCreated

```csharp
public event EventHandler<WebViewAdapterEventArgs>? AdapterCreated;
```

底层 webview 适配器初始化完成后触发。

### AdapterDestroyed

```csharp
public event EventHandler<WebViewNavigationCompletedEventArgs>? AdapterDestroyed;
```

底层 webview 适配器销毁之后触发。

### EnvironmentRequested

```csharp
public event EventHandler<WebViewEnvironmentRequestedEventArgs>? EnvironmentRequested;
```

在底层 webview 适配器创建之前触发，用于定制 webview 环境。可以在 webview 初始化之前，用这个事件修改环境选项（比如启用隐私模式或开发者工具）。事件参数的类型因平台而异。

详见[环境选项](/controls/web/webview-environment)页面。

### NavigationCompleted

```csharp
public event EventHandler<WebViewNavigationCompletedEventArgs>? NavigationCompleted;
```

顶层文档导航渲染完成后触发，无论成功与否。

### NavigationStarted

```csharp
public event EventHandler<WebViewNavigationStartingEventArgs>? NavigationStarted;
```

顶层文档的新导航开始之前触发。

### NewWindowRequested

```csharp
public event EventHandler<WebViewNewWindowRequestedEventArgs>? NewWindowRequested;
```

顶层文档的新导航开始之前触发。

### WebMessageReceived

```csharp
public event EventHandler<WebMessageReceivedEventArgs>? WebMessageReceived;
```

网页内容通过 `invokeCSharpAction(body)` 向宿主应用发送消息后触发。

### WebResourceRequested

```csharp
public event EventHandler<WebResourceRequestedEventArgs>? WebResourceRequested;
```

WebView 向匹配的 URL 发起请求时触发。参数中包含请求信息和请求头字典。

:::note
请求头字典是否只读，视请求和平台而定。请务必检查 `TrySet` 和 `TryRemove` 方法的返回结果。
:::

#### 用法示例 {#usage-example}

JS&lt;-&gt;C# 双向通信示例：

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

## 方法 {#methods}

### Navigate

```csharp
public void Navigate(Uri url)
```

把 WebView 导航到指定的 URI。

### NavigateToString

```csharp
public void NavigateToString(string text)
```

把给定的 HTML 字符串渲染为顶层文档。

### InvokeScript

```csharp
public Task<string?> InvokeScript(string scriptName)
```

在顶层文档中执行给定的 JavaScript。

#### 用法示例 {#usage-example-1}

```xml
<NativeWebView Source="https://avaloniaui.net/" NavigationCompleted="WebView_NavigationCompleted" />
```

```csharp
private async void WebView_NavigationCompleted(object? sender, WebViewNavigationCompletedEventArgs args)
{
    // Execute JavaScript
    await webView.InvokeScript("alert('Hello World')");
}
```

### GoBack

```csharp
public bool GoBack()
```

回到导航历史中的上一页。无法导航时返回 `false`。

### GoForward

```csharp
public bool GoForward()
```

前往导航历史中的下一页。无法导航时返回 `false`。

### Refresh

```csharp
public bool Refresh()
```

重新加载当前页面。

### Stop

```csharp
public bool Stop()
```

停止正在进行的导航。

### ShowPrintUI

```csharp
void ShowPrintUI();
```

打开打印对话框，打印当前网页。

### PrintToPdfStreamAsync

```csharp
Task<Stream> PrintToPdfStreamAsync();
```

异步获取当前网页的 PDF 数据。

:::note

该 API 不接受页边距、纸张方向这类扩展打印选项。若要兼顾更多平台，建议改用自定义 CSS 规则——[@media print](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media#print) 和 [@page](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@page)。

:::

### TryGetCommandManager

```csharp
public NativeWebViewCommandManager? TryGetCommandManager()
```

若平台支持，返回一个 `NativeWebViewCommandManager` 实例，用于执行常见的键盘命令。

#### 用法示例 {#usage-example-2}

```csharp
var commandManager = webView.TryGetCommandManager();
if (commandManager != null)
{
    // Copy selected content
    commandManager.Copy();
}
```

### TryGetCookieManager

```csharp
public NativeWebViewCookieManager? TryGetCookieManager()
```

若平台支持，返回一个 `NativeWebViewCookieManager` 实例，用于管理 Cookie。

`NativeWebViewCookieManager` 对外提供：

```csharp
public Task<IReadOnlyList<Cookie>> GetCookiesAsync()
public void AddOrUpdateCookie(Cookie cookie)
public void DeleteCookie(Cookie cookie)
```

`DeleteCookie(string name, string domain, string path)` 已废弃，且在 Linux 上无效；请改为传入 `System.Net.Cookie`。

#### 用法示例 {#usage-example-3}

```csharp
var cookieManager = webView.TryGetCookieManager();
if (cookieManager != null)
{
    // Get all cookies
    var cookies = await cookieManager.GetCookiesAsync();

    // Delete one of them
    foreach (var cookie in cookies.Where(c => c.Name == "session"))
        cookieManager.DeleteCookie(cookie);
}
```

### TryGetPlatformHandle

```csharp
public IPlatformHandle? TryGetPlatformHandle()
```

返回原生控件的平台句柄，用于访问平台专有 API。详见[嵌入网页内容](/docs/app-development/embedding-web-content)页面。

### BeginReparenting

```csharp
public IDisposable BeginReparenting(bool yieldOnLayoutBeforeExiting = true)
```

在父级变更期间推迟销毁原生控件。

### BeginReparentingAsync

```csharp
public IAsyncDisposable BeginReparentingAsync()
```

在父级变更期间异步推迟销毁原生控件。

## 平台支持 {#platform-support}

| 特性                | Windows WebView2-Edge | macOS/iOS WKWebView | Linux WPE / WebKitGTK | Android | 浏览器 |
|------------------------|-----------------------|---------------------|------------------|---------|---------|
| `NativeWebView`        | ✓                     | ✓                   | ✓                | ✓       | ✗*      |
| `TryGetCommandManager` | ✓                     | ✓                   | ✗*               | ✓       | ✗*      |
| `TryGetCookieManager`  | ✓                     | ✓                   | ✓                | ✓       | ✗*      |
| `ShowPrintUI`          | ✓                     | ✓                   | ✗*               | ✗*      | ✗*      |
| `PrintToPdfStreamAsync`| ✓                     | ✓**                 | ✗*               | ✗*      | ✗*      |

\* 技术上可行，但尚未实现。如果这挡住了你的项目，欢迎提 issue。

\** macOS 不允许使用 PrintToPdfStreamAsync 的扩展打印选项，请改用自定义 CSS 规则——[@media print](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media#print) 和 [@page](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@page)。

:::note

在 Linux 上，`NativeWebView` 会自动挑选后端：它优先使用 [WPE WebKit](https://wpewebkit.org)（通过 SHM 离屏渲染），未安装 WPE 时则改用 WebKitGTK。两种情形都不需要额外配置——各后端所需的软件包见 [Linux 前置条件](/docs/app-development/embedding-web-content#linux)。

若机器上装了 WPE 却仍想用 WebKitGTK，请把 [`LinuxWpeWebViewEnvironmentRequestedEventArgs.PreferWebKitGtkInstead`](/controls/web/webview-environment#linux-wpe-webkit) 设为 `true`。
:::

## 另请参阅 {#see-also}

- [NativeWebDialog](/controls/web/nativewebdialog)
- [WebAuthenticationBroker](/controls/web/webauthenticationbroker)
- [WebView 环境选项](/controls/web/webview-environment)
- [嵌入网页内容](/docs/app-development/embedding-web-content)
- [FAQ](/tools/faq#webview)
