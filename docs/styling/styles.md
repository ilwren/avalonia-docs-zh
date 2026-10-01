---
id: styles
title: 样式
description: 了解如何用 Avalonia 的样式、选择器和 setter 在控件之间共享属性设置。
doc-type: explanation
---

Avalonia 的样式系统是一套在控件之间共享属性设置的机制。
Avalonia 为控件样式提供了三种主要手段：

## Styles

- [样式](/docs/styling/styles)类似 CSS 的样式，通常用于依据控件在应用中的内容或用途来套样式，比如为标题文本块做一套样式。

## 控件主题 {#control-themes}

- [控件主题](/docs/styling/control-themes)类似 WPF/UWP 的样式，通常用于给控件套上一整套主题。

## 容器查询 {#container-queries}
- [容器查询](/docs/styling/container-queries)是一组依容器尺寸而生效的样式。

## 运作原理 {#how-it-works}

说到底，样式机制分两步：选择与替换。两步都可以在 XAML 里规定，不过你通常会给控件元素打上 'class' 标签，以便第一步的选择。

:::info
Avalonia 样式系统在控件元素上使用 'class' 标签的做法，与 CSS（层叠样式表）配合 HTML 元素的方式如出一辙。
:::

样式系统在选择这一步会从控件出发沿[逻辑树](/docs/custom-controls/control-trees)向上搜寻，由此实现样式的层叠。这意味着定义在应用最高层（`App.axaml` 文件）的样式随处可用，但仍可能被离控件更近的定义（比如窗口或用户控件中的）盖过。

一旦选择这步找到匹配，被匹配控件的属性便按样式中的 setter 相应改变。

## 样式怎么写 {#how-styles-are-written}

XAML 中的样式由两部分组成：一个 selector 特性，以及一个或多个 setter 元素。selector 的值是一个采用 Avalonia **样式选择器语法**的字符串。每个 setter 元素按名称指明要改的属性，以及要替换成的新值。写法大致如下：

```xml
<Style Selector="selector syntax">
     <Setter Property="property name" Value="new value"/>
     ...
</Style>
```

:::info
Avalonia 的**样式选择器语法**与 CSS（层叠样式表）的那套相仿。详细的参考信息请见[样式选择器语法](/docs/styling/style-selector-syntax)。
:::

## Example

下面这个例子演示了样式的写法，以及如何借助[样式类](/docs/styling/style-classes)把它套到控件元素上：

```xml
<Window ... >
    <Window.Styles>
        <Style Selector="TextBlock.h1">
            <Setter Property="FontSize" Value="24"/>
            <Setter Property="FontWeight" Value="Bold"/>
        </Style>
    </Window.Styles>
    <StackPanel Margin="20">
       <TextBlock Classes="h1">Heading 1</TextBlock>
    </StackPanel>
</Window>
```

在这个例子中，所有带 `h1` 样式类的 `TextBlock` 元素，都会按该样式设定的字号和字重显示。

## 样式该放在哪儿 {#where-to-put-styles}

你把样式放进 `Control` 或 `Application` 上的 `Styles` 集合元素里。比如窗口的样式集合长这样：

```xml
<Window.Styles>
   <Style> ...  </Style>
</Window.Styles>
```

样式集合所在的位置决定了其中样式的作用范围。在上面的例子中，这些样式作用于该窗口及其全部内容。若你把样式加到 `Application` 上，它便是全局生效的。

## 选择器 {#the-selector}

样式选择器规定该样式作用于哪些控件。选择器有多种写法，最简单的一种是：

```xml
<Style Selector="TargetControlClass.styleClassName">
```

这条选择器匹配所有样式键为 `TargetControlClass`、且带有 `styleClassName` 样式类的控件。

:::info
完整的选择器清单可在[样式选择器语法](/docs/styling/style-selector-syntax)参考中找到。
:::

## Setters

setter 描述选择器匹配到控件之后要做什么。它们就是简单的「属性/值」对，格式如下：

```xml
<Setter Property="FontSize" Value="24"/>
<Setter Property="Padding" Value="4 2 0 4"/>
```

只要某个样式匹配到控件，该样式中的所有 setter 都会套到这个控件上。

:::info
关于 setter 的更多信息，请见[属性 setter](/docs/styling/property-setters)。
:::

## 嵌套样式 {#nested-styles}

样式可以嵌套在别的样式里。要嵌套样式，请把子样式写成父 `<Style>` 元素的子元素，并让其选择器以[`Nesting selector (^)`](/docs/styling/style-selector-syntax)开头：

```xml
<Style Selector="TextBlock.h1">
    <Setter Property="FontSize" Value="24"/>
    <Setter Property="FontWeight" Value="Bold"/>
    
    // highlight-start
    <Style Selector="^:pointerover">
        <Setter Property="Foreground" Value="Red"/>
    </Style>
    // highlight-end
</Style>
```

嵌套时，父样式的选择器会自动作用于子样式。上面的例子中，嵌套样式的实际选择器相当于 `TextBlock.h1:pointerover`，也就是说指针悬停在控件上时它会显示为红色前景。

:::info
嵌套选择器不可省略，而且必须出现在子选择器的开头。
:::

## 样式键 {#style-key}

样式选择器所匹配对象的类型，并不由控件的具体类型决定，而是看它的 `StyleKey` 属性。

`StyleKey` 属性默认返回当前实例的类型。不过，若你希望自己继承自 `Button` 的控件按 `Button` 来套样式，可以在类中重写 `StyleKeyOverride` 属性，让它返回 `typeof(Button)`。

```csharp
public class MyButton : Button
{
    // `MyButton` will be styled as a standard `Button` control.
    protected override Type StyleKeyOverride => typeof(Button);
}
```

:::info
请注意这套逻辑与 WPF/UWP 恰好相反：在那些框架里，你派生出的新控件默认按基类控件套样式，除非你重写 `DefaultStyleKey` 属性；而在 Avalonia 中，控件默认按自己的具体类型套样式，除非你另给一个样式键。
:::

:::info
在 Avalonia 11 之前，重写样式键的办法是实现 `IStyleable` 并为 `IStyleable.StyleKey` 属性提供新的实现。Avalonia 11 出于兼容仍然支持这套机制，但它可能在未来版本中被移除。
:::

## 样式与资源 {#styles-and-resources}

资源常与样式搭配使用，以维持呈现上的一致。你可以用资源定义应用中的标准配色和图标；若把它们放进单独的文件引入，还能在多个应用之间共用。

:::info
关于如何在应用中使用资源，请见[资源字典](/docs/app-development/resource-dictionary)。
:::

## 另请参阅 {#see-also}

- [共享样式](/docs/styling/sharing-styles)
- [样式类](/docs/styling/style-classes)
- [样式选择器语法](/docs/styling/style-selector-syntax)
- [属性 setter](/docs/styling/property-setters)
- [资源字典](/docs/app-development/resource-dictionary)
