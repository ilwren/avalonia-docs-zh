---
id: generics
title: XAML 中的泛型类型
description: '借助 x:TypeArguments 指令，在 Avalonia XAML 中使用泛型 .NET 类型，包括泛型集合和自定义控件。'
doc-type: explanation
---

Avalonia 通过 `x:TypeArguments` 指令支持在 XAML 中使用泛型 .NET 类型。于是你可以直接在标记里实例化泛型类、使用泛型集合。

## `x:TypeArguments`

`x:TypeArguments` 指令用于指定泛型类型的类型参数。它只能用在 XAML 文件的根元素上，或者同时带有 `x:Class` 的元素上，又或者资源字典内部的元素上。

### 基本语法 {#basic-syntax}

```xml
<local:MyGenericControl x:TypeArguments="x:String" />
```

### 多个类型参数 {#multiple-type-arguments}

多个类型参数之间用逗号分隔：

```xml
<local:Pair x:TypeArguments="x:String, x:Int32" />
```

## 在资源中使用泛型集合 {#using-generic-collections-in-resources}

泛型集合可以定义成资源：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:sys="using:System"
        xmlns:scg="using:System.Collections.Generic">

    <Window.Resources>
        <scg:List x:Key="Colors" x:TypeArguments="sys:String">
            <sys:String>Red</sys:String>
            <sys:String>Blue</sys:String>
            <sys:String>Green</sys:String>
        </scg:List>
    </Window.Resources>

    <ListBox ItemsSource="{StaticResource Colors}" />
</Window>
```

## 泛型自定义控件 {#generic-custom-controls}

编写泛型自定义控件时，先在 C# 中定义类型参数：

```csharp
public class TypedList<T> : ItemsControl
{
    public static readonly StyledProperty<T?> SelectedValueProperty =
        AvaloniaProperty.Register<TypedList<T>, T?>(nameof(SelectedValue));

    public T? SelectedValue
    {
        get => GetValue(SelectedValueProperty);
        set => SetValue(SelectedValueProperty, value);
    }
}
```

在 XAML 中配合 `x:TypeArguments` 使用它：

```xml
<local:TypedList x:TypeArguments="vm:Person" ItemsSource="{Binding People}" />
```

## XAML 中常见的泛型类型 {#common-generic-types-in-xaml}

| 类型 | XAML Prefix | 示例 |
|---|---|---|
| `System.String` | `x:String` | `x:TypeArguments="x:String"` |
| `System.Int32` | `x:Int32` | `x:TypeArguments="x:Int32"` |
| `System.Double` | `x:Double` | `x:TypeArguments="x:Double"` |
| `System.Boolean` | `x:Boolean` | `x:TypeArguments="x:Boolean"` |
| 自定义类型 | `local:` or `vm:` | `x:TypeArguments="vm:MyModel"` |

## 限制 {#limitations}

- 在根元素上使用 `x:TypeArguments` 时，必须同时指定 `x:Class`。
- XAML 不支持嵌套泛型（例如 `List<List<string>>`）。请在代码中定义它们，再通过绑定或 `x:Static` 引用。
- 并非所有 XAML 上下文都支持 `x:TypeArguments`，它适用于对象元素和资源定义。

## 不支持场景的变通办法 {#workarounds-for-unsupported-scenarios}

当 XAML 泛型不好使时，可以定义一个具体的子类：

```csharp
// Define a non-generic subclass for use in XAML
public class StringList : List<string> { }
public class PersonCollection : ObservableCollection<Person> { }
```

```xml
<!-- Use the concrete type directly -->
<local:StringList x:Key="Names">
    <sys:String>Alice</sys:String>
    <sys:String>Bob</sys:String>
</local:StringList>
```

这种写法在 .NET 的各种 XAML 框架中都很常见，能绕开 `x:TypeArguments` 的所有限制。

## 另请参阅 {#see-also}

- [XAML 命名空间](/docs/xaml/namespaces)：如何在 XAML 中引用 CLR 命名空间。
- [x: 指令](/docs/xaml/directives)：`x:TypeArguments` 及其他指令的完整参考。
- [类型转换器](/docs/xaml/type-converters)：把字符串值转换成 .NET 类型。
