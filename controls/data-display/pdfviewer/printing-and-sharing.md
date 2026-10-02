---
id: printing-and-sharing
title: 打印与分享
description: 通过原生打印对话框和分享面板，从 Avalonia PdfViewer 打印和分享 PDF 文档，也可以用自己的流程接管这些请求。
doc-type: how-to
tags:
  - avalonia pro
  - avalonia enterprise
---

**打印**和**分享**位于工具栏的**更多选项**菜单中，同时也以 `Print()`、`PrintAsync()`、`Share()`、`ShareAsync()`、`PrintCommand` 和 `ShareCommand` 的形式提供。两者都会带上当前的改动。

## 平台支持 {#platform-support}

| 平台 | 打印 | 分享 |
|---|---|---|
| Windows | 标准打印对话框，矢量输出。 | Windows 分享面板。分享界面不可用时，回退为「保存副本」选择器。 |
| macOS | 系统打印面板，带预览。 | 系统分享选择器，锚定在工具栏按钮上。 |
| iOS | 系统打印控制器。 | 系统分享面板，在 iPad 上以浮出框形式呈现。 |
| Android | 系统打印框架。 | 分享选择器，无需改动清单文件。 |
| Linux | 未内置。 | 未内置。 |
| Browser | 未内置。 | 未内置。 |

当平台没有相应服务、应用又不处理该请求时，对应的菜单项会隐藏。`CanPrint` 和 `CanShare` 会报告此刻能否打印或分享。若要显式隐藏这些菜单项，请使用 `IsPrintVisible`、`IsShareVisible` 或 `IsMoreOptionsVisible`。

## 用代码打印或分享 {#print-or-share-from-code}

```csharp
await Viewer.PrintAsync();
await Viewer.ShareAsync();
```

`PrintAsync` 接受一个 `PrintOptions`（`Title`、`PageRange`、`Copies`、`Color`、`Duplex`、`Orientation`、`Scaling`），`ShareAsync` 则接受一个 `ShareOptions`（`Title`、`Text`、`Subject`）。两者都位于 `Avalonia.Controls.Pdf.Services` 命名空间下。查看器会为两者自动填好 `Owner` 和 `Anchor`。

## 在应用中自行处理请求 {#handle-the-request-in-your-app}

处理 `PrintRequested` 或 `ShareRequested` 即可接管。在首次 `await` 之前把 `Handled` 设为 `true`，内置服务就会被跳过。`GetDocumentBytesAsync()` 会返回带改动的 PDF。在 Linux 和浏览器上添加打印能力，走的也是这条路。

```csharp
Viewer.PrintRequested += async (_, e) =>
{
    e.Handled = true;
    var pdf = await e.GetDocumentBytesAsync();
    await myPrintPipeline.PrintAsync(pdf, e.Options.Title);
};
```

## 替换平台服务 {#replace-the-platform-service}

若要替换平台实现，请把你自己的 `IPrintService` 或 `IShareService` 赋给 `PrintService` 或 `ShareService`。`IPrintService` 带有 `PrintAsync(IPdfDocument, PrintOptions?, CancellationToken)` 和 `ShowPrintPreviewAsync(IPdfDocument, PrintOptions?)`，`IShareService` 带有 `ShareAsync(IPdfDocument, ShareOptions?, CancellationToken)` 和 `ShareFileAsync(string filePath, ShareOptions?, CancellationToken)`。属性留空则使用内置服务，设为 `null` 则关闭该功能。

```csharp
Viewer.PrintService = new MyPrintService();
Viewer.ShareService = null; // no Share entry
```

## 另请参阅 {#see-also}

- [PdfViewer 控件](index.md)
- [加载与保存](loading-and-saving.md)
- [平台与性能](platforms-and-performance.md)
