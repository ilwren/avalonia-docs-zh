---
id: webassembly
title: WebAssembly
---

Avalonia 应用可以借助 WebAssembly（WASM）跑在浏览器里。本页讲解如何为浏览器部署配置项目，以及如何使用 JavaScript 互操作。

## 为 WebAssembly 配置 Avalonia 项目 {#setting-up-an-avalonia-project-for-webassembly}

1. 安装 `wasm-tools` 工作负载，它提供了把 .NET 编译成 WebAssembly 的构建工具链。

```bash
dotnet workload install wasm-tools
```

:::note
若你在 .NET 9 SDK 上运行 `net8.0-browser` 应用，应改装 `wasm-tools-net8` 工作负载。
若你的 .NET SDK 较旧，它可能还会要求你装上 `wasm-experimental` 之类的其他工作负载。
:::

2. 安装或把 dotnet 模板更新到最新版。

```bash
dotnet new install avalonia.templates
```

3. 为项目新建一个目录。

```bash
mkdir BrowserTest
cd BrowserTest
```

4. 生成一个支持在浏览器中运行的新项目。运行 `dotnet new list` 可查看所有可用的 Avalonia 模板。

```bash
dotnet new avalonia.xplat
```

5. 控制台输出里会给出打开应用的 HTTP 和 HTTPS 链接。
运行应用：

```bash
cd BrowserTest.Browser
dotnet run

# Output:
# App url: http://127.0.0.1:53576/
# App url: https://127.0.0.1:53577/
# Debug at url: http://127.0.0.1:53576/_framework/debug
# Debug at url: https://127.0.0.1:53577/_framework/debug
```

## 部署 {#deployment}

关于如何发布和部署 WebAssembly 应用，请见[部署 WebAssembly](/docs/deployment/webassembly)。

## JavaScript 互操作 {#javascript-interop}

Avalonia Browser 应用可以借助 .NET 标准的 `[JSImport]`/`[JSExport]` 互操作 API，从 C# 调用 JavaScript，也能把 C# 方法暴露给 JavaScript。该 API 属于 `System.Runtime.InteropServices.JavaScript` 命名空间，在任何 .NET WebAssembly 应用中都能用。

### 配置 {#setup}

在 Browser 项目文件中加上 `AllowUnsafeBlocks`。生成互操作绑定的 .NET 源生成器需要它：

```xml
<PropertyGroup>
    <AllowUnsafeBlocks>true</AllowUnsafeBlocks>
</PropertyGroup>
```

### 从 C# 调用 JavaScript {#calling-javascript-from-c}

在 `partial` 方法上使用 `[JSImport]` 特性即可导入一个 JavaScript 函数。第一个参数是 JS 函数名，第二个是加载它时所用的模块名。

创建一个 JavaScript 模块（比如 `wwwroot/js/interop.js`）：

```javascript
export function showAlert(message) {
    globalThis.alert(message);
}

export function getCurrentUrl() {
    return globalThis.window.location.href;
}
```

定义与这些 JS 函数对应的 C# 方法：

```csharp
using System.Runtime.InteropServices.JavaScript;
using System.Runtime.Versioning;

[SupportedOSPlatform("browser")]
public partial class JsInterop
{
    [JSImport("showAlert", "MyInterop")]
    public static partial void ShowAlert(string message);

    [JSImport("getCurrentUrl", "MyInterop")]
    public static partial string GetCurrentUrl();
}
```

启动时（通常在 `Program.cs` 中）用 `JSHost.ImportAsync` 加载该模块，之后便可在应用的任何地方调用这些方法：

```csharp
using System.Runtime.InteropServices.JavaScript;

await JSHost.ImportAsync("MyInterop", "../js/interop.js");

// Now you can call:
JsInterop.ShowAlert("Hello from Avalonia!");
string url = JsInterop.GetCurrentUrl();
```

传给 `JSHost.ImportAsync` 的模块名必须与 `[JSImport]` 特性中的第二个参数一致。

### 从 JavaScript 调用 C# {#calling-c-from-javascript}

用 `[JSExport]` 特性把 C# 方法暴露给 JavaScript：

```csharp
[SupportedOSPlatform("browser")]
public partial class JsInterop
{
    [JSExport]
    public static string GetAppVersion() => "1.0.0";
}
```

在 JavaScript 一侧，通过 .NET 运行时访问导出的方法：

```javascript
export async function callDotNet() {
    const { getAssemblyExports } = await globalThis.getDotnetRuntime(0);
    const exports = await getAssemblyExports("MyApp.dll");
    const version = exports.MyNamespace.JsInterop.GetAppVersion();
    console.log(version);
}
```

### 访问全局函数 {#accessing-global-functions}

若要从全局作用域（而非某个模块）导入函数，请在函数名前加上 `globalThis` 前缀并省略模块名：

```csharp
[JSImport("globalThis.console.log")]
public static partial void ConsoleLog(string message);
```

### 类型封送 {#type-marshalling}

.NET 类型会自动封送为对应的 JavaScript 类型。若想精确掌控封送方式，请使用 `[JSMarshalAs]` 特性：

```csharp
[JSImport("processData", "MyInterop")]
public static partial void ProcessData(
    [JSMarshalAs<JSType.Number>] long value);
```

你可以把 `Action`/`Func` 回调作为参数传过去（会被封送成可调用的 JS 函数），JS 对象引用和托管对象引用也都能以代理对象的形式跨越边界传递。

## 另请参阅 {#see-also}

- [Deploying WebAssembly](/docs/deployment/webassembly)
- [WebAssembly 排查问题](/troubleshooting/platform-specific-issues/webassembly)
