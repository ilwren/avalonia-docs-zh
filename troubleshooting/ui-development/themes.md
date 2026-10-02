---
id: themes
title: 主题
description: 排查 Avalonia UI 主题的常见问题，包括找不到控件主题、意料之外的样式覆盖，以及应用窗口透明。
doc-type: troubleshooting
---

## 我的控件主题没被找到 {#my-control-theme-isnt-being-found}

若 Avalonia 没有采用你的自定义控件主题，请确认该主题返回的[样式键](/docs/styling/styles)与控件主题的 `x:Key` 和 `TargetType` 都对得上。

常见原因有：

- **`x:Key` 对不上**：你在 XAML 中引用的键，与控件主题资源中定义的键不一致。
- **`TargetType` 不对**：你 `ControlTheme` 上的 `TargetType` 与你想套样式的那个控件对不上。
- **主题没被引入**：你没有添加指向控件主题所在文件的 `StyleInclude` 或 `ResourceInclude`。

要诊断这个问题，可在运行时打开 [Avalonia DevTools](/tools/developer-tools/installation)，查看 `Styles` 面板。它会列出所选控件上生效的样式和主题，帮你确认自己的主题是否已加载并应用。

```xml title="Example: defining and referencing a control theme"
<!-- In your theme file (e.g., MyButtonTheme.axaml) -->
<ControlTheme x:Key="{x:Type Button}" TargetType="Button">
    <Setter Property="Background" Value="SlateBlue" />
    <!-- Additional setters and template here -->
</ControlTheme>

<!-- In App.axaml, include the theme -->
<Application.Styles>
    <FluentTheme />
    <StyleInclude Source="/Themes/MyButtonTheme.axaml" />
</Application.Styles>
```

## 我的控件主题把别的控件搞坏了 {#my-control-theme-is-breaking-other-controls}

许多 Avalonia 控件内部本身就是由其他 Avalonia 控件拼起来的。若你写的样式或控件主题瞄准某个类型的所有控件，结果可能出人意料——它会套到视觉树中该类型的每个实例上，包括嵌在其他控件内部的那些。

举例来说，若你在 `Window` 中写了一条瞄准 `TextBlock` 的样式，窗口里的每个 `TextBlock` 都会被套上，哪怕它是另一个控件模板的一部分（比如某个 `ListBox` 项或 `Button` 的标签）。

```xml title="Example: a style that unintentionally affects nested controls"
<Window.Styles>
    <Style Selector="TextBlock">
        <Setter Property="Foreground" Value="Red" />
    </Style>
</Window.Styles>
```

想让样式只作用于你真正想改的那些控件，就得把选择器写得更具体些。你可以按样式类、按名称，或者按嵌套上下文来圈定范围：

```xml title="Example: scoping a style with a class selector"
<Window.Styles>
    <Style Selector="TextBlock.heading">
        <Setter Property="Foreground" Value="Red" />
    </Style>
</Window.Styles>

<!-- Only this TextBlock is affected -->
<TextBlock Classes="heading" Text="Page title" />
```

## 应用窗口透明，或者什么内容都没渲染 {#application-window-is-transparent-or-no-content-is-rendered}

若应用窗口显得透明，或者看不到任何可见内容，最可能的原因是没有装任何 Avalonia 主题。Avalonia 需要一套基础主题（比如 `FluentTheme` 或 `SimpleTheme`）来提供默认的控件模板和样式；没有它，控件就没有任何视觉呈现。

解决办法是确保你的 `App.axaml` 中引入了一套主题：

```xml title="App.axaml"
<Application.Styles>
    <FluentTheme />
</Application.Styles>
```

若你用的是第三方主题，请确认：

- 该主题的 NuGet 包已装进你的项目。
- 该主题已加入你的 `Application.Styles` 集合。
- 该主题与你所用的 Avalonia 版本兼容。

若用第三方主题时问题依旧，请联系该主题的维护者寻求支持。

## 另请参阅 {#see-also}

- [主题概述](/docs/styling/themes)
- [Styles](/docs/styling/styles)
- [排查样式问题](/troubleshooting/ui-development/styles)
- [如何使用控件主题](/docs/styling/control-themes)
- [开发者工具](/tools/developer-tools/installation)
