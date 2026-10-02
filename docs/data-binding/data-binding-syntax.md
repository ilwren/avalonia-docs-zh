---
id: data-binding-syntax
title: 数据绑定语法
description: Avalonia 数据绑定标记语法参考，涵盖路径、模式、转换器与回退值。
doc-type: reference
---

import DataBindingModeDiagram from '/img/concepts/data-concepts/data-binding-syntax/data-binding-mode.png';

Avalonia 支持在 XAML 和代码中创建数据绑定。XAML 中的数据绑定一般用 `Binding` [`MarkupExtension`](/api/avalonia/markup/xaml/markupextension) 创建，也就是本文要讲的内容。若想在代码中创建数据绑定，请见[如何在代码中创建绑定](/docs/data-binding/binding-from-code)。

## 数据绑定 `MarkupExtension` {#data-binding-markupextension}

`Binding` `MarkupExtension` 以关键字 `Binding` 开头，再搭配若干可选参数来指定数据源和其他选项，如下例所示：

```xml
<SomeControl SomeProperty="{Binding Path, Mode=ModeValue, StringFormat=Pattern}" />
```

| 参数             | 说明                                                                       |
|-----------------------|-----------------------------------------------------------------------------------|
| `Path`                | 要绑定的源属性名称。                                       |
| `Mode`                | 绑定的数据同步方向。                                     |
| `Priority`            | 属性赋值的优先级。                                                  |
| `Source`              | 包含 `Path` 所指属性的那个对象。                           |
| `ElementName`         | 以某个具名 `Control` 作为 `Source`。                                           |
| `RelativeSource`      | 以视觉树层级中某个相对位置的 `Control` 作为 `Source`。       |
| `StringFormat`        | 把属性值格式化为字符串所用的模式。                               |
| `Converter`           | 负责在源值与目标值之间双向转换的 `IValueConverter`。 |
| `ConverterParameter`  | 传给 `Converter` 的参数。                                         |
| `FallbackValue`       | 当绑定无法建立、或无法产生值时所使用的值。        |
| `TargetNullValue`     | 当源属性的值为 `null` 时所使用的值。                    |
| [`UpdateSourceTrigger`](/api/avalonia/data/updatesourcetrigger) | 在满足预定义条件时触发源属性更新。            |
| `Delay`               | 源值变化后，延迟多久再更新绑定目标。 |

这些参数必须在创建绑定时就设定好。它们是 CLR 属性，无法再由其他绑定来设置或更新。

## 数据绑定路径 {#data-binding-path}

第一个参数通常就是 `Path`，即 `Source`（默认为 `DataContext`）中某个属性的名称，Avalonia 在创建绑定时会去定位它。

当 `Path=` 作为第一个参数出现时可以省略不写。下面两种写法等价：

```xml
<TextBlock Text="{Binding Name}"/>
<TextBlock Text="{Binding Path=Name}"/>
```

绑定路径可以是单个属性，也可以是一串子属性。举例来说，如果数据源有个 `Student` 属性，而该属性返回的对象又有个 `Name` 属性，那么可以这样绑定到学生的姓名：

```xml
<TextBlock Text="{Binding Student.Name}"/>
```

如果数据源支持索引（比如数组或列表），可以把索引写进绑定路径：

```xml
<TextBlock Text="{Binding Students[0].Name}"/>
```

### null 条件运算符 {#null-conditional-operator}

在绑定路径中使用 `?.` 运算符，可以安全地穿过那些可能为 `null` 的属性。路径中任意一段为 `null` 时，绑定产生一个 `null` 值，而不会抛出异常：

```xml
<TextBlock Text="{Binding SelectedStudent?.Address?.City}"/>
```

它等同于 C# 的 null 条件运算符。若不写 `?.`，当 `null` 时 `SelectedStudent` 就会产生一个绑定错误。

## 空绑定路径 {#empty-binding-path}

数据绑定也可以不写 `Path`，此时绑定的是声明该绑定的控件自身的 `DataContext`。下面两种写法等价：

```xml
<TextBlock Text="{Binding}" />
<TextBlock Text="{Binding .}" />
```

## 数据绑定模式 {#data-binding-mode}

通过指定 `Mode` 可以改变数据同步的方向。

<Image light={DataBindingModeDiagram} alt="Diagram showing data binding mode directions between source and target" position="center" maxWidth={400} cornerRadius="true"/>
<br/><br/>

例如：

```xml
<TextBlock Text="{Binding Name, Mode=OneTime}" />
```

可用的绑定模式如下：

| 模式             | 说明                                                                                                               |
|------------------|---------------------------------------------------------------------------------------------------------------------------|
| `OneWay`         | 数据源的变化会传播到绑定目标。                                                               |
| `TwoWay`         | 数据源的变化会传播到绑定目标，反之亦然。                                                |
| `OneTime`        | 数据源的值只向绑定目标传播一次。`DataContext` 变化时绑定会重新求值，但同一数据源上后续的属性变化会被忽略。 |
| `OneWayToSource` | 绑定目标的变化会传播到数据源，反向则不会。                                        |
| `Default`        | 采用该属性在代码中定义的默认模式，详见下文。                              |

未指定 `Mode` 时采用 `Default`。对于不会因用户交互而改变取值的控件属性，默认模式一般是 `OneWay`；而对于会因用户输入而改变取值的控件属性，默认模式通常是 `TwoWay`。

举例来说，`TextBlock.Text` 属性的默认模式是 `OneWay`，而 `TextBox.Text` 属性的默认模式是 `TwoWay`。

## 数据绑定源 {#data-binding-sources}

`Source` 指定 `Path` 所相对的根对象实例，默认是所在 `Control` 的 `DataContext`。最常见的场景是用 `ElementName` 或 `RelativeSource` 参数绑定到另一个控件，或者用它们在 `Path` 中的简写形式（分别是 `#controlName` 和 `$parent[ControlType]`）。

```xml
<TextBox Name="input" />
<TextBlock Text="{Binding Text, ElementName=input}" />
<TextBlock Text="{Binding #input.Text}" />

<TextBlock Text="{Binding Title, 
    RelativeSource={RelativeSource FindAncestor, AncestorType=Window}}" />
<TextBlock Text="{Binding $parent[Window].Title}" />
```

:::info
关于如何绑定到控件的更多细节，请见[如何绑定到控件](/docs/data-binding/binding-to-controls)
:::

## 转换绑定值 {#converting-bound-values}

绑定提供了多种办法，把数据绑定送来的值转换或替换成更适合目标属性的类型或取值。

### 字符串格式化 {#string-formatting}

可以给 `OneWay` 绑定设置 `StringFormat` 参数，用一个模式把绑定的源属性格式化成文本；该参数内部使用的是 `string.Format`。

模式中的索引从 0 开始，且必须写在花括号里。当花括号位于模式开头时必须转义 —— 即便它同时被包在单引号中也一样。转义方式是在模式最前面加一对空花括号，或者给每个花括号加一个反斜杠。

```xml
<TextBlock Text="{Binding FloatProperty, StringFormat={}{0:0.0}}" />
```

也可以用反斜杠来转义模式所需的花括号。例如：

```xml
<TextBlock Text="{Binding FloatProperty, StringFormat=\{0:0.0\}}" />
```

不过，如果模式不是以 0 开头，就不需要转义。另外，模式中若含有空白字符，必须用单引号把它包起来。例如：

```xml
<TextBlock Text="{Binding Animals.Count, StringFormat='I have {0} animals.'}" />
```

换句话说，只要模式是以你绑定的那个值打头，就得转义。例如：

```xml
<TextBlock Text="{Binding Animals.Count, 
    StringFormat='{}{0} animals live in the farm.'}" />
```

### 带多个参数的字符串格式化 {#string-formatting-with-multiple-parameters}

需要格式化多个绑定参数时，可以用 `MultiBinding`。下面的例子把多个数值输入拼成一个字符串显示出来。

```xml
<StackPanel Spacing="8">
  <NumericUpDown x:Name="red" Minimum="0" Maximum="255" Value="0" FormatString="{}{0:0.}" Foreground="Red" />
  <NumericUpDown x:Name="green" Minimum="0" Maximum="255" Value="0" FormatString="{}{0:0.}" Foreground="Green" />
  <NumericUpDown x:Name="blue" Minimum="0" Maximum="255" Value="0" FormatString="{}{0:0.}" Foreground="Blue" />

  <TextBlock>
    <TextBlock.Text>
      <MultiBinding StringFormat="(r: {0:0.}, g: {1:0.}, b: {2:0.})">
        <Binding Path="Value" ElementName="red" />
        <Binding Path="Value" ElementName="green" />
        <Binding Path="Value" ElementName="blue" />
      </MultiBinding>
    </TextBlock.Text>
  </TextBlock>
</StackPanel>
```

`NumericUpDown` 内部用 `FormatString` 来调整取值的显示方式。这里因为 RGB 颜色都是整数，不应显示小数部分，所以传入 .NET 认识的自定义数字格式说明符 `0.`。

若三个输入的值分别为 `red = 100`、`green = 80` 和 `blue = 255`，则显示出来的文本是 `(r: 100, g: 80, b: 255)`。

:::tip
另一种办法是用一组 `InlineCollection`，其中每个 `Run` 各自带一个单参数绑定。这样每一段的外观都能单独定制。
:::

### 内置转换 {#built-in-conversions}

Avalonia 提供了一系列内置的数据绑定转换器，包括：

* null 判定类转换器
* 布尔运算类转换器

:::info
Avalonia 内置数据绑定转换器的完整清单，请见[内置数据绑定转换器参考](/docs/data-binding/built-in-data-binding-converters)。
:::

### 自定义转换 {#custom-conversions}

如果内置转换器满足不了需求，可以实现 `IValueConverter` 来创建自定义转换器。

:::info
自定义转换器的具体写法，请见[如何创建自定义数据绑定转换器](/docs/data-binding/how-to-create-a-custom-data-binding-converter)。
:::

### FallbackValue

当属性绑定无法建立、或转换器返回 `AvaloniaProperty.UnsetValue` 时，就会使用 `FallbackValue`。

一个常见场景是子属性绑定中的父级属性为 `null`。在下面的例子里，若 `Student` 为 `null`，则使用 `FallbackValue`：

```xml
<TextBlock Text="{Binding Student.Name, FallbackValue=Cannot find name}"/>
```

:::tip
`ReflectionBinding` 可以绑定到任意类型，不受编译期安全检查的约束。当绑定无法建立时，用 `FallbackValue` 顶上会很有用。
:::

### `TargetNullValue`

当属性绑定成功建立、而属性值为 `null` 时，可以用 `TargetNullValue` 指定一个替代值。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
            Margin="10">
    <NumericUpDown x:Name="number" Value="200" />
    <TextBlock Text="{Binding #number.Value, TargetNullValue=Value is null}" />
</StackPanel>
```

</XamlPreview>

## `UpdateSourceTrigger`

像 `TextBox` 这类控件，默认每敲一个键就把 `Text` 绑定同步回源属性。某些场景下这会触发耗时任务或不必要的校验。`UpdateSourceTrigger` 让你自己决定何时同步。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui">
    <TextBlock Width="200">PropertyChanged</TextBlock>
    <TextBox Text="{Binding #propertyChanged.Text}"
             Width="200" />
    <TextBlock Name="propertyChanged"
               Width="200" />

    <TextBlock Width="200">LostFocus</TextBlock>
    <TextBox Text="{Binding #lostFocus.Text, UpdateSourceTrigger=LostFocus}"
             Width="200" />
    <TextBlock Name="lostFocus"
               Width="200" />
</StackPanel>
```

</XamlPreview>

| UpdateSourceTrigger | 说明                                                                                      |
|---------------------|--------------------------------------------------------------------------------------------------|
| `Default`           | 目前默认为 `PropertyChanged`。                                                    |
| `PropertyChanged`   | 绑定目标属性一变化，就立即更新绑定源。             |
| `LostFocus`         | 绑定目标元素失去焦点时才更新绑定源。                      |
| `Explicit`          | 仅在你调用 `BindingExpressionBase.UpdateSource()` 方法时才更新绑定源。 |

## `Delay`

_自 Avalonia 11.3 起可用_

`Delay` 参数指定源值变化后要等待多久（单位：毫秒）再更新绑定目标。源值每变化一次，延时计时器就重新开始；只有距上次变化满了指定时长，目标才会更新。这种做法通常称为「防抖」。

它在「边输入边搜索」这类场景中特别有用 —— 你不希望每敲一个键就触发一次昂贵的操作（比如筛选或请求服务）。

### XAML 用法 {#xaml-usage}

```xml
<TextBox Text="{Binding SearchText, Delay=300}" />
```

在这个例子中，视图模型上的 `SearchText` 属性只会在用户停止输入 300 毫秒之后才更新。

### 代码用法 {#code-usage}

在代码中创建绑定时，把 `Delay` 属性设为一个 `TimeSpan`：

```csharp
var binding = new Binding("SearchText")
{
    Delay = TimeSpan.FromMilliseconds(300)
};
myTextBox.Bind(TextBox.TextProperty, binding);
```

### 实例演示 {#practical-example}

下面的例子展示一个搜索用的 TextBox：它在用户停止输入 300 毫秒后才更新绑定的属性，避免每敲一个键都执行一次搜索。

```xml
<StackPanel Spacing="8">
    <TextBox PlaceholderText="Search..."
             Text="{Binding SearchText, Delay=300}" />
    <TextBlock Text="{Binding SearchResults}" />
</StackPanel>
```

```csharp
public class SearchViewModel : ObservableObject
{
    private string _searchText = string.Empty;
    private string _searchResults = string.Empty;

    public string SearchText
    {
        get => _searchText;
        set
        {
            if (SetProperty(ref _searchText, value))
            {
                // This will only be called 300ms after the user stops typing
                PerformSearch(value);
            }
        }
    }

    public string SearchResults
    {
        get => _searchResults;
        set => SetProperty(ref _searchResults, value);
    }

    private void PerformSearch(string query)
    {
        SearchResults = string.IsNullOrEmpty(query)
            ? string.Empty
            : $"Searching for: {query}";
    }
}
```

## 另请参阅 {#see-also}

- [数据上下文](/docs/data-binding/data-context)：数据绑定器从何处取得数据对象。
- [编译绑定](/docs/data-binding/compiled-bindings)：编译期的绑定校验。
- [如何创建自定义数据绑定转换器](/docs/data-binding/how-to-create-a-custom-data-binding-converter)：自定义值转换器。
