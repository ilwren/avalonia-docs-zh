---
id: drag-and-drop-how-to
title: "操作指南：实现拖放"
description: 在 Avalonia 中发起拖拽、处理放下、给出视觉反馈，以及接收拖入的文件。
doc-type: how-to
---

本指南介绍拖放的常见场景：发起拖拽、处理放下、给出视觉反馈，以及接收拖入的文件。

## 接收拖入的文件 {#accepting-dropped-files}

最常见的拖放场景，就是接收用户从操作系统文件管理器里拖过来的文件。

### XAML 配置 {#xaml-setup}

在目标元素上把 `DragDrop.AllowDrop` 设为 `True`，即可允许放下：

```xml
<Border Background="#F3F4F6" Padding="40"
        DragDrop.AllowDrop="True">
    <TextBlock Text="Drop files here"
               HorizontalAlignment="Center" VerticalAlignment="Center" />
</Border>
```

### 代码隐藏中的处理程序 {#code-behind-handler}

为 `DragOver`（表明你接受哪些效果）和 `Drop`（处理放下的数据）注册处理程序：

```csharp
public MainWindow()
{
    InitializeComponent();

    DragDrop.AddDropHandler(this, OnDrop);
    DragDrop.AddDragOverHandler(this, OnDragOver);
}

private void OnDragOver(object? sender, DragEventArgs e)
{
    // Accept file drops only; reject everything else
    e.DragEffects = e.DataTransfer.Contains(DataFormat.File)
        ? DragDropEffects.Copy
        : DragDropEffects.None;
}

private void OnDrop(object? sender, DragEventArgs e)
{
    if (e.DataTransfer.TryGetFiles() is { } files)
    {
        foreach (var file in files)
        {
            var path = file.Path.LocalPath;
            // Process the file
        }
    }
}
```

你在 `e.DragEffects` 中设的值同时也决定了光标形状，好让用户明白放下之后会发生什么：

| DragDropEffects | 光标 | 含义 |
|---|---|---|
| `None` | 禁止放下光标 | 不允许放下。 |
| `Copy` | 复制光标（+） | 项目将被复制。 |
| `Move` | 移动光标 | 项目将被移动。 |
| `Link` | 链接光标 | 将创建一个链接或快捷方式。 |

:::tip
请务必在 `DragOver` 处理程序中设置 `e.DragEffects`。否则即便你的控件本可接收，平台也可能显示「禁止放下」的光标。
:::

## 接收拖入的文本 {#accepting-dropped-text}

你也可以接收纯文本的放下操作，用 `TryGetText()` 取出字符串值：

```csharp
private void OnDrop(object? sender, DragEventArgs e)
{
    if (e.DataTransfer.TryGetText() is { } text)
    {
        // Use the dropped text
        ViewModel.Content = text;
    }
}
```

## 发起拖拽操作 {#initiating-a-drag-operation}

要从你的控件（比如某个列表项）发起拖拽，请在指针按下的处理程序中调用 `DragDrop.DoDragDropAsync`：

```csharp
private async void OnPointerPressed(object? sender, PointerPressedEventArgs e)
{
    if (sender is not Control control) return;

    var dragData = new DataTransfer();
    dragData.Add(DataTransferItem.CreateText("Dragged item text"));

    var result = await DragDrop.DoDragDropAsync(e, dragData, DragDropEffects.Copy | DragDropEffects.Move);

    if (result == DragDropEffects.Move)
    {
        // Item was moved, remove from source
    }
}
```

:::warning
别在每次 `PointerPressed` 事件里都发起拖拽。应当加一个最小距离阈值，或者等到 `PointerMoved` 再确认用户想拖而不是想点。
:::

:::note
不要释放你传给 `DoDragDropAsync` 的 `DataTransfer`，也不要在 `using` 语句中创建它。拖拽操作结束时 Avalonia 会自动释放它。
:::

## 在两个列表之间拖拽 {#drag-between-lists}

有个常见套路是在两个列表控件之间拖动项目：一个处理程序负责从源头发起拖拽，另一个负责在目标上接收放下。

这两个处理程序共用一种自定义数据格式。由于被拖的项目是个视图模型、从不离开你的应用，你可以把它做成进程内格式：

```csharp
private static readonly DataFormat<ItemViewModel> ItemFormat =
    DataFormat.CreateInProcessFormat<ItemViewModel>("my-app-item");
```

### 源列表 {#source-list}

```csharp
private async void SourceList_PointerPressed(object? sender, PointerPressedEventArgs e)
{
    if (sender is ListBox listBox && listBox.SelectedItem is ItemViewModel item)
    {
        var data = new DataTransfer();
        data.Add(DataTransferItem.Create(ItemFormat, item));

        var result = await DragDrop.DoDragDropAsync(e, data, DragDropEffects.Move);

        if (result == DragDropEffects.Move)
            ViewModel.SourceItems.Remove(item);
    }
}
```

### 目标列表 {#target-list}

在放下的处理程序中取出你的自定义对象，并把它加进目标集合：

```csharp
private void TargetList_Drop(object? sender, DragEventArgs e)
{
    if (e.DataTransfer.TryGetValue(ItemFormat) is { } item)
    {
        ViewModel.TargetItems.Add(item);
        e.DragEffects = DragDropEffects.Move;
    }
}
```

## 拖拽过程中的视觉反馈 {#visual-feedback-during-drag}

给出视觉反馈能帮用户看清哪里可以放下。下面这个例子会在用户把东西拖到放置目标上方时改变其外观——这里假定目标是在 XAML 中声明、并带有 `x:Name="DropZone"` 和 `DragDrop.AllowDrop="True"` 的 `Border`：

```csharp
public MainWindow()
{
    InitializeComponent();

    DragDrop.AddDragEnterHandler(DropZone, (s, e) =>
    {
        DropZone.BorderBrush = Brushes.Blue;
        DropZone.BorderThickness = new Thickness(2);
    });

    DragDrop.AddDragLeaveHandler(DropZone, (s, e) =>
    {
        DropZone.BorderBrush = Brushes.Transparent;
        DropZone.BorderThickness = new Thickness(0);
    });

    DragDrop.AddDropHandler(DropZone, (s, e) =>
    {
        DropZone.BorderBrush = Brushes.Transparent;
        DropZone.BorderThickness = new Thickness(0);
        // Handle drop...
    });
}
```

请把处理程序挂在放置区本身上，而不是整个窗口上。否则用户在窗口任意位置拖动时都会触发高亮。

:::tip
记得在 `DragLeave` 和 `Drop` 两个处理程序里都重置视觉状态。若只在 `DragLeave` 中重置，用户真的放下之后高亮就会一直留着。
:::

## 自定义数据格式 {#custom-data-formats}

若要传输你自己的数据，请创建一个带类型的 `DataFormat<T>`，并在拖拽源和放置目标两边复用它：

```csharp
// Set
var data = new DataTransfer();
data.Add(DataTransferItem.Create(MyTypeFormat, myObject));

// Get
if (e.DataTransfer.TryGetValue(MyTypeFormat) is { } obj)
{
    // Use obj
}
```

`MyTypeFormat` 是一个静态字段，由 `DataFormat` 方法创建，例如 `DataFormat.CreateInProcessFormat<MyType>("my-app-type")`。可用方法和支持的数据类型清单，请参阅 [`DataFormat<T>` API 参考](/api/avalonia/input/dataformat-1)。

:::caution
传给 `CreateStringApplicationFormat` 和 `CreateBytesApplicationFormat` 的标识只能包含 ASCII 字母、数字、点号（`.`）和连字符（`-`），不接受 `application/x-my-type` 这类 MIME 风格的标识。
:::

## 边界情况与排查 {#edge-cases-and-troubleshooting}

- **放下的处理程序没触发：**确认目标元素上的 `DragDrop.AllowDrop` 已设为 `True`，并且你的 `DragOver` 处理程序把 `e.DragEffects` 设成了 `None` 以外的值。
- **单击就开始拖拽：**在调用 `DoDragDropAsync` 之前加一个距离阈值。否则随手一点就会触发拖拽，容易把用户搞糊涂。
- **自定义数据跨进程后丢失：**用 `CreateInProcessFormat` 创建的格式，其数据从不离开当前进程。要把自定义数据拖到另一个进程，请先把它序列化成 `string` 或 `byte[]`，并改用应用格式或平台格式。
- **多种数据格式：**对同一个 `DataTransferItem` 多次调用 `Set`，每种格式一次，然后把这个项目加入 `DataTransfer`。这样放置目标就能从中挑出自己支持的最丰富的格式。
- **拖拽途中数据被释放：**不要释放你传给 `DoDragDropAsync` 的 `DataTransfer`，拖拽结束时 Avalonia 会负责释放。

## 平台须知 {#platform-notes}

| 平台 | 支持程度 | 注释支持情况 |
|---|---|---|
| Windows | Full | 从资源管理器拖入文件、跨应用拖放文本和位图，以及应用内的自定义格式，全都能用。 |
| macOS | Full | 支持从 Finder 拖入文件。系统的拖拽光标会遵循 `DragDropEffects`。 |
| Linux (X11/Wayland) | Full | 行为与 Windows 一致。各家 Wayland 合成器在光标渲染上可能略有差异。 |
| Browser (WebAssembly) | Limited | 多数浏览器都支持从操作系统文件管理器拖入文件。但应用内元素之间的拖动需要自行实现，因为指针捕获由浏览器接管。 |
| iOS / Android | 不支持 | 无法使用拖放。想实现类似功能，可以考虑长按手势或列表重排的交互方式。 |

## 另请参阅 {#see-also}

- [拖放](/docs/input-interaction/drag-and-drop)：拖放机制的概念性介绍。
- [手势](/docs/input-interaction/gestures)：触摸与指针的手势识别器。
- [存储提供程序](/docs/services/storage/storage-provider)：与 `IStorageItem` 搭配使用的文件访问 API。
