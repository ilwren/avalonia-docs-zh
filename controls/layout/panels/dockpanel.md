---
id: dockpanel
title: DockPanel
description: 了解如何用 Avalonia 的 DockPanel 把子控件停靠到容器的各个边缘。
doc-type: reference
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import DockPanelTopScreenshot from '/img/controls/dockpanel/dockpanel-top.png';

[`DockPanel`](/api/avalonia/controls/dockpanel) 控件把子控件沿指定的「停靠边」（上、下、左、右）排布，最后一个子元素则填满剩余空间。dock panel 会保持子控件与停靠边平行的那个方向上的尺寸，让子元素沿停靠边占满可用空间。

举例来说，若某个子控件的停靠边定义为「上」，且只定义了高度、没定义宽度，它会这样绘制：

<Image light={DockPanelTopScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

:::caution
你必须定义子控件在垂直于停靠边方向上的尺寸，否则它不会显示。
:::

与停靠边平行方向上的尺寸则可选。一旦定义了它，子元素会按同方向的对齐设置来绘制。比如一个定义了宽度、停靠在上边缘的子元素，会遵循它的水平对齐属性（默认居中）。

子控件按它们在 XAML 中定义的顺序依次停靠。Avalonia 在为子控件确定尺寸时会把先前已绘制的控件考虑在内，因此绝不会出现重叠。

最后定义的那个子控件会填满剩余空间。

:::caution
你必须始终定义一个（不带 dock 属性的）末位子控件，否则停靠计算不会正确进行。换句话说，dock panel 至少需要两个子控件。
:::

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table><thead><tr><th width="266">Property</th><th>说明</th></tr></thead><tbody><tr><td>DockPanel.Dock<code>.Left</code></td><td>附加到子控件上——把它停靠到左侧。</td></tr><tr><td>DockPanel.Dock<code>.Top</code></td><td>附加到子控件上——把它停靠到上边缘。</td></tr><tr><td>DockPanel.Dock<code>.Right</code></td><td>附加到子控件上——把它停靠到右侧。</td></tr><tr><td>DockPanel.Dock<code>.Bottom</code></td><td>附加到子控件上——把它停靠到下边缘。</td></tr><tr><td><code>HorizontalSpacing</code></td><td>设置已停靠子控件之间的水平间距（double，默认 0）。</td></tr><tr><td><code>VerticalSpacing</code></td><td>设置已停靠子控件之间的垂直间距（double，默认 0）。</td></tr></tbody></table>

## 按内容确定尺寸 {#sizing-to-content}

若未指定 `Height` 和 `Width` 属性，`DockPanel` 会按内容确定自身尺寸：它可以随子元素的大小而放大或缩小。但一旦指定了这些属性，当空间不足以容纳下一个子元素时，`DockPanel` 就不再显示该子元素及其之后的子元素，也不会再去测量它们。

## LastChildFill

默认情况下，`DockPanel` 元素的最后一个子元素会「填满」剩余的未分配空间。若不希望如此，请把 `LastChildFill` 属性设为 `false`。

## Example

把橙色矩形的不透明度设为 0.5，就能看出它们并无重叠。

<XamlPreview>

```xml
<DockPanel xmlns="https://github.com/avaloniaui"
           Width="300" Height="300">
    <Rectangle Fill="Red" Height="100" DockPanel.Dock="Top"/>
    <Rectangle Fill="Blue" Width="100" DockPanel.Dock="Left" />
    <Rectangle Fill="Green" Height="100" DockPanel.Dock="Bottom"/>
    <Rectangle Fill="Orange" Width="100" DockPanel.Dock="Right" Opacity="0.5"/>
    <Rectangle Fill="Gray" />
</DockPanel>
```

</XamlPreview>

## 在代码中定义 DockPanel {#defining-a-dockpanel-in-code}

<Tabs
  defaultValue="xaml"
  values={[
      { label: 'XAML', value: 'xaml', },
      { label: 'C#', value: 'cs', },
  ]}
>
<TabItem value="xaml">

```xml
<DockPanel LastChildFill="True">
  <Border Height="25" Background="SkyBlue" BorderBrush="Black" BorderThickness="1" DockPanel.Dock="Top">
    <TextBlock Foreground="Black">Dock = "Top"</TextBlock>
  </Border>
  <Border Height="25" Background="SkyBlue" BorderBrush="Black" BorderThickness="1" DockPanel.Dock="Top">
    <TextBlock Foreground="Black">Dock = "Top"</TextBlock>
  </Border>
  <Border Height="25" Background="LemonChiffon" BorderBrush="Black" BorderThickness="1" DockPanel.Dock="Bottom">
    <TextBlock Foreground="Black">Dock = "Bottom"</TextBlock>
  </Border>
  <Border Width="200" Background="PaleGreen" BorderBrush="Black" BorderThickness="1" DockPanel.Dock="Left">
    <TextBlock Foreground="Black">Dock = "Left"</TextBlock>
  </Border>
  <Border Background="White" BorderBrush="Black" BorderThickness="1">
    <TextBlock Foreground="Black">This content will "Fill" the remaining space</TextBlock>
  </Border>
</DockPanel>
```

</TabItem>
<TabItem value="cs">

```cs
// Create the DockPanel
DockPanel myDockPanel = new DockPanel();
myDockPanel.LastChildFill = true;

// Define the child content
Border myBorder1 = new Border();
myBorder1.Height = 25;
myBorder1.Background = Brushes.SkyBlue;
myBorder1.BorderBrush = Brushes.Black;
myBorder1.BorderThickness = new Thickness(1);
DockPanel.SetDock(myBorder1, Dock.Top);
TextBlock myTextBlock1 = new TextBlock();
myTextBlock1.Foreground = Brushes.Black;
myTextBlock1.Text = "Dock = Top";
myBorder1.Child = myTextBlock1;

Border myBorder2 = new Border();
myBorder2.Height = 25;
myBorder2.Background = Brushes.SkyBlue;
myBorder2.BorderBrush = Brushes.Black;
myBorder2.BorderThickness = new Thickness(1);
DockPanel.SetDock(myBorder2, Dock.Top);
TextBlock myTextBlock2 = new TextBlock();
myTextBlock2.Foreground = Brushes.Black;
myTextBlock2.Text = "Dock = Top";
myBorder2.Child = myTextBlock2;

Border myBorder3 = new Border();
myBorder3.Height = 25;
myBorder3.Background = Brushes.LemonChiffon;
myBorder3.BorderBrush = Brushes.Black;
myBorder3.BorderThickness = new Thickness(1);
DockPanel.SetDock(myBorder3, Dock.Bottom);
TextBlock myTextBlock3 = new TextBlock();
myTextBlock3.Foreground = Brushes.Black;
myTextBlock3.Text = "Dock = Bottom";
myBorder3.Child = myTextBlock3;

Border myBorder4 = new Border();
myBorder4.Width = 200;
myBorder4.Background = Brushes.PaleGreen;
myBorder4.BorderBrush = Brushes.Black;
myBorder4.BorderThickness = new Thickness(1);
DockPanel.SetDock(myBorder4, Dock.Left);
TextBlock myTextBlock4 = new TextBlock();
myTextBlock4.Foreground = Brushes.Black;
myTextBlock4.Text = "Dock = Left";
myBorder4.Child = myTextBlock4;

Border myBorder5 = new Border();
myBorder5.Background = Brushes.White;
myBorder5.BorderBrush = Brushes.Black;
myBorder5.BorderThickness = new Thickness(1);
TextBlock myTextBlock5 = new TextBlock();
myTextBlock5.Foreground = Brushes.Black;
myTextBlock5.Text = "This content will Fill the remaining space";
myBorder5.Child = myTextBlock5;

// Add child elements to the DockPanel Children collection
myDockPanel.Children.Add(myBorder1);
myDockPanel.Children.Add(myBorder2);
myDockPanel.Children.Add(myBorder3);
myDockPanel.Children.Add(myBorder4);
myDockPanel.Children.Add(myBorder5);
```
</TabItem>  

</Tabs>

## 另请参阅 {#see-also}

- [DockPanel API 参考](/api/avalonia/controls/dockpanel)
- [GitHub 上的 `DockPanel.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/DockPanel.cs)
- [Canvas](/controls/layout/panels/canvas)
- [Grid](/controls/layout/panels/grid)
- [Panel](/controls/layout/panels/panel)
- [RelativePanel](/controls/layout/panels/relativepanel)
- [StackPanel](/controls/layout/panels/stackpanel)
- [UniformGrid](/controls/layout/panels/uniformgrid)
- [WrapPanel](/controls/layout/panels/wrappanel)
