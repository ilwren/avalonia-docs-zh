---
id: introduction-to-data-binding
title: 数据绑定入门
description: 了解 Avalonia 的数据绑定如何用 XAML 标记扩展把界面控件和数据源连接起来。
doc-type: overview
---

import DataBindingDiagram from '@site/src/components/global/DataBindingDiagram/DataBindingDiagram';

Avalonia 用数据绑定把应用对象中的数据搬进界面控件，根据用户输入反过来修改应用对象中的数据，并在用户发出命令时触发应用对象上的操作。

<DataBindingDiagram />

在这套机制里，控件是**绑定目标**，对象则是**数据源**。

Avalonia 运行着一套数据绑定系统，只要在 XAML 中声明简单的映射关系，上述大部分工作它都能代劳，你不必额外写一大堆代码。

数据绑定的映射关系用 XML 写在 Avalonia 控件的特性与应用对象的属性之间。大致语法如下：

```xml
<SomeControl Attribute="{Binding PropertyName}" />
```

映射可以是双向的：绑定对象的属性一变，控件随之更新；控件这边的变化（无论因何而起）也会写回底层对象。双向绑定的典型例子是把一个文本输入框绑定到对象的字符串属性，XML 大致长这样：

```xml
<TextBox Text="{Binding FirstName}" />
```

如果用户编辑了文本框里的文字，底层对象的 `FirstName` 属性会自动更新。反过来，底层对象的 `FirstName` 属性一变，文本框中显示的文字也会刷新。

绑定也可以是单向的：绑定对象的属性变化会反映到控件上，但用户无法通过控件修改数据。只读的文本块控件就是一例。

```xml
<TextBlock Text="{Binding StatusMessage}" />
```

绑定是 MVVM 架构模式的基石，也是用 Avalonia UI 编程的主要方式之一。

:::info
关于如何在 Avalonia 中运用 MVVM 模式，详见 [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)。
:::

:::info
想了解 MVVM 模式在 _Microsoft_ 的起源与演进，可参阅 [Microsoft Patterns and Practices 文章](https://msdn.microsoft.com/en-us/library/hh848246.aspx)。
:::

## 绑定模式 {#binding-modes}

绑定可以在不同模式下工作，模式决定了数据的流向：

| 模式 | 说明 |
|---|---|
| `OneWay` | 源的变化更新目标，目标的变化不回传。 |
| `TwoWay` | 源和目标任一方变化都会更新另一方。 |
| `OneTime` | 源值只读取一次，之后的属性变化一概不跟踪。`DataContext` 变化时绑定会重新求值。 |
| `OneWayToSource` | 目标的变化更新源，反向则不会。 |
| `Default` | 模式由目标属性决定。多数用于显示的属性默认是 `OneWay`；而像 `TextBox.Text` 这类可编辑属性默认是 `TwoWay`。 |

```xml
<TextBox Text="{Binding Name, Mode=TwoWay}" />
<TextBlock Text="{Binding Name, Mode=OneWay}" />
```

## FallbackValue 与 TargetNullValue {#fallbackvalue-and-targetnullvalue}

| 属性 | 说明 |
|---|---|
| `FallbackValue` | 绑定无法解析（例如属性不存在）时显示的值。 |
| `TargetNullValue` | 源属性为 `null` 时显示的值。 |

```xml
<TextBlock Text="{Binding Description, TargetNullValue='No description available'}" />
<Image Source="{Binding AvatarUrl, FallbackValue={StaticResource DefaultAvatar}}" />
```

## 另请参阅 {#see-also}

- [数据上下文](/docs/data-binding/data-context)：数据绑定器从何处取得数据对象。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定路径、模式与转换器。
- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)：与数据绑定配套的架构模式。
