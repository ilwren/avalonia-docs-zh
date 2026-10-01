---
id: built-in-data-binding-converters
title: 内置数据绑定转换器
description: Avalonia 内置值转换器参考，用于常见的数据绑定转换场景。
doc-type: reference
---

_Avalonia UI_ 为一些常见场景内置了若干数据绑定转换器：

| 转换器                           | 说明                                                                                                                         |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Negation Operator                   | 把 ! 运算符放在绑定路径前面，即可取布尔值的反。另见下方的说明。 |
| `StringConverters.IsNullOrEmpty`    | 输入字符串为 null 或空时返回 `true`                                                                                 |
| `StringConverters.IsNotNullOrEmpty` | 输入字符串为 null 或空时返回 `false`                                                                                |
| `ObjectConverters.IsNull`           | 输入为 null 时返回 `true`                                                                                                 |
| `ObjectConverters.IsNotNull`        | 输入为 null 时返回 `false`                                                                                                |
| `BoolConverters.And`                | 多值转换器，所有输入都为 true 时返回 `true`。                                                                 |
| `BoolConverters.Or`                 | 多值转换器，任一输入为 true 时即返回 `true`。                                                                   |

## 取反运算符示例 {#negation-operator-examples}

本例在绑定值为 false 时显示 `TextBlock`：

```xml
<StackPanel>
  <TextBox Name="input" IsEnabled="{Binding AllowInput}"/>
  <TextBlock IsVisible="{Binding !AllowInput}">Input is not allowed</TextBlock>
</StackPanel>
```

绑定到非布尔值时取反同样有效。原理是先把绑定值转换成布尔值（用 `Convert.ToBoolean` 函数），再对结果取反。

举例来说，整数 0 会被 `Convert.ToBoolean` 函数转换为 false，其余整数都转换为 true，于是可以用取反运算符在集合为空时显示一条提示：

```xml
<Panel>
  <ListBox ItemsSource="{Binding Items}"/>
  <TextBlock IsVisible="{Binding !Items.Count}">No results found</TextBlock>
</Panel>
```

取反运算符也可以连用两次。比如你想先把整数转换成布尔值，再对结果取反。

可以借此在集合为空（计数为零）时隐藏某个控件：

```xml
<Panel>
  <ListBox ItemsSource="{Binding Items}" IsVisible="{Binding !!Items.Count}"/>
</Panel>
```

## 其他转换示例 {#other-conversion-examples}

下面这个绑定会在文本块绑定的文字为 null 或空时把它隐藏：

```xml
<TextBlock Text="{Binding MyText}"
           IsVisible="{Binding MyText, 
                       Converter={x:Static StringConverters.IsNotNullOrEmpty}}"/>
```

这个例子会在绑定对象为 null 或空时隐藏内容控件：

```xml
<ContentControl Content="{Binding MyContent}"
                IsVisible="{Binding MyContent, 
                            Converter={x:Static ObjectConverters.IsNotNull}}"/>
```

下面这个例子演示绑定多个参数：当绑定对象的 `MyText` 属性既不为 null 也不为空，且 `IsMyNotEmptyTextVisible` 属性为 `true` 时，才显示该文本块：

```xml
<TextBlock Text="{Binding MyText, StringFormat='My text: {0}'}">
  <TextBlock.IsVisible>
    <MultiBinding Converter="{x:Static BoolConverters.And}">
        <Binding Path="MyText" Converter="{x:Static StringConverters.IsNotNullOrEmpty}"/>
        <Binding Path="IsMyNotEmptyTextVisible"/>
    </MultiBinding>
  </TextBlock.IsVisible>
</TextBlock>
```

## 更多信息 {#more-information}


:::info
可以参考 [Avalonia UI 值转换器示例](https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/MVVM/ValueConversionSample)。
:::

## 另请参阅 {#see-also}

- [如何创建自定义数据绑定转换器](/docs/data-binding/how-to-create-a-custom-data-binding-converter)：编写自定义值转换器。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定参数与转换器的用法。
- [MultiBinding](/docs/data-binding/multi-binding)：把多个绑定值组合起来。
