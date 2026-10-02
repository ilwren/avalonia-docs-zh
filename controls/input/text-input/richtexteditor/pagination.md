---
id: pagination
title: 分页
doc-type: guide
tags:
 - avalonia pro
 - avalonia enterprise
---

分页输出——`FlowDocumentPageViewer` 的分页视图、处于 `DocumentViewMode.PageLayout` 的编辑器，以及 [PDF 导出](/controls/input/text-input/richtexteditor/pdf-export)——都是逐行填充页面，并随时向文档确认一页可以在哪里结束。本指南讲如何控制页面布局：显式分页符、三条保持规则，以及各小节自己的页面设置。

连续视图对这些一概无视，只会把分页符标记画出来。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 输出完全一致 {#identical-output}

分页引擎有两个：分页视图的填充遍历，以及 PDF 分页器。两者内部机制各不相同，但判断一页在哪里结束时遵循的是同一套规则。于是同一份文档在屏幕上和在 PDF 导出中，都在同样的位置断页。

## 显式分页符 {#explicit-page-breaks}

框架里没有「分页符」这种元素。一个分页符就是加在某个块上的一项请求：`Block.BreakPageBefore`。

```csharp title="C#"
heading.BreakPageBefore = true;
```

```xml title="XAML"
<Paragraph BreakPageBefore="True" FontSize="18" FontWeight="Bold">
    <RichRun Text="Appendix A" />
</Paragraph>
```

在编辑器中，<kbd>Ctrl</kbd>+<kbd>Enter</kbd>（macOS 上是 <kbd>Cmd</kbd>+<kbd>Return</kbd>）会在插入符处应用 `BreakPageBefore`，并替换掉当前选区。该操作算作一步撤销。分页符对内容的影响取决于插入符的位置：

- 位于块边界时，它给后一个块置上 `BreakPageBefore`。
- 位于内容中间时，它像按 <kbd>Enter</kbd> 那样把块一分为二。

删除一个分页符会导致段落合并：被标记的段落与它前面的邻居合为一体，标记也随之消失。若无法合并，则这次删除只是把标记清掉。

显式分页符永远压过保持规则。强制断页从不为保持规则作让步。

这个标记只存在一处，并能在所有格式之间往返：

- 在 DOCX 中它写作 `w:pageBreakBefore`（包含由样式定义的分页符），读取时则对应 `w:br`。
- 在 RTF 中它写作 `\pagebb`，读取时对应 `\page`。
- 在 XAML 和纯文本中，它以换页符作为被标记块的分隔符写出，读取时再把换页符映射回该标记。

### 在连续视图中查看分页符 {#seeing-breaks-in-the-continuous-view}

连续视图会在被标记的块顶边画一条虚线，类似 MS Word 的草稿视图。它只是画出来而已，绝不影响布局。

| 成员（位于 `TextViewBase` 上） | 默认值 | 含义 |
|---|---|---|
| `ShowPageBreakMarkers` | `true` | 是否绘制这条线 |
| `PageBreakMarkerBrush` | `DocumentPageBreakMarkerBrush` | 线的颜色 |

## 保持规则 {#keep-rules}

有三个属性决定自动断页落在哪里。三者都只会把断点往前挪，绝不会往后推。三者都能在 DOCX、RTF 和 XAML 之间往返；HTML 读取器会把 `break-inside: avoid`、`break-after: avoid` 和 `orphans`/`widows` 映射到它们上面。

| 属性 | 效果 | DOCX | RTF |
|---|---|---|---|
| `Block.KeepTogether` | 把整个块挪到下一页，而不是把它拆开 | `w:keepLines` | `\keep` |
| `Block.KeepWithNext` | 让该块的结尾与下一个块的开头留在同一页 | `w:keepNext` | `\keepn` |
| `Paragraph.WidowControl` | 确保分页符两侧各至少留有两行该段落的文字 | `w:widowControl` | 关闭时为 `\nowidctlpar` |
<br />

```csharp
heading.KeepWithNext = true;      // a heading never ends a page alone
table.KeepTogether = true;        // this table moves rather than splits
paragraph.WidowControl = false;   // let this paragraph strand a single line
```

若某个块本身就比一整页还高，`KeepTogether` 也拦不住它被分页。

`KeepWithNext` 可以串联：连续几个被标记的块（比如标题、副标题和第一段）会作为一个整体一起挪动。和 `KeepTogether` 一样，若整条链比一页还长，它同样拦不住分页。

### 孤行控制 {#widow-control}

`Paragraph.WidowControl` 默认为 `true`，意即至少两行留在本页、至少两行挪到下页。因此三行的段落根本不会被拆开。

若允许段落落下孤零零一行，把它关掉即可：

```csharp
foreach (var block in document.Blocks)
{
    if (block is Paragraph paragraph)
        paragraph.WidowControl = false;
}
```

这个默认值只对没有另行设置的段落生效。从 DOCX 或 RTF 加载的文档一律以文件中的设定为准，包括由样式定义的值。

## 逐小节的页面设置 {#per-section-page-setup}

`Section` 可以声明自己的页面设置。未声明时，`PageWidth`、`PageHeight` 和 `PagePadding` 继承自文档的属性定义，或外层小节的定义。

只要声明了这三个属性中的**任意一个**，该小节就是一个页面几何小节：

- 它从新的一页开始，其后的内容也要另起一页。
- 它的页面采用它自己的页面尺寸和页边距。
- 它的内容按它自己的内容宽度测量和折行。
- 进入和离开它都算断页边界，因此它会像显式分页符那样切断「与下段同页」的链条。

```xml title="XAML"
<Section PageWidth="1056" PageHeight="816" PagePadding="48">
    <Paragraph FontSize="18" FontWeight="Bold">
        <RichRun Text="Wide Tables" />
    </Paragraph>
    <Paragraph>
        <RichRun Text="This section is US Letter on its side." />
    </Paragraph>
</Section>
```

```csharp title="C#"
using Avalonia;
using Avalonia.Controls.Documents;

var landscape = PageSizes.Landscape(PageSizes.Letter);
var section = new Section
{
    PageWidth = landscape.Width,
    PageHeight = landscape.Height,
    PagePadding = new Thickness(PageSizes.Inches(0.5)),
};
```

没有页面设置的小节只是个纯粹的分组容器，不具备任何页面语义。页眉页脚带则完全不理会小节的页面几何。

在分页视图中，每个小节都按它指定的页面尺寸渲染，并在宽度方向居中。翻页、`CurrentPageNumber`、适应缩放和滚动几何都随这种可变的页面堆叠而变——滚动进入横向小节时，会重新适配更宽的纸面。

PDF 导出为每一页输出一个 `MediaBox`，断页位置与屏幕上完全一致。

有一个「统一纸张」的覆盖开关：在阅读器上显式设置 `PageSize` 或 `PageMargins`，或设置 `PdfSerializerOptions.PageSize` 和 `Margins`，会让所有页面尺寸一致。此时有独立页面设置的小节依然会另起一页，但不会获得它所要求的页面设置。

小节的页面设置能在 DOCX（`sectPr`）、RTF 和 XAML 之间往返，也会随区间快照和 `Clone` 一起传递。

## 内容如何填满一页 {#how-content-fills-a-page}

作为参照，分页策略所依托的填充规则如下：

- 页面逐行填充。放不下的那一行会另起一页，并恰好从内容顶端开始，它上方的间距在页顶被吞掉。
- 比一页还高的行会溢出。
- 段落可以从内容中间拆开。
- 列表可以在条目之间拆开，也可以在条目内部拆开。
- 表格只在行与行之间拆开，绝不从一行中间穿过。被跨行单元格覆盖的各行会与它们的锚定行一起挪动。网格在断点之上收口，在断点之下重新展开。
- 被拆开的元素仍是同一个元素，只是几何形状跨越了页面。选择、复制、放置插入符和命中测试在片段中间照常可用。

脚注也参与填充。含有锚点的行会在所在页底部预留出相应注释的高度，放不下的行会连同注释一起挪到下一页。参阅[脚注](/controls/input/text-input/richtexteditor/footnotes)。

超出页边距的页眉或页脚会压缩该页的正文高度。参阅[页眉与页脚](/controls/input/text-input/richtexteditor/headers-and-footers)。

## 另请参阅 {#see-also}

- [PDF 导出](/controls/input/text-input/richtexteditor/pdf-export) —— 同一套策略，只是写进了文件
- [页眉与页脚](/controls/input/text-input/richtexteditor/headers-and-footers) —— 页眉页脚带，以及那个会压缩页面的距离
- [脚注](/controls/input/text-input/richtexteditor/footnotes) —— 注释在所属页底部预留的空间
