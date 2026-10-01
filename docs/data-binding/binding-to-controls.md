---
id: binding-to-controls
title: 如何绑定到控件
description: 借助 ElementName 或源绑定，把一个控件的属性绑定到另一个控件的属性上。
doc-type: how-to
---


在 _Avalonia UI_ 中，除了绑定到数据上下文，你还可以让一个控件直接绑定到另一个控件。

:::info
注意这种做法完全不经过数据上下文 —— 你绑定的就是另一个控件本身。
:::

## 绑定到具名控件 {#binding-to-a-named-control}

想绑定到另一个具名控件的属性，在控件名前加一个 `#` 字符即可。

```xml
<TextBox Name="other">

<!-- Binds to the Text property of the "other" control -->
<TextBlock Text="{Binding #other.Text}"/>
```

它等价于下面这种长写法，WPF 和 UWP 用户应该很熟悉：

```xml
<TextBox Name="other">
<TextBlock Text="{Binding Text, ElementName=other}"/>
```

_Avalonia UI_ 两种语法都支持。

## 绑定到祖先元素 {#binding-to-an-ancestor}

用 `$parent` 语法可以绑定到目标的父级（按逻辑控件树）：

```xml
<Border Tag="Hello World!">
  <TextBlock Text="{Binding $parent.Tag}"/>
</Border>
```

配合 `$parent` 语法加上索引，就能绑定到任意层级的祖先：

```xml
<Border Tag="Hello World!">
  <Border>
    <TextBlock Text="{Binding $parent[1].Tag}"/>
  </Border>
</Border>
```

索引从零开始，所以 `$parent[0]` 等价于 `$parent`。

也可以这样绑定到最近的某个指定类型的祖先：

```xml
<Border Tag="Hello World!">
  <Decorator>
    <TextBlock Text="{Binding $parent[Border].Tag}"/>
  </Decorator>
</Border>
```

最后，索引和类型还能组合使用：

```xml
<Border Tag="Hello World!">
  <Border>
    <Decorator>
    <TextBlock Text="{Binding $parent[Border;1].Tag}"/>
    </Decorator>
  </Border>
</Border>
```

如果祖先类型需要带上 XAML 命名空间，用冒号分隔命名空间和类名：

```xml
<local:MyControl Tag="Hello World!">
  <Decorator>
    <TextBlock Text="{Binding $parent[local:MyControl].Tag}"/>
  </Decorator>
</local:MyControl>
```

要访问父级 `DataContext` 上的属性，必须用类型转换表达式 `(vm:MyUserControlViewModel)DataContext` 把它转成实际类型。否则 `DataContext` 会被当作 `object` 类型，访问自定义属性会导致编译错误。

```xml
<local:MyControl Tag="Hello World!">
  <Decorator>
    <TextBlock Text="{Binding $parent[local:MyControl].((vm:MyUserControlViewModel)DataContext).CustomProperty}"/>
  </Decorator>
</local:MyControl>
```

:::caution
_Avalonia UI_ 同样支持 WPF/UWP 的 `RelativeSource` 语法，作用相似但_并不等同_：`RelativeSource` 作用于_视觉_树，而本文介绍的语法作用于_逻辑_树。
:::

## 另请参阅 {#see-also}

- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定路径、模式与转换器。
- [编译绑定](/docs/data-binding/compiled-bindings)：编译期受校验的类型安全绑定。
- [控件树](/docs/custom-controls/control-trees)：逻辑树与视觉树的结构。
