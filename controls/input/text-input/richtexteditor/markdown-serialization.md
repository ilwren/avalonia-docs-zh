---
id: markdown-serialization
title: Markdown Serialization
doc-type: guide
tags:
 - avalonia pro
 - avalonia enterprise
---

`MarkdownSerializer` 既能把 Markdown 读进文档，也能把文档写回 Markdown，即 `CanRead` 和 `CanWrite` 都报告为 `true`，并像其他序列化器一样出现在保存格式列表中。它位于 `Avalonia.Controls.Markdown` 包中，命名空间为 `Avalonia.Controls.Documents.Serialization.Markdown`。

编辑器打开和保存 `.md` 文件时，背后用的就是它。[Markdown 控件](/controls/data-display/text-display/markdown)也用它。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 读与写 {#reading-and-writing}

```csharp
using Avalonia.Controls.Documents;
using Avalonia.Controls.Documents.Serialization.Markdown;

var serializer = new MarkdownSerializer();

FlowDocument document;
await using (var input = File.OpenRead("notes.md"))
    document = FlowDocument.Load(input, serializer);

await using (var output = File.Create("notes.md"))
    document.Save(output, serializer);
```

除了接受流的重载，还有接受字符串的重载，方便手里拿着文本而非文件的调用方：

```csharp
var snapshot = serializer.Deserialize("# Title\n\nBody.");
string markdown = serializer.Serialize(document.CreateSnapshot());
```

序列化器通过构造函数配置，此后便不可变，可安全地并发使用：

```csharp
var serializer = new MarkdownSerializer(
    new MarkdownSerializerOptions { BulletMarker = '*', EmphasisChar = '_' },
    codeHighlighter);
```

它的契约是同步的。解析和写出 Markdown 都是 CPU 密集型工作，输出也在内存中拼装，没有异步 I/O 可等。要把它挪出 UI 线程，请自行包一层。

```csharp
var snapshot = document.CreateSnapshot();
await Task.Run(() => serializer.Serialize(snapshot, stream, cancellationToken), cancellationToken);
```

读写两侧都是逐块检查取消令牌的。渲染之前的 Markdig 解析一旦开始就会跑完，因此在此期间取消的令牌要到下一个块才生效。

对任何可读的流，`CanDeserialize` 都返回 `true`。所以格式选择器总把 Markdown 放在最后尝试。

:::info
请用构造函数来配置序列化器。`Options` 和 `CodeHighlighter` 虽然仍可赋值，但若把序列化器交给后台读取之后又通过 setter 改配置，格式就会在读取过程中中途生变。
:::

### 输出写法 {#output-spellings}

对于文档模型并不存储的那些语法细节，`MarkdownSerializerOptions` 负责选定规范写法。内容本身不受影响。

| 选项 | 默认值 | 有效取值 |
|---|---|---|
| `BulletMarker` | `-` | `-`, `+`, `*` |
| `EmphasisChar` | `*` | `*`, `_` |
| `FenceChar` | backtick | backtick, `~` |
| `OrderedDelimiter` | `.` | `.`, `)` |
| `HardBreak` | `Backslash` | `Backslash`, `TwoSpaces` |

`MarkdownSerializerOptions.Default` 是默认的一套。

## 有类型的 Markdown 元素 {#typed-markdown-elements}

Markdown 中的各种构造在 `Avalonia.Controls.Documents` 命名空间里各有对应的元素类型。还原源文所需的数据在实体化和编辑过程中都不会丢失，因此这些构造同样可以通过 FlowDocument API 来撰写。

| 元素 | 基类 | 携带的数据 |
|---|---|---|
| `MarkdownHeading` | `Paragraph` | `Level` (1-6) |
| `MarkdownCodeBlock` | `Paragraph` | `LanguageId`, `InfoArguments`, `Highlighter` |
| `MarkdownAlertBlock` | `Section` | `AlertKind`（「Note」「Warning」「Tip」「Important」「Caution」） |
| `MarkdownHtmlBlock` | `Section` | `RawHtml` |
| `MarkdownHtmlInline` | `RichSpan` | `RawHtml` |
| `MarkdownImage` | `RichImage` | `ImageSource`、`ImageTitle`、`ImageLoader`，以及基类的 `AltText` |
| `MarkdownTaskListItem` | `ListItem` | `IsChecked` |

### Example

```csharp
document.Blocks.Add(new MarkdownHeading { Level = 2, Inlines = { new RichRun("Design notes") } });
```

`new MarkdownHeading { Level = 2 }` 的写出结果与解析得到的 `## ` 完全一致。

:::note
这些类型沿用其基类型的样式键，因此 `Paragraph.h1`、`Section.alertBlock` 之类的主题选择器和应用选择器照常匹配。请通过它们的 CSS 类而非类型名来设置样式。`MarkdownCodeBlock` 和 `MarkdownImage` 则各有自己的键。
:::

`MarkdownCodeBlock.InfoArguments` 是围栏信息串中语言标识之后的剩余部分，因此像 ` ```text title=foo ` 这样的指令在保存后依然还在。

## Footnotes

Markdown 脚注会加载到文档自身的脚注模型上：

- 某个标签的第一处引用成为 `RichFootnoteReference` 锚点，按引用顺序编号。
- 定义成为 `FlowDocument.Footnotes` 中的 `Footnote`，其标签存为 `Footnote.Label`。
- 同一标签之后的引用，以及注释内部的引用，都会变成指向同一条注释的 `RichFootnoteCitation` 元素。

于是从 Markdown 读入的注释能够正常渲染：它们和其他文档的注释一样参与分页和导出，编辑器的脚注命令也对它们有效。点击锚点或引用会滚动到对应注释。参阅[脚注](/controls/input/text-input/richtexteditor/footnotes)。

写出时，每条注释按注释顺序变成正文之后的一条 `[^label]: ...` 定义。有标签的注释保留其标签，写法照旧；没有标签的则按位置命名。任意两条注释的名字都不能相同，否则重新解析时重复的定义会被合并。标签中的 `]`、`[` 或 `\` 会被转义。无人引用的定义也会保留。

若某个片段并未指向任何注释（比如 `[Back to top](#top)` 这样的标题锚点），它不会被处理，而是继续向上冒泡，这样自带锚点处理逻辑的应用仍能收到它。

## HTML 的回写 {#html-write-back}

HTML 块会被转换成富文本元素以供显示，`MarkdownHtmlBlock.RawHtml` 则保留着原始源码。只要该块未被编辑过，写出时就原样输出。写出器会把原始 HTML 重新转换一遍，再把结果文本与该块当前的文本比对；只要文本有任何改动，就退回到把转换后的子元素序列化成规范 Markdown。

转换器不认识的行内 HTML 会以 `MarkdownHtmlInline` 的形式保留而不是被丢弃，于是一个零散的标签能挺过一轮往返，而不会从文件里凭空消失。

## 往返保真度 {#round-trip-fidelity}

逐字节还原任意 Markdown 既不是目标，也做不到——那需要存储源文的琐碎细节，而快照并不存。Markdown 序列化器着力保证的是下面这些：

**语义等价。** 对受支持的构造集合而言，把写出器的产物再解析一遍，得到的文档与解析原文等价。

**完整保留。** 那些读者在 diff 中一眼能看出来的写作选择，因为模型把它们存下来了。包括：

- 标题层级
- 代码语言、信息串参数及代码正文
- 任务列表的勾选状态
- 警示块的种类
- 列表类型与起始序号
- 表格列对齐方式与表头行
- 链接与图片的 URL、标题和替代文字
- 脚注标签
- 未经编辑的 HTML 块、以及无法识别的行内标签的原始源码

**规范化。** 统一成 `MarkdownSerializerOptions` 选定的写法：

- 强调所用的定界符及其个数
- 项目符号字符；有序列表的定界符
- 代码围栏的字符与长度（缩进式代码块会写成围栏式）
- 分隔线样式
- 硬换行的写法
- 引用块的标记
- indentation
- 实体与反斜杠转义的写法
- emoji 与符号的短代码：字符本身能往返，但短代码不会被还原
- 软换行的折行位置，这些不会被还原

**不在覆盖范围内：**

| 缺口 | 效果 |
|---|---|
| 网格表格 | 能读，但写出时变成管道表格 |
| 表格的跨列与跨行 | 管道表格形式表达不了 |
| YAML front matter | 不识别；开头的 `---` 块会被解析成一条分隔线加一段正文 |
| 剪贴板集成 | Markdown 不在编辑器的剪贴板格式之列 |
<br />

即便文档并非来自 Markdown，而是从 RTF 或任意 `FlowDocument` 加载的，序列化也绝不会失败：凡是能映射过去的结构，都会写成规范的 Markdown；Markdown 表达不了的格式（颜色、字体、间距等）则一概丢弃。

### 受支持的构造集合 {#supported-construct-set}

处理流水线是 Markdig 加 `UseSupportedExtensions()`。受支持的构造有：

- 自动链接
- 警示块
- emoji 与颜文字
- footnotes
- 网格表格
- 管道表格
- 扩展强调（删除线、下标、上标、插入、标记）
- 任务列表
- Markdig 库自带的 symbol 扩展

## 另请参阅 {#see-also}

- [Markdown 控件](/controls/data-display/text-display/markdown) —— 不用编辑器也能渲染 Markdown
- [代码高亮器](/controls/data-display/text-display/markdown/codehighlighter) —— 序列化器所接受的 `CodeHighlighter`
- [脚注](/controls/input/text-input/richtexteditor/footnotes) —— Markdown 注释加载到的那个模型
