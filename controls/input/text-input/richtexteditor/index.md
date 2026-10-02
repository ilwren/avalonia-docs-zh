---
id: index
title: RichTextEditor 控件
doc-type: reference
tags:
 - avalonia pro
 - avalonia enterprise
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

`Avalonia.Controls.RichTextEditor` 是面向 Avalonia 应用的富文本编辑方案，提供交互式文本编辑、文档架构和文件序列化等能力。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 适用场景 {#when-to-use}

用 `RichTextEditor` 开辟一块区域，让用户编辑文本内容并执行常见的文本操作，比如设置格式、对齐、高亮或撤销/重做。

## 快速上手 {#getting-started}

1. 运行 `dotnet add package` 安装 `Avalonia.Controls.RichTextEditor` 和 `Avalonia.Controls.Documents` 两个 NuGet 包。你还可以按需安装特定文件格式的序列化器。

```bash
# Editor control
dotnet add package Avalonia.Controls.RichTextEditor

# Core document model, includes plain text serializer
dotnet add package Avalonia.Controls.Documents

# Serializers (add only what you need)
dotnet add package Avalonia.Controls.Documents.Serialization.Rtf     # RTF support
dotnet add package Avalonia.Controls.Documents.Serialization.Docx    # DOCX (Open XML) support
dotnet add package Avalonia.Controls.Documents.Serialization.Xaml    # XAML serialization
dotnet add package Avalonia.Controls.Documents.Serialization.Html    # HTML import (read only)
dotnet add package Avalonia.Controls.Documents.Serialization.Pdf     # PDF export (write only)
dotnet add package Avalonia.Controls.Markdown                        # Markdown viewer and serializer
```

2. 在可执行项目文件（`.csproj`）中填入你的 Avalonia 许可证密钥。密钥可以在 [Avalonia 门户](https://portal.avaloniaui.net)中获取。

```xml
<ItemGroup>
  <AvaloniaUILicenseKey Include="YOUR_LICENSE_KEY" />
</ItemGroup>
```

:::tip
对于多项目解决方案，可以把许可证密钥放进[环境变量](https://learn.microsoft.com/en-us/visualstudio/msbuild/how-to-use-environment-variables-in-a-build)或[共享 props 文件](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory?view=vs-2022#directorybuildprops-example)，免得到处重复。
:::

3. 在 `App.axaml` 文件中用 `StyleInclude` 引用 `RichTextEditor` 的默认主题，这会带入渲染该控件所需的资源。

```xml
<Application.Styles>
   <StyleInclude Source="avares://Avalonia.Controls.RichTextEditor/Themes/Default.axaml" />
   <!-- other styles -->
</Application.Styles>
```

关于安装 Avalonia Pro 控件的更多内容，请参阅[安装 Avalonia Pro](/tools/installing-avalonia-pro)。

## 基本用法 {#basic-usage}

照此准备好之后，就可以着手实现一个最基本的富文本编辑器了。

<Tabs>
<TabItem value="xaml" label="XAML">

    ```xml
    <Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="My Rich Text Editor" 
        Width="800" Height="600">
    
    <RichTextEditor x:Name="Editor">
        <RichTextEditor.Document>
            <FlowDocument>
                <Paragraph>
                    <RichRun Text="Welcome to " />
                    <RichBold>
                        <RichRun Text="RichTextEditor" />
                    </RichBold>
                    <RichRun Text="!" />
                </Paragraph>
            </FlowDocument>
        </RichTextEditor.Document>
    </RichTextEditor>
    
    </Window>
    ```
    
</TabItem>

<TabItem value="csharp" label="Code-behind">

  ```csharp
  using Avalonia.Controls;
  using Avalonia.Controls.Documents;

  public partial class MainWindow : Window
  {
      public MainWindow()
      {
          InitializeComponent();
          
          var editor = this.FindControl<RichTextEditor>("Editor");

          // Undo/redo is ready to use: the editor creates an UndoManager
          // automatically when a Document is attached. UndoManager is the
          // single sealed implementation, and editor.UndoManager is typed
          // UndoManager?. To change the limit:
          // editor.UndoLimit = 50;
      }
  }
  ```

</TabItem>
</Tabs>

## 用代码构建文档 {#programmatic-document-construction}

如果你更习惯这种方式，也可以在代码隐藏中（而非 XAML 里）创建和编辑文档：直接调用 `Avalonia.Controls.Documents` 中相应的[组件](#components)、[块级元素](#block-elements)或[行内元素](#inline-elements)即可。

<Tabs>
<TabItem value="create" label="Create document">

  ```csharp
  var document = new FlowDocument();
  var paragraph = new Paragraph();
  paragraph.Inlines.Add(new RichRun("Hello "));
  paragraph.Inlines.Add(new RichBold(new RichRun("World")));
  paragraph.Inlines.Add(new RichRun("!"));
  document.Blocks.Add(paragraph);
  
  editor.Document = document;
  ```

</TabItem>

<TabItem value="insert" label="Insert text">

  ```csharp
  // FlowDocument.TextDocument creates the backing store on first read,
  // so it is never null.
  var doc = editor.Document.TextDocument;

  // Insert at start
  doc.ContentStart.InsertText("Header: ");

  // Insert at end
  doc.ContentEnd.InsertText("\n\nFooter");
  ```

</TabItem>

<TabItem value="formatting" label="Format selected text">

  ```csharp
  var doc = editor.Document.TextDocument;
  var range = new TextRange(doc.ContentStart, doc.ContentStart.GetPositionAtOffset(10));

  range.ApplyPropertyValue(RichTextElement.ForegroundProperty, Brushes.Red);
  range.ApplyPropertyValue(RichTextElement.FontSizeProperty, 20.0);
  ```

</TabItem>
</Tabs>

## 加载与保存文件 {#loading-and-saving-files}

Load 和 Save 接受一个 `IDocumentSerializer` 实例，每种格式都在各自的包里。

```csharp
using Avalonia.Controls.Documents.Serialization.Rtf;

// Load RTF, keeping the parse off the UI thread
await using (var stream = File.OpenRead("document.rtf"))
{
    await editor.LoadAsync(stream, new RtfSerializer());
}

// Save RTF, keeping the write off the UI thread
await using (var stream = File.Create("output.rtf"))
{
    await editor.SaveAsync(stream, new RtfSerializer());
}
```

也有同步重载，但全部开销都压在调用线程上：

```csharp
editor.Load(stream, new RtfSerializer());
editor.Save(stream, new RtfSerializer());
```

:::info
`IDocumentSerializer` 只有同步版本。没有哪种格式会做异步 I/O——`LoadAsync` 和 `SaveAsync` 也不例外，它们只是把调用包进 `Task.Run` 以便把活儿挪出当前线程。`LoadAsync` 在线程池上解析，随后在 UI 线程上构建元素树，因为 `FlowDocument` 及其元素归属于构造它们的那个线程的调度器。
:::

可用的序列化器：

| 序列化器 | NuGet 包 | 扩展名 | 方向 |
|---|---|---|---|
| `RtfSerializer` | `Avalonia.Controls.Documents.Serialization.Rtf` | `.rtf` | 可读可写 |
| `DocxSerializer` | `Avalonia.Controls.Documents.Serialization.Docx` | `.docx` | 可读可写 |
| `XamlSerializer` | `Avalonia.Controls.Documents.Serialization.Xaml` | `.xaml` | 可读可写 |
| `MarkdownSerializer` | `Avalonia.Controls.Markdown` | `.md` | 可读可写 |
| `HtmlSerializer` | `Avalonia.Controls.Documents.Serialization.Html` | `.html` | 只读（`CanWrite` 为 `false`） |
| `PdfSerializer` | `Avalonia.Controls.Documents.Serialization.Pdf` | `.pdf` | 只写（`CanRead` 为 `false`） |
| `PlainTextSerializer` | 已包含在 `Avalonia.Controls.Documents`（核心包）中 | `.txt` | 可读可写 |
<br />

每个序列化器都通过 `CanRead` 和 `CanWrite` 表明自己的读写方向，格式选择器可据此过滤列表。

`PdfSerializer` 是通往纸面的官方途径。

### 不借助编辑器加载文档 {#loading-a-document-without-an-editor}

`FlowDocument.Load` 和 `FlowDocument.LoadAsync` 直接从流创建文档，适合预览或格式转换的场景。两者都接受一个可选的 `CancellationToken`：

```csharp
await using var stream = File.OpenRead("document.rtf");
var document = await FlowDocument.LoadAsync(stream, new RtfSerializer(), cancellationToken);
```

若希望全程不牵涉 UI 线程，可以用序列化器读出一个 `DocumentSnapshot`，再用 `TextDocument.FromSnapshot` 把它实体化——它承载着整篇文档。

## 加个字数统计 {#adding-a-word-counter}

你可以写一个返回字数的事件。下面的例子加了一个实时字数统计，文本变化时自动更新。

```csharp
editor.ContentChanged += (sender, args) =>
{
    Console.WriteLine("Document changed");
    UpdateWordCount();
};

void UpdateWordCount()
{
    string? text = editor.Document.ContentRange?.GetText();
    if (text != null)
    {
        int wordCount = text.Split(new[] { ' ', '\n', '\r' }, 
                                    StringSplitOptions.RemoveEmptyEntries).Length;
        Console.WriteLine($"Word count: {wordCount}");
    }
}
```

## 自定义选区高亮颜色 {#customizing-selection-highlight-color}

给 `SelectionBrush` 指定一个 ARGB 值，即可自定义文本选区的高亮颜色。

```xml
<RichTextEditor SelectionBrush="#ffff529e">
```

## Components

Avalonia 富文本编辑器由四个部分组成：

1. `RichTextEditor`：交互式编辑控件，负责渲染文档，让用户输入、选择、设置格式、撤销/重做等等。
2. `FlowDocumentScrollViewer`：只读阅读器，把文档显示为一整条连续的栏，不提供编辑能力。
3. `FlowDocumentPageViewer`：只读阅读器，把文档显示为一页页独立的纸面，就像文字处理软件的打印版式。它派生自 `FlowDocumentScrollViewer`。
4. `FlowDocument`：文档模型，把富文本内容组织成一个个[块](#block-elements)。

文档还拥有两类嵌套文档，它们本身也都是 `FlowDocument`：页眉页脚带（通栏[页眉与页脚](/controls/input/text-input/richtexteditor/headers-and-footers)，存放在 `FlowDocument.PageBands` 中）和[脚注](/controls/input/text-input/richtexteditor/footnotes)（存放在 `FlowDocument.Footnotes` 中）。插入符落在哪一个里面，编辑器就改为面向哪一个；并不存在嵌套的 `RichTextEditor`。

### RichTextEditor 属性 {#richtexteditor-properties}

下列属性供 `RichTextEditor` 组件使用。

| 属性 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| `AcceptsReturn` | `bool`| 决定编辑器是否接受回车键输入。 | `true` |
| `AcceptsTab` | `bool` | 决定编辑器是否接受 Tab 键输入。 | `true` |
| `CaretBrush` | `IBrush?` | 插入符（文本光标）的颜色。| None |
| `Document` | `FlowDocument` | 选定要显示和编辑的文档。 | 一个新的空 `FlowDocument` |
| `IsReadOnly` | `bool` | 决定编辑器是否只读。 | `false` |
| `PageBandDistance` | `double` | 从纸面边缘到通栏页眉或页脚的距离。该值归文档所有，这里的设置会回写过去。 | 12.5 mm |
| `PageGap` | `double` | 分页布局中纸面之间的间隙。 | 24 |
| `PageMargins` | `Thickness?` | 分页布局所用的页边距。未设置时回落到文档的 `PagePadding`。 | `null` |
| `PageSize` | `Size?` | 分页布局所用的页面尺寸。未设置时先回落到文档的页面尺寸，再回落到 A4。 | `null` |
| `SelectionBrush` | `IBrush?` | 文本选区的颜色。 | None |
| `SelectionFlyout` | `EditorSelectionFlyout?` | 选区上方浮现的迷你工具栏。设为 `null` 即可去掉它。 | `null`（默认主题会提供一个） |
| `ShowBlockAdorners` | `bool` | 决定是否显示块装饰物。 | `true` |
| `ShowPageBandsInContinuousLayout` | `bool` | 在连续布局中，于首个块之上显示通栏页眉、末个块之下显示通栏页脚。对分页布局无效。 | `false` |
| `ShowPageBounds` | `bool` | 决定是否显示页面边界标记。 | `false` |
| `ShowSelectionFlyout` | `bool` | 显示或隐藏选区浮层，但不替换它。 | `true` |
| `ShowToolbar` | `bool` | 决定工具栏是否可见。 | `true` |
| `Toolbar` | `EditorToolbar?` | 自定义工具栏的外观与布局。 | `null`（默认主题会提供一个） |
| `UndoLimit` | `int` | 可供撤销的操作最多保留多少步。 | 100 |
| `ViewMode` | `DocumentViewMode` | `Continuous` 表示一整条连续的栏，`PageLayout` 表示一页页独立的纸面。 | `Continuous` |

### FlowDocument 属性 {#flowdocument-properties}

下列属性供 `FlowDocument` 组件使用。

| 属性 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| `Background` | `IBrush` | 文档背景色，为 ARGB 值。 | `Null` |
| `FontFamily` | `FontFamily ` | 文档中文本的字体。 | `Null` |
| `FontSize` | `double` | 文档中文本的字号。 | 12 |
| `FontStretch` | `FontStretch` | 文档中文本的字体拉伸，比如 `Normal`、`Condensed`、`Expanded`。 | `Normal` |
| `FontStyle` | `FontStyle` | 文档中文本的字形，比如 `Normal`、`Italic`、`Oblique`。 | `Null` |
| `FontWeight` | `FontWeight` | 文档中文本的字重，比如 `Normal`、`Bold`。 | `Normal` |
| `FootnoteNumberFormat` | `FootnoteNumberFormat` | 脚注锚点所用的编号格式，比如 `Decimal`、`LowerRoman`、`Symbols`。 | `Decimal` |
| `Foreground` | `IBrush` | 文档前景色，为 ARGB 值。 | `Null` |
| `PageBandDistance` | `double` | 从纸面边缘到通栏页眉或页脚的距离。`NaN` 表示文档未作声明，采用默认值。 | `double.NaN` |
| `PageHeight` | `double` | 页面高度。 | `double.NaN` |
| `PagePadding` | `Thickness` | 块的边框与其内容之间的内侧间距。 | `Null` |
| `PageWidth` | `double` | 页面宽度。 | `double.NaN` |
| `TextAlignment` | `TextAlignment` | 文档中文本的对齐方式，即 `Left`、`Center`、`Right`、`Justify`。 | `Null` |
<br />

`FlowDocument` 还拥有两组嵌套文档：[`PageBands`](/controls/input/text-input/richtexteditor/headers-and-footers)（通栏页眉与页脚）和[脚注](/controls/input/text-input/richtexteditor/footnotes)。两者都能完整经受快照往返，并把撤销并入所属文档的栈，因此不论是否有元素被实体化，它们都在那儿。

## 块级元素 {#block-elements}

`FlowDocument` 用块级元素来搭建文档模型、组织内容。

| 元素 | 说明 |
| --- | --- |
| `Block` | 块级元素的抽象基类。 |
| `BlockUIContainer` | 用于把 UI 元素作为块嵌入的包装器。 |
| `List` | 显示项目符号列表或编号列表。 |
| `ListItem` | `List` 中的单个条目。 |
| `Paragraph` | 最基本的块级元素，内含富文本内容。 |
| `Section` | 把其他块级元素归为一组的块级元素。它自带 `PageWidth`、`PageHeight` 和 `PagePadding`，因此各小节的页面设置可以各不相同。 |
| `Table` | 显示表格。 |
| `TableCell` | `Table` 中的单个单元格。 |
| `TableColumn` | `Table` 中的一列单元格。 |
| `TableRow` | `Table` 中的一行单元格。 |
| `TableRowGroup` | `Table` 中的一组行。 |

### 属性 {#properties}

| 属性 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| `Background` | `IBrush` | 块的背景色，为 ARGB 值。 | `Null` |
| `BorderBrush`| `IBrush` | 块的边框颜色，为 ARGB 值。 | `Null` |
| `BorderThickness` | `Thickness` | 块的边框粗细。 | `Null` |
| `BreakPageBefore` | `bool` | 在分页布局、打印和 PDF 导出中让该块另起一页。按 Ctrl+Enter 可设置它。 | `false` |
| `Child` | `Control` | 供 `BlockUIContainer` 使用。指定要放进该块的控件。 | `Null` |
| `ColumnSpan` | `int` | 供 `TableCell` 使用。单元格横跨的列数。 | 1 |
| `CornerRadius ` | `CornerRadius` | 块的圆角半径。 | `Null` |
| `FlowDirection` | `FlowDirection` | 文本的排列方向，即 `LeftToRight` 或 `RightToLeft`。 | `Null` |
| `FontFamily` | `FontFamily ` | 块中文本的字体。 | `Null` |
| `FontFeatures` | `FontFeatureCollection` | 作用于块中文本的一组字体特性。 |
| `FontSize` | `double` | 块中文本的字号。 | 12 |
| `FontStretch` | `FontStretch` | 块中文本的字体拉伸，比如 `Normal`、`Condensed`、`Expanded`。 | `Normal` |
| `FontStyle` | `FontStyle` | 块中文本的字形，比如 `Normal`、`Italic`、`Oblique`。 | `Null` |
| `FontWeight` | `FontWeight` | 块中文本的字重，比如 `Normal`、`Bold`。 | `Normal` |
| `Foreground` | `IBrush` | 块的前景色，为 ARGB 值。 | `Null` |
| `Height` | `double` | 供 `TableRow` 使用。行的最小高度。为零时按内容撑开。 | 0 |
| `InsideBorderBrush` | `IBrush?` | 供 `Table` 使用。单元格之间内部网格线的颜色。 | `Null` |
| `InsideBorderThickness` | `double` | 供 `Table` 使用。单元格之间内部网格线的粗细。 | 0 |
| `KeepTogether` | `bool` | 让整个块保持在同一页上，而不被分页符拆开。 | `false` |
| `KeepWithNext` | `bool` | 让该块与紧随其后的块留在同一页上。 | `false` |
| `LetterSpacing` | `double` | 字符之间额外的水平间距。默认值 0 表示常规间距。 | 0 |
| `LineHeight` | `double` | 块中每一行文本的行高。 | `double.NaN` |
| `Margin` | `Thickness` | 块级元素周围的外侧间距。 | `Null` |
| `MarkerAlignment` | `TextAlignment` | 供 `List` 使用。标记在其列内的对齐方式，`Left` 或 `Right`。 | `Left` |
| `MarkerOffset` | `double` | 供 `List` 使用。决定列表标记之后留多少间距。 | `double.NaN` |
| `MarkerStyle` | `TextMarkerStyle` | 供 `List` 使用。选择列表标记的样式，比如 `Disc`、`Decimal`、`LowerLatin`。 | `Null` |
| `Padding` | `Thickness` | 块的边框与其内容之间的内侧间距。 | `Null` |
| `RowSpan` | `int` | 供 `TableCell` 使用。单元格纵跨的行数。 | 1 |
| `StartIndex` | `int` | 供 `List` 使用。指定编号列表的起始序号。 | 1 |
| `TabStopPositions` | `IReadOnlyList<double>?` | 块中文本的制表位位置。 | `Null` |
| `TextAlignment` | `TextAlignment` | 块中文本的对齐方式，即 `Left`、`Center`、`Right`、`Justify`。 | `Null` |
| `TextDecorations` | `TextDecorations` | 作用于块中文本的装饰线，比如 `Underline`、`Overline`、`Strikethrough`。 |
| `TextIndent` | `double` | 首行文本之前的缩进宽度。设为负值可以做出悬挂缩进。 | `double.NaN` |
| `VerticalAlignment` | `VerticalAlignment` | 供 `TableCell` 使用。单元格内容在行高范围内的对齐方式，`Top`、`Center` 或 `Bottom`。 | `Top` |
| `WidowControl` | `bool` | 供 `Paragraph` 使用。确保分页符两侧各至少留有两行该段落的文字。 | `true` |

## 行内元素 {#inline-elements}

行内元素用于指定块内部的内容样式。

| 元素 | 说明 |
| --- | --- |
| `RichBold` | 表示加粗文本。会覆盖全局的 `FontWeight` 属性。 |
| `RichFootnoteCitation` | 对某条注释的再次引用，其锚点在别处。通过 `NoteId` 与 `Footnote` 配对。 |
| `RichFootnoteReference` | 脚注的原子锚点，通过 `NoteId` 与 `FlowDocument.Footnotes` 中的 `Footnote` 配对。 |
| `RichHyperlink` | 标记一个行内超链接。 |
| `RichImage` | 行内图片。内容来自 `RichImageSource`，只占一个对象替换字符。 |
| `RichInline` | 行内元素的抽象基类。 |
| `RichInlineUIContainer` | 用于把 UI 元素嵌入文本流的包装器。 |
| `RichItalic` | 表示斜体文本。会覆盖全局的 `FontStyle` 属性。 |
| `RichLineBreak` | 强制换行。 |
| `RichPageNumberField` | 页码字段，`CurrentPage` 或 `PageCount`。它不存储任何数字：值来自分页结果，因此同一条页眉带在每页渲染出的号码各不相同。 |
| `RichRun`| 最基本的文本段，支持字符级格式设置。文本内容由 [`Text` 属性](#properties-1)指定。 |
| `RichSpan` | 把其他行内元素归为一组的行内元素。 |
| `RichSubscript` | 表示下标文本。会把 `BaselineAlignment` 属性设为 `Subscript`。  |
| `RichSuperscript` | 表示上标文本。会把 `BaselineAlignment` 属性设为 `Superscript`。 |
| `RichUnderline` | 表示带下划线的文本。会覆盖全局的 `TextDecorations` 属性。 |

### 属性 {#properties-1}

| 属性 | 类型 | 使用者 | 说明 |
| --- | --- | --- | --- |
| `AltText` | `string?` | `RichImage` | 图片的替代文字。 |
| `Child` | `Control` | `RichInlineUIContainer` | 指定要放进行内容器的控件。 |
| `Height` | `double` | `RichImage` | 显示高度，单位为设备无关像素。未设置时采用图片的固有高度。 |
| `IsVisited` | `bool` | `RichHyperlink` | 该超链接是否已被访问过。 |
| `Kind` | `PageNumberFieldKind` | `RichPageNumberField` | `CurrentPage` or `PageCount`. |
| `NavigateUri` | `Uri?` | `RichHyperlink` | 点击超链接时导航到的 URI。 |
| `NoteId` | `int` | `RichFootnoteReference`, `RichFootnoteCitation` | 把锚点与它的 `Footnote` 配成一对。 |
| `Source` | `RichImageSource?` | `RichImage` | 图片内容，可以是 `EmbeddedImageSource`、`DeferredImageSource` 或 `PixelImageSource`。 |
| `Text` | `string` | `RichRun` | 获取或设置文本内容。读写的是所附着的 `TextDocument`；若未附着，则使用本地存储。 |
| `ToolTip` | `object?` | `RichHyperlink` | 与超链接关联的工具提示。 |
| `UnderlineStyle` | `UnderlineStyle?` | 所有行内元素 | 下划线的样式，比如 `Single`、`Double`、`Dotted`、`Wave`。可继承。 |
| `Width` | `double` | `RichImage` | 显示宽度，单位为设备无关像素。未设置时采用图片的固有宽度。 |

### RichHyperlink 伪类 {#richhyperlink-pseudoclasses}

超链接文本的状态发生变化时，`RichHyperlink` 会置上下列伪类。

- `:pointerover`：指针停在超链接上时。
- `:pressed`：超链接被点击时。
- `:visited`：超链接至少被点击过一次之后。

## Architecture

Avalonia 富文本编辑器把各项职能拆分成八层架构。

| 层 | 名称 | 说明 | 核心组成 |
| --- | --- | --- | --- |
| 1 | 文档模型 | 文本内容与文档层级的核心数据存储。采用 rope 数据结构，以求存储和操作的高效。 | `TextDocument`, `FlowDocument` |
| 2 | 文本指针 API | 在文档内进行位置跟踪与导航。位置的变更由 `TextRange` 统一负责。 | `TextPointer`, `TextRange`, `LogicalDirection` |
| 3 | Rendering | 视觉呈现、坐标映射、命中测试、行查询。视图可以通过组件或高亮层来扩展，但不能通过派生子类扩展。 | `ITextView`, `TextViewBase`, `InteractiveTextView`, `PagedTextView`, `ITextLine`, `DocumentNode` |
| 4 | Editing | 处理来自键盘、鼠标或其他设备的用户输入。 | `TextSelection`, `TextViewKeyboard`, `TextViewMouse`, `TextEditorKeyboard`, `CaretElement` |
| 5 | Highlighting | 用于高亮的视觉效果，服务于选区、批注、查找/替换等场景。 | `IHighlightLayer`, `HighlightLayerBase`, `HighlightLayerCollection`, `SelectionHighlightLayer` |
| 6 | Undo/Redo | 保存操作历史以支持回退。`UndoManager` 是唯一的 sealed 实现，没有可供替换的撤销接口。 | `UndoManager`, `IUndoUnit`, `IUndoScope`, `SelectionSnapshot` |
| 7 | Serialization | 以多种格式（RTF、DOCX、XAML、HTML、Markdown、PDF、纯文本）导入导出文档。序列化器是同步的，且不依赖 UI。 | `IDocumentSerializer`, `DocumentSnapshot`, `DocumentSnapshotBuilder` |
| 8 | 面向用户的控件 | 把以上各层整合进一个模板化的 Avalonia 控件。 | `RichTextEditor`、`FlowDocumentScrollViewer`、`FlowDocumentPageViewer`、`FlowDocument`，以及块级和行内元素 |

## 另请参阅 {#see-also}

- [文档阅读器](/controls/input/text-input/richtexteditor/document-viewer) —— 只读的 `FlowDocumentScrollViewer` 怎么搭
- [工具栏与选区浮层](/controls/input/text-input/richtexteditor/toolbar) —— 定制工具栏、迷你工具条和上下文菜单
- [扩展范式](/controls/input/text-input/richtexteditor/extension-patterns) —— 自定义节点、高亮层、序列化器和组件
- [Performance Tuning](/controls/input/text-input/richtexteditor/performance-tuning)
- [Thread Safety](/controls/input/text-input/richtexteditor/thread-safety)
- [疑难排查](/troubleshooting/controls/richtexteditor)