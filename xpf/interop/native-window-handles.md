---
id: native-window-handles
title: 获取原生窗口句柄
description: 如何在 XPF 应用中取得各平台的原生窗口句柄，以及虚拟句柄与原生句柄的区别。
---

## 概述 {#overview}

XPF 有一套机制，各类 WPF API 调用返回的句柄其实都是_虚拟句柄_。如此一来，XPF 便能拦下用到这些句柄的 API 调用，并自动翻译成相应的跨平台 API。于是 `WindowInteropHelper.Handle` 这类 WPF API 乃至[模拟的 Win32 API](/xpf/third-party/win32-api-shims)返回的，都是这些虚拟化的窗口句柄。

## 什么时候需要原生句柄 {#when-you-need-native-handles}

下列情形下你可能需要拿到真正的原生窗口句柄：

- 与需要窗口句柄的原生平台 API 打交道
- 嵌入原生控件或渲染表面（OpenGL、DirectX、Metal）
- 使用 WPF 或 Avalonia API 给不了的平台专属功能
- 与原生的无障碍或自动化框架集成

## 取得原生句柄 {#getting-a-native-handle}

窗口的原生句柄可以从[底层的 Avalonia `Window`](/xpf/interop/embedding-avalonia-in-xpf#getting-the-avalonia-window) 取得：

```csharp
using Atlantis;

var avaloniaWindow = XpfWpfAbstraction.GetAvaloniaWindowForWindow(myWpfWindow);
var platformHandle = avaloniaWindow.TryGetPlatformHandle();

if (platformHandle != null)
{
    IntPtr nativeHandle = platformHandle.Handle;
    string handleType = platformHandle.HandleDescriptor;
    // Use the native handle
}
```

## 各平台的句柄类型 {#handle-types-by-platform}

返回什么类型的句柄取决于操作系统：

| 平台 | Handle Type | HandleDescriptor | 注释支持情况 |
|---|---|---|---|
| Windows | HWND | `"HWND"` | 标准的 Win32 窗口句柄 |
| macOS | NSWindow* | `"NSWindow"` | 指向 NSWindow 对象的指针 |
| Linux (X11) | X11 Window | `"XID"` | X11 窗口标识符 |

:::caution
原生句柄不能传给 Win32 API 模拟层。模拟层认的是 XPF 的虚拟句柄，而非平台原生句柄。若要调用经过 shim 的 Win32 API，请改用 `WindowInteropHelper.Handle` 给出的虚拟句柄。
:::

## 取得 Avalonia 的 `TopLevel` {#getting-the-avalonia-toplevel}

有些操作不需要窗口句柄，但要用到 Avalonia 层面的属性（比如渲染缩放或输入处理），这时请用 `GetAvaloniaTopLevelForWindow`：

```csharp
using Atlantis;

var topLevel = XpfWpfAbstraction.GetAvaloniaTopLevelForWindow(myWpfWindow);

// Access render scaling (useful for DPI-aware rendering)
double scaling = topLevel.RenderScaling;
```

## 示例：DPI 感知的原生渲染 {#example-dpi-aware-native-rendering}

```csharp
using Atlantis;

private void SetupNativeRendering(System.Windows.Window wpfWindow)
{
    var avaloniaWindow = XpfWpfAbstraction.GetAvaloniaWindowForWindow(wpfWindow);
    var platformHandle = avaloniaWindow.TryGetPlatformHandle();

    if (platformHandle == null)
        return;

    double scaling = avaloniaWindow.RenderScaling;
    IntPtr handle = platformHandle.Handle;

    switch (platformHandle.HandleDescriptor)
    {
        case "HWND":
            // Windows: use HWND for DirectX/OpenGL context creation
            InitializeWindowsRenderer(handle, scaling);
            break;
        case "NSWindow":
            // macOS: use NSWindow for Metal/OpenGL context creation
            InitializeMacRenderer(handle, scaling);
            break;
        case "XID":
            // Linux: use X11 Window for OpenGL context creation
            InitializeLinuxRenderer(handle, scaling);
            break;
    }
}
```

## 另请参阅 {#see-also}

- [在 XPF 中嵌入 Avalonia](/xpf/interop/embedding-avalonia-in-xpf)——如何从 XPF 中用上 Avalonia 的能力
- [性能：嵌入高性能内容](/xpf/configuration/performance#embedding-high-performance-content)——OpenGL 集成
