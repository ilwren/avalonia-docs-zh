---
id: thread-safety
title: Thread Safety
doc-type: explanation
tags:
 - avalonia pro
 - avalonia enterprise
---

`RichTextEditor` 的架构用不可变快照来支撑可在后台安全进行的序列化，而实时文档操作则必须在 UI 线程上进行。本指南讲解它的线程模型和安全写法。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

:::caution
这个库里没有任何东西会做异步 I/O：每种格式都是在内存缓冲区上做分词、建树或排版。`IDocumentSerializer.SerializeAsync` 和 `DeserializeAsync` 只是帮你把活儿挪出当前线程的便利封装，它们在线程池上执行同步的主体逻辑；`Serialize` 和 `Deserialize` 则是谁调用就在谁的线程上跑。

若需要把工作挪出 UI 线程，请使用随附的异步版本，或在调用处用 `Task.Run`。
:::

## 线程模型 {#threading-model}

### 必须在 UI 线程上做的事 {#ui-thread-required}

下列操作必须在 UI 线程上运行：
- **文档编辑**（`TextDocument`、`TextPointer`、`TextRange`）
- **Rendering** (`TextViewBase`, `InteractiveTextView`, `PagedTextView`, `ITextView`)
- **用户交互**（`TextSelection`、各类组件）
- **撤销/重做操作**
- **元素访问**（`FlowDocument`、`RichTextElement` 以及任何子元素——它们都是 Avalonia 的 `StyledElement`）

### 可以在后台线程上做的事 {#background-thread-safe}

下列操作可以在后台线程上运行：

- **通过 `DocumentSnapshot` 序列化** —— 它是不可变的
- **`IDocumentSerializer.Serialize` / `Deserialize`** —— 同步且不挑线程，谁调用就在谁的线程上跑。包进 `Task.Run` 即可把工作挪出 UI 线程。
- **RTF 分词** —— 流式处理
- **消费 `DocumentSnapshot`** —— `TextDocument.CreateSnapshot()` 必须在 UI 线程上调用，但返回的对象可以从任意线程安全读取。
- **`TextDocument.FromSnapshot`** —— `TextDocument` 承载整篇文档且没有线程亲和性，因此可以完全不牵涉 UI 线程就把文档实体化。

### 不是线程安全的 {#not-thread-safe}

- **活动中的 `TextDocument`** —— 不允许并发修改
- **访问 UI 元素** —— Avalonia 控件不是线程安全的
- **`TextPointer`/`TextRange`** —— 与 UI 线程上的文档绑定
- **`FlowDocumentBuilder`** —— 只能在 UI 线程上（它返回的 `FlowDocument` 本身就是一个 `StyledElement`）

## 安全写法 {#safe-patterns}

### 后台序列化 {#background-serialization}

```csharp
async Task SaveAsync(string path)
{
    // SaveAsync captures the snapshot on the calling thread, because reading
    // the document requires the thread that owns it. Then it writes on the pool.
    await using var stream = File.Create(path);
    await editor.SaveAsync(stream, new RtfSerializer());
}
```

若你需要自己掌控快照（比如用于自定义格式）：

```csharp
async Task SaveManualAsync(string path)
{
    // UI thread: snapshot the document through FlowDocument
    await using var stream = File.Create(path);
    await editor.Document.SaveAsync(stream, new RtfSerializer());
}
```

### 后台反序列化 {#background-deserialization}

```csharp
async Task LoadAsync(string path)
{
    // LoadAsync parses on the thread pool, then builds the element tree
    // on the UI thread.
    await using var stream = File.OpenRead(path);
    await editor.LoadAsync(stream, new RtfSerializer());
}
```

或者脱离编辑器单独加载：

```csharp
async Task LoadStandaloneAsync(string path)
{
    await using var stream = File.OpenRead(path);
    var document = await FlowDocument.LoadAsync(stream, new RtfSerializer());

    // Assign on UI thread
    editor.Document = document;
}
```

`FlowDocument.LoadAsync` 在线程池上解析，随后通过显式的 `Dispatcher.UIThread.InvokeAsync` 构建元素树。这里的调度是显式的，而不是依赖环境中的 `SynchronizationContext`——控制台宿主、或本就不在 UI 线程上的调用方，根本就没有这么个东西。

若希望全程不碰 UI 线程，请用序列化器读出一个 `DocumentSnapshot`，再用 `TextDocument.FromSnapshot` 把它实体化。

```csharp
// Any thread, no dispatcher involved
var snapshot = new RtfSerializer().Deserialize(stream, cancellationToken);
var textDocument = TextDocument.FromSnapshot(snapshot);
```

### 后台文档处理 {#background-document-processing}

```csharp
async Task<string> ExtractPlainTextAsync()
{
    // Read text through the public TextRange API (UI thread)
    string? text = editor.Document.ContentRange?.GetText();
    if (text == null) return string.Empty;

    // Background thread: Process the extracted text
    return await Task.Run(() =>
    {
        return ProcessText(text);
    });
}
```

## 不安全的写法 {#unsafe-patterns}

### 别在后台线程上访问活动中的文档 {#dont-access-live-document-from-background-thread}

```csharp
// WRONG — will throw
await Task.Run(() =>
{
    var doc = editor.Document?.TextDocument;
    string? text = editor.Document.ContentRange?.GetText(); // Exception
});
```

### 别在后台线程上修改文档 {#dont-modify-document-from-background-thread}

```csharp
// WRONG — will throw
await Task.Run(() =>
{
    document.ContentStart.InsertText("Hello"); // Exception
});
```

### 别在后台线程上访问 UI 元素 {#dont-access-ui-elements-from-background-thread}

```csharp
// WRONG — will throw
await Task.Run(() =>
{
    // FlowDocument and RichTextElement are Avalonia StyledElements;
    // touching their properties from a background thread throws.
    var firstParagraph = flowDocument.Blocks.FirstOrDefault();
    var background = firstParagraph?.Background; // Exception
});
```

## DocumentSnapshot 的设计 {#documentsnapshot-design}

### 不可变结构 {#immutable-structure}

`DocumentSnapshot` 就是为线程安全而设计的：
- **不可变** —— 创建之后无法修改
- **不引用 UI** —— 纯粹的数据结构
- **共享节点** —— 与活动文档高效共享内存
- **自成一体** —— 所有数据都已从活动文档复制过来

### 快照的层级结构 {#snapshot-hierarchy}

```
DocumentSnapshot (thread-safe)
├─ BlockSnapshotNode
│  ├─ InlineSnapshotNode
│  └─ InlineSnapshotNode
└─ BlockSnapshotNode
   └─ InlineSnapshotNode
```

`SnapshotNode` 是这棵树的根基，`BlockSnapshotNode` 和 `InlineSnapshotNode` 分别构成两类内容。树在捕获时一次建成，此后不再变动，它所引用的文本也是不可变的 rope 快照。因此从任意线程读取快照都是安全的。

用 `DocumentSnapshot.GetText`、`GetTextMemory` 或 `WriteTextTo` 读取文本，用 `EnumerateNodes` 遍历。

### 创建快照 {#creating-snapshots}

`SaveAsync` 和 `LoadAsync` 在内部自行创建并消费快照，因此一次寻常的保存或加载根本碰不到 `DocumentSnapshot`：

```csharp
// Save using the async API (handles snapshot internally)
await using var stream = File.Create("output.rtf");
await editor.SaveAsync(stream, new RtfSerializer());
```

若要让多个使用方共用同一份快照（比如导出成不止一种格式），请在 UI 线程上用 `FlowDocument.CreateSnapshot()` 或 `TextDocument.CreateSnapshot()` 显式捕获快照，再把结果交给后台任务：

```csharp
// UI thread
var snapshot = editor.Document.CreateSnapshot();

// Any thread. The serializers are synchronous, so Task.Run is what
// moves the work off the UI thread.
await Task.Run(() =>
{
    using var rtf = File.Create("out.rtf");
    new RtfSerializer().Serialize(snapshot, rtf);

    using var docx = File.Create("out.docx");
    new DocxSerializer().Serialize(snapshot, docx);
});
```

## FlowDocumentBuilder

`FlowDocumentBuilder` 提供了一套构建文档的流式 API。它在 UI 线程上运行：

```csharp
var builder = FlowDocumentBuilder.Create();
builder.AddParagraph("First paragraph");
builder.AddParagraph("Second paragraph");
var document = builder.Build();

editor.Document = document;
```

## 同步策略 {#synchronization-strategies}

### 调度器写法 {#dispatcher-pattern}

```csharp
async Task UpdateFromBackgroundAsync()
{
    // Background work
    var data = await FetchDataAsync();
    
    // Switch to UI thread
    await Dispatcher.UIThread.InvokeAsync(() =>
    {
        UpdateDocument(data);
    });
}
```

### async/await 写法 {#asyncawait-pattern}

```csharp
async Task SaveAndProcessAsync(string path)
{
    // Snapshot on the UI thread, write on the thread pool
    await using var stream = File.Create(path);
    await editor.SaveAsync(stream, new RtfSerializer());

    // Automatically back on UI thread after await
    ShowSaveComplete();
}
```

## 常见场景 {#common-scenarios}

### 在后台线程上做拼写检查 {#spell-check-on-background-thread}

```csharp
class SpellChecker
{
    public async Task<List<SpellError>> CheckAsync()
    {
        // UI thread: Get full text
        string? text = editor.Document.ContentRange?.GetText();
        if (string.IsNullOrEmpty(text)) return new List<SpellError>();

        // Background: Check spelling
        return await Task.Run(() =>
        {
            var errors = new List<SpellError>();
            // Run spell check algorithm on the extracted text
            return errors;
        });
    }
    
    public async Task ApplyCorrectionsAsync(
        TextDocument document,
        List<SpellError> errors)
    {
        // UI thread: Apply corrections
        await Dispatcher.UIThread.InvokeAsync(() =>
        {
            using (document.BeginChange())
            {
                foreach (var error in errors)
                {
                    var start = document.ContentStart.CreatePointer(error.Offset);
                    var end = document.ContentStart.CreatePointer(error.Offset + error.Length);
                    var range = new TextRange(start, end);
                    range.ReplaceText(error.Correction);
                }
            }
        });
    }
}
```

### 在后台统计字数 {#word-count-in-background}

```csharp
async Task<int> CountWordsAsync()
{
    // UI thread: Get text through public API
    string? text = editor.Document.ContentRange?.GetText();
    if (string.IsNullOrEmpty(text)) return 0;

    // Background: Count
    return await Task.Run(() =>
    {
        return text.Split(new[] { ' ', '\n', '\r', '\t' },
                         StringSplitOptions.RemoveEmptyEntries).Length;
    });
}
```

### 在后台线程上导出 PDF {#export-to-pdf-on-background-thread}

`PdfSerializer` 就是个普通的 `IDocumentSerializer`。和其他序列化器一样，它是同步且只写的。它接受一份快照，因此排版过程完全不牵涉 UI：

```csharp
async Task ExportPdfAsync(string path)
{
    // UI thread: capture the snapshot
    var snapshot = editor.Document.CreateSnapshot();

    // Background: lay out and write the PDF
    await Task.Run(() =>
    {
        using var stream = File.Create(path);
        new PdfSerializer().Serialize(snapshot, stream);
    });
}
```

## 元素生命周期与线程安全 {#element-lifetime-and-thread-safety}

内部节点树对它所呈现的 `RichTextElement` 实例只持有弱引用，所以模型不会把 UI 元素钉死在内存里。 

这意味着在文档把元素实体化之前，通过 `TextPointer.GetContainingElement()` 拿到的元素可能是 `null`。所有元素访问都只能在 UI 线程上进行。

```csharp
void SafeAccessElement(TextPointer pointer)
{
    // Pointers are UI-thread only.
    if (!Dispatcher.UIThread.CheckAccess())
    {
        throw new InvalidOperationException("Must be on UI thread");
    }

    var element = pointer.EnsureElement(); // materializes if needed
    if (element != null)
    {
        ProcessElement(element);
    }
}
```

直接读取元素树时同样如此：

```csharp
// Must be on UI thread
var firstBlock = flowDocument.Blocks.FirstOrDefault();
if (firstBlock != null)
{
    var background = firstBlock.Background;
}
```

## 实践建议 {#best-practices}

### Do's

1. **在 UI 线程上创建快照** —— 这是个快操作
2. **在后台线程上处理快照** —— 既安全又高效
3. **回到 UI 线程再更新文档** —— 用 Dispatcher
4. **做 UI 操作前先检查线程** —— 防御式编程
5. **用 async/await 让代码清爽** —— 线程切换顺理成章

### Don'ts

1. **别在后台线程上访问活动中的文档**
2. **别在后台线程上修改文档**
3. **别在后台线程上访问 UI 元素**
4. **别指望快照会自动更新** —— 它们是不可变的
5. **别长期持有元素引用** —— 要用的时候再从指针解析出来

## 性能考量 {#performance-considerations}

### 创建快照的开销 {#snapshot-creation-cost}

- **小文档（&lt;10KB）**：约 1 毫秒
- **大文档（1MB）**：约 10 毫秒
- **影响**：对后台操作而言可以忽略不计

### 线程切换的开销 {#thread-switching-cost}

- **Dispatcher 调用**：约 1-2 毫秒的额外开销
- **建议**：把界面更新攒成批，别每个字符都切一次线程

### 最佳写法 {#optimal-pattern}

```csharp
// Bad: Too many thread switches
await Task.Run(async () =>
{
    for (int i = 0; i < 1000; i++)
    {
        await Dispatcher.UIThread.InvokeAsync(() =>
        {
            UpdateUI(i); // 1000 dispatches
        });
    }
});

// Good: One switch
var results = await Task.Run(() =>
{
    var items = new List<Item>();
    for (int i = 0; i < 1000; i++)
    {
        items.Add(ProcessItem(i));
    }
    return items;
});

await Dispatcher.UIThread.InvokeAsync(() =>
{
    UpdateUIBatch(results); // 1 dispatch
});
```

## 另请参阅 {#see-also}

- [RichTextEditor 参考](/controls/input/text-input/richtexteditor)
- [性能调优](/controls/input/text-input/richtexteditor/performance-tuning)
- [扩展范式](/controls/input/text-input/richtexteditor/extension-patterns)
