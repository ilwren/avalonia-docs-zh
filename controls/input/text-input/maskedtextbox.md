---
id: maskedtextbox
title: MaskedTextBox
---

import MaskedTextPhoneBoxScreenshot from '/img/reference/controls/maskedtextbox/maskedtextbox-phone.gif';

`MaskedTextBox` 提供一块供键盘输入的区域，但其格式和可输入的字符会受一套由特殊字符组成的掩码模式约束。

掩码模式中还可以含有字面字符，它们会出现在输入内容里，且无法被覆盖输入。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性    | 说明                                                                  |
|-------------|------------------------------------------------------------------------------|
| `Mask`      | 要使用的掩码模式。特殊掩码字符见下表。 |
| `AsciiOnly` | 把输入限制为 ASCII 字母 a-z 和 A-Z。                            |
| `Text`      | 最终的输入文本，包含其中的字面字符。                   |

## 掩码字符 {#mask-characters}

Mask 属性接受一个字符串，其中可以混合固定字符与下列特殊字符：

| Mask Character | 说明                                                                                                                                                                             |
|:--------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|      `0`       | 数字，必填。此处接受 0 到 9 之间的任意一位数字。                                                                                                             |
|      `9`       | 数字或空格，选填。                                                                                                                                                               |
|      `#`       | 数字或空格，选填。如果掩码中该位置为空，它在 Text 属性里会呈现为一个空格。允许加号（+）和减号（-）。                         |
|      `L`       | 字母，必填。输入限制为 ASCII 字母 a-z 和 A-Z                                                                                                                      |
|      `?`       | 字母，选填。输入限制为 ASCII 字母 a-z 和 A-Z                                                                                                                      |
|      `&`       | 字符，必填。若 AsciiOnly 属性为 true，它的行为与「L」相同。                                                                                      |
|      `C`       | 字符，选填。任意非控制字符。若 AsciiOnly 属性设为 true，它的行为与「?」相同。                                                    |
|      `A`       | 字母或数字，必填。若 AsciiOnly 属性为 true，则只接受 ASCII 字母 a-z 和 A-Z，此时它的行为与「a」相同。        |
|      `a`       | 字母或数字，选填。若 AsciiOnly 属性设为 true，则只接受 ASCII 字母 a-z 和 A-Z，此时它的行为与「A」相同。 |
|      `.`       | 小数点占位符。实际显示的字符取决于格式提供程序所对应的小数符号，由控件的 FormatProvider 属性决定。           |
|      `,`       | 千位分隔占位符。实际显示的字符取决于格式提供程序所对应的千位分隔符，由控件的 FormatProvider 属性决定。  |
|      `:`       | 时间分隔符。实际显示的字符取决于格式提供程序所对应的时间符号，由控件的 FormatProvider 属性决定。                   |
|      `/`       | 日期分隔符。实际显示的字符取决于格式提供程序所对应的日期符号，由控件的 FormatProvider 属性决定。                   |
|      `$`       | 货币符号。实际显示的字符取决于格式提供程序所对应的货币符号，由控件的 FormatProvider 属性决定。                 |
|      `<`       | 转为小写。把之后的所有字符转换成小写。                                                                                                                           |
|      `>`       | 转为大写。把之后的所有字符转换成大写。                                                                                                                             |
|      `\|`      | 取消之前的转大写或转小写。                                                                                                                                              |
|      `\`       | 转义。对掩码字符转义，把它变成字面字符。                                                                                                                            |

用转义字符（反斜杠）可以把特殊字符当作字面字符插入。比如要插入美元符号：

`Mask="\$999,000.00"`

## Example

这是一个基础示例：

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Margin="20">
  <TextBlock Margin="0 5">International phone number:</TextBlock>
  <MaskedTextBox Mask="(+09) 000 000 0000" />
  <TextBlock Margin="0 15 0 5">UK VAT number:</TextBlock>
  <MaskedTextBox Mask="GB 000 000 000" />
</StackPanel>
```

</XamlPreview>

## 另请参阅 {#see-also}

- [GitHub 上的 `MaskedTextBox.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/MaskedTextBox.cs)
