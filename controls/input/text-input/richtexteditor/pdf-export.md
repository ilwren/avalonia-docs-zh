---
id: pdf-export
title: PDF Export
doc-type: guide
tags:
 - avalonia pro
 - avalonia enterprise
---

`PdfSerializer` 把文档写成矢量 PDF 1.7。它位于 `Avalonia.Controls.Documents.Serialization.Pdf` 包中，命名空间为 `Avalonia.Controls.Documents.Serialization.Pdf`。

它只写不读：`CanWrite` 为 true，`CanRead` 为 false，`Deserialize` 会抛出 `NotSupportedException`。导出 PDF 时的分页遵循与分页视图相同的规则，因此屏幕上的纸面和文件中的页面断在同样的位置。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 导出文档 {#exporting-a-document}

```csharp
using Avalonia.Controls.Documents.Serialization.Pdf;

await using var stream = File.Create(path);
document.Save(stream, new PdfSerializer());
```

`FlowDocument.Save` 负责取快照并交给序列化器。`SaveAsync` 做同样的事，只是把写出放到线程池上跑。快照仍在调用线程上获取，因为读取文档必须由拥有它的那个线程来做：

```csharp
await document.SaveAsync(stream, new PdfSerializer(options));
```

序列化器的契约是同步的，所以没有可等待的异步版本。要让 UI 线程腾出手来，可以先取快照再把活儿挪走：

```csharp
var snapshot = document.CreateSnapshot();   // on the UI thread
await Task.Run(() => new PdfSerializer(options).Serialize(snapshot, stream, cancellationToken),
               cancellationToken);
```

一份快照可以喂给多个序列化器。对于「保存为所有格式」这类命令（同时写出 PDF 和 DOCX），这么做很划算。

## 在非 UI 线程上运行 {#running-off-the-ui-thread}

导出流水线不依赖 UI：它直接消费 `DocumentSnapshot`，不创建任何控件，也不需要调度器，从不依赖实时布局。

话虽如此，PDF 导出仍需要一个已初始化的 Avalonia 平台，用于字体管理器和文本排版器。完全没做 Avalonia 初始化的裸控制台进程无法导出。

`PdfSerializer` 可安全地并发使用，其选项在构造时就已固定。

## 选项 {#options}

| 属性 | 默认值 | 含义 |
|---|---|---|
| `PageSize` | `null` | 页面尺寸，单位为设备无关像素。`Null` 表示采用文档固定的 `PageWidth` 和 `PageHeight`，再回落到 A4。 |
| `Margins` | `null` | 页边距。`Null` 表示采用文档的 `PagePadding`，再回落到 2 厘米。 |
| `FontEmbedding` | `Full` | 见下文。 |
| `Title` | `null` | 写入 PDF 元数据。 |
| `Author` | `null` | 写入 PDF 元数据。 |
| `Subject` | `null` | 写入 PDF 元数据。 |
| `Keywords` | `null` | 写入 PDF 元数据。 |
| `Language` | `null` | BCP 47 语言标签，写作文档目录的语言。 |
| `Deterministic` | `false` | 使用固定的创建日期和文件 ID，而非当前时间和随机 ID，以便产出逐字节稳定的结果。 |
| `Diagnostics` | `null` | 用于上报可接受的保真度损失的回调。见下文。 |
| `Document` | new | 各序列化器共用的选项。 |

:::note
页面相关的属性都以设备无关像素（1/96 英寸）为单位，而非磅。例如 US Letter 是 816 x 1056 设备无关像素。请使用 `PageSizes` 及其换算辅助方法，别写字面量。
:::

`PageSize` 在两个方向上都必须是有限的正值，否则会被直接拒绝，而不是产出一个任何阅读器都打不开的文件。无穷大或负的 `Margins` 会回落到 2 厘米的默认值。

显式设置 `PageSize` 或 `Margins` 相当于启用「统一纸张」覆盖。[有独立页面几何的小节](/controls/input/text-input/richtexteditor/pagination#per-section-page-setup)依然会另起一页，但会遵循统一尺寸，而拿不到它所要求的页面设置。

若某张图片因 `Document` 的 `MaxImageBytes` 或 `ImageEncodingPolicy` 而未进入 PDF 导出，它的布局盒子仍会保留，分页结果不变。`ExportMode` 对此没有影响。

```csharp
using Avalonia;
using Avalonia.Controls.Documents;
using Avalonia.Controls.Documents.Serialization;
using Avalonia.Controls.Documents.Serialization.Pdf;

var options = new PdfSerializerOptions
{
    PageSize = PageSizes.Letter,
    Margins = new Thickness(PageSizes.Inches(1)),
    FontEmbedding = PdfFontEmbedding.Full,
    Title = "Quarterly Report",
    Author = "Finance",
    Language = "en-US",
    Deterministic = true,
    Diagnostics = diagnostic => log.Warning(diagnostic.Message),
    Document = new DocumentSerializerOptions
    {
        MaxImageBytes = 4 * 1024 * 1024,
        ImageEncodingPolicy = ImageEncodingPolicy.PreserveEncodedOnly,
    },
};
```

## Fonts

| `PdfFontEmbedding` | 行为 |
|---|---|
| `Full` (default) | 为文档用到的每一种字体嵌入完整的字体文件。 |
| `Subset` | 尚未实现，行为等同于 `Full`。 |
| `None` | 不嵌入任何字体程序，交由阅读器自行替换。字体度量仍会写出，因此布局大体得以保留 |

被嵌入的字型会写成一个 Type0 字体，带完整文件嵌入（`FontFile2`，CFF 字体则为 `FontFile3`）、一个 `W` 宽度数组和一张 `ToUnicode` CMap。

### 字体无法嵌入时 {#when-a-font-cannot-be-embedded}

下列情况下字体程序不会进入文件：

- `FontEmbedding` is `None`
- 该字型没有可读的流
- 它是 TrueType 集合，或
- 它的 `OS/2` fsType 禁止嵌入。

此时导出不会失败，也不会悄悄产出读不了的页面。字型会写成**简单字体**：范围之外的字符用一个 `Differences` 数组表示，并带有自己的 `Widths` 数组和一张单字节的 `ToUnicode` CMap。阅读器会替换成本地字型，文字照样渲染，也仍能按文档原文选择和复制。

简单字体只能承载 255 个字符码。若某个未嵌入字体的文本需要的字符超出这个数，超出的字符会从页面上被丢弃，并通过诊断信息告知。

彩色字体可以嵌入，但在阅读器中会渲染成单色轮廓。

可变字体按其默认实例渲染。

## Diagnostics

上述每一种降级都通过可选的 `Diagnostics` 回调上报，且仅通过它上报。回调为 null 时，导出不会发出任何提示。

```csharp
var losses = new List<PdfDiagnostic>();

var serializer = new PdfSerializer(new PdfSerializerOptions
{
    Diagnostics = losses.Add,
});

serializer.Serialize(snapshot, stream);

foreach (var loss in losses)
    log.Warning("{Kind}: {Message}", loss.Kind, loss.Message);
```

| `PdfDiagnosticKind` | 含义 |
|---|---|
| `FontNotEmbedded` | 字体程序缺失，阅读器必须替换字体。文字仍可选择，度量也得以保留。 |
| `FontFidelity` | 字体已嵌入，但无法完全一致地呈现，比如彩色字形数据被忽略，或可变字体按默认实例渲染。 |
| `EncodingExhausted` | 某个未嵌入字体的文本所需的字符码超过了简单字体能提供的 255 个，超出的字符会从页面上被丢弃。 |

`PdfDiagnostic` 是一个由 `Kind` 和 `Message` 组成的 `readonly record struct`，其中 `ToString()` 是消息内容。该回调在执行导出的那个线程上调用，且早于任何字节写入目标流。

## 哪些内容会被导出 {#what-gets-exported}

- **文本：** 使用与编辑器相同的引擎进行排版。
- **块：** 包括列表、表格、小节、图片和超链接注释。
- **页眉页脚带：** 即页眉和页脚。会压缩页面正文的带，其导出效果与分页布局在屏幕上所显示的完全一致。
- **脚注：** 注释出现在其锚点所在页的底部、分隔线之下。注释主体内的超链接保留其注释信息。
- **分页：** 由显式的 `BreakPageBefore` 分页符、保持规则、孤行控制以及不可拆分的表格行共同决定。有独立页面设置的小节则按页获得各自的 `MediaBox`。

## 另请参阅 {#see-also}

- [分页](/controls/input/text-input/richtexteditor/pagination) —— 导出与分页视图共用的断页规则
- [页眉与页脚](/controls/input/text-input/richtexteditor/headers-and-footers) —— 每一页各自解析出的带
- [脚注](/controls/input/text-input/richtexteditor/footnotes) —— 位于锚点所在页底部的注释
- [线程安全](/controls/input/text-input/richtexteditor/thread-safety) —— 快照与后台工作
