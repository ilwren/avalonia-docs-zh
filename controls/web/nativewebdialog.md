---
id: nativewebdialog
title: NativeWebDialog
---

`NativeWebDialog` 是一个承载原生网页浏览器的对话框窗口。若你想在独立窗口中展示网页内容、而不把它嵌进自己的布局，或者目标平台上没有可嵌入的 `NativeWebView` 控件，就可以用它。

## 常用属性 {#useful-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Title` | `string?` | 对话框窗口的标题。 |
| `CanUserResize` | `bool` | 用户能否调整对话框大小。 |
| `Source` | `Uri` | WebView 中所显示页面的 URI。设置该属性等同于调用 `Navigate()`。默认值：`about:blank`。 |
| `CanGoBack` | `bool` | 只读。当 WebView 可以在历史记录中后退时为 `true`。 |
| `CanGoForward` | `bool` | 只读。当 WebView 可以在历史记录中前进时为 `true`。 |
| `DefaultBackground` | `Color?` | 对话框及其内部 web 视图的背景色。为 `null` 时使用所有者窗口的背景色，再退一步则用白色。 |
| `ShowFocused` | `bool` | 对话框显示时是否把键盘焦点移到网页内容上。默认值：`true`。 |

## 基本示例 {#basic-example}

创建对话框、导航到某个 URL，并等它关闭：

```csharp
var dialog = new NativeWebDialog
{
    Title = "Avalonia Docs",
    CanUserResize = false,
    Source = new Uri("https://docs.avaloniaui.net/")
};

var tcs = new TaskCompletionSource();
dialog.Closing += (s, e) => tcs.SetResult();

dialog.Show(mainWindow);

await tcs.Task;
```

也可以直接加载 HTML：

```csharp
var dialog = new NativeWebDialog { Title = "Preview" };
dialog.Show();
dialog.NavigateToString("<h1>Hello from Avalonia</h1>");
```

## 显示对话框 {#showing-the-dialog}

调用 `Show()` 可把对话框作为独立窗口打开，调用 `Show(IPlatformHandle)` 则可带所有者窗口打开：

```csharp
// Standalone
dialog.Show();

// With an owner window
dialog.Show(mainWindow);
```

用 `Close()` 可以在代码中关闭它。`Closing` 事件在对话框关闭之前触发，便于你做清理工作。

对话框显示时默认会把键盘焦点移进网页内容。把 `ShowFocused` 设为 `false` 可让焦点原地不动，之后再调用 `Focus()` 激活对话框并把键盘焦点移到网页内容上：

```csharp
dialog.ShowFocused = false;
dialog.Show(mainWindow);

// Later, bring it forward and focus the page.
dialog.Focus();
```

## Navigation

| 方法 | 说明 |
|---|---|
| `Navigate(Uri)` | 导航到指定的 URI。 |
| `NavigateToString(string)` | 把一段 HTML 字符串渲染为页面内容。 |
| `GoBack()` | 后退。若没有历史记录则返回 `false`。 |
| `GoForward()` | 前进。若没有历史记录则返回 `false`。 |
| `Refresh()` | 重新加载当前页面。 |
| `Stop()` | 停止正在进行的导航。 |

## Running JavaScript

在已加载的页面中执行 JavaScript 并取回结果：

```csharp
var result = await dialog.InvokeScript("document.title");
```

要接收来自 JavaScript 的消息，请订阅 `WebMessageReceived`。网页内容通过调用 `invokeCSharpAction(body)` 发送消息：

```csharp
dialog.WebMessageReceived += (sender, e) =>
{
    var message = e.Body;
    // Process the message from JavaScript
};
```

## Printing

| 方法 | 说明 |
|---|---|
| `ShowPrintUI()` | 打开平台的打印对话框。 |
| `PrintToPdfStreamAsync()` | 把当前页面导出为 PDF 流。 |

:::note
`PrintToPdfStreamAsync` 不接受页边距、纸张方向这类扩展打印选项。若要兼顾更多平台，请改用 [@media print](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media#print) 和 [@page](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@page) 这类 CSS 规则。
:::

## 拦截请求 {#intercepting-requests}

WebView 发起 URL 请求时会触发 `WebResourceRequested` 事件，你可以借此查看或修改请求头：

```csharp
dialog.WebResourceRequested += (sender, e) =>
{
    // Inspect e.Request and e.Headers
};
```

:::note
请求头字典是否只读，视请求和平台而定。请务必检查 `TrySet` 和 `TryRemove` 方法的返回结果。
:::

## 环境选项 {#environment-options}

`EnvironmentRequested` 事件在 WebView 适配器创建之前触发，让你定制各种选项，比如启用隐私模式或开发者工具：

```csharp
dialog.EnvironmentRequested += (sender, e) =>
{
    // Configure WebView environment before initialization
};
```

详见 [WebView 环境选项](/controls/web/webview-environment)。事件参数的类型因平台而异。

## 窗口大小与位置 {#window-sizing-and-position}

| 方法 | 说明 |
|---|---|
| `Resize(int, int)` | 把对话框调整为指定的宽度和高度。 |
| `Move(int, int)` | 把对话框移动到指定的屏幕坐标。 |

## Advanced

| 方法 | 说明 |
|---|---|
| `TryGetCommandManager()` | 若平台支持，返回用于键盘命令（复制、粘贴等）的 `NativeWebViewCommandManager`。 |
| `TryGetCookieManager()` | 若平台支持，返回用于管理 Cookie 的 `NativeWebViewCookieManager`。 |
| `TryGetWebViewPlatformHandle()` | 返回所承载 WebView 的平台句柄，参见[嵌入网页内容](/docs/app-development/embedding-web-content)。 |
| `TryGetPlatformHandle()` | 返回对话框窗口本身的平台句柄。 |

## 事件 {#events}

| 事件 | 说明 |
|---|---|
| `Closing` | 在对话框关闭之前触发。 |
| `AdapterCreated` | WebView 适配器初始化完成后触发。 |
| `AdapterDestroyed` | WebView 适配器销毁之后触发。 |
| `EnvironmentRequested` | 在 WebView 适配器创建之前触发，用于配置环境选项。 |
| `NavigationStarted` | 新的导航开始之前触发。 |
| `NavigationCompleted` | 导航结束后触发，无论成功与否。 |
| `NewWindowRequested` | WebView 请求打开新窗口时触发（例如来自 `window.open()`）。 |
| `WebMessageReceived` | 网页内容调用 `invokeCSharpAction(body)` 时触发。 |
| `WebResourceRequested` | WebView 发起 URL 请求时触发。 |

## 平台支持 {#platform-support}

| 特性 | Windows | macOS | Linux | iOS | Android | 浏览器 |
|---|---|---|---|---|---|---|
| `Show` | Yes | Yes | Yes | No | No | No |
| `Show(Window)` | Yes | Yes | Yes* | No | No | No |
| `WebMessageReceived` | Yes | Yes | No | No | No | No |
| `ShowPrintUI` | Yes | Yes | Yes | No | No | No |
| `PrintToPdfStreamAsync` | Yes | Yes** | Yes | No | No | No |

\* Linux 上的支持情况可能因窗口管理器而异。

\** macOS 不支持扩展的 `PrintToPdfStreamAsync` 打印选项，请改用 CSS 的 `@media print` 和 `@page` 规则。

## 另请参阅 {#see-also}

- [NativeWebView](/controls/web/nativewebview)：可嵌入自己布局中的 WebView 控件。
- [WebAuthenticationBroker](/controls/web/webauthenticationbroker)：OAuth 与基于网页的认证流程。
- [WebView 环境选项](/controls/web/webview-environment)：配置 WebView 运行环境。
- [嵌入网页内容](/docs/app-development/embedding-web-content)：在 Avalonia 应用中承载网页内容。
- [常见问题](/tools/faq#webview)：WebView 的常见疑问。
