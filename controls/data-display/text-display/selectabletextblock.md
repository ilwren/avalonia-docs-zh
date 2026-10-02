---
id: selectabletextblock
title: SelectableTextBlock
description: 一个只读文本标签，允许用户选中并复制其中显示的文字。
doc-type: reference
---

`SelectableTextBlock` 是一个只读标签，用于显示文字，并允许用户选中和复制。它的表现与 `TextBlock` 类似，但内置了用鼠标或键盘选择文本的能力。它可以显示多行文字，字体也完全可控。

## 常用属性 {#common-properties}

| 属性                   | 类型        | 说明                                                                                                                                                                                                           |
| -------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Text`                     | `string`    | 要显示的文本。                                                                                                                                                                                                  |
| `SelectionStart`           | `int`       | 当前选区起点的字符索引。                                                                                                                                                           |
| `SelectionEnd`             | `int`       | 当前选区终点的字符索引。                                                                                                                                                             |
| `SelectedText`             | `string`    | 获取当前选中的文本（只读）。                                                                                                                                                                         |
| `SelectionBrush`           | `IBrush`    | 高亮选中文本所用的画刷。                                                                                                                                                                            |
| `SelectionForegroundBrush` | `IBrush`    | 选中文本前景色所用的画刷。                                                                                                                                                                   |
| `FontSize`                 | `double`    | 字号。                                                                                                                                                                                                 |
| `FontWeight`               | `FontWeight`| 字重。默认为 normal，可选值包括 `Bold`。                                                                                                                                                    |
| `FontStyle`                | `FontStyle` | 作用于字形的样式。默认为 normal，可选值包括 `Italic`。                                                                                                                                       |
| `TextDecorations`          | `TextDecorationCollection` | 作用于字形的线条装饰。默认为 none，可选值包括 `Underline`、`Strikethrough`、`Baseline` 和 `Overline`。要同时套用多项，用空格分隔列出即可。 |
| `TextWrapping`             | `TextWrapping` | 控制文本到达控件边缘时是否换行。可选值包括 `NoWrap`、`Wrap` 和 `WrapWithOverflow`。                                                                                    |
| `xml:space`                | XML 特性 | 设置 `xml:space="preserve"` 可让 XML 解析器保留换行和空白。不加这个特性，空白默认会被剥除。                                                              |

## 事件 {#events}

| 事件                | 说明                                                        |
| -------------------- | ------------------------------------------------------------------ |
| `CopyingToClipboard` | 选中的文本被复制到剪贴板时触发。可用它修改或取消这次复制操作。 |

## 基本示例 {#basic-example}

下面这个例子展示了三种用法：把可选中文本用作标题、配上自定义选区画刷的单行文本，以及预先设好选区范围的多行文本。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Width="200"
            Margin="20">
  <SelectableTextBlock Margin="0 5" FontSize="18" FontWeight="Bold">Heading</SelectableTextBlock>
  <SelectableTextBlock Margin="0 5" FontStyle="Italic"
                       xml:space="preserve"
                       SelectionBrush="Red">This is a single line.</SelectableTextBlock>
  <SelectableTextBlock Margin="0 5" xml:space="preserve"
                       SelectionStart="3" SelectionEnd="13">This is a multi-line
  display that has
  returns in it.
  The text block
  respects the
  line breaks
  set out in XAML.</SelectableTextBlock>
</StackPanel>
```

</XamlPreview>

## 用代码选中文本 {#selecting-text-programmatically}

你可以在代码隐藏或视图模型中设置 `SelectionStart` 和 `SelectionEnd` 属性，来控制选中哪一段文字。

```xml
<SelectableTextBlock x:Name="MyTextBlock"
                     Text="Select part of this text programmatically." />
<Button Content="Select words 2-4" Click="OnSelectClicked" />
```

```csharp
private void OnSelectClicked(object? sender, RoutedEventArgs e)
{
    MyTextBlock.SelectionStart = 7;
    MyTextBlock.SelectionEnd = 24;
}
```

把 `SelectionStart` 设为 `0`、`SelectionEnd` 设为文本长度，即可全选。

```csharp
MyTextBlock.SelectionStart = 0;
MyTextBlock.SelectionEnd = MyTextBlock.Text?.Length ?? 0;
```

## 定制选区外观 {#customizing-selection-appearance}

设置 `SelectionBrush` 和 `SelectionForegroundBrush` 即可定制选中文本的外观。

```xml
<SelectableTextBlock Text="Custom selection colors"
                     SelectionBrush="#335599FF"
                     SelectionForegroundBrush="White" />
```

## 另请参阅 {#see-also}

- [TextBlock](/controls/data-display/text-display/textblock)
- [Label](/controls/data-display/text-display/label)
- [SelectableTextBlock API 参考](/api/avalonia/controls/selectabletextblock)
- [GitHub 上的 `SelectableTextBlock.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/SelectableTextBlock.cs)
