---
id: native-interop
title: 与原生平台互操作
description: 在 Avalonia 应用中访问原生平台 API、嵌入原生视图、使用 P/Invoke。
doc-type: overview
---

Avalonia 提供了多种机制，让你既能调用原生平台 API，也能把原生内容嵌入应用之中。

## 平台专属代码的写法 {#platform-specific-code-patterns}

简单的平台分支，用运行时检测或条件编译即可，相关写法参见[跨平台架构](/docs/fundamentals/cross-platform-architecture)。

面对更复杂的原生集成，Avalonia 让你能直接拿到底层平台的窗口句柄和原生 API。

## 获取原生窗口句柄 {#accessing-native-window-handles}

你可以取出原生窗口句柄，以便与平台 API 互操作：

```csharp
if (TopLevel.GetTopLevel(this)?.TryGetPlatformHandle() is { } handle)
{
    // handle.Handle is the native handle
    IntPtr nativeHandle = handle.Handle;

    // handle.HandleDescriptor tells you the type
    string kind = handle.HandleDescriptor;
}
```

返回的句柄类型因平台而异：

| 平台 | HandleDescriptor | Native Type |
|---|---|---|
| Windows | `HWND` | Win32 窗口句柄 |
| macOS | `NSWindow` | AppKit 窗口指针 |
| Linux (X11) | `X11` | X11 Window ID |
| iOS | `UIViewControlHandle` | UIKit 视图引用 |
| Android | `AndroidViewControlHandle` | Android 视图引用 |
| Browser | `JSObjectControlHandle` | 容器 `<div>` 元素的引用 |

它在下列场景中很有用：
- 通过操作系统 API 注册全局热键
- 调用原生的窗口函数（比如 Win32 的 `SetWindowPos`）
- 把窗口句柄传给需要父窗口的原生库
- 与各平台专属的移动端 SDK 集成

## 嵌入原生视图 {#embedding-native-views}

Avalonia 支持用 [`NativeControlHost`](/api/avalonia/controls/nativecontrolhost) 把原生 UI 控件嵌进 Avalonia 的视觉树，于是你可以在 Avalonia 布局中使用平台专属控件（比如原生网页浏览器、媒体播放器或地图视图）。

### NativeControlHost

`NativeControlHost` 这个控件会在 Avalonia 布局中占出一块空间，并在该区域内承载一个原生视图：

```csharp
public class NativeTextEditor : NativeControlHost
{
    protected override IPlatformHandle CreateNativeControlCore(
        IPlatformHandle parent)
    {
        if (OperatingSystem.IsWindows())
        {
            // Create a Win32 EDIT control
            var hwnd = CreateWindowEx(0, "EDIT", "",
                WS_CHILD | WS_VISIBLE | ES_MULTILINE,
                0, 0, 100, 100,
                parent.Handle, IntPtr.Zero, IntPtr.Zero, IntPtr.Zero);

            return new PlatformHandle(hwnd, "HWND");
        }

        return base.CreateNativeControlCore(parent);
    }

    protected override void DestroyNativeControlCore(
        IPlatformHandle control)
    {
        if (OperatingSystem.IsWindows())
        {
            DestroyWindow(control.Handle);
        }
        else
        {
            base.DestroyNativeControlCore(control);
        }
    }
}
```

在 XAML 中像使用任何其他控件那样使用 `NativeControlHost`：

```xml
<Border BorderBrush="Gray" BorderThickness="1">
    <local:NativeTextEditor MinHeight="200" />
</Border>
```

### 嵌入原生视图的局限 {#limitations-of-native-embedding}

原生视图位于 Avalonia 渲染表面之上，这意味着：

- **不支持透明**：原生视图的背景无法做成透明，也就看不到它后面的 Avalonia 内容。
- **不支持变换**：Avalonia 的渲染变换（旋转、缩放）对原生视图不起作用。
- **Z 序受限**：原生视图始终绘制在 Avalonia 内容之上，你没法把 Avalonia 控件叠在原生视图上面。
- **裁剪**：原生视图会被裁剪到宿主边界之内，但不支持复杂的裁剪几何。

## P/Invoke 与原生库 {#pinvoke-and-native-libraries}

要调用原生 C 库，用标准的 .NET P/Invoke 即可：

```csharp
using System.Runtime.InteropServices;

public static partial class NativeMethods
{
    // .NET 7+ LibraryImport (AOT-compatible)
    [LibraryImport("user32")]
    public static partial int MessageBoxW(
        IntPtr hWnd,
        [MarshalAs(UnmanagedType.LPWStr)] string text,
        [MarshalAs(UnmanagedType.LPWStr)] string caption,
        uint type);
}
```

若要以 Native AOT 方式发布，请用 `LibraryImport` 取代 `DllImport`，以确保封送代码在编译期生成。详见 [Native AOT 发布](/docs/deployment/native-aot)。

### 加载各平台专属的原生库 {#loading-platform-specific-native-libraries}

把原生库放进对应平台的 `runtimes` 文件夹：

```text
MyApp/
├── runtimes/
│   ├── win-x64/native/mylib.dll
│   ├── osx-arm64/native/libmylib.dylib
│   └── linux-x64/native/libmylib.so
```

在 `.csproj` 中引用它们：

```xml
<ItemGroup>
    <NativeLibrary Include="runtimes\win-x64\native\mylib.dll"
                   Pack="true"
                   PackagePath="runtimes/win-x64/native/" />
</ItemGroup>
```

.NET 运行时会自动为当前平台加载正确的库。

## 用依赖注入提供平台专属服务 {#platform-specific-services-with-dependency-injection}

面对复杂的原生集成，可以在共享项目中定义服务接口，再按平台分别实现：

```csharp
// Shared project
public interface INativeNotification
{
    void ShowNotification(string title, string message);
}

// Windows implementation
public class WindowsNotification : INativeNotification
{
    public void ShowNotification(string title, string message)
    {
        // Use Windows Toast Notification API
    }
}

// macOS implementation
public class MacNotification : INativeNotification
{
    public void ShowNotification(string title, string message)
    {
        // Use NSUserNotificationCenter
    }
}
```

在启动时注册对应的实现：

```csharp
if (OperatingSystem.IsWindows())
    services.AddSingleton<INativeNotification, WindowsNotification>();
else if (OperatingSystem.IsMacOS())
    services.AddSingleton<INativeNotification, MacNotification>();
```

完整的配置方法请参阅[依赖注入](/docs/app-development/dependency-injection)。

## Using Microsoft.Maui.Essentials

对于常见的设备 API（传感器、网络连接、电量、权限），`Microsoft.Maui.Essentials` 提供了跨平台抽象，可在 .NET 8+ 上与 Avalonia 配合使用：

```xml
<PackageReference Include="Microsoft.Maui.Essentials" Version="8.0.0" />
```

```csharp
using Microsoft.Maui.Devices;

var model = DeviceInfo.Model;
var platform = DeviceInfo.Platform;
```

注意 Maui.Essentials 支持 Windows、macOS（通过 Catalyst）、Android 和 iOS，不支持 Linux、WebAssembly，也不支持非 Catalyst 的 macOS 构建。

## 用 SkiaSharp 自定义渲染 {#custom-rendering-with-skiasharp}

要在 Avalonia 控件内直接做 GPU 渲染，可以把 `ICustomDrawOperation` 与 SkiaSharp 搭配使用：

```csharp
using Avalonia.Media;
using Avalonia.Platform;
using Avalonia.Rendering.SceneGraph;
using Avalonia.Skia;
using SkiaSharp;

public class SkiaCanvas : Control
{
    public override void Render(DrawingContext context)
    {
        var bounds = new Rect(0, 0, Bounds.Width, Bounds.Height);
        context.Custom(new SkiaDrawOperation(bounds));
    }

    private class SkiaDrawOperation : ICustomDrawOperation
    {
        public SkiaDrawOperation(Rect bounds) => Bounds = bounds;

        public Rect Bounds { get; }

        public void Render(ImmediateDrawingContext context)
        {
            var leaseFeature = context.TryGetFeature<ISkiaSharpApiLeaseFeature>();
            if (leaseFeature is null) return;

            using var lease = leaseFeature.Lease();
            var canvas = lease.SkCanvas;

            // Direct SkiaSharp drawing
            using var paint = new SKPaint
            {
                Color = SKColors.CornflowerBlue,
                IsAntialias = true,
                Style = SKPaintStyle.Fill
            };

            canvas.DrawCircle(
                (float)Bounds.Width / 2,
                (float)Bounds.Height / 2,
                50,
                paint);
        }

        public bool HitTest(Point p) => Bounds.Contains(p);
        public bool Equals(ICustomDrawOperation? other) => false;
        public void Dispose() { }
    }
}
```

添加 SkiaSharp 的 NuGet 包：

```xml
<PackageReference Include="SkiaSharp" Version="2.88.*" />
```

## 另请参阅 {#see-also}

- [跨平台架构](/docs/fundamentals/cross-platform-architecture)：解决方案结构与平台分支模式。
- [平台专属 .NET](/docs/platform-specific-guides/dotnet)：运行时检测与条件编译。
- [依赖注入](/docs/app-development/dependency-injection)：注册平台服务。
- [Native AOT 发布](/docs/deployment/native-aot)：原生互操作在 AOT 下的注意事项。
