---
id: custom-rendering
title: 自定义渲染
description: 重写 Render 方法，用 DrawingContext 绘制自定义图形。
doc-type: how-to
---

Avalonia 提供了 `DrawingContext` API，用于在控件内渲染自定义图形。当内置的形状和几何控件不够灵活、满足不了需求时，它就派上用场了。

## 重写 render {#overriding-render}

要绘制自定义内容，在任意 `Control` 上重写 `Render` 方法：

```csharp
public class SimpleCircle : Control
{
    public override void Render(DrawingContext context)
    {
        var center = new Point(Bounds.Width / 2, Bounds.Height / 2);
        var radius = Math.Min(Bounds.Width, Bounds.Height) / 2 - 4;

        context.DrawEllipse(
            Brushes.CornflowerBlue,         // fill brush
            new Pen(Brushes.Navy, 2),       // stroke pen
            center,
            radius,                          // radiusX
            radius);                         // radiusY
    }
}
```

在 XAML 中使用这个控件：

```xml
<local:SimpleCircle Width="100" Height="100" />
```

控件每次需要重绘时都会调用 `Render` 方法。数据变化时，请调用 `InvalidateVisual()` 来请求重绘。

## DrawingContext 的各项操作 {#drawingcontext-operations}

`DrawingContext` 提供下列绘制操作：

| 方法 | 说明 |
|---|---|
| `DrawRectangle(brush, pen, rect, radiusX, radiusY)` | 绘制矩形，可带圆角 |
| `DrawEllipse(brush, pen, center, radiusX, radiusY)` | 绘制椭圆 |
| `DrawLine(pen, p1, p2)` | 在两点之间绘制直线 |
| `DrawGeometry(brush, pen, geometry)` | 绘制任意几何图形 |
| `DrawText(formattedText, origin)` | 在指定点绘制带格式的文本 |
| `DrawImage(bitmap, sourceRect, destRect)` | 绘制位图图像 |
| `DrawGlyphRun(brush, glyphRun)` | 绘制已整形的文本字形 |

### 带状态地绘制 {#drawing-with-state}

用 `PushClip`、`PushOpacity`、`PushTransform` 等方法修改绘制状态。它们都返回一个 `IDisposable`，释放时会还原先前的状态：

```csharp
public override void Render(DrawingContext context)
{
    // Clip to a rounded rectangle
    using (context.PushClip(new RoundedRect(new Rect(Bounds.Size), 8)))
    {
        // Fill background
        context.DrawRectangle(Brushes.White, null, new Rect(Bounds.Size));

        // Apply opacity to a group of draws
        using (context.PushOpacity(0.5))
        {
            context.DrawEllipse(Brushes.Red, null,
                new Point(30, 30), 20, 20);
        }

        // Apply a transform
        using (context.PushTransform(Matrix.CreateRotation(0.2)))
        {
            context.DrawRectangle(Brushes.Blue, null,
                new Rect(10, 10, 50, 50));
        }
    }
}
```

### 绘制文本 {#drawing-text}

用 [`FormattedText`](/api/avalonia/media/formattedtext) 来测量并渲染单段文本：

```csharp
public override void Render(DrawingContext context)
{
    var text = new FormattedText(
        "Hello, Avalonia!",
        CultureInfo.CurrentCulture,
        FlowDirection.LeftToRight,
        new Typeface("Segoe UI"),
        16,
        Brushes.Black);

    context.DrawText(text, new Point(10, 10));
}
```

`FormattedText` 适合简单的单行或短文本。要处理多行文本、自动换行、两端对齐或逐行度量，请改用 `TextLayout`。`TextLayout` 支持不少 `FormattedText` 没有的特性，`TextAlignment.Justify` 便是其中之一：

```csharp
var layout = new TextLayout(
    "Multi-line text with wrapping and justification support.",
    new Typeface("Segoe UI"),
    16,
    Brushes.Black,
    textAlignment: TextAlignment.Justify,
    maxWidth: 200);

// Access line metrics
foreach (var line in layout.TextLines)
{
    // line.Height, line.Width, line.Start, and other metrics
}

layout.Draw(context, new Point(10, 10));
```

### 绘制图片 {#drawing-images}

加载并绘制位图图像：

```csharp
private IImage? _image;

protected override void OnLoaded(RoutedEventArgs e)
{
    base.OnLoaded(e);
    var uri = new Uri("avares://MyApp/Assets/photo.png");
    _image = new Bitmap(AssetLoader.Open(uri));
    InvalidateVisual();
}

public override void Render(DrawingContext context)
{
    if (_image is null) return;

    var destRect = new Rect(0, 0, Bounds.Width, Bounds.Height);
    var sourceRect = new Rect(0, 0, _image.Size.Width, _image.Size.Height);

    context.DrawImage(_image, sourceRect, destRect);
}
```

## 让视觉失效 {#invalidating-the-visual}

框架会缓存 `Render` 的结果。当控件的数据发生变化时，你必须显式请求重绘：

```csharp
public static readonly StyledProperty<double> ProgressProperty =
    AvaloniaProperty.Register<ProgressRing, double>(nameof(Progress));

public double Progress
{
    get => GetValue(ProgressProperty);
    set => SetValue(ProgressProperty, value);
}

static ProgressRing()
{
    // Automatically invalidate visual when Progress changes
    AffectsRender<ProgressRing>(ProgressProperty);
}
```

`AffectsRender` 会注册一个回调，使得 `Progress` 的任何变化都自动触发 `InvalidateVisual()`。需要时你也可以手动调用 `InvalidateVisual()`。

## RenderTargetBitmap

要把控件的渲染结果捕获成位图（比如存成文件或作图像处理）：

```csharp
var pixelSize = new PixelSize(
    (int)myControl.Bounds.Width,
    (int)myControl.Bounds.Height);

var renderTarget = new RenderTargetBitmap(pixelSize, new Vector(96, 96));
renderTarget.Render(myControl);

// Save to file
renderTarget.Save("output.png");
```

:::note
`RenderTargetBitmap` 走的是软件渲染。那些依赖 GPU 专属渲染路径的控件（比如 `OpenGlControlBase` 或自定义 GPU 互操作）这样捕获出来可能不对。
:::

:::tip[离屏渲染]
`RenderTargetBitmap.Render` 要求目标控件已附加到一个可见窗口上。若你需要在不显示窗口的前提下渲染控件（比如服务端生成图片或批量导出），请使用启用了 Skia 渲染器的[无头平台](/docs/testing/setting-up-the-headless-platform)。无头平台能在内存中提供完整的布局和渲染管线，无需打开可见窗口。
:::

## 用 ICustomDrawOperation 对接 SkiaSharp {#icustomdrawoperation-for-skiasharp}

若要直接操作 SkiaSharp 画布（比如绘制复杂图表、做 3D 渲染或游戏画面），请实现 `ICustomDrawOperation`：

```csharp
using Avalonia.Rendering.SceneGraph;
using Avalonia.Skia;
using SkiaSharp;

public class ChartControl : Control
{
    public override void Render(DrawingContext context)
    {
        context.Custom(new ChartDrawOperation(new Rect(Bounds.Size)));
    }

    private class ChartDrawOperation : ICustomDrawOperation
    {
        public ChartDrawOperation(Rect bounds) => Bounds = bounds;

        public Rect Bounds { get; }

        public void Render(ImmediateDrawingContext context)
        {
            var feature = context.TryGetFeature<ISkiaSharpApiLeaseFeature>();
            if (feature is null) return;

            using var lease = feature.Lease();
            var canvas = lease.SkCanvas;

            // Use full SkiaSharp API
            using var paint = new SKPaint
            {
                IsAntialias = true,
                Style = SKPaintStyle.Stroke,
                StrokeWidth = 2,
                Color = SKColors.DodgerBlue
            };

            var path = new SKPath();
            path.MoveTo(0, (float)Bounds.Height);
            path.LineTo((float)Bounds.Width * 0.25f, (float)Bounds.Height * 0.6f);
            path.LineTo((float)Bounds.Width * 0.5f, (float)Bounds.Height * 0.8f);
            path.LineTo((float)Bounds.Width * 0.75f, (float)Bounds.Height * 0.2f);
            path.LineTo((float)Bounds.Width, (float)Bounds.Height * 0.4f);

            canvas.DrawPath(path, paint);
        }

        public bool HitTest(Point p) => Bounds.Contains(p);
        public bool Equals(ICustomDrawOperation? other) => false;
        public void Dispose() { }
    }
}
```

添加所需的 NuGet 包：

```xml
<PackageReference Include="Avalonia.Skia" Version="11.2.*" />
<PackageReference Include="SkiaSharp" Version="2.88.*" />
```

## 借组合表面实现 GPU 互操作 {#gpu-interop-with-composition-surfaces}

面对视频播放、3D 引擎集成、跨进程 GPU 纹理共享等进阶场景，Avalonia 的组合 API 支持把外部 GPU 资源导入 `CompositionDrawingSurface`。

### 导入 GPU 图像 {#importing-gpu-images}

用 compositor 导入外部 GPU 纹理（比如 Vulkan 图像，或 macOS 上的 IOSurface），并把它显示在组合表面中：

```csharp
var compositor = ElementComposition.GetElementVisual(this)!.Compositor;

// Import an external GPU image handle
var image = compositor.ImportGpuImage(
    PlatformGraphicsExternalImageProperties.CreateForVulkan(
        pixelSize, format),
    new PlatformHandle(handle, handleType));

// Import semaphores for GPU synchronization
var waitSemaphore = compositor.ImportGpuSemaphore(
    new PlatformHandle(semaphoreHandle, semaphoreType));
var signalSemaphore = compositor.ImportGpuSemaphore(
    new PlatformHandle(semaphoreHandle2, semaphoreType));

// Update the surface with the imported image
await surface.UpdateWithKeyedMutexAsync(image);
// or with timeline semaphores (macOS Metal):
await surface.UpdateWithTimelineSemaphoresAsync(
    image,
    waitSemaphore, waitValue,
    signalSemaphore, signalValue);
```

### 受支持的句柄类型 {#supported-handle-types}

GPU 图像和信号量的句柄类型因平台而异。用 `KnownPlatformGraphicsExternalImageHandleTypes` 和 `KnownPlatformGraphicsExternalSemaphoreHandleTypes` 可以查出有哪些可用类型：

| 平台 | 图像句柄类型 | 信号量句柄类型 |
|---|---|---|
| Windows | `D3D11TextureNtHandle`, `VulkanOpaqueNtHandle` | `D3D11Fence`, `VulkanOpaqueNtHandle` |
| macOS | `IOSurfaceRef` | `MetalSharedEvent` |
| Linux | `DmaBuf`, `VulkanOpaqueFd` | `VulkanOpaqueFd` |

在导入的图像上检查 `CompositionGpuImportedImageSynchronizationCapabilities`，即可知道有哪些同步方式可用（`KeyedMutex`、`Semaphores`、`TimelineSemaphores`）。

## CompositionCustomVisualHandler

[`CompositionCustomVisualHandler`](/api/avalonia/rendering/composition/compositioncustomvisualhandler) 提供逐帧回调，这些回调直接运行在渲染线程上，不会阻塞 UI 线程。要做顺滑连续的动画或实时可视化、又顾虑 UI 线程开销时，它很有用。

若场景比较简单、能接受回调跑在 UI 线程上，请改用 [`TopLevel.RequestAnimationFrame`](/docs/fundamentals/top-level#requestanimationframe)。

### 搭建自定义视觉处理器 {#setting-up-a-custom-visual-handler}

创建一个 `CompositionCustomVisualHandler`，并把它注册到某个控件的组合视觉元素上：

```csharp
public class RenderThreadAnimationControl : Control
{
    private CompositionCustomVisualHandler? _handler;

    protected override void OnAttachedToVisualTree(VisualTreeAttachmentEventArgs e)
    {
        base.OnAttachedToVisualTree(e);

        var visual = ElementComposition.GetElementVisual(this);
        if (visual == null) return;

        var compositor = visual.Compositor;

        _handler = new CompositionCustomVisualHandler(
            OnRender, OnMessage);

        compositor.CreateCustomVisual(_handler);
    }

    private void OnRender(
        CompositionCustomVisualHandler sender,
        SkiaSharp.SKCanvas canvas,
        RenderBounds bounds)
    {
        // This runs on the render thread.
        // Draw directly with the SkiaSharp canvas.
        using var paint = new SkiaSharp.SKPaint
        {
            IsAntialias = true,
            Color = SkiaSharp.SKColors.CornflowerBlue
        };
        canvas.DrawCircle(
            (float)bounds.Width / 2,
            (float)bounds.Height / 2,
            50f, paint);

        // Request another frame for continuous rendering
        sender.RequestNextFrameRendering();
    }

    private void OnMessage(
        CompositionCustomVisualHandler sender,
        object message)
    {
        // Handle messages sent from the UI thread
        // via sender.SendHandlerMessage(data)
    }
}
```

### 跨线程通信 {#communicating-between-threads}

由于 `OnRender` 跑在渲染线程上，你没法直接访问 UI 线程的状态。请用 `SendHandlerMessage` 把数据从 UI 线程传给渲染回调：

```csharp
// On the UI thread: send updated data to the render thread
_handler?.SendHandlerMessage(new AnimationData(progress: 0.5));
```

消息会送达 `OnMessage` 回调，你可以把它存下来供下一轮渲染使用。这套做法让渲染线程专心作画，UI 线程则始终保持跟手。

### 何时该用 CompositionCustomVisualHandler {#when-to-use-compositioncustomvisualhandler}

| 办法 | 线程 | 适用场景 |
|---|---|---|
| `TopLevel.RequestAnimationFrame` | UI 线程 | 简单的逐帧更新、属性动画循环 |
| `CompositionCustomVisualHandler` | 渲染线程 | 实时可视化、游戏主循环、视频渲染 |
| `Render()` override | UI 线程 | 常规的自定义控件绘制 |

## 性能考量 {#performance-considerations}

- `Render` 是在 UI 线程上调用的。请让绘制操作尽量快，并尽可能避免内存分配。
- 参数不变时，请复用 `Pen`、`Brush` 和 `FormattedText` 对象：把它们存成字段，只有输入变了才重建。
- 对那些频繁渲染的控件（比如图表、仪表），用 `AffectsRender` 来避免无谓的重绘。
- 场景复杂时，不妨把控件拆成若干小控件，这样只有真正变化的那部分才需要重绘。
- `ICustomDrawOperation` 会绕过 Avalonia 的场景图缓存。只有当你确实需要 SkiaSharp 级别的掌控力时才用它。

## 另请参阅 {#see-also}

- [TopLevel.RequestAnimationFrame](/docs/fundamentals/top-level#requestanimationframe)：UI 线程上的逐帧回调。
- [组合动画](/docs/graphics-animation/composition-animations)：用组合 API 实现的渲染线程属性动画。
- [形状与几何](/docs/graphics-animation/shapes-and-geometries)：内置形状控件与几何类型。
- [自绘控件](/docs/custom-controls/custom-drawn-controls)：编写自己画自己的控件。
- [画刷](/docs/graphics-animation/brushes)：可用于填充和描边的各类画刷。
- [效果](/docs/graphics-animation/effects)：阴影、模糊等视觉效果。
