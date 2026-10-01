---
id: canvas
title: Canvas
description: 了解如何用 Avalonia 的 Canvas 面板按绝对坐标摆放子控件。
doc-type: reference
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CanvasContentZoneScreenshot from '/img/controls/canvas/canvas-contentzone.png';

canvas 控件把子控件显示在指定位置（以坐标给出）。

每个子控件的位置由两段距离定义：canvas 内容区的边缘，到子元素外边距区外沿的距离。比如下图所示，就是子元素左上角到 canvas 左上角的距离：

<Image light={CanvasContentZoneScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

若多个元素占据同一坐标，它们在标记中出现的先后顺序决定了绘制顺序。

[`Canvas`](/api/avalonia/controls/canvas) 是所有 `Panel` 中布局最灵活的一个。Height 和 Width 属性定义 canvas 的区域，其中的元素则按相对于父 `Canvas` 区域的绝对坐标摆放。四个附加属性——`Canvas.Left`、`Canvas.Top`、`Canvas.Right` 和 `Canvas.Bottom`——让你能精细控制对象在 `Canvas` 中的位置，从而把元素精确地安排在屏幕上。

:::info
想回顾布局区域这个概念，请参阅[布局](/docs/layout/)。
:::

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table><thead><tr><th width="205">Property</th><th>说明</th></tr></thead><tbody><tr><td><code>Canvas.Left</code></td><td>附加到子控件上——给出 canvas 内容区左内沿到子元素左外沿（外边距区）的距离。</td></tr><tr><td><code>Canvas.Top</code></td><td>附加到子控件上——给出 canvas 内容区上内沿到子元素上外沿（外边距区）的距离。</td></tr><tr><td><code>Canvas.Right</code></td><td>附加到子控件上——给出 canvas 内容区右内沿到子元素右外沿（外边距区）的距离。</td></tr><tr><td><code>Canvas.Bottom</code></td><td>附加到子控件上——给出 canvas 内容区下内沿到子元素下外沿（外边距区）的距离。</td></tr><tr><td><code>ZIndex</code></td><td>一个继承自 <code>Visual</code> 的属性，可以覆盖默认的绘制顺序（见下文）。</td></tr></tbody></table>

canvas 中的子控件按定义顺序绘制，因此它们可能相互重叠。

:::caution
canvas 不会为任何子控件确定尺寸。你必须在子控件上设置宽度和高度属性，否则它根本不会显示！
:::

## Z-index

默认情况下每个子元素的 z-index 都是零。不过你可以在任意子控件上设置 `ZIndex` 属性。该属性继承自 `Visual`，会覆盖绘制顺序（数值最大的最后绘制），从而改变子控件之间的重叠关系。

## Opacity

不管绘制顺序如何定义，子控件的不透明度都会被遵守。也就是说，子控件相互重叠时，若上层控件的不透明度小于 1，重叠区域显示的内容会发生混合。

## ClipToBounds

`Canvas` 可以把子元素摆在屏幕上的任意位置，哪怕坐标超出了它自己定义的 `Height` 和 `Width`。而且 `Canvas` 不受其子元素尺寸的影响。于是子元素有可能画到父 `Canvas` 的边界矩形之外、盖住别的元素。`Canvas` 的默认行为就是允许子元素画到父 `Canvas` 的边界之外。若不希望如此，可以把 `ClipToBounds` 属性设为 `true`，这会让 `Canvas` 按自身尺寸裁剪。`Canvas` 是唯一允许子元素画出边界的布局元素。

## Example

<XamlPreview>

```xml
<Canvas xmlns="https://github.com/avaloniaui"
        Background="AliceBlue" Margin="20">
  <Rectangle Fill="Red" Height="100" Width="100" Margin="10"/>
  <Rectangle Fill="Blue" Height="100" Width="100" Opacity="0.5"
             Canvas.Left="50" Canvas.Top="20"/>
  <Rectangle Fill="Green" Height="100" Width="100" 
             Canvas.Left="60" Margin="40" Canvas.Top="40"/>
  <Rectangle Fill="Orange" Height="100" Width="100" 
             Canvas.Right="70" Canvas.Bottom="60"/>
</Canvas>
```

</XamlPreview>

:::info
canvas 面板要悠着点用。这样摆放子控件固然省事，但你的界面就不再能随应用窗口尺寸自适应了。
:::

## 在代码中定义 canvas {#defining-a-canvas-in-code}

<Tabs
  defaultValue="xaml"
  values={[
      { label: 'XAML', value: 'xaml', },
      { label: 'C#', value: 'cs', },
  ]}
>
<TabItem value="xaml">

```xml
<Canvas Height="400" Width="400">
  <Canvas Height="100" Width="100" Top="0" Left="0" Background="Red"/>
  <Canvas Height="100" Width="100" Top="100" Left="100" Background="Green"/>
  <Canvas Height="100" Width="100" Top="50" Left="50" Background="Blue"/>
</Canvas>
```

</TabItem>
<TabItem value="cs">

```cs
// Create the Canvas
myParentCanvas = new Canvas();
myParentCanvas.Width = 400;
myParentCanvas.Height = 400;

// Define child Canvas elements
myCanvas1 = new Canvas();
myCanvas1.Background = Brushes.Red;
myCanvas1.Height = 100;
myCanvas1.Width = 100;
Canvas.SetTop(myCanvas1, 0);
Canvas.SetLeft(myCanvas1, 0);

myCanvas2 = new Canvas();
myCanvas2.Background = Brushes.Green;
myCanvas2.Height = 100;
myCanvas2.Width = 100;
Canvas.SetTop(myCanvas2, 100);
Canvas.SetLeft(myCanvas2, 100);

myCanvas3 = new Canvas();
myCanvas3.Background = Brushes.Blue;
myCanvas3.Height = 100;
myCanvas3.Width = 100;
Canvas.SetTop(myCanvas3, 50);
Canvas.SetLeft(myCanvas3, 50);

// Add child elements to the Canvas' Children collection
myParentCanvas.Children.Add(myCanvas1);
myParentCanvas.Children.Add(myCanvas2);
myParentCanvas.Children.Add(myCanvas3);
```
</TabItem>  

</Tabs>

## 另请参阅 {#see-also}

- [Canvas API 参考](/api/avalonia/controls/canvas)
- [GitHub 上的 `Canvas.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Canvas.cs)
- [DockPanel](/controls/layout/panels/dockpanel)
- [Grid](/controls/layout/panels/grid)
- [Panel](/controls/layout/panels/panel)
- [RelativePanel](/controls/layout/panels/relativepanel)
- [StackPanel](/controls/layout/panels/stackpanel)
- [UniformGrid](/controls/layout/panels/uniformgrid)
- [WrapPanel](/controls/layout/panels/wrappanel)
