---
id: label
title: Label
description: 一个显示文本的控件：被点击或按下访问键时，会把焦点转交给指定的输入元素。
doc-type: reference
---

[`Label`](/api/avalonia/controls/label) 控件显示一段文本，并能把焦点转交给指定的目标控件。当你点击该标签，或按下 Alt 加它的访问键时，焦点会移到 `Target` 属性所指定的控件上。正因如此，构建无障碍表单时 `Label` 尤其好用——每个输入框都能配一段对应的文字标签。

## 常用属性 {#common-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Content` | `object` | 标签中显示的内容。可以直接写成字符串，也可以绑定到视图模型的某个属性。 |
| `Target` | `IInputElement` | 标签被点击、或其访问键被按下时获得焦点的目标控件。把它设为目标控件的 `x:Name`。 |

## 基本用法 {#basic-usage}

要把 `Label` 与某个输入控件关联起来，请把 `Target` 属性设为该输入控件的名称。用户点击标签文字时，焦点就会移到目标上：

```xml
<StackPanel Spacing="4">
    <Label Target="nameBox" Content="Name" />
    <TextBox x:Name="nameBox" />
</StackPanel>
```

## 访问键 {#access-keys}

在 `Content` 字符串中某个字符前加一个下划线（`_`），即可定义一个键盘快捷键（访问键）。字母、数字和带重音符号的字符都支持。用户按下 Alt 加该字符时，焦点就会移到目标控件上：

```xml
<StackPanel Spacing="4">
    <Label Target="nameBox" Content="_Name" />
    <TextBox x:Name="nameBox" />

    <Label Target="emailBox" Content="_Email" />
    <TextBox x:Name="emailBox" />
</StackPanel>
```

在上面的例子中，按 Alt+N 会聚焦到姓名 `TextBox`，按 Alt+E 则聚焦到邮箱 `TextBox`。

:::tip
同一个视图内的访问键字符要各不相同，免得冲突。用户按下 Alt 键时，带下划线的那个字符会显示出来作为提示。
:::

## 绑定内容 {#binding-content}

你可以把 `Content` 属性绑定到视图模型的某个属性，让标签文字随之动态更新：

```xml
<Label Target="quantityBox" Content="{Binding QuantityLabel}" />
<NumericUpDown x:Name="quantityBox" Value="{Binding Quantity}" />
```

```csharp
public string QuantityLabel => "Quantity";
```

## 构建无障碍表单 {#building-accessible-forms}

`Label` 控件是无障碍表单的关键积木。为每个输入框配一个带 `Target` 的 `Label`，用户就有两种方式聚焦到该字段：点击标签，或按下它的访问键。下面这个例子给出了一份完整的表单布局：

```xml
<Grid ColumnDefinitions="Auto,*" RowDefinitions="Auto,Auto,Auto" Margin="8">
    <Label Grid.Row="0" Grid.Column="0" Target="firstNameBox" Content="_First name" Margin="0,0,8,4" />
    <TextBox Grid.Row="0" Grid.Column="1" x:Name="firstNameBox" />

    <Label Grid.Row="1" Grid.Column="0" Target="lastNameBox" Content="_Last name" Margin="0,0,8,4" />
    <TextBox Grid.Row="1" Grid.Column="1" x:Name="lastNameBox" />

    <Label Grid.Row="2" Grid.Column="0" Target="ageBox" Content="_Age" Margin="0,0,8,4" />
    <NumericUpDown Grid.Row="2" Grid.Column="1" x:Name="ageBox" />
</Grid>
```

## Label 与 TextBlock 的取舍 {#label-vs-textblock}

| 特性 | `Label` | `TextBlock` |
|---|---|---|
| 转移焦点 | 支持（通过 `Target`） | No |
| 支持访问键 | Yes | No |
| 富文本格式 | No | 支持（通过 `Inlines`） |
| 典型用途 | 表单字段标签 | 显示文字、段落 |

在表单中需要无障碍和键盘导航能力时，用 `Label`；只是单纯显示文字、不需要转移焦点时，用 `TextBlock`。

## 另请参阅 {#see-also}

- [TextBlock](/controls/data-display/text-display/textblock)
- [SelectableTextBlock](/controls/data-display/text-display/selectabletextblock)
- [Label API 参考](/api/avalonia/controls/label)
- [GitHub 上的 `Label.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Label.cs)
