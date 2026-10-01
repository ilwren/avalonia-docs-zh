---
id: directives
title: "x: 指令"
---

XAML 指令是 `x:` 命名空间下的一组特殊特性，用来控制 XAML 引擎如何处理元素。它们属于 XAML 语言规范的一部分，并不针对某个具体控件。

要使用这些指令，需要先声明 XAML 语言命名空间：

```xml
xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
```

## `x:Class`

把 XAML 文件与它的代码隐藏类关联起来。该指令必须写在 XAML 文件的根元素上。

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="MyApp.MainWindow">
</Window>
```

所指定的类必须是 `partial` 类，且继承自根元素的类型：

```csharp
namespace MyApp;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }
}
```

## `x:Name`

为元素取个名字，并在代码隐藏类中生成相应字段，于是你可以在 C# 里引用该控件。

```xml
<TextBox x:Name="SearchBox" PlaceholderText="Search..." />
<Button Content="Search" Click="OnSearchClick" />
```

```csharp
private void OnSearchClick(object? sender, RoutedEventArgs e)
{
    var query = SearchBox.Text;
    // Use the named control
}
```

:::info
对大多数 Avalonia 控件而言，`x:Name` 和 `Name` 可以互换使用：`StyledElement` 上的 `Name` 属性设置的是同一个底层值。当元素类型本身没有 `Name` 属性时，就用 `x:Name`。
:::

## `x:Key`

为资源指定字典键，用在 `ResourceDictionary`、`Styles` 或 `Application.Resources` 中：

```xml
<Application.Resources>
    <SolidColorBrush x:Key="PrimaryBrush" Color="#1976D2" />
    <x:Double x:Key="DefaultSpacing">8</x:Double>
</Application.Resources>
```

取用资源时用 `{StaticResource}` 或 `{DynamicResource}`：

```xml
<Border Background="{StaticResource PrimaryBrush}" Padding="{StaticResource DefaultSpacing}" />
```

## `x:DataType`

指定某个作用域内数据绑定所期望的数据类型。[编译绑定](/docs/data-binding/compiled-bindings)必须有它，它也让绑定路径获得 IntelliSense 支持。

```xml
<Window x:DataType="vm:MainWindowViewModel">
    <TextBlock Text="{Binding UserName}" />
</Window>
```

在 `DataTemplate` 上：

```xml
<DataTemplate x:DataType="vm:TodoItemViewModel">
    <StackPanel>
        <CheckBox IsChecked="{Binding IsComplete}" />
        <TextBlock Text="{Binding Title}" />
    </StackPanel>
</DataTemplate>
```

## `x:CompileBindings`

为作用域内的所有绑定启用或关闭编译绑定。编译绑定会在编译期得到校验，性能也更好。

```xml
<UserControl x:CompileBindings="True"
             x:DataType="vm:MyViewModel">
    <!-- All bindings here are compiled -->
    <TextBlock Text="{Binding Name}" />
</UserControl>
```

也可以在项目文件中全局设置：

```xml
<AvaloniaUseCompiledBindingsByDefault>true</AvaloniaUseCompiledBindingsByDefault>
```

若想让某个绑定单独退出编译绑定，用 `ReflectionBinding`：

```xml
<TextBlock Text="{ReflectionBinding DynamicProperty}" />
```

## `x:Static`

引用静态字段、属性、常量或枚举值：

```xml
<TextBlock Text="{x:Static sys:Environment.MachineName}" />

<Rectangle Fill="{x:Static Brushes.Red}" />

<Border Width="{x:Static local:Constants.DefaultWidth}" />
```

引用枚举值：

```xml
<ComboBox SelectedItem="{x:Static local:Priority.High}" />
```

## `x:Type`

引用一个 `System.Type` 对象：

```xml
<Style Selector="Button">
    <Setter Property="Tag" Value="{x:Type Button}" />
</Style>
```

## `x:Null`

把属性设为 `null`：

```xml
<Button Background="{x:Null}" Content="No background" />
```

## `x:True` and `x:False`

布尔值的简写形式。它们是 Avalonia 特有的扩展：

```xml
<CheckBox IsChecked="{x:True}" />
<TextBox IsReadOnly="{x:False}" />
```

它们等价于：

```xml
<CheckBox IsChecked="True" />
<TextBox IsReadOnly="False" />
```

## `x:Shared`

控制资源是只实例化一次反复复用，还是每次引用都重新创建。资源默认是共享的（每次都返回同一个实例）。设置 `x:Shared="False"` 可让每次引用都新建一个实例：

```xml
<Application.Resources>
    <ColumnDefinitions x:Key="TwoColumnLayout" x:Shared="False">
        <ColumnDefinition Width="*" />
        <ColumnDefinition Width="Auto" />
    </ColumnDefinitions>
</Application.Resources>
```

若不加 `x:Shared="False"`，把同一个 `ColumnDefinitions` 资源赋给多个 `Grid` 控件会失败 —— 单个实例不可能有多个父级。

:::info
`x:Shared` 只对 `ResourceDictionary` 中的资源有效，在资源定义之外不起作用。
:::

## 基元类型元素 {#primitive-type-elements}

XAML 语言命名空间为常见的 .NET 基元类型提供了对应的元素：

```xml
<x:String>Hello World</x:String>
<x:Double>3.14</x:Double>
<x:Int32>42</x:Int32>
<x:Boolean>True</x:Boolean>
```

它们在定义资源时很有用：

```xml
<Application.Resources>
    <x:Double x:Key="HeaderFontSize">24</x:Double>
    <x:String x:Key="AppTitle">My Application</x:String>
</Application.Resources>
```

## 另请参阅 {#see-also}

- [XAML 参考](/docs/xaml)：XAML 语法总览。
- [命名空间](/docs/xaml/namespaces)：XAML 命名空间的工作方式。
- [标记扩展](/docs/xaml/markup-extensions)：`{Binding}`、`{StaticResource}` 及其他扩展。
- [编译绑定](/docs/data-binding/compiled-bindings)：编译绑定的工作原理。
