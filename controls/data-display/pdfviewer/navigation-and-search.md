---
id: navigation-and-search
title: 导航、缩放与搜索
description: 用 Avalonia PdfViewer 控件翻页、缩放、跟进链接和书签、搜索文本，并提取页面内容或图像。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

:::note
导航相关的成员使用从 1 开始的页码，与 `CurrentPage` 以及工具栏上的页码框一致。批注、文本提取和渲染相关的成员则使用从 0 开始的页面索引。
:::

## 页面导航 {#page-navigation}

| 成员 | 说明 |
|---|---|
| `CurrentPage` | 当前页码，从 1 开始。支持双向绑定。 |
| `GoToPage(int pageNumber)` | 跳转到指定页。 |
| `NextPage()` / `PreviousPage()` | 向前或向后翻页。 |
| `GetPageLabel(int pageNumber)` | 文档中为该页定义的标签，比如 `iv` 或 `A-2`；没有标签时为 `null`。缩略图和页码框在有标签时优先显示标签。 |
| `PageChanged` | 当前页变化时触发。参数包含 `OldPage` 和 `NewPage`。 |

```csharp
Viewer.PageChanged += (_, e) =>
    StatusText = $"Page {e.NewPage} of {Viewer.PageCount}";
```

## 视图模式 {#view-modes}

`ViewMode` 决定页面如何排布。

| 值 | 说明 |
|---|---|
| `SinglePage` | 一次显示一页。方向键和滑动手势用于翻页。 |
| `Continuous` | 各页排成一列纵向滚动。只有靠近视口的页面才会被解码。 |
| `TwoPages` | 两页并排显示。 |
| `TwoPagesContinuous` | 两页并排，并排成一列纵向滚动。 |

## Zoom

| 成员 | 说明 |
|---|---|
| `ZoomLevel` | 缩放倍数。`1.0` 表示 100%。支持双向绑定。 |
| `ZoomMode` | `Manual`, `FitWidth`, `FitPage`, `FitHeight` or `ActualSize`. |
| `MinZoom` / `MaxZoom` | 缩放的上下限。 |
| `ZoomStep` | `ZoomIn` 和 `ZoomOut` 每次调整的步长。取 `0` 时采用内置的自适应步长。 |
| `ZoomIn()` / `ZoomOut()` / `ResetZoom()` | 调整缩放。 |
| `FitWidth()` / `FitPage()` / `FitHeight()` | 套用某种适配模式。 |
| `ZoomChanged` | 缩放级别变化时触发。 |

触摸屏和触控板上的捏合缩放、单页与双页模式下的滑动翻页，以及长按弹出上下文菜单，都由控件自行处理。

## 大纲与链接 {#outline-and-links}

`GetOutline()` 以 `PdfBookmark` 项组成的树返回文档目录，每一项都带有 `Title`、可选的 `PageIndex`、`Children` 以及可选的 `Destination`。当 `IsTableOfContentsEnabled` 为 `true` 时，侧栏会在**目录**选项卡中显示它。文档是否带目录可由 `HasOutline` 判断。

| 成员 | 说明 |
|---|---|
| `GetOutline()` | 文档的目录。 |
| `GoToBookmark(PdfBookmark)` | 跳转到某个大纲条目：若它带有目标位置（页码加位置），则跳到该位置，否则跳到它所在的页。 |
| `NavigateTo(PdfLinkDestination)` | 跳转到某个页面目标；若目标指定了位置和缩放，也一并应用。对于 URI 目标和文件目标，返回 `false`。 |

### Links

页面中的链接可以点击。点击时先触发 `LinkClicked`，目标放在 `Destination` 中，类型为 `PdfLinkDestination.PageDestination`、`UriDestination` 或 `FileDestination`。除非有处理程序把 `Handled` 设为 `true`，否则：

- 页面目标会在文档内部跳转。
- `http`、`https` 或 `mailto` 这类 URI 会在用户确认后，用系统浏览器或邮件客户端打开。
- 文件目标和其他 URI 方案只会触发事件，查看器从不代为打开。

```csharp
Viewer.LinkClicked += (_, e) =>
{
    if (e.Destination is PdfLinkDestination.UriDestination uri
        && uri.Uri.StartsWith("myapp:"))
    {
        e.Handled = true;
        HandleDeepLink(uri.Uri);
    }
};
```

## 用户书签 {#user-bookmarks}

用户书签与文档大纲是两码事。它们按 macOS 预览（Preview）所用的格式存在 PDF 文件内部，因此两个应用看到的是同一批书签。当 `IsBookmarksEnabled` 为 `true` 时，侧栏会在**书签**选项卡中列出它们；`ShowBookmarkIndicators` 则会在加了书签的页面和缩略图上画一条标带。

| 成员 | 说明 |
|---|---|
| `IsPageBookmarked(int pageNumber)` | 该页是否已加书签。 |
| `AddBookmark(int pageNumber)` / `RemoveBookmark(int pageNumber)` / `ToggleBookmark(int pageNumber)` | 改变某一页的书签状态。返回是否确实发生了变化。 |
| `ToggleBookmarkCurrentPage()` | 切换当前页的书签状态。 |
| `HasBookmarks` | 文档是否带有用户书签。 |
| `BookmarksChanged` | 任何变化之后触发。 |

书签的改动会在下一次保存时写入，且不纳入撤销历史。

## Search

| 成员 | 说明 |
|---|---|
| `SearchAsync(string query, SearchOptions? options = null)` | 在文档中搜索。返回所有命中项，并在页面上高亮它们。 |
| `SearchAsync(string query, SearchOptions? options, CancellationToken)` | 同上，但支持取消。搜索过程中，命中项会逐页浮现。 |
| `FindNext()` / `FindPrevious()` | 切换当前命中项。 |
| `ClearSearch()` | 清除所有命中项及其高亮。 |
| `SearchResults` | 上一次搜索的命中项。 |
| `SearchResultCount` | 命中项的数量。 |
| `CurrentSearchResultIndex` | 当前命中项的索引。 |
| `SearchCompleted` | 搜索完成时触发。 |

`SearchOptions` 带有 `MatchCase`、`MatchWholeWord`、`StartPage`（从 0 开始的页面索引）和 `MaxResults`（`0` 表示不限）。每个 `PdfSearchResult` 都带有 `PageIndex`、该命中项的 `CharIndex` 和 `CharCount`，以及它在页面上的 `Bounds`。

工具栏的搜索框绑定到 `SearchQuery`、`SearchMatchCase` 和 `SearchMatchWholeWord`。

```csharp
var results = await Viewer.SearchAsync("invoice", new SearchOptions
{
    MatchCase = false,
    MatchWholeWord = true,
});

Console.WriteLine($"{results.Count} matches");
Viewer.FindNext();
```

## 文本选择 {#text-selection}

选区不能跨页。`AllowTextSelection` 可以彻底关闭文本选择。

| 成员 | 说明 |
|---|---|
| `SelectAll()` | 选中当前页的全部文本。 |
| `ClearSelection()` | 清除选区。 |
| `GetSelectedText()` | 返回选中的文本。 |
| `CopySelectionToClipboard()` | 把选区复制到剪贴板。 |
| `HasSelection` / `SelectedText` | 当前的选区状态。 |

选中文本后会弹出上下文菜单，其中有**复制**和各种文本标记工具。参见[批注](annotations.md#markup-from-a-selection)。

## 文本提取与页面图像 {#text-extraction-and-page-images}

下列成员使用从 0 开始的页面索引。

| 成员 | 说明 |
|---|---|
| `GetPageTextAsync(int pageIndex, CancellationToken)` | 提取某一页的纯文本。未加载文档或索引越界时返回空字符串。 |
| `GetTextAsync(CancellationToken)` | 提取整份文档的文本，每页一个字符串。 |
| `RenderPageToImageAsync(int pageIndex, double scale = 1.0, CancellationToken)` | 按给定缩放比例把某一页渲染成 `Bitmap`，其中 `1.0` 表示 100%。未加载文档或索引越界时返回 `null`。用完之后请释放该位图。 |

```csharp
// A thumbnail of the first page for a file list
using var thumbnail = await Viewer.RenderPageToImageAsync(0, scale: 0.25);
```

## 键盘快捷键 {#keyboard-shortcuts}

<kbd>Cmd</kbd> is <kbd>⌘</kbd> 用于 macOS 和 iOS， <kbd>Ctrl</kbd> 则用于其他所有平台。修饰键需要精确匹配，因此查看器未列出的组合键（比如 <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>A</kbd>）会直接交给你自己的处理程序。

### 文档类快捷键 {#document-shortcuts}

这些快捷键需要 `EnableKeyboardShortcuts`。把它设为 `false`，这些按键就会留给你自己的命令。表单输入和 <kbd>Esc</kbd> 不受影响。

| 快捷键 | 动作 | 注释支持情况 |
|---|---|---|
| <kbd>Cmd</kbd>+<kbd>C</kbd> | 复制选中的批注；没有选中批注时则复制选中的文本 | 仅在有内容被选中时才会处理 |
| <kbd>Cmd</kbd>+<kbd>V</kbd> | 把已复制的批注粘贴到当前页 | 需要先复制过批注，且 `CanEditAnnotations` 为真 |
| <kbd>Cmd</kbd>+<kbd>A</kbd> | 选中当前页的全部文本 | |
| <kbd>Cmd</kbd>+<kbd>+</kbd> | 放大 | <kbd>=</kbd> 以及小键盘上的 <kbd>+</kbd> 同样有效 |
| <kbd>Cmd</kbd>+<kbd>-</kbd> | 缩小 | <kbd>_</kbd> 以及小键盘上的 <kbd>-</kbd> 同样有效 |
| <kbd>Cmd</kbd>+<kbd>0</kbd> | 实际大小（100%） | |
| <kbd>Cmd</kbd>+<kbd>1</kbd> | 适合整页 | |
| <kbd>Cmd</kbd>+<kbd>2</kbd> | 适合宽度 | |
| <kbd>Cmd</kbd>+<kbd>D</kbd> | 为当前页加书签 | 只能添加。移除请到**书签**选项卡或调用 API |
| <kbd>Cmd</kbd>+<kbd>Z</kbd> | Undo | |
| <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>Z</kbd>, <kbd>Ctrl</kbd>+<kbd>Y</kbd> | Redo | |
| <kbd>Cmd</kbd>+<kbd>S</kbd> | 保存到 `Source` | 仅在文档可保存时生效，否则交给宿主处理 |
| <kbd>Delete</kbd>, <kbd>Backspace</kbd> | 删除选中的批注 | Needs `CanEditAnnotations`. Undoable |
| 方向键 | 把选中的批注微移 1 像素 | 按住 <kbd>Shift</kbd> 则微移 10 像素。可用 `IsArrowKeyNudgeEnabled` 关闭这一行为 |
| <kbd>↑</kbd> / <kbd>↓</kbd> | 在连续视图模式下滚动 | |
| <kbd>←</kbd> / <kbd>↑</kbd>, <kbd>→</kbd> / <kbd>↓</kbd> | 在单页和双页模式下切换上一页/下一页 | |

### 始终生效 {#always-on}

下列快捷键不受 `EnableKeyboardShortcuts` 影响。

| 快捷键 | 动作 |
|---|---|
| <kbd>Esc</kbd> | 关闭上下文菜单、清除批注或文本选区、取消当前激活的工具。只有确实发生了变化时，才会标记为已处理 |
| 用 <kbd>Tab</kbd> / <kbd>Shift</kbd>+<kbd>Tab</kbd> 聚焦到查看器 | 进入当前页的第一个 / 最后一个表单字段 |
| 在表单字段中按 <kbd>Tab</kbd> / <kbd>Shift</kbd>+<kbd>Tab</kbd> | 切到下一个 / 上一个字段。没有下一个字段时则离开查看器 |
| 在表单字段中按 <kbd>Esc</kbd> | 退出表单焦点 |
| 在表单字段中按 <kbd>Cmd</kbd>+<kbd>A</kbd>、<kbd>Cmd</kbd>+<kbd>C</kbd>、<kbd>Cmd</kbd>+<kbd>X</kbd>、<kbd>Cmd</kbd>+<kbd>V</kbd> | 对该字段的文本执行全选、复制、剪切和粘贴 |
| 在表单字段中按 <kbd>Cmd</kbd>+<kbd>Z</kbd>、<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>Z</kbd> | 在该字段内部撤销和重做 |

### 在查看器自身的界面内 {#inside-the-viewers-own-chrome}

| 所在位置 | 按键 |
|---|---|
| 就地文本编辑器（文本框或形状上的文字） | <kbd>Esc</kbd> 取消，<kbd>Ctrl</kbd>+<kbd>Enter</kbd> 提交 |
| 搜索框 | <kbd>Enter</kbd> 跳到下一个结果，<kbd>Esc</kbd> 清空并关闭 |
| 页码框 | <kbd>Enter</kbd> 提交，<kbd>Esc</kbd> 还原 |
| 链接 URL 对话框，以及密码、跳转页码和自定义缩放这几个浮层 | <kbd>Enter</kbd> 确认，<kbd>Esc</kbd> 取消 |
| 十六进制颜色输入框 | <kbd>Enter</kbd> 应用 |

`FocusViewer()` 会把键盘焦点移到查看器上，这些快捷键才会生效。

## 另请参阅 {#see-also}

- [PdfViewer 控件](index.md)
- [Annotations](annotations.md)
- [平台与性能](platforms-and-performance.md)
