---
id: wrappanel
title: WrapPanel
description: 一个面板：把子控件按流式布局排布，排不下就换行。
doc-type: reference
---

`WrapPanel` 把子控件从左到右依次排布，空间不够时（包括各种外边距和边框在内）就换到下一行。

把 `Orientation` 属性设为 `Vertical` 后，排布方向变成自上而下，高度不够时就另起一列。

当你需要一种灵活的流式布局、让子元素随可用空间变化自动重排时，`WrapPanel` 就派上用场了。常见场景包括标签列表、缩略图画廊和按钮工具栏。

## 常用属性 {#useful-properties}

| 属性 | 说明 |
|---|---|
| `Orientation` | 排布的流向：`Horizontal`（默认）或 `Vertical`。 |
| `ItemSpacing` | 条目之间的水平间隙。 |
| `LineSpacing` | 行与行之间的垂直间隙（纵向模式下则是列与列之间的水平间隙）。 |
| `ItemWidth` | 所有条目的固定宽度。不设置时，条目使用各自的自然宽度。 |
| `ItemHeight` | 所有条目的固定高度。不设置时，条目使用各自的自然高度。 |
| `ItemsAlignment` | 控制条目在所分配单元格内的对齐方式。类型：`WrapPanelItemsAlignment`。取值：`Start`、`Center`、`End`。 |

## 常见用法 {#common-usage}

### 让条目尺寸统一 {#uniform-item-sizing}

若希望每个子元素都占同样大的空间，请设置 `ItemWidth` 和 `ItemHeight`。当各条目内容长短不一、你却想要整齐划一的视觉结构时，这尤其有用。

```xml
<WrapPanel ItemWidth="120" ItemHeight="120"
           ItemSpacing="8" LineSpacing="8">
    <Button Content="Short" />
    <Button Content="Medium text" />
    <Button Content="A longer button label" />
</WrapPanel>
```

### 单元格内的对齐 {#alignment-within-cells}

用了 `ItemWidth` 或 `ItemHeight` 之后，子控件可能比所分配的单元格更小。此时可以用 `ItemsAlignment` 控制它在单元格内的位置。

```xml
<WrapPanel ItemWidth="100" ItemHeight="100"
           ItemsAlignment="Center">
    <Button Content="A" />
    <Button Content="B" />
    <Button Content="C" />
</WrapPanel>
```

## 示例 {#examples}

### 横向排布（默认） {#horizontal-arrangement-default}

<XamlPreview>

```xml
<WrapPanel xmlns="https://github.com/avaloniaui"
           ItemSpacing="20" LineSpacing="20"
           Margin="20">
    <Rectangle Fill="Navy" Width="80" Height="80" />
    <Rectangle Fill="Yellow" Width="80" Height="80" />
    <Rectangle Fill="Green" Width="80" Height="80" />
    <Rectangle Fill="Red" Width="80" Height="80" />
    <Rectangle Fill="Purple" Width="80" Height="80" />
</WrapPanel>
```

</XamlPreview>

### 纵向排布 {#vertical-arrangement}

<XamlPreview>

```xml
<WrapPanel xmlns="https://github.com/avaloniaui"
           Orientation="Vertical"
           ItemSpacing="20" LineSpacing="20"
           Margin="20">
    <Rectangle Fill="Navy" Width="80" Height="80" />
    <Rectangle Fill="Yellow" Width="80" Height="80" />
    <Rectangle Fill="Green" Width="80" Height="80" />
    <Rectangle Fill="Red" Width="80" Height="80" />
    <Rectangle Fill="Purple" Width="80" Height="80" />
</WrapPanel>
```

</XamlPreview>

## 另请参阅 {#see-also}

- [StackPanel](/controls/layout/panels/stackpanel)
- [DockPanel](/controls/layout/panels/dockpanel)
- [WrapPanel API 参考](/api/avalonia/controls/wrappanel)
- [GitHub 上的 `WrapPanel.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/WrapPanel.cs)
