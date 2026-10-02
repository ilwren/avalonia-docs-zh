---
id: loading-and-saving
title: 加载与保存文档
description: 把 PDF 文档从路径、流或字节数组加载进 Avalonia PdfViewer，处理密码与权限，并把改动就地保存或另存为副本。
doc-type: how-to
tags:
  - avalonia pro
  - avalonia enterprise
---

## 加载文档 {#load-a-document}

把 `Source` 设成文件路径，查看器就会加载它。当来源可能是文件路径 `string`、`Stream` 或 `byte[]` 时，可改用支持绑定的 `DocumentSource`。传给 `DocumentSource` 的字符串会被转交给 `Source` 处理，因此就地保存依然可用。在代码中则调用 `LoadDocumentAsync`。

```csharp
// From a file path
await Viewer.LoadDocumentAsync("/path/to/document.pdf");

// From a stream
await using var stream = File.OpenRead("/path/to/document.pdf");
await Viewer.LoadDocumentAsync(stream);

// From bytes in memory
byte[] bytes = await File.ReadAllBytesAsync("/path/to/document.pdf");
await Viewer.LoadDocumentAsync(bytes);
```

| 方法 | 说明 |
|---|---|
| `LoadDocumentAsync(string path, string? password = null)` | 从文件路径加载 PDF。 |
| `LoadDocumentAsync(Stream stream, string? password = null)` | 从流加载 PDF。读取从流的当前位置开始；若流可定位且已到末尾，则从头开始读。 |
| `LoadDocumentAsync(ReadOnlyMemory<byte> data, string? password = null)` | 从内存中的字节加载 PDF。整个数组会被直接使用，若传入的是切片则会复制一份。 |
| `CloseDocument()` | 关闭当前文档并释放其原生状态。 |
| `ClearError()` | 清除 `ErrorMessage`。已打开的文档保持打开。 |

文档加载完成时触发 `DocumentLoaded`，参数中带有 `PageCount` 和 `Metadata`。加载失败时触发 `LoadError`，错误信息同时显示在画布上，也会体现在可绑定的 `ErrorMessage` 属性中。

```csharp
Viewer.DocumentLoaded += (_, e) =>
    Title = $"{e.Metadata.Title} ({e.PageCount} pages)";

Viewer.LoadError += (_, e) =>
    Console.WriteLine($"Load failed: {e.Message}");
```

## 带密码保护的文档 {#password-protected-documents}

把密码传给 `LoadDocumentAsync`，或者在设置 `Source` 之前先设好 `Password`。若加载加密文档时没有提供密码，查看器会弹出提示框，让用户重新输入。

```csharp
await Viewer.LoadDocumentAsync("/path/to/encrypted.pdf", password: "secret");
```

## 文档权限 {#document-permissions}

PDF 可以禁止批注、表单填写、复制或打印。当 `RespectDocumentPermissions` 为 `true`（默认）时，文档禁止哪一项，查看器就相应地关闭哪一项。用所有者密码打开的文档不受任何限制。把 `RespectDocumentPermissions` 设为 `false` 即可忽略这些标志。

文档的各项标志以 `PdfPermissions` 的形式呈现在 `Permissions` 属性上，包含 `CanPrint`、`CanPrintHighQuality`、`CanModify`、`CanCopyContent`、`CanAnnotate`、`CanFillForms`、`CanExtractForAccessibility` 和 `CanAssemble`。未打开任何文档时它为 `null`。

你自己设的闸门则是另一回事：

| 属性 | 效果 |
|---|---|
| `IsReadOnly` | 一个开关即可禁止批注和表单编辑。此时各工具都会解除激活，选中的批注也不能移动或删除。 |
| `AllowTextSelection` | 启用文本选择与复制。 |
| `AllowAnnotationEditing` | 启用批注的创建与编辑。 |
| `AllowFormEditing` | 启用交互式表单字段的编辑。 |
| `AllowDocumentSaving` | 启用保存。它同时把关 `SaveCommand` 和 `SaveAsync`。 |

`CanEditAnnotations` 给出的是综合结果：`IsReadOnly` 未被禁用、`AllowAnnotationEditing` 为 `true`，且在 `RespectDocumentPermissions` 开启时文档本身也允许。

## 保存文档 {#save-a-document}

每次保存都会把批注改动、表单取值、涂黑删除和书签一并写入文档。

| 方法 | 说明 |
|---|---|
| `SaveAsync()` / `Save()` | 就地覆盖保存到 `Source`，受 `AllowDocumentSaving` 约束。从流或字节数组加载的文档没有路径：此时 `SaveAsync` 会抛出 `InvalidOperationException`，`Save()` 则通过 `ErrorMessage` 报告这一情况。 |
| `SaveDocumentAsync(string filePath)` | 保存到指定路径。 |
| `SaveDocumentAsync(Stream stream)` | 保存到流。 |
| `SaveAsAsync()` / `SaveAs()` | 弹出平台保存选择器，把文档写入用户选定的文件；否则触发 `SaveAsRequested`。 |

```csharp
// Save a copy
await Viewer.SaveDocumentAsync("/path/to/output.pdf");

// Save to a stream
await using var output = new MemoryStream();
await Viewer.SaveDocumentAsync(output);
```

文档存在未保存的改动时 `IsDirty` 为 `true`。保存成功或加载另一份文档后，该标志会被清除。

把 `AutoSave` 设为 `true`，每次批注、表单或涂黑删除改动后都会写回 `Source`。这需要 `AllowDocumentSaving`，且文档必须是从路径加载的。

### 带数字签名的文档 {#signed-documents}

带数字签名的文档会以增量更新的方式保存，这样已签名的版本保持完好，阅读器仍能验证签名。其他文档则整份重写。

## 「打开」「保存」「另存为」菜单项 {#open-save-and-save-as-menu-entries}

**更多选项**菜单还能显示**打开**、**保存**和**另存为**三项，它们默认关闭。可分别用 `IsOpenVisible`、`IsSaveVisible` 和 `IsSaveAsVisible` 逐项开启。

- **打开**会弹出平台文件选择器并加载选中的文件。若文件带有本地路径，就按路径打开，这样就地保存依然可用；若选择器给不出路径（浏览器、部分移动端选择器），则通过流读取该文件。
- **保存**执行就地保存。当 `AllowDocumentSaving` 为 `false` 时该项隐藏；对于从流加载的文档，该项为禁用状态。
- **另存为**会弹出平台保存选择器，把带改动的文档写出去。如果用户选了另一个本地文件，查看器会切换到那个文件，并停留在当前页。

无论菜单是否显示这三项，它们都一并提供 `Open()`、`OpenAsync()`、`SaveAs()`、`SaveAsAsync()`、`OpenCommand` 和 `SaveAsCommand` 供调用。

### 改用你自己的对话框 {#use-your-own-dialogs}

处理 `OpenRequested` 或 `SaveAsRequested`，并把 `Handled` 设为 `true`，即可取代内置的选择器。`PdfSaveAsRequestedEventArgs.GetDocumentBytesAsync()` 会返回待写出的 PDF。

```csharp
Viewer.SaveAsRequested += async (_, e) =>
{
    e.Handled = true;
    var pdf = await e.GetDocumentBytesAsync();
    await myDocumentStore.SaveAsync(pdf);
};
```

## Lifecycle

- 把查看器从视觉树上摘下来（比如切换选项卡时），文档、未保存的改动、撤销历史、当前页和缩放级别都会保留。重新挂回去时，它们会原样回来。
- `Source` 可以在查看器挂到视觉树之前就设好，文档会在挂上之后绘制出来。
- 关闭窗口会释放原生文档，`CloseDocument()` 同样如此。
- 传给查看器的 `Stream` 只会被读取一次，且不会被释放，所以请在加载调用返回之后自行释放它。而 `byte[]` 会在文档的整个生命周期内被直接使用，文档打开期间不得修改它。

## 另请参阅 {#see-also}

- [PdfViewer 控件](index.md)
- [打印与分享](printing-and-sharing.md)
- [平台与性能](platforms-and-performance.md)
