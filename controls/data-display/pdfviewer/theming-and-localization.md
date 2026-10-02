---
id: theming-and-localization
title: 主题、本地化与无障碍
description: 用主题画刷、伪类和自定义模板为 Avalonia PdfViewer 定制外观，翻译它的文案，并了解它的无障碍支持情况。
doc-type: how-to
tags:
  - avalonia pro
  - avalonia enterprise
---

## Themes

该包提供两套主题，每套都有浅色和深色配色。请在 `App.axaml` 中引入其中一套。

| 主题 | 说明 |
|---|---|
| `Default.axaml` | 中性、圆润、无边框的外观，自带一套配色，不依赖宿主的 Avalonia 主题。 |
| `Fluent.axaml` | 把同一批键映射到 `SystemAccentColor`、`ControlCornerRadius` 等 `FluentTheme` 资源上，于是查看器会跟随宿主的强调色、主题变体，以及应用覆盖过的任何 Fluent 资源。 |

```xml
<Application.Styles>
    <FluentTheme />
    <StyleInclude Source="avares://Avalonia.Controls.PdfViewer/Themes/Fluent.axaml" />
</Application.Styles>
```

两套主题使用同一份控件模板，而该模板只引用 `Pdf*` 资源。因此只要引入了其中一个主题文件，查看器在 `SimpleTheme` 或自定义应用主题下都能完整渲染。

## 覆盖主题画刷 {#override-theme-brushes}

在 `App.axaml` 中覆盖 `Pdf*` 资源，即可让外观贴合你的应用。这些键按主题变体解析，因此覆盖时可以用一个 `ResourceDictionary.ThemeDictionaries` 块分别给出浅色和深色取值。

```xml
<Application.Resources>
    <SolidColorBrush x:Key="PdfBackground" Color="#252526" />
    <SolidColorBrush x:Key="PdfErrorForeground" Color="#F48771" />
    <SolidColorBrush x:Key="PdfToolbarBackground" Color="#2D2D30" />
    <SolidColorBrush x:Key="PdfToolbarIconColor" Color="#CCCCCC" />
    <SolidColorBrush x:Key="PdfToolbarTextColor" Color="#E0E0E0" />
    <SolidColorBrush x:Key="PdfToolbarHoverBackground" Color="#3E3E42" />
    <SolidColorBrush x:Key="PdfToolbarBorderColor" Color="#555555" />
    <SolidColorBrush x:Key="PdfToolbarSeparatorColor" Color="#444444" />
    <SolidColorBrush x:Key="PdfMenuIconColor" Color="#AAAAAA" />

    <!-- Chrome the viewer builds in code -->
    <SolidColorBrush x:Key="PdfThumbnailBackground" Color="#2E2E2E" />
    <SolidColorBrush x:Key="PdfThumbnailSelectedBorder" Color="#4A9EDF" />
    <SolidColorBrush x:Key="PdfThumbnailLabelColor" Color="#B0B0B0" />
    <SolidColorBrush x:Key="PdfPagePlaceholderBackground" Color="#2A2A2A" />
    <SolidColorBrush x:Key="PdfDestructiveColor" Color="#FF6B6B" />

    <!-- Highlights and edit adorners drawn on the page -->
    <SolidColorBrush x:Key="PdfTextSelectionHighlight" Color="#5033A0FF" />
    <SolidColorBrush x:Key="PdfSearchHighlight" Color="#66FFEB3B" />
    <SolidColorBrush x:Key="PdfSearchHighlightActive" Color="#99FF9800" />
    <SolidColorBrush x:Key="PdfAdornerAccent" Color="#33A0FF" />
    <SolidColorBrush x:Key="PdfAdornerHandleBackground" Color="White" />
    <SolidColorBrush x:Key="PdfLinkHoverColor" Color="#DCA0A0A0" />
</Application.Resources>
```

在控件上设置 `SidebarSelectionBrush`，可为单个查看器覆盖 `PdfThumbnailSelectedBorder`。

## Pseudo-classes

查看器把自己的各种状态暴露为伪类，供样式选择器使用。

| 伪类 | 状态 |
|---|---|
| `:has-document` | 已打开文档。 |
| `:loading` | 文档正在加载。 |
| `:error` | `ErrorMessage` 已设置。 |
| `:read-only` | `IsReadOnly` is `true`. |
| `:annotating` | 有工具处于激活状态。 |
| `:sidebar-open` | 侧栏已展开。 |
| `:mobile` | 正在使用紧凑的移动端布局。 |
| `:narrow` | 控件宽度不足 640 个设备无关像素，比如竖屏的手机。此时搜索框会收成一个图标。 |
| `:search-open` | 搜索框已展开。 |
| `:text-selected` | 有文本被选中。 |
| `:shape-selected` | 有批注被选中。 |
| `:form-field-focused` | 某个表单字段获得了焦点。 |
| `:editing-text` | 就地文本编辑器已打开。 |

```xml
<Style Selector="pdf|PdfViewer:read-only">
    <Setter Property="Opacity" Value="0.9" />
</Style>
```

## 自定义模板 {#custom-templates}

各个模板部件通过 `PdfViewer` 上的 `[TemplatePart]` 特性声明。其中只有 `PART_ScrollViewer` 和 `PART_PagesContainer` 是必需的，其余部件都可选；自定义模板若省略了某个部件，对应功能即不存在。

要做自己的主题，可以把包里的 `Default.axaml` 复制出来，改掉其中的取值，再以同样的方式引入该模板。

## Localization

查看器显示的每一处文字都来自 `PdfViewerStrings`：工具提示、菜单项、对话框文案、侧栏标签、占位文字和错误信息。把一个填好译文的实例赋给 `Strings` 即可。没填的属性保持英文默认值。

```csharp
Viewer.Strings = new PdfViewerStrings
{
    Highlight = "Surligner",
    SearchPlaceholder = "Rechercher...",
    PageCountFormat = "sur {0}",
    Loading = "Chargement...",
};
```

以 `Format` 结尾的属性是 `string.Format` 模式串，必须保留其中的 `{0}` 占位符，比如 `PageCountFormat`（`"of {0}"`）和 `PageLabelFormat`（`"Page {0}"`）。

请在加载文档之前设好 `Strings`。改动后工具栏会立即刷新，但上下文菜单、**图章**下拉菜单和缩略图标签要等到下次构建时才会用上新文案。缩放百分比按当前区域设置格式化。

## 无障碍 {#accessibility}

- 工具栏和侧栏按钮会把自己的工具提示暴露为 `AutomationProperties.Name`，于是屏幕阅读器读出的是「高亮」「缩放」，而不是控件类型。
- 该控件以文档区域的身份对外报告，名称取自文档标题（或文件名）和当前页码。要覆盖这一点，请在 `PdfViewer` 上设置 `AutomationProperties.Name`。
- 隐藏的浮层（密码、跳转页码、自定义缩放）不在 Tab 顺序之内。
- 表单字段可以用 <kbd>Tab</kbd> 访问，并会显示焦点框。参见[表单](annotations.md#forms)。

页面内容是以位图渲染的，因此 PDF 中的文字不会以元素的形式暴露给辅助技术。如果你需要这些文字，可以用 `GetPageTextAsync` 读出来，再放进你自己的无障碍界面中呈现。

## 另请参阅 {#see-also}

- [PdfViewer 控件](index.md)
- [导航、缩放与搜索](navigation-and-search.md)
- [控件主题](/docs/styling/control-themes)
