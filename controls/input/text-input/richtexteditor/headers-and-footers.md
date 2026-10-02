---
id: headers-and-footers
title: 页眉与页脚
doc-type: guide
tags:
 - avalonia pro
 - avalonia enterprise
---

这里所说的页眉或页脚是一个 `PageBand`：它是一份小文档，由拥有它的文档持有，并在它所服务的每张纸面上重复出现。每条带都有一个 `Role`（页眉或页脚）和一条 `Rule`，用来声明它负责哪些页面；`Section` 也可以显式指名某条带，因此一条带可以服务任意多个小节。

本指南涵盖：构建页眉页脚带、页码、某一页用哪条带、与纸面边缘的距离、就地编辑带，以及如何在连续视图中显示通栏的页眉页脚。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 通栏页眉与页脚 {#running-header-and-footer}

`FlowDocument.PageBands` 是集合属性，因此页眉页脚带与正文并列声明：

```xml
<FlowDocument PageWidth="816" PageHeight="1056" PagePadding="72">
    <FlowDocument.PageBands>
        <PageBand Role="Header" Rule="Default">
            <Paragraph FontSize="11">
                <RichRun Text="Quarterly Report" />
            </Paragraph>
        </PageBand>
        <PageBand Role="Footer" Rule="Default">
            <Paragraph FontSize="11" TextAlignment="Center">
                <RichRun Text="Page " />
                <RichPageNumberField />
                <RichRun Text=" of " />
                <RichPageNumberField Kind="PageCount" />
            </Paragraph>
        </PageBand>
    </FlowDocument.PageBands>

    <Paragraph>
        <RichRun Text="Body text." />
    </Paragraph>
</FlowDocument>
```

同样的页脚，用代码写出来是这样：

```csharp
using Avalonia.Controls.Documents;
using Avalonia.Media;

var footer = new PageBand { Role = PageBandRole.Footer, Rule = PageBandRule.Default };
var line = new Paragraph { TextAlignment = TextAlignment.Center };
line.Inlines.Add(new RichRun("Page "));
line.Inlines.Add(new RichPageNumberField());
line.Inlines.Add(new RichRun(" of "));
line.Inlines.Add(new RichPageNumberField { Kind = PageNumberFieldKind.PageCount });
footer.Blocks.Add(line);

document.PageBands.Add(footer);
```

在文档的 `TextDocument` 尚不存在时添加的带会处于待定状态，和块一样，所以标记的书写顺序无关紧要，由 XAML 填充的文档也依然保持惰性。

`TextDocument.PageBands` 独占 `TextPageBand` 的所有实例。`FlowDocument.PageBands` 会按需实体化出一个 `PageBand` 元素。不论是否有元素被实体化，带都会随文档一起被快照、克隆和导出。此外，它的撤销并入所有者的栈；移除它时，各小节对它的引用也会一并清除。嵌套文档、带或脚注都不能拥有带。

带集合发生变化、或某条带的角色或规则改变时，会触发 `FlowDocument.PageBandsChanged`。

## 页码 {#page-numbers}

`RichPageNumberField` 是一个行内元素，代表一个取决于分页（而非文档）的数字，所以同一个页眉在每张纸面上都渲染出不同的号码，而且没有任何数字被存下来。该字段只占一个对象替换字符，并针对它所落的页面求值。

| `Kind` | 求值结果 | MS Word 对应项 |
|---|---|---|
| `CurrentPage` (default) | 该字段所落页面的页码 | PAGE |
| `PageCount` | 文档的总页数 | NUMPAGES |
<br />

在编辑器中，`EditorActions.InsertPageNumber` 插入 `CurrentPage`，`EditorActions.InsertPageCount` 插入 `PageCount`，两者都只在插入符位于带内时才可用。在正文中，这些字段只会显示一个缓存的结果。

模型层的动作是 `TextRange.InsertPageNumberField(kind)`。它算作一个撤销单元，且在[脚注](/controls/input/text-input/richtexteditor/footnotes)主体中会被拒绝，因为注释没有「页」的概念。

该字段作为一个不可分割的整体参与编辑。完全没有分页的布局视作只有一页。

## 某一页用哪条带 {#which-band-a-page-gets}

每条带都带着一条 `Rule`，声明它自己负责哪些页面：

| `PageBandRule` | 负责范围 |
|---|---|
| `Default` | 其他带都不认领的每一页，即通栏带 |
| `FirstPage` | 文档的首页 |
| `EvenPage` | 没有被显式认领的偶数页；它的存在本身就意味着启用对开页 |
| `None` | 自身不认领任何页面；只在被某个小节引用处显示 |
<br />

顶层的 `Section` 也可以通过四个属性直接指向某条带，无论那条带自身的规则如何：`Header` 和 `Footer` 用于通栏页面，`FirstPageHeader` 和 `FirstPageFooter` 用于首页。设置首页属性，正是让该小节首页「与众不同」的开关；设置一条尚无归属的带会把它收归本文档所有，而属于其他文档的带则会被拒绝。

分页视图和 PDF 导出共同遵循 `PageBandPolicy` 这一条规则，按角色依下列顺序逐一尝试：

1. 小节的首页引用，用于该小节的首页。
2. 文档的 `FirstPage` 带，用于第一页。
3. 文档的 `EvenPage` 带，用于偶数页。
4. 小节的通栏引用。
5. 文档的 `Default` 带。

某个角色在规则中没有对应的带，并不会让页面留白：通栏带会顶上。真正求值为空的，才什么都不显示。对于给定的角色和规则，排在最前面的那条带才是该规则所采用的。

你也可以直接向这套策略发问，这在做预览面板或写测试时很有用：

```csharp
PageBand? header = PageBandPolicy.Resolve(
    document,
    section: null,           // null for content at the document root
    PageBandRole.Header,
    isSectionFirstPage: true,
    pageNumber: 1);
```

`document.PageBands.Find(PageBandRole.Header, PageBandRule.Default)` 按角色和规则查找带，`Find(Guid id)` 则按小节引用和快照所用的标识 `PageBand.Id` 来查找。

## 带的边距，以及会挤占正文的带 {#band-distance-and-bands-that-push-the-body}

从纸面边缘到带的距离归文档所有，因为它决定了分页的位置。

| 成员 | 含义 |
|---|---|
| `TextDocument.PageBandDistance` | `double?`。模型中的取值，未设置时为 null。 |
| `TextDocument.ResolvePageBandDistance()` | 实际采用的值，未设置时回落到默认值。 |
| `FlowDocument.PageBandDistance` | 元素一侧的镜像。`NaN`（默认）表示交给回落值决定。 |
| `PagedTextView.PageBandDistance`, `RichTextEditor.PageBandDistance` | 视图层的入口。设置其中之一会回写到文档，而它们各自遵循文档自带的那个距离。 |

`PageBandPolicy.DefaultDistance` 是回落值，12.5 毫米，约合半英寸，也是文字处理软件的通行默认值。

```csharp
document.PageBandDistance = PageSizes.Inches(0.75);
```

由于这个值归文档所有，分页视图和 PDF 导出会在同一份文档的同样位置断页。

当带加上它的边距超出了所在页边距时，带不会被裁掉，而是页面正文从页眉下方开始、或在页脚上方结束。因此同一小节的各页正文高度可能不同——更高的首页带或偶数页带会压缩它自己那一页。

## 就地编辑页眉页脚带 {#editing-bands-in-place}

在 `DocumentViewMode.PageLayout` 中，编辑器会把每张纸面上解析出的页眉和页脚显示为可操作的实时内容。点进其中一处，编辑器的选区就切换到那条带的文档。整篇文档及其所有带共用一个编辑器、一个插入符、一套工具栏和一个撤销栈。

| 成员 | 含义 |
|---|---|
| `RichTextEditor.ActiveDocument` | 插入符所在的带；在正文中时为 null |
| `ActiveDocumentChanged` | 插入符进入或离开带时引发 |
| `ActivateDocument(document, position)` | 进入某条带，或用 `null` 返回正文 |
<br />

插入符位于带中时，会出现下列情况：

- `:band-editing` 伪类被置上
- `PageBandFocusBrush` 中会有一个框标出该带的位置
- `Selection` 即为该带的对应值
- `ToolbarTargetAreas.PageBand` 让工具栏按钮可以只针对带生效。

<kbd>Esc</kbd> 返回正文，正文的选区仍停在离开时的位置。

## 带相关的命令 {#band-commands}

带相关的命令都在 `EditorActions` 上，每一条都算作一个撤销单元：

| 动作 | 行为 |
|---|---|
| `GoToHeader` / `GoToFooter` | 进入插入符所在页的带。若该页还没有带，则创建文档的通栏带。如果当前是连续视图，编辑器会切换到分页布局。 |
| `RemoveHeader` / `RemoveFooter` | 移除插入符所在的带，或插入符所在页所显示的那条带。各小节对它的引用也会一并移除。 |
| `DifferentFirstPage` | 添加或移除文档的首页带。派生状态。 |
| `DifferentOddAndEvenPages` | 添加或移除文档的偶数页带。派生状态。|
| `LinkToPrevious` | 把插入符所在的顶层小节关联到通栏带，或给它一套自己的带——由它各页原本显示的内容克隆而来。 |
| `InsertPageNumber` / `InsertPageCount` | 在带中插入相应的字段。 |
| `ReturnToBody` | <kbd>Esc</kbd> 的命令形式，即返回正文，并回到离开时的选区。 |

```csharp
if (EditorActions.GoToFooter.CanExecute(editor))
    EditorActions.GoToFooter.Execute(editor);
```

随附工具栏「插入」分组中的 `PageBandFlyoutTool` 把这些命令连同带边距一并呈现出来；带内部的上下文菜单则提供这些字段以及返回正文的入口。

## 连续视图中的页眉页脚带 {#bands-in-the-continuous-view}

连续流排类似 MS Word 的草稿视图：只显示正文，页面级的边饰不在其内。打开 `ShowPageBandsInContinuousLayout` 可以在首个块之上显示文档的通栏页眉、在末个块之下显示通栏页脚：

```xml
<RichTextEditor ShowPageBandsInContinuousLayout="True" />
<FlowDocumentScrollViewer ShowPageBandsInContinuousLayout="True" />
```

该属性默认关闭，定义在 `TextViewBase` 上，因此只读阅读器也能用。启用后会显示下列内容：

- 只显示通栏（`Default`）带。首页带、偶数页带以及小节自有的带都是「页」的概念，只在分页布局中出现。
- 用的是与纸面相同的那些容器，因此带在这里同样可以就地编辑。`GoToHeader` 和 `GoToFooter` 会留在连续布局中，不会切换到分页布局。
- 页码字段显示的是缓存结果，因为这里没有页面可供求值。

## 来回存取 {#round-trip}

带是作为 `DocumentSnapshot.PageBands` 上的嵌套快照随行的，连同它的角色、规则和标识一起。`Clone`、`FromSnapshot` 和结构性撤销都会保全小节的各项引用。

- XAML、DOCX（页眉与页脚部件）和 RTF 都能读写页眉页脚带。 
- PDF 导出会输出每一页解析出来的带，含页码字段的带每页各合成一次。
- 纯文本永远看不到带。从其他文档粘贴过来的小节不会带上引用。

## 另请参阅 {#see-also}

- [分页](/controls/input/text-input/richtexteditor/pagination) —— 分页符、保持规则以及各小节的页面设置
- [PDF 导出](/controls/input/text-input/richtexteditor/pdf-export) —— 导出的每一页各自解析出哪条带
- [脚注](/controls/input/text-input/richtexteditor/footnotes) —— 页面承载的另一种嵌套文档
