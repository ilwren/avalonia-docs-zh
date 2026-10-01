---
id: document-viewer
title: Document Viewer
doc-type: how-to
tags:
 - avalonia pro
 - avalonia enterprise
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

用 `FlowDocumentScrollViewer` 展示富文本文档而不提供编辑。本指南涵盖环境准备、文档加载、样式、布局，以及常见的阅读器范式。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 何时使用 FlowDocumentScrollViewer {#when-to-use-flowdocumentscrollviewer}

有三个控件可以承载 `FlowDocument`：

| 控件 | 用途 | Selection / Copy | 插入符 | 撤销 | 开销 |
|---|---|---|---|---|---|
| `FlowDocumentScrollViewer` | 以单一连续栏的形式只读展示 | Yes | No | No | Low |
| `FlowDocumentPageViewer` | 以一页页独立纸面的形式只读展示 | Yes | No | No | Low |
| `RichTextEditor` | 可交互编辑 | Yes | Yes | Yes | Higher |
<br />

帮助面板、报表预览、文件浏览和只读摘要，都该用 `FlowDocumentScrollViewer`。它开箱即支持文本选择和复制到剪贴板（底层与编辑器用的是同一套 `TextViewMouse` / `TextViewKeyboard` 组件），但不提供插入符、编辑操作和撤销管理器。

当读者需要看到真正的「页」时就用 `FlowDocumentPageViewer`：打印预览、忠于分页的审阅、翻页与缩放。它派生自 `FlowDocumentScrollViewer`，并且与打印、PDF 导出共用同一套分页断行策略，因此三者的结果天生一致。

只有当你需要在本质只读的内容上提供插入符时（比如要放光标但不允许编辑），才用 `RichTextEditor` 搭配 `IsReadOnly="True"`。这会把整套编辑基础设施（插入符元素、撤销管理器、编辑组件）都牵扯进来。

两种阅读器都支持在页眉页脚带和脚注内部选择：按进页眉、页脚或注释区域，选区就会进入那个嵌套文档。

## 安装 {#installation}

```bash
# Core package (includes FlowDocument, FlowDocumentScrollViewer, PlainTextSerializer)
dotnet add package Avalonia.Controls.RichTextEditor

# Add serializers for the formats you need
dotnet add package Avalonia.Controls.Documents.Serialization.Rtf     # RTF
dotnet add package Avalonia.Controls.Documents.Serialization.Docx    # DOCX (Open XML)
dotnet add package Avalonia.Controls.Documents.Serialization.Xaml    # XAML round-trip
dotnet add package Avalonia.Controls.Documents.Serialization.Html    # HTML import (read only)
dotnet add package Avalonia.Controls.Documents.Serialization.Pdf     # PDF export (write only)
```

所有文档类型（`FlowDocument`、`Paragraph`、`RichRun` 等）以及 `FlowDocumentScrollViewer` 都映射到了 Avalonia 的默认 XML 命名空间（`https://github.com/avaloniaui`），不需要额外声明 `xmlns`。

## 最简 XAML 示例 {#minimal-xaml-example}

`FlowDocument` 是 `FlowDocumentScrollViewer` 的 `[Content]` 属性，因此可以直接写成子元素：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Document Viewer" Width="800" Height="600">

    <FlowDocumentScrollViewer Padding="20">
        <FlowDocument FontSize="14">
            <Paragraph FontSize="24" FontWeight="Bold">
                <RichRun Text="Welcome" />
            </Paragraph>
            <Paragraph>
                <RichRun Text="This document is displayed in a read-only viewer." />
            </Paragraph>
        </FlowDocument>
    </FlowDocumentScrollViewer>

</Window>
```

阅读器把一个虚拟化的 `TextViewBase` 包在 `ScrollViewer` 里。垂直滚动默认开启，水平滚动则关闭。

## 从文件加载文档 {#loading-documents-from-files}

### 异步加载（推荐） {#async-loading-preferred}

用 `FlowDocument.LoadAsync` 反序列化文件，再把结果赋给阅读器：

```csharp
await using var stream = File.OpenRead("report.rtf");
var document = await FlowDocument.LoadAsync(stream, new RtfSerializer());
viewer.Document = document;
```

`LoadAsync` 在线程池上解析，随后通过一次显式的调度器调用在 UI 线程上构建元素树。返回的 `FlowDocument` 可以立即显示。

:::info
`IDocumentSerializer` 是同步的。`LoadAsync` 和 `SaveAsync` 只是帮你把活儿挪出当前线程的便利封装，元素树仍必须在 UI 线程上构建——因为 `FlowDocument` 及其元素归属于构造它们的那个线程的调度器。

若你需要全程不碰 UI 线程，请用序列化器读出一个 `DocumentSnapshot`，再用 `TextDocument.FromSnapshot` 把它实体化。
:::

### 同步加载 {#synchronous-loading}

```csharp
using var stream = File.OpenRead("report.rtf");
viewer.Document = FlowDocument.Load(stream, new RtfSerializer());
```

`Load` 在调用线程上解析并构建，因此大文件更推荐异步加载。两个重载都接受一个可选的 `CancellationToken`。

### 选择序列化器 {#choosing-a-serializer}

按文件格式挑选序列化器：

| 扩展名 | 序列化器 | NuGet 包 | 方向 |
|---|---|---|---|
| `.rtf` | `RtfSerializer` | `Avalonia.Controls.Documents.Serialization.Rtf` | 可读可写 |
| `.docx` | `DocxSerializer` | `Avalonia.Controls.Documents.Serialization.Docx` | 可读可写 |
| `.xaml` / `.axaml` | `XamlSerializer` | `Avalonia.Controls.Documents.Serialization.Xaml` | 可读可写 |
| `.md` | `MarkdownSerializer` | `Avalonia.Controls.Markdown` | 可读可写 |
| `.html` | `HtmlSerializer` | `Avalonia.Controls.Documents.Serialization.Html` | 只读 |
| `.pdf` | `PdfSerializer` | `Avalonia.Controls.Documents.Serialization.Pdf` | 只写 |
| `.txt` | `PlainTextSerializer` | 已包含在 `Avalonia.Controls.Documents`（核心包）中 | 可读可写 |
<br />

每个序列化器都通过 `CanRead` 和 `CanWrite` 表明自己的读写方向，格式选择器可据此过滤列表。框架没有内置格式注册表，具体如何发现由应用自行决定。`MarkdownSerializer` 接受任意可读流，所以把它放在最后尝试。

一个把扩展名映射到序列化器的辅助方法：

```csharp
static IDocumentSerializer GetSerializer(string path)
{
    return Path.GetExtension(path).ToLowerInvariant() switch
    {
        ".rtf" => new RtfSerializer(),
        ".docx" => new DocxSerializer(),
        ".xaml" or ".axaml" => new XamlSerializer(),
        _ => new PlainTextSerializer()
    };
}
```

### 从嵌入资源加载 {#loading-from-embedded-resources}

用 Avalonia 的 `AssetLoader` 可以从程序集资源中打开一个流。FlowDocument 数据文件请使用 `.xml` 扩展名——`.axaml` 和 `.xaml` 扩展名会触发 Avalonia 的 XAML 编译器，而它编译不了以 `FlowDocument` 为根元素的文件。

```csharp
var uri = new Uri("avares://MyApp/Assets/Help.xml");
using var stream = AssetLoader.Open(uri);
viewer.Document = FlowDocument.Load(stream, new XamlSerializer());
```

### 从字节数组加载 {#loading-from-a-byte-array}

```csharp
using var stream = new MemoryStream(rtfBytes);
viewer.Document = await FlowDocument.LoadAsync(stream, new RtfSerializer());
```

## 在代码中构建文档 {#building-documents-in-code}

### 手工构建 {#manual-construction}

```csharp
var document = new FlowDocument();

// Heading
var heading = new Paragraph
{
    FontSize = 24,
    FontWeight = FontWeight.Bold,
    Margin = new Thickness(0, 0, 0, 10)
};
heading.Inlines.Add(new RichRun { Text = "Report Title" });
document.Blocks.Add(heading);

// Body paragraph with mixed formatting
var body = new Paragraph();
body.Inlines.Add(new RichRun { Text = "Status: " });
body.Inlines.Add(new RichBold(new RichRun { Text = "Complete" }));
body.Inlines.Add(new RichRun { Text = ". See " });
body.Inlines.Add(new RichHyperlink(new RichRun { Text = "details" })
{
    NavigateUri = new Uri("https://example.com")
});
body.Inlines.Add(new RichRun { Text = " for more information." });
document.Blocks.Add(body);

viewer.Document = document;
```

### FlowDocumentBuilder（流式 API） {#flowdocumentbuilder-fluent-api}

`FlowDocumentBuilder` 提供了一套简洁的流式接口来构建文档：

```csharp
using Avalonia.Controls.Documents;                             // FlowDocumentBuilder, InlineFactory
using Avalonia.Controls.Documents.Primitives.DocumentNodes;    // TextMarkerStyle

var document = FlowDocumentBuilder.Create()
    .AddParagraph("Report Title")
    .AddParagraph()
    .AddText("Body text with ")
    .AddBold("bold")
    .AddText(" and ")
    .AddItalic("italic")
    .AddText(" formatting.")
    .Build();

viewer.Document = document;
```

这个构建器同样支持列表和表格：

```csharp
var document = FlowDocumentBuilder.Create()
    .AddParagraph("Shopping List")
    .StartList(TextMarkerStyle.Disc)
        .AddListItem("Apples")
        .AddListItem("Bread")
        .AddListItem("Milk")
    .EndList()
    .AddParagraph("Price Table")
    .StartTable()
        .SetTableColumns(new double[] { 200, 100 })
        .StartTableRow()
            .AddTableCell("Item")
            .AddTableCell("Price")
        .EndTableRow()
        .StartTableRow()
            .AddTableCell("Apples")
            .AddTableCell("$3.00")
        .EndTableRow()
    .EndTable()
    .Build();
```

`InlineFactory` 类提供了一组静态工厂方法，用于拼装行内元素：

```csharp
var doc = FlowDocumentBuilder.Create()
    .AddParagraph(
        InlineFactory.Text("Normal "),
        InlineFactory.Bold("bold "),
        InlineFactory.Italic("italic"))
    .Build();
```

构建器最适合线性结构的文档。若结构层层嵌套（列表项里套表格、小节内容混杂），还是手工构建更可控。

## 文档结构参考 {#document-structure-reference}

```
FlowDocument
├── Paragraph              Block containing inline elements
│   ├── RichRun            Text with uniform formatting
│   ├── RichBold           Bold wrapper (RichSpan subclass)
│   ├── RichItalic         Italic wrapper
│   ├── RichUnderline      Underline wrapper
│   ├── RichSuperscript    Superscript positioning
│   ├── RichSubscript      Subscript positioning
│   ├── RichSpan           Generic inline container
│   ├── RichHyperlink      Clickable link (NavigateUri)
│   ├── RichLineBreak      Explicit line break
│   └── RichInlineUIContainer  Embedded control (inline)
├── Section                Groups blocks together
├── List                   Bulleted or numbered list
│   └── ListItem           Contains blocks (Paragraph, nested List, ...)
├── Table                  Grid layout
│   ├── TableColumn        Column width definitions
│   └── TableRowGroup      Header/body/footer grouping
│       └── TableRow
│           └── TableCell  Contains blocks
└── BlockUIContainer       Embedded control (full-width block)
```

### 块级元素的公共属性 {#common-block-properties}

所有块级元素都继承自 `Block`，共享下列属性：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Margin` | `Thickness` | Outer spacing |
| `Padding` | `Thickness` | Inner spacing |
| `BorderThickness` | `Thickness` | Border width |
| `BorderBrush` | `IBrush?` | Border color |
| `CornerRadius` | `CornerRadius` | Rounded corners |
| `TextAlignment` | `TextAlignment` | Left, Center, Right, Justify (inherited) |
| `LineHeight` | `double` | Line spacing |
| `FlowDirection` | `FlowDirection` | LTR or RTL (inherited) |

### Common inline properties

| 属性 | 类型 | Available On |
|---|---|---|
| `Text` | `string` | `RichRun` |
| `FontSize` | `double` | All inlines (inherited) |
| `FontWeight` | `FontWeight` | All inlines (inherited) |
| `FontStyle` | `FontStyle` | All inlines (inherited) |
| `FontFamily` | `FontFamily` | All inlines (inherited) |
| `Foreground` | `IBrush?` | All inlines (inherited) |
| `TextDecorations` | `TextDecorationCollection?` | All inlines |
| `BaselineAlignment` | `BaselineAlignment` | All inlines |

## Styling and theming

### Document-level defaults

`FlowDocument` properties cascade to all child elements:

```xml
<FlowDocumentScrollViewer>
    <FlowDocument FontFamily="Segoe UI" FontSize="14"
                  Foreground="#333333" TextAlignment="Left">
        <Paragraph>
            <RichRun Text="Inherits font and color from FlowDocument." />
        </Paragraph>
    </FlowDocument>
</FlowDocumentScrollViewer>
```

Individual elements override the defaults:

```xml
<Paragraph FontSize="24" FontWeight="Bold" Foreground="DarkBlue">
    <RichRun Text="This heading overrides the document defaults." />
</Paragraph>
```

### Theming with styles

Use Avalonia styles to control the viewer's appearance:

```xml
<Window.Styles>
    <Style Selector="FlowDocumentScrollViewer">
        <Setter Property="Background" Value="{DynamicResource SystemRegionBrush}" />
        <Setter Property="Padding" Value="24" />
    </Style>
</Window.Styles>
```

### Hyperlinks

`RichHyperlink` supports the `NavigateUri` property and raises a `RequestNavigate` routed event:

```xml
<Paragraph>
    <RichRun Text="Visit the " />
    <RichHyperlink NavigateUri="https://avaloniaui.net">
        <RichRun Text="Avalonia website" />
    </RichHyperlink>
    <RichRun Text=" for more information." />
</Paragraph>
```

Handle navigation in code-behind:

```csharp
viewer.AddHandler(RichHyperlink.RequestNavigateEvent, (sender, e) =>
{
    if (e.Uri is { } uri)
    {
        Process.Start(new ProcessStartInfo(uri.AbsoluteUri) { UseShellExecute = true });
        e.Handled = true;
    }
});
```

`RichHyperlink` exposes `:pointerover`, `:pressed`, and `:visited` pseudo-classes for styling.

## Page layout

### PageWidth and PagePadding

By default, content fills the available width (`PageWidth = NaN`). Set a fixed `PageWidth` to simulate a fixed-width page:

```xml
<FlowDocumentScrollViewer>
    <FlowDocument PageWidth="700" PagePadding="40">
        <Paragraph>
            <RichRun Text="This content is constrained to a 700 DIP wide page with 40 DIP padding." />
        </Paragraph>
    </FlowDocument>
</FlowDocumentScrollViewer>
```

When `PageWidth` is set, the page area is centered within the viewer and the background outside the page area remains visible.

### ShowPageBounds

Enable `ShowPageBounds` to render visual indicators at the page boundary. This is useful for print-preview scenarios:

```xml
<FlowDocumentScrollViewer ShowPageBounds="True">
    <FlowDocument PageWidth="700" PagePadding="40" PageHeight="900">
        <!-- Content -->
    </FlowDocument>
</FlowDocumentScrollViewer>
```

### Viewer properties

| 属性 | 类型 | 说明 | 默认值 |
|---|---|---|---|
| `IsSelectionEnabled` | `bool` | Set to `False` to make the viewer a pure display control. The inner view stops being focusable, which matters for a viewer inside an items control. | `true` |
| `IsCaretVisible` | `bool` | Shows an insertion caret without enabling editing. | `false` |
| `ShowPageBounds` | `bool` | Draws indicators at the page boundary. | `false` |
| `ShowPageBreakMarkers` | `bool` | Draws a dashed rule across the top edge of a block carrying `BreakPageBefore`. Can be colored by `PageBreakMarkerBrush`. Defaults `false` in the page viewer. | `true` |
| `ShowPageBandsInContinuousLayout` | `bool` | Shows the document's running header above the first block and its running footer below the last. No effect in the page viewer. | `false` |

## Embedding controls

### BlockUIContainer

Embed any Avalonia control as a full-width block element:

```xml
<FlowDocumentScrollViewer>
    <FlowDocument>
        <Paragraph FontSize="20" FontWeight="Bold">
            <RichRun Text="Monthly Revenue" />
        </Paragraph>
        <BlockUIContainer>
            <Image Source="/Assets/revenue-chart.png" MaxHeight="300"
                   HorizontalAlignment="Center" />
        </BlockUIContainer>
        <Paragraph>
            <RichRun Text="Figure 1: Revenue trends for the past 12 months." />
        </Paragraph>
    </FlowDocument>
</FlowDocumentScrollViewer>
```

In code:

```csharp
var container = new BlockUIContainer(new Image
{
    Source = bitmap,
    MaxHeight = 300
});
document.Blocks.Add(container);
```

### RichInlineUIContainer

Embed a small control inline with text:

```xml
<Paragraph>
    <RichRun Text="Status: " />
    <RichInlineUIContainer>
        <Border Background="Green" CornerRadius="4" Padding="4,2">
            <TextBlock Text="Active" Foreground="White" FontSize="11" />
        </Border>
    </RichInlineUIContainer>
    <RichRun Text=" since January 2026." />
</Paragraph>
```

:::note
Embedded controls are live Avalonia controls. They participate in layout and rendering but are not captured in serialization snapshots.
:::

## Background loading and thread safety

### Safe async pattern

`FlowDocument.LoadAsync` deserializes on a background thread and returns a document ready for UI-thread assignment:

```csharp
async Task LoadDocumentAsync(string path)
{
    IDocumentSerializer serializer = GetSerializer(path);

    await using var stream = File.OpenRead(path);
    viewer.Document = await FlowDocument.LoadAsync(stream, serializer);
}
```

### Snapshot-based workflows

For conversion pipelines (load, display, re-export), call `CreateSnapshot()` once and share the result across operations. Snapshots are immutable and safe to use from any thread:

`FlowDocumentScrollViewer.Document` is typed `FlowDocument?`, so check it before dereferencing:

```csharp
// UI thread: take a snapshot
if (viewer.Document is null) return;
var snapshot = viewer.Document.CreateSnapshot();

// Background thread: serialize to multiple formats from one snapshot.
// IDocumentSerializer is synchronous, so Task.Run is what moves the work
// off the UI thread.
await Task.Run(() =>
{
    using var rtfStream = File.Create("output.rtf");
    new RtfSerializer().Serialize(snapshot, rtfStream);

    using var docxStream = File.Create("output.docx");
    new DocxSerializer().Serialize(snapshot, docxStream);
});
```

`SaveAsync` is a convenience wrapper that creates a snapshot and serializes in one call. Use `CreateSnapshot()` directly when you need to serialize to multiple formats from the same document state.

For a detailed discussion of threading constraints, see the [Thread Safety](/controls/input/text-input/richtexteditor/thread-safety) guide.

## Performance considerations

### Virtualization

`FlowDocumentScrollViewer` virtualizes rendering through its inner `TextViewBase`:

- Only blocks within the viewport plus a buffer zone are realized and measured.
- Unrealized blocks use an estimated height that starts at 24 DIPs and adapts dynamically as blocks are measured. The estimate is a running average of all measured block heights.
- As the user scrolls, estimates are replaced by actual measurements. This can cause minor scroll-position adjustments on first scroll through unseen content.

This means documents with thousands of blocks remain responsive — rendering cost is proportional to visible content, not total document size.

### Large documents

For documents with many blocks:

- Use `FlowDocument.LoadAsync` to avoid blocking the UI thread during deserialization.
- Avoid `PageWidth` values significantly wider than the viewport. Wider pages produce longer text lines, increasing line-breaking and rendering work.
- If loading user-provided files, validate file size before opening.

### Reuse snapshots

When a document is used in a preview-then-export pipeline, create a single `DocumentSnapshot` with `CreateSnapshot()` and reuse it. Each call traverses the document tree (O(n) for structure). One snapshot can be serialized to multiple formats without redundant tree walks.

For more optimization techniques, see the [Performance Tuning](/controls/input/text-input/richtexteditor/performance-tuning) guide.

## 常见写法 {#common-patterns}

### File preview pane

A file browser that previews documents as the user selects files. Cancel in-flight loads when the selection changes:

```csharp
public partial class FilePreviewPane : UserControl
{
    private CancellationTokenSource? _loadCts;

    public async Task PreviewFileAsync(string path)
    {
        // Cancel any previous load
        _loadCts?.Cancel();
        _loadCts = new CancellationTokenSource();
        var token = _loadCts.Token;

        try
        {
            IDocumentSerializer serializer = GetSerializer(path);
            await using var stream = File.OpenRead(path);
            var document = await FlowDocument.LoadAsync(stream, serializer, token);

            token.ThrowIfCancellationRequested();
            Viewer.Document = document;
        }
        catch (OperationCanceledException)
        {
            // Selection changed before load completed — expected
        }
    }
}
```

### Help / about viewer

Load a static XAML document from an embedded resource:

```csharp
public partial class HelpWindow : Window
{
    public HelpWindow()
    {
        InitializeComponent();

        var uri = new Uri("avares://MyApp/Assets/Help.xml");
        using var stream = AssetLoader.Open(uri);
        HelpViewer.Document = FlowDocument.Load(stream, new XamlSerializer());
    }
}
```

```xml
<!-- HelpWindow.axaml -->
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="MyApp.HelpWindow"
        Title="Help" Width="600" Height="500">
    <FlowDocumentScrollViewer x:Name="HelpViewer" Padding="20" />
</Window>
```

### Print preview

For a true print preview use `FlowDocumentPageViewer`, which lays the document out as real page sheets with the same pagination that PDF export produces. Within the continuous viewer, `ShowPageBounds` plus a fixed `PageWidth` and `PageHeight` visualizes the page boundaries in the flowing column:

```xml
<FlowDocumentScrollViewer ShowPageBounds="True"
                          Background="#F0F0F0"
                          Padding="40">
    <FlowDocument PageWidth="816" PageHeight="1056" PagePadding="72">
        <!-- US Letter: 8.5 x 11 inches = 816 x 1056 device-independent pixels
             (96 per inch); 72 DIP padding = 0.75 inch margins. -->
        <Paragraph FontSize="20" FontWeight="Bold">
            <RichRun Text="Quarterly Report" />
        </Paragraph>
        <Paragraph>
            <RichRun Text="Content laid out within print margins." />
        </Paragraph>
    </FlowDocument>
</FlowDocumentScrollViewer>
```

### Dynamic report generation

Generate a report from a data model and display it:

```csharp
FlowDocument BuildReport(IReadOnlyList<SalesRecord> records)
{
    var builder = FlowDocumentBuilder.Create()
        .AddParagraph("Sales Report");

    builder.StartTable()
        .SetTableColumns(new double[] { 200, 120, 120 })
        .StartTableRow()
            .AddTableCell("Product")
            .AddTableCell("Quantity")
            .AddTableCell("Revenue")
        .EndTableRow();

    foreach (var record in records)
    {
        builder.StartTableRow()
            .AddTableCell(record.Product)
            .AddTableCell(record.Quantity.ToString())
            .AddTableCell(record.Revenue.ToString("C"))
        .EndTableRow();
    }

    builder.EndTable();

    builder.AddParagraph()
        .AddText("Total revenue: ")
        .AddBold(records.Sum(r => r.Revenue).ToString("C"));

    return builder.Build();
}

// Usage
viewer.Document = BuildReport(salesData);
```

## 限制 {#limitations}

Current limitations of `FlowDocumentScrollViewer`:

| Limitation | Workaround / Details |
|---|---|
| No insertion caret and no editing | Use `RichTextEditor` for editing |
| No built-in search/find | Implement search against document text and scroll programmatically |
| Continuous scroll only | Use `FlowDocumentPageViewer` for discrete page sheets; `ShowPageBounds` shows boundaries in the flowing column |
| Embedded controls not serialized | `BlockUIContainer` / `RichInlineUIContainer` children are excluded from snapshots |
| `ITextView` not publicly exposed | The `TextView` property on `FlowDocumentScrollViewer` is internal; the host's `ITextViewHost.TextView` explicit interface implementation is the only public access |
