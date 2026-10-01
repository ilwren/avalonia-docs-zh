---
id: drag-and-drop
title: 拖放
---

Avalonia 支持拖放操作，可在控件之间、或在你的应用与操作系统之间传递数据。拖放机制用 [`DragDrop`](/api/avalonia/input/dragdrop) 静态类和 [`DataTransfer`](/api/avalonia/input/datatransfer) 类型来管理操作过程中的数据。

## 让目标接受放下 {#enabling-drop-on-a-target}

要接收放下的内容，元素的 `DragDrop.AllowDrop` 附加属性必须设为 `True`。此外，你还得为拖放事件挂上处理程序：

<Tabs>

<TabItem value="xaml" label="XAML">

```xml
<Border DragDrop.AllowDrop="True"
        Background="LightGray" Padding="40"
        DragDrop.DragEnter="OnDragEnter"
        DragDrop.DragLeave="OnDragLeave"
        DragDrop.DragOver="OnDragOver"
        DragDrop.Drop="OnDrop">
    <TextBlock Text="Drop files here" HorizontalAlignment="Center" />
</Border>
```

</TabItem>

<TabItem value="cs" label="Code-behind">

```csharp
using Avalonia.Controls;
using Avalonia.Input;

namespace MyApp.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }
    private void OnDragEnter(object? sender, DragEventArgs e){}
    private void OnDragLeave(object? sender, DragEventArgs e){}
    private void OnDragOver(object? sender, DragEventArgs e){}
    private void OnDrop(object? sender, DragEventArgs e){}
}
```

</TabItem>

</Tabs>

## 拖放事件 {#drag-and-drop-events}

| 事件 | 触发时机 |
|---|---|
| `DragEnter` | 拖拽过程中指针进入目标元素。 |
| `DragLeave` | 拖拽过程中指针离开目标元素。 |
| `DragOver` | 拖拽过程中指针在目标元素上移动，会持续触发。 |
| `Drop` | 用户在目标元素上松开指针。 |

所有事件都提供一个 `DragEventArgs`，其中有这些属性：

| 属性 | 说明 |
|---|---|
| `DataTransfer` | 装着被拖数据的 `IDataTransfer` 对象。 |
| `DragEffects` | 允许的以及请求的拖拽效果。设置它来表明你的目标接受什么。 |
| `KeyModifiers` | 当前按下的键盘修饰键（Ctrl、Shift、Alt）。 |
| `GetPosition(Visual)` | 返回指针相对某个视觉元素的位置。 |

## 处理放下事件 {#handling-drop-events}

```csharp
private void OnDragOver(object? sender, DragEventArgs e)
{
    // Check if we can accept the data
    if (e.DataTransfer.Formats.Contains(DataFormat.File))
    {
        e.DragEffects = DragDropEffects.Copy;
    }
    else
    {
        e.DragEffects = DragDropEffects.None;
    }
}

private void OnDrop(object? sender, DragEventArgs e)
{
    if (e.DataTransfer.Formats.Contains(DataFormat.File))
    {
        var files = e.DataTransfer.TryGetFiles();
        if (files != null)
        {
            foreach (var file in files)
            {
                // Process each dropped file
                Debug.WriteLine($"Dropped: {file.Name}");
            }
        }
    }
}
```

## DragDropEffects

`DragDropEffects` 这个标志枚举表示允许哪些操作：

| 值 | 说明 |
|---|---|
| `None` | 放置目标不接受这份数据。 |
| `Copy` | 数据被复制到目标处。 |
| `Move` | 数据被移动到目标处。 |
| `Link` | 创建一个指向原数据的链接。 |

在 `DragOver` 中设置 `e.DragEffects` 以控制光标反馈，在 `Drop` 中设置它以表明操作的结果。

## 发起拖拽操作 {#starting-a-drag-operation}

要从你的控件发起拖放操作，请在某个指针事件中调用 `DragDrop.DoDragDropAsync`，并创建一个装着待拖数据的 `DataTransfer` 对象：

```csharp
private async void OnPointerPressed(object? sender, PointerPressedEventArgs e)
{
    var dragData = new DataTransfer();
    dragData.Add(DataTransferItem.CreateText("Hello from drag!"));

    var result = await DragDrop.DoDragDropAsync(
        e,
        dragData,
        DragDropEffects.Copy | DragDropEffects.Move);

    // result indicates what the drop target did
    if (result == DragDropEffects.Move)
    {
        // Remove the source data since it was moved
    }
}
```

:::info
`DoDragDropAsync` 是异步的。用户完成或取消拖拽操作后，该方法才会返回，返回值表明放置目标最终施加了哪种效果。
:::

## DataTransfer 与数据格式 {#datatransfer-and-data-formats}

`DataTransfer` 类是个可变的拖放数据容器。标准格式请使用 `DataFormat` 的静态属性：

| 格式 | 类型 | 说明 |
|---|---|---|
| `DataFormat.Text` | `string` | 纯文本。 |
| `DataFormat.Bitmap` | `Bitmap` | 位图图像数据。 |
| `DataFormat.File` | `IStorageItem` | 文件系统项目。 |

你也可以创建自定义格式：

```csharp
var myFormat = DataFormat.CreateStringApplicationFormat("myapp-item");
```

### 写入数据 {#setting-data}

```csharp
var data = new DataTransfer();
data.Add(DataTransferItem.Create(DataFormat.Text, "Some text"));
```

### 读取数据 {#reading-data}

```csharp
// In a DragOver or Drop handler
if (e.DataTransfer.Formats.Contains(DataFormat.Text))
{
    var text = e.DataTransfer.TryGetText();
}

if (e.DataTransfer.Formats.Contains(DataFormat.File))
{
    var files = e.DataTransfer.TryGetFiles();
}
```

## 拖拽过程中的视觉反馈 {#visual-feedback-during-drag}

用 `DragEnter` 和 `DragLeave` 事件给出视觉反馈：

```csharp
private void OnDragEnter(object? sender, DragEventArgs e)
{
    if (sender is Border border)
    {
        border.BorderBrush = Brushes.Blue;
        border.BorderThickness = new Thickness(2);
    }
}

private void OnDragLeave(object? sender, DragEventArgs e)
{
    if (sender is Border border)
    {
        border.BorderBrush = null;
        border.BorderThickness = new Thickness(0);
    }
}
```

## 完整示例 {#complete-example}

下面这个例子做了一个既收文本又收文件的放置区：

<Tabs>

<TabItem value="xaml" label="XAML">

```xml
<Border x:Name="DropZone"
        DragDrop.AllowDrop="True"
        Background="#F5F5F5" CornerRadius="8"
        Padding="40" Margin="20"
        BorderBrush="DarkGray" BorderThickness="1">
    <StackPanel Spacing="8" HorizontalAlignment="Center">
        <TextBlock Text="Drop text or files here"
                   HorizontalAlignment="Center" />
        <TextBlock x:Name="StatusText" Foreground="Gray"
                   HorizontalAlignment="Center" />
    </StackPanel>
</Border>
```

</TabItem>

<TabItem value="cs" label="Code-behind">

```csharp
using System.Linq;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Media;

namespace MyApp.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        DragDrop.AddDragOverHandler(DropZone, OnDragOver);
        DragDrop.AddDropHandler(DropZone, OnDrop);
        DragDrop.AddDragEnterHandler(DropZone, OnDragEnter);
        DragDrop.AddDragLeaveHandler(DropZone, OnDragLeave);
    }

    private void OnDragEnter(object? sender, DragEventArgs e)
    {
        DropZone.Background = Brushes.LightBlue;
    }

    private void OnDragLeave(object? sender, DragEventArgs e)
    {
        DropZone.Background = new SolidColorBrush(Color.Parse("#F5F5F5"));
    }

    private void OnDragOver(object? sender, DragEventArgs e)
    {
        e.DragEffects = e.DataTransfer.Formats.Contains(DataFormat.Text)
                     || e.DataTransfer.Formats.Contains(DataFormat.File)
            ? DragDropEffects.Copy
            : DragDropEffects.None;
    }

    private void OnDrop(object? sender, DragEventArgs e)
    {
        DropZone.Background = new SolidColorBrush(Color.Parse("#F5F5F5"));

        if (e.DataTransfer.Formats.Contains(DataFormat.Text))
        {
            StatusText.Text = $"Dropped text: {e.DataTransfer.TryGetText()}";
        }
        else if (e.DataTransfer.Formats.Contains(DataFormat.File))
        {
            var files = e.DataTransfer.TryGetFiles();
            if (files != null)
            {
                StatusText.Text = $"Dropped {files.Count()} file(s)";
            }
        }
    }
}
```

</TabItem>

</Tabs>

## 在 XAML 中处理还是在代码中处理 {#handling-events-in-xaml-vs-code}

拖放事件是 `DragDrop` 类上的附加事件。你既可以在 XAML 中用事件特性语法处理（如上所示），也可以在代码里显式注册：

```csharp
// Register in code
DragDrop.AddDropHandler(myBorder, OnDrop);

// Remove handler
DragDrop.RemoveDropHandler(myBorder, OnDrop);
```

`DragDrop` 类为每个事件都提供了 `Add*Handler` 和 `Remove*Handler` 静态方法：`DragEnter`、`DragLeave`、`DragOver` 和 `Drop`。

## 另请参阅 {#see-also}

- [指针事件](/docs/input-interaction/pointer)：检测指针移动以便发起拖拽。
- [剪贴板](/docs/services/clipboard)：通过剪贴板共享数据。
- [存储提供程序](/docs/services/storage/storage-provider)：处理文件与文件夹。
