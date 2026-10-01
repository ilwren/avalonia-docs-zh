---
id: sharing-styles
title: 共享样式
---

import VsStylesTemplateScreenshot from '/img/guides/ui-development/styling/vs-styles-template.png';

你可以把样式定义在单独的文件里，再在应用的任意层级引入它们。这样便能在多个窗口、用户控件之间——甚至跨项目——共用同一套样式。

## 如何使用引入的样式 {#how-to-use-included-styles}

本指南演示如何从一个单独的样式文件共享样式，并把它引入应用。这种做法让你能在多个应用之间共用样式。

具体做法是：在一个新的 XAML 文件里定义样式，其根元素必须是 `Style` 或 `Styles`。例如：

```xml
<Styles xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Style Selector="TextBlock.h1">
        <Setter Property="FontSize" Value="24"/>
        <Setter Property="FontWeight" Value="Bold"/>
    </Style>
</Styles>
```

Avalonia 的解决方案模板提供了往项目里添加样式文件的捷径。步骤如下：

-  在**解决方案资源管理器**中右键点击你的项目。
-  依次点击 **Add** 和 **New Item**
-  在 Avalonia 项目类型中点击 **Styles (Avalonia)**
-  为样式文件取个名字

<Image light={VsStylesTemplateScreenshot} alt="Visual Studio Add New Item dialog showing the Styles (Avalonia) template" position="center" maxWidth={400} cornerRadius="true"/>

要用上定义在单独文件里的样式，你必须用 [`StyleInclude`](/api/avalonia/markup/xaml/styling/styleinclude) 元素引用它。source 特性指明样式文件的位置。在哪一层添加这个元素由你决定。

举例来说，要使用 `AppStyles.axaml` 文件（存放在 `/Styles` 文件夹中）里定义的样式，可以在窗口里这样写一个 `StyleInclude` 元素：

```xml
<Window ... >
    <Window.Styles>
        <StyleInclude Source="/Styles/AppStyles.axaml" />
    </Window.Styles>

    <StackPanel>
       <TextBlock Classes="h1">Heading 1</TextBlock>
       <TextBlock>This is not a heading and will not be changed.</TextBlock>
    </StackPanel>
</Window>
```

不过更常见的做法是在 `App.axaml` 文件中引用样式文件：

```xml
<Application... > 
    <Application.Styles>
        <FluentTheme />
        <StyleInclude Source="/AppStyles.axaml"/>
    </Application.Styles>
</Application>
```

这样你就能在整个应用中使用那个独立文件里的样式了。

你还可以用 `avares://` 前缀引入另一个程序集里的样式：

```xml
<Application... > 
    <Application.Styles>
        <FluentTheme />
        <StyleInclude Source="avares://MyApp.Shared/Styles/CommonAppStyles.axaml"/>
    </Application.Styles>
</Application>
```

这引用的是 `MyApp.Shared` 项目中的 `/Styles/CommonAppStyles.axaml` 文件。

## 排查问题：引入的样式里找不到 StaticResource {#troubleshooting-staticresource-not-found-in-included-styles}

当你把资源和样式拆进多个引入文件时，即便资源文件排在引用它的样式文件之前，`StaticResource` 查找照样可能失败。

原因在于：每个 `StyleInclude` 都是在挂到父级 `Styles` 集合之前独立加载的。加载那一刻，被引入的样式并不知道有哪些同级引入，自然解析不了定义在另一个文件里的 `StaticResource`。

举个例子，假设你有一个定义字体资源的 `Fonts.axaml` 和一个引用它们的 `TextStyles.axaml`：

```xml
<Application.Styles>
    <StyleInclude Source="/Styles/Fonts.axaml" />
    <StyleInclude Source="/Styles/TextStyles.axaml" />
</Application.Styles>
```

`TextStyles.axaml` 里对 `Fonts.axaml` 中所定义字体的 `StaticResource` 引用，会在加载时失败。

有两种解决办法：

- **用 `DynamicResource` 代替 `StaticResource`。**`DynamicResource` 是在所有样式挂载完毕后于运行时解析的，因此能找到同级引入中定义的资源。多数情况下都推荐这么做，而且由于主题资源很少变动，性能影响微乎其微。
- **把资源和引用它们的样式写在同一个文件里。**若某个样式文件需要字体或画刷资源，就把这些资源定义一并放进该文件，而不是依赖另一个独立的资源文件。

## 另请参阅 {#see-also}

- [Styles](/docs/styling/styles)
- [属性值优先级](/docs/properties/value-precedence)
