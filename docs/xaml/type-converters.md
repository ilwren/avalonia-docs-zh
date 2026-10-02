---
id: type-converters
title: 类型转换器
description: XAML 类型转换器如何把特性里的字符串转换成 .NET 类型，内置转换器有哪些，以及如何编写自定义转换器。
doc-type: explanation
---

XAML 特性的值永远是字符串，类型转换器负责把它们转换成相应的 .NET 类型。当你在 XAML 中写下 `Background="Red"` 时，就是某个类型转换器把字符串 `"Red"` 变成了 [`SolidColorBrush`](/api/avalonia/media/solidcolorbrush) 对象。

## 类型转换器的工作方式 {#how-type-converters-work}

XAML 引擎遇到一个属性特性时，会：

1. 先看属性类型是否就是 `string`。若是，则直接采用原值。
2. 查找与该属性类型关联的 `TypeConverter`。
3. 用这个转换器把字符串转换成目标类型。

整个过程是自动且透明的，你不需要指定该用哪个转换器。

## 内置类型转换器 {#built-in-type-converters}

Avalonia 为许多常见类型都提供了类型转换器，其中最常用的有：

### 颜色与画刷 {#colors-and-brushes}

| String Value | 转换结果 | 示例 |
|---|---|---|
| `"Red"`, `"Blue"`, `"Green"` | `Color` / `SolidColorBrush` | 颜色名称 |
| `"#FF0000"` | `Color` / `SolidColorBrush` | Hex RGB |
| `"#80FF0000"` | `Color` / `SolidColorBrush` | Hex ARGB |
| `"#F00"` | `Color` / `SolidColorBrush` | 十六进制 RGB 简写 |

```xml
<Border Background="LightBlue" BorderBrush="#333333" />
```

### Thickness (Margins, Padding, BorderThickness)

| String Value | 结果 |
|---|---|
| `"8"` | 四边统一：各边均为 8 |
| `"8,4"` | 左右为 8，上下为 4 |
| `"4,2,4,2"` | Left, Top, Right, Bottom |

```xml
<Border Margin="8" Padding="12,6" BorderThickness="1,0,1,0" />
```

### CornerRadius

| String Value | 结果 |
|---|---|
| `"4"` | 统一的圆角半径 |
| `"4,4,0,0"` | TopLeft, TopRight, BottomRight, BottomLeft |

```xml
<Border CornerRadius="8" />
```

### GridLength (Column/Row Definitions)

| String Value | 结果 |
|---|---|
| `"Auto"` | 按内容自适应尺寸 |
| `"*"` | 按比例占据剩余空间 |
| `"2*"` | 占据两倍的比例空间 |
| `"200"` | 以设备无关像素表示的固定尺寸 |

```xml
<Grid ColumnDefinitions="200,Auto,*,2*" />
```

### Point

```xml
<Line StartPoint="0,0" EndPoint="100,50" />
```

### Size

```xml
<Viewbox MaxWidth="200" MaxHeight="150" />
```

### Uri / Bitmap

```xml
<Image Source="/Assets/logo.png" />
<Image Source="avares://MyApp/Assets/logo.png" />
```

### 枚举值 {#enum-values}

枚举属性会直接按名称字符串自动转换：

```xml
<StackPanel Orientation="Horizontal" />
<TextBlock TextAlignment="Center" FontWeight="Bold" />
<DockPanel LastChildFill="True" />
```

### Geometry (Path Data)

`Geometry` 类型转换器解析的是 SVG 风格的路径数据：

```xml
<Path Data="M 0,0 L 100,0 L 100,100 Z" Fill="Blue" />
```

路径数据的语法细节，请见[绘制图形](/docs/graphics-animation/drawing-graphics)中的几何图形参考。

### KeyGesture

```xml
<KeyBinding Gesture="Ctrl+S" Command="{Binding SaveCommand}" />
```

### TimeSpan

```xml
<Animation Duration="0:0:0.5" />
```

格式：`hours:minutes:seconds.milliseconds`

## 编写自定义类型转换器 {#creating-a-custom-type-converter}

要为自己的类型编写类型转换器，实现 `TypeConverter` 并用 `[TypeConverter]` 特性把它挂上去：

```csharp
[TypeConverter(typeof(TemperatureConverter))]
public struct Temperature
{
    public double Value { get; }
    public string Unit { get; }

    public Temperature(double value, string unit)
    {
        Value = value;
        Unit = unit;
    }
}

public class TemperatureConverter : TypeConverter
{
    public override bool CanConvertFrom(ITypeDescriptorContext? context, Type sourceType)
    {
        return sourceType == typeof(string) || base.CanConvertFrom(context, sourceType);
    }

    public override object? ConvertFrom(
        ITypeDescriptorContext? context, CultureInfo? culture, object value)
    {
        if (value is string text)
        {
            // Parse "72F" or "22C"
            var numericPart = text.TrimEnd('C', 'F', 'K');
            var unit = text[^1..];
            return new Temperature(double.Parse(numericPart, culture), unit);
        }

        return base.ConvertFrom(context, culture, value);
    }
}
```

现在就可以在 XAML 中使用该类型了：

```xml
<local:Thermostat CurrentTemperature="72F" />
```

## 另请参阅 {#see-also}

- [XAML 参考](/docs/xaml)：XAML 语法总览。
- [数据绑定转换器](/docs/data-binding/how-to-create-a-custom-data-binding-converter)：数据绑定用的值转换器（与类型转换器是两回事）。
- [内置数据绑定转换器](/docs/data-binding/built-in-data-binding-converters)：可用于绑定变换的各种转换器。
