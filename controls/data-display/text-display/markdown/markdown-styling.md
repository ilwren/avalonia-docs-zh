---
id: markdown-styling
title: Markdown 样式
tags:
  - avalonia pro
  - avalonia enterprise
---

`Markdown` 控件建立在共享的 FlowDocument 模型之上，渲染出的每个元素（`Paragraph`、`Section`、`Table`、`RichSpan`、`RichHyperlink` 等）都是完整的 Avalonia `StyledElement`。因此，为 Markdown 的呈现结果定制样式有两条互补的路子：

1. **DocumentNode 样式选择器**——按类型和 CSS 式的类选中元素（比如 `Paragraph.h1`、`Section.quoteBlock`）。
2. **具名资源**——覆盖字号、外边距、画刷颜色等主题取值。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## DocumentNode 样式选择器 {#documentnode-style-selectors}

由于所有文档元素都是 `StyledElement` 实例，你可以用标准的 Avalonia 样式选择器选中它们。Markdown 渲染器会给每个元素加上 CSS 式的类，于是你能只针对某种 Markdown 结构定制样式，而不波及其他。

### 可用的选择器 {#available-selectors}

下表列出默认主题所用的样式选择器。你可以在自己的应用样式中覆盖或扩展其中任意一条。

#### 块级选择器 {#block-selectors}

| 选择器 | 说明 |
|---|---|
| `:is(Block)` | 所有块级元素（段落、小节等），设定基准外边距。 |
| `:is(Block).codeBlock` | 围栏代码块。背景、边框、内边距和等宽字体。 |
| `Paragraph.header` | 所有标题段落（h1–h6）。粗体字重。 |
| `Paragraph.h1` | 一级标题。 |
| `Paragraph.h2` | 二级标题。 |
| `Paragraph.h3` | 三级标题。 |
| `Paragraph.h4` | 四级标题。 |
| `Paragraph.h5` | 五级标题。 |
| `Paragraph.h6` | 六级标题。 |
| `Section.quoteBlock` * | 引用块。左侧竖线、内边距、弱化的前景色。 |
| `Section.alertBlock` * | 所有提示块（NOTE、TIP、IMPORTANT、WARNING、CAUTION）。 |
| `Section.alertBlock.note` * | Note 提示块的边框。 |
| `Section.alertBlock.tip` * | Tip 提示块的边框。 |
| `Section.alertBlock.important` * | Important 提示块的边框。 |
| `Section.alertBlock.warning` * | Warning 提示块的边框。 |
| `Section.alertBlock.caution` * | Caution 提示块的边框。 |
| `BlockUIContainer.thematicBreak` | 水平分隔线（主题分隔）。 |
| `Table` | 表格元素。边框、单元格间距。 |
| `TableCell` | 表格单元格元素。边框。 |
| `TableRow.tableHeader` | 表头行。粗体字重。 |
| `List` | 列表元素。左内边距、行高。 |
| `ListItem` | 列表项元素。行高。 |

\* 提示块的标题（比如「Note」「Warning」）由提示块自己绘制。它们在文档中不算段落，因此没法直接选中来设样式。改为通过 `Section.alertBlock` 来设置：它的 `FontFamily`、`FontSize` 和 `Foreground` 可继承，会同时作用于标题和正文。

#### 行内选择器 {#inline-selectors}

| 选择器 | 说明 |
|---|---|
| `RichRun.code` | 行内代码片段。背景和等宽字体。 |
| `RichSpan.header` | 标题内部的行内片段。粗体字重。 |
| `RichSpan.h1` through `RichSpan.h6` | 采用标题级字号的行内片段。 |
| `RichSpan.strikeThrough` | 删除线文字装饰。 |
| `RichSpan.inserted` | 下划线文字装饰（插入的文本）。 |
| `RichSpan.marked` | 高亮/标记文本的背景。 |
| `RichHyperlink` | 超链接元素。前景色。 |
| `RichHyperlink:pointerover` | 悬停状态的超链接。下划线 + 悬停配色。 |
| `RichHyperlink:visited` | 已访问超链接的颜色。 |

#### 文档元素选择器 {#document-element-selectors}

| 选择器 | 说明 |
|---|---|
| `MarkdownCodeBlock` | 代码块元素。`Highlighter` 属性就设在这里。 |
| `MarkdownImage` | 行内图片元素。`ImageLoader` 属性就设在这里。 |

### 自定义样式示例 {#custom-styling-examples}

覆盖标题配色：

```xml
<Style Selector="Paragraph.h1">
    <Setter Property="Foreground" Value="#1a73e8" />
</Style>
<Style Selector="Paragraph.h2">
    <Setter Property="Foreground" Value="#188038" />
</Style>
```

定制引用块的外观：

```xml
<Style Selector="Section.quoteBlock">
    <Setter Property="Background" Value="#f8f9fa" />
    <Setter Property="BorderBrush" Value="#6c757d" />
    <Setter Property="BorderThickness" Value="3,0,0,0" />
    <Setter Property="CornerRadius" Value="4" />
</Style>
```

定制行内代码的样式：

```xml
<Style Selector="RichRun.code">
    <Setter Property="Background" Value="#e8f0fe" />
    <Setter Property="FontFamily" Value="Cascadia Code" />
</Style>
```

定制代码块：圆角加不同的背景：

```xml
<Style Selector=":is(Block).codeBlock">
    <Setter Property="Background" Value="#1e1e1e" />
    <Setter Property="Foreground" Value="#d4d4d4" />
    <Setter Property="CornerRadius" Value="8" />
    <Setter Property="Padding" Value="20" />
</Style>
```

限定范围的嵌套选择器同样可用。比如去掉表格内段落的外边距：

```xml
<Style Selector="Table Paragraph">
    <Setter Property="Margin" Value="0" />
</Style>
```

## 可定制的资源 {#customizable-resources}

除了样式选择器，你还可以在自己的主题或资源字典中覆盖具名资源。默认样式用的正是它们，不必重写选择器就能调整取值。

### Blocks
| 按键 | 类型 | 默认值 | 注释支持情况 |
|---|---|---|---|
| `MarkdownBlockMargin` | Thickness | `0,8` | 块的外边距 |

### Hyperlinks
| 按键 | 类型 | Default (Light) | Default (Dark) | 注释支持情况 |
|---|---|---|---|---|
| `MarkdownHyperlinkForeground` | Brush | `#0969da` | `#58a6ff` | 链接颜色 |
| `MarkdownHyperlinkForegroundVisited` | Brush | `#551A8B` | `#bc8cff` | 已访问链接的颜色 |
| `MarkdownHyperlinkForegroundPointerOver` | Brush | `#0056b3` | `#79c0ff` | 悬停链接的颜色 |

### Selection
| 按键 | 类型 | 默认值 | 注释支持情况 |
|---|---|---|---|
| `MarkdownSelectionBrush` | Brush | `#FF086F9E` | 选区高亮 |

### Code
| 按键 | 类型 | 默认值 | 注释支持情况 |
|---|---|---|---|
| `MarkdownCodeFontFamily` | FontFamily | `Courier New` | 行内/代码字体 |

### 代码块 {#code-blocks}
| 按键 | 类型 | Default (Light) | Default (Dark) | 注释支持情况 |
|---|---|---|---|---|
| `MarkdownCodeBlockParagraphPadding` | Thickness | `16` | `16` | 内边距 |
| `MarkdownCodeBlockParagraphBorderThickness` | Thickness | `1` | `1` | 边框粗细 |
| `MarkdownCodeBlockParagraphCornerRadius` | CornerRadius | `6` | `6` | 圆角半径 |
| `MarkdownCodeBlockParagraphBackground` | Brush | `#1f818b98` | `#20484f58` | 背景 |
| `MarkdownCodeBlockParagraphBorderBrush` | Brush | `#e3ebf6` | `#30363d` | 边框画刷 |

### 行内代码 {#inline-code}
| 按键 | 类型 | Default (Light) | Default (Dark) | 注释支持情况 |
|---|---|---|---|---|
| `MarkdownCodeRunBackground` | Brush | `#1f818b98` | `#20484f58` | 行内代码背景 |

### 主题分隔线 {#thematic-break}
| 按键 | 类型 | Default (Light) | Default (Dark) | 注释支持情况 |
|---|---|---|---|---|
| `MarkdownThematicBreakRectangleFill` | Brush | `#d1d9e0` | `#30363d` | 主题分隔线颜色 |

### 各级标题 {#headers-per-level}
每级标题都提供 `FontSize`、`BorderThickness`、`Padding`、`Margin` 四项。

| 按键 | 类型 | 默认值 | 注释支持情况 |
|---|---|---|---|
| `MarkdownHeader1ParagraphFontSize` | Double | `31.5` | H1 字号 |
| `MarkdownHeader1ParagraphBorderThickness` | Thickness | `0,0,0,1` | H1 下边框 |
| `MarkdownHeader1ParagraphPadding` | Thickness | `0,0,0,16` | H1 内边距（底部） |
| `MarkdownHeader1ParagraphMargin` | Thickness | `0,31,0,14` | H1 外边距 |
| `MarkdownHeader2ParagraphFontSize` | Double | `24.5` | H2 字号 |
| `MarkdownHeader2ParagraphBorderThickness` | Thickness | `0,0,0,1` | H2 下边框 |
| `MarkdownHeader2ParagraphPadding` | Thickness | `0,0,0,12` | H2 内边距（底部） |
| `MarkdownHeader2ParagraphMargin` | Thickness | `0,24.5,0,14` | H2 外边距 |
| `MarkdownHeader3ParagraphFontSize` | Double | `21` | H3 字号 |
| `MarkdownHeader3ParagraphBorderThickness` | Thickness | `0,0,0,1` | H3 下边框 |
| `MarkdownHeader3ParagraphPadding` | Thickness | `0,0,0,8` | H3 内边距（底部） |
| `MarkdownHeader3ParagraphMargin` | Thickness | `0,21,0,14` | H3 外边距 |
| `MarkdownHeader4ParagraphFontSize` | Double | `16.8` | H4 字号 |
| `MarkdownHeader4ParagraphBorderThickness` | Thickness | `0,0,0,1` | H4 下边框 |
| `MarkdownHeader4ParagraphPadding` | Thickness | `0,0,0,6` | H4 内边距（底部） |
| `MarkdownHeader4ParagraphMargin` | Thickness | `0,16.8,0,14` | H4 外边距 |
| `MarkdownHeader5ParagraphFontSize` | Double | `14` | H5 字号 |
| `MarkdownHeader5ParagraphBorderThickness` | Thickness | `0,0,0,1` | H5 下边框 |
| `MarkdownHeader5ParagraphPadding` | Thickness | `0,0,0,4` | H5 内边距（底部） |
| `MarkdownHeader5ParagraphMargin` | Thickness | `0,14,0,14` | H5 外边距 |
| `MarkdownHeader6ParagraphFontSize` | Double | `14` | H6 字号 |
| `MarkdownHeader6ParagraphBorderThickness` | Thickness | `0,0,0,1` | H6 下边框 |
| `MarkdownHeader6ParagraphPadding` | Thickness | `0,0,0,2` | H6 内边距（底部） |
| `MarkdownHeader6ParagraphMargin` | Thickness | `0,14,0,14` | H6 外边距 |

### 引用块 {#quote-blocks}
| 按键 | 类型 | Default (Light) | Default (Dark) | 注释支持情况 |
|---|---|---|---|---|
| `MarkdownQuoteBlockSectionBorderThickness` | Thickness | `4,0,0,0` | `4,0,0,0` | 引用块左侧竖线的粗细 |
| `MarkdownQuoteBlockSectionBorderBrush` | Brush | `#DDDDDD` | `#3b434b` | 引用块边框画刷 |
| `MarkdownQuoteBlockSectionForeground` | Brush | `#777777` | `#8b949e` | 引用块前景色 |
| `MarkdownQuoteBlockSectionPadding` | Thickness | `15,0` | `15,0` | 引用块内边距 |
| `MarkdownQuoteBlockFirstChildSectionMargin` | Thickness | `0,0,0,14` | `0,0,0,14` | 引用块内第一个子元素的外边距 |
| `MarkdownQuoteBlockLastChildSectionMargin` | Thickness | `0` | `0` | 引用块内最后一个子元素的外边距 |

### Tables
| 按键 | 类型 | Default (Light) | Default (Dark) | 注释支持情况 |
|---|---|---|---|---|
| `MarkdownTableCellBorderBrush` | Brush | `Black` | `#30363d` | 表格单元格边框画刷 |
| `MarkdownTableBorderBrush` | Brush | `Black` | `#30363d` | 表格边框画刷 |
| `MarkdownTableBorderThickness` | Thickness | `0,0,1,1` | `0,0,1,1` | 表格外边框粗细 |
| `MarkdownTableCellBorderThickness` | Thickness | `1,1,0,0` | `1,1,0,0` | 单元格边框粗细 |
| `MarkdownTableCellParagraphPadding` | Thickness | `12,5` | `12,5` | 单元格内段落的内边距 |

### 行内样式 {#inline-styles}
| 按键 | 类型 | Default (Light) | Default (Dark) | 注释支持情况 |
|---|---|---|---|---|
| `MarkdownMarkedSpanBackground` | Brush | `Yellow` | `#bb8009` | 标记片段的高亮背景 |

### 各类提示块 {#alert-blocks-per-type}
| 按键 | 类型 | Default (Light) | Default (Dark) | 注释支持情况 |
|---|---|---|---|---|
| `MarkdownAlertBlockNoteBorderBrush` | Brush | `#0969da` | `#58a6ff` | Note 提示块的边框画刷 |
| `MarkdownAlertBlockTipBorderBrush` | Brush | `#1a7f37` | `#3fb950` | Tip 提示块的边框画刷 |
| `MarkdownAlertBlockImportantBorderBrush` | Brush | `#8250df` | `#bc8cff` | Important 提示块的边框画刷 |
| `MarkdownAlertBlockWarningBorderBrush` | Brush | `#9a6700` | `#d29922` | Warning 提示块的边框画刷 |
| `MarkdownAlertBlockCautionBorderBrush` | Brush | `#d1242f` | `#f85149` | Caution 提示块的边框画刷 |

### 复制按钮 {#copy-button}
| 按键 | 类型 | Default (Light) | Default (Dark) | 注释支持情况 |
|---|---|---|---|---|
| `MarkdownCopyButtonFill` | Brush | `#59636e` | `#8b949e` | 复制按钮的填充色 |
| `MarkdownCopyButtonContentTemplate` | DataTemplate | — | — | 复制按钮的内容模板 |

## 如何覆盖 {#how-to-override}

### 样式选择器（推荐） {#style-selectors-recommended}

把你的样式放在 `App.axaml` 中 `Default.axaml` 的 `StyleInclude` 之后，或放进合并的资源字典里。靠后的样式优先级更高：

```xml
<Application.Styles>
    <StyleInclude Source="avares://Avalonia.Controls.Markdown/Themes/Default.axaml" />

    <!-- Your overrides -->
    <Style Selector="Paragraph.h1">
        <Setter Property="Foreground" Value="Navy" />
    </Style>
    <Style Selector="Section.quoteBlock">
        <Setter Property="Background" Value="#f0f4f8" />
    </Style>
</Application.Styles>
```

### 具名资源 {#named-resources}

在你的应用主题或资源字典中定义这些资源：

```xml
<SolidColorBrush x:Key="MarkdownHyperlinkForeground" Color="#FF0000" />
```

## 示例：自定义主题 {#example-custom-theme}

```xml
<ResourceDictionary>
    <SolidColorBrush x:Key="MarkdownSelectionBrush" Color="#FFD700" />
    <FontFamily x:Key="MarkdownCodeFontFamily">Cascadia Code</FontFamily>
</ResourceDictionary>
```

再配合样式选择器，做出一套深色代码主题：

```xml
<Style Selector=":is(Block).codeBlock">
    <Setter Property="Background" Value="#2d2d2d" />
    <Setter Property="Foreground" Value="#cccccc" />
    <Setter Property="CornerRadius" Value="8" />
</Style>
```

## 另请参阅 {#see-also}

- [Markdown 控件](/controls/data-display/text-display/markdown)