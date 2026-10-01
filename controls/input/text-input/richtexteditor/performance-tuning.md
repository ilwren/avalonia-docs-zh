---
id: performance-tuning
title: Performance Tuning
doc-type: how-to
tags:
 - avalonia pro
 - avalonia enterprise
---

`RichTextEditor` 的性能调优指南，涵盖批量编辑、事件优化、内存管理、序列化和性能剖析策略。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 核心性能特征 {#core-performance-characteristics}

### 时间复杂度 {#time-complexity}

| 操作 | 复杂度 | 注释支持情况 |
|-----------|-----------|-------|
| 插入文本 | O(log n) | rope 数据结构 |
| 删除文本 | O(log n) | 平衡树更新 |
| 查找位置 | O(log n) | 树遍历 |
| Undo/Redo | O(1) - O(log n) | 结构性撤销 |
| Serialize | O(n) | 流式分词器 |
| Render | O(可见节点数) | 视口剔除 |

### 内存占用 {#memory-usage}

- **文档**：O(n) 文本 + O(m) 节点
- **rope 额外开销**：约为基础文本的 2 倍
- **撤销栈**：采用结构性撤销约为 10%（传统做法则是 100 倍）
- **快照**：共享结构，开销极小

## 性能自查清单 {#performance-checklist}

- 凡是多步编辑，一律批量进行
- 开销大的操作请用 `TextDocument.Changed`（每次提交触发一次），而不是 `TextDocument.TextChanged`（每次编辑都触发）
- 对用户触发的更新做防抖
- 给编辑器设置合适的 `UndoLimit`
- 批量加载期间关闭撤销
- 序列化放到后台线程
- 尽量少分配指针对象
- 先剖析，再优化

## 批量编辑优化 {#batch-edit-optimization}

### 多步操作务必批量执行 {#always-batch-multiple-operations}

只发出一次变更通知，而不是每次编辑都发一次：

```csharp
// Bad: 100 Changed events, 100 layout passes
for (int i = 0; i < 100; i++)
{
    pointer.InsertText("Line " + i + "\n");
}

// Good: 1 Changed event, 1 layout pass
using (document.BeginChange())
{
    for (int i = 0; i < 100; i++)
    {
        pointer.InsertText("Line " + i + "\n");
    }
}
```

**效果**：批量操作提速 10 到 100 倍。

## 事件处理程序优化 {#event-handler-optimization}

### 把重活儿往后挪 {#defer-expensive-operations}

请处理 `TextDocument.Changed`——它在每个变更作用域提交时触发一次，不必对每一次编辑都作出反应：

```csharp
// Bad — called for every keystroke
editor.ContentChanged += (s, e) =>
{
    RebuildUI();
};

// Good — called once per batch
var textDoc = editor.Document.TextDocument;
textDoc.Changed += (s, e) =>
{
    // Changed is suppressed on no-op scopes, so e.HasChanges is true here.
    RebuildUI();
};
```

`TextDocument` 会引发两种变更事件：(1) `TextChanged` 每次文本编辑触发一次，带一个 `TextChangeEventArgs`；(2) `Changed` 在变更作用域提交时触发一次，带一个携有 `HasChanges` 的 `DocumentChangedEventArgs`。开销大的工作最好交给 `Changed` 来处理。

### 对用户触发的更新做防抖 {#debounce-user-triggered-updates}

```csharp
private DispatcherTimer _updateTimer;

void Setup()
{
    _updateTimer = new DispatcherTimer
    {
        Interval = TimeSpan.FromMilliseconds(300)
    };
    _updateTimer.Tick += OnDelayedUpdate;

    editor.ContentChanged += (s, e) =>
    {
        _updateTimer.Stop();
        _updateTimer.Start(); // Restart timer
    };
}

void OnDelayedUpdate(object? sender, EventArgs e)
{
    _updateTimer.Stop();
    // Expensive operation (word count, spell check, etc.)
    UpdateStatistics();
}
```

**效果**：降低连续输入期间的 CPU 占用。

## 指针与区间优化 {#pointer-and-range-optimization}

### 尽量少分配指针对象 {#minimize-pointer-allocations}

```csharp
// Bad — creating a pointer per character index
for (int i = 0; i < 1000; i++)
{
    var p = document.ContentStart.CreatePointer(i); // allocates, O(log n) per call
}

// Good — snapshot once and read text in bulk
var snapshot = document.CreateSnapshot();
string slice = snapshot.GetText(offset: 0, length: 1000);
for (int i = 0; i < slice.Length; i++)
{
    char c = slice[i]; // direct array access
}
```

`DocumentSnapshot.GetText`、`GetTextMemory` 和 `WriteTextTo` 都能取出子串，而不必为每个字符分配指针。

### 能复用指针时就复用 {#reuse-pointers-when-possible}

```csharp
var pointer = document.ContentStart.CreatePointer(0);
for (int i = 0; i < 100; i++)
{
    pointer.InsertText("Line\n");
    // pointer auto-updates to after insertion
}
```

## 内存管理 {#memory-management}

### 限制撤销栈大小 {#undo-stack-limits}

```csharp
// Default: 100 operations (set via RichTextEditor.UndoLimit)
editor.UndoLimit = 50;  // Reduce for memory-constrained environments
editor.UndoLimit = 200; // Increase for power users
```

**取舍**：内存占用与撤销历史深度之间的权衡。

### 批量加载时关闭撤销 {#disable-undo-for-bulk-loads}

`RichTextEditor.UndoManager` 和 `TextDocument.UndoManager` 的类型都是 `UndoManager?`。若要完全不记录，可以用 `IsEnabled` 把实例关掉，或把文档的管理器设为 `null`——框架没有可供替换的空对象管理器。

```csharp
void LoadLargeDocument(string rtfPath)
{
    UndoManager? undoManager = editor.UndoManager;
    if (undoManager != null)
        undoManager.IsEnabled = false;

    try
    {
        using var stream = File.OpenRead(rtfPath);
        editor.Load(stream, new RtfSerializer());
    }
    finally
    {
        if (undoManager != null)
            undoManager.IsEnabled = true;
    }
}
```

**效果**：加载快 50%，且没有撤销带来的内存开销。

### 必要时清空撤销历史 {#clear-undo-history-when-needed}

```csharp
// After saving document
editor.ClearUndoHistory();
```

## 序列化性能 {#serialization-performance}

### 用后台线程 {#use-background-threads}

`IDocumentSerializer` 是同步的：你在哪个线程调用 `Serialize` 和 `Deserialize`，它们就在哪个线程上跑。`SaveAsync` 和 `LoadAsync` 是随附的封装，会把工作挪到线程池上，让你自行决定序列化在哪个线程进行。

```csharp
async Task SaveDocumentAsync(string path)
{
    // SaveAsync captures the snapshot on the calling thread, then writes
    // on the thread pool.
    await using var stream = File.Create(path);
    await editor.SaveAsync(stream, new RtfSerializer());
}
```

**效果**：保存时不再卡住界面。

自己驱动序列化器时，请把调用包起来：

```csharp
var snapshot = editor.Document.CreateSnapshot();   // UI thread, cheap
await Task.Run(() => serializer.Serialize(snapshot, stream, cancellationToken), cancellationToken);
```

一份快照可以喂给多个序列化器，省去每种格式各遍历一次树的重复开销。

### 大文件用流式处理 {#stream-large-files}

```csharp
// Streaming tokenizer handles large files efficiently
await using var stream = File.OpenRead("large.rtf");
await editor.LoadAsync(stream, new RtfSerializer());
// Memory usage: O(output size), not O(file size)
```

## 渲染性能 {#rendering-performance}

### 视口剔除 {#viewport-culling}

内置能力：只渲染可见元素，无需你做任何事。

### 减少布局遍数 {#reduce-layout-passes}

```csharp
// Batch formatting changes
using (document.BeginChange())
{
    range1.ApplyPropertyValue(prop1, value1);
    range2.ApplyPropertyValue(prop2, value2);
    range3.ApplyPropertyValue(prop3, value3);
}
// Single layout pass
```

### 简化复杂文档 {#simplify-complex-documents}

- 控制嵌套深度（小于 10 层）
- 合并格式相同的相邻文本段
- 使用元数据规范化

### 插入符的上下移动 {#vertical-caret-navigation}

<kbd>↑</kbd> and <kbd>↓</kbd> 是按结构遍历文档树来实现的，而不是靠扫描视觉行去找 Y 坐标的变化。因此：

- 开销取决于树的深度，而非可见行数。在一个 50 行 50 列的表格里按一次键，开销大致是行数加上下降深度的量级。
- 目标列在第一次按上下键时记录一次，之后一直沿用，直到选区因上下移动之外的原因发生变化为止。正是这种沿用，才让插入符在短行、空段落和表格单元格之间上下移动时始终停在同一视觉列上。

任何非上下方向的选区变化都会丢弃这个列意图，比如点击、以代码设置 `Select`、左右方向键、<kbd>Home</kbd>、<kbd>End</kbd> 或按词跳转。若希望保住列位置，请避免在连续按 <kbd>↑</kbd> / <kbd>↓</kbd> 的间隙清除或重新赋值 `Selection.CaretPosition`。

### 页面布局 {#page-layout}

编辑引发重新分页时，分页布局会让纸面一直留在屏幕上，而不是拆掉断页表、等空闲时再重建。屏幕、打印和 PDF 导出共用同一套分页策略，断页位置完全一致；而分页的开销每个模型只付一次。

## 大文档应对策略 {#large-document-strategies}

### 已验证的规模 {#tested-limits}

- 10,000+ paragraphs
- 1MB 以上的 RTF 文件
- 100 步以上的撤销操作

### 超大文档（100MB 以上） {#for-very-large-documents-100mb}

可以考虑：
1. **分段** —— 按需加载各小节
2. **虚拟滚动** —— 只渲染可见的页面
3. **只读模式** —— 通过 `FlowDocumentScrollViewer` 关闭撤销以节省内存
4. **流式处理** —— 分块处理

## Benchmarking

### 内置基准测试 {#built-in-benchmarks}

```bash
cd benchmarks/Avalonia.Controls.Documents.Benchmarks
dotnet run -c Release
```

基准测试涵盖：
- 文本插入/删除
- 批量编辑
- Serialization
- 元数据规范化

### 自定义基准测试 {#custom-benchmarks}

```csharp
using BenchmarkDotNet.Attributes;
using BenchmarkDotNet.Running;

[MemoryDiagnoser]
public class CustomBenchmark
{
    private TextDocument _document;
    
    [GlobalSetup]
    public void Setup()
    {
        _document = new TextDocument("Initial text");
    }
    
    [Benchmark]
    public void BulkInsert()
    {
        var pointer = _document.ContentStart.CreatePointer(0);

        // BeginChange returns an IDisposable; there is no public EndChange.
        using (_document.BeginChange())
        {
            for (int i = 0; i < 1000; i++)
            {
                pointer.InsertText("X");
            }
        }
    }
}
```

运行方式：

```csharp
BenchmarkRunner.Run<CustomBenchmark>();
```

## Anti-patterns

### 别轮询文档状态 {#dont-poll-document-state}

```csharp
// Bad: Polling
var timer = new DispatcherTimer { Interval = TimeSpan.FromMilliseconds(100) };
timer.Tick += (s, e) => CheckDocumentState();

// Good: Event-driven
var textDoc = editor.Document.TextDocument;
textDoc.Changed += (s, e) => UpdateState();
```

### 别每敲一个键就重建界面 {#dont-rebuild-ui-on-every-keystroke}

```csharp
// Bad
editor.ContentChanged += (s, e) => RebuildEntireUI();

// Good
var textDoc = editor.Document.TextDocument;
textDoc.Changed += (s, e) =>
{
    if (e.HasChanges)
        RefreshAffectedRegions();
};
```

### 别为了撤销而保存整份文本副本 {#dont-store-full-text-copies-for-undo}

```csharp
// Bad: Undo via full text
undoStack.Push(editor.Document.ContentRange?.GetText() ?? "");

// Good: Built-in UndoManager (auto-created by the editor)
editor.UndoLimit = 100;
```

## 性能剖析小贴士 {#profiling-tips}

### 善用诊断工具 {#use-diagnostic-tools}

**Windows**: Visual Studio Performance Profiler  
**macOS/Linux**：dotnet-trace、PerfView

### 需要盯住的热点路径 {#hot-paths-to-monitor}

1. `TextRange.DeleteText` / `ReplaceText` and `TextPointer.InsertText`
2. rope 相关操作——它们是 internal 的，体现为上述各项所耗的时间
3. `TextViewBase` / `InteractiveTextView` 中的布局，以及分页布局中 `PagedTextView` 的布局
4. `TextDocument.TextChanged` 和 `TextDocument.Changed` 上的事件处理程序

### 危险信号 {#red-flags}

- 自定义事件处理程序中出现 O(n^2) 算法
- 分配过多（简单编辑就超过 1MB）
- 布局反复重算（一次编辑跑了好几遍布局）
- 撤销栈无限膨胀

## 另请参阅 {#see-also}

- [RichTextEditor 参考](/controls/input/text-input/richtexteditor)
- [线程安全](/controls/input/text-input/richtexteditor/thread-safety)
- [扩展范式](/controls/input/text-input/richtexteditor/extension-patterns)
