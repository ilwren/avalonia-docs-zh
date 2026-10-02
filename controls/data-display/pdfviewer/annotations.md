---
id: annotations
title: 批注、表单与涂黑删除
description: 使用 Avalonia 中 PdfViewer 的批注工具：文本标记、手绘、形状、便签、图章、链接、涂黑删除、表单填写以及撤销/重做。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

用户从工具栏挑一件工具，然后在页面上画。每一次改动都纳入撤销与重做，并在保存时写入文件。

批注相关的方法接受从 0 开始的页码索引和 PDF 页面坐标：原点在页面左下角，单位是 PDF 点（1/72 英寸）。

## Tools

`ActiveTool` 决定下一次指针手势所使用的工具。内置工具栏读写的正是这同一个属性，所以即便隐藏了工具栏，你自己的控件照样能激活任意工具。`SetToolCommand` 通过命令参数来设置它，参数可以是 `PdfViewerTool` 的值，也可以是它的名称。只要 `CanEditAnnotations` 为 `false`，`ActiveTool` 就一直保持 `None`。

| `PdfViewerTool` | 快捷键 | 结果 |
|---|---|---|
| `Highlight`, `Underline`, `Strikeout`, `Squiggly` | 在文本上拖动 | 一条采用当前工具颜色的文本标记批注。 |
| `Redact` | 在文本上拖动 | 把覆盖范围内的内容从页面上删除。参见[涂黑删除](#redaction)。 |
| `Draw` | 随手拖画 | 一条带 `DrawStrokeColor` 和 `DrawStrokeWidth` 的手绘批注。 |
| `Shape` | 拖出一个方框 | `SelectedShapeType` 中所选的形状：`Line`、`Arrow`、`Rectangle`、`Circle`、`Polygon`、`Star` 或 `Text`。未设置时为矩形。 |
| `Text` | 点击或拖动 | 一个采用 `TextAnnotation*` 排版设置的文本框。 |
| `Note` | Click | 一张便签，带就地编辑器和配色色块。 |
| `Link` | 拖出一个方框 | 一条链接批注。会弹出对话框询问 URL。 |
| `Stamp` | Click | 从工具栏下拉菜单中选出的橡皮图章。参见[图章](#stamps)。 |
| `None` | 点击或拖动某条批注 | 选中、移动、缩放、改样式、复制、粘贴和删除已有的批注。 |

```xml
<pdf:PdfViewer x:Name="Viewer" ActiveTool="Highlight" />

<Button Content="Draw"
        Command="{Binding #Viewer.SetToolCommand}"
        CommandParameter="Draw" />
```

在 Acrobat、预览（Preview）等其他应用中创建的批注同样可以编辑。它们的作者、日期、主题、不透明度和各类标志都会保留；移动或缩放时，形状也会保留自己原有的外观，比如虚线或云状边框。

### 工具的显示与隐藏 {#tool-visibility}

每件工具都有自己的可见性属性，因此你可以只开放工具栏的一部分。

| 属性 | 工具 |
|---|---|
| `IsHighlightToolVisible` | Highlight |
| `IsUnderlineToolVisible` | Underline |
| `IsStrikethroughToolVisible` | Strikeout |
| `IsSquigglyToolVisible` | Squiggly |
| `IsRedactToolVisible` | Redact |
| `IsDrawToolVisible` | Draw |
| `IsShapeToolVisible` | Shape |
| `IsTextToolVisible` | 文本框 |
| `IsNoteToolVisible` | 便签 |
| `IsLinkToolVisible` | Link |
| `IsStampToolVisible` | Stamp |

若想干脆禁止编辑、而不只是把工具藏起来，请使用 `IsReadOnly` 或 `AllowAnnotationEditing`。参见[文档权限](loading-and-saving.md#document-permissions)。

## 基于选区的文本标记 {#markup-from-a-selection}

选中文本后会弹出带各种标记工具的上下文菜单。同样的操作也可以用代码完成，作用于当前选区。每个方法都返回新批注在该页上的索引，失败时返回 `-1`。颜色是 `PdfAnnotationColor` 值，由 `R`、`G`、`B` 和 `A` 四个字节分量组成。

| 方法 | 说明 |
|---|---|
| `HighlightSelectionAsync(PdfAnnotationColor? color = null)` | 为选区加高亮。 |
| `UnderlineSelectionAsync(PdfAnnotationColor? color = null)` | 为选区加下划线。 |
| `StrikeoutSelectionAsync(PdfAnnotationColor? color = null)` | 为选区加删除线。 |
| `SquigglySelectionAsync(PdfAnnotationColor? color = null)` | 为选区加波浪下划线。 |
| `RedactSelectionAsync(PdfAnnotationColor? color = null)` | 对选区作涂黑删除。 |

当 `color` 为 `null` 时，采用对应的颜色属性（`HighlightColor` 等等）。

```csharp
await Viewer.HighlightSelectionAsync();
await Viewer.UnderlineSelectionAsync(new PdfAnnotationColor(0, 0, 255, 255));
```

## 便签 {#sticky-notes}

| 方法 | 说明 |
|---|---|
| `AddStickyNoteAsync(int pageIndex, double pdfX, double pdfY, string text, PdfAnnotationColor? color = null)` | 在 PDF 空间的指定位置添加一张便签。返回批注索引，失败时返回 `-1`。 |
| `UpdateStickyNoteAsync(int pageIndex, int annotIndex, string? text, PdfAnnotationColor? color)` | 修改某张便签的文字或颜色。 |
| `GetAnnotationsAsync(int pageIndex, CancellationToken)` | 把某一页的批注列为 `PdfAnnotationInfo` 项，各项带有 `AnnotationIndex`、`Type`、`Bounds`、`Color`、`Contents` 和 `Author`。 |

```csharp
int index = await Viewer.AddStickyNoteAsync(0, 72, 720, "Check this figure");
await Viewer.UpdateStickyNoteAsync(0, index, "Checked", null);
```

## Stamps

**图章**下拉菜单提供一组标签，比如 **Approved**、**Draft**、**Received**，另有样式选择器和一个**包含日期**开关。图章会保存为标准的 `/Stamp` 批注，因此其他阅读器也能正常渲染和移动。

| 属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `StampLabels` | `IReadOnlyList<string>` | `DefaultStampLabels` | 下拉菜单提供的标签，一律以大写绘制。 |
| `StampColor` | `PdfAnnotationColor?` | `null` | 所有图章的颜色。`null` 会按标签自动挑选：内置的通过类标签（Approved、Completed、Paid、Received、Reviewed、Final、For Public Release）用绿色，内置的状态类标签（Draft、For Comment、As Is、Experimental、Departmental、Copy）用蓝色，其余一律用红色，包括你自定义的标签。 |
| `StampStyle` | `PdfStampStyle` | `Classic` | 新图章的外观：`Classic`、`Flat`、`Outline`、`Legal` 或 `Pill`。该设置会随每个图章一起保存。 |
| `IncludeStampDate` | `bool` | `false` | 在新图章上加一行今天的日期。 |
| `StampDateFormat` | `string` | `dd MMM yyyy` | 日期行所用的 .NET 日期格式，采用固定区域设置。 |

`AddStampAsync(int pageIndex, string label, double pdfX, double pdfY, PdfAnnotationColor? color = null, PdfStampStyle? style = null, bool? includeDate = null)` 以 PDF 空间中的某个点为中心添加一枚图章。留为 `null` 的参数会回落到上面那些属性。

```csharp
Viewer.StampLabels = new[] { "Approved", "Rejected", "Paid" };
await Viewer.AddStampAsync(0, "Approved", 300, 700, includeDate: true);
```

## 形状与文字 {#shapes-and-text}

形状按标准 PDF 子类型保存（`/Square`、`/Circle`、`/Line`、`/Polygon`），因此在其他阅读器中依然可编辑。文本框是 `/FreeText`，曲线则保存为 `/Stamp`。`ShapeSubtypeMode` 决定带文字的形状以何种方式写入。

| `PdfShapeSubtypeMode` | 说明 |
|---|---|
| `Auto` | 不带文字的形状用标准子类型，带文字的形状用 `/Stamp`。这与 macOS 预览（Preview）的做法一致。 |
| `Standard` | 一律使用标准子类型，带文字的也不例外。若其他阅读器编辑了该形状，文字会丢失。 |
| `Strict` | 只用标准子类型。形状不能附加文字，线条也不能画成曲线。 |

文本框、形状和图章中的非拉丁文字（西里尔文、希腊文、中日韩文字等）会以字体子集的形式嵌入，因此在各种阅读器中渲染效果一致。

### 默认配色与排版 {#default-colours-and-typography}

| 属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `HighlightColor` | `PdfAnnotationColor` | 黄色，50% 透明度 | 高亮颜色。 |
| `UnderlineColor` | `PdfAnnotationColor` | Green | 下划线颜色。 |
| `StrikeoutColor` | `PdfAnnotationColor` | Red | 删除线颜色。 |
| `SquigglyColor` | `PdfAnnotationColor` | Blue | 波浪下划线颜色。 |
| `DrawStrokeColor` | `PdfAnnotationColor` | Red | 手绘线条的颜色。 |
| `DrawStrokeWidth` | `float` | `2.0` | 手绘线条的宽度，单位为 PDF 点。 |
| `ShapeFillColor` | `PdfAnnotationColor?` | White | 形状填充。`null` 表示不填充。 |
| `ShapeStrokeColor` | `PdfAnnotationColor?` | Black | 形状描边。`null` 表示不描边。 |
| `ShapeStrokeWidth` | `float` | `2.0` | 形状描边宽度，单位为 PDF 点。 |
| `SelectedShapeType` | `ShapeType` | `None` | `Shape` 工具所绘制的形状。 |
| `TextAnnotationFillColor` | `PdfAnnotationColor?` | `null` | 文本框填充。`null` 表示不填充。 |
| `TextAnnotationStrokeColor` | `PdfAnnotationColor?` | `null` | 文本框边框。`null` 表示无边框。 |
| `TextAnnotationStrokeWidth` | `float` | `1.0` | 文本框边框宽度。 |
| `TextAnnotationTextColor` | `PdfAnnotationColor` | Black | 文本框的文字颜色。 |
| `TextAnnotationFont` | `string` | `Helvetica` | 文本框字体。 |
| `TextAnnotationFontSize` | `float` | `12` | 文本框字号。 |
| `TextAnnotationFontAttributes` | `FontAttributes` | `None` | 加粗、倾斜等文字属性。 |
| `TextAnnotationTextAlign` | `TextAnnotationAlignment` | `Center` | 文本框的对齐方式。 |
| `NoteColor` | `PdfAnnotationColor` | Yellow | 便签颜色。 |

工具栏上的拾色器写入的正是这些属性。

## Redaction

`Redact` 工具和 `RedactSelectionAsync` 是把内容删掉，而不是遮住。被涂黑的字符会连同该区域下方的图像一起从页面中移除。矢量路径和表单 XObject 只有被完全覆盖时才会移除。

当 `RedactionRemovesHiddenInformation` 为 `true`（默认）时，涂黑删除还会清除 PDF 可能另存在别处的页面内容副本：标签结构树、页面内嵌的缩略图，以及文档元数据（标题、作者、关键词）。书签标题和附件不受影响。

只要 `IsRedactionUndoEnabled` 为 `true`，涂黑删除就可以撤销。每次涂黑删除都会保留一份改动前的文档副本，因此这类历史记录另有 `MaxRedactionUndoSteps` 单独限定上限。

## Forms

交互式表单字段可以用指针和键盘填写。从文档外 <kbd>Tab</kbd> 进来会落到本页第一个字段上，<kbd>Tab</kbd> 和 <kbd>Shift</kbd>+<kbd>Tab</kbd> 在各字段之间移动并显示焦点框，按 <kbd>Esc</kbd> 或从最后一个字段继续 Tab 则离开表单。表单改动同样纳入撤销与重做，并在保存时写入。

`AllowFormEditing` 可关闭表单填写。浏览器中不支持表单填写。

## 撤销与重做 {#undo-and-redo}

批注改动、表单字段改动和涂黑删除都会被记录，书签则不会。

| 成员 | 说明 |
|---|---|
| `Undo()` / `Redo()` | 套用上一条或下一条历史记录。`UndoAsync()` 和 `RedoAsync()` 会等待其完成。 |
| `CanUndo` / `CanRedo` | 是否还有可套用的历史记录。可绑定。 |
| `UndoRedoStateChanged` | 二者之一发生变化时触发。 |
| `MaxUndoSteps` | 撤销历史的深度，取值 0 到 1000，默认 `100`。取 `0` 则关闭撤销与重做。 |
| `MaxRedactionUndoSteps` | 可撤销的涂黑删除保留多少次，取值 0 到 100，默认 `10`。保留的是最近的几次。 |
| `IsRedactionUndoEnabled` | 是否记录涂黑删除。默认 `true`。 |

## Errors

用指针完成的编辑在后台执行，没有什么可等待的。订阅 `AnnotationError` 即可在操作失败时收到通知，其参数包含 `Operation`、`Message` 以及底层的 `Exception`。

```csharp
Viewer.AnnotationError += (_, e) =>
    ShowToast($"{e.Operation} failed: {e.Message}");
```

## 输出兼容性 {#output-compatibility}

每条批注保存时都会带上外观流（appearance stream），因此在 Acrobat、预览、Chrome 等阅读器中都能正常呈现。

编辑由其他应用创建的批注会重建它的外观。附在其上的回复链（`/Popup`、`/IRT`）会被丢弃，该批注也会被移到本页批注顺序的末尾。

## 另请参阅 {#see-also}

- [PdfViewer 控件](index.md)
- [加载与保存](loading-and-saving.md)
- [导航、缩放与搜索](navigation-and-search.md)
