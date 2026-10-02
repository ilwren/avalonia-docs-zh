---
id: extension-patterns
title: Extension Patterns
doc-type: how-to
tags:
 - avalonia pro
 - avalonia enterprise
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

RichTextEditor 在多个层面都为扩展留好了口子。本指南介绍如何在不改动核心代码的前提下扩展功能。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 扩展点 {#extension-points}

1. **自定义文档元素** —— 新的块级/行内类型
2. **自定义高亮层** —— 查找、拼写检查、批注
3. **自定义序列化格式** —— 你自己的文件格式
4. **自定义编辑器组件** —— 新的输入处理程序
5. **成组的撤销操作** —— 通过 `UndoManager.BeginUndoUnit` 实现（自定义 `IUndoUnit` 子类并不是公开的扩展点）

:::info
由于相关元素是 sealed 或 internal 的，无法对视图做派生。你可以改用 `ITextViewComponent` 或 `IHighlightLayer` 来扩展视图，或者考虑使用 `InteractiveTextView`。
:::

## 自定义文档元素 {#custom-document-elements}

自定义文档元素需要三样东西：

1. **元素类** —— 模型类型（继承 `RichSpan`、`RichHyperlink`、`Section` 等）
2. **快照节点** —— 让自定义数据在快照/撤销的来回往返中得以保全
3. **处理程序** —— 负责创建元素、采集快照并恢复格式

启动时通过 `TextDocumentNodeKind.Register` 注册每一种元素：

```csharp
using Avalonia.Controls.Documents.TextModel;

public static class CustomNodeRegistration
{
    public static TextDocumentNodeKind CalloutBlockKind { get; private set; }
    public static TextDocumentNodeKind MentionInlineKind { get; private set; }

    public static void Register()
    {
        CalloutBlockKind = TextDocumentNodeKind.Register<CalloutBlock>(
            "CalloutBlock",
            NodeKindFlags.Block | NodeKindFlags.BlockContainer,
            new CalloutBlockHandler());

        MentionInlineKind = TextDocumentNodeKind.Register<MentionInline>(
            "MentionInline",
            NodeKindFlags.Inline,
            new MentionHandler());
    }
}
```

### 创建自定义行内元素 {#creating-a-custom-inline-element}

下面的例子做了一个继承自 `RichHyperlink` 的 `MentionInline`，于是「提及」自带了悬停效果、点击处理和工具提示。处理程序把 `NavigateUri` 设为一个 `mention:{userId}` URI——在编辑器上处理 `RequestNavigate` 即可拦截点击。

<Tabs>
<TabItem value="element" label="Element">

```csharp
using Avalonia.Controls.Documents;

public class MentionInline : RichHyperlink
{
    public string? UserId { get; set; }
    public string? DisplayName { get; set; }
}
```

</TabItem>
<TabItem value="snapshot" label="Snapshot node">

让 `UserId` / `DisplayName` 在撤销与序列化的往返中得以保全：

```csharp
using Avalonia.Controls.Documents.TextModel;
using Avalonia.Controls.Documents.Serialization.Snapshot;

public class MentionSnapshotNode : InlineSnapshotNode
{
    public string? UserId { get; }
    public string? DisplayName { get; }

    public MentionSnapshotNode(
        TextDocumentNodeKind kind,
        int startOffset,
        int length,
        InlineFormatting inlineFormatting,
        SnapshotNodeChildren children,
        TextElementFormatting textElementFormatting,
        string? userId,
        string? displayName)
        : base(kind, startOffset, length, inlineFormatting, children, textElementFormatting)
    {
        UserId = userId;
        DisplayName = displayName;
    }
}
```

</TabItem>
<TabItem value="handler" label="Handler">

```csharp
using Avalonia.Controls.Documents;
using Avalonia.Controls.Documents.TextModel;
using Avalonia.Controls.Documents.TextModel.Handlers;
using Avalonia.Controls.Documents.Serialization.Snapshot;
using Avalonia.Media;

public class MentionHandler : InlineNodeKindHandler
{
    private static readonly ISolidColorBrush MentionBackground =
        new SolidColorBrush(Color.Parse("#E3F2FD"));
    private static readonly ISolidColorBrush MentionForeground =
        new SolidColorBrush(Color.Parse("#1565C0"));

    public override RichTextElement? CreateElement(TextDocumentNodeKind kind)
    {
        var mention = new MentionInline();
        ApplyDefaultStyle(mention);
        return mention;
    }

    protected override SnapshotNode CreateInlineSnapshot(
        TextDocumentNodeKind kind, int startOffset, int length,
        InlineFormatting inlineFormatting, SnapshotNodeChildren children,
        TextElementFormatting textElementFormatting,
        RichTextElement? element, SnapshotNode? deferredSnapshot)
    {
        string? userId = null;
        string? displayName = null;

        if (deferredSnapshot is MentionSnapshotNode ms)
        {
            userId = ms.UserId;
            displayName = ms.DisplayName;
        }
        if (element is MentionInline mention)
        {
            userId = mention.UserId;
            displayName = mention.DisplayName;
        }

        return new MentionSnapshotNode(
            kind, startOffset, length,
            inlineFormatting, children, textElementFormatting,
            userId, displayName);
    }

    public override void ApplyFormatting(RichTextElement element, SnapshotNode snapshotNode)
    {
        base.ApplyFormatting(element, snapshotNode);

        if (element is MentionInline mention && snapshotNode is MentionSnapshotNode ms)
        {
            mention.UserId = ms.UserId;
            mention.DisplayName = ms.DisplayName;
            ApplyDefaultStyle(mention);
        }
    }

    public static void ApplyDefaultStyle(MentionInline mention)
    {
        mention.Background = MentionBackground;
        mention.Foreground = MentionForeground;
        mention.FontWeight = FontWeight.SemiBold;

        if (mention.UserId is { } userId)
        {
            mention.NavigateUri = new Uri($"mention:{userId}");
            mention.ToolTip = mention.DisplayName is { } name
                ? $"@{name} ({userId})"
                : $"@{userId}";
        }
    }
}
```

</TabItem>
</Tabs>

**用法：**

```csharp
var mention = new MentionInline { UserId = "alice", DisplayName = "Alice" };
mention.Inlines.Add(new RichRun { Text = "@Alice" });
MentionHandler.ApplyDefaultStyle(mention);
paragraph.Inlines.Add(mention);
```

### 创建自定义块级元素 {#creating-a-custom-block-element}

下面的例子做了一个继承自 `Section`（块容器）的 `CalloutBlock`，并提供了一个自定义的 `StackLayoutNode` 子类，用来绘制彩色强调条和带底色的背景。配色方案由 `CalloutType` 枚举控制。

<Tabs>
<TabItem value="element" label="Element">

```csharp
using Avalonia.Controls.Documents;

public enum CalloutType { Note, Warning, Tip, Important }

public class CalloutBlock : Section
{
    public CalloutType Type { get; set; }
}
```

</TabItem>
<TabItem value="snapshot" label="Snapshot node">

```csharp
using Avalonia.Controls.Documents.TextModel;
using Avalonia.Controls.Documents.Serialization.Snapshot;

public class CalloutSnapshotNode : BlockSnapshotNode
{
    public CalloutType CalloutType { get; }

    public CalloutSnapshotNode(
        TextDocumentNodeKind kind,
        int startOffset,
        int length,
        BlockFormatting blockFormatting,
        SnapshotNodeChildren children,
        TextElementFormatting textElementFormatting,
        CalloutType calloutType)
        : base(kind, startOffset, length, blockFormatting, children, textElementFormatting)
    {
        CalloutType = calloutType;
    }
}
```

</TabItem>
<TabItem value="docnode" label="DocumentNode">

带强调条和底色背景的自定义渲染：

```csharp
using Avalonia;
using Avalonia.Controls.Documents;
using Avalonia.Controls.Documents.Primitives.DocumentNodes;
using Avalonia.Media;

public class CalloutDocumentNode : StackLayoutNode
{
    private const double AccentBarWidth = 4;
    private readonly CalloutBlock _callout;

    public CalloutDocumentNode(CalloutBlock callout) : base(callout)
    {
        _callout = callout;
    }

    protected override IEnumerable<RichTextElement> GetEnumerable() => _callout.Blocks;

    public override void Render(DrawingContext context)
    {
        var bounds = new Rect(Bounds.Size);
        context.FillRectangle(GetBackgroundBrush(_callout.Type), bounds);
        context.FillRectangle(GetAccentBrush(_callout.Type),
            new Rect(0, 0, AccentBarWidth, bounds.Height));
    }

    private static ISolidColorBrush GetAccentBrush(CalloutType type) => type switch
    {
        CalloutType.Note     => new SolidColorBrush(Color.Parse("#1976D2")),
        CalloutType.Warning  => new SolidColorBrush(Color.Parse("#F57C00")),
        CalloutType.Tip      => new SolidColorBrush(Color.Parse("#388E3C")),
        CalloutType.Important => new SolidColorBrush(Color.Parse("#D32F2F")),
        _ => new SolidColorBrush(Color.Parse("#757575"))
    };

    private static ISolidColorBrush GetBackgroundBrush(CalloutType type) => type switch
    {
        CalloutType.Note     => new SolidColorBrush(Color.Parse("#E3F2FD")),
        CalloutType.Warning  => new SolidColorBrush(Color.Parse("#FFF3E0")),
        CalloutType.Tip      => new SolidColorBrush(Color.Parse("#E8F5E9")),
        CalloutType.Important => new SolidColorBrush(Color.Parse("#FFEBEE")),
        _ => new SolidColorBrush(Color.Parse("#F5F5F5"))
    };
}
```

</TabItem>
<TabItem value="handler" label="Handler">

```csharp
using Avalonia;
using Avalonia.Controls.Documents;
using Avalonia.Controls.Documents.Primitives.DocumentNodes;
using Avalonia.Controls.Documents.TextModel;
using Avalonia.Controls.Documents.TextModel.Handlers;
using Avalonia.Controls.Documents.Serialization.Snapshot;

public class CalloutBlockHandler : BlockNodeKindHandler
{
    public override RichTextElement? CreateElement(TextDocumentNodeKind kind)
    {
        return new CalloutBlock { Padding = new Thickness(12, 6, 6, 6) };
    }

    protected override SnapshotNode CreateBlockSnapshot(
        TextDocumentNodeKind kind, int startOffset, int length,
        BlockFormatting blockFormatting, SnapshotNodeChildren children,
        TextElementFormatting textElementFormatting,
        RichTextElement? element, SnapshotNode? deferredSnapshot)
    {
        var calloutType = CalloutType.Note;

        if (deferredSnapshot is CalloutSnapshotNode cs)
            calloutType = cs.CalloutType;
        if (element is CalloutBlock callout)
            calloutType = callout.Type;

        return new CalloutSnapshotNode(
            kind, startOffset, length,
            blockFormatting, children, textElementFormatting,
            calloutType);
    }

    public override void ApplyFormatting(RichTextElement element, SnapshotNode snapshotNode)
    {
        base.ApplyFormatting(element, snapshotNode);

        if (element is CalloutBlock callout && snapshotNode is CalloutSnapshotNode cs)
        {
            callout.Type = cs.CalloutType;
            callout.Padding = new Thickness(12, 6, 6, 6);
        }
    }

    public override DocumentNode? CreateDocumentNode(RichTextElement element)
        => element is CalloutBlock callout ? new CalloutDocumentNode(callout) : null;
}
```

</TabItem>
</Tabs>

**用法：**

```csharp
var callout = new CalloutBlock
{
    Type = CalloutType.Warning,
    Padding = new Thickness(12, 6, 6, 6),
    Margin = new Thickness(0, 5, 0, 5)
};
var body = new Paragraph();
body.Inlines.Add(new RichRun { Text = "Breaking changes ahead." });
callout.Blocks.Add(body);
doc.Blocks.Add(callout);
```

## 自定义高亮层 {#custom-highlight-layers}

### 查找/替换高亮层 {#findreplace-highlight-layer}

`HighlightLayerBase` 只接受 `(string name, int zIndex)`。`AddRegion`、`RemoveRegion` 是 `protected` 的，因此子类需要用公开的包装方法把它们暴露出来。它们会自动引发 `RegionsChanged`，所以包装方法事后不必再调用 `OnRegionsChanged`。

```csharp
using Avalonia.Controls.Documents.Primitives.Highlighting; // HighlightLayerBase, HighlightRegion, HighlightStyle

public class FindHighlightLayer : HighlightLayerBase
{
    public FindHighlightLayer()
        : base(name: "Find", zIndex: 50)
    {
    }

    public void HighlightMatches(IEnumerable<TextRange> matches)
    {
        ClearRegions();

        foreach (var match in matches)
        {
            var region = new HighlightRegion(
                match.Start,
                match.End,
                brush: Brushes.Yellow,
                opacity: 0.4);
            AddRegion(region);
        }
    }

    public void HighlightCurrent(TextRange current)
    {
        var region = new HighlightRegion(
            current.Start,
            current.End,
            brush: Brushes.Orange,
            opacity: 0.5);
        AddRegion(region);
    }
}
```

:::warning
- `HighlightLayerCollection` 是 sealed 的。
- 当某个层的 `Name` 已存在于集合中时，`Add` 会抛出异常，以保证按 `GetLayer` 查找始终有效。
- 遇到没有对应渲染器的高亮样式时，`HighlightLayerBase.RenderRegion` 会抛出异常，而不是悄悄什么都不画。
- `HighlightStyle.Custom` 已不再使用。要绘制内置样式之外的自定义高亮，请重写 `RenderRegion`。
:::

**Integration:**

```csharp
var findLayer = new FindHighlightLayer();
editor.HighlightLayers.Add(findLayer);

// Find matches
var matches = FindInDocument(searchText);
findLayer.HighlightMatches(matches);
```

### 拼写检查层 {#spell-check-layer}

```csharp
public class SpellCheckHighlightLayer : HighlightLayerBase
{
    public SpellCheckHighlightLayer()
        : base(name: "SpellCheck", zIndex: 10)
    {
    }

    public async Task CheckSpellingAsync(TextDocument document)
    {
        var errors = await RunSpellCheckAsync(document);

        // Update highlights on the UI thread; TextPointer is UI-thread only.
        await Dispatcher.UIThread.InvokeAsync(() =>
        {
            ClearRegions();

            foreach (var error in errors)
            {
                var region = new HighlightRegion(
                    document.ContentStart.CreatePointer(error.Offset),
                    document.ContentStart.CreatePointer(error.Offset + error.Length),
                    brush: Brushes.Red,
                    style: HighlightStyle.WavyUnderline);
                AddRegion(region);
            }
        });
    }

    private Task<List<SpellError>> RunSpellCheckAsync(TextDocument doc)
    {
        return Task.Run(() =>
        {
            // Spell check logic here
            return new List<SpellError>();
        });
    }
}
```

## 自定义序列化格式 {#custom-serialization-formats}

`IDocumentSerializer` 是同步的。每个实现都要提供 `Deserialize`、`Serialize`、`CanDeserialize` 以及下列属性：
- `FormatName`
- `FileExtension`
- `MimeType`
- `CanRead`
- `CanWrite`

所有序列化器都不做异步 I/O：格式处理是 CPU 密集型的，输出也在内存中拼装。把调用包进 `Task.Run`，只是为了把这份工作从调用方自己的线程上挪开。

`CanRead` 和 `CanWrite` 没有默认值，两者都必须显式声明。

### 自己写一个 HTML 序列化器 {#writing-your-own-html-serializer}

:::info
`Avalonia.Controls.Documents.Serialization.Html` 中的 `HtmlSerializer` 只支持读。下面的例子做了一个可读可写的自定义 HTML 序列化器。
:::

```csharp
using Avalonia.Controls.Documents;
using Avalonia.Controls.Documents.Serialization;
using Avalonia.Controls.Documents.Serialization.Snapshot;
using Avalonia.Controls.Documents.TextModel;
using System.Threading;
using System.Threading.Tasks;

public class MyHtmlSerializer : IDocumentSerializer
{
    public string FormatName => "Html";
    public string FileExtension => ".html";
    public string MimeType => "text/html";

    public bool CanRead => true;
    public bool CanWrite => true;

    public bool CanDeserialize(Stream stream) => true;

    public DocumentSnapshot Deserialize(
        Stream stream, CancellationToken cancellationToken = default)
    {
        using var reader = new StreamReader(stream);
        string html = reader.ReadToEnd();

        var builder = FlowDocumentBuilder.Create();
        ParseHtml(html, builder);
        var doc = builder.Build();
        return doc.TextDocument.CreateSnapshot();
    }

    public void Serialize(
        DocumentSnapshot snapshot, Stream stream,
        CancellationToken cancellationToken = default)
    {
        using var writer = new StreamWriter(stream);
        writer.WriteLine("<html><body>");

        foreach (var child in snapshot.Root.Children)
        {
            if (child is BlockSnapshotNode block)
                WriteBlock(block, snapshot, writer);
        }

        writer.WriteLine("</body></html>");
    }

    public Task<DocumentSnapshot> DeserializeAsync(
        Stream stream, CancellationToken cancellationToken = default)
        => Task.Run(() => Deserialize(stream, cancellationToken), cancellationToken);

    public Task SerializeAsync(
        DocumentSnapshot snapshot, Stream stream,
        CancellationToken cancellationToken = default)
        => Task.Run(() => Serialize(snapshot, stream, cancellationToken), cancellationToken);

    private void WriteBlock(BlockSnapshotNode block,
                            DocumentSnapshot snapshot, StreamWriter writer)
    {
        writer.Write("<p>");

        foreach (var child in block.Children)
        {
            if (child is InlineSnapshotNode inline)
                WriteInline(inline, snapshot, writer);
        }

        writer.WriteLine("</p>");
    }

    private void WriteInline(InlineSnapshotNode inline,
                             DocumentSnapshot snapshot, StreamWriter writer)
    {
        var text = snapshot.GetText(inline.StartOffset, inline.Length);

        bool isBold = inline.Kind == TextDocumentNodeKind.Bold;
        bool isItalic = inline.Kind == TextDocumentNodeKind.Italic;

        if (isBold) writer.Write("<strong>");
        if (isItalic) writer.Write("<em>");

        // Encode text to prevent XSS
        writer.Write(System.Net.WebUtility.HtmlEncode(text));

        if (isItalic) writer.Write("</em>");
        if (isBold) writer.Write("</strong>");
    }

    private void ParseHtml(string html, FlowDocumentBuilder builder)
    {
        // Parse HTML and populate builder
    }
}
```

**用法：**

```csharp
var serializer = new MyHtmlSerializer();
await using var stream = File.Create("output.html");
await editor.SaveAsync(stream, serializer);
```

框架里没有可供注册序列化器的格式注册表：每个序列化器包都依赖核心包，核心包里的注册表自然没法反过来引用它们。请指定 `CanRead` / `CanWrite` / `CanDeserialize`，好让格式选择器能发现你的序列化器。

## 自定义编辑器组件 {#custom-editor-components}

### 自动补全组件 {#auto-complete-component}

`ITextViewComponent` 接口让你能编写与编辑器宿主基础设施打通的输入处理组件。

`ITextViewComponent.OnAttach` 接受的是 `IInteractiveTextHost`——这是只读阅读器也实现的宿主接口，而非编辑器专有的 `ITextEditorHost`。若你需要编辑器自己的界面，请做一次类型转换。

```csharp
using Avalonia.Controls.Documents.Primitives.Components; // ITextViewComponent, TextViewComponentBase
using Avalonia.Controls.Documents.Primitives; // IInteractiveTextHost
using Avalonia.Controls.Documents.TextModel;

public class AutoCompleteComponent : ITextViewComponent
{
    private IInteractiveTextHost? _host;
    private Popup? _completionPopup;
    private ListBox? _completionList;

    public bool IsAttached => _host is not null;

    public void OnAttach(IInteractiveTextHost host)
    {
        if (_host is not null)
            OnDetach();

        _host = host;
        _host.ContentChanged += OnContentChanged;
        InitializePopup();
    }

    public void OnDetach()
    {
        if (_host is null)
            return;

        _host.ContentChanged -= OnContentChanged;
        _host = null;
        _completionPopup = null;
    }

    private void OnContentChanged(object? sender, EventArgs e)
    {
        var selection = _host?.Selection;
        if (selection is not { IsEmpty: true }) return;

        var caretPos = selection.Start;
        string wordBeforeCaret = GetWordBeforeCaret(caretPos);

        if (wordBeforeCaret.Length >= 3)
            ShowCompletions(wordBeforeCaret);
        else
            HideCompletions();
    }

    private string GetWordBeforeCaret(TextPointer caret)
    {
        var doc = caret.TextDocument;
        if (doc == null) return string.Empty;

        int offset = caret.Offset;
        int readStart = Math.Max(0, offset - 64);
        if (readStart >= offset) return string.Empty;

        var start = doc.ContentStart.CreatePointer(readStart);
        var range = new TextRange(start, caret);
        string text = range.GetText();

        int i = text.Length - 1;
        while (i >= 0 && char.IsLetterOrDigit(text[i]))
            i--;

        return text[(i + 1)..];
    }

    private void InsertCompletion()
    {
        if (_completionList?.SelectedItem is string completion)
        {
            var editor = _host as RichTextEditor;
            var caret = editor?.Selection?.CaretPosition;
            if (caret == null) return;

            string prefix = GetWordBeforeCaret(caret);
            var start = caret.GetPositionAtOffset(-prefix.Length);
            if (start != null)
            {
                var range = new TextRange(start, caret);
                range.ReplaceText(completion);
            }

            HideCompletions();
        }
    }

    private void ShowCompletions(string prefix) { /* ... */ }
    private void HideCompletions() { /* ... */ }
    private void InitializePopup() { /* ... */ }
}
```

**Registration:**

```csharp
editor.RegisterComponent(new AutoCompleteComponent());
```

## 自定义撤销单元 {#custom-undo-units}

### 把多步操作合并成一次撤销 {#grouping-operations-into-a-single-undo-step}

用 `UndoManager.BeginUndoUnit` 可以把作用域内的全部改动记录成单个可撤销的动作：

```csharp
using Avalonia.Controls.Documents.Undo;

// RichTextEditor.UndoManager and TextDocument.UndoManager are both
// typed UndoManager?; there is no undo interface to substitute.
UndoManager? undoManager = editor.UndoManager;
if (undoManager != null)
{
    using (undoManager.BeginUndoUnit("Find and Replace All"))
    {
        // All edits inside this scope are a single undo step
        foreach (var match in matches)
        {
            match.ReplaceText(replacement);
        }
    }
}
```

#### `IUndoUnit`

`IUndoUnit` 只对外暴露 `Description` 属性，其撤销 / 重做 / 合并机制都是 internal 的，你无法创建自定义撤销单元。请改用 `BeginUndoUnit`；若没有用撤销管理器，则用 `TextDocument.BeginChange()`。

#### 如何关闭记录 {#how-to-turn-off-recording}

要关闭记录，可以把 `TextDocument.UndoManager` 设为 `null`，或者保留实例及其订阅者而改用 `new UndoManager { IsEnabled = false }`。界面通常绑定的是 `UndoManager.CanUndo`、`CanRedo` 和 `StateChanged`；撤销单元栈本身是 internal 的。

#### 恢复插入符位置 {#restoring-the-caret}

`SelectionSnapshot.Capture(selection)` 会生成一个 `BeginUndoUnit` 和 `IUndoScope.SetSelectionAfter` 都接受的快照，于是一次成组编辑可以把插入符恢复到它开始时的位置。

## 实践建议 {#best-practices}

### Do's

1. **实现 `ITextViewComponent`** —— 借助 attach/detach 生命周期做好清理，并支持首次扫描
2. **在 `host.UIScope` 上订阅输入事件** —— 宿主本身收不到输入事件，只有 UIScope 能收到
3. **用 `RoutingStrategies.Tunnel` 拦截指针事件** —— `TextViewMouse` 等内置组件会在冒泡阶段把事件标记为已处理；用隧道阶段才能抢先查看
4. **用 `ITextView.GetTextPositionFromPoint` 做命中测试** —— 选区状态可能是过时的（隧道阶段尤其如此），请直接对点击点做命中测试
5. **从基类继承** —— 用 `HighlightLayerBase` 而不是裸的 `IHighlightLayer`；用 `TextViewComponentBase` 而不是从零实现 `ITextViewComponent`
6. **妥善处理 null** —— 宿主、UIScope 和 TextView 在状态切换期间都可能为 null
7. **写单元测试** —— 把扩展测充分
8. **耗时操作用异步** —— 别阻塞 UI 线程

### Don'ts

1. **别直接在宿主/编辑器上订阅事件** —— 请通过 `AddHandler`/`RemoveHandler` 使用 `host.UIScope`
2. **别在指针处理程序里依赖选区状态** —— 改为对点做命中测试；隧道阶段选区还没来得及更新
3. **别对视图做派生** —— `TextViewBase` 是抽象类，`PagedTextView` 是 sealed 的，而 `TextViewKeyboard` 的构造函数是 internal 的。
4. **别碰内部实现** —— 只用公开 API
5. **别持有文档的强引用** —— 那会导致内存泄漏
6. **别阻塞 UI 线程** —— CPU 和 IO 的活儿请用异步
7. **别臆断文档结构** —— 访问之前先校验
8. **别绕开撤销系统** —— 可撤销的操作一律记录在案
9. **别忘了 detach** —— 清理好事件处理程序

## 完整示例：智能链接识别 {#complete-example-smart-link-detection}

这个组件会识别文档中的 URL，用蓝色下划线高亮它们，并支持 <kbd>Ctrl</kbd>+单击打开链接。它演示了以下几个关键套路：

- **`ITextViewComponent` 生命周期** —— attach 时扫描一遍现有内容，之后每次文本或文档变化都再扫一遍
- **`host.UIScope`** —— 在 UIScope 而非宿主本身上订阅指针事件，因为只有 UIScope 才收得到输入事件
- **`RoutingStrategies.Tunnel`** —— 在隧道阶段订阅，好让处理程序赶在 `TextViewMouse` 于冒泡阶段把事件标记为已处理之前触发
- **`ITextView` 命中测试** —— 用 `GetTextPositionFromPoint` 把点击位置解析成 `TextPointer`；隧道阶段的选区状态是过时的

它用来绘制的那个层，包装了 `HighlightLayerBase` 的受保护成员：

```csharp
public class LinkHighlightLayer : HighlightLayerBase
{
    public LinkHighlightLayer() : base("Links", zIndex: 40) { }

    public void AddLink(TextPointer start, TextPointer end)
        => AddRegion(new HighlightRegion(start, end, Brushes.Blue, 0.3, HighlightStyle.Underline));

    public void ClearHighlights() => ClearRegions();

    public void RaiseChanged() => OnRegionsChanged();
}
```

组件本身：

```csharp
// Register via editor.RegisterComponent(new SmartLinkExtension()).
// Unregister via editor.UnregisterComponent(component).

public class SmartLinkExtension : ITextViewComponent
{
    private IInteractiveTextHost? _host;
    private readonly LinkHighlightLayer _linkLayer = new();
    private readonly List<DetectedLink> _links = new();

    public bool IsAttached => _host is not null;

    public event Action<Uri>? LinkActivated;

    public void OnAttach(IInteractiveTextHost host)
    {
        if (_host is not null)
            OnDetach();

        _host = host;

        if (_host is RichTextEditor editor)
            editor.HighlightLayers.Add(_linkLayer);

        _host.ContentChanged += OnTextChanged;
        _host.DocumentChanged += OnDocumentChanged;

        // Subscribe on UIScope (the element that receives input events)
        // using Tunnel so we fire before TextViewMouse's Bubble handler.
        _host.UIScope?.AddHandler(
            InputElement.PointerPressedEvent,
            OnPointerPressed,
            RoutingStrategies.Tunnel);

        // Scan existing content immediately
        _ = DetectLinksAsync();
    }

    public void OnDetach()
    {
        if (_host is null)
            return;

        _host.ContentChanged -= OnTextChanged;
        _host.DocumentChanged -= OnDocumentChanged;

        _host.UIScope?.RemoveHandler(
            InputElement.PointerPressedEvent,
            OnPointerPressed);

        if (_host is RichTextEditor editor)
            editor.HighlightLayers.Remove(_linkLayer);

        _links.Clear();
        _linkLayer.ClearHighlights();
        _host = null;
    }

    private async void OnTextChanged(object? sender, EventArgs e)
        => await DetectLinksAsync();

    private async void OnDocumentChanged(object? sender, EventArgs e)
        => await DetectLinksAsync();

    private async Task DetectLinksAsync()
    {
        var doc = _host?.TextDocument;
        if (doc is null) return;

        var start = doc.ContentStart.CreatePointer(0);
        var end = doc.ContentStart.CreatePointer(doc.Length);
        string text = new TextRange(start, end).GetText();

        var found = await Task.Run(() => FindUrls(text));

        await Dispatcher.UIThread.InvokeAsync(() =>
        {
            // Guard against detach or document swap while awaiting
            if (_host is null) return;
            var currentDoc = _host.TextDocument;
            if (currentDoc != doc) return;

            _links.Clear();
            _linkLayer.ClearHighlights();

            foreach (var (offset, length, uri) in found)
            {
                _links.Add(new DetectedLink(
                    offset, offset + length, uri));
                _linkLayer.AddLink(
                    currentDoc.ContentStart.CreatePointer(offset),
                    currentDoc.ContentStart.CreatePointer(offset + length));
            }

            _linkLayer.RaiseChanged();
        });
    }

    private void OnPointerPressed(object? sender, PointerPressedEventArgs e)
    {
        var host = _host;
        if (host is null) return;

        var uiScope = host.UIScope;
        var textView = host.TextView;
        if (uiScope is null || textView is null) return;

        if (!e.KeyModifiers.HasFlag(KeyModifiers.Control)) return;
        if (!e.GetCurrentPoint(uiScope).Properties.IsLeftButtonPressed) return;

        // Hit-test the click point — don't rely on selection state,
        // which hasn't been updated yet during the Tunnel phase.
        var clickPoint = e.GetPosition((Visual)textView);
        var pointer = textView.GetTextPositionFromPoint(
            clickPoint, snapToText: false);
        if (pointer is null) return;

        int offset = pointer.Offset;
        var link = _links.Find(l => offset >= l.Start && offset <= l.End);

        if (link is not null)
        {
            LinkActivated?.Invoke(link.Uri);
            e.Handled = true;
        }
    }

    // Scanning is the extension's own work; swap in whatever URL detector you use.
    private static IReadOnlyList<(int offset, int length, Uri uri)> FindUrls(string text)
        => Array.Empty<(int, int, Uri)>();

    private record DetectedLink(int Start, int End, Uri Uri);
}
```

## 测试扩展 {#testing-extensions}

`DocumentSnapshot.EnumerateNodes` 是检视快照的公开入口。若连重建路径也要一并验证，可以用你自己的格式（或任意随附的序列化器）把快照序列化出去，再用 `FlowDocument.Load` 读回来。

凡是涉及 `AvaloniaObject` 的测试都要用 `[AvaloniaFact]` 而不是普通的 `[Fact]`：线程亲和性会让普通写法变得时灵时不灵。

```csharp
public class MentionInlineTests
{
    [AvaloniaFact]
    public void MentionInline_PreservesUserIdThroughSnapshot()
    {
        // Arrange — register the custom kind
        var kind = TextDocumentNodeKind.Register<MentionInline>(
            "TestMention", NodeKindFlags.Inline, new MentionHandler());

        var doc = new FlowDocument();
        var para = new Paragraph();
        var mention = new MentionInline { UserId = "alice", DisplayName = "Alice" };
        mention.Inlines.Add(new RichRun { Text = "@Alice" });
        MentionHandler.ApplyDefaultStyle(mention);
        para.Inlines.Add(mention);
        doc.Blocks.Add(para);

        // Act, capture and inspect a snapshot
        var snapshot = doc.CreateSnapshot();
        var snapshotMention = snapshot
            .EnumerateNodes(n => n.Kind == kind)
            .OfType<MentionSnapshotNode>()
            .FirstOrDefault();

        // Assert, the handler captured the custom payload
        Assert.NotNull(snapshotMention);
        Assert.Equal("alice", snapshotMention!.UserId);
        Assert.Equal("Alice", snapshotMention.DisplayName);
    }
}
```

## 另请参阅 {#see-also}

- [RichTextEditor 参考](/controls/input/text-input/richtexteditor)
- [性能调优](/controls/input/text-input/richtexteditor/performance-tuning)
- [线程安全](/controls/input/text-input/richtexteditor/thread-safety)
