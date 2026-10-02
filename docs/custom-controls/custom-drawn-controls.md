---
id: custom-drawn-controls
title: 自绘控件
description: 创建一个外观完全由代码指定的自定义控件类。
doc-type: how-to
---

如果你想完全掌控自定义控件的外观，就新建一个继承自 `Control` 的控件类，重写 `Render` 方法，用 [`DrawingContext`](/api/avalonia/media/drawingcontext) 直接绘制。你甚至可以重写 `MeasureOverride` 和 `ArrangeOverride`，让这个控件参与布局过程。

## 编写一个自绘控件 {#creating-a-custom-drawn-control}

下面的例子做了一个简单的圆形控件，带一个可配置的 `Fill` 属性。

```csharp
using System;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;

namespace AvaloniaCCExample.CustomControls
{
    public class CircleControl : Control
    {
        public static readonly StyledProperty<IBrush> FillProperty =
            AvaloniaProperty.Register<CircleControl, IBrush>(nameof(Fill), Brushes.Blue);

        public IBrush Fill
        {
            get => GetValue(FillProperty);
            set => SetValue(FillProperty, value);
        }

        static CircleControl()
        {
            AffectsRender<CircleControl>(FillProperty);
        }

        public override void Render(DrawingContext context)
        {
            var radius = Math.Min(Bounds.Width, Bounds.Height) / 2;
            var center = new Point(Bounds.Width / 2, Bounds.Height / 2);
            context.DrawEllipse(Fill, null, center, radius, radius);
        }
    }
}
```

几点说明：

- `FillProperty` 是样式化属性，因此可以在 XAML 中设置、绑定到数据，也能被样式选中。
- 静态构造函数里调用了 `AffectsRender`，它告诉 Avalonia：只要 `Fill` 变了就重绘该控件。
- `Render` 会收到一个 [`DrawingContext`](#drawingcontext-methods)，它提供了 `DrawEllipse`、`DrawRectangle`、`DrawLine`、`DrawText` 等方法。

## 在 XAML 中使用 {#using-in-xaml}

要在 XAML 中使用自定义控件，先添加一个映射到该控件所在 CLR 命名空间的 XML 命名空间，然后按类名引用这个控件。

```xml title='XAML'
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        // highlight-next-line
        xmlns:cc="using:AvaloniaCCExample.CustomControls"
        x:Class="AvaloniaCCExample.MainWindow"
        Title="Avalonia Custom Control">
  // highlight-next-line
  <cc:CircleControl Height="200" Width="200" Fill="Red" />
</Window>
```

`cc` 这个前缀是随便取的，它的作用只是映射 `AvaloniaCCExample.CustomControls`，好让 XAML 解析器能解析出 `CircleControl`。

:::info
若你的控件放在独立的类库中，还需要一些额外配置，参见[自定义控件库](/docs/custom-controls/custom-control-library)。
:::

## 让渲染失效 {#invalidating-rendering}

Avalonia 提供两种机制来告诉布局和渲染系统某个控件需要更新：[`Affects` 系列辅助方法](#affectsrender-affectsmeasure-and-affectsarrange)和[手动失效](#manual-invalidation)。

### `AffectsRender`, `AffectsMeasure`, and `AffectsArrange`

`AffectsRender`、`AffectsMeasure` 和 `AffectsArrange` 都是静态辅助方法。在控件的静态构造函数中调用它们，即可声明哪个属性会触发渲染管线的哪个阶段。

```csharp
static CircleControl()
{
    AffectsRender<CircleControl>(FillProperty);
    AffectsMeasure<CircleControl>(SomeOtherProperty);
    AffectsArrange<CircleControl>(YetAnotherProperty);
}
```

- `AffectsRender` 让属性变化时触发重绘（也就是再调一次 `Render`）。
- `AffectsMeasure` 触发一轮新的测量，适用于那些会改变控件期望尺寸的属性。
- `AffectsArrange` 触发一轮新的排列，适用于那些会改变控件如何摆放其内容的属性。

### 手动失效 {#manual-invalidation}

若要因属性变化之外的原因（比如计时器滴答）触发控件的视觉更新，可以在控件实例上手动调用失效方法。

```csharp
// Forces a repaint
InvalidateVisual();

// Forces a measure pass
InvalidateMeasure();

// Forces an arrange pass
InvalidateArrange();
```

:::tip
手动失效能少用就少用。更推荐用 `AffectsRender` 声明属性依赖，这样失效既自动又可预期。
:::

## `DrawingContext` 的方法 {#drawingcontext-methods}

[`DrawingContext`](/api/avalonia/media/drawingcontext) 为自绘控件提供了下列方法：

| 方法 | 说明 |
|---|---|
| `DrawRectangle` | 绘制矩形。 |
| `DrawEllipse` | 绘制椭圆。 |
| `DrawLine` | 在两点之间绘制直线。 |
| `DrawGeometry` | 绘制任意几何路径。 |
| `DrawText` | 绘制带格式的文本。 |
| `DrawImage` | 绘制位图图像。 |
| `FillRectangle` | 填充矩形（简便写法）。 |

### 绘制形状 {#drawing-shapes}

你可以在一次 `Render` 重写中绘制多个形状：

```csharp
public override void Render(DrawingContext context)
{
    var pen = new Pen(Brushes.Black, 2);

    // Draw a filled rectangle
    context.DrawRectangle(Brushes.LightBlue, pen, new Rect(10, 10, 100, 60));

    // Draw an ellipse
    context.DrawEllipse(Brushes.Orange, pen, new Point(200, 40), 50, 30);

    // Draw a line
    context.DrawLine(new Pen(Brushes.Red, 3), new Point(10, 100), new Point(290, 100));
}
```

### 绘制文本 {#drawing-text}

用 `DrawText` 配合一个 `FormattedText` 对象即可绘制带格式的文本：

```csharp
public override void Render(DrawingContext context)
{
    var text = new FormattedText(
        "Hello, Avalonia!",
        CultureInfo.CurrentCulture,
        FlowDirection.LeftToRight,
        new Typeface("Arial"),
        24,
        Brushes.Black);

    context.DrawText(text, new Point(10, 10));
}
```

### 裁剪与变换 {#clipping-and-transforming}

用 `PushClip` 和 `PushTransform` 来裁剪区域或施加变换。两者都返回可释放对象，请用 `using` 语句包住，以确保状态自动还原：

```csharp
public override void Render(DrawingContext context)
{
    // Save and restore state with PushClip
    using (context.PushClip(new Rect(0, 0, 100, 100)))
    {
        context.FillRectangle(Brushes.Blue, new Rect(0, 0, 200, 200));
        // Only the portion within 100x100 is visible
    }

    // Apply a transform
    using (context.PushTransform(Matrix.CreateRotation(Math.PI / 4)))
    {
        context.FillRectangle(Brushes.Green, new Rect(150, 50, 40, 40));
    }
}
```

## 另请参阅 {#see-also}

- [定义属性](/docs/custom-controls/defining-properties)：为自定义控件添加样式化属性、直接属性和附加属性。
- [自定义模板化控件](/docs/custom-controls/templated-controls)：另一条路子——外观由控件主题定义。
- [创建自定义控件](/docs/custom-controls)：各类自定义控件概览。
- [自定义控件示例项目](https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/CustomControls/SnowflakesControlSample)：演示自绘控件的实战示例。
- [画刷](/docs/graphics-animation/brushes)：可用的画刷类型。
- [形状与几何](/docs/graphics-animation/shapes-and-geometries)：用于绘制的几何类型。