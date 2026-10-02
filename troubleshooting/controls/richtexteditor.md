---
id: richtexteditor
title: RichTextEditor 问题
description: 排查 RichTextEditor 的常见毛病。
doc-type: troubleshooting
sidebar_label: RichTextEditor
tags:
  - avalonia pro
  - avalonia enterprise
---

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

该控件的参考信息请见 [RichTextEditor](/controls/input/text-input/richtexteditor) 页。

## 查看器什么都不显示 {#a-viewer-shows-nothing}

`FlowDocumentScrollViewer.Document` 和 `FlowDocumentPageViewer.Document` 初始均为 null，因此没有指定文档的查看器只会渲染一片空白，并不会报错。

```csharp
viewer.Document = new FlowDocument
{
    Blocks = { new Paragraph { Inlines = { new RichRun("Hello") } } }
};
```

`RichTextEditor.Document` 则不同：编辑器会自行创建一个空的 `FlowDocument`，所以除非你主动赋了 null，它永远不会是 null。

## 撤销没反应 {#undo-does-nothing}

文档挂上来时编辑器会替你创建一个 `UndoManager`，不需要你自己装配。`RichTextEditor.UndoManager` 是只读的，只是告诉你当前用的是哪一个。

有两种情况会让撤销失效：

```csharp
// Recording is disabled
editor.UndoManager!.IsEnabled = false;

// Or the history is too short to hold the edit
editor.UndoLimit = 0;
```

你自己构造并赋给 `TextDocument.UndoManager` 的文档会被原样采用——编辑器会沿用其中已有的管理器，而不是另起一个顶替。

## 编辑的结果没有显现 {#edits-do-not-appear}

把若干操作归成一次变更，视图便只刷新一次，撤销时也当作一步处理。`BeginChange` 返回一个 `IDisposable`，因此作用域随 `using` 块结束而结束。

```csharp
using (document.TextDocument.BeginChange())
{
    // Your edits
}
```

## 在后台线程加载的文档，首次使用时抛异常 {#a-document-loaded-on-a-background-thread-throws-on-first-use}

`FlowDocument` 及其元素会绑定到构造它们的那个线程的 dispatcher 上，因此在线程池线程上拼出来的文档，UI 线程第一次读它的属性时就会抛 `InvalidOperationException`。

`FlowDocument.LoadAsync` 替你处理了这件事：它在调用线程上解析，再通过 UI 线程的 dispatcher 构建元素树。

若想全程不碰 UI 线程，那就直接操作模型而非外观层。`TextDocument` 不绑定线程：

```csharp
var snapshot = serializer.Deserialize(stream);
var document = TextDocument.FromSnapshot(snapshot);
```

## 导出的 PDF 里文字是乱的 {#text-in-an-exported-pdf-is-unreadable}

若某款字体的 OS/2 `fsType` 禁止嵌入，它就嵌不进去，导出时会换用别的字体。与其凭空猜测，不如直接问导出器它到底做了什么：

```csharp
var options = new PdfSerializerOptions
{
    Diagnostics = d => Console.WriteLine($"{d.Kind}: {d.Message}")
};
```

## 调试线程问题 {#debugging-threading-issues}

### 启用线程断言 {#enable-thread-assertions}

Avalonia 内置了线程检查：

```csharp
// Throws if not on UI thread
Dispatcher.UIThread.VerifyAccess();
```

### 常见异常 {#common-exceptions}

**InvalidOperationException**：“The calling thread cannot access this object because a different thread owns it.”
- **原因**：`FlowDocument` 或某个元素在一个线程上构造，却被另一个线程读取。
- **解决办法**：在 UI 线程上构建外观层，或者改用不绑定线程的 `TextDocument` 和 `DocumentSnapshot`。

编辑过程中序列化器抛出 **InvalidOperationException**。
- **原因**：在文档正被编辑时去序列化这个活动文档。
- **解决办法**：先在 UI 线程上取一个 `DocumentSnapshot` 快照，之后随你在哪儿序列化这份快照都行。

## 另请参阅 {#see-also}

- [RichTextEditor 控件](/controls/input/text-input/richtexteditor)
- [线程安全](/controls/input/text-input/richtexteditor/thread-safety)
