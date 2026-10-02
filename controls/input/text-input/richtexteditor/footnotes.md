---
id: footnotes
title: 脚注
doc-type: guide
tags:
 - avalonia pro
 - avalonia enterprise
---

脚注总是由形影不离的两样东西组成：正文中的 `RichFootnoteReference` 锚点，以及承载注释内容的 `Footnote` 主体。锚点显示一个编号，主体在内容旁显示同一个编号，两者靠 `NoteId` 配对。编号本身谁都不存储，而是由该注释在全文所有注释中的位置（从 1 开始）决定。任何移动、新增或删除锚点的编辑都会让全文重新编号，而一个字符的文本都不用动。

本指南涵盖：插入注释、编辑注释、编号规则、「锚点拥有其注释」的生命周期、同一条注释的多次引用、注释在连续视图与分页视图中的呈现方式，以及文件来回存取后哪些信息能保留下来。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 插入脚注 {#inserting-a-footnote}

在编辑器中，`EditorActions.InsertFootnote` 一步到位：锚点替换掉选区，随之创建一个空的注释主体，各锚点重新编号，插入符移进新注释，可以直接开始输入。整个过程算作一个撤销单元。

```csharp
using Avalonia.Controls.Documents.Primitives.Actions;

// editor is a RichTextEditor, which implements ITextEditorHost.
if (EditorActions.InsertFootnote.CanExecute(editor))
    EditorActions.InsertFootnote.Execute(editor);
```

框架没有预设按键手势，也没有内置的工具栏按钮。要让用户用上它，请把这个动作绑到菜单项、`ButtonTool` 或你选定的某个按键上。当插入符位于页眉页脚带或另一条注释内部时，`CanExecute` 为 `false`。

在代码中，对应的动作是 `TextRange.InsertFootnote`。它返回新建的注释，其主体是一个空段落：

```csharp
using Avalonia.Controls.Documents;
using Avalonia.Controls.Documents.TextModel;

var caret = document.TextDocument.ContentEnd;
var note = new TextRange(caret, caret).InsertFootnote();

if (note is not null)
{
    var body = (Paragraph)note.Blocks[0];
    body.Inlines.Add(new RichRun("Figures are unaudited."));
}
```

由于选区本身就是一个区间，同一个调用也能作用于编辑器的实时选区，并顺带获得「替换选区」的语义：

```csharp
var note = editor.Selection?.InsertFootnote();
```

当区间起点无法承载锚点时（位于页眉页脚带内、另一条注释内，或位于没有 `FlowDocument` 根的 `TextDocument` 中），`InsertFootnote` 返回 `null` 而不是抛出异常。你也可以传入自己的锚点元素，以便预先设定它的格式，或留一个引用在手：

```csharp
var anchor = new RichFootnoteReference();
var note = editor.Selection?.InsertFootnote(anchor);
```

## 从锚点找到它的注释 {#reaching-a-note-from-its-anchor}

`FlowDocument.FindFootnote` 负责解析这层配对关系：

```csharp
Footnote? note = document.FindFootnote(anchor);
```

若锚点属于别的文档、或还没有对应的注释，它返回 `null`。全部注释存放在 `FlowDocument.Footnotes`（一个 `FootnoteCollection`）中，按锚点顺序排列，并可用 `Find(int noteId)` 按 ID 查找。文本模型拥有自己的脚注，把 `TextFootnote` 的所有实例都存在 `TextDocument.Footnotes` 里。因此，哪怕一个元素都没实体化，被快照、克隆、序列化或分页的文档也会带上全部注释。

注释集合发生变化、某条注释的 ID 或标签改变、编号格式改变时，都会触发 `FlowDocument.FootnotesChanged`。该事件会引发视图重新渲染，你也可以拿它来驱动「文档已修改」标记。

## 在 XAML 中撰写 {#authoring-in-xaml}

`FlowDocument.Footnotes` 是集合属性，因此注释与正文并列声明，并靠 ID 配对：

```xml
<FlowDocument>
    <Paragraph>
        <RichRun Text="Revenue grew twelve percent." /><RichFootnoteReference NoteId="1" />
    </Paragraph>

    <FlowDocument.Footnotes>
        <Footnote NoteId="1">
            <Paragraph>
                <RichRun Text="Constant currency, excluding the Nordic divestment." />
            </Paragraph>
        </Footnote>
    </FlowDocument.Footnotes>
</FlowDocument>
```

`NoteId` 把 `RichFootnoteReference` 和 `Footnote` 配成一对。`NoteId` 的值本身永远不会显示出来。读者看到的编号来自锚点顺序，所以调整段落顺序会让注释重新编号，而调整 `Footnote` 元素的顺序则不会。

## 编辑注释 {#editing-a-note}

注释本身就是一份独立的文档，在它渲染所在的视图中呈现：

- 双击锚点可以进入它的注释，点进注释容器同样可以。
- `EditorActions.GoToFootnote` 会进入插入符当前所在、或刚刚经过的那个锚点对应的注释。
- `EditorActions.GoToFootnoteReference` 则反其道而行：离开注释，回到正文中紧随其锚点之后的位置。
- 按 Esc 返回正文，正文的选区仍停在离开时的位置。`EditorActions.ReturnToBody` 是供按钮使用的命令形式。

插入符位于注释中时，`RichTextEditor.ActiveDocument` 就是那条注释。此时：（1）`:footnote-editing` 伪类被置上，（2）`PageBandFocusBrush` 中会有一个框标出该注释的容器，（3）`Selection`、工具栏和各项格式操作都作用于该注释。 

撤销仍与正文共用同一个栈。执行撤销时，插入符会回到当初做出该次编辑的那份文档中。

由于注释是独立文档，正文的选区永远不会伸进注释里；在正文中按 <kbd>Ctrl</kbd>+<kbd>A</kbd> 只会选中正文；删除字符也绝不会越过注释的边界。

## Numbering

`FlowDocument.FootnoteNumberFormat`（它镜像的是真正持有该值的 `TextDocument.FootnoteNumberFormat`）为整篇文档设定编号格式。编号按锚点顺序连续排列。

| `FootnoteNumberFormat` | 序列 |
|---|---|
| `Decimal` (default) | 1, 2, 3 |
| `LowerRoman` | i、ii、iii |
| `UpperRoman` | I, II, III |
| `LowerLatin` | a、b、c，然后 aa、ab |
| `UpperLatin` | A、B、C，然后 AA、AB |
| `Symbols` | 星号、剑标、双剑标、分节符、双竖线、段落符。第七条注释起每个符号翻倍，第十三条起三倍，依此类推。 |

```csharp
document.FootnoteNumberFormat = FootnoteNumberFormat.Symbols;
```

设置它算作一个撤销单元，会让每个锚点和每条注释的编号重新渲染；由于没有任何数字被存储下来，文本本身不会有任何改动。在文档的 `TextDocument` 尚不存在时设置的值，会在它创建时生效；而嵌套文档（比如页眉页脚带、注释）会忽略自己的取值，一律跟随所有者。

锚点的编号以上标字号绘制在上标基线上。注释自身的编号则遵循编号列表的规则：字体、字号和颜色取自注释的第一段文本，位置在注释左缘的一条竖带中——这条竖带由全文所有注释共用，宽度足以容纳文档中最大的序号。因此，给 `Footnote` 加一条主题 setter，就能把注释正文和它的编号一并改样式：

```xml
<Style Selector="Footnote">
    <Setter Property="FontSize" Value="10" />
    <Setter Property="Foreground" Value="#555555" />
</Style>
```

## 锚点拥有它的注释 {#anchor-owns-its-note}

```csharp
paragraph.Inlines.Add(anchor);      // creates the paired empty note
paragraph.Inlines.Remove(anchor);   // the note leaves with the anchor
otherParagraph.Inlines.Add(anchor); // and comes back, content intact
```

锚点被移除时，它会保住注释的内容，就像脱离文档的 `RichRun` 会保住自己的文本一样。把锚点重新插回去——无论是插回原文档还是另一份文档——这一对就复原了；换句话说，移动锚点即可搬走整条注释。

同理，删除锚点会把注释一并删掉，其余脚注会在同一次操作中重新编号。撤销则会把那条注释连同内容一起找回来。内容被清空的注释仍留在脚注集合中，除非它的锚点也被删除。

复制一段含有锚点的区间时，注释也会被一并复制。粘贴这段内容会克隆出一条带新 ID 的注释。

单独粘贴一个锚点会被丢弃。往页眉页脚带或注释主体里粘贴锚点同样会被丢弃，因为它们承载不了锚点。

## 同一条注释引用两次 {#citing-one-note-twice}

一条注释有且只有一个锚点。要再次引用它，请用 `RichFootnoteCitation`——它按 `NoteId` 指向某条注释，但并不拥有它：

```csharp
paragraph.Inlines.Add(new RichFootnoteCitation { NoteId = anchor.NoteId });
```

它的呈现与锚点别无二致，编号也完全相同：由注释的位置推算得出，不存储在任何地方，所以新增或删除注释会让它的每一处引用一并重新编号。真正的区别在于归属：

| &nbsp; | `RichFootnoteReference` | `RichFootnoteCitation` |
|---|---|---|
| 插入时会创建一条注释 | Yes | No |
| 删除它会连带删除注释 | Yes | No |
| 可以出现在注释主体内 | No | Yes |
| 粘贴时不带上注释 | Dropped | Dropped |

如上表所示，在一条注释内部引用另一条已有的注释是允许的。此时该引用按拥有这条注释的那份文档来编号。

## 注释如何呈现 {#how-notes-render}

注释主体从来都不是文档的块，所以任何块级样式选择器都够不着它们，它们也不会与正文一起流排。

**连续布局**（`FlowDocumentScrollViewer`，以及 `DocumentViewMode.Continuous` 中的 `RichTextEditor`）把文档的所有注释显示为末个块下方的一个区域，上面有一条分隔线，按锚点顺序每条注释一个容器。只要文档里有注释，这个区域就会出现；它的高度算在布局内边距里，因此滚动范围和滚动锚定都会把它计算在内。

**分页布局**（`FlowDocumentPageViewer`、`DocumentViewMode.PageLayout` 中的 `RichTextEditor`）把每条注释放在其锚点所落页面的底部，就像 MS Word 那样：

- 含有锚点的行会在页底之上预留出相应注释的高度，有注释的页面还会各加一条分隔线。
- 若某一行在高度被压缩后放不下了，它会连同自己的注释一起挪到下一页——锚点与它的注释永远同处一页。
- 编辑注释会让它所在的页面重新排版。
- 比所在页面还高的注释按空页规则安置。

点进注释会把插入符放到该注释的文档中。命中测试和插入符的几何计算在容器内部照常工作。`EnsurePositionVisible` 能够抵达屏幕外页面上的注释，或流排末尾的注释。

## 来回存取 {#round-trip}

注释是作为 `DocumentSnapshot.Footnotes` 上的嵌套快照随行的，所以 `FlowDocument.Clone`、`FromSnapshot` 和结构性撤销都会保全它们，下列各种格式也都从同一处读写它们。

| 格式 | 注释支持情况 |
|---|---|
| XAML | 完整：主体、ID、标签以及编号格式 |
| DOCX | 完整：作为 Word 脚注 |
| RTF | 完整：作为 RTF 脚注组 |
| Markdown | 可读可写，按名称寻址：`[^label]` 引用与 `[^label]: ...` 定义。参阅 [Markdown 序列化](/controls/input/text-input/richtexteditor/markdown-serialization) |
| PDF | 只写，排在锚点所在页的底部，与分页视图完全一致 |
| 纯文本 | 锚点不写出任何内容，所有嵌入对象都是如此 |

在要求名称的格式里，`note.Label` 就是注释的名字，它从不显示出来。在 `RichTextEditor` 控件中创建的注释默认没有 `Label`，写入其他格式时会按位置自动命名。若你希望输出文件里的名字稳定且可读，可以显式设置 `Label`：

```csharp
note.Label = "constant-currency";
```

## 另请参阅 {#see-also}

- [分页](/controls/input/text-input/richtexteditor/pagination) —— 注释如何参与一页内容的填充
- [页眉与页脚](/controls/input/text-input/richtexteditor/headers-and-footers) —— 页面承载的另一种嵌套文档
- [Markdown 序列化](/controls/input/text-input/richtexteditor/markdown-serialization) —— markdown 的引用与定义如何映射到注释
