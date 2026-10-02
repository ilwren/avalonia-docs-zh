---
id: codehighlighter
title: CodeHighlighter
description: 为 Markdown 控件渲染的代码块加上语法高亮；ColorCode 和 TextMate 两套实现以独立包的形式提供。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

`Markdown` 控件支持为围栏代码块加语法高亮。在控件上设置 `Markdown.CodeHighlighter`，其文档中的每个代码块就都会用上它。两套实现以独立的 NuGet 包分发：`ColorCodeHighlighter`（轻量，支持的语言有限）和 `TextMateHighlighter`（完整的 TextMate 语法支持，自带主题）。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 安装 {#installation}

高亮器以独立的 NuGet 包分发。按需安装其中一个即可：

**ColorCode** 是一款轻量高亮器，覆盖 C#、XML、JSON、JavaScript 等常见语言：

```bash
dotnet add package Avalonia.Controls.Markdown.ColorCode
```

**TextMate** 提供完整的 TextMate 语法支持和内置主题，覆盖的语言相当广：

```bash
dotnet add package Avalonia.Controls.Markdown.TextMate
```

## 该选哪款高亮器 {#choosing-a-highlighter}

| 特性 | `ColorCodeHighlighter` | `TextMateHighlighter` |
|---|---|---|
| 语言覆盖面 | 常见语言（C#、XML、JSON、JS 等） | 借助 TextMate 语法，覆盖面很广 |
| Theming | 沿用你的应用主题配色 | 内置若干 `ThemeName` 取值，比如 `LightPlus` 和 `DarkPlus` |
| 包体积 | Smaller | 较大（内含语法文件） |
| 配置 | Minimal | 需要给出 `Theme` 属性值 |

如果你只需高亮少数几种常见语言、又想让依赖尽量轻，请用 `ColorCodeHighlighter`；如果需要广泛的语言支持，或想让配色主题独立于应用主题，请用 `TextMateHighlighter`。

## 在 XAML 中使用 `TextMateHighlighter` {#using-textmatehighlighter-in-xaml}

`Markdown.CodeHighlighter` 是附加属性，直接设置在控件上：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:textMate="clr-namespace:Avalonia.Controls;assembly=Avalonia.Controls.Markdown.TextMate">
  <Markdown Text="# Example&#10;&#10;```csharp&#10;var x = 1;&#10;```">
    <Markdown.CodeHighlighter>
      <textMate:TextMateHighlighter Theme="LightPlus" />
    </Markdown.CodeHighlighter>
  </Markdown>
</Window>
```

改变高亮器的 `Theme` 属性即可在运行时切换主题，用到它的每个代码块都会重新高亮。

## 在 XAML 中使用 `ColorCodeHighlighter` {#using-colorcodehighlighter-in-xaml}

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:cc="clr-namespace:Avalonia.Controls;assembly=Avalonia.Controls.Markdown.ColorCode">
  <Markdown Text="# Example&#10;&#10;```csharp&#10;var x = 1;&#10;```">
    <Markdown.CodeHighlighter>
      <cc:ColorCodeHighlighter />
    </Markdown.CodeHighlighter>
  </Markdown>
</Window>
```

## 让多个控件共用一个高亮器 {#sharing-one-highlighter-across-several-controls}

把高亮器声明为资源，再让各个控件都指向它。一个实例可以服务任意多个 `Markdown` 控件：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:textMate="clr-namespace:Avalonia.Controls;assembly=Avalonia.Controls.Markdown.TextMate">
  <Window.Resources>
    <textMate:TextMateHighlighter x:Key="Highlighter" Theme="DarkPlus" />
  </Window.Resources>

  <StackPanel>
    <Markdown Markdown.CodeHighlighter="{StaticResource Highlighter}" Text="{Binding First}" />
    <Markdown Markdown.CodeHighlighter="{StaticResource Highlighter}" Text="{Binding Second}" />
  </StackPanel>
</Window>
```

## 在代码中设置高亮器 {#setting-the-highlighter-in-code}

```csharp
using TextMateSharp.Grammars; // ThemeName

var highlighter = new TextMateHighlighter { Theme = ThemeName.DarkPlus };

// Every code block in this control's document uses it
markdown.CodeHighlighter = highlighter;

// Or through the static accessor, which takes any StyledElement
Markdown.SetCodeHighlighter(markdown, highlighter);
```

若想让某个代码块与众不同，可以在那个元素上设置 `MarkdownCodeBlock.Highlighter`。写在单个代码块上的取值会盖过控件给出的取值。

## 在代码块中指定语言 {#specifying-languages-in-code-blocks}

要获得正确的高亮，请在 Markdown 源码里起始的三个反引号后面写上语言标识符。例如：

````markdown
```csharp
Console.WriteLine("Hello, world!");
```
````

若省略语言标识符，高亮器会把该代码块当作纯文本渲染，不上色。语言标识符保存在 `MarkdownCodeBlock.LanguageId` 属性上。

## 注释支持情况 {#notes}

- 当你改变代码块所用高亮器的某个属性（比如 `Theme`）时，代码块会自行重新渲染。自定义高亮器要调用 `OnInvalidated` 来发出这一通知。
- `Markdown.CodeHighlighter` 是一个可继承的附加属性，因此一个实例无需样式就能覆盖控件文档中的所有代码块。写在单个代码块上的 `MarkdownCodeBlock.Highlighter` 会覆盖它。
- `MarkdownCodeBlock` 继承自 `Paragraph`，是完整的 `StyledElement`，因此样式选择器照样能选中它，用来定制背景、内边距、字体族等外观。

## 另请参阅 {#see-also}

- [Markdown 控件](/controls/data-display/text-display/markdown)
- [Markdown 样式](/controls/data-display/text-display/markdown/markdown-styling)
