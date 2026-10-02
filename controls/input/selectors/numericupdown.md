---
id: numericupdown
title: NumericUpDown
description: 一个控件：用微调按钮、键盘方向键或鼠标滚轮输入并调整数值。
doc-type: reference
---

`NumericUpDown` 是一个可编辑的数值输入框，旁边带有上下微调按钮。输入中的非数字字符会被忽略。点击微调按钮、按键盘方向键、滚动鼠标滚轮，都可以改变数值。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Value` | `decimal?` | 获取或设置当前的数值。 |
| `Increment` | `decimal` | 微调按钮、键盘方向键和鼠标滚轮每次调整的步长，默认值为 `1`。 |
| `Minimum` | `decimal?` | 允许的最小值。 |
| `Maximum` | `decimal?` | 允许的最大值。 |
| `FormatString` | `string` | 应用于所显示数值的格式字符串。用了自定义步长时，这一项尤为重要。 |
| `ButtonSpinnerLocation` | `Location` | 微调按钮的位置：`Left` 或 `Right`（默认）。 |
| `AllowSpin` | `bool` | 是否允许通过微调按钮、键盘和鼠标滚轮增减数值，默认值为 `true`。 |
| `ShowButtonSpinner` | `bool` | 微调按钮是否可见，默认值为 `true`。 |
| `InnerLeftContent` | `object` | 显示在输入区左侧内部的内容（比如货币符号）。 |
| `InnerRightContent` | `object` | 显示在输入区右侧内部的内容（比如单位标签）。 |

## 示例 {#examples}

这是一个不限定取值范围的基础示例：

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Margin="20">
  <TextBlock Margin="0 5">Number of items:</TextBlock>
  <NumericUpDown Value="10" />
</StackPanel>
```

</XamlPreview>

### 自定义步长与取值范围 {#custom-increment-and-range}

`Value`、`Minimum`、`Maximum` 和 `Increment` 属性都是可空的 decimal，因此需要时可以自定义小数范围和步长。

:::info
用了自定义的小数步长和范围后，别忘了设置 `FormatString` 属性，否则显示出来的值可能达不到你预期的精度。
:::

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Margin="20">
  <TextBlock Margin="0 5">Opacity:</TextBlock>
  <NumericUpDown Value="0.5" Increment="0.05"
      FormatString="0.00"
      Minimum="0" Maximum="1"/>
</StackPanel>
```

</XamlPreview>

### 隐藏微调按钮 {#hiding-the-spinner-buttons}

若只想要一个不带微调按钮的普通数值文本框，请把 `ShowButtonSpinner` 设为 `False`。再配上 `AllowSpin="False"`，还能一并禁止用键盘和鼠标滚轮改值。

```xml
<NumericUpDown Value="42"
               ShowButtonSpinner="False"
               AllowSpin="False" />
```

### 添加前缀或后缀 {#adding-a-prefix-or-suffix}

用 `InnerLeftContent` 和 `InnerRightContent` 可以在输入区内显示货币符号、单位之类的标签。

```xml
<NumericUpDown Value="9.99" Increment="0.01" FormatString="0.00">
  <NumericUpDown.InnerLeftContent>
    <TextBlock Text="$" VerticalAlignment="Center" />
  </NumericUpDown.InnerLeftContent>
</NumericUpDown>
```

### 绑定到视图模型 {#binding-to-a-view-model}

可以把 `Value`、`Minimum` 和 `Maximum` 绑定到视图模型的属性上。由于 `Value` 是可空的 `decimal`，视图模型中的属性类型也要与之匹配。

```xml
<NumericUpDown Value="{Binding Quantity}"
               Minimum="1" Maximum="{Binding MaxQuantity}" />
```

```csharp
[ObservableProperty]
private decimal? _quantity = 1;

[ObservableProperty]
private decimal? _maxQuantity = 100;
```

:::caution
把控件文本框中的内容全部清空，可能会引发绑定异常。如何避免，请参阅[疑难排查页面](/troubleshooting/controls/numericupdown)。
:::

## 实用提示 {#practical-notes}

- 若用户键入的值超出 `Minimum`/`Maximum` 范围，控件会在失去焦点时把它钳制到最近的边界值。
- 把 `Value` 设为 `null` 会清空输入。要表示「尚未设定」的状态时，这很有用。
- `FormatString` 属性接受标准的 .NET 数值格式字符串。比如 `"C2"` 把值显示为保留两位小数的货币，`"P0"` 则把它显示为不带小数的百分数。

## 另请参阅 {#see-also}

- [Slider](/controls/input/selectors/slider)
- [TextBox](/controls/input/text-input/textbox)
- [绑定到控件](/docs/data-binding/binding-to-controls)
- [NumericUpDown 疑难排查](/troubleshooting/controls/numericupdown)
- [NumericUpDown API Reference](/api/avalonia/controls/numericupdown)
- [`NumericUpDown.cs` 在 GitHub 上的源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/NumericUpDown/NumericUpDown.cs)
