---
id: scrollbar
title: ScrollBar
description: 一个基础控件，提供可拖动的滑块和轨道，用于横向或纵向滚动内容。
doc-type: reference
---

import ScrollBarScreenshot from '/img/controls/scrollbar/scrollbar.gif';

[`ScrollBar`](/api/avalonia/controls/primitives/scrollbar) 控件提供可拖动的滑块和轨道，可用来滚动内容。它既能横向显示，也能纵向显示。默认取值范围是 0 到 100（类型为 `double`）。

设置 `Minimum` 和 `Maximum` 属性即可调整取值范围，还可以分别控制小步长和大步长。小步长由键盘方向键触发，大步长则由点击滚动条轨道、或按 Page Up / Page Down 键触发。

:::info
多数情况下你不必直接使用 `ScrollBar`，`ScrollViewer` 控件会自动管理滚动条。只有当你需要独立的滑块式输入、或自定义滚动行为时，才用得上 `ScrollBar`。
:::

## 常用属性 {#common-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| [`Orientation`](/api/avalonia/layout/orientation) | `Orientation` | 设置滚动条的方向，可取 `Horizontal` 或 `Vertical`，默认值是 `Vertical`。 |
| `Minimum` | `double` | 滚动条能表示的最小值，默认值是 `0`。 |
| `Maximum` | `double` | 滚动条能表示的最大值，默认值是 `100`。 |
| `Value` | `double` | 滚动条的当前值。 |
| `ViewportSize` | `double` | 可见区域（视口）相对于内容总长度的大小，它决定了滑块的尺寸。 |
| `SmallChange` | `double` | 小步长（按方向键）时值的变化量，默认值是 `1`。 |
| `LargeChange` | `double` | 大步长（点击轨道或按 Page Up / Page Down）时值的变化量，默认值是 `10`。 |
| `Visibility` | `ScrollBarVisibility` | 控制滚动条何时可见，可取 `Disabled`、`Auto`、`Visible` 或 `Hidden`。 |
| [`VerticalAlignment`](/api/avalonia/layout/verticalalignment) | `VerticalAlignment` | 滚动条在其容器中的垂直对齐方式，可取 `Top`、`Bottom`、`Center` 或 `Stretch`。 |
| [`HorizontalAlignment`](/api/avalonia/layout/horizontalalignment) | `HorizontalAlignment` | 滚动条在其容器中的水平对齐方式，可取 `Left`、`Right`、`Center` 或 `Stretch`。 |

:::caution
要让布局合理，方向和对齐这两类属性得搭配得当。举例来说，`Vertical` 的滚动条通常靠 `HorizontalAlignment` 来定位（比如 `Left` 或 `Right`），而 `Horizontal` 的滚动条则靠 `VerticalAlignment` 定位。
:::

## Orientation

设置 `Orientation` 属性来控制滚动条的方向。

```xml
<!-- Vertical scroll bar (default) -->
<ScrollBar Orientation="Vertical" HorizontalAlignment="Left" />

<!-- Horizontal scroll bar -->
<ScrollBar Orientation="Horizontal" VerticalAlignment="Bottom" />
```

## 配置取值范围 {#configuring-the-range}

取值范围和步长都可以按需调整。

```xml
<ScrollBar Minimum="0"
           Maximum="500"
           SmallChange="5"
           LargeChange="50"
           Value="100" />
```

## Example

下面的例子在一个面板中放了一条垂直滚动条，并在滚动时把当前值实时显示到文本块上。

```xml
<Panel>
  <Border Background="AliceBlue">
    <ScrollBar Visibility="Auto"
               HorizontalAlignment="Left"
               Scroll="ScrollHandler" />
  </Border>
  <TextBlock Name="valueText" Margin="60">0</TextBlock>
</Panel>
```

```csharp title='C#'
using Avalonia.Controls;
using Avalonia.Controls.Primitives;

namespace AvaloniaControls.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        public void ScrollHandler(object source, ScrollEventArgs args)
        {
            valueText.Text = args.NewValue.ToString();
        }
    }
}
```

配上这段代码隐藏文件，拖动滚动条时文本块就会显示它的当前值。

<Image light={ScrollBarScreenshot} alt="ScrollBar example showing value tracking" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [ScrollViewer](/controls/layout/containers/scrollviewer)
- [ScrollBar API 参考](/api/avalonia/controls/primitives/scrollbar)
- [GitHub 上的 `ScrollBar.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Primitives/ScrollBar.cs)
