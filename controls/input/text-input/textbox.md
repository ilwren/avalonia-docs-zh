---
title: TextBox
description: 单行或多行的文本输入控件，支持水印、密码掩码、校验和内嵌内容。
doc-type: reference
---

import TextBoxEntryScreenshot from '/img/controls/textbox/textbox-entry.gif';

[`TextBox`](/api/avalonia/controls/textbox) 提供一块供键盘输入的区域。它既可以当作用户名这类单行字段，也可以开启多行编辑，用来写笔记、评论等较长的内容。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Text` | `string` | 输入框中当前的文本。 |
| `PlaceholderText` | `string` | 输入为空时显示的淡色提示文字，有时也叫水印。 |
| `PlaceholderForeground` | `IBrush` | 渲染占位文字所用的画刷。 |
| `PasswordChar` | `char` | 把键入的字符统统藏起来，用指定的字符代替显示。 |
| `RevealPassword` | `bool` | 为 `true` 时显示真实的密码文本，而不是掩码字符。 |
| `AcceptsReturn` | `bool` | 允许用户输入换行，从而把输入框变成多行的。 |
| `AcceptsTab` | `bool` | 允许用户插入制表符，而不是用 Tab 切换焦点。 |
| `TextWrapping` | `TextWrapping` | 决定一行横向超出时如何处理。可选值：`NoWrap`、`Wrap`、`WrapWithOverflow`。 |
| `MaxLength` | `int` | 限制用户最多能输入多少个字符。`0` 表示不限。 |
| `IsReadOnly` | `bool` | 为 `true` 时，用户可以选择和复制文本，但不能编辑。 |
| `TextAlignment` | `TextAlignment` | 文本的水平对齐方式：`Left`、`Center`、`Right`。 |
| `InnerLeftContent` | `object` | 显示在 `TextBox` 内部左侧的内容（用于图标或标签）。 |
| `InnerRightContent` | `object` | 显示在 `TextBox` 内部右侧的内容（用于按钮或指示符）。 |
| `MinLines` | `int` | 可见的最少行数。当 `AcceptsReturn` 为 `true` 时，`TextBox` 会把自己撑到至少能显示这么多行。 |
| `CaretBlinkInterval` | `TimeSpan` | 插入符闪烁的间隔。设为 `TimeSpan.Zero` 可以让它不闪。 |

## Example

下面的例子包含一个基础的单行文本框、一个密码框，以及一个会自动换行的多行文本框：

```xml
<StackPanel Margin="20">
  <TextBlock Margin="0 5">Name:</TextBlock>
  <TextBox PlaceholderText="Enter your name"/>
  <TextBlock Margin="0 5">Password:</TextBlock>
  <TextBox PasswordChar="*" PlaceholderText="Enter your password"/>
  <TextBlock Margin="0 15 0 5">Notes:</TextBlock>
  <TextBox Height="100" AcceptsReturn="True" TextWrapping="Wrap"/>
</StackPanel>
```

<Image light={TextBoxEntryScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 水印（占位文字） {#watermark-placeholder-text}

设置 `PlaceholderText` 即可在 `TextBox` 为空时显示一行提示。提示文字的颜色可以用 `PlaceholderForeground` 来定：

```xml
<TextBox PlaceholderText="e.g. jane@example.com"
         PlaceholderForeground="Gray" />
```

用户一开始输入，占位文字就自动消失；内容被清空后它又会回来。

## 多行输入 {#multi-line-input}

要接受多行内容，请把 `AcceptsReturn` 设为 `True`，并配合 `TextWrapping="Wrap"`，让长行自动换行而不是横向滚动。用 `MinLines` 可以保证一个最小可见高度：

```xml
<TextBox AcceptsReturn="True"
         TextWrapping="Wrap"
         MinLines="4"
         PlaceholderText="Enter your comments here..." />
```

若同时把 `AcceptsTab` 设为 `True`，按 Tab 会插入制表符，而不是把焦点移到下一个控件。

## 限制输入长度 {#limiting-input-length}

用 `MaxLength` 可以限定用户最多能键入多少字符。对于长度上限已知的字段（邮政编码、用户名等），这很有用：

```xml
<TextBox MaxLength="50" PlaceholderText="Username (max 50 characters)" />
```

取值为 `0`（默认）表示不作限制。

## Validation

你可以在视图模型上用数据注解特性来校验 `TextBox` 的输入。只要实现了 `INotifyDataErrorInfo`，Avalonia 的绑定系统就会自动把校验错误呈现出来。例如，配合 CommunityToolkit.Mvvm 的源生成器：

```csharp
using System.ComponentModel.DataAnnotations;
using CommunityToolkit.Mvvm.ComponentModel;

public partial class MyViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "Email is required.")]
    [EmailAddress(ErrorMessage = "Enter a valid email address.")]
    private string _email = "";
}
```

```xml
<TextBox Text="{Binding Email}" PlaceholderText="Email address" />
```

校验未通过时，`TextBox` 默认会显示错误边框和工具提示。你可以在样式中通过该控件的 `:error` 伪类来定制这套外观。

## 视图模型绑定 {#view-model-binding}

以双向模式绑定 `Text`（这也是 `TextBox.Text` 的默认模式）：

```xml
<TextBox Text="{Binding Username}" PlaceholderText="Enter username" />
```

```csharp
[ObservableProperty]
private string _username = "";
```

## 带内嵌内容的输入框 {#input-with-inner-content}

用 `InnerLeftContent` 和 `InnerRightContent` 可以在 `TextBox` 内部放置图标或按钮：

```xml
<TextBox PlaceholderText="Search...">
    <TextBox.InnerRightContent>
        <Button Content="✕" Command="{Binding ClearSearchCommand}"
                Background="Transparent" BorderThickness="0" Padding="4" />
    </TextBox.InnerRightContent>
</TextBox>
```

## 另请参阅 {#see-also}

- [TextBox API 参考](/api/avalonia/controls/textbox)
- [GitHub 上的 `TextBox.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/TextBox.cs)
- [MaskedTextBox](/controls/input/text-input/maskedtextbox)
- [AutoCompleteBox](/controls/input/text-input/autocompletebox)
