---
id: scrollviewer
title: ScrollViewer
description: 一个容器控件：当内容超出可见区域时提供滚动条。
doc-type: reference
---

[`ScrollViewer`](/api/avalonia/controls/scrollviewer) 控件允许其内容大于自身的内容区，并提供滚动条，让用户把隐藏的内容滚动到视野中。

:::warning
不能把 `ScrollViewer` 放进在滚动方向上高度或宽度无限的控件里（比如 `StackPanel`）。要避开这个坑，可以给 `ScrollViewer` 设置固定的 `Height`/`Width` 或 `MaxHeight`/`MaxWidth`，或者换一个容器面板。
:::

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
|---|---|---|
| `HorizontalScrollBarVisibility` | [`ScrollBarVisibility`](/api/avalonia/controls/primitives/scrollbarvisibility) | 控制水平滚动条：`Auto`、`Visible`、`Hidden`、`Disabled`。 |
| `VerticalScrollBarVisibility` | `ScrollBarVisibility` | 控制垂直滚动条：`Auto`、`Visible`、`Hidden`、`Disabled`。 |
| `AllowAutoHide` | `bool` | 默认 `true`。设置指针移开控件时滚动条是否自动隐藏。 |
| `Offset` | `Vector` | 当前的滚动位置（X, Y）。 |
| `Extent` | `Size` | 可滚动内容的总尺寸。 |
| `Viewport` | `Size` | 可见区域的尺寸。 |
| `IsScrollChainingEnabled` | `bool` | 附加属性，默认 `true`。设在内层可滚动控件上，决定滚动事件是否向外层 `ScrollViewer` 传递。 |
| `IsDeferredScrollingEnabled` | `bool` | 默认 `false`。为 `true` 时，内容要等到用户松开滚动条滑块之后才滚动。内容很重时，这有助于性能。 |
| `BringIntoViewOnFocusChange` | `bool` | 默认 `true`。当某个子控件获得焦点时，`ScrollViewer` 会自动滚动，把它带进视野。 |

## 滚动条可见性的取值 {#scrollbar-visibility-options}

两个方向的滚动条都接受以下 `ScrollBarVisibility` 取值之一：

| 值 | 行为 |
|---|---|
| `Auto` | 仅当内容溢出时显示滚动条。这是垂直滚动的默认值。 |
| `Visible` | 始终显示滚动条，哪怕内容在视口内放得下。 |
| `Hidden` | 隐藏滚动条，但仍可用触摸、鼠标滚轮或键盘滚动。 |
| `Disabled` | 彻底禁止该方向的滚动。这是水平滚动的默认值。 |

```xml
<!-- Always show the vertical scrollbar, disable horizontal scrolling -->
<ScrollViewer VerticalScrollBarVisibility="Visible"
              HorizontalScrollBarVisibility="Disabled">
    <TextBlock Text="{Binding LongText}" TextWrapping="Wrap" />
</ScrollViewer>
```

## 滚动传递 {#scroll-chaining}

当你把一个可滚动控件嵌进 `ScrollViewer`，而用户又把内层控件滚到了头，滚动传递决定外层 `ScrollViewer` 是否接着滚。在内层控件上用 `IsScrollChainingEnabled` 附加属性即可开关这一行为：

```xml
<ScrollViewer>
    <StackPanel>
        <!-- This inner ListBox will NOT chain scrolling to the outer ScrollViewer -->
        <ListBox ScrollViewer.IsScrollChainingEnabled="False"
                 ItemsSource="{Binding Items}"
                 MaxHeight="200" />
        <TextBlock Text="Other content below" />
    </StackPanel>
</ScrollViewer>
```

下列控件支持该附加属性：

* `ScrollViewer`
* `DataGrid`
* `ListBox`
* `TextBox`
* `TreeView`

## 用代码控制滚动 {#programmatic-scrolling}

滚动位置可以在代码隐藏或视图模型中控制：

```csharp
// Scroll to a specific position
scrollViewer.Offset = new Vector(0, 500);

// Scroll to the top
scrollViewer.Offset = new Vector(scrollViewer.Offset.X, 0);

// Scroll to the bottom
scrollViewer.Offset = new Vector(scrollViewer.Offset.X, scrollViewer.Extent.Height);

// Scroll a child element into view
targetControl.BringIntoView();
```

订阅 `Offset` 的属性变化，还能监听滚动位置的改变：

```csharp
scrollViewer.GetObservable(ScrollViewer.OffsetProperty).Subscribe(offset =>
{
    // React to scroll position changes
    Debug.WriteLine($"Scrolled to: {offset.X}, {offset.Y}");
});
```

## Example

下面的例子创建了一个比它所在的 `Border` 更高的 `StackPanel`，于是 `ScrollViewer` 自动显示出垂直滚动条。

<XamlPreview>

```xml
<Border xmlns="https://github.com/avaloniaui" Background="Gray" Width="200" Height="200">
  <ScrollViewer>
    <StackPanel>
      <TextBlock FontSize="22" Height="50" Background="Blue">Block 1</TextBlock>
      <TextBlock FontSize="22" Height="50">Block 2</TextBlock>
      <TextBlock FontSize="22" Height="50" Background="Blue">Block 3</TextBlock>
      <TextBlock FontSize="22" Height="50">Block 4</TextBlock>
      <TextBlock FontSize="22" Height="50" Background="Blue">Block 5</TextBlock>
    </StackPanel>
  </ScrollViewer>
</Border>
```

</XamlPreview>

### 水平滚动 {#horizontal-scrolling}

要启用水平滚动，请把 `HorizontalScrollBarVisibility` 设为 `Auto` 或 `Visible`：

```xml
<ScrollViewer HorizontalScrollBarVisibility="Auto"
              VerticalScrollBarVisibility="Disabled"
              Height="100">
    <StackPanel Orientation="Horizontal" Spacing="8">
        <Border Width="200" Height="80" Background="CornflowerBlue" />
        <Border Width="200" Height="80" Background="SeaGreen" />
        <Border Width="200" Height="80" Background="Coral" />
        <Border Width="200" Height="80" Background="MediumPurple" />
    </StackPanel>
</ScrollViewer>
```

## 另请参阅 {#see-also}

- [ScrollViewer API 参考](/api/avalonia/controls/scrollviewer)
- [GitHub 上的 `ScrollViewer.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ScrollViewer.cs)

