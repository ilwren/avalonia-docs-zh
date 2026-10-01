---
id: clipboard-how-to
title: "操作指南：使用剪贴板"
description: 用 Avalonia 剪贴板 API 复制和粘贴文本、图片与自定义数据。
doc-type: how-to
---

本指南演示如何用 Avalonia 剪贴板 API 复制和粘贴文本、图片与自定义数据。你将学到如何拿到剪贴板引用、传输常见数据类型、注册自定义格式，以及挂上键盘快捷键。

## 获取剪贴板 {#getting-the-clipboard}

你通过 `TopLevel` 访问剪贴板。在代码隐藏文件中，可以对树中任意视觉元素调用 `GetTopLevel`：

```csharp
var clipboard = TopLevel.GetTopLevel(this)?.Clipboard;
```

若需要在视图模型里访问剪贴板，请通过构造函数注入 `IClipboard`，这样视图模型依然可测试：

```csharp
public class MainViewModel
{
    private readonly IClipboard? _clipboard;

    public MainViewModel(IClipboard? clipboard)
    {
        _clipboard = clipboard;
    }
}
```

:::tip
所有剪贴板方法都是异步的，因为底层平台 API 可能需要用户授权或跨进程通信。记得 `await` 这些调用，并处理可能返回的 `null`。
:::

## 把文本复制到剪贴板 {#copy-text-to-the-clipboard}

用 `SetTextAsync` 把一个纯文本字符串放到剪贴板上：

```csharp
[RelayCommand]
private async Task CopyText()
{
    var clipboard = TopLevel.GetTopLevel(this)?.Clipboard;
    if (clipboard is not null)
    {
        await clipboard.SetTextAsync("Hello, clipboard!");
    }
}
```

## 从剪贴板粘贴文本 {#paste-text-from-the-clipboard}

用 `TryGetTextAsync` 读取纯文本。没有可用文本时，该方法返回 `null`：

```csharp
[RelayCommand]
private async Task PasteText()
{
    var clipboard = TopLevel.GetTopLevel(this)?.Clipboard;
    if (clipboard is not null)
    {
        var text = await clipboard.TryGetTextAsync();
        if (text is not null)
        {
            Content = text;
        }
    }
}
```

## 检查剪贴板的内容 {#check-clipboard-content}

粘贴之前，你可以先查询剪贴板当前持有哪些格式。当你的应用支持多种数据类型、希望挑出最合适的那一种时，这招很有用：

```csharp
var clipboard = TopLevel.GetTopLevel(this)?.Clipboard;
if (clipboard is not null)
{
    using var data = await clipboard.TryGetDataAsync();
    if (data is not null)
    {
        if (data.Formats.Contains(DataFormat.Text))
        {
            var text = await data.TryGetTextAsync();
            // Use the text value
        }
    }
}
```

:::note
`TryGetDataAsync` 返回的 `DataTransfer` 对象是可释放的。把它放进 `using` 语句里，好让平台资源及时归还。
:::

## 把图片复制到剪贴板 {#copy-an-image-to-the-clipboard}

加载一个 `Bitmap` 并把它传给 `SetBitmapAsync`：

```csharp
var clipboard = TopLevel.GetTopLevel(this)?.Clipboard;
if (clipboard is not null)
{
    var bitmap = new Bitmap("assets/photo.png");
    await clipboard.SetBitmapAsync(bitmap);
}
```

## 从剪贴板粘贴图片 {#paste-an-image-from-the-clipboard}

用 `TryGetBitmapAsync` 取回图片。没有可用图片数据时，该方法返回 `null`：

```csharp
var clipboard = TopLevel.GetTopLevel(this)?.Clipboard;
if (clipboard is not null)
{
    var bitmap = await clipboard.TryGetBitmapAsync();
    if (bitmap is not null)
    {
        MyImage.Source = bitmap;
    }
}
```

## 复制自定义数据 {#copy-custom-data}

用 `DataTransfer` 和 `DataTransferItem` 把结构化数据放到剪贴板上。先用一个唯一标识创建应用作用域的格式，再往 `DataTransferItem` 里填入一种或多种表示形式。顺带加上 `DataFormat.Text` 条目，就能给其他应用留一个纯文本的退路：

```csharp
var myFormat = DataFormat.CreateBytesApplicationFormat("mycompany-myapp-mydata");

var item = new DataTransferItem();
item.Set(DataFormat.Text, "Plain text fallback");
item.Set(myFormat, mySerializedBytes);

var data = new DataTransfer();
data.Add(item);

await clipboard.SetDataAsync(data);
```

## 粘贴自定义数据 {#paste-custom-data}

要把自定义格式读回来，创建同样的 `DataFormat` 并调用 `TryGetValueAsync`：

```csharp
var myFormat = DataFormat.CreateBytesApplicationFormat("mycompany-myapp-mydata");

using var data = await clipboard.TryGetDataAsync();
if (data is not null)
{
    var bytes = await data.TryGetValueAsync(myFormat);
    if (bytes is not null)
    {
        // Deserialize the byte array into your object
    }
}
```

:::tip
复制端和粘贴端必须使用同一个格式标识字符串（`"mycompany-myapp-mydata"`）。剪贴板正是靠这个标识把数据与你的应用格式对上号的。
:::

## 键盘快捷键 {#keyboard-shortcuts}

在 `TextBox`、`TextPresenter` 这类内置文本控件中，标准剪贴板快捷键（`Ctrl+C`、`Ctrl+V`、`Ctrl+X`）自动生效。对于自定义控件，则需要你显式地把按键手势绑定到自己的命令上：

```xml
<UserControl.KeyBindings>
    <KeyBinding Gesture="Ctrl+C" Command="{Binding CopyCommand}" />
    <KeyBinding Gesture="Ctrl+V" Command="{Binding PasteCommand}" />
    <KeyBinding Gesture="Ctrl+X" Command="{Binding CutCommand}" />
</UserControl.KeyBindings>
```

在 macOS 上，只要你在 XAML 中写了 `Ctrl` 修饰键，Avalonia 就会自动把 `Cmd+C`、`Cmd+V`、`Cmd+X` 映射过去，无需再写平台相关的绑定。

## 平台须知 {#platform-notes}

剪贴板 API 在所有 Avalonia 目标平台上都可用，但并非每个平台都支持全部数据类型。下表汇总了当前的支持情况：

| 平台 | 文本 | 图片 | 文件 | 自定义格式 |
|---|---|---|---|---|
| Windows | Yes | Yes | Yes | Yes |
| macOS | Yes | Yes | Yes | Yes |
| Linux | Yes | Yes | 因桌面环境而异 | Yes |
| Browser (WASM) | 支持（需要授权） | Yes | No | Limited |
| iOS | Yes | Yes | No | Limited |
| Android | Yes | 只读 | No | Limited |

在 **Browser/WASM** 上，你的应用首次调用剪贴板方法时，浏览器可能会向用户索要剪贴板权限。你的代码应当妥善处理权限被拒、调用返回 `null` 的情形。

在 **Linux** 上，文件剪贴板的支持取决于桌面环境及其剪贴板管理器。文本和图片操作在 GNOME、KDE 等主流环境下都能稳定工作。

## 另请参阅 {#see-also}

- [剪贴板服务](/docs/services/clipboard)
- [拖放操作指南](/docs/how-to/drag-and-drop-how-to)
- [Hotkeys](/docs/input-interaction/keyboard-and-hotkeys)
