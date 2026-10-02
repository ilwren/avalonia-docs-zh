---
id: uniformgrid
title: UniformGrid
description: 一个面板：把子元素排进单元格大小完全相同的网格里。
doc-type: reference
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

[`UniformGrid`](/api/avalonia/controls/primitives/uniformgrid) 把可用空间划成大小相同的单元格。你只需指定要几行几列，子控件就会按出现顺序依次填进下一个空格。与 `Grid` 不同，它不需要定义行列尺寸，也不用给子元素指定单元格。因此，当你要的是工具栏、调色板、图标网格这类简单而均匀的布局时，`UniformGrid` 是个好选择。

## 常用属性 {#common-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Rows` | `int` | 设置等高行的数量。为 `0`（默认值）时，行数会根据子元素个数和 `Columns` 的值自动算出。 |
| `Columns` | `int` | 设置等宽列的数量。为 `0`（默认值）时，列数会根据子元素个数和 `Rows` 的值自动算出。 |
| `FirstColumn` | `int` | 设置第一个子元素的列偏移。用它可以在第一行开头留出几个空格。 |
| `RowSpacing` | `double` | 设置行与行之间的垂直间隙。 |
| `ColumnSpacing` | `double` | 设置列与列之间的水平间隙。 |

## 尺寸是怎么算的 {#how-sizing-works}

同时设置 `Rows` 和 `Columns` 时，网格就恰好造出那么多单元格。只设其中一个时，另一个会自动算出，以保证所有子元素都放得下。两个都不设时，`UniformGrid` 默认排成接近正方形的样子。

每个单元格等宽等高：把可用总空间（扣除间距）在各个方向上均分，就是单元格的尺寸。子元素默认被拉伸填满所在单元格，不过你可以在各个子控件上用 `HorizontalAlignment` 和 `VerticalAlignment` 来控制。

## 基本示例 {#basic-example}

下面的例子做了一个单行网格，里面是三个等大的彩色矩形。

<XamlPreview>

```xml
<UniformGrid xmlns="https://github.com/avaloniaui"
             Rows="1" Columns="3"
             ColumnSpacing="10"
             Margin="20">
    <Rectangle Fill="Navy" />
    <Rectangle Fill="White" />
    <Rectangle Fill="Red" />
</UniformGrid>
```

</XamlPreview>

## 多行网格示例 {#multi-row-grid-example}

下面的例子创建了一个 3 行 4 列的 `UniformGrid`，并往里放了 12 个矩形。每个 `Rectangle` 都会按行优先的顺序自动落进下一个单元格。

<Tabs
  defaultValue="xaml"
  values={[
      { label: 'XAML', value: 'xaml', },
      { label: 'C#', value: 'cs', },
  ]}
>
<TabItem value="xaml">

```xml
<UniformGrid Rows="3" Columns="4">
  <Rectangle Width="50" Height="50" Fill="#330000"/>
  <Rectangle Width="50" Height="50" Fill="#660000"/>
  <Rectangle Width="50" Height="50" Fill="#990000"/>
  <Rectangle Width="50" Height="50" Fill="#CC0000"/>
  <Rectangle Width="50" Height="50" Fill="#FF0000"/>
  <Rectangle Width="50" Height="50" Fill="#FF3300"/>
  <Rectangle Width="50" Height="50" Fill="#FF6600"/>
  <Rectangle Width="50" Height="50" Fill="#FF9900"/>
  <Rectangle Width="50" Height="50" Fill="#FFCC00"/>
  <Rectangle Width="50" Height="50" Fill="#FFFF00"/>
  <Rectangle Width="50" Height="50" Fill="#FFFF33"/>
  <Rectangle Width="50" Height="50" Fill="#FFFF66"/>
</UniformGrid>
```

</TabItem>
<TabItem value="cs">

```csharp
// Create the UniformGrid
var myUniformGrid = new UniformGrid
{
    Rows = 3,
    Columns = 4
};

// Add 12 rectangles with a color gradient
for (int i = 0; i < 12; i++)
{
    var rectangle = new Rectangle
    {
        Fill = new SolidColorBrush(Color.FromRgb((byte)(i * 20), 0, 0)),
        Width = 50,
        Height = 50
    };
    myUniformGrid.Children.Add(rectangle);
}
```

</TabItem>

</Tabs>

## Using `FirstColumn`

用 `FirstColumn` 属性可以让第一个子元素往后错开，在第一行开头留出空格。当你不希望内容从最左侧的单元格开始时，这很有用。

```xml
<UniformGrid Rows="2" Columns="3" FirstColumn="1">
  <Button Content="A" />
  <Button Content="B" />
  <Button Content="C" />
  <Button Content="D" />
  <Button Content="E" />
</UniformGrid>
```

本例中第一行的第一个单元格是空的，按钮「A」出现在第一行第二列。

## 小贴士 {#tips}

- 如果需要大小不一的单元格，请改用 `Grid`。
- 当子元素的数量多于单元格时，多出来的子元素仍会参与布局，但可能跑到可见区域之外。
- `UniformGrid` 会遵守子控件上的 `Margin`，因此除了 `RowSpacing` 和 `ColumnSpacing`，你还可以给单个条目单独加间距。

## 另请参阅 {#see-also}

- [Grid](/controls/layout/panels/grid)
- [WrapPanel](/controls/layout/panels/wrappanel)
- [StackPanel](/controls/layout/panels/stackpanel)
- [UniformGrid API 参考](https://reference.avaloniaui.net/api/Avalonia.Controls.Primitives/UniformGrid/)

