---
id: styles
title: 样式
description: 排查 Avalonia 样式的常见问题。
doc-type: troubleshooting
---

## 选择器匹配不到任何目标 {#selector-has-no-targets}

和 CSS 选择器一样，Avalonia 的选择器匹配不到控件时既不报错也不警告，样式就这么悄无声息地没了踪影。

看看你是不是用了并不存在的名称或样式类。

看看你是不是用了子级选择器，而那儿压根没有子级可匹配。

## 生效的是另一条样式 {#wrong-style-is-applied}

在 `BindingPriority` 相同的前提下，样式按声明顺序应用。若多个样式文件都瞄准同一个控件属性，最后匹配上的那条胜出。

比如在下面这几个文件中，`Style2.axaml` 里的样式优先于 `Style1.axaml` 里的，最终 `TextBlock` 会是 `FontSize="16"` 和 `Foreground="Blue"`。同一个样式文件内部也是按这个先后顺序定优先级的。

<Tabs>

<TabItem value="app-styles" label="App.axaml">

```xml
<Application.Styles>
    <StyleInclude Source="Style1.axaml" />
    <!-- Later style has priority -->
    // highlight-next-line
    <StyleInclude Source="Style2.axaml" />
</Application.Styles>
```

</TabItem>

<TabItem value="style1" label="Style1.axaml">

```xml
<Style Selector="TextBlock.header">
    <Setter Property="Foreground" Value="Green" />
</Style>
```

</TabItem>

<TabItem value="style2" label="Style2.axaml">

```xml
<Style Selector="TextBlock.header">
    <Setter Property="Foreground" Value="Blue" />
    <Setter Property="FontSize" Value="16" />
</Style>
```

</TabItem>

</Tabs>

## 样式盖不过本地属性 {#style-cannot-override-a-local-property}

直接设在控件上的本地属性值，优先级高于任何样式值。比如下面这个文本块的前景色就是红的：

```xml
<Style Selector="TextBlock.header">
    <Setter Property="Foreground" Value="Green" />
</Style>

<TextBlock Classes="header" Foreground="Red" />
```

若想让样式在运行时改得动这个属性，就别在本地设它，改为通过样式来设。

## 伪类样式没有生效 {#pseudoclass-style-is-not-applied}

受控件模板结构所限，有些伪类的表现未必如你所料。下面的例子里，`Button` 悬停时变成了灰色，可按 `:pointerover` 伪类的写法，你本以为它该变蓝才对。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <UserControl.Styles>
    <Style Selector="Button">
      <Setter Property="Background" Value="Red" />
    </Style>
    <Style Selector="Button:pointerover">
      <Setter Property="Background" Value="Blue" />
    </Style>
  </UserControl.Styles>

  <Button HorizontalAlignment="Center" 
          Content="lolwut?" />
</UserControl>
```

</XamlPreview>

原因出在 [Fluent 主题的按钮模板](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Themes.Fluent/Controls/Button.xaml)上——新建的 Avalonia 项目默认就用它。在该模板中，按钮的背景由一个绑定到按钮 `Background` 属性的 `ContentPresenter` 负责绘制。进入 pointer-over 状态时，选择器会把另一种背景直接套到 `ContentPresenter` 这个模板部件上，绕开了针对 `Background` 的其他属性 setter。正因如此，哪怕是动画改了按钮的 `Background`，也起不了任何作用。

```xml
<Style Selector="Button">
    <Setter Property="Background" Value="{DynamicResource ButtonBackground}"/>
    <Setter Property="Template">
        <ControlTemplate>
            <ContentPresenter Name="PART_ContentPresenter"
                              Background="{TemplateBinding Background}"
                              Content="{TemplateBinding Content}"/>
        </ControlTemplate>
    </Setter>
</Style>
<Style Selector="Button:pointerover /template/ ContentPresenter#PART_ContentPresenter">
    <Setter Property="Background" Value="{DynamicResource ButtonBackgroundPointerOver}" />
</Style>
```

要让伪类样式确实生效，你的样式选择器必须瞄准相关的模板部件。就本例而言，把那条蓝色背景 setter 改成选中 `PART_ContentPresenter` 即可。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <UserControl.Styles>
    <Style Selector="Button">
        <Setter Property="Background" Value="Red" />
    </Style>
    <Style Selector="Button:pointerover /template/ ContentPresenter#PART_ContentPresenter">
        <Setter Property="Background" Value="Blue" />
    </Style>
  </UserControl.Styles>

  <Button HorizontalAlignment="Center" 
          Content="woo!" />
</UserControl>
```

</XamlPreview>

## 样式不再生效时，先前的属性值没有恢复 {#previous-property-value-is-not-restored-when-style-is-no-longer-applied}

Avalonia 有多种属性类型，详见[定义属性](/docs/custom-controls/defining-properties)。

**直接属性**不支持样式化。它不会按优先级存多个值，而是只认最后一次写入的值，因此也无从恢复到先前的值。它的用意是在只需简单机制的场合降低开销、提高性能。

若你发现先前的属性值恢复不了，多半是碰上了直接属性。不妨换一个属性，或者[自定义一个属性](/docs/custom-controls/defining-properties)。

## 另请参阅 {#see-also}

- [Styles](/docs/styling/styles)
- [样式选择器](/docs/styling/style-selectors)
- [样式选择器语法](/docs/styling/style-selector-syntax)
- [Pseudoclasses](/docs/styling/pseudoclasses)
- [属性 setter](/docs/styling/property-setters)
- [属性值优先级](/docs/properties/value-precedence)
- [共享样式](/docs/styling/sharing-styles)
- [控件模板实战](/docs/styling/control-template-walkthrough)
- [定义属性](/docs/custom-controls/defining-properties)
- [排查主题问题](/troubleshooting/ui-development/themes)