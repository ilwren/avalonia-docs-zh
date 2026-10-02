---
id: stackpanel
title: StackPanel
description: 一个面板：把子控件横着或竖着排成一条线。
doc-type: reference
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

[`StackPanel`](/api/avalonia/controls/stackpanel) 把子控件横向或纵向堆叠排布。界面上的小块区域，常常就用堆叠面板来编排。

在 `StackPanel` 中，若不给子控件设置垂直于堆叠方向的那个尺寸属性，子控件会被拉伸填满可用空间。比如横向排布时，没有显式设置 `Height` 的子控件会被拉伸填满可用高度。

在堆叠方向上，`StackPanel` 总会扩展到刚好容纳全部子控件。

:::tip
`StackPanel` 本身不滚动。如果堆叠的内容可能超出可用空间，请把 `StackPanel` 包进 `ScrollViewer`。
:::

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性      | 说明                                                                     |
| ------------- | ------------------------------------------------------------------------------- |
| [`Orientation`](/api/avalonia/layout/orientation) | 设置堆叠方向，可选 `Horizontal` 或 `Vertical`（默认）。 |
| `Spacing`     | 在相邻子控件之间留出均等的间隙。                         |
| `HorizontalAlignment` | 控制面板自身在其父级中的水平位置。 |
| `VerticalAlignment`   | 控制面板自身在其父级中的垂直位置。   |

## Example

下面这段 XAML 演示如何创建一个纵向堆叠面板。可以看到子控件被拉伸以填满宽度，而堆叠面板的总高度等于各子控件高度之和。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Width="200">
    <Rectangle Fill="Red" Height="50"/>
    <Rectangle Fill="Blue" Height="50"/>
    <Rectangle Fill="Green" Height="50"/>
    <Rectangle Fill="Orange" Height="50"/>
</StackPanel>
```

</XamlPreview>

## 在代码中定义 StackPanel {#defining-a-stackpanel-in-code}

下面的例子演示如何用 `StackPanel` 做出一列纵向排列的按钮。若要横向排列，把 `Orientation` 属性设为 `Horizontal` 即可。

<Tabs
  defaultValue="xaml"
  values={[
      { label: 'XAML', value: 'xaml', },
      { label: 'C#', value: 'cs', },
  ]}
>
<TabItem value="xaml">

```xml
<StackPanel HorizontalAlignment="Center"
            VerticalAlignment="Top"
            Spacing="25">
    <Button Content="Button 1" />
    <Button Content="Button 2" />
    <Button Content="Button 3" />
</StackPanel>
```

</TabItem>
<TabItem value="cs">

```csharp
// Define the StackPanel
var myStackPanel = new StackPanel();
myStackPanel.HorizontalAlignment = HorizontalAlignment.Center;
myStackPanel.VerticalAlignment = VerticalAlignment.Top;
myStackPanel.Spacing = 25;

// Define child content
Button myButton1 = new Button();
myButton1.Content = "Button 1";
Button myButton2 = new Button();
myButton2.Content = "Button 2";
Button myButton3 = new Button();
myButton3.Content = "Button 3";

// Add child elements to the parent StackPanel
myStackPanel.Children.Add(myButton1);
myStackPanel.Children.Add(myButton2);
myStackPanel.Children.Add(myButton3);
```

</TabItem>

</Tabs>

## 让条目居中 {#centering-items}

要让所有子元素在堆叠中居中，请把 `HorizontalAlignment` 设为 `Center`：

```xml
<StackPanel HorizontalAlignment="Center" Spacing="8">
    <Button Content="Short" />
    <Button Content="A longer button" />
</StackPanel>
```

## 带间距的横向堆叠 {#horizontal-stack-with-spacing}

把 `Orientation` 设为 `Horizontal` 并加上 `Spacing`，就能做出一条横向按钮栏：

```xml
<StackPanel Orientation="Horizontal" Spacing="12">
    <Button Content="Save" />
    <Button Content="Cancel" />
</StackPanel>
```

## 实用提示 {#practical-notes}

- **尺寸行为**：`StackPanel` 不会在堆叠方向上约束子元素，每个子元素要多少空间就给多少。若希望子元素按比例分享空间，不妨改用 `Grid`。
- **性能**：条目很多的列表请用 `ListBox`，别把一大堆控件塞进 `StackPanel`。
- **滚动**：由于 `StackPanel` 会撑到容纳全部子元素，它自己永远不会裁剪内容。可能溢出时，请把它包进 `ScrollViewer`。
- **逆序**：`StackPanel` 不支持反向堆叠。要让视觉顺序倒过来，请把子元素的顺序倒过来写，或改用自定义面板。

## 另请参阅 {#see-also}

- [StackPanel API 参考](/api/avalonia/controls/stackpanel)
- [GitHub 上的 `StackPanel.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/StackPanel.cs)
- [DockPanel](/controls/layout/panels/dockpanel)
- [Grid](/controls/layout/panels/grid)
- [WrapPanel](/controls/layout/panels/wrappanel)
- [Panel](/controls/layout/panels/panel)
