---
id: gridsplitter
title: GridSplitter
description: 一个控件：用户在运行时拖动分隔条，即可调整 Grid 中列或行的尺寸。
doc-type: reference
---

[`GridSplitter`](/api/avalonia/controls/gridsplitter) 控件让用户在运行时调整 `Grid` 中列或行的尺寸。分隔器本身绘制成一列或一行（尺寸可以指定），并带有一个可供用户在运行时拖动的手柄。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Background` | `IBrush` | 分隔条的背景色。 |
| `ResizeDirection` | `GridResizeDirection` | 分隔器的移动方向：`Auto`、`Columns`、`Rows`。参见下方说明。 |
| `ResizeBehavior` | `GridResizeBehavior` | 调整哪些列/行：`BasedOnAlignment`、`CurrentAndNext`、`PreviousAndCurrent`、`PreviousAndNext`。 |
| `DragIncrement` | `double` | 分隔器每次移动的最小像素数。 |
| `ShowsPreview` | `bool` | 为 `true` 时，拖动过程中只显示一条预览线，而不实时调整尺寸。 |

:::caution
要让拖动真正起作用，分隔器的移动方向必须与它的位置定义一致。也就是说：列分隔器指定 `ResizeDirection="Columns"`，行分隔器指定 `ResizeDirection="Rows"`。
:::

## 拖动行为 {#drag-behavior}

用户按住并拖动 `GridSplitter` 时，相邻的列或行会按 `ResizeBehavior` 属性来调整尺寸：

- **`BasedOnAlignment`**（默认值）：具体调整哪些列或行，取决于分隔器在其单元格内的 `HorizontalAlignment` 或 `VerticalAlignment`。
- **`CurrentAndNext`**：调整当前列/行与它后面那一个。
- **`PreviousAndCurrent`**：调整当前列/行与它前面那一个。
- **`PreviousAndNext`**：调整前一个和后一个列/行，跳过分隔器自己所在的那一列/行。

若把 `ShowsPreview` 设为 `true`，拖动时会有一条半透明的预览线跟着指针走，直到松开鼠标才真正应用尺寸调整。布局复杂时，这能改善性能。

`DragIncrement` 属性控制吸附粒度。比如设成 `DragIncrement="10"`，分隔器的位置就会按 10 像素的步长吸附。

## 最小/最大约束 {#minmax-constraints}

可以在 `ColumnDefinition` 元素上设置 `MinWidth`/`MaxWidth`（或在 `RowDefinition` 元素上设置 `MinHeight`/`MaxHeight`），限定分隔器能走多远。`GridSplitter` 会自动遵守这些约束，用户拖不出设定的范围。

```xml
<Grid>
    <Grid.ColumnDefinitions>
        <ColumnDefinition Width="200" MinWidth="100" MaxWidth="400" />
        <ColumnDefinition Width="4" />
        <ColumnDefinition Width="*" MinWidth="200" />
    </Grid.ColumnDefinitions>
    <Border Grid.Column="0" Background="LightBlue">
        <TextBlock Text="Sidebar (100-400px)" Margin="8" />
    </Border>
    <GridSplitter Grid.Column="1" Background="Gray" ResizeDirection="Columns" />
    <Border Grid.Column="2" Background="LightGreen">
        <TextBlock Text="Content (min 200px)" Margin="8" />
    </Border>
</Grid>
```

## 键盘支持 {#keyboard-support}

出于无障碍考虑，`GridSplitter` 支持键盘操作。分隔器获得焦点后，可以使用以下按键：

| 按键 | 动作 |
|---|---|
| `Left` / `Right` | 把列分隔器左移或右移。 |
| `Up` / `Down` | 把行分隔器上移或下移。 |

每按一次，分隔器移动 `DragIncrement` 指定的距离（默认 1 像素）。

## 示例 {#examples}

这是一个列分隔器。拖动列与列之间的边界即可调整它们的宽度。

<XamlPreview>

```xml
<Grid xmlns="https://github.com/avaloniaui"
      ColumnDefinitions="*, 4, *">
    <Rectangle Grid.Column="0" Fill="Blue"/>
    <GridSplitter Grid.Column="1" Background="Black" ResizeDirection="Columns"/>
    <Rectangle Grid.Column="2" Fill="Red"/>
</Grid>
```

</XamlPreview>

这是一个行分隔器。拖动行与行之间的边界即可调整它们的高度。

<XamlPreview>

```xml
<Grid xmlns="https://github.com/avaloniaui"
      RowDefinitions="*, 4, *">
    <Rectangle Grid.Row="0" Fill="Blue"/>
    <GridSplitter Grid.Row="1" Background="Black" ResizeDirection="Rows"/>
    <Rectangle Grid.Row="2" Fill="Red"/>
</Grid>
```

</XamlPreview>

## 另请参阅 {#see-also}

- [Grid](/controls/layout/panels/grid)
- [GridSplitter API 参考](/api/avalonia/controls/gridsplitter)
- [GitHub 上的 `GridSplitter.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/GridSplitter.cs)
