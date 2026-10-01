---
id: pdfviewer
title: PdfViewer 问题
description: 排查 Avalonia 中 PdfViewer 的常见毛病，包括控件一片空白、许可证报错、保存失败、打印项缺失以及浏览器托管。
doc-type: troubleshooting
sidebar_label: PdfViewer
tags:
  - avalonia pro
  - avalonia enterprise
---

## 控件什么都不显示 {#the-control-renders-nothing}

在引入它的某套主题之前，`PdfViewer` 是没有模板的，于是它占着位置却什么也画不出来。

**解决办法：**把 `Default.axaml` 或 `Fluent.axaml` 的 `StyleInclude` 加进 `App.axaml`：

```xml
<Application.Styles>
    <FluentTheme />
    <StyleInclude Source="avares://Avalonia.Controls.PdfViewer/Themes/Default.axaml" />
</Application.Styles>
```

请见[快速上手](/controls/data-display/pdfviewer#getting-started)。

## 首次使用查看器时报 `AvaloniaLicensingException` {#avalonialicensingexception-when-the-viewer-is-first-used}

控件会在首次使用时检查许可证密钥；若密钥缺失或不涵盖 PDF Viewer，就会抛出 `AvaloniaLicensingException`。

**解决办法：**在每个应用 head（桌面、iOS、Android 和浏览器）中都引用 `AvaloniaUI.Licensing` 包，并在各自的项目文件里加上 `AvaloniaUILicenseKey` 项。另请到 [Avalonia 门户](https://portal.avaloniaui.net)确认你的许可证确实涵盖 PDF Viewer。请见[安装 Avalonia Pro](/tools/installing-avalonia-pro)。

## XAML 里找不到 `PdfViewer` {#xaml-cannot-find-pdfviewer}

该控件位于 `Avalonia.Controls` 命名空间，而这个命名空间并不属于默认的 Avalonia XAML 命名空间。

**解决办法：**给该命名空间映射一个前缀，然后在元素上使用它：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:pdf="using:Avalonia.Controls">
    <pdf:PdfViewer Source="/path/to/document.pdf" />
</Window>
```

## `SaveAsync` throws `InvalidOperationException`

`SaveAsync` 会就地覆盖 `Source` 保存。而从流或字节数组加载的文档没有可写回的路径。`Save()` 遇到同样的情况不会抛异常，而是通过 `ErrorMessage` 告知你。

**解决办法：**改用带路径或流的 `SaveDocumentAsync`，或者用 `SaveAsAsync` 弹出平台的保存选取框。请见[保存文档](/controls/data-display/pdfviewer/loading-and-saving#save-a-document)。

## 批注工具呈灰色不可用 {#annotation-tools-are-greyed-out}

下列情形下工具会被禁用，此时 `CanEditAnnotations` 为 `false`：`IsReadOnly` 为 `true` 时、`AllowAnnotationEditing` 为 `false` 时，或者 `RespectDocumentPermissions` 已开启而文档本身禁止批注时。

**解决办法：**查看 `Permissions` 属性了解文档的权限标志。把 `RespectDocumentPermissions` 设为 `false` 可无视这些限制，或者用文档的所有者密码打开它，限制便会解除。请见[文档权限](/controls/data-display/pdfviewer/loading-and-saving#document-permissions)。

## “更多选项”菜单里没有打印或共享 {#print-or-share-is-missing-from-the-more-options-menu}

当平台没有内置相应服务、应用自身又不处理该请求时，这些菜单项会被隐藏。Linux 和浏览器上没有内置的打印与共享。

**解决办法：**处理 `PrintRequested` 或 `ShareRequested`，把 `Handled` 设为 `true`，再从 `GetDocumentBytesAsync()` 取出 PDF 字节。请见[打印与共享](/controls/data-display/pdfviewer/printing-and-sharing)。

## 调用 `*Async` 时抛出关于 UI 线程的异常 {#an-async-call-throws-about-the-ui-thread}

`PdfViewer` 的每个公共成员都必须在 Avalonia UI 线程上调用。`*Async` 的成员会对此做校验，不满足就抛异常。

**解决办法：**用 `Dispatcher.UIThread.InvokeAsync` 把调用封送过去：

```csharp
await Dispatcher.UIThread.InvokeAsync(() => Viewer.LoadDocumentAsync(path));
```

## 键盘快捷键被查看器吃掉，没传到我的命令 {#keyboard-shortcuts-reach-the-viewer-instead-of-my-commands}

`EnableKeyboardShortcuts` 开启时，只要查看器持有焦点，复制、粘贴、全选、缩放、书签、撤销、重做、保存、删除以及方向键都归它处理。

**解决办法：**把 `EnableKeyboardShortcuts` 设为 `false`，把这些按键让给宿主；或者把 `IsArrowKeyNudgeEnabled` 设为 `false`，只保留方向键用于翻页。请见[键盘快捷键](/controls/data-display/pdfviewer/navigation-and-search#keyboard-shortcuts)。

## 文档在浏览器中加载不出来 {#the-document-does-not-load-in-the-browser}

在浏览器中，应用必须提供 `pdfium.wasm`。文件缺失、脚本被严格的内容安全策略拦下，或者启用了多线程运行时（`WasmEnableThreads`），都会让 PDFium 起不来。失败情况会通过 `LoadError` 告知。

**解决办法：**把 `pdfium.wasm` 复制到 `wwwroot`，或者把 `PdfViewerBrowserOptions.PdfiumWasmUrl` 指到它实际的服务地址。在严格策略下，还要一并提供桥接脚本并设置 `PdfViewerBrowserOptions.ScriptsBaseUrl`。另外请从 `Stream` 或 `byte[]` 加载文档，而不是从路径加载。请见[浏览器托管](/controls/data-display/pdfviewer/platforms-and-performance#browser-webassembly-hosting)。

## 快速滚动时页面一片空白 {#pages-are-blank-while-scrolling-quickly}

只有视口附近的页面会被解码。滚动得比解码还快时，没跟上的页面就先显示占位内容。

**解决办法：**调高 `PageRenderBuffer`，让视口之前解码更多页面，并把 `PageRetentionBuffer` 保持在不低于它的水平。值越大越吃内存。请见[内存与大文档](/controls/data-display/pdfviewer/platforms-and-performance#memory-and-large-documents)。

## 在查看器中所做的编辑，换个阅读器打开就不一样了 {#edits-made-in-the-viewer-look-different-in-another-reader}

带文字的形状默认保存为 `/Stamp` 批注，因此其他阅读器只能移动它们，改不了内容，而文字得以保留。

**解决办法：**把 `ShapeSubtypeMode` 设为 `Standard`，让每个形状都以其标准子类型写出；或者设为 `Strict`，干脆不让形状带文字。请见[形状与文字](/controls/data-display/pdfviewer/annotations#shapes-and-text)。

## 另请参阅 {#see-also}

- [PdfViewer 控件](/controls/data-display/pdfviewer)
- [Installing Avalonia Pro](/tools/installing-avalonia-pro)
