---
id: compiled-bindings
title: 编译绑定
description: 使用编译绑定，在 Avalonia XAML 中获得编译期校验和更好的性能。
doc-type: how-to
---

Avalonia 默认使用编译绑定（自[版本 12](/docs/avalonia12-breaking-changes) 起）来访问视图模型中的目标属性。编译绑定有这些好处：

* 绑定的属性不存在时，你会直接拿到一个编译错误，排查起来更省事。
* 众所周知反射很慢，编译绑定能提升应用的性能。

## 启用与关闭编译绑定 {#enabling-and-disabling-compiled-bindings}

从版本 12 起，Avalonia 默认启用编译绑定。也就是说，你只需为要绑定的对象提供 `x:DataType`，不必再在控件和窗口上设置 `x:CompileBindings="[True|False]"`。

如果你确实想关掉编译绑定，可以在项目的 `.csproj` 文件中加上 `<AvaloniaUseCompiledBindingsByDefault>` 标记并设为 `false`。不过并不建议这么做。

若项目文件中没有定义 `<AvaloniaUseCompiledBindingsByDefault>`，它从 v12 起默认为 `true`，在更早的 Avalonia 版本中则是 `false`。

## 指定数据类型 {#setting-the-data-type}

编译绑定必须知道所绑定对象的 `DataType`。

[`DataTemplates`](/docs/data-templates/introduction-to-data-templates) 自带 `DataType` 属性。其余元素则在根节点上用 `x:DataType` 指定数据类型，通常是 `Window` 或 `UserControl`。

也可以直接在 `Binding` 中指定 `DataType`。

```xml
<!-- Set DataType in the root node -->
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:vm="using:MyApp.ViewModels"
             // highlight-next-line
             x:DataType="vm:MyViewModel">

    <StackPanel>
        <TextBlock Text="Last name:" />
        <TextBox Text="{Binding LastName}" />
        <TextBlock Text="Given name:" />
        <TextBox Text="{Binding GivenName}" />
        <TextBlock Text="E-Mail:" />
        <!-- Set DataType inside the Binding -->
        <TextBox Text="{Binding MailAddress, DataType={x:Type vm:MyViewModel}}" />

        <Button Content="Send an E-Mail"
                Command="{Binding SendEmailCommand}" />
    </StackPanel>
</UserControl>
```

## `DataContext` 类型推断 {#datacontext-type-inference}

使用编译绑定时，即便你是通过具名元素（`#MyElement.DataContext`）或向上查找父级（`$parent[ControlType].DataContext`）来引用目标，Avalonia 的 XAML 编译器也能推断出目标类型。

大多数情况下都不需要显式类型转换。

```xml
<Window x:Name="MyWindow"
        xmlns:vm="using:MyApp.ViewModels"
        x:DataType="vm:TestDataContext">
    <TextBlock Text="{Binding #MyWindow.DataContext.StringProperty}" />
    <TextBlock Text="{Binding $parent[Window].DataContext.StringProperty}" />
</Window>
```

:::note
`DataContext` 类型推断自 11.3.0 起引入。在更早的 Avalonia 版本中，凡是绑定表达式的目标类型无法自动确定的场合，都需要显式类型转换。
:::

### 显式类型转换 {#explicit-type-casting}

如果你用的是较早版本的 Avalonia，或者编译器推断不出类型，仍可在绑定表达式中写显式类型转换，以确保用上正确的类型。

一般不推荐使用显式类型转换。

```xml
<Window x:Name="MyWindow"
        xmlns:vm="using:MyApp.ViewModels"
        x:DataType="vm:TestDataContext">
    <TextBlock Text="{Binding #MyWindow.((vm:TestDataContext)DataContext).StringProperty}" />
    <TextBlock Text="{Binding $parent[Window].((vm:TestDataContext)DataContext).StringProperty}" />
</Window>
```

## `ReflectionBinding` 与 `CompiledBinding` 标记 {#reflectionbinding-and-compiledbinding-markup}

想让某个绑定单独走反射绑定，用 `ReflectionBinding` 标记。

反过来也成立：即便你已经[在项目中关闭了编译绑定](#enabling-and-disabling-compiled-bindings)，仍可以用 `CompiledBinding` 标记让某个绑定单独走编译绑定。

<Tabs>

<TabItem value="reflection-binding-markup" label="ReflectionBinding markup">

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:vm="using:MyApp.ViewModels"
             x:DataType="vm:MyViewModel">
    <StackPanel>
        <!-- Use the default compiled bindings -->
        <TextBlock Text="Last name:" />
        <TextBox Text="{Binding LastName}" />
        <TextBlock Text="Given name:" />
        <TextBox Text="{Binding GivenName}" />
        <TextBlock Text="E-Mail:" />
        <TextBox Text="{Binding MailAddress}" />

        <!-- This command uses reflection binding instead -->
        <Button Content="Send an E-Mail"
                Command="{ReflectionBinding SendEmailCommand}" />
    </StackPanel>
</UserControl>
```

</TabItem>

<TabItem value="compiled-binding-markup" label="CompiledBinding markup">

```xml
<!-- Set DataType -->
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:vm="using:MyApp.ViewModels"
             x:DataType="vm:MyViewModel">
    <StackPanel>
        <!-- Use compiled bindings -->
        <TextBlock Text="Last name:" />
        <TextBox Text="{CompiledBinding LastName}" />
        <TextBlock Text="Given name:" />
        <TextBox Text="{CompiledBinding GivenName}" />
        <TextBlock Text="E-Mail:" />
        <TextBox Text="{CompiledBinding MailAddress}" />

        <!-- This command uses reflection binding instead -->
        <Button Content="Send an E-Mail"
                Command="{Binding SendEmailCommand}" />
    </StackPanel>
</UserControl>
```

</TabItem>

</Tabs>

## 与反射绑定的差异 {#differences-from-reflection-bindings}

两种绑定解析的是同一套绑定路径，但行为上有两点不同：

**命令参数的转换。** 当 `Command` 绑定到一个接受强类型参数的方法时，反射绑定会在运行时把 `CommandParameter` 的值转换成该类型；而编译绑定走的是类型转换，类型对不上就抛异常。详见[直接绑定到方法](/docs/data-binding/binding-to-commands#binding-directly-to-a-method)。

**报错时机。** 编译绑定把无法解析的路径报成构建错误；反射绑定则在运行时把它作为绑定错误写进日志。详见[调试数据绑定](/docs/data-binding/binding-debugging)。

## 在代码中使用编译绑定 {#compiled-bindings-from-code}

你也可以用 `CompiledBinding.Create` 工厂方法在 C# 代码中创建编译绑定。它用 LINQ 表达式取代字符串属性路径，带来与 XAML 编译绑定同样的编译期安全性和性能优势。示例见[在代码中使用编译绑定](/docs/data-binding/binding-from-code#creating-compiled-bindings-from-code)。

## 另请参阅 {#see-also}

- [在代码中使用编译绑定](/docs/data-binding/binding-from-code#creating-compiled-bindings-from-code)
- [数据绑定语法](/docs/data-binding/data-binding-syntax)
- [绑定到命令](/docs/data-binding/binding-to-commands)