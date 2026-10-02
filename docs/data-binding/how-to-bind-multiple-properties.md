---
id: how-to-bind-multiple-properties
title: 如何同时绑定多个属性
description: 把多个视图模型属性绑定到控件，并用多值转换器把它们合成一个结果。
doc-type: how-to
---

import MultiBindingRgbScreenshot from '/img/guides/data/multibinding-rgb.gif';

当一个目标属性的取值同时取决于多个来源时，可以用 [`MultiBinding`](/api/avalonia/data/multibinding) 把多个 `Binding` 聚合起来，再通过 [`IMultiValueConverter`](/api/avalonia/data/converters/imultivalueconverter) 产出合成结果。只要其中任一绑定属性发出变更通知，转换器的 `Convert` 方法就会重新运行，目标属性因此始终保持同步。

和普通的 `Binding` 一样，`MultiBinding` 可以用于视图模型属性、具名控件以及其他各种绑定源。

:::caution
`MultiBinding` 只支持 `BindingMode.OneTime` 和 `BindingMode.OneWay`。双向多重绑定是不支持的 —— 把一次多值转换反推回各个源值，并没有通用的办法。
:::

## 前置条件 {#prerequisites}

开始之前，请先熟悉：

- [数据绑定语法](/docs/data-binding/data-binding-syntax)以及 `Binding` 表达式的工作方式。
- 如何用 `x:Key` 在 XAML 中声明资源，以便通过 `StaticResource` 引用转换器。

## Understand `IMultiValueConverter`

`IMultiValueConverter` 与 `IValueConverter` 类似，区别在于它接收的是一组值而不是单个值。它没有 `ConvertBack` 方法，因为聚合运算通常不可逆。

```csharp
public interface IMultiValueConverter
{
    object? Convert(IList<object?> values, Type targetType, object? parameter, CultureInfo culture);
}
```

你的转换器会收到：

| 参数 | 用途 |
|---|---|
| `values` | 各个子 `Binding` 的当前值，顺序与声明顺序一致。 |
| `targetType` | 目标属性的类型（例如 `IBrush` 或 `string`）。 |
| `parameter` | 来自 `ConverterParameter` 的可选值。 |
| `culture` | 绑定引擎传入的区域性信息。 |

:::tip
初始化期间，`values` 中可能有若干项为 `UnsetValueType`，因为那些绑定还没解析完。处理之前务必先做判断。
:::

## 把 RGB 滑块绑定到前景画刷 {#bind-rgb-sliders-to-a-foreground-brush}

下面这个示例把三个 `NumericUpDown` 控件（红、绿、蓝三个通道）绑定到 `TextBlock` 的 `Foreground` 上，实时预览合成出来的颜色。

### 第 1 步：编写 XAML 布局 {#step-1-define-the-xaml-layout}

`MultiBinding` 的子绑定必须用属性元素语法，所以每个 `<Binding>` 元素都要显式写出来。用 `ElementName` 指向那几个具名的 `NumericUpDown` 控件。

```xml title="MainWindow.axaml"
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:local="clr-namespace:ExampleApp">

    <Window.Resources>
        <local:RgbToBrushMultiConverter x:Key="RgbToBrushMultiConverter" />
    </Window.Resources>

    <StackPanel HorizontalAlignment="Center" VerticalAlignment="Center" Spacing="8">
        <NumericUpDown x:Name="red" Minimum="0" Maximum="255" Increment="20" Value="0" Foreground="Red" />
        <NumericUpDown x:Name="green" Minimum="0" Maximum="255" Increment="20" Value="0" Foreground="Green" />
        <NumericUpDown x:Name="blue" Minimum="0" Maximum="255" Increment="20" Value="0" Foreground="Blue" />

        <TextBlock Text="MultiBinding Text Color!" FontSize="24">
            <TextBlock.Foreground>
                <MultiBinding Converter="{StaticResource RgbToBrushMultiConverter}">
                    <Binding Path="Value" ElementName="red" />
                    <Binding Path="Value" ElementName="green" />
                    <Binding Path="Value" ElementName="blue" />
                </MultiBinding>
            </TextBlock.Foreground>
        </TextBlock>
    </StackPanel>
</Window>
```

### 第 2 步：实现转换器 {#step-2-implement-the-converter}

务必仔细做类型判断。`NumericUpDown.Value` 是 `decimal?`，所以转换器要能应付 `decimal`、`null` 和 `UnsetValueType`。对尚未解析出来的值一律返回 `BindingOperations.DoNothing`，这样在绑定初始化期间，目标属性会保留原来的值。

```csharp title="RgbToBrushMultiConverter.cs"
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using Avalonia.Data;
using Avalonia.Data.Converters;
using Avalonia.Media;
using Avalonia.Media.Immutable;

public sealed class RgbToBrushMultiConverter : IMultiValueConverter
{
    public object? Convert(IList<object?> values, Type targetType, object? parameter, CultureInfo culture)
    {
        // Ensure all bindings are provided and the target type is compatible
        if (values?.Count != 3 || !targetType.IsAssignableFrom(typeof(ImmutableSolidColorBrush)))
            throw new NotSupportedException();

        // Ensure all bindings are the correct type
        if (!values.All(x => x is decimal or UnsetValueType or null))
            throw new NotSupportedException();

        // Return DoNothing while any binding is still unresolved
        if (values[0] is not decimal r ||
            values[1] is not decimal g ||
            values[2] is not decimal b)
            return BindingOperations.DoNothing;

        byte a = 255;
        var color = new Color(a, (byte)r, (byte)g, (byte)b);
        return new ImmutableSolidColorBrush(color);
    }
}
```

### 第 3 步：运行程序 {#step-3-run-the-application}

拖动三个滑块中的任意一个，文字颜色都会立即跟着变化：

<Image light={MultiBindingRgbScreenshot} alt="App showing RGB sliders bound to multiple properties producing a combined color" position="center" maxWidth={400} cornerRadius="true"/>

## 用 `FuncMultiValueConverter` 简化写法 {#simplify-with-funcmultivalueconverter}

对于逻辑简单的转换，不必专门写一个类。Avalonia 的 `FuncMultiValueConverter<TIn, TOut>` 允许你直接用 lambda 定义转换逻辑。把转换器暴露成静态属性，XAML 里就能用 `x:Static` 引用它。

```csharp title="Converters.cs"
using System.Linq;
using Avalonia.Data.Converters;

public static class Converters
{
    public static readonly FuncMultiValueConverter<string, string> FullName =
        new(parts => string.Join(" ", parts.Where(p => !string.IsNullOrEmpty(p))));
}
```

```xml title="Usage in AXAML"
<TextBlock>
    <TextBlock.Text>
        <MultiBinding Converter="{x:Static local:Converters.FullName}">
            <Binding Path="FirstName" />
            <Binding Path="LastName" />
        </MultiBinding>
    </TextBlock.Text>
</TextBlock>
```

这种写法省掉了资源声明，也让简单的转换器待在它被用到的地方附近。

## 小贴士 {#tips}

- **把转换器注册为资源** —— 如果你打算用 `StaticResource` 引用它的话；或者把它暴露成 `static` 字段并改用 `x:Static`，彻底省掉资源查找。
- 转换器暂时产不出有效结果时，**请返回 `BindingOperations.DoNothing`** 而不是 `null`。这会告诉绑定引擎：保持目标属性不变。
- 当同一套 `MultiBinding` 写法要在很多地方重复使用时，**不妨考虑写一个 `MarkupExtension`** 来简化 XAML。

## 另请参阅 {#see-also}

- [MultiBinding](/docs/data-binding/multi-binding)：`MultiBinding` 的完整参考，包含 `StringFormat`、`FallbackValue` 以及属性一览表。
- [如何创建自定义数据绑定转换器](/docs/data-binding/how-to-create-a-custom-data-binding-converter)：单值 `IValueConverter` 的实现方式。
- [内置数据绑定转换器](/docs/data-binding/built-in-data-binding-converters)：Avalonia 自带的转换器。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定参数，包括 `StringFormat` 和 `ConverterParameter`。
