---
id: custom-panel
title: Custom Panel
description: 通过重写 MeasureOverride 和 ArrangeOverride 实现自定义布局面板。
doc-type: how-to
---

如果你需要的布局比[内置面板](/controls)所能提供的更复杂或更特别，可以自己写一个面板。自定义面板让你精确掌控子元素如何被测量和排列，做法是继承 `Panel` 并重写它的布局方法。

## 布局过程 {#layout-process}

Avalonia 采用两轮制的布局系统：

1. **测量（`MeasureOverride`）：**面板拿到一个可用尺寸，据此算出自己需要多大空间。这一轮里你必须对每个子元素调用 `child.Measure()`，之后每个子元素都会设好自己的 `DesiredSize` 属性，你可以用它来计算面板自身的期望尺寸。

2. **排列（`ArrangeOverride`）：**面板拿到最终分配给它的尺寸，并在这片空间里给每个子元素定位。你必须对每个子元素调用 `child.Arrange()`，并传入一个 `Rect` 来指定该子元素的位置和大小。

任何面板都必须参与这两轮。

关于 Avalonia 布局系统的更多内容，请参阅[布局系统](/docs/layout/#the-layout-system)。

## 做一个带固定偏移的自定义 `PlotPanel` {#creating-a-custom-plotpanel-with-a-fixed-offset}

这个简单的例子重点演示自定义面板时该怎么重写 `MeasureOverride` 和 `ArrangeOverride`。这个自定义 `PlotPanel` 把子元素摆在写死的 (50, 50) 偏移处。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:local="using:MyApp">
        
        <local:PlotPanel Background="Gray" Margin="10">
                <TextBlock Background="Blue" Text="Hello world!" />
        </local:PlotPanel>
        
</UserControl>
```

```csharp
using Avalonia;
using Avalonia.Controls;

namespace MyApp;

public class PlotPanel : Panel
{
    // Override the default Measure method of Panel
    protected override Size MeasureOverride(Size availableSize)
    {
        var panelDesiredSize = new Size();

        // In our example, we just have one child.
        // Report that our panel requires just the size of its only child.
        foreach (var child in Children)
        {
            child.Measure(availableSize);
            panelDesiredSize = child.DesiredSize;
        }

        return panelDesiredSize;
    }

    protected override Size ArrangeOverride(Size finalSize)
    {
        foreach (var child in Children)
        {
            double x = 50;
            double y = 50;

            child.Arrange(new Rect(new Point(x, y), child.DesiredSize));
        }

        return finalSize; // Returns the final Arranged size
    }
}
```

</XamlPreview>

## 做一个自定义 `RadialPanel` {#creating-a-custom-radialpanel}

这是一个更进阶的例子：自定义的径向面板，把子元素沿圆周均匀排布，相邻两个子元素的角度间隔相同。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:local="using:MyApp">

    <local:RadialPanel Width="300" Height="300">
        <Button Content="1" />
        <Button Content="2" />
        <Button Content="3" />
        <Button Content="4" />
        <Button Content="5" />
    </local:RadialPanel>

</UserControl>
```

```csharp
using System;
using Avalonia;
using Avalonia.Controls;

namespace MyApp;

public class RadialPanel : Panel
{
    protected override Size MeasureOverride(Size availableSize)
    {
        foreach (var child in Children)
        {
            child.Measure(availableSize);
        }
        return availableSize;
    }

    protected override Size ArrangeOverride(Size finalSize)
    {
        double centerX = finalSize.Width / 2;
        double centerY = finalSize.Height / 2;
        double radius = Math.Min(centerX, centerY) - 30;

        for (int i = 0; i < Children.Count; i++)
        {
            double angle = 2 * 3.14159 * i / Children.Count - 3.14159 / 2;
            double x = centerX + radius * Math.Cos(angle) - Children[i].DesiredSize.Width / 2;
            double y = centerY + radius * Math.Sin(angle) - Children[i].DesiredSize.Height / 2;
            Children[i].Arrange(new Rect(new Point(x, y), Children[i].DesiredSize));
        }
        return finalSize;
    }
}
```

</XamlPreview>

## 添加附加属性 {#adding-an-attached-property}

给 `RadialPanel` 加一个 `Slot` 属性，让子元素能指定自己在圆周上的位置。这里选用附加属性，是为了能逐个子元素地指定数据。

关于附加属性的更多指引，请参阅[附加属性](/docs/custom-controls/defining-properties#attached-properties)。

```csharp
public static readonly AttachedProperty<int> SlotProperty =
    AvaloniaProperty.RegisterAttached<RadialPanel, Control, int>("Slot");

public static int GetSlot(Control element) => element.GetValue(SlotProperty);
public static void SetSlot(Control element, int value) => element.SetValue(SlotProperty, value);
```

## 小贴士 {#tips}

- 在 `MeasureOverride` 中务必对每个子元素调用 `Measure`，没被测量的子元素渲染不正常。
- 在 `ArrangeOverride` 中务必对每个子元素调用 `Arrange`，没被排列的子元素根本不会出现。
- 注册会影响布局的样式化属性时，请使用 [`AffectsMeasure` 或 `AffectsArrange`](/docs/custom-controls/custom-drawn-controls#affectsrender-affectsmeasure-and-affectsarrange)，这样这些属性一变，面板就会重新布局。
- 从 `MeasureOverride` 返回面板实际需要的尺寸。返回得太大会浪费空间，太小则可能把子元素裁掉。

## 另请参阅 {#see-also}

- [附加属性](/docs/custom-controls/defining-properties#attached-properties)：让子控件为你的面板携带逐个子元素的布局数据。
- [布局](/docs/layout)：测量与排列机制的工作方式。
- [选择布局面板](/docs/layout/choosing-a-layout-panel)：自己动手写之前，先看看能不能用现成的内置面板。
