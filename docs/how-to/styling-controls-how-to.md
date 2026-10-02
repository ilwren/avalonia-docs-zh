---
id: styling-controls-how-to
title: "操作指南：为控件设置样式与主题"
description: 在 Avalonia 中用颜色、变体、主题和可复用样式自定义控件外观。
doc-type: how-to
---

本指南汇总了在 Avalonia 应用中自定义控件外观的实用做法，包括改颜色、做变体、适配浅色与深色模式，以及编写可复用的样式。

## 改变控件的颜色 {#change-a-controls-colors}

### 使用样式类 {#using-style-classes}

你可以定义一条按类型和类名匹配控件的样式类，再在 AXAML 标记里给控件加上这个类。下面的例子为 [`Button`](/api/avalonia/controls/button) 控件创建了一个 `primary` 类，设置了 `Background` 和 `Foreground` 属性，同时照顾到悬停和按下状态：

```xml
<Window.Styles>
    <Style Selector="Button.primary">
        <Setter Property="Background" Value="#6366F1" />
        <Setter Property="Foreground" Value="White" />
    </Style>
    <Style Selector="Button.primary:pointerover">
        <Setter Property="Background" Value="#818CF8" />
    </Style>
    <Style Selector="Button.primary:pressed">
        <Setter Property="Background" Value="#4F46E5" />
    </Style>
</Window.Styles>

<Button Classes="primary" Content="Submit" />
```

### 多个样式类 {#multiple-classes}

同一个控件上可以叠加多个样式类，把彼此独立的样式关注点分层处理。每个类各自贡献一组属性设置器，因此你可以随意搭配：

```xml
<Style Selector="Button.rounded">
    <Setter Property="CornerRadius" Value="999" />
</Style>
<Style Selector="Button.large">
    <Setter Property="Padding" Value="24,12" />
    <Setter Property="FontSize" Value="16" />
</Style>

<Button Classes="primary rounded large" Content="Submit" />
```

在这个例子里，`Button` 同时受到 `primary`、`rounded` 和 `large` 三个类的影响。

## 制作按钮变体 {#create-button-variants}

你可以先写一条作用于全部 `Button` 控件的基础样式，再为各个变体加上基于样式类的覆盖，从而为应用攒出一套统一的按钮变体。这样既保住了视觉语言的一致性，又能因地制宜：

```xml
<Application.Styles>
    <!-- Base button styles -->
    <Style Selector="Button">
        <Setter Property="CornerRadius" Value="6" />
        <Setter Property="Padding" Value="16,8" />
        <Setter Property="Transitions">
            <Transitions>
                <BrushTransition Property="Background" Duration="0:0:0.15" />
            </Transitions>
        </Setter>
    </Style>

    <!-- Primary variant -->
    <Style Selector="Button.primary">
        <Setter Property="Background" Value="#6366F1" />
        <Setter Property="Foreground" Value="White" />
    </Style>
    <Style Selector="Button.primary:pointerover">
        <Setter Property="Background" Value="#818CF8" />
    </Style>
    <Style Selector="Button.primary:pressed">
        <Setter Property="Background" Value="#4F46E5" />
    </Style>

    <!-- Danger variant -->
    <Style Selector="Button.danger">
        <Setter Property="Background" Value="#EF4444" />
        <Setter Property="Foreground" Value="White" />
    </Style>
    <Style Selector="Button.danger:pointerover">
        <Setter Property="Background" Value="#F87171" />
    </Style>
    <Style Selector="Button.danger:pressed">
        <Setter Property="Background" Value="#DC2626" />
    </Style>

    <!-- Ghost variant (no background) -->
    <Style Selector="Button.ghost">
        <Setter Property="Background" Value="Transparent" />
        <Setter Property="BorderThickness" Value="0" />
    </Style>
    <Style Selector="Button.ghost:pointerover">
        <Setter Property="Background" Value="#10000000" />
    </Style>
</Application.Styles>
```

之后在应用的任何地方都能用上这些变体：

```xml
<StackPanel Orientation="Horizontal" Spacing="8">
    <Button Classes="primary" Content="Save" />
    <Button Classes="danger" Content="Delete" />
    <Button Classes="ghost" Content="Cancel" />
</StackPanel>
```

## 随主题而变的颜色 {#theme-aware-colors}

要让你的自定义颜色在用户切换浅色/深色模式时自动适配，请把它们定义在 `ThemeDictionaries` 里。每本字典都以 `Light` 或 `Dark` 为键，Avalonia 会在运行时挑出正确的那一本：

```xml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.ThemeDictionaries>
            <ResourceDictionary x:Key="Light">
                <SolidColorBrush x:Key="CardBackground" Color="#FFFFFF" />
                <SolidColorBrush x:Key="CardBorder" Color="#E5E7EB" />
                <SolidColorBrush x:Key="TextPrimary" Color="#111827" />
                <SolidColorBrush x:Key="TextSecondary" Color="#6B7280" />
            </ResourceDictionary>
            <ResourceDictionary x:Key="Dark">
                <SolidColorBrush x:Key="CardBackground" Color="#1F2937" />
                <SolidColorBrush x:Key="CardBorder" Color="#374151" />
                <SolidColorBrush x:Key="TextPrimary" Color="#F9FAFB" />
                <SolidColorBrush x:Key="TextSecondary" Color="#9CA3AF" />
            </ResourceDictionary>
        </ResourceDictionary.ThemeDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

在样式中用 `DynamicResource` 引用这些资源，主题一变，取值也跟着更新：

```xml
<Style Selector="Border.card">
    <Setter Property="Background" Value="{DynamicResource CardBackground}" />
    <Setter Property="BorderBrush" Value="{DynamicResource CardBorder}" />
    <Setter Property="BorderThickness" Value="1" />
    <Setter Property="CornerRadius" Value="8" />
    <Setter Property="Padding" Value="16" />
</Style>
```

:::tip
主题字典里的值请用 `DynamicResource`，不要用 `StaticResource`。`StaticResource` 在加载时解析一次就定下了，主题切换后不会更新。
:::

## 自定义 `TextBox` 的外观 {#custom-textbox-appearance}

你可以把 `TextBox` 改造成只带下划线、不要完整边框。下面的例子把 `BorderThickness` 设成只显示底边，并在 `:focus` 和 `:error` 伪类下改变颜色：

```xml
<Style Selector="TextBox.underline">
    <Setter Property="BorderThickness" Value="0,0,0,2" />
    <Setter Property="BorderBrush" Value="#D1D5DB" />
    <Setter Property="Background" Value="Transparent" />
    <Setter Property="CornerRadius" Value="0" />
    <Setter Property="Padding" Value="0,8" />
</Style>
<Style Selector="TextBox.underline:focus">
    <Setter Property="BorderBrush" Value="#6366F1" />
</Style>
<Style Selector="TextBox.underline:error">
    <Setter Property="BorderBrush" Value="#EF4444" />
</Style>
```

## 卡片组件 {#card-component}

给 `Border` 控件套上样式类，就能做出可复用的卡片样式。`card` 类给出的是带可见边框的扁平卡片，而 `card-elevated` 则用 `BoxShadow` 营造出浮起的效果：

```xml
<Style Selector="Border.card">
    <Setter Property="Background" Value="{DynamicResource CardBackground}" />
    <Setter Property="BorderBrush" Value="{DynamicResource CardBorder}" />
    <Setter Property="BorderThickness" Value="1" />
    <Setter Property="CornerRadius" Value="8" />
    <Setter Property="Padding" Value="16" />
</Style>

<Style Selector="Border.card-elevated">
    <Setter Property="Background" Value="{DynamicResource CardBackground}" />
    <Setter Property="BoxShadow" Value="0 4 6 0 #15000000" />
    <Setter Property="CornerRadius" Value="8" />
    <Setter Property="Padding" Value="16" />
</Style>
```

像这样使用你的卡片样式：

```xml
<Border Classes="card">
    <StackPanel Spacing="8">
        <TextBlock Text="Card Title" FontWeight="Bold" />
        <TextBlock Text="Card content here" Foreground="Gray" />
    </StackPanel>
</Border>
```

## 把样式抽到共享文件里 {#extract-styles-to-a-shared-file}

样式一多，就该把它们挪进单独的 `.axaml` 文件了。这样 `App.axaml` 能保持清爽，样式也能跨项目复用：

```xml title="Styles/ButtonStyles.axaml"
<Styles xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Style Selector="Button.primary">
        <Setter Property="Background" Value="#6366F1" />
        <Setter Property="Foreground" Value="White" />
    </Style>
    <!-- more styles... -->
</Styles>
```

然后在 `App.axaml` 中用 `StyleInclude` 引用这个文件。`avares://` URI 方案指向的是程序集中的嵌入资源：

```xml
<Application.Styles>
    <FluentTheme />
    <StyleInclude Source="avares://MyApp/Styles/ButtonStyles.axaml" />
</Application.Styles>
```

## 覆盖主题自带的样式 {#override-theme-styles}

应用的样式在内置主题之后生效，所以任何默认外观你都能改写。把覆盖样式放在 `Application.Styles` 里 `<FluentTheme />` 的后面，确保它们优先级更高：

```xml
<Application.Styles>
    <FluentTheme />

    <!-- Override all TextBlock to use your preferred font -->
    <Style Selector="TextBlock">
        <Setter Property="FontFamily" Value="Inter, Segoe UI, sans-serif" />
    </Style>

    <!-- Override ComboBox dropdown max height -->
    <Style Selector="ComboBox /template/ Popup#PART_Popup">
        <Setter Property="MaxHeight" Value="300" />
    </Style>
</Application.Styles>
```

`/template/` 选择器让你能探入控件模板、指向其中的内部部件。这里指向的是 `ComboBox` 模板内名为 `PART_Popup` 的那个 `Popup`。

## 用伪类做条件样式 {#conditional-styling-with-pseudo-classes}

伪类让你能依据控件的当前状态施加样式，一行代码隐藏都不用写。控件状态一变，Avalonia 就会自动重新判定伪类选择器：

```xml
<!-- Disabled state -->
<Style Selector="Button:disabled">
    <Setter Property="Opacity" Value="0.5" />
</Style>

<!-- Checked state (ToggleButton, CheckBox, RadioButton) -->
<Style Selector="ToggleButton:checked">
    <Setter Property="Background" Value="#6366F1" />
    <Setter Property="Foreground" Value="White" />
</Style>

<!-- Focus visible (keyboard navigation only) -->
<Style Selector="Button:focus-visible">
    <Setter Property="BorderBrush" Value="#6366F1" />
    <Setter Property="BorderThickness" Value="2" />
</Style>
```

常见的伪类有 `:pointerover`、`:pressed`、`:disabled`、`:focus`、`:focus-visible`、`:checked` 和 `:error`。完整清单请参阅[伪类](/docs/styling/pseudoclasses)。

## 另请参阅 {#see-also}

- [Styles](/docs/styling/styles)
- [Style Classes](/docs/styling/style-classes)
- [Style Selectors](/docs/styling/style-selectors)
- [Pseudo-classes](/docs/styling/pseudoclasses)
- [Style Best Practices](/docs/styling/style-best-practices)
- [Sharing Styles](/docs/styling/sharing-styles)
- [Control Template Walkthrough](/docs/styling/control-template-walkthrough)
- [Theme Variants](/docs/styling/theme-variants)
