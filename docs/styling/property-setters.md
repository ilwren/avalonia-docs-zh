---
id: property-setters
title: 属性 setter
description: 用 setter、绑定和模板在样式中设定属性值，并弄懂 setter 的优先级规则。
doc-type: reference
---

属性 setter 规定：当 Avalonia 用选择器匹配到某个控件后，该样式要给它套上哪些属性值。

## 基本用法 {#basic-usage}

setter 在 XAML 中写成「属性—值」特性对，格式如下：

```xml
<Setter Property="propertyName" Value="newValueString"/>
```

例如：

```xml
<Setter Property="FontSize" Value="24"/>
<Setter Property="Padding" Value="4 2 0 4"/>
```

你也可以用长格式语法，把控件属性设成一个带多个属性的对象，像这样：

```xml
<Setter Property="MyProperty">
   <MyObject Property1="My Value" Property2="999"/>
</Setter>
```

样式还能用绑定来设定属性。走完常规的选择流程后，Avalonia 会从目标控件的数据上下文中取值。例如：

```xml
<Setter Property="FontSize" Value="{Binding SelectedFontSize}"/>
```

:::caution
setter 中的绑定是针对**目标控件**的 `DataContext` 解析的。即便样式声明在 `<Application.Styles>` 里，绑定依然指向被匹配控件的 `DataContext`，而不是 `Application` 自身设的 `DataContext`。`Application` 不在视觉树或逻辑树中，因此给它设 `DataContext` 对 setter 绑定毫无影响。

若你需要在应用层面套用可配置的值（比如用户选定的颜色），请改用 `DynamicResource` 引用配合运行时资源更新，而不是数据绑定。细节请见[资源概述](/docs/app-development/resources)和[如何切换主题](/docs/how-to/theme-switching-how-to)。
:::

## 样式优先级 {#style-priority}

当一个选择器匹配到多个样式时，由两条规则决定哪个属性 setter 说了算：

* 所在样式集合在应用中的位置——「离得近的」优先。
* 样式在该集合中的位置——「写在后面的」优先。

首先，这意味着离控件更近的样式会生效，比如窗口级样式会盖过应用级样式。其次，当所选中的样式集合处于同一层级时，文件中写在后面的定义优先。

:::caution
**与 CSS 不同**，`Classes` 特性中类名的书写顺序在 Avalonia 里不影响 setter 的优先级。若这两个样式类都设了颜色，那么无论怎么排列类名，结果都一样：

```xml
<Button Classes="h1 blue"/>
<Button Classes="blue h1"/>
```
:::

## 值的回退 {#value-reversion}

只要样式与控件匹配上，它的所有 setter 都会套到控件上。若因选择器的缘故该样式不再匹配某控件，属性值就会回退到优先级次高的那个值。

完整的属性优先级规则请见[属性值优先级](/docs/properties/value-precedence)。

## 可变的值 {#mutable-values}

[`Setter`](/api/avalonia/styling/setter) 只会创建一个 `Value` 实例，并套用到所有被该样式匹配的控件上。若这个对象是可变的，对它的改动会同时反映到所有控件上。

定义在 setter 值里的对象，其绑定访问不到目标控件的数据上下文，因为目标控件可能不止一个。像下面这样定义样式时就会碰上这种情形：

```xml
<Style Selector="MyControl" x:DataType="MyViewModelClass">
  <Setter Property="MyProperty">
     <MyObject Property1="{Binding MyViewModelProperty}"/>
  </Setter>
</Style>
```

上面的例子中，setter 的绑定源会是 `MyObject.DataContext` 而非 `MyControl.DataContext`。若 `MyObject` 没有数据上下文，这个绑定就产不出值来。

## setter 中的数据模板 {#setter-data-templates}

如上一节所述，若 setter 不配**数据模板**，setter 的值只会创建一个实例，由所有匹配的控件共用。若要让值随数据模板而变，请把目标控件放进一个模板元素里，像这样：

```xml
<Style Selector="Border.empty">
  <Setter Property="Child">
    <Template>
      <TextBlock>No content available.</TextBlock>
    </Template>
  </Setter>
</Style>
```

## setter 的优先级 {#setter-precedence}

Avalonia 的 `Setters` 按 [`BindingPriority`](/api/avalonia/data/bindingpriority)、视觉树上的远近，以及 `Styles` 集合顺序这三级依次裁定。优先级是逐个 `StyledProperty` 单独判定的，这样样式才能受益于组合。`DirectProperty` 和 CLR 属性无法被样式化，因此也不参与优先级裁定。

`BindingPriority` 无法在 XAML 中显式设置。完整的优先级清单请见[属性值优先级](/docs/properties/value-precedence)。

## 视觉树上的远近 {#visual-tree-locality}

`BindingPriority` 相同的 setter，接着按它们相对于 `Control` 在视觉树上的位置来挑选：向上找到它所需经过的节点最少的那个 setter 胜出。这一步中，内联样式 setter 的优先级最高。

```xml
<Window>
    <Window.Styles>
        <Style Selector="Button">
            <Setter Property="FontSize" Value="16" />
            <Setter Property="Foreground" Value="Red" />
        </Style>
    </Window.Styles>
    <StackPanel>
        <StackPanel.Styles>
            <Style Selector="Button">
                <Setter Property="FontSize" Value="24" />
            </Style>
        </StackPanel.Styles>

        <Button Content="This Has FontSize=24 with Foreground=Red" />
    </StackPanel>
</Window>
```

## 样式集合顺序 {#styles-collection-order}

当 `BindingPriority` 与视觉树远近都打平时，最后的裁决依据是在 `Styles` 集合中的顺序：最后一个适用的 `Setter` 胜出。

```xml
<StackPanel>
    <StackPanel.Styles>
        <Style Selector="Button.small">
            <Setter Property="FontSize" Value="12" />
        </Style>
        <Style Selector="Button.big">
            <Setter Property="FontSize" Value="24" />
        </Style>
    </StackPanel.Styles>

    <Button Classes="small big" Content="This Has FontSize=24" />
    <Button Classes="big small" Content="This Also Has FontSize=24" />
</StackPanel>
```

:::info
下面这些按钮以不同顺序写出各自的 `Classes`。在 Avalonia 中，这对 setter 优先级没有任何影响。
:::

## 另请参阅 {#see-also}

- [Styles](/docs/styling/styles)
- [属性值优先级](/docs/properties/value-precedence)
- [控件主题](/docs/styling/control-themes)