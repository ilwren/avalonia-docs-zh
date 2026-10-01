---
id: texttrimming
title: TextTrimming
description: 关于 TextTrimming 属性
---

import CharacterEllipsis from '/img/reference/text/texttrimming/texttrimming-characterellipsis.png';
import LeadingCharacterEllipsis from '/img/reference/text/texttrimming/texttrimming-leadingcharacterellipsis.png';
import NoTrimming from '/img/reference/text/texttrimming/texttrimming-none.png';
import PrefixCharacterEllipsis from '/img/reference/text/texttrimming/texttrimming-prefixcharacterellipsis.png';
import WordEllipsis from '/img/reference/text/texttrimming/texttrimming-wordellipsis.png';
import TextWrappingWithTextTrimming from '/img/reference/text/texttrimming/textwrapping-with-texttrimming.png';

## 概述 {#overview}

[`TextTrimming`](/api/avalonia/media/texttrimming) 属性让你控制文字超出控件可用空间时如何显示。[`TextBlock`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/TextBlock.cs)、[`SelectableTextBlock`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/SelectableTextBlock.cs)、[`ContentPresenter`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Presenters/ContentPresenter.cs) 等显示文本的控件都提供该属性。

文本截断会加上省略号（…）来表示文字被截短，而不是生硬地把文字切断。

:::note
Avalonia 默认使用 Unicode 省略号字符 `U+2026`，而不是三个句点。
:::

## 截断模式 {#trimming-modes}

Avalonia 提供六种文本截断方式：

1. None
2. CharacterEllipsis
3. WordEllipsis
4. PrefixCharacterEllipsis
5. LeadingCharacterEllipsis
6. PathSegmentEllipsis

### None

不作截断。文字到达控件边界即被切断。

```xml
<TextBlock Text="This is a very long line of text that will get cut off."
           TextTrimming="None"
           Width="200" />
```

<Image light={NoTrimming} alt="A screenshot of an IDE, displaying a long line of text in a box that is abruptly cut off." position="center" maxWidth={400} cornerRadius="true" />

### CharacterEllipsis

在某个字符结束处截断，并在截断处加上省略号。

适合通用场景——当界面设计对空间占用有精确要求时。

```xml
<TextBlock Text="This is a very long line of text that will get cut off."
           TextTrimming="CharacterEllipsis"
           Width="200" />
```

<Image light={CharacterEllipsis} alt="A screenshot of an IDE, displaying a long line of text in a box that is cut off after a character, with an ellipsis added." position="center" maxWidth={400} cornerRadius="true" />

### WordEllipsis

在某个单词结束处截断，保证单词完整；实在放不下时再加省略号。

避免出现残缺的单词，以求可读性最佳。

```xml
<TextBlock Text="This is a very long line of text that will get cut off."
           TextTrimming="WordEllipsis"
           Width="200" />
```

<Image light={WordEllipsis} alt="A screenshot of an IDE, displaying a long line of text in a box that is cut off after a complete word, with an ellipsis added." position="center" maxWidth={400} cornerRadius="true" />

### PrefixCharacterEllipsis

从中间截断。字符串的开头和结尾都保留，中间用省略号隔开。

默认先显示前八个字符，接着是省略号，再把剩余可用空间用末尾的字符填满。

适合文件路径、URL，以及任何开头和结尾都需要看到的文字。

```xml
<TextBlock Text="C:\Users\Documents\Projects\MyProject\source.cs"
           TextTrimming="PrefixCharacterEllipsis"
           Width="200" />
```

<Image light={PrefixCharacterEllipsis} alt="A screenshot of an IDE, displaying a long line of text in a box that is cut off in the middle, with an ellipsis placed between the starting and ending characters." position="center" maxWidth={400} cornerRadius="true" />

### LeadingCharacterEllipsis

从开头截断。显示的文字以省略号开头，后面接文本末尾的字符。

适合文件路径，以及任何只有结尾才重要的文字。

```xml
<TextBlock Text="C:\Users\Documents\Projects\MyProject\source.cs"
           TextTrimming="LeadingCharacterEllipsis"
           Width="200" />
```

<Image light={LeadingCharacterEllipsis} alt="A screenshot of an IDE, displaying a long line of text in a box that is cut off at the start, with an ellipsis replacing the starting characters and the ending characters visible." position="center" maxWidth={400} cornerRadius="true" />

### PathSegmentEllipsis

折叠路径中间的若干段，同时保留文件路径或 URL 的开头（盘符、服务器名）和结尾（文件名）。算法会去掉靠近路径中部的那些段，用省略号代替。

比如空间紧张时，`C:\Users\Alice\Documents\Projects\Avalonia\src\Button.cs` 会变成 `C:\Users\...\Button.cs`。

```xml
<TextBlock Text="C:\Users\Alice\Documents\Projects\Avalonia\src\Controls\Button.cs"
           TextTrimming="PathSegmentEllipsis"
           Width="200" />
```

这种模式把正斜杠和反斜杠都当作路径分隔符，因此文件系统路径和 URL 都适用。

## 用法示例 {#example-uses}

### 与 MaxWidth 搭配 {#combining-with-maxwidth}

把 `TextTrimming` 与 `MaxWidth` 搭配使用，可以做出自适应的文字显示，同时让界面上的占位区域保持稳定。

```xml
<TextBlock Text="{Binding UserName}"
           MaxWidth="300"
           TextTrimming="CharacterEllipsis" />
```

### 与 TextWrapping 搭配 {#combining-with-textwrapping}

把 `TextTrimming` 和 `TextWrapping` 组合起来，即可在启用换行的同时，对最后一行可见文字作截断。

```xml
<TextBlock Text="{Binding Content}"
           Width="300"
           MaxLines="3"
           TextWrapping="Wrap"
           TextTrimming="WordEllipsis" />
```

<Image light={TextWrappingWithTextTrimming} alt="A screenshot of an IDE, displaying a long line of text in a box that wraps within the box for three lines, before being cut off with an ellipsis added." position="center" maxWidth={400} cornerRadius="true" />

## 另请参阅 {#see-also}

- [TextBlock 控件](https://docs.avaloniaui.net/docs/reference/controls/textblock)
- [SelectableTextBlock 控件](https://docs.avaloniaui.net/docs/reference/controls/selectable-textblock)
- [TextTrimming API 参考](https://reference.avaloniaui.net/api/Avalonia.Media/TextTrimming/)