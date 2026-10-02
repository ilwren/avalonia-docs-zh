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
| `Margin` | `Thickness` | 外侧间距 |
| `Padding` | `Thickness` | 内侧间距 |
| `BorderThickness` | `Thickness` | 边框宽度 |
| `BorderBrush` | `IBrush?` | 边框颜色 |
| `CornerRadius` | `CornerRadius` | 圆角 |
| `TextAlignment` | `TextAlignment` | Left、Center、Right、Justify（可继承） |
| `LineHeight` | `double` | 行距 |
| `FlowDirection` | `FlowDirection` | LTR 或 RTL（可继承） |

### 行内元素的公共属性 {#common-inline-properties}

| 属性 | 类型 | 适用于 |
|---|---|---|
| `Text` | `string` | `RichRun` |
| `FontSize` | `double` | 所有行内元素（可继承） |
| `FontWeight` | `FontWeight` | 所有行内元素（可继承） |
| `FontStyle` | `FontStyle` | 所有行内元素（可继承） |
| `FontFamily` | `FontFamily` | 所有行内元素（可继承） |
| `Foreground` | `IBrush?` | 所有行内元素（可继承） |
| `TextDecorations` | `TextDecorationCollection?` | 所有行内元素 |
| `BaselineAlignment` | `BaselineAlignment` | 所有行内元素 |

## 样式与主题 {#styling-and-theming}

### 文档级默认值 {#document-level-defaults}

`FlowDocument` 上的属性会层层传递给所有子元素：

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

单个元素可以覆盖这些默认值：

```xml
<Paragraph FontSize="24" FontWeight="Bold" Foreground="DarkBlue">
    <RichRun Text="This heading overrides the document defaults." />
</Paragraph>
```

### 用样式做主题 {#theming-with-styles}

用 Avalonia 样式来控制阅读器的外观：

```xml
<Window.Styles>
    <Style Selector="FlowDocumentScrollViewer">
        <Setter Property="Background" Value="{DynamicResource SystemRegionBrush}" />
        <Setter Property="Padding" Value="24" />
    </Style>
</Window.Styles>
```

### Hyperlinks

`RichHyperlink` 支持 `NavigateUri` 属性，并会引发 `RequestNavigate` 路由事件：

```xml
<Paragraph>
    <RichRun Text="Visit the " />
    <RichHyperlink NavigateUri="https://avaloniaui.net">
        <RichRun Text="Avalonia website" />
    </RichHyperlink>
    <RichRun Text=" for more information." />
</Paragraph>
```

在代码隐藏中处理导航：

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

`RichHyperlink` 对外提供 `:pointerover`、`:pressed` 和 `:visited` 三个伪类供设置样式。

## 页面布局 {#page-layout}

### PageWidth 与 PagePadding {#pagewidth-and-pagepadding}

默认情况下内容会铺满可用宽度（`PageWidth = NaN`）。设定一个固定的 `PageWidth` 即可模拟定宽页面：

```xml
<FlowDocumentScrollViewer>
    <FlowDocument PageWidth="700" PagePadding="40">
        <Paragraph>
            <RichRun Text="This content is constrained to a 700 DIP wide page with 40 DIP padding." />
        </Paragraph>
    </FlowDocument>
</FlowDocumentScrollViewer>
```

设置了 `PageWidth` 之后，页面区域会在阅读器中居中，页面之外的背景依然可见。

### ShowPageBounds

启用 `ShowPageBounds` 可在页面边界处绘制视觉标记，这在打印预览场景中很有用：

```xml
<FlowDocumentScrollViewer ShowPageBounds="True">
    <FlowDocument PageWidth="700" PagePadding="40" PageHeight="900">
        <!-- Content -->
    </FlowDocument>
</FlowDocumentScrollViewer>
```

### 阅读器属性 {#viewer-properties}

| 属性 | 类型 | 说明 | 默认值 |
|---|---|---|---|
| `IsSelectionEnabled` | `bool` | 设为 `False` 可把阅读器变成纯展示控件，内部视图不再可获得焦点——当阅读器嵌在项目控件里时，这一点很关键。 | `true` |
| `IsCaretVisible` | `bool` | 显示插入符，但不启用编辑。 | `false` |
| `ShowPageBounds` | `bool` | 在页面边界处绘制标记。 | `false` |
| `ShowPageBreakMarkers` | `bool` | 在带有 `BreakPageBefore` 的块顶边画一条虚线。颜色可由 `PageBreakMarkerBrush` 指定。在分页阅读器中默认为 `false`。 | `true` |
| `ShowPageBandsInContinuousLayout` | `bool` | 在首个块之上显示文档的通栏页眉，在末个块之下显示通栏页脚。对分页阅读器无效。 | `false` |

## 嵌入控件 {#embedding-controls}

### BlockUIContainer

可以把任意 Avalonia 控件作为整宽的块级元素嵌入：

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

在代码中：

```csharp
var container = new BlockUIContainer(new Image
{
    Source = bitmap,
    MaxHeight = 300
});
document.Blocks.Add(container);
```

### RichInlineUIContainer

把小控件与文字一起行内嵌入：

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
嵌入的控件是活生生的 Avalonia 控件：它们参与布局和渲染，但不会被纳入序列化快照。
:::

## 后台加载与线程安全 {#background-loading-and-thread-safety}

### 安全的异步写法 {#safe-async-pattern}

`FlowDocument.LoadAsync` 在后台线程上反序列化，返回的文档可直接在 UI 线程上赋值：

```csharp
async Task LoadDocumentAsync(string path)
{
    IDocumentSerializer serializer = GetSerializer(path);

    await using var stream = File.OpenRead(path);
    viewer.Document = await FlowDocument.LoadAsync(stream, serializer);
}
```

### 基于快照的工作流 {#snapshot-based-workflows}

对于「加载 → 显示 → 再导出」这类转换流水线，调用一次 `CreateSnapshot()` 并把结果在各道工序间共享即可。快照是不可变的，任何线程都能安全使用：

`FlowDocumentScrollViewer.Document` 的类型是 `FlowDocument?`，解引用之前记得先判空：

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

`SaveAsync` 是个便利封装，一次调用就完成「创建快照 + 序列化」。若要把同一份文档状态序列化成多种格式，请直接用 `CreateSnapshot()`。

关于线程约束的详细讨论，请参阅[线程安全](/controls/input/text-input/richtexteditor/thread-safety)指南。

## 性能考量 {#performance-considerations}

### Virtualization

`FlowDocumentScrollViewer` 通过其内部的 `TextViewBase` 实现渲染虚拟化：

- 只有视口内及其缓冲区里的块才会被实体化和测量。
- 尚未实体化的块使用估算高度，初始为 24 DIP，并随着块被实际测量而动态调整——这个估值是所有已测量块高度的滑动平均。
- 随着用户滚动，估算值会被实际测量值替换。因此首次滚动经过未见过的内容时，滚动位置可能略有跳动。

这意味着上千个块的文档依然流畅：渲染开销只与可见内容成正比，与文档总体量无关。

### 大文档 {#large-documents}

块数众多的文档：

- 请用 `FlowDocument.LoadAsync`，避免反序列化期间阻塞 UI 线程。
- 避免把 `PageWidth` 设得比视口宽出许多。页面越宽，文本行越长，断行和渲染的开销也越大。
- 若要加载用户提供的文件，请在打开前先校验文件大小。

### 复用快照 {#reuse-snapshots}

当文档要走「先预览后导出」的流程时，请用 `CreateSnapshot()` 创建一个 `DocumentSnapshot` 并反复使用。每次调用都要遍历整棵文档树（结构部分为 O(n)），而一份快照可以序列化成多种格式，不必重复遍历。

更多优化手法请参阅[性能调优](/controls/input/text-input/richtexteditor/performance-tuning)指南。

## 常见写法 {#common-patterns}

### 文件预览面板 {#file-preview-pane}

一个文件浏览器，用户选中文件时即时预览文档。选择发生变化时，取消仍在进行的加载：

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

### 帮助 / 关于页面的阅读器 {#help-about-viewer}

从嵌入资源加载一份静态 XAML 文档：

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

### 打印预览 {#print-preview}

要做真正的打印预览，请用 `FlowDocumentPageViewer`：它把文档排布成一张张真实的纸面，分页方式与 PDF 导出完全一致。若用连续滚动的阅读器，则可以用 `ShowPageBounds` 搭配固定的 `PageWidth` 和 `PageHeight`，在连续栏中把页面边界标示出来：

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

### 动态生成报表 {#dynamic-report-generation}

从数据模型生成报表并显示出来：

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

`FlowDocumentScrollViewer` 目前的局限：

| 局限 | Workaround / Details |
|---|---|
| 没有插入符，也不能编辑 | 需要编辑请用 `RichTextEditor` |
| 没有内置的查找功能 | 可针对文档文本自行实现搜索，再用代码滚动定位 |
| 只支持连续滚动 | 需要一页页的纸面请用 `FlowDocumentPageViewer`；在连续栏中可用 `ShowPageBounds` 标示边界 |
| 嵌入的控件不会被序列化 | `BlockUIContainer` / `RichInlineUIContainer` 的子元素不会进入快照 |
| `ITextView` 未公开暴露 | `FlowDocumentScrollViewer` 上的 `TextView` 属性是 internal 的；唯一的公开访问途径是宿主的 `ITextViewHost.TextView` 显式接口实现 |
