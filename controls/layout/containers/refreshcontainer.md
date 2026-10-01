---
id: refreshcontainer
title: RefreshContainer
---

`RefreshContainer` 让用户下拉内容或数据列表来刷新内容、加载更多数据。刷新进度由 `RefreshVisualizer` 指示，它会从发起下拉手势的那一侧边缘出现。`RefreshContainer` 的内容必须是 `ScrollViewer`，或是一个内含滚动视图的控件。

## Example

```xml
<RefreshContainer xmlns="https://github.com/avaloniaui" PullDirection="TopToBottom"
                RefreshRequested="RefreshContainerPage_RefreshRequested">
    <ListBox ItemsSource="{Binding Items}"/>
</RefreshContainer>
```

```csharp
private void RefreshContainerPage_RefreshRequested(object? sender, RefreshRequestedEventArgs e)
{
    // Retrieve a deferral object.
    var deferral = e.GetDeferral();

    // Refresh List Box Items

    // Notify the Refresh Container that the refresh is complete.
    deferral.Complete();
}
```

## Refreshing
沿 `PullDirection` 属性指定的方向一直拉到可视化指示器完全展开，或是调用 RefreshContainer 的 `RequestRefresh` 方法，都可以发起一次刷新。刷新进度由 `Visualizer` 的 `RefreshVisualizerState` 指示，它可能处于以下任一状态：

### Idle
这是指示器的默认状态：用户没有与容器交互，也没有刷新在进行中，指示器处于隐藏状态。

### Interacting
用户正沿 `PullDirection` 属性指定的方向下拉，但还没达到下拉阈值。随着下拉，指示器逐渐显现，直至达到阈值。若在达到阈值之前松手，`Visualizer` 会回到 `Idle` 状态，不会发起刷新；若达到了阈值，`Visualizer` 则进入 `Pending` 状态。

### Pending
用户已经拉过了下拉阈值。此状态下指示器完全可见。如果用户又把触点挪回阈值以内，指示器会退回 `Interacting` 状态；如果用户在 `Pending` 状态下松手，指示器则进入 `Refreshing` 状态。

### Refreshing
用户在指示器处于 `Pending` 状态时松开了触点，此时会引发 `RefreshRequested` 事件。事件参数中含有一个 `Deferral` 对象，用于告知 Refresh Container 刷新动作已经完成；耗时较长的刷新应当使用它，以免阻塞 UI 线程。如果没有取用该对象，`Refreshing` 状态会在 `RefreshRequested` 调用结束时终止。此状态下指示器完全可见，刷新动画开始播放。

### Peeking
当用户在内容处于不允许刷新的位置时发起下拉手势，就会进入这个状态。典型情形是：下拉开始时，子 ScrollViewer 在对应的下拉方向和滚动方向上并不处于偏移量 0 的位置。此时指示器保持隐藏，并且只有在松手之后，其状态才可能推进到 `Idle`。

## 另请参阅 {#see-also}

- [GitHub 上的 `RefreshContainer.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/PullToRefresh/RefreshContainer.cs)
