---
id: textblock
title: TextBlock
description: 一个只读控件，用于显示带格式的文本，支持多行、行内格式和完整的字体控制。
doc-type: reference
---

import TextBlockRunScreenshot from '/img/controls/textblock/textblock-run.png';
import TextBlockUIContainerScreenshot from '/img/controls/textblock/textblock-uicontainer.png';

[`TextBlock`](/api/avalonia/controls/textblock) 是一个只读标签，用于显示文字。它可以显示多行，字体也完全可控。若用户需要选中并复制这些文字，请改用 `SelectableTextBlock`。

## 常用属性 {#common-properties}

| 属性          | 类型                       | 说明                                                                                                                                                                                                           |
| ----------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Text`            | `string`                   | 要显示的文本。                                                                                                                                                                                                  |
| `FontSize`        | `double`                   | 字号，单位为设备无关像素。                                                                                                                                                                    |
| `FontWeight`      | `FontWeight`               | 字重。默认为 `Normal`，可选值包括 `Bold`。                                                                                                                                                  |
| `FontStyle`       | `FontStyle`                | 作用于字形的样式。默认为 `Normal`，可选值包括 `Italic`。                                                                                                                                     |
| `FontFamily`      | `FontFamily`               | 渲染文本所用的字体族。可以用逗号分隔列出若干后备字体。                                                                                                                        |
| `Foreground`      | `IBrush`                   | 绘制文字所用的画刷。                                                                                                                                                                                     |
| `Background`      | `IBrush`                   | 绘制文字背后区域所用的画刷。                                                                                                                                                                     |
| `TextAlignment`   | [`TextAlignment`](/api/avalonia/media/textalignment) | 控制文本在控件内的水平对齐方式。可选值有 `Left`、`Center`、`Right`、`Justify` 和 `DetectFromContent`。                                                                                  |
| `TextWrapping`    | [`TextWrapping`](/api/avalonia/media/textwrapping) | 控制文本到达控件边缘时是否换行。可选值有 `NoWrap`（默认）、`Wrap` 和 `WrapWithOverflow`。                                                                                  |
| `TextTrimming`    | [`TextTrimming`](/api/avalonia/media/texttrimming) | 控制文本溢出时如何截断。可选值包括 `None`（默认）、`CharacterEllipsis`、`WordEllipsis` 等。完整说明请参阅 [TextTrimming](/controls/data-display/text-display/texttrimming)。                                  |
| `MaxLines`        | `int`                      | 限制可见行数。与 `TextWrapping` 和 `TextTrimming` 搭配使用时，超过这么多行之后的内容会被截断。                                                                                   |
| `LineHeight`      | `double`                   | 每行文字的行高。设为 `NaN`（默认）则由字体度量决定行高。                                                                                                            |
| `TextDecorations` | `TextDecorationCollection` | 作用于字形的线条装饰。默认为 none，可选值包括 `Underline`、`Strikethrough`、`Baseline` 和 `Overline`。要同时套用多项，用空格分隔列出即可。 |
| `LetterSpacing`   | `double`                   | 字符之间的额外间距，单位为设备无关像素，默认为 `0`。它是继承自 `TextElement` 的可继承附加属性，因此也可以设在父控件上。                                   |
| `Padding`         | `Thickness`                | 控件边界与文字内容之间的间距。                                                                                                                                                              |
| `xml:space`       | XML 特性              | 设置 `xml:space="preserve"` 可让 XML 解析器保留换行和空白。不加这个特性，空白默认会被剥除。                                                                 |

## 基本示例 {#basic-example}

下面这个例子用多个 `TextBlock` 控件分别呈现标题、含额外空格的单行文字，以及多行文字。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui" Margin="20" Spacing="10">
  <TextBlock FontSize="18" FontWeight="Bold">Heading</TextBlock>
  <TextBlock FontStyle="Italic" xml:space="preserve">This is  a single line.</TextBlock>
  <TextBlock xml:space="preserve">This is a multi-line
  display that has
  returns in it.
  The text block
  respects the line
  breaks set out in XAML.</TextBlock>
</StackPanel>
```

</XamlPreview>

## 文本换行 {#text-wrapping}

`TextBlock` 默认不换行，文字比可用空间宽时会被裁掉。设置 `TextWrapping` 可以改变这一行为：

| 值             | 行为                                                                                      |
| ----------------- | --------------------------------------------------------------------------------------------- |
| `NoWrap`          | 不换行，文字可能被裁掉（默认）。                                             |
| `Wrap`            | 在可用宽度内最靠近边缘、放得下的那个字符处换行。                     |
| `WrapWithOverflow`| 尽量换行，但若某个单词比控件还宽，则允许它溢出。 |

```xml
<TextBlock Width="200"
           TextWrapping="Wrap"
           Text="This is a long sentence that will wrap when it reaches the edge of the control." />
```

## 文本截断 {#text-trimming}

文字超出可用空间时，与其生硬地裁掉，不如显示一个省略号。设置 `TextTrimming` 属性即可控制省略号出现在哪里，常用取值有 `CharacterEllipsis` 和 `WordEllipsis`。

```xml
<TextBlock Width="150"
           TextTrimming="CharacterEllipsis"
           Text="This text will be trimmed with an ellipsis." />
```

你可以把 `TextWrapping`、`TextTrimming` 和 `MaxLines` 组合起来，让文字换行到固定的行数，并在最后一行截断溢出部分：

```xml
<TextBlock Width="200"
           MaxLines="3"
           TextWrapping="Wrap"
           TextTrimming="WordEllipsis"
           Text="This is a long paragraph that wraps for up to three lines, then trims any remaining overflow with an ellipsis." />
```

完整的截断模式清单和效果示例，请参阅 [TextTrimming](/controls/data-display/text-display/texttrimming)。

## 文本对齐 {#text-alignment}

用 `TextAlignment` 属性控制文字在控件内的水平摆放方式：

```xml
<StackPanel Width="300" Spacing="8">
  <TextBlock TextAlignment="Left" Text="Left-aligned text" />
  <TextBlock TextAlignment="Center" Text="Center-aligned text" />
  <TextBlock TextAlignment="Right" Text="Right-aligned text" />
  <TextBlock TextAlignment="Justify" TextWrapping="Wrap"
             Text="Justified text spreads words evenly across the full width of the control when wrapping is enabled." />
</StackPanel>
```

## Inlines

文本行内元素让你能在一个 `TextBlock` 内部混排各式各样的格式和控件。`TextBlock.Text` 通常只用来显示一段格式统一的文字，而它的子内容则可以容纳一组行内元素。

### Run

`Run` 行内元素表示一段格式统一的连续文字。你可以把 `Run.Text` 绑定到视图模型的属性，并为每一段单独设置样式。

```xml
<TextBlock xmlns="https://github.com/avaloniaui">
  <TextBlock.Styles>
    <Style Selector="Run.activity">
      <Setter Property="Foreground" Value="#C469EE" />
      <Setter Property="FontStyle" Value="Italic" />
      <Setter Property="TextDecorations" Value="Underline" />
    </Style>
  </TextBlock.Styles>

  <Run Text="Your name is" />
  <Run FontSize="24" FontWeight="Bold" Foreground="Orange" Text="{Binding Name}" />
  <Run Text="and your favorite activity is" />
  <Run Classes="activity" Text="{Binding Activity}" />
</TextBlock>
```

<Image light={TextBlockRunScreenshot} alt="A TextBlock using Run inlines with mixed formatting and data binding" position="center" maxWidth={400} cornerRadius="true"/>

### LineBreak

`LineBreak` 行内元素在文本流中强制换行。

<XamlPreview>

```xml
<TextBlock xmlns="https://github.com/avaloniaui">
    This is the first line and<LineBreak />here comes the second
</TextBlock>
```

</XamlPreview>

### Span

[`Span`](/api/avalonia/controls/documents/span) 行内元素把其他行内元素归为一组，并可套用自己的格式。Avalonia 还提供了几个派生自 `Span` 的预设格式行内元素：`Bold`、`Italic` 和 `Underline`。除了写样式，你也可以派生 `Span` 来定义自己的格式。

<XamlPreview>

```xml
<TextBlock xmlns="https://github.com/avaloniaui"
           TextWrapping="Wrap">
  This text is <Span Foreground="Green"> green with <Bold>bold sections,</Bold>
  <Italic>italic <Span Foreground="Red">red</Span> sections,</Italic>
  some
  <Run FontSize="24"> enlarged font runs,</Run>
  and</Span>
  back to the original formatting
</TextBlock>
```

</XamlPreview>

### InlineUIContainer

`InlineUIContainer` 让你能把任意 `Control` 当作行内元素嵌进文本流中。

```xml
<TextBlock xmlns="https://github.com/avaloniaui"
           ClipToBounds="False"
           FontSize="32"
           TextWrapping="Wrap">
    This <Span BaselineAlignment="TextTop">example</Span> shows the <Bold>power</Bold> of
    <InlineUIContainer BaselineAlignment="Baseline">
        <Image Width="32" Height="32" VerticalAlignment="Top" Source="/Assets/avalonia-logo.ico" />
    </InlineUIContainer>
    in creating rich text displays with
    <InlineUIContainer>
        <Button Padding="0,8,0,0">
            <TextBlock ClipToBounds="False" FontSize="24" Text="inline button" />
        </Button>
    </InlineUIContainer>
    inline controls
</TextBlock>
```

<Image light={TextBlockUIContainerScreenshot} alt="A TextBlock with inline UI containers including an image and a button" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [SelectableTextBlock](/controls/data-display/text-display/selectabletextblock)
- [Label](/controls/data-display/text-display/label)
- [TextTrimming](/controls/data-display/text-display/texttrimming)
- [TextBlock API 参考](/api/avalonia/controls/textblock)
- [GitHub 上的 `TextBlock.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/TextBlock.cs)
