---
id: top-level
title: 顶层（TopLevel）
description: 通过 TopLevel 基类访问窗口、剪贴板、存储等各项服务。
doc-type: reference
video:
  src: https://youtu.be/sgLcNJiYRj8
  title: Avalonia TopLevel 与 MainWindow 的区别 —— GetTopLevel、Clipboard 与 FocusManager
---

[`TopLevel`](/api/avalonia/controls/toplevel) 充当视觉根，是所有顶层控件（例如 [`Window`](/api/avalonia/controls/window)）的基类。它负责调度布局、样式和渲染，并跟踪客户区尺寸。大多数服务都通过 `TopLevel` 来访问。

## 获取 TopLevel {#getting-the-toplevel}

下面是取得 `TopLevel` 实例的两种常见方式。

### Using TopLevel.GetTopLevel

可以用 `TopLevel` 类的静态方法 `GetTopLevel` 取得包含当前控件的那个顶层控件。

```csharp
var topLevel = TopLevel.GetTopLevel(control);
// Here you can reference various services like Clipboard or StorageProvider from topLevel instance.
```

当你在用户控件或更底层的组件中工作，又需要访问 TopLevel 的各项服务时，这个办法很好使。

:::note
如果 `TopLevel.GetTopLevel` 返回 null，多半是因为控件还没挂到根上。为确保控件已附加，应当处理 `Control.Loaded` 和 `Control.Unloaded` 事件，并在这两个事件中跟踪当前的顶层。
:::

### 使用 Window 类 {#using-the-window-class}

由于 `Window` 类继承自 `TopLevel`，你可以直接从 `Window` 实例上访问这些服务：

```csharp
var topLevel = window;
```

当你本来就处在某个窗口的上下文中时（比如在 ViewModel 里，或在 `Window` 类的事件处理程序中），一般就用这个办法。

## 常用属性 {#common-properties}

### ActualTransparencyLevel

获取平台最终能够提供的 `WindowTransparencyLevel`。

```csharp
WindowTransparencyLevel ActualTransparencyLevel { get; }
```

### ClientSize

获取窗口的客户区尺寸。

```csharp
Size ClientSize { get; }
```

### Clipboard

获取平台的 [Clipboard](/docs/services/clipboard) 实现。

```csharp
IClipboard? Clipboard { get; }
```

### FocusManager

获取根的[焦点管理器](/docs/services/focus-manager)。

```csharp
IFocusManager? FocusManager { get; }
```

### FrameSize

获取顶层的总尺寸，若存在系统边框则一并计入。

```csharp
Size? FrameSize { get; }
```

### InsetsManager

获取平台的 [InsetsManager](/docs/services/insets-manager) 实现。

```csharp
IInsetsManager? InsetsManager { get; }
```

### PlatformSettings

表示访问顶层[平台专有设置](/docs/services/platform-settings)的约定。

```csharp
IPlatformSettings? PlatformSettings { get; }
```

### RendererDiagnostics

获取一个值，指示渲染器是否应绘制特定的诊断信息。

```csharp
RendererDiagnostics RendererDiagnostics { get; }
```

### RenderScaling

获取渲染时所用的缩放系数。

```csharp
double RenderScaling { get; }
```

### Screens

获取 [`Screens`](/api/avalonia/controls/screens) 实例，可从中了解已连接显示器的信息，包括分辨率、工作区、缩放和方向。

```csharp
Screens Screens { get; }
```

用 `Screens` 可以查询主显示器、枚举全部显示器，或找出包含某个窗口或某个点的屏幕。用法示例见[使用屏幕](/docs/app-development/window-management#working-with-screens)。

### RequestedThemeVariant

获取或设置该控件（及其子元素）在解析资源时所用的界面主题变体。你用 `ThemeVariant` 指定的界面主题会覆盖应用级的 `ThemeVariant`。

```csharp
ThemeVariant? RequestedThemeVariant { get; set; }
```

### StorageProvider

供文件选择器和书签使用的[文件系统存储](/docs/services/storage/storage-provider)服务。

```csharp
IStorageProvider StorageProvider { get; }
```

### TransparencyBackgroundFallback

获取或设置当平台不支持或限制透明时，透明度所混合的 `IBrush`。默认是纯白色画刷。

```csharp
IBrush TransparencyBackgroundFallback { get; set; }
```

### TransparencyLevelHint

获取或设置 TopLevel 在条件允许时应采用的 `WindowTransparencyLevel`。可以给多个值，按回退顺序依次应用。例如填 "Mica, Blur"，则只在支持 Mica 的平台上应用 Mica，其余平台一律用 Blur。默认值是空数组，即 "None"。

```csharp
IReadOnlyList<WindowTransparencyLevel> TransparencyLevelHint { get; set; }
```

## 常用事件 {#common-events}

### BackRequested

按下实体返回键、或收到返回导航请求时发生。

```csharp
event EventHandler<RoutedEventArgs> BackRequested { add; remove; }
```

### Closed

窗口关闭时触发。

```csharp
event EventHandler Closed;
```

### Opened

窗口打开时触发。

```csharp
event EventHandler Opened;
```

### ScalingChanged

TopLevel 的缩放发生变化时触发。

```csharp
event EventHandler ScalingChanged;
```

## 常用方法 {#common-methods}

### GetTopLevel

获取承载给定 `Visual` 的那个 `TopLevel`。

`visual` 参数指定要查询的视觉元素。

```csharp
static TopLevel? GetTopLevel(Visual? visual)
```

### RequestAnimationFrame

把一个回调排入队列，在下一个动画时间片上调用。该回调运行在 UI 线程上，与 Avalonia 的渲染周期同步。每次调用只安排一次执行；若要形成连续的动画循环，请在回调内部再次调用 `RequestAnimationFrame`。

`action` 参数会收到一个 `TimeSpan`，表示自动画系统启动以来经过的时间。用它来计算与帧率无关的动画进度。

```csharp
void RequestAnimationFrame(Action<TimeSpan> action)
```

#### 示例：连续的动画循环 {#example-continuous-animation-loop}

```csharp
var topLevel = TopLevel.GetTopLevel(this);

topLevel.RequestAnimationFrame(OnAnimationFrame);

private void OnAnimationFrame(TimeSpan elapsed)
{
    // Update your visual state based on elapsed time
    _angle = elapsed.TotalSeconds * 90; // 90 degrees per second
    InvalidateVisual();

    // Schedule the next frame to keep the loop running
    TopLevel.GetTopLevel(this)?.RequestAnimationFrame(OnAnimationFrame);
}
```

这相当于 WPF 中的 `CompositionTarget.Rendering`。若需要不阻塞 UI 线程的渲染线程回调，请见 [CompositionCustomVisualHandler](/docs/graphics-animation/custom-rendering#compositioncustomvisualhandler)。

### RequestPlatformInhibition

请求抑制某项 `PlatformInhibitionType`。在返回值被释放之前，该行为将一直处于被抑制状态。可用的 `PlatformInhibitionType` 取决于平台；若在不支持该类型的平台上发起抑制请求，则请求不会产生任何效果。

```csharp
async Task<IDisposable> RequestPlatformInhibition(PlatformInhibitionType type, string reason)
```

### TryGetPlatformHandle

尝试获取该 TopLevel 派生控件的平台句柄。

```csharp
IPlatformHandle? TryGetPlatformHandle()
```

## 另请参阅 {#see-also}

- [主窗口](/docs/fundamentals/main-window)
- [应用程序生命周期](/docs/fundamentals/application-lifetimes)
- [使用屏幕](/docs/app-development/window-management#working-with-screens)：查询显示器的分辨率、边界与缩放。
- [自定义渲染](/docs/graphics-animation/custom-rendering)：自定义绘制与渲染线程回调。
- [合成动画](/docs/graphics-animation/composition-animations)：在渲染线程上执行的属性动画。
- [GitHub 上的 `TopLevel.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/TopLevel.cs)
