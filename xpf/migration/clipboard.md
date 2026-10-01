---
id: clipboard
title: 剪贴板
description: 了解 WPF 的剪贴板 API 在 XPF 中于 Windows、macOS 和 Linux 上的表现，包括文本、位图和自定义数据格式的支持情况。
doc-type: reference
---

## 概述 {#overview}

XPF 在所有平台上都实现了 WPF 的剪贴板 API（`System.Windows.Clipboard`）。不过与 WPF 在 Windows 上的原生实现相比，有几处差异值得留心。

## 基本用法 {#basic-usage}

标准的 WPF 剪贴板操作在 XPF 中都能用。你可以用 `Clipboard.SetText` 和 `Clipboard.GetText` 复制和读取文本，也可以通过 `DataObject` 处理更复杂的数据：

```csharp
// Text
Clipboard.SetText("Hello, World!");
string text = Clipboard.GetText();

// Data object
var data = new DataObject();
data.SetData(DataFormats.Text, "Hello");
Clipboard.SetDataObject(data);
```

读取之前，你也可以先查一下剪贴板里有没有某种格式：

```csharp
if (Clipboard.ContainsText())
{
    string text = Clipboard.GetText();
}
```

## 位图支持 {#bitmap-support}

自 XPF 1.6.0 起，支持把位图复制到剪贴板以及从剪贴板读取位图：

```csharp
// Copy bitmap to clipboard
Clipboard.SetImage(myBitmapSource);

// Retrieve bitmap from clipboard
BitmapSource image = Clipboard.GetImage();
```

在 macOS 上，用系统快捷键（Cmd+Shift+Ctrl+3）截的图可能采用与 WPF 惯例不同的像素格式。XPF 1.6.0 及以上会自动把它们转码成兼容的格式。

## 自定义数据格式 {#custom-data-formats}

自定义剪贴板数据格式在同一进程内可用。若要跨进程传递自定义数据，XPF 会把你的数据序列化成字符串，所以请确保你的自定义类型是可序列化的：

```csharp
var data = new DataObject();
data.SetData("MyCustomFormat", mySerializableObject);
Clipboard.SetDataObject(data);
```

读取自定义数据时，请用 `Clipboard.GetDataObject` 并以同样的格式字符串调用 `GetData`：

```csharp
IDataObject clipboardData = Clipboard.GetDataObject();
if (clipboardData?.GetDataPresent("MyCustomFormat") == true)
{
    var result = clipboardData.GetData("MyCustomFormat");
}
```

## STA 线程（Windows） {#sta-threading-windows}

在 Windows 上，剪贴板操作走 COM，要求主线程标记为 STA。若你遇到消息为 `CoInitialize was not called` 的 `COMException`，请确认入口点带有 `[STAThread]` 特性：

```csharp
[STAThread]
static void Main(string[] args)
{
    // Your application startup
}
```

另一个办法是采用[自定义初始化](/xpf/configuration/customizing-initialization)，它会自动处理好 STA 线程。

## 平台差异 {#platform-differences}

下表汇总了剪贴板各项功能在各平台上的支持情况：

| 特性 | Windows | macOS | Linux |
|---|---|---|---|
| Text | Supported | Supported | Supported |
| Bitmap | Supported (1.6.0+) | Supported (1.6.0+) | Supported (1.6.0+) |
| 自定义格式（同一进程） | Supported | Supported | Supported |
| 自定义格式（跨进程） | Supported (1.6.0+) | Supported (1.6.0+) | Supported (1.6.0+) |
| `Clipboard.Flush()` | Supported | 无效果 | Supported (X11) |

`Clipboard.Flush()` 会把剪贴板数据持久化，这样应用关掉之后内容仍在。在不支持 flush 的平台上，该方法什么也不做。

## 另请参阅 {#see-also}

- [已知差异](/xpf/migration/known-differences)
- [定制初始化](/xpf/configuration/customizing-initialization)
- [疑难排查](/xpf/troubleshooting)
