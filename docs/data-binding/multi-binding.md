---
id: multi-binding
title: MultiBinding
description: 用 MultiBinding 和 IMultiValueConverter 把多个绑定源合成一个值。
doc-type: how-to
---

[`MultiBinding`](/api/avalonia/data/multibinding) 可以把多个源属性的值合成到一个目标属性上。当某个显示值取决于不止一个数据源时它就很有用，比如把分开的姓和名拼成全名，或者算出一个复合值。

## 搭配 StringFormat 的基本用法 {#basic-usage-with-stringformat}

`MultiBinding` 最简单的用法，就是把多个值拼成一个格式化字符串：

```xml
<TextBlock>
    <TextBlock.Text>
        <MultiBinding StringFormat="{}{0} {1}">
            <Binding Path="FirstName" />
            <Binding Path="LastName" />
        </MultiBinding>
    </TextBlock.Text>
</TextBlock>
```

`MultiBinding` 内部的每个 `Binding` 依次对应 `StringFormat` 模式里的一个占位符（`{0}`、`{1}` 等等）。格式字符串遵循 .NET `string.Format` 的标准规则。

### 格式化数字 {#formatting-numbers}

```xml
<TextBlock>
    <TextBlock.Text>
        <MultiBinding StringFormat="Total: {0:C2} ({1} items)">
            <Binding Path="TotalPrice" />
            <Binding Path="ItemCount" />
        </MultiBinding>
    </TextBlock.Text>
</TextBlock>
```

:::tip
当 `StringFormat` 以 `{0` 开头时，必须转义最前面的花括号：在模式前加上 `{}`，或者用反斜杠转义 —— `StringFormat='\{0\} items'`。
:::

## 使用 IMultiValueConverter {#using-an-imultivalueconverter}

若逻辑超出了字符串格式化的范畴，就实现 `IMultiValueConverter`。该转换器会收到一个数组，里面装着所有子绑定的值，最终返回单个结果。

### 定义转换器 {#defining-the-converter}

```csharp
using System;
using System.Collections.Generic;
using System.Globalization;
using Avalonia.Data.Converters;

public class AllTrueConverter : IMultiValueConverter
{
    public object? Convert(
        IList<object?> values,
        Type targetType,
        object? parameter,
        CultureInfo culture)
    {
        foreach (var value in values)
        {
            if (value is not true)
                return false;
        }
        return true;
    }
}
```

### 在 XAML 中使用该转换器 {#using-the-converter-in-xaml}

先把转换器声明为资源，再在 `MultiBinding` 中引用它：

```xml
<Window.Resources>
    <local:AllTrueConverter x:Key="AllTrue" />
</Window.Resources>

<Button Content="Submit"
        IsEnabled="{MultiBinding Converter={StaticResource AllTrue}}">
    <!-- Intentionally empty: MultiBinding must use property element syntax
         for child bindings. See below for the full form. -->
</Button>
```

由于带子绑定的 `MultiBinding` 必须使用属性元素语法，完整写法是：

```xml
<Button Content="Submit">
    <Button.IsEnabled>
        <MultiBinding Converter="{StaticResource AllTrue}">
            <Binding Path="IsFormValid" />
            <Binding Path="HasAcceptedTerms" />
            <Binding Path="IsNotBusy" />
        </MultiBinding>
    </Button.IsEnabled>
</Button>
```

只有当三个绑定属性全都为 `true` 时，按钮才可用。

## 绑定到控件 {#binding-to-controls}

`MultiBinding` 内部的子绑定支持与普通绑定相同的各种源选项，包括 `ElementName`、`RelativeSource` 以及 Avalonia 的 `#elementName` 简写：

```xml
<StackPanel>
    <NumericUpDown x:Name="width" Value="100" Minimum="0" Maximum="500" />
    <NumericUpDown x:Name="height" Value="50" Minimum="0" Maximum="500" />

    <TextBlock>
        <TextBlock.Text>
            <MultiBinding StringFormat="Area: {0} x {1} = {2}">
                <Binding Path="Value" ElementName="width" />
                <Binding Path="Value" ElementName="height" />
                <Binding Path="#width.Value"
                         Converter="{x:Static local:MultiplyConverter.Instance}"
                         ConverterParameter="{Binding #height.Value}" />
            </MultiBinding>
        </TextBlock.Text>
    </TextBlock>
</StackPanel>
```

## MultiBinding 的属性 {#multibinding-properties}

| 属性 | 说明 |
|---|---|
| `Bindings` | 子 `Binding` 对象的集合。 |
| `Converter` | 负责处理这些绑定值的 `IMultiValueConverter`。 |
| `ConverterParameter` | 传给转换器的参数。 |
| `StringFormat` | 未指定转换器（或转换器返回字符串）时所应用的格式字符串。 |
| `FallbackValue` | 多重绑定无法产出结果时所使用的值。 |
| `TargetNullValue` | 转换器返回 `null` 时所使用的值。 |
| `Mode` | 绑定模式。`MultiBinding` 支持 `OneWay` 和 `OneTime` 两种模式。 |
| `Priority` | 绑定优先级。 |

:::info
`MultiBinding` 默认是单向的。双向多重绑定是不支持的 —— 把一次多值转换反推回各个源属性，并没有通用的办法。
:::

:::tip
与 WPF 不同，Avalonia 支持把一个 `MultiBinding` 嵌套在另一个 `MultiBinding` 里。每个嵌套的 `MultiBinding` 会在父转换器的输入数组中归结为一个值。
:::

## FuncMultiValueConverter

对于那些不想专门写个类、只想就地定义转换逻辑的简单场景，Avalonia 提供了 `FuncMultiValueConverter<TIn, TOut>`。

转换函数收到的是一个 `IReadOnlyList<TIn>`，你可以遍历这些值，也可以按下标取用：

```csharp
public static class Converters
{
    // Iterate over all values
    public static readonly FuncMultiValueConverter<string, string> FullName =
        new(parts => string.Join(" ", parts.Where(p => !string.IsNullOrEmpty(p))));

    // Access values by index
    public static readonly FuncMultiValueConverter<string, string> FormattedName =
        new(parts => $"{parts[1]}, {parts[0]}");
}
```

```xml
<TextBlock>
    <TextBlock.Text>
        <MultiBinding Converter="{x:Static local:Converters.FullName}">
            <Binding Path="FirstName" />
            <Binding Path="MiddleName" />
            <Binding Path="LastName" />
        </MultiBinding>
    </TextBlock.Text>
</TextBlock>
```

## 常见写法 {#common-patterns}

### 由多个条件共同决定可见性 {#visibility-from-multiple-conditions}

```csharp
public class AnyTrueConverter : IMultiValueConverter
{
    public static readonly AnyTrueConverter Instance = new();

    public object? Convert(
        IList<object?> values,
        Type targetType,
        object? parameter,
        CultureInfo culture)
    {
        return values.Any(v => v is true);
    }
}
```

```xml
<Border>
    <!-- Shown when any condition is true -->
    <Border.IsVisible>
        <MultiBinding Converter="{x:Static local:AnyTrueConverter.Instance}">
            <Binding Path="HasErrors" />
            <Binding Path="HasWarnings" />
        </MultiBinding>
    </Border.IsVisible>
</Border>
```

### 由多个输入算出一个值 {#computing-a-value-from-multiple-inputs}

```csharp
public class RectangleAreaConverter : IMultiValueConverter
{
    public object? Convert(
        IList<object?> values,
        Type targetType,
        object? parameter,
        CultureInfo culture)
    {
        if (values.Count >= 2
            && values[0] is double width
            && values[1] is double height)
        {
            return width * height;
        }
        return 0.0;
    }
}
```

## 另请参阅 {#see-also}

- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定参数，含 StringFormat。
- [如何创建自定义转换器](/docs/data-binding/how-to-create-a-custom-data-binding-converter)：单值转换器。
- [内置数据绑定转换器](/docs/data-binding/built-in-data-binding-converters)：Avalonia 自带的转换器。
