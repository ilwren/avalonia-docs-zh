---
id: layout
title: 布局
description: WPF 与 Avalonia 在布局系统、面板、尺寸和定位上的差异。
doc-type: migration
---

Avalonia 的布局系统与 WPF 非常相似。若你熟悉 WPF 的面板和布局概念，上手会很自然。不过还是有几处关键差异和新增之处值得一提。

## 面板类型 {#panel-types}

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| [`StackPanel`](/api/avalonia/controls/stackpanel) | `StackPanel` | 相同。Avalonia 多了一个 `Spacing` 属性。 |
| [`Grid`](/api/avalonia/controls/grid) | `Grid` | 相同。支持 `ColumnDefinitions="Auto,*"` 简写。 |
| `DockPanel` | `DockPanel` | 相同。`LastChildFill` 默认为 `true`。 |
| `WrapPanel` | `WrapPanel` | Same. |
| `Canvas` | `Canvas` | Same. |
| `UniformGrid` | `UniformGrid` | Same. |
| `VirtualizingStackPanel` | `VirtualizingStackPanel` | 概念相同。 |

## Grid 的简写语法 {#grid-shorthand-syntax}

Avalonia 支持用内联字符串定义 Grid 的行和列，XAML 写起来更精炼：

```xml
<!-- WPF verbose -->
<Grid>
    <Grid.ColumnDefinitions>
        <ColumnDefinition Width="Auto" />
        <ColumnDefinition Width="*" />
        <ColumnDefinition Width="200" />
    </Grid.ColumnDefinitions>
</Grid>

<!-- Avalonia shorthand (also works in WPF .NET 6+) -->
<Grid ColumnDefinitions="Auto,*,200" RowDefinitions="Auto,*" />
```

## 分层叠放该用 Panel 还是 Grid {#panel-vs-grid-for-layering}

Avalonia 提供了轻量的 `Panel` 控件，可用来把子元素叠在一起。在 WPF 中，开发者常用一个不定义行列的 `Grid` 来做内容叠放；在 Avalonia 中，这种场合更建议用 `Panel`，省去了 Grid 布局引擎的那份开销。

```xml
<!-- WPF approach for layering -->
<Grid>
    <Image Source="background.png" />
    <TextBlock Text="Overlay" />
</Grid>

<!-- Avalonia preferred approach -->
<Panel>
    <Image Source="background.png" />
    <TextBlock Text="Overlay" />
</Panel>
```

## Spacing 属性 {#spacing-property}

Avalonia 的 `StackPanel` 带有 `Spacing` 属性，省得你给每个子元素都设外边距：

```xml
<!-- Avalonia -->
<StackPanel Spacing="8">
    <Button Content="First" />
    <Button Content="Second" />
</StackPanel>
```

在 WPF 中，你通常得给每个子元素都加外边距才能达到同样效果：

```xml
<!-- WPF -->
<StackPanel>
    <Button Content="First" Margin="0,0,0,8" />
    <Button Content="Second" />
</StackPanel>
```

## ScrollViewer 的差异 {#scrollviewer-differences}

`ScrollViewer` 在两个框架中用法相同，`HorizontalScrollBarVisibility` 和 `VerticalScrollBarVisibility` 属性的取值也一样（`Auto`、`Visible`、`Hidden`、`Disabled`）。各平台默认的滚动行为可能略有出入，所以请在目标平台上实际试一试滚动效果。

## Viewbox

`Viewbox` 在两个框架中用法相同，都会拉伸或缩放子内容以填满可用空间。

## 布局取整 {#layout-rounding}

Avalonia 用 `UseLayoutRounding`（与 WPF 相同）把布局测量结果吸附到像素边界上，以免次像素定位导致画面发糊。

## 另请参阅 {#see-also}

- [布局](/docs/layout)：Avalonia 布局系统概览。
- [摆放控件](/docs/layout/positioning-controls)：外边距、对齐与定位。
