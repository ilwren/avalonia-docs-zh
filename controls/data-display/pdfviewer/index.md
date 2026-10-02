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
| `IsMobileLayout` | `bool` | | 是否正处于紧凑的移动端布局。该值由控件设定：在 iOS、Android 上，以及任何平台上控件宽度不足 500 个设备无关像素时，均为 `true`。要强制指定布局，请使用 `ToolbarLayoutMode`。 |

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
| `Metadata` | `PdfMetadata?` | 文档元数据，比如标题和作者。 |
| `Permissions` | `PdfPermissions?` | 文档的权限标志。 |
| `CanEditAnnotations` | `bool` | 当前是否可以创建和编辑批注。 |
| `CanPrint` | `bool` | 已打开文档，且存在可用的打印服务或处理程序。 |
| `CanShare` | `bool` | 已打开文档，且存在可用的分享服务或处理程序。 |
| `CanUndo` | `bool` | 撤销历史中还有可套用的记录。 |
| `CanRedo` | `bool` | 重做历史中还有可套用的记录。 |

## Commands

所有命令都是 `ICommand`，并会随文档和选区状态的变化更新 `CanExecute`。如果你隐藏了内置工具栏，可以把它们绑定到自己的按钮上。

| 命令 | 说明 |
|---|---|
| `ZoomInCommand`, `ZoomOutCommand`, `ResetZoomCommand` | 调整缩放。 |
| `FitWidthCommand`, `FitPageCommand` | 套用某种适配模式。 |
| `NextPageCommand`, `PreviousPageCommand`, `GoToPageCommand` | 在页面之间导航。 |
| `SelectAllCommand`, `CopyCommand` | 选中当前页的全部文本；复制选区。 |
| `OpenCommand`, `SaveCommand`, `SaveAsCommand` | 文件操作。参见[加载与保存](loading-and-saving.md)。 |
| `PrintCommand`, `ShareCommand` | 参见[打印与分享](printing-and-sharing.md)。 |
| `SetToolCommand` | 激活某件批注工具。参数为 `PdfViewerTool` 的值或其名称。 |
| `ToggleBookmarkCommand`, `AddBookmarkCommand`, `RemoveBookmarkCommand` | 改变某一页的书签状态。参数为从 1 开始的页码，不传则作用于当前页。 |
| `DismissErrorCommand` | Clears `ErrorMessage`. |

```xml
<Button Content="Fit width" Command="{Binding #Viewer.FitWidthCommand}" />
<Button Content="Highlight" Command="{Binding #Viewer.SetToolCommand}" CommandParameter="Highlight" />
```

## 事件 {#events}

| 事件 | 事件参数 | 说明 |
|---|---|---|
| `DocumentLoaded` | `PdfDocumentLoadedEventArgs` | 文档加载完成。参数包含 `PageCount` 和 `Metadata`。 |
| `DocumentClosed` | `EventArgs` | 文档已关闭。 |
| `LoadError` | `PdfLoadErrorEventArgs` | 文档加载失败。 |
| `AnnotationError` | `PdfAnnotationErrorEventArgs` | 某次批注操作失败。参数包含 `Operation` 以及底层的 `Exception`。 |
| `AnnotationAdded` | `PdfAnnotationEventArgs` | 新增了一条批注。 |
| `PageChanged` | `PdfPageChangedEventArgs` | 当前页发生变化。参数包含 `OldPage` 和 `NewPage`，均从 1 开始计数。 |
| `ZoomChanged` | `PdfZoomChangedEventArgs` | 缩放级别发生变化。 |
| `PageRendered` | `PdfPageRenderedEventArgs` | 某一页渲染完成。 |
| `SearchCompleted` | `PdfSearchCompletedEventArgs` | 一次搜索完成。 |
| `LinkClicked` | `PdfLinkClickedEventArgs` | 某个链接被点击。参见[链接](navigation-and-search.md#links)。 |
| `BookmarksChanged` | `EventArgs` | 新增或移除了一个用户书签。 |
| `UndoRedoStateChanged` | `EventArgs` | `CanUndo` 或 `CanRedo` 发生变化。 |
| `PrintRequested` | `PdfPrintRequestedEventArgs` | 打印之前触发。设置 `Handled` 即可在应用内自行打印，而不走平台服务。 |
| `ShareRequested` | `PdfShareRequestedEventArgs` | 分享之前触发。设置 `Handled` 即可在应用内自行分享，而不走平台服务。 |
| `OpenRequested` | `PdfOpenRequestedEventArgs` | 弹出内置文件选择器之前触发。设置 `Handled` 即可在应用内自行打开文件。 |
| `SaveAsRequested` | `PdfSaveAsRequestedEventArgs` | 弹出内置保存选择器之前触发。设置 `Handled` 即可在应用内自行写出 PDF。 |

## Threading

`PdfViewer` 的所有公共成员都必须在 UI 线程上调用。`*Async` 系列成员若从其他线程调用会抛出异常。页面解码期间它们不会阻塞界面。PDFium 本身是单线程的，因此同一进程中的多个查看器共用一条解码流水线。

## 另请参阅 {#see-also}

- [加载与保存](loading-and-saving.md)
- [导航与搜索](navigation-and-search.md)
- [Annotations](annotations.md)
- [打印与分享](printing-and-sharing.md)
- [主题与本地化](theming-and-localization.md)
- [平台与性能](platforms-and-performance.md)
- [Installing Avalonia Pro](/tools/installing-avalonia-pro)
- [疑难排查](/troubleshooting/controls/pdfviewer)
