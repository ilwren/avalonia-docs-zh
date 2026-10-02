---
id: how-to-create-a-custom-data-binding-converter
title: 如何创建自定义数据绑定转换器
description: 实现 IValueConverter，在 Avalonia 绑定中对源与目标之间的数据做转换。
doc-type: how-to
---


当内置的数据绑定转换器满足不了你的转换需求时，可以基于 [`IValueConverter`](/api/avalonia/data/converters/ivalueconverter) 接口自己写一个。本文就来讲讲怎么做。

:::info
`IValueConverter` 接口的 _Microsoft_ 官方文档，见 [IValueConverter API 参考](https://docs.microsoft.com/en-gb/dotnet/api/system.windows.data.ivalueconverter?view=netframework-4.7.1)。
:::

:::info
由于 .NET Standard 2.0 中没有 `IValueConverter` 接口，Avalonia UI 在 `Avalonia.Data.Converters` 命名空间下自带了一份副本，参见 [Avalonia IValueConverter API 文档](/api/avalonia/data/converters/ivalueconverter)。
:::

自定义转换器必须先在某处资源中引用，才能使用。放在应用的哪一层都可以。本例中，自定义转换器 `myConverter` 是在窗口资源里引用的：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:local="clr-namespace:ExampleApp;assembly=ExampleApp">

  <Window.Resources>
    <local:MyConverter x:Key="myConverter"/>
  </Window.Resources>

  <TextBlock Text="{Binding Value, Converter={StaticResource myConverter}}"/>
</Window>
```

## Example

下面这个示例转换器可以根据参数把文本转换成指定的大小写形式：

```xml
<TextBlock Text="{Binding TheContent, 
    Converter={StaticResource textCaseConverter},
    ConverterParameter=lower}" />
```

上面这段 XAML 的前提是 `textCaseConverter` 已经在资源中引用过了。

```csharp
public class TextCaseConverter : IValueConverter
{
    public static readonly TextCaseConverter Instance = new();

    public object? Convert(object? value, Type targetType, object? parameter, 
                                                            CultureInfo culture)
    {
        if (value is string sourceText && parameter is string targetCase
            && targetType.IsAssignableTo(typeof(string)))
        {
            switch (targetCase)
            {
                case "upper":
                case "SQL":
                    return sourceText.ToUpper();
                case "lower":
                    return sourceText.ToLower();
                case "title": // Every First Letter Uppercase
                    var txtinfo = new System.Globalization.CultureInfo("en-US",false)
                                    .TextInfo;
                    return txtinfo.ToTitleCase(sourceText);
                default:
                    // invalid option, return the exception below
                    break;
            }
        }
        // converter used for the wrong type
        return new BindingNotification(new InvalidCastException(), 
                                                BindingErrorType.Error);
    }

    public object ConvertBack(object? value, Type targetType, 
                                object? parameter, CultureInfo culture)
    {
      throw new NotSupportedException();
    }
}
```

## 目标属性类型 {#target-property-type}

有时你希望转换器能根据目标属性的需要切换输出类型。这是可以做到的 —— `Convert` 方法会收到一个 `targetType` 参数，用 `IsAssignableTo` 函数判断它即可。

在这个例子中，`animalConverter` 可以为绑定的 `Animal` 类对象取到一张图片，也可以取到一段文字名称：  

```xml title='XAML'
<Image Width="42" 
       Source="{Binding Animal, Converter={StaticResource animalConverter}}"/>
<TextBlock 
       Text="{Binding Animal, Converter={StaticResource animalConverter}}" />
```

```csharp title='AnimalConverter.cs'
public class AnimalConverter : IValueConverter
{
    public static readonly AnimalConverter Instance = new();

    public object? Convert( object? value, Type targetType, 
                                    object? parameter, CultureInfo culture )
    {
        if (value is Animal animal)
        {
            if (targetType.IsAssignableTo(typeof(IImage)))
            {
                img = @"icons/generic-animal-placeholder.png"
                switch (animal)
                {
                    case Dog d:
                      img = d.IsGoodBoy ? @"icons/dog-happy.png" 
                                                      : @"icons/dog.png";
                      break;
                    case Cat:
                      img = @"icons/cat.png";
                      break;
                    // other animal types
                }
                // see https://docs.avaloniaui.net/docs/guides/data-binding/how-to-create-a-custom-data-binding-converter
                return BitmapAssetValueConverter.Instance
                    .Convert(img, typeof(Bitmap), parameter, culture);
            }
            else if (targetType.IsAssignableTo(typeof(string)))
            {
                return !string.IsNullOrEmpty(animal.NickName) ? 
                    $"{animal.Name} \"{animal.NickName}\"" : animal.Name;
            }
        }
        // converter used for the wrong type
        return new BindingNotification(new InvalidCastException(), 
                                                    BindingErrorType.Error);
        
    }

    public object ConvertBack( object? value, Type targetType, 
                                    object? parameter, CultureInfo culture )
    {
      throw new NotSupportedException();
    }
}
```

## FuncValueConverter 与 FuncMultiConverter {#funcvalueconverter-and-funcmulticonverter}

你也可以实现 `FuncValueConverter`。`FuncValueConverter` 带两个或三个泛型参数：

* **TIn**：指定期望的输入类型。如果想把该转换器用在 MultiBinding 中，这里也可以是数组。

* **TParam**（可选）：指定传入的 `Binding.ConverterParameter` 的类型。

* **TOut**：指定期望的输出类型。


### 单向绑定示例 {#one-way-example}

```csharp
public static class MyConverters
{
    public static FuncValueConverter<decimal?, string> MyConverter { get; } =
        new FuncValueConverter<decimal?, string>(num => $"Your number is: '{num}'");

    public static FuncMultiValueConverter<decimal?, string> MyMultiConverter { get; } =
        new FuncMultiValueConverter<decimal?, string>(num => $"Your numbers are: '{string.Join(", ", num)}'");
}
```

### 双向绑定示例 {#two-way-example}

传入一个可选的 `convertBack` 函数即可支持双向绑定：

```csharp
public static class MyConverters
{
    public static FuncValueConverter<double, string> TemperatureConverter { get; } =
        new(
            celsius => $"{celsius:F1} °C",
            text => double.TryParse(text?.Replace(" °C", ""), out var c) ? c : 0
        );
}
```

```xml
<StackPanel>
    <!-- Input -->
    <NumericUpDown x:Name="Num1" Value="3" />
    <NumericUpDown x:Name="Num2" Value="3" />
    <!-- Output -->
    <TextBlock Text="{Binding #Num1.Value, Converter={x:Static my:MyConverters.MyConverter}}" />
    <TextBlock>
        <TextBlock.Text>
            <MultiBinding Converter="{x:Static my:MyConverters.MyMultiConverter}">
                <Binding Path="#Num1.Value" />
                <Binding Path="#Num2.Value" />
            </MultiBinding>
        </TextBlock.Text>
    </TextBlock>
</StackPanel>
```

## 更多信息 {#more-information}

:::info
关于绑定图片的更多说明，请见[如何绑定图片文件](/docs/data-binding/how-to-bind-image-files)。
:::
