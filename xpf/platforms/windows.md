---
id: windows
title: Windows
description: 运行 XPF 应用时与 Windows 相关的注意事项，包括 Win32 API 的行为和兼容性说明。
---

## 概述 {#overview}

Windows 是 WPF 的原生平台，XPF 应用在 Windows 上完全兼容地运行。本页讲的是用 XPF（而非标准 WPF）时，Windows 上需要留意的事项。

## Win32 API 的行为 {#win32-api-behavior}

在 Windows 上启用 Win32 API shim 后，相关调用会绕道 XPF 的 shim 层，而不是直通原生 Win32 API。这样一来，开发和测试期间的行为就与非 Windows 平台保持一致了。

若你需要直接调用原生 Win32 API（绕开 shim），请把这些调用挪到一个单独的程序集里，并把它从 shim 中排除：

```csharp
AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable(asm =>
{
    if (asm.GetName().Name == "MyNativeWindowsInterop")
        return true; // skip this assembly
    return false;
});
```

## 承载 WinForms {#winforms-hosting}

XPF 在 Windows 上可以承载 WinForms 控件。在按 Windows 条件生效的属性组中加上下面的内容即可启用：

```xml
<PropertyGroup Condition="$([MSBuild]::IsOSPlatform('Windows'))">
    <XpfUseMicrosoftWindowsForms>true</XpfUseMicrosoftWindowsForms>
</PropertyGroup>
```

这会关掉 XPF 的 WinForms shim 层，改用原生的 WinForms 集成。承载 WinForms 只在 Windows 上可用，请给属性组加上条件，免得在别的平台上构建失败。

## STA 线程 {#sta-threading}

有些 Windows 操作要求主线程标记为 STA（单线程单元）：

- 通过 COM 进行的剪贴板操作
- OLE 拖放
- 某些第三方 COM 组件

若你遇到 `COMException: CoInitialize was not called`，请给入口点加上 `[STAThread]` 特性。若采用[自定义初始化](/xpf/configuration/customizing-initialization)，XPF 会自动处理好这件事。

## CefSharp

`CefSharp.Wpf.NetCore` 在 Windows 上可与 XPF 搭配使用。若 `CursorInteropHelper.Create()` 抛出 `NotImplementedException`，请升级到 XPF 1.6.0 或更高版本。

对更老的 XPF 版本，变通办法是从 `ChromiumWebBrowser` 派生并重写 `OnCursorChange`：

```csharp
protected override void OnCursorChange(object sender, CursorChangeEventArgs e)
{
    // Map CefSharp cursor types to WPF Cursors
    var cursor = e.CursorType switch
    {
        CefCursorType.Hand => Cursors.Hand,
        CefCursorType.IBeam => Cursors.IBeam,
        CefCursorType.Cross => Cursors.Cross,
        CefCursorType.Wait => Cursors.Wait,
        _ => Cursors.Arrow
    };
    Cursor = cursor;
}
```

跨平台的浏览器嵌入请见[嵌入网页内容](/xpf/interop/web-content)。

## 窗口句柄 {#window-handles}

对 `WindowInteropHelper.Handle` 这类 WPF API 调用，XPF 用的是虚拟窗口句柄。在 Windows 上，它们就是真正的 HWND。若要直接拿到底层句柄，请用 Avalonia 的互操作 API：

```csharp
using Atlantis;

var avaloniaWindow = XpfWpfAbstraction.GetAvaloniaWindowForWindow(myWpfWindow);
var handle = avaloniaWindow.TryGetPlatformHandle();
// handle.Handle is the native HWND on Windows
```

更多细节请见[原生窗口句柄](/xpf/interop/native-window-handles)。

## 部署 {#deployment}

发布、打包和安装程序方面的指引，请见 [Windows 部署](/xpf/deployment/windows)。
