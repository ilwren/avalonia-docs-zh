---
id: index
title: Markdown 控件
description: 用 Avalonia.Controls.Markdown 控件渲染 Markdown 文本。它构建在共享的 FlowDocument 模型之上，完整支持 DocumentNode 样式、文本选择、流式更新和自定义图片加载。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

`Markdown` 控件用于在 Avalonia 应用中渲染 Markdown 格式的文本。它与 [RichTextEditor](/controls/input/text-input/richtexteditor) 建立在同一套 FlowDocument 模型之上，因此完整支持基于 DocumentNode 的样式、文本选择，以及高性能的流式更新。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 快速上手 {#getting-started}

1. 运行 `dotnet add package` 安装 `Avalonia.Controls.Markdown` NuGet 包。

```bash
dotnet add package Avalonia.Controls.Markdown
```

2. 在可执行项目文件（`.csproj`）中填入你的 Avalonia 许可证密钥。密钥可以在 [Avalonia 门户](https://portal.avaloniaui.net)中获取。

```xml
<ItemGroup>
  <AvaloniaUILicenseKey Include="YOUR_LICENSE_KEY" />
</ItemGroup>
```

:::tip
对于多项目解决方案，可以把许可证密钥放进[环境变量](https://learn.microsoft.com/en-us/visualstudio/msbuild/how-to-use-environment-variables-in-a-build)或[共享 props 文件](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory?view=vs-2022#directorybuildprops-example)，免得到处重复。
:::

3. 在 `App.axaml` 文件中通过 `StyleInclude` 引用默认主题。它会带来 Markdown 控件所需的资源。

```xml
<Application.Styles>
   <StyleInclude Source="avares://Avalonia.Controls.Markdown/Themes/Default.axaml" />
   <!-- other styles -->
</Application.Styles>
```

关于安装 Avalonia Pro 控件的更多内容，请参阅[安装 Avalonia Pro](/tools/installing-avalonia-pro)。

## Architecture

`Markdown` 控件按下面这条流水线，把 Markdown 文本变成一份活的 `FlowDocument`：

1. **Markdown 文本**先被解析成 Markdig AST。
2. AST 再渲染成 `DocumentSnapshot`（一份不可变、线程安全的表示）。
3. 该快照被应用到 `FlowDocument` 上，由后者持有活的文档树。
4. 最后由 `EditorTextView`（与 `RichTextEditor` 所用的是同一个渲染器）把文档画出来。

由于该控件与 `RichTextEditor` 共用文档模型，所有文档元素（`Paragraph`、`Section`、`Table`、`RichSpan`、`RichHyperlink` 等）都是完整的 `StyledElement` 实例。也就是说，你可以用 Avalonia 的样式选择器和 CSS 式的类来选中它们，而不只是依赖具名资源。

## 用法示例 {#usage-examples}

### XAML 用法 {#xaml-usage}

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:local="using:MarkdownSample"
        mc:Ignorable="d"
        x:Class="MarkdownSample.MainWindow">
 <Markdown xml:space="preserve">
  # Markdown
  ## Headings
  ### Heading 3
  #### Heading 4
  ##### Heading 5
  ###### Heading 6

  **Bold Text**
  *Italic Text*
  ~~Strikethrough~~
  __Bold__ and _Italic_

  [Link to Avalonia](https://avaloniaui.net)

  `Inline code`

  - Unordered list item 1
  - Unordered list item 2
    - Nested item 2a
    - Nested item 2b
  ---
  1. Ordered list item 1
  2. Ordered list item 2
     1. Nested ordered 2a
     2. Nested ordered 2b
  ---  
  > Blockquote example
  >> Nested blockquote
  ---
  | Header 1 | Header 2 |
  |----------|----------|
  | Cell 1   | Cell 2   |
  | Cell 3   | Cell 4   |

  ![Sample Image](https://private-user-images.githubusercontent.com/552074/446176752-21950b56-cd28-4574-9a0a-73bb17b89d31.png)
 </Markdown>
</Window>
```
> **注意：** XAML 示例中的 `xml:space="preserve"` 特性很重要。它能确保 Markdown 文本中的空白和换行被原样保留，不被 XAML 编译器规整掉。把 Markdown 直接内嵌进 XAML 时，务必带上这个特性。

### XAML 用法（绑定到视图模型） {#xaml-usage-with-view-model-binding}

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:local="using:MarkdownSample"
        mc:Ignorable="d"
        x:Class="MarkdownSample.MainWindow">
    <Window.DataContext>
        <local:MarkdownViewModel/>
    </Window.DataContext>
    <Markdown Text="{Binding MarkdownText}" />
</Window>
```

### 视图模型示例（从文件加载） {#view-model-example-load-from-file}

```csharp
namespace MarkdownSample;

public class MarkdownViewModel
{
    public string MarkdownText { get; }

    public MarkdownViewModel()
    {
        MarkdownText = File.ReadAllText("Example.md");
    }
}
```

### C# 用法 {#c-usage}

```csharp
var markdown = new Markdown
{
    Text = "# Hello, Markdown!"
};
```

### 流式用法 {#streaming-usage}

`Markdown` 控件支持增量追加文本，适合渲染来自大模型或其他流式来源的内容：

```csharp
// Simple convenience method with automatic session management
markdown.AppendText("# Streaming\n\nContent arrives ");
markdown.AppendText("incrementally...");

// Full control via a streaming session
using var session = markdown.BeginStreaming();
session.Append("# Response\n\n");
session.Append("Paragraph text...");
await session.CompleteAsync();
```

流式引擎在后台线程上解析 Markdown，把新的 AST 与上一版作差分，只把变化的块应用到活文档上。设置 `AutoScrollToEnd="True"` 可让视口在流式输出期间始终停在底部。

## API 一览 {#api-overview}

### 属性 {#properties}

| 属性           | 类型                        | 说明                                              |
|--------------------|-----------------------------|----------------------------------------------------------|
| Text               | string?                     | 要渲染的 Markdown 文本。                                 |
| SelectionBrush     | IBrush?                     | 选区高亮所用的画刷。                           |
| CaretBrush         | IBrush?                     | 插入符所用的画刷。                              |
| SelectedText       | string                      | 只读。当前选区的内容。             |
| CanCopy            | bool                        | 只读。当前能否执行「复制」命令。     |
| AutoScrollToEnd    | bool                        | 流式输出期间让视口始终滚动到底部。 |

### 方法 {#methods}

| 方法                            | 说明                                                        |
|-----------------------------------|--------------------------------------------------------------------|
| Copy()                            | 把当前选区复制到剪贴板。                     |
| SelectAll()                       | 全选内容。                                               |
| ClearSelection()                  | 清除当前选区。                                      |
| ScrollToEnd()                     | 把视口滚动到文档末尾。                   |
| BeginStreaming()                   | 开启一次 `MarkdownStreamingSession` 以增量追加内容。     |
| AppendText(string, TimeSpan?)     | 便捷方法：创建或复用一个流式会话。     |

### 事件 {#events}

| 事件                | 说明                                          |
|----------------------|------------------------------------------------------|
| CopyingToClipboard   | 在选区被复制到剪贴板之前触发。可以在处理程序中阻止这次复制。 |
| SelectionChanged     | 文本选区变化时触发。              |

## 定制 Markdown 流水线 {#customizing-the-markdown-pipeline}

`Markdown` 控件用 [Markdig](https://github.com/xoofx/markdig) 解析 Markdown。默认启用下列扩展：自动链接、提示块、emoji、脚注、网格表格、管道表格、强调扩展（删除线、上标、下标）、任务列表，以及一个内置的符号扩展。

要增删 Markdig 扩展，请派生 `Markdown` 并重写 `ConfigurePipeline`。传入的构建器已经套用了默认扩展，所以你的重写是在此基础上叠加：

```csharp
public class CustomMarkdown : Markdown
{
    protected override void ConfigurePipeline(MarkdownPipelineBuilder builder)
    {
        // Add the Markdig mathematics extension (LaTeX-style math blocks)
        builder.UseMathematics();
    }
}
```

流水线只构建一次，并在控件实例的整个生命周期内缓存复用。静态渲染和流式会话用的都是它。

### 移除某个默认扩展 {#removing-a-default-extension}

Markdig 没有提供内置的 `Remove` 辅助方法，但你可以在流水线构建之前按类型把某个扩展移掉：

```csharp
public class NoEmojiMarkdown : Markdown
{
    protected override void ConfigurePipeline(MarkdownPipelineBuilder builder)
    {
        // Remove the emoji extension that was added by the default configuration
        var emoji = builder.Extensions.OfType<Markdig.Extensions.Emoji.EmojiExtension>().FirstOrDefault();
        if (emoji != null)
            builder.Extensions.Remove(emoji);
    }
}
```

### 在 XAML 中使用派生类 {#using-the-subclass-in-xaml}

为你的派生类注册一个命名空间，用它取代 `Markdown`：

```xml
<Window xmlns:local="using:MyApp">
    <local:CustomMarkdown Text="{Binding MarkdownText}" />
</Window>
```

### 让默认主题作用于派生类 {#applying-the-default-theme-to-a-subclass}

默认主题和样式直接以基类型为目标，不会自动套用到派生类型上。如果你用的是派生类（比如上面例子里的 `CustomMarkdown`），它渲染出来将是没有样式的。

要把针对 `Markdown` 的那套样式也用到 `CustomMarkdown` 上，请重写 `StyleKeyOverride`，把样式键重定向回基类型。

```csharp
public class CustomMarkdown : Markdown
{
    protected override Type StyleKeyOverride => typeof(Markdown);

    // Your customizations
}
```

## 自定义图片加载器 {#custom-image-loader}

图片加载由 `MarkdownImage` 文档元素负责，而不是 `Markdown` 控件本身。你可以写一条以 `MarkdownImage` 为目标的样式来指派加载器：

```xml
<Style Selector="MarkdownImage">
    <Setter Property="ImageLoader" Value="{StaticResource MyCustomLoader}" />
</Style>
```

实现自定义 `MarkdownImageLoader` 的详细示例，请参阅[图片加载器](/controls/data-display/text-display/markdown/imageloader)页面。

## 代码高亮器 {#code-highlighter}

语法高亮由 `MarkdownCodeBlock` 文档元素负责。你可以写一条样式来指派高亮器：

```xml
<Style Selector="MarkdownCodeBlock">
    <Setter Property="Highlighter" Value="{StaticResource TextMateHighlighter}" />
</Style>
```

安装包和用法示例请参阅[代码高亮器](/controls/data-display/text-display/markdown/codehighlighter)页面。

## Styling

由于 `Markdown` 控件建立在共享的文档模型之上，渲染出的所有元素（`Paragraph`、`Section`、`Table`、`RichSpan`、`RichHyperlink` 等）都是带 CSS 式类的完整 Avalonia `StyledElement` 实例。你可以用标准的 Avalonia 样式选择器来定制它们：

```xml
<!-- Make all H1 headings red -->
<Style Selector="Paragraph.h1">
    <Setter Property="Foreground" Value="Red" />
</Style>

<!-- Custom quote block background -->
<Style Selector="Section.quoteBlock">
    <Setter Property="Background" Value="#f0f0f0" />
</Style>
```

字号、外边距、主题变体配色等常用取值，也都提供了具名资源。

完整的样式选择器和资源清单请参阅 [Markdown 样式](/controls/data-display/text-display/markdown/markdown-styling)页面。

## 安装 {#installation}

安装 Avalonia Pro 组件的分步说明，请参阅[安装指南](/tools/installing-avalonia-pro)。

把 Markdown 包添加到你的项目中：

```bash
dotnet add package Avalonia.Controls.Markdown
```

在 `App.axaml` 中通过 `StyleInclude` 引用随包提供的 `Default.axaml` 主题，把资源带进来：

```xml
<Application.Styles>
   <StyleInclude Source="avares://Avalonia.Controls.Markdown/Themes/Default.axaml" />
   <!-- other styles -->
</Application.Styles>
```

## 另请参阅 {#see-also}

- [Markdown 样式](/controls/data-display/text-display/markdown/markdown-styling)
- [图片加载器](/controls/data-display/text-display/markdown/imageloader)
- [代码高亮器](/controls/data-display/text-display/markdown/codehighlighter)
