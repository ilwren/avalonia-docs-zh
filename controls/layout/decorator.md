---
id: decorator
title: Decorator
description: 一个基类，供那些包裹并装饰单个子元素的控件使用；它提供内边距，也是自定义包装控件的基础。
doc-type: reference
---

[`Decorator`](/api/avalonia/controls/decorator) 控件是一个基类，供那些包裹并装饰单个子元素的控件使用。它负责把一个子元素同时纳入逻辑树和视觉树，并在其四周应用可选的内边距。

## 何时使用 [`Decorator`](/api/avalonia/controls/decorator) {#when-to-use-decorator}

一般不会在 XAML 里直接用 `Decorator`，而是用由它派生的内置控件，比如 `Border` 或 `Viewbox`。不过有两种场景下 `Decorator` 很有用：

- **派生子类**：当你需要一个自定义包装控件，在单个子元素周围加上布局、渲染或行为逻辑时，就从 `Decorator` 派生一个子类。
- **纯内边距包装**：当你只想给子元素加点内边距，不要边框、背景之类的视觉装饰时，直接用 `Decorator`。

## 内置的 decorator {#built-in-decorators}

下列控件继承自 `Decorator`：

| 控件 | 用途 |
| :--- | :--- |
| [Border](/controls/layout/containers/border) | 在子元素四周绘制边框、背景、圆角和阴影 |
| [Viewbox](/controls/layout/containers/viewbox) | 缩放子元素以适配可用空间 |
| [LayoutTransformControl](/controls/layout/layouttransformcontrol) | 应用一个参与布局的渲染变换 |

## 属性 {#properties}

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `Child` | `Control` | 要装饰的那个子控件。它标注为 `[Content]`，因此在 XAML 中可以直接设置，不必写出属性元素。 |
| `Padding` | `Thickness` | decorator 边缘与其子元素之间的空隙。 |

## `Decorator` 的运作原理 {#how-decorator-works}

设置 `Child` 属性时，`Decorator` 会自动把子元素加入自己的逻辑树和视觉树。布局期间，它在扣除 `Padding` 之后剩下的区域里测量并排列子元素。也就是说，你的子类不必操心单子元素的基础布局，只需专注于想额外加的渲染或测量逻辑。

由于 `Decorator` 只接受一个子元素，它比 `StackPanel`、`Grid` 这类基于面板的容器更轻量。当你的控件在概念上只是包裹或增强单块内容、而非编排多个子元素时，就该用它。

## 示例 {#examples}

### 创建自定义 decorator {#creating-a-custom-decorator}

下面的例子做了一个自定义 decorator，在子元素背后绘制一块彩色背景。先为画刷颜色声明一个样式化属性，再重写 `Render`，在子元素自绘之前把背景画出来。

```csharp
public class HighlightDecorator : Decorator
{
    public static readonly StyledProperty<IBrush?> HighlightBrushProperty =
        AvaloniaProperty.Register<HighlightDecorator, IBrush?>(
            nameof(HighlightBrush), Brushes.Yellow);

    public IBrush? HighlightBrush
    {
        get => GetValue(HighlightBrushProperty);
        set => SetValue(HighlightBrushProperty, value);
    }

    public override void Render(DrawingContext context)
    {
        if (HighlightBrush is not null)
        {
            context.FillRectangle(HighlightBrush, new Rect(Bounds.Size));
        }
    }
}
```

之后就能在 XAML 中使用这个自定义 decorator：

```xml
<local:HighlightDecorator HighlightBrush="LightBlue" Padding="8">
  <TextBlock Text="Highlighted content" />
</local:HighlightDecorator>
```

### 直接使用 `Decorator` {#using-decorator-directly}

虽然不常见，但你完全可以把 `Decorator` 当作一个简单的内边距包装来用：

```xml
<Decorator Padding="16">
  <TextBlock Text="Padded content" />
</Decorator>
```

它的表现就像一个没有边框和背景的 `Border`，只给子元素加上内边距。

## 另请参阅 {#see-also}

- [Border](/controls/layout/containers/border)
- [Viewbox](/controls/layout/containers/viewbox)
- [LayoutTransformControl](/controls/layout/layouttransformcontrol)
- [`Decorator` API 参考](/api/avalonia/controls/decorator)
- [GitHub 上的 `Decorator.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Decorator.cs)
