---
id: printing-and-sharing
title: Printing and sharing
description: Print and share PDF documents from the Avalonia PdfViewer through the native print dialog and share sheet, or handle the request with your own pipeline.
doc-type: how-to
tags:
  - avalonia pro
  - avalonia enterprise
---

**Print** and **Share** live in the toolbar's **More Options** menu and are also available as `Print()`, `PrintAsync()`, `Share()`, `ShareAsync()`, `PrintCommand` and `ShareCommand`. Both include the current edits.

## 平台支持 {#platform-support}

| 平台 | Print | Share |
|---|---|---|
| Windows | Standard print dialog, vector output. | Windows share sheet. Falls back to a save-a-copy picker if the share UI is unavailable. |
| macOS | System print panel with preview. | System share picker, anchored to the toolbar button. |
| iOS | System print controller. | System share sheet, as a popover on iPad. |
| Android | System print framework. | Share chooser. No manifest changes are needed. |
| Linux | Not built in. | Not built in. |
| Browser | Not built in. | Not built in. |

The menu entries are hidden when the platform has no service and the app does not handle the request. `CanPrint` and `CanShare` report whether printing or sharing is possible right now. Hide the entries explicitly with `IsPrintVisible`, `IsShareVisible` or `IsMoreOptionsVisible`.

## Print or share from code

```csharp
await Viewer.PrintAsync();
await Viewer.ShareAsync();
```

`PrintAsync` accepts a `PrintOptions` (`Title`, `PageRange`, `Copies`, `Color`, `Duplex`, `Orientation`, `Scaling`) and `ShareAsync` a `ShareOptions` (`Title`, `Text`, `Subject`). Both are in the `Avalonia.Controls.Pdf.Services` namespace. The viewer fills in `Owner` and `Anchor` on both.

## Handle the request in your app

Handle `PrintRequested` or `ShareRequested` to take over. Set `Handled` to `true` before the first `await` and the built-in service is skipped. `GetDocumentBytesAsync()` returns the PDF with its edits. This is also how you add printing on Linux and in the browser.

```csharp
Viewer.PrintRequested += async (_, e) =>
{
    e.Handled = true;
    var pdf = await e.GetDocumentBytesAsync();
    await myPrintPipeline.PrintAsync(pdf, e.Options.Title);
};
```

## Replace the platform service

To replace the platform implementation, assign your own `IPrintService` or `IShareService` to `PrintService` or `ShareService`. `IPrintService` has `PrintAsync(IPdfDocument, PrintOptions?, CancellationToken)` and `ShowPrintPreviewAsync(IPdfDocument, PrintOptions?)`. `IShareService` has `ShareAsync(IPdfDocument, ShareOptions?, CancellationToken)` and `ShareFileAsync(string filePath, ShareOptions?, CancellationToken)`. Leave a property unset to use the built-in service, or set it to `null` to remove the feature.

```csharp
Viewer.PrintService = new MyPrintService();
Viewer.ShareService = null; // no Share entry
```

## 另请参阅 {#see-also}

- [PdfViewer 控件](index.md)
- [加载与保存](loading-and-saving.md)
- [平台与性能](platforms-and-performance.md)
