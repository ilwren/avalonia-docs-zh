---
id: platforms-and-performance
title: 平台与性能
description: Avalonia PdfViewer 控件的包目标平台、WebAssembly 托管方式、大文档的内存占用、裁剪、诊断以及已知限制。
doc-type: how-to
tags:
  - avalonia pro
  - avalonia enterprise
---

## 包的目标平台 {#package-targets}

该包提供 `net10.0`（Windows、macOS 和 Linux）、`net10.0-ios`、`net10.0-android` 和 `net10.0-browser` 四套资产。每一套只依赖各自平台所需的 PDFium 包，NuGet 会为每个应用头项目挑选正确的那一套。

## 浏览器（WebAssembly）托管 {#browser-webassembly-hosting}

在浏览器中，PDFium 以独立的 WebAssembly 模块运行，应用必须把它作为静态文件 `pdfium.wasm` 提供出去。`bblanchon.PDFium.WebAssembly` 包里就带着这个文件。

1. 在浏览器头项目中以 `ExcludeAssets="native"` 的方式引用该包，这样 WebAssembly SDK 就不会试图去链接它。

```xml
<PackageReference Include="bblanchon.PDFium.WebAssembly" Version="155.0.8044" ExcludeAssets="native" />
```

2. 把包里的 `runtimes/browser-wasm/native/pdfium.wasm` 复制到 `wwwroot`，例如在浏览器头项目中写一个 MSBuild 目标来完成。

```xml
<Target Name="CopyPdfiumWasm" AfterTargets="Build">
  <Copy SourceFiles="$(NuGetPackageRoot)bblanchon.pdfium.webassembly/155.0.8044/runtimes/browser-wasm/native/pdfium.wasm"
        DestinationFolder="wwwroot" />
</Target>
```

控件默认按相对于页面的路径去取 `./pdfium.wasm`。如果该文件托管在别处（比如 CDN），请在加载第一份文档之前设好这个 URL。`PdfViewerBrowserOptions` 是静态类，在应用启动时设置是安全的。

```csharp
#if BROWSER
PdfViewerBrowserOptions.PdfiumWasmUrl = "https://cdn.example.com/pdf/pdfium.wasm";
#endif
```

### Content Security Policy

控件的 JavaScript 默认内嵌，并通过 `data:` URL 求值；若内容安全策略（CSP）不含 `data:` 和 `'unsafe-eval'`，这种方式会被拦截。遇到这类宿主，请把包中 `browser/` 文件夹下的 `pdfium-bridge.js` 和 `pdfium.wrapped.js` 一并放到 `pdfium.wasm` 旁边提供出去，并让控件指向它们。

```csharp
#if BROWSER
PdfViewerBrowserOptions.ScriptsBaseUrl = "./";
#endif
```

这样一来，`script-src 'self' 'wasm-unsafe-eval'` 就够用了。.NET 自身则还需要 `wasm-unsafe-eval`。

### 浏览器端的限制 {#browser-limitations}

- 不支持多线程运行时（`WasmEnableThreads`）。
- 启动失败（比如脚本被拦截或缺少 wasm 文件）会通过 `LoadError` 上报，并在下次加载时重试。
- 表单字段会被绘制出来，但无法编辑。
- 没有文件系统。请从 `Stream` 或 `byte[]` 加载文档，必要时自行把文件下载下来。
- 打印、分享以及内置的保存和打开对话框均不可用。请处理 `PrintRequested`、`ShareRequested`、`OpenRequested` 和 `SaveAsRequested` 来自行提供这些能力。

## 内存与大文档 {#memory-and-large-documents}

在连续视图模式下，只有视口附近的页面会被解码，滚出范围的页面则会释放，因此内存不会随文档长度一路增长。缩略图条也是同样的机制。

有两个属性可以在滚动流畅度与内存占用之间作权衡。

| 属性 | 默认值 | 说明 |
|---|---|---|
| `PageRenderBuffer` | `2` | 视口两侧各预先解码多少页。调大它可以减少快速滚动时的空白占位，调小则省内存。收束到 0 至 10。 |
| `PageRetentionBuffer` | `4` | 两侧各保留多少页解码结果不被释放。把它设得比 `PageRenderBuffer` 大，可以避免来回小幅滚动时反复重绘。收束到 0 至 20。 |

```xml
<pdf:PdfViewer Source="/path/to/large.pdf"
               PageRenderBuffer="3"
               PageRetentionBuffer="8" />
```

单页位图的边长不会超过 8192 像素，总量不会超过 3000 万像素。缩放超出这一上限后，页面会以较低分辨率解码再放大。`MaxRenderScale` 的上限为 4。

## 裁剪与 AOT {#trimming-and-aot}

该库支持裁剪，也兼容 AOT。裁剪发布或 AOT 发布的应用不会因它产生任何警告。

## Diagnostics

查看器通过 Avalonia 的日志系统以 `PdfViewer` 为区域输出日志，Release 构建中同样如此。

```csharp
AppBuilder.Configure<App>()
    .UsePlatformDetect()
    .LogToTrace(LogEventLevel.Warning, "PdfViewer");
```

凡是需要用户处理的问题，都会同时体现在可绑定的 `ErrorMessage` 属性上；批注类失败还会通过 `AnnotationError` 事件上报。参见[错误处理](annotations.md#errors)。

## 已知限制 {#known-limitations}

- 页面内容不会以文本形式暴露给辅助技术。参见[无障碍](theming-and-localization.md#accessibility)。
- Linux 和浏览器上没有内置的打印与分享。浏览器中还不支持表单填写和内置文件对话框。
- 文本选区不能跨页。
- 涂黑删除会移除文本、图像以及被完全覆盖的矢量内容，但不会移除由部分覆盖的表单 XObject 所绘制的内容。

## 另请参阅 {#see-also}

- [PdfViewer 控件](index.md)
- [加载与保存](loading-and-saving.md)
- [打印与分享](printing-and-sharing.md)
- [疑难排查](/troubleshooting/controls/pdfviewer)
