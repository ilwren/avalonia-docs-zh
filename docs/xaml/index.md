---
id: index
title: XAML 参考
---

本章是 Avalonia 中可用的 XAML 语言特性参考。基本概念已在 [Avalonia XAML 基础](/docs/fundamentals/avalonia-xaml)一文中讲过，这里则深入语法、指令、标记扩展以及 XAML 编译流程。

## 什么是 XAML？ {#what-is-xaml}

XAML（eXtensible Application Markup Language，可扩展应用程序标记语言）是一种基于 XML、用于声明对象图的语言。在 Avalonia 中，XAML 用来以声明的方式定义用户界面：每个 XML 元素对应一个 .NET 对象，XML 特性则为这些对象设置属性。

Avalonia 用 `.axaml` 作为文件扩展名（Avalonia XAML），以便和 WPF 或其他 XAML 方言的文件区分开，避免在 Visual Studio 等工具中产生冲突。

## XAML 语法 {#xaml-syntax}

### 对象元素 {#object-elements}

一个 XML 元素就创建一个该类型的实例：

```xml
<Button />
<TextBlock />
<StackPanel />
```

### 属性特性 {#property-attributes}

用 XML 特性设置属性：

```xml
<Button Content="Click me" Width="200" Background="Blue" />
```

XAML 引擎借助[类型转换器](/docs/xaml/type-converters)把特性里的字符串转换成相应的 .NET 类型（例如 `"Blue"` 变成 `SolidColorBrush`）。

### 属性元素语法 {#property-element-syntax}

对于无法用字符串表达的复杂值，改用属性元素语法：

```xml
<Button>
    <Button.Background>
        <LinearGradientBrush StartPoint="0%,0%" EndPoint="100%,100%">
            <GradientStop Color="Red" Offset="0" />
            <GradientStop Color="Blue" Offset="1" />
        </LinearGradientBrush>
    </Button.Background>
    <Button.Content>
        <StackPanel Orientation="Horizontal">
            <Image Source="/Assets/icon.png" Width="16" Height="16" />
            <TextBlock Text="Click me" Margin="4,0,0,0" />
        </StackPanel>
    </Button.Content>
</Button>
```

### 内容属性 {#content-property}

许多控件都指定了一个默认的内容属性。直接写在控件标签内部的子元素，就会被赋给该属性：

```xml
<!-- These are equivalent -->
<Button>Click me</Button>
<Button Content="Click me" />
```

```xml
<!-- StackPanel's content property is Children -->
<StackPanel>
    <TextBlock Text="First" />
    <TextBlock Text="Second" />
</StackPanel>
```

### 集合语法 {#collection-syntax}

集合类型的属性可以用多个子元素来填充：

```xml
<Grid.ColumnDefinitions>
    <ColumnDefinition Width="Auto" />
    <ColumnDefinition Width="*" />
    <ColumnDefinition Width="200" />
</Grid.ColumnDefinitions>
```

有些集合属性还支持紧凑的字符串写法：

```xml
<Grid ColumnDefinitions="Auto,*,200" RowDefinitions="Auto,*" />
```

### 附加属性语法 {#attached-property-syntax}

用 `OwnerType.PropertyName` 这种写法设置附加属性：

```xml
<Grid>
    <Button Grid.Row="0" Grid.Column="1" Content="Cell (0,1)" />
</Grid>
```

## Topics

- [命名空间](/docs/xaml/namespaces)：XAML 命名空间的工作方式，以及如何引用自己的类型。
- [x: 指令](/docs/xaml/directives)：`x:Name`、`x:Key`、`x:Class`、`x:DataType` 等指令的参考。
- [标记扩展](/docs/xaml/markup-extensions)：`{Binding}`、`{StaticResource}`、`{DynamicResource}`、`{TemplateBinding}` 等扩展的参考。
- [类型转换器](/docs/xaml/type-converters)：XAML 中的字符串值如何转换成 .NET 类型。

## 另请参阅 {#see-also}

- [Avalonia XAML](/docs/fundamentals/avalonia-xaml)：XAML 基础与文件结构。
- [数据绑定](/docs/data-binding/introduction-to-data-binding)：数据绑定参考。
- [样式](/docs/styling/styles)：Avalonia 中类 CSS 的样式机制。
