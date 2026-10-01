---
id: webauthenticationbroker
title: WebAuthenticationBroker
---

## 概述 {#overview}

`WebAuthenticationBroker` 是一个工具类，为桌面应用提供安全的网页认证处理方式，用来跑通 OAuth 等基于网页的认证流程。

它会导航到起始 URI，等待流程走到重定向 URI，再把回调结果交还给你。流程以何种形式呈现，取决于所选的[模式](#webauthenticatormode)。

这个 broker 只负责流程中浏览器那一段。若还要构造授权请求、用授权码换令牌，请参阅 [OAuth 2.0 与 PKCE](#oauth-20-with-pkce)。

## 静态方法 {#static-methods}

### AuthenticateAsync

```csharp
public static Task<WebAuthenticationResult> AuthenticateAsync(
    TopLevel topLevel, WebAuthenticatorOptions options)
```

导航到指定的起始 URI，并监视是否导航到结束 URI，以此启动一次认证流程。

#### 参数 {#parameters}

- `topLevel`：所有者顶层元素，在桌面平台上就是一个窗口。
- `options`：控制 broker 行为的认证选项

#### 返回值 {#returns}

一个 `Task<WebAuthenticationResult>`，其中包含认证结果。

## WebAuthenticatorMode <MinVersion version="12.1" isNewVersion="true" />

选择由哪个实现来跑这个流程。

| 模式 | 说明 | 平台 |
|------|-------------|-----------|
| `Auto` | 默认值。按 `System`、`NativeWebDialog`、`Browser` 的顺序解析为第一个受支持的模式。 | All |
| `System` | 使用平台原生的网页认证 API。 | macOS, iOS, Android, Browser |
| `NativeWebDialog` | 在一个内嵌 web 视图的 [NativeWebDialog](/controls/web/nativewebdialog) 中展示流程。 | Windows, macOS, Linux, Android |
| `Browser` | 在用户的默认浏览器中打开流程，并由本地 HTTP 监听器接收重定向。 | 除浏览器外的全部平台 |

## WebAuthenticatorOptions

### 属性 {#properties}

```csharp
public Uri RequestUri { get; init; }
```

启动认证流程的初始 URI。

```csharp
public Uri RedirectUri { get; init; }
```

标志认证流程结束的 URI。

```csharp
public WebAuthenticatorMode Mode { get; init; }
```

用于跑这个流程的实现，参见 [WebAuthenticatorMode](#webauthenticatormode)。

```csharp
public bool NonPersistent { get; init; }
```

提示平台实现不要持久化任何会话数据。`WebAuthenticatorMode.Browser` 会忽略它，因为那用的是用户自己的浏览器会话。

```csharp
public BrowserOptions? BrowserOptions { get; init; }
```

当 `Mode` 为 `WebAuthenticatorMode.Browser` 时所用的选项，参见 [BrowserOptions](#browseroptions)。

```csharp
public Func<NativeWebDialog?> NativeWebDialogFactory { get; init; }
```

当 WebAuthenticationBroker 走对话框实现（而非系统认证 API）时，可用这个回调接管 [NativeWebDialog](/controls/web/nativewebdialog) 的创建。

## 浏览器模式 <MinVersion version="12.1" isNewVersion="true" /> {#browser-mode}

`WebAuthenticatorMode.Browser` 会拉起系统浏览器，并在回环接口上启动监听器接收重定向。`RedirectUri` 必须是 `http` 回环地址，比如 `http://127.0.0.1:5000/callback`。URI 中若未指定端口，操作系统会分配一个空闲端口。

:::warning
该监听器接受本机上任意进程的连接，因此回调属于不可信输入。请把 [`State`](#webauthenticationresult) 与你发出的值比对，并在使用 `Code` 之前先处理 `Error`。

强烈建议使用 PKCE [（RFC 8252 第 8.1 节）](https://www.rfc-editor.org/info/rfc8252/#section-8.1)：正是它让被注入的授权码在令牌端点上无从使用。用 [`CallbackFilter`](#callbackfilter) 可以在收到不属于本流程的请求时让监听器继续等待。
:::

### BrowserOptions

#### Timeout
```csharp
public TimeSpan Timeout { get; init; }
```

#### CallbackFilter
等待回调的时长，超时则取消流程。默认 5 分钟。

```csharp
public BrowserCallbackFilter? CallbackFilter { get; init; }
```

判断重定向路径上收到的请求是否属于本流程。返回 `false` 表示拒绝它并继续等待。常见做法是把 `State` 与授权请求中发出的值作比对。注意：过滤器放行并不等于该请求可信，调用方仍须自行校验结果。

```csharp
public delegate bool BrowserCallbackFilter(WebAuthenticationResult result);
```

#### ResponseHandler
```csharp
public BrowserResponseHandler? ResponseHandler { get; init; }
```

定制收到回调后返回给浏览器的 HTTP 响应。未指定时会发送一个默认响应。

```csharp
public delegate Task BrowserResponseHandler(
    WebAuthenticationResult result, BrowserResponse response);
```

`BrowserResponse` 提供了 `StatusCode` 和 `OutputStream`，你可以借此写一个「可以关闭此窗口了」的页面。`Redirect(Uri)` 则改为把浏览器重定向到某个绝对 URI，并把状态码设为 `302 Found`：

```csharp
ResponseHandler = (result, response) =>
{
    response.Redirect(new Uri("https://example.com/signed-in"));
    return Task.CompletedTask;
}
```

### Example

```csharp
var result = await WebAuthenticationBroker.AuthenticateAsync(
    mainWindow,
    new WebAuthenticatorOptions(requestUri, new Uri("http://127.0.0.1:5000/callback"))
    {
        Mode = WebAuthenticatorMode.Browser,
        BrowserOptions = new BrowserOptions
        {
            Timeout = TimeSpan.FromMinutes(2),
            CallbackFilter = callback => callback.State == expectedState
        }
    });

if (result.Error is { } error)
    throw new InvalidOperationException($"{error}: {result.ErrorDescription}");

var code = result.Code;
```

## WebAuthenticationResult

### 属性 {#properties-1}

#### CallbackUri
```csharp
public Uri CallbackUri { get; }
```

包含认证数据的响应 URI。

#### 查询参数 {#query-parameters}
```csharp
public IReadOnlyDictionary<string, string> Parameters { get; }
```

`CallbackUri` 查询字符串中的各个参数。名称区分大小写。重复出现的名称会被忽略，因为 OAuth 2.0 不允许参数重复。

```csharp
public string? Code { get; }
public string? State { get; }
public string? Error { get; }
public string? ErrorDescription { get; }
```

对应的 OAuth 2.0 查询参数；若参数缺失或重复则为 `null`。请把 `State` 与授权请求中发出的值比对，并在使用 `Code` 之前先检查 `Error`。

## 用法示例 {#usage-example}

本例以 Google OAuth 为例。

最低限度的准备工作如下：

1. 创建 Google 凭据（类型：Windows/macOS/Linux 选 Desktop，或选 iOS），参见 [Console Credentials](https://console.cloud.google.com/apis/credentials)。这一步会生成客户端 ID 和重定向 URI。
2. 想了解总体原理，请阅读 Google 的 [OAuth 2.0](https://developers.google.com/identity/protocols/oauth2/web-server#httprest) 文档。

```csharp
var googleAuthRedirectUri = "http://localhost";
var googleAuthRequestUri = "https://accounts.google.com/o/oauth2/auth?response_type=code&access_type=offline&scope=openid";
googleAuthRequestUri += "&client_id=" + /* YOUR CLIENT ID */;
googleAuthRequestUri += "&redirect_uri=" + googleAuthRedirectUri;

var result = await WebAuthenticationBroker.AuthenticateAsync(
    mainWindow,
    new WebAuthenticatorOptions(
        RequestUri: new Uri(googleAuthRequestUri),
        RedirectUri: new Uri(googleAuthRedirectUri)));
```

[Microsoft identity](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)、[Facebook Login](https://developers.facebook.com/docs/facebook-login/) 等兼容 OAuth2 标准的方案，做法也大同小异。

## OAuth 2.0 与 PKCE <MinVersion version="12.1" isNewVersion="true" /> {#oauth-20-with-pkce}

`Avalonia.Controls.OAuth2` 命名空间下的 `AuthorizationCodePkceSession` 负责授权码流程中浏览器之外的那些环节，省得你手工拼装上面那个请求：

```csharp
var session = await AuthorizationCodePkceSession.CreateAsync(
    "https://id.example.com", clientId, "http://127.0.0.1:5000/callback", "openid profile");

var options = new WebAuthenticatorOptions(session.AuthorizationUri, session.RedirectUri)
{
    Mode = WebAuthenticatorMode.Browser,
    BrowserOptions = new BrowserOptions { CallbackFilter = session.IsCallbackFor }
};

var result = await WebAuthenticationBroker.AuthenticateAsync(topLevel, options);
var token = await session.ExchangeCodeAsync(result);
```

`CreateAsync` 会按 [RFC 8414](https://www.rfc-editor.org/rfc/rfc8414) 从颁发者处发现各个端点，不行再退回 OpenID Connect discovery。若服务器没有发布元数据，请改用 `Create` 并显式指定端点。

`ExchangeCodeAsync` 会先检查 `state`，再去读回调中的其他内容；遇到 `error` 响应则直接拒绝，并返回一个 `OAuth2TokenResponse`。其中的 `IdToken` 按收到的原样透传，不做校验。

## 平台支持 {#platform-support}

| 特性                     | Windows | macOS (10.15+) | Linux | iOS (iOS 12.0+) | Android  | 浏览器  |
|-----------------------------|---------|-------|-------|-----|-----------|-----------|
| Platform Implementation  | ✗       | ✓*     | ✗     | ✓*   | ✓**         | ✓***         |
| NativeWebDialog         | ✓       | ✓     | ✓     | ✗   | ✗         | ✗         |
| Browser                 | ✓       | ✓     | ✓     | ✓   | ✓         | ✗         |

\* Apple 平台使用 ASWebAuthenticationSession 实现。  
\** Android 使用 CustomTabsIntent 实现，但该支持尚属实验性，后续可能变动。  
\*** 浏览器方案需要配置 CORS 以允许访问重定向后的页面；在浏览器中运行这个库还需要 .NET 10。

## 另请参阅 {#see-also}

- [NativeWebView](/controls/web/nativewebview)
- [NativeWebDialog](/controls/web/nativewebdialog)
- [WebView 环境选项](/controls/web/webview-environment)
- [嵌入网页内容](/docs/app-development/embedding-web-content)
- [FAQ](/tools/faq#webview)
