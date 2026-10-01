---
id: relativepanel
title: RelativePanel
description: 了解如何用 Avalonia 的 RelativePanel 让子控件相对彼此或相对面板定位。
doc-type: reference
---

`RelativePanel` 控件让你通过指定子控件相对于其他（同级）子控件、或相对于面板本身的位置来排布它们。位置的计算以面板控件的内侧（内容区）和子控件外边距区的外沿为准。

子控件的默认位置是面板的左上角。

子控件的布局用附加的相对位置属性来指定，格式如下：

`RelativePanel.PositionProperty="NameOfSibling"`

其中 `PositionProperty` 属性是某个相对位置属性（见下表），`NameOfSibling` 则是另一个子控件的 name 属性值。

:::danger
把相对位置属性的值写成子控件自己的名字是错误的——那会造成循环引用！
:::

每个子控件最多可以指定四个相对位置属性，分别用于计算上、下、左、右四条边。

:::danger
为同一个子控件重复定义同一个相对位置属性是错误的。
:::

指定若干不同但可能彼此冲突的相对位置属性并不算错，只是结果可能让人摸不着头脑。

若有多个子控件最终算到了同一个位置，它们会按在 XAML 中出现的顺序绘制，于是可能相互重叠或遮挡。

:::caution
也就是说，你必须给子控件起名字，并在相对位置属性的值里写对名字。一旦写错，该控件会退回默认的左上角位置，并可能与别的控件重叠或遮挡。
:::

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table><thead><tr><th width="348">Property</th><th>说明</th></tr></thead><tbody><tr><td><code>AlignTopWithPanel</code></td><td>布尔值。让子控件的上边缘与面板的上边缘对齐。</td></tr><tr><td><code>AlignBottomWithPanel</code></td><td>布尔值。附加到子控件上，让它的下边缘与面板的下边缘对齐。</td></tr><tr><td><code>AlignLeftWithPanel</code></td><td>布尔值。附加到子控件上，让它的左边缘与面板的左边缘对齐。</td></tr><tr><td><code>AlignRightWithPanel</code></td><td>布尔值。附加到子控件上，让它的右边缘与面板的右边缘对齐。</td></tr><tr><td><code>AlignHorizontalCenterWithPanel</code></td><td>布尔值。附加到子控件上，让它的水平中心与面板的水平中心对齐。</td></tr><tr><td><code>AlignVerticalCenterWithPanel</code></td><td>布尔值。附加到子控件上，让它的垂直中心与面板的垂直中心对齐。</td></tr><tr><td><code>AlignTopWith</code></td><td>附加到子控件上，让它的上边缘与指定同级控件的上边缘对齐。</td></tr><tr><td><code>AlignBottomWith</code></td><td>附加到子控件上，让它的下边缘与指定同级控件的下边缘对齐。</td></tr><tr><td><code>AlignLeftWith</code></td><td>附加到子控件上，让它的左边缘与指定同级控件的左边缘对齐。</td></tr><tr><td><code>AlignRightWith</code></td><td>附加到子控件上，让它的右边缘与指定同级控件的右边缘对齐。</td></tr><tr><td><code>AlignHorizontalCenterWith</code></td><td>附加到子控件上，让它的水平中心与指定同级控件的水平中心对齐。</td></tr><tr><td><code>AlignVerticalCenterWith</code></td><td>附加到子控件上，让它的垂直中心与指定同级控件的垂直中心对齐。</td></tr><tr><td><code>Above</code></td><td>附加到子控件上，让它的下边缘与指定同级控件的上边缘对齐。</td></tr><tr><td><code>Below</code></td><td>附加到子控件上，让它的上边缘与指定同级控件的下边缘对齐。</td></tr><tr><td><code>LeftOf</code></td><td>附加到子控件上，让它的右边缘与指定同级控件的左边缘对齐。</td></tr><tr><td><code>RightOf</code></td><td>附加到子控件上，让它的左边缘与指定同级控件的右边缘对齐。</td></tr></tbody></table>

## Example

下面这段 XAML 演示了几种不同的子控件排布方式：

<XamlPreview>

```xml
<Border xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        BorderBrush="DarkGray" BorderThickness="1"
        Margin="20">
  <RelativePanel>
    <Rectangle x:Name="RedRect" Fill="Red" Height="50" Width="50"/>
    <Rectangle x:Name="BlueRect" Fill="Blue" Opacity="0.5" Height="50" Width="150"
               RelativePanel.RightOf="RedRect" />
    <Rectangle x:Name="GreenRect" Fill="Green" Height="100"
               RelativePanel.Below="RedRect"
               RelativePanel.AlignLeftWith="RedRect"
               RelativePanel.AlignRightWith="BlueRect"/>
    <Rectangle Fill="Orange"
               RelativePanel.Below="GreenRect"
               RelativePanel.AlignLeftWith="BlueRect"
               RelativePanel.AlignRightWithPanel="True"
               RelativePanel.AlignBottomWithPanel="True"/>
  </RelativePanel>
</Border>
```

</XamlPreview>

关于上面这个例子，有几点说明：

* 红色矩形给了尺寸（50x50），但没给相对位置，因此落在默认的左上角位置。
* 蓝色矩形的不透明度设为 50%，好让你看出它并没有和别的矩形重叠。
* 绿色矩形给了高度（100）却没给宽度。它的左侧与红色矩形对齐、右侧与蓝色矩形对齐，宽度就是这么算出来的。
* 橙色矩形没给尺寸。它的左侧与蓝色矩形对齐，右边缘和下边缘与面板边缘对齐，因此尺寸完全由这些对齐关系决定；面板本身改变大小时，它也会跟着变。

## 另请参阅 {#see-also}

- [RelativePanel API 参考](/api/avalonia/controls/relativepanel)
- [GitHub 上的 `RelativePanel.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/RelativePanel.cs)
- [Canvas](/controls/layout/panels/canvas)
- [DockPanel](/controls/layout/panels/dockpanel)
- [Grid](/controls/layout/panels/grid)
- [Panel](/controls/layout/panels/panel)
- [StackPanel](/controls/layout/panels/stackpanel)
- [UniformGrid](/controls/layout/panels/uniformgrid)
- [WrapPanel](/controls/layout/panels/wrappanel)
