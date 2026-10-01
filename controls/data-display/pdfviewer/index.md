---
id: index
title: PdfViewer 控件
description: 用 Avalonia.Controls.PdfViewer 包中的 PdfViewer 控件，在 Avalonia 中显示、搜索、批注、填写和打印 PDF 文档。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

`PdfViewer` 用于在 Avalonia 应用中显示 PDF 文档。它开箱即是一个完整的阅读器：只要设好文档来源，你就拥有了工具栏和侧栏、页面缩略图与文档大纲、翻页导航、缩放与视图模式、文本选择与搜索、带撤销重做的完整批注工具集、表单填写、书签，以及原生的打印与分享。这些功能都可以隐藏或禁用，而且除了内置界面之外，统统也能用代码调用。同一个控件、同一个包，可在 Windows、macOS、Linux、iOS、Android 和 WebAssembly 上运行。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 适用场景 {#when-to-use}

用 `PdfViewer` 在你的应用里展示 PDF 文档。每一件工具、每一项菜单都可以隐藏或禁用，因此它既能当纯只读阅读器，也能当完整的批注编辑器。

若要在查看器之外把某一页渲染成图片——比如在文件列表里做缩略图——请使用 [`RenderPageToImageAsync`](navigation-and-search.md#text-extraction-and-page-images)。

## 环境要求 {#requirements}

- .NET 10 或更高版本。
- Avalonia 12.0 或更高版本。
- 一份涵盖 PDF Viewer 的 Avalonia Pro 或 Enterprise 许可证。
- Windows、macOS、Linux（x64 与 arm64）、iOS 15 及以上、Android API 23 及以上，或 WebAssembly。

## Dependencies

该包使用 [PDFium](https://pdfium.googlesource.com/pdfium/) 渲染，后者通过 `bblanchon.PDFium.*` 系列 NuGet 包以原生库的形式随包分发。每个目标框架只依赖自己平台所需的包，因此应用头项目不会还原任何用不上的东西。

| 目标平台 | 所需包 |
|---|---|
| `net10.0` (Windows, macOS, Linux) | `Avalonia`, `AvaloniaUI.Licensing`, `bblanchon.PDFium.Win32`, `bblanchon.PDFium.macOS`, `bblanchon.PDFium.Linux` |
| `net10.0-ios` | `Avalonia`, `AvaloniaUI.Licensing`, `bblanchon.PDFium.iOS` |
| `net10.0-android` | `Avalonia`, `Avalonia.Android`, `AvaloniaUI.Licensing`, `bblanchon.PDFium.Android` |
| `net10.0-browser` | `Avalonia`, `AvaloniaUI.Licensing`, `bblanchon.PDFium.WebAssembly` |

PDFium 以 [BSD 3-Clause 许可证](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/LICENSE) 分发。请在你应用的第三方声明中附上它的许可声明。

## 快速上手 {#getting-started}

1. 运行 `dotnet add package` 安装 `Avalonia.Controls.PdfViewer` NuGet 包。请把它加到存放视图的项目中，并加到每一个应用头项目（桌面、iOS、Android、浏览器），这样各个头项目才能还原各自平台所需的 PDFium 二进制文件。

```bash
dotnet add package Avalonia.Controls.PdfViewer
```

2. 在每个应用头项目中引用 `AvaloniaUI.Licensing` 包，并把你的 Avalonia 许可证密钥写进可执行项目文件（`.csproj`）。许可证密钥可在 [Avalonia 门户](https://portal.avaloniaui.net) 获取。若密钥缺失或不涵盖 PDF Viewer，控件会在首次使用时抛出 `AvaloniaLicensingException`。

```xml
<ItemGroup>
  <PackageReference Include="AvaloniaUI.Licensing" Version="3.1.2" />
</ItemGroup>
<ItemGroup>
  <AvaloniaUILicenseKey Include="YOUR_LICENSE_KEY" />
</ItemGroup>
```

:::tip
对于多项目解决方案，可以把许可证密钥放进[环境变量](https://learn.microsoft.com/en-us/visualstudio/msbuild/how-to-use-environment-variables-in-a-build)或[共享 props 文件](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory?view=vs-2022#directorybuildprops-example)，免得到处重复。
:::

3. 在 `App.axaml` 文件中通过 `StyleInclude` 引用两套主题中的一套。没有主题，控件什么也画不出来。`Default.axaml` 自带一套配色，在任何宿主主题下都适用；`Fluent.axaml` 则跟随宿主的 `FluentTheme` 强调色和主题变体。

```xml
<Application.Styles>
    <FluentTheme />
    <StyleInclude Source="avares://Avalonia.Controls.PdfViewer/Themes/Default.axaml" />
</Application.Styles>
```

关于安装 Avalonia Pro 控件的更多内容，请参阅[安装 Avalonia Pro](/tools/installing-avalonia-pro)。

## 基本用法 {#basic-usage}

该控件位于 `Avalonia.Controls` 命名空间下。`Avalonia.Controls.PdfViewer` 既是包名也是程序集名，因此在 XAML 中请用 `xmlns` 前缀映射该命名空间。

<Tabs>
<TabItem value="xaml" label="XAML">

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:pdf="using:Avalonia.Controls"
        Width="1000" Height="700">

    <pdf:PdfViewer x:Name="Viewer"
                   Source="/path/to/document.pdf"
                   ViewMode="Continuous"
                   SidebarMode="Thumbnails" />

</Window>
```

</TabItem>

<TabItem value="csharp" label="Code-behind">

```csharp
using Avalonia.Controls;          // PdfViewer, its enums and event args
using Avalonia.Controls.Pdf.Core; // PdfAnnotationColor, PdfBookmark, PdfSearchResult, SearchOptions

// Load from a file path, a stream, or a password-protected file
await Viewer.LoadDocumentAsync("/path/to/document.pdf");
await Viewer.LoadDocumentAsync(fileStream);
await Viewer.LoadDocumentAsync("/path/to/encrypted.pdf", password: "secret");

// Navigate and zoom
Viewer.GoToPage(5);
Viewer.NextPage();
Viewer.FitWidth();

// Search
var results = await Viewer.SearchAsync("keyword", new SearchOptions { MatchCase = true });
Viewer.FindNext();

// Read the selection
string? text = Viewer.GetSelectedText();
await Viewer.CopySelectionToClipboard();

// Annotate the current selection, then save with the edits
await Viewer.HighlightSelectionAsync();
await Viewer.UnderlineSelectionAsync(new PdfAnnotationColor(0, 0, 255, 255));
await Viewer.SaveDocumentAsync("/path/to/output.pdf");
```

</TabItem>
</Tabs>

设置 `Source` 即加载文档。它可以在查看器挂到视觉树之前就设好，比如在视图模型的构造函数里。

## Namespaces

| 命名空间 | 本章内容 |
|---|---|
| `Avalonia.Controls` | `PdfViewer` 及其枚举、事件参数和 `PdfViewerStrings`。 |
| `Avalonia.Controls.Pdf.Core` | 数据类型：`PdfAnnotationColor`、`PdfBookmark`、`PdfSearchResult`、`PdfMetadata`、`PdfPermissions`、`SearchOptions`、`PdfLinkDestination`。 |
| `Avalonia.Controls.Pdf.Services` | 打印与分享类型：`PrintOptions`、`IPrintService`、`ShareOptions`、`IShareService`。 |

## 属性 {#properties}

### 文档、视图与缩放 {#document-view-and-zoom}

| 属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `Source` | `string?` | `null` | PDF 文件的路径。设置它即加载文档。 |
| `DocumentSource` | `object?` | `null` | 更灵活的来源：文件路径 `string`、`Stream` 或 `byte[]`。 |
| `Password` | `string?` | `null` | 加密 PDF 的密码。 |
| `CurrentPage` | `int` | `0` | 当前页码。文档打开后从 1 开始计数，未打开时为 `0`。取值会被收束到 1 至 `PageCount` 之间。 |
| `ZoomLevel` | `double` | `1.0` | 缩放级别，从 `MinZoom` 到 `MaxZoom`。`1.0` 表示 100%。 |
| `ZoomMode` | `PdfZoomMode` | `FitPage` | `Manual`, `FitWidth`, `FitPage`, `FitHeight` or `ActualSize`. |
| `MinZoom` | `double` | `0.05` | 缩放下限。 |
| `MaxZoom` | `double` | `5.0` | 缩放上限。 |
| `ZoomStep` | `double` | `0.0` | `ZoomIn` 和 `ZoomOut` 每次调整的步长。取 `0` 时采用内置的自适应步长。 |
| `ViewMode` | `PdfViewMode` | `Continuous` | `SinglePage`, `Continuous`, `TwoPages` or `TwoPagesContinuous`. |
| `PageRenderBuffer` | `int` | `2` | 连续模式下，视口两侧各预先解码多少页。收束到 0 至 10。 |
| `PageRetentionBuffer` | `int` | `4` | 两侧各保留多少页解码结果不被回收。收束到 0 至 20。 |
| `MaxRenderScale` | `double` | `2.0` | 解码页面时每个设备无关像素最多对应多少设备像素。强制收束到 1 至 4。 |
| `VerticalScrollOffset` | `double` | | 当前的垂直滚动偏移量。 |

### 侧栏与工具栏 {#sidebar-and-toolbar}

| 属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `SidebarMode` | `SidebarMode` | `Thumbnails` | `None`, `Thumbnails`, `TableOfContents` or `Bookmarks`. |
| `IsSidebarVisible` | `bool` | `true` | 显示或隐藏侧栏。 |
| `SidebarWidth` | `double` | `210` | 侧栏宽度，单位为设备无关像素。 |
| `SidebarPlacement` | `SidebarPlacement` | `Auto` | `Auto`（移动端布局下为覆盖式，桌面端为挤开式）、`Overlay` 或 `Offset`。 |
| `SidebarSelectionBrush` | `IBrush?` | `null` | 选中的缩略图和大纲条目所用的画刷。取 `null` 时使用主题的 `PdfThumbnailSelectedBorder` 资源。 |
| `IsTableOfContentsEnabled` | `bool` | `true` | 在侧栏中提供大纲选项卡。 |
| `IsBookmarksEnabled` | `bool` | `true` | 在侧栏中提供书签选项卡。 |
| `ShowBookmarkIndicators` | `bool` | `true` | 在加了书签的页面和缩略图上画一条标带。 |
| `IsToolbarVisible` | `bool` | `true` | 显示或隐藏工具栏。 |
| `IsMoreOptionsVisible` | `bool` | `true` | 显示或隐藏工具栏的**更多选项**菜单（打印、分享、视图模式）。 |
| `IsPrintVisible` | `bool` | `true` | 在**更多选项**菜单中提供**打印**。当前环境无法打印时，它无论如何都不会显示。 |
| `IsShareVisible` | `bool` | `true` | 在**更多选项**菜单中提供**分享**。当前环境无法分享时，它无论如何都不会显示。 |
| `IsOpenVisible` | `bool` | `false` | 在**更多选项**菜单顶部提供**打开**。 |
| `IsSaveVisible` | `bool` | `false` | 在**更多选项**菜单中提供**保存**。当 `AllowDocumentSaving` 为 `false` 时隐藏。 |
| `IsSaveAsVisible` | `bool` | `false` | 在**更多选项**菜单中提供**另存为**。 |
| `PrintService` | `IPrintService?` | platform | 打印的具体实现。不设置则使用内置的平台服务，设为 `null` 则禁用打印。 |
| `ShareService` | `IShareService?` | platform | 分享的具体实现，语义与 `PrintService` 相同。 |
| `ToolbarLayoutMode` | `PdfToolbarLayoutMode` | `Auto` | `Auto` 会依据平台和宽度自行挑选布局，`Mobile` 和 `Desktop` 则强制指定其一。 |
| `IsMobileLayout` | `bool` | | Whether the compact mobile layout is active. Set by the control: `true` on iOS and Android, and on any platform when the control is narrower than 500 DIPs. Use `ToolbarLayoutMode` to force a layout. |

每件批注工具的显示与否，都由各自的属性控制。参见[批注](annotations.md#tool-visibility)。

### 功能开关与权限 {#capabilities-and-permissions}

| 属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `IsReadOnly` | `bool` | `false` | 一个开关即可禁止批注和表单编辑。保存则另由 `AllowDocumentSaving` 把关。 |
| `AllowTextSelection` | `bool` | `true` | 启用文本选择与复制。 |
| `AllowAnnotationEditing` | `bool` | `true` | 启用批注的创建与编辑。 |
| `AllowFormEditing` | `bool` | `true` | 启用交互式表单字段的编辑。 |
| `AllowDocumentSaving` | `bool` | `true` | 启用保存。它同时把关 `SaveCommand` 和 `SaveAsync`。 |
| `RespectDocumentPermissions` | `bool` | `true` | 遵从文档自身的权限标志。文档禁止时，批注编辑、表单填写、文本选择和打印会相应地被逐项限制。用所有者密码打开的文档不受任何限制。 |
| `AutoSave` | `bool` | `false` | 每次编辑后都写回 `Source`。需要 `AllowDocumentSaving`。 |
| `EnableKeyboardShortcuts` | `bool` | `true` | 处理查看器内置的[键盘快捷键](navigation-and-search.md#keyboard-shortcuts)。设为 `false` 可让这些按键落到宿主自己的命令上。 |
| `IsArrowKeyNudgeEnabled` | `bool` | `true` | 选中某条批注时，方向键改为移动该批注，而不再用于翻页导航。 |
| `SearchQuery` | `string?` | `null` | 工具栏搜索框中的文字。 |
| `SearchMatchCase` | `bool` | `false` | 工具栏搜索框的「区分大小写」选项。 |
| `SearchMatchWholeWord` | `bool` | `false` | 工具栏搜索框的「全词匹配」选项。 |
| `Strings` | `PdfViewerStrings` | `PdfViewerStrings.Default` | 所有面向用户的文案。参见[本地化](theming-and-localization.md#localization)。 |

### State

下列属性为只读且可绑定。

| 属性 | 类型 | 说明 |
|---|---|---|
| `PageCount` | `int` | 已加载文档的页数。 |
| `HasDocument` | `bool` | 当前是否打开着文档。 |
| `IsLoading` | `bool` | 文档加载过程中为 `true`。 |
| `IsDirty` | `bool` | 文档有尚未写入的改动。保存成功或加载另一份文档后，该标志会被清除。 |
| `IsSidebarOpen` | `bool` | 侧栏展开时为 `true`。 |
| `HasOutline` | `bool` | 文档带有目录。 |
| `HasBookmarks` | `bool` | 文档带有用户书签。 |
| `HasSelection` | `bool` | 当前有文本处于选中状态。 |
| `SelectedText` | `string?` | 当前的文本选区。 |
| `SearchResults` | `IReadOnlyList<PdfSearchResult>?` | 上一次搜索的结果。 |
| `SearchResultCount` | `int` | 搜索命中的数量。 |
| `CurrentSearchResultIndex` | `int` | 当前高亮命中项的索引。 |
| `ErrorMessage` | `string?` | 最近一条错误信息。文档已打开时，它以可关闭的横幅显示在文档之上；加载失败时，则作为画布的状态显示。用 `ClearError()` 清除它。 |
| `Metadata` | `PdfMetadata?` | Document metadata such as title and author. |
| `Permissions` | `PdfPermissions?` | Document permission flags. |
| `CanEditAnnotations` | `bool` | Annotations can be created and edited right now. |
| `CanPrint` | `bool` | A document is open and a print service or handler exists. |
| `CanShare` | `bool` | A document is open and a share service or handler exists. |
| `CanUndo` | `bool` | The undo history has an entry to apply. |
| `CanRedo` | `bool` | The redo history has an entry to apply. |

## Commands

All commands are `ICommand` and update `CanExecute` as document and selection state changes. Bind them from your own buttons if you hide the built-in toolbar.

| Command | 说明 |
|---|---|
| `ZoomInCommand`, `ZoomOutCommand`, `ResetZoomCommand` | Adjust the zoom. |
| `FitWidthCommand`, `FitPageCommand` | Apply a fit mode. |
| `NextPageCommand`, `PreviousPageCommand`, `GoToPageCommand` | Navigate between pages. |
| `SelectAllCommand`, `CopyCommand` | Select all text on the current page, copy the selection. |
| `OpenCommand`, `SaveCommand`, `SaveAsCommand` | File operations. See [Loading and saving](loading-and-saving.md). |
| `PrintCommand`, `ShareCommand` | See [Printing and sharing](printing-and-sharing.md). |
| `SetToolCommand` | Arms an annotation tool. The parameter is a `PdfViewerTool` value or its name. |
| `ToggleBookmarkCommand`, `AddBookmarkCommand`, `RemoveBookmarkCommand` | Change the bookmark on a page. The parameter is a 1-based page number, else the current page. |
| `DismissErrorCommand` | Clears `ErrorMessage`. |

```xml
<Button Content="Fit width" Command="{Binding #Viewer.FitWidthCommand}" />
<Button Content="Highlight" Command="{Binding #Viewer.SetToolCommand}" CommandParameter="Highlight" />
```

## 事件 {#events}

| 事件 | Args | 说明 |
|---|---|---|
| `DocumentLoaded` | `PdfDocumentLoadedEventArgs` | A document finished loading. Args include `PageCount` and `Metadata`. |
| `DocumentClosed` | `EventArgs` | The document was closed. |
| `LoadError` | `PdfLoadErrorEventArgs` | Document loading failed. |
| `AnnotationError` | `PdfAnnotationErrorEventArgs` | An annotation operation failed. Args include `Operation` and the underlying `Exception`. |
| `AnnotationAdded` | `PdfAnnotationEventArgs` | An annotation was added. |
| `PageChanged` | `PdfPageChangedEventArgs` | The current page changed. Args include `OldPage` and `NewPage`, 1-based. |
| `ZoomChanged` | `PdfZoomChangedEventArgs` | The zoom level changed. |
| `PageRendered` | `PdfPageRenderedEventArgs` | A page finished rendering. |
| `SearchCompleted` | `PdfSearchCompletedEventArgs` | A search finished. |
| `LinkClicked` | `PdfLinkClickedEventArgs` | A link was clicked. See [Links](navigation-and-search.md#links). |
| `BookmarksChanged` | `EventArgs` | A user bookmark was added or removed. |
| `UndoRedoStateChanged` | `EventArgs` | `CanUndo` or `CanRedo` changed. |
| `PrintRequested` | `PdfPrintRequestedEventArgs` | Raised before printing. Set `Handled` to print in the app instead of the platform service. |
| `ShareRequested` | `PdfShareRequestedEventArgs` | Raised before sharing. Set `Handled` to share in the app instead of the platform service. |
| `OpenRequested` | `PdfOpenRequestedEventArgs` | Raised before the built-in file picker. Set `Handled` to open in the app. |
| `SaveAsRequested` | `PdfSaveAsRequestedEventArgs` | Raised before the built-in save picker. Set `Handled` to write the PDF in the app. |

## Threading

Every public member of `PdfViewer` must be called on the UI thread. The `*Async` members throw if called from another thread. They do not block the UI while a page is decoding. PDFium itself is single-threaded, so several viewers in one process share one decode pipeline.

## 另请参阅 {#see-also}

- [加载与保存](loading-and-saving.md)
- [Navigation and search](navigation-and-search.md)
- [Annotations](annotations.md)
- [Printing and sharing](printing-and-sharing.md)
- [Theming and localization](theming-and-localization.md)
- [Platforms and performance](platforms-and-performance.md)
- [Installing Avalonia Pro](/tools/installing-avalonia-pro)
- [疑难排查](/troubleshooting/controls/pdfviewer)
