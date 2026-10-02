---
id: scrollviewer-how-to
title: "操作指南：使用 ScrollViewer"
description: 学会在 Avalonia 中控制滚动行为、用代码滚动、响应滚动事件、实现无限滚动，以及处理嵌套的滚动区域。
doc-type: how-to
---

本指南介绍 [`ScrollViewer`](/api/avalonia/controls/scrollviewer) 的常见场景，包括控制滚动行为、用代码滚动、响应滚动事件，以及处理嵌套的滚动区域。

## 基本用法 {#basic-usage}

凡是可能超出可用空间的内容，都可以包进 `ScrollViewer` 里：

```xml
<ScrollViewer>
    <StackPanel Spacing="8">
        <!-- Content that may be taller than the viewport -->
        <TextBlock Text="Item 1" />
        <TextBlock Text="Item 2" />
        <!-- ... many more items ... -->
    </StackPanel>
</ScrollViewer>
```

内容溢出可见区域时，`ScrollViewer` 会自动显示滚动条。

:::tip
`ScrollViewer` 不能放进在滚动方向上提供无限高度或宽度的容器里，比如 `StackPanel`。真这么做了，`ScrollViewer` 永远察觉不到溢出，因为父级给了它无限空间。请改用尺寸受约束的容器（比如 `Grid`、`DockPanel`，或者固定的 `Height`/`MaxHeight`）。
:::

## 滚动条的可见性 {#scrollbar-visibility}

设置 `HorizontalScrollBarVisibility` 和 `VerticalScrollBarVisibility` 即可控制各个滚动条何时出现：

```xml
<!-- Always show vertical scrollbar, never show horizontal -->
<ScrollViewer VerticalScrollBarVisibility="Visible"
              HorizontalScrollBarVisibility="Disabled">
    <TextBlock Text="{Binding LongText}" TextWrapping="Wrap" />
</ScrollViewer>
```

| 值 | 行为 |
|---|---|
| `Auto` | 仅在内容溢出时显示滚动条（垂直方向的默认值） |
| `Visible` | 始终显示滚动条，内容装得下也照样显示 |
| `Hidden` | 隐藏滚动条，但仍可通过触摸、鼠标滚轮或键盘滚动 |
| `Disabled` | 彻底禁止该方向的滚动 |

:::note
若把 `HorizontalScrollBarVisibility` 设为 `Disabled`（默认值），比视口更宽的内容会被裁掉。需要横向滚动时，请把它设为 `Auto` 或 `Visible`。
:::

## 用代码控制滚动 {#programmatic-scrolling}

### 滚动到指定位置 {#scroll-to-a-specific-position}

设置 `Offset` 属性即可直接跳到某个位置：

```csharp
// Scroll to 500 pixels from the top
scrollViewer.Offset = new Vector(0, 500);
```

`Offset` 以设备无关像素计量。这个值会被自动钳制，所以即便设成超出可滚动范围的值，也只是滚到尽头，而不会抛异常。

### 滚动到顶部或底部 {#scroll-to-top-or-bottom}

```csharp
// Scroll to top
scrollViewer.Offset = new Vector(scrollViewer.Offset.X, 0);

// Scroll to bottom
scrollViewer.Offset = new Vector(
    scrollViewer.Offset.X,
    scrollViewer.Extent.Height - scrollViewer.Viewport.Height);
```

### 把某个子元素带入视野 {#bring-a-child-element-into-view}

对子控件调用 `BringIntoView`，页面就会恰好滚到让它可见为止。当你知道目标控件、却不清楚它的确切位置时，这招特别管用：

```csharp
targetControl.BringIntoView();
```

你也可以指定一个相对目标控件的矩形区域：

```csharp
targetControl.BringIntoView(new Rect(0, 0, targetControl.Bounds.Width, targetControl.Bounds.Height));
```

:::tip
`BringIntoView` 在虚拟化面板上同样有效。当你对启用了虚拟化的 `ItemsControl` 中的某一项调用它时，面板会先把该项实体化出来，再滚动过去。
:::

## 响应滚动事件 {#respond-to-scroll-events}

### 监视滚动位置的变化 {#monitor-scroll-position-changes}

订阅 `ScrollChanged` 事件，即可在用户滚动时作出响应：

```csharp
scrollViewer.ScrollChanged += (sender, e) =>
{
    var offset = scrollViewer.Offset;
    var extent = scrollViewer.Extent;
    var viewport = scrollViewer.Viewport;

    // Check if scrolled to bottom (with a 1-pixel tolerance)
    var isAtBottom = offset.Y >= extent.Height - viewport.Height - 1;

    if (isAtBottom)
    {
        LoadMoreItems();
    }
};
```

### 观察偏移属性 {#observe-the-offset-property}

若你写的是响应式风格的代码，可以直接观察 `Offset` 属性：

```csharp
scrollViewer.GetObservable(ScrollViewer.OffsetProperty).Subscribe(offset =>
{
    Debug.WriteLine($"Scrolled to: {offset.Y}");
});
```

这种写法与 Avalonia 的响应式属性系统契合得很好，而且每次偏移变化都会触发，包括用代码引起的变化。

## 实现无限滚动 {#implement-infinite-scrolling}

有个常见做法是在用户快滚到底时继续加载内容。把滚动位置判断和异步数据加载方法结合起来即可：

```csharp
public partial class InfiniteListViewModel : ObservableObject
{
    private int _page = 0;
    private bool _isLoading;

    public ObservableCollection<Item> Items { get; } = new();

    public async Task LoadMoreAsync()
    {
        if (_isLoading) return;
        _isLoading = true;

        try
        {
            var newItems = await _api.GetItemsAsync(_page++, pageSize: 20);
            foreach (var item in newItems)
                Items.Add(item);
        }
        finally
        {
            _isLoading = false;
        }
    }
}
```

在代码隐藏里，当用户滚到距底部一定阈值内时触发加载：

```csharp
private async void OnScrollChanged(object? sender, ScrollChangedEventArgs e)
{
    if (sender is not ScrollViewer sv) return;

    var distanceFromBottom = sv.Extent.Height - sv.Viewport.Height - sv.Offset.Y;
    if (distanceFromBottom < 100)
    {
        await ((InfiniteListViewModel)DataContext!).LoadMoreAsync();
    }
}
```

:::note
阈值（本例中是 100 像素）决定加载提前多久开始。阈值大一些，数据源就有更充裕的时间在用户滚到尽头之前作出响应，体验也更顺滑。
:::

## 处理嵌套的 ScrollViewer {#handle-nested-scrollviewers}

嵌套可滚动内容时，请把外层 `ScrollViewer` 已经负责的那个滚动方向在内层关掉，免得两个滚动区域争抢同一份输入：

```xml
<ScrollViewer VerticalScrollBarVisibility="Auto">
    <StackPanel Spacing="16">
        <TextBlock Text="Section 1" FontSize="20" />

        <!-- Inner horizontal scroll only -->
        <ScrollViewer HorizontalScrollBarVisibility="Auto"
                      VerticalScrollBarVisibility="Disabled">
            <StackPanel Orientation="Horizontal" Spacing="8">
                <Border Width="200" Height="150" Background="Red" />
                <Border Width="200" Height="150" Background="Blue" />
                <Border Width="200" Height="150" Background="Green" />
            </StackPanel>
        </ScrollViewer>

        <TextBlock Text="Section 2" FontSize="20" />
        <!-- More content... -->
    </StackPanel>
</ScrollViewer>
```

若内层控件与外层在同一方向上都能滚动，你可以在内层控件上设置 `ScrollViewer.IsScrollChainingEnabled` 附加属性，决定滚动事件是否「接力」传给父级：

```xml
<!-- Prevent inner scroll from chaining to the outer ScrollViewer -->
<ListBox ScrollViewer.IsScrollChainingEnabled="False"
         Height="200"
         ItemsSource="{Binding InnerItems}" />
```

## 使用滚动吸附点 {#use-scroll-snap-points}

启用吸附点，做出轮播那样的滚动效果：

```xml
<ScrollViewer HorizontalScrollBarVisibility="Auto"
              VerticalScrollBarVisibility="Disabled"
              IsScrollChainingEnabled="True">
    <StackPanel Orientation="Horizontal" Spacing="16">
        <!-- Cards that snap into view -->
        <Border Width="300" Height="200" Background="#6366F1" CornerRadius="8" />
        <Border Width="300" Height="200" Background="#8B5CF6" CornerRadius="8" />
        <Border Width="300" Height="200" Background="#A78BFA" CornerRadius="8" />
    </StackPanel>
</ScrollViewer>
```

## 做一个吸顶标题布局 {#create-a-sticky-header-layout}

用 `Grid` 让标题固定不动，内容在它下方滚动：

```xml
<Grid RowDefinitions="Auto,*">
    <!-- Fixed header -->
    <Border Grid.Row="0" Background="White" Padding="16"
            ZIndex="1" BoxShadow="0 2 4 0 #20000000">
        <TextBlock Text="Fixed Header" FontWeight="Bold" />
    </Border>

    <!-- Scrollable content -->
    <ScrollViewer Grid.Row="1">
        <StackPanel Spacing="8" Margin="16">
            <!-- Your scrollable content here -->
        </StackPanel>
    </ScrollViewer>
</Grid>
```

这种写法能让标题始终可见。标题 `Border` 上的 `ZIndex` 保证了过渡或动画期间若发生重叠，它依然渲染在可滚动内容之上。

## 关键属性 {#key-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Offset` | `Vector` | 当前的滚动位置（X、Y） |
| `Extent` | `Size` | 可滚动内容的总尺寸 |
| `Viewport` | `Size` | 可见区域的尺寸 |
| `HorizontalScrollBarVisibility` | `ScrollBarVisibility` | 控制水平滚动条的行为 |
| `VerticalScrollBarVisibility` | `ScrollBarVisibility` | 控制垂直滚动条的行为 |
| `AllowAutoHide` | `bool` | 滚动条是否在闲置一段时间后自动隐藏（默认 `true`） |
| `IsScrollChainingEnabled` | `bool` | 滚动事件是否接力传给父级滚动区域 |

## 另请参阅 {#see-also}

- [ScrollViewer 参考](/controls/layout/containers/scrollviewer)
- [挑选布局面板](/docs/layout/choosing-a-layout-panel)
- [性能优化](/docs/app-development/performance)
- [ItemsControl 操作指南](/docs/how-to/itemscontrol-how-to)
