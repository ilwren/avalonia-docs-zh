---
id: style-best-practices
title: 样式编写的最佳实践
---

本页汇集了在 Avalonia 中编写样式、主题和模板的实用准则。照着这些套路走，样式代码会更好维护、性能也更好。

## 选择器的具体程度 {#selector-specificity}

Avalonia 按声明顺序求值样式选择器。当两个选择器匹配同一个控件、又设了同一个属性时，写在后面的那个胜出。请让你的选择器从宽泛逐步走向具体：

```xml
<!-- General: applies to all Buttons -->
<Style Selector="Button">
    <Setter Property="Background" Value="#6366F1" />
</Style>

<!-- More specific: applies to Buttons with the .primary class -->
<Style Selector="Button.primary">
    <Setter Property="Background" Value="#2563EB" />
</Style>

<!-- Most specific: applies to primary Buttons that are hovered -->
<Style Selector="Button.primary:pointerover">
    <Setter Property="Background" Value="#3B82F6" />
</Style>
```

别用 `*` 或 `:is(Control)` 这类过于宽泛的选择器，它们会匹配树中的每一个控件，可能惹出意料之外的麻烦。

## 用样式类，而不是内联属性 {#use-style-classes-instead-of-inline-properties}

优先用样式类，而不是直接在控件上设属性：

```xml
<!-- Avoid: repeated inline styles -->
<Button Background="#6366F1" Foreground="White" CornerRadius="6" Padding="16,8"
        Content="Save" />
<Button Background="#6366F1" Foreground="White" CornerRadius="6" Padding="16,8"
        Content="Cancel" />

<!-- Prefer: shared style class -->
<Style Selector="Button.action">
    <Setter Property="Background" Value="#6366F1" />
    <Setter Property="Foreground" Value="White" />
    <Setter Property="CornerRadius" Value="6" />
    <Setter Property="Padding" Value="16,8" />
</Style>

<Button Classes="action" Content="Save" />
<Button Classes="action" Content="Cancel" />
```

这样既减少重复，日后改外观也只需动一处。

## 随主题而变的值请用 DynamicResource {#use-dynamicresource-for-theme-aware-values}

引用主题的颜色、字体或尺寸时，请用 `DynamicResource` 而不是写死的值，这样样式才能跟着主题（浅色/深色）变化：

```xml
<Style Selector="Button.themed">
    <Setter Property="Background" Value="{DynamicResource SystemAccentColor}" />
    <Setter Property="Foreground" Value="{DynamicResource SystemControlForegroundBaseHighBrush}" />
</Style>
```

`StaticResource` 只留给运行时绝不会变的值，比如布局常量和自定义转换器。

## 模板要尽量精简 {#keep-templates-minimal}

编写自定义模板时，只绑定模板真正用到的属性。可别为了一点小小的视觉改动就搭一套复杂模板：

```xml
<!-- For a color change, use a style, not a template -->
<Style Selector="Button.custom">
    <Setter Property="Background" Value="Red" />
</Style>

<!-- Only create a template when you need a different visual structure -->
<Style Selector="Button.pill">
    <Setter Property="Template">
        <ControlTemplate>
            <Border Background="{TemplateBinding Background}"
                    CornerRadius="999"
                    Padding="{TemplateBinding Padding}">
                <ContentPresenter Content="{TemplateBinding Content}" />
            </Border>
        </ControlTemplate>
    </Setter>
</Style>
```

## 按作用域组织样式 {#organize-styles-by-scope}

把样式放在视觉树中合适的层级上：

| 作用范围 | 声明位置 | 适用场景 |
|---|---|---|
| Application-wide | `App.axaml`，或由 `App.axaml` 引用的 `Styles` 文件 | 品牌色、排版、控件的默认主题 |
| 窗口/页面级 | `<Window.Styles>` or `<UserControl.Styles>` | 页面专属的覆写 |
| Control-level | `<Control.Styles>` | 不该外泄的组件专属样式 |

```xml
<!-- App.axaml: global styles -->
<Application.Styles>
    <FluentTheme />
    <StyleInclude Source="avares://MyApp/Styles/Global.axaml" />
</Application.Styles>
```

```xml
<!-- A page-specific override -->
<UserControl.Styles>
    <Style Selector="TextBlock.page-title">
        <Setter Property="FontSize" Value="28" />
        <Setter Property="FontWeight" Value="Bold" />
    </Style>
</UserControl.Styles>
```

## 别搞 !important 那一套 {#avoid-important-style-hacks}

Avalonia 没有 CSS 那样的 `!important`。若你的样式没生效，原因通常是：

1. **另一个写在后面的样式把它盖掉了**：调整样式顺序即可。
2. **本地值优先**：直接设在控件上的本地值会盖过样式值。要么去掉本地值，要么改用样式。
3. **被控件主题盖掉了**：控件主题里含有伪类样式，具体程度可能更高。

用 DevTools（F12）即可查看某个属性最终是哪个值来源胜出。

## 命名约定 {#naming-conventions}

样式类用 kebab-case 命名，与 CSS 的惯例保持一致：

```xml
<!-- Good -->
<Button Classes="btn-primary" />
<Border Classes="card-elevated" />

<!-- Also acceptable: single words -->
<Button Classes="primary" />
```

模板部件则用 `PART_` 前缀：

```xml
<Border x:Name="PART_Background" />
<ContentPresenter x:Name="PART_ContentPresenter" />
```

## 为状态变化加上过渡 {#transitions-for-state-changes}

加上过渡，让伪类状态的切换显得顺滑：

```xml
<Style Selector="Button.smooth">
    <Setter Property="Transitions">
        <Transitions>
            <BrushTransition Property="Background" Duration="0:0:0.15" />
            <DoubleTransition Property="Opacity" Duration="0:0:0.15" />
        </Transitions>
    </Setter>
</Style>
```

过渡时长要短（100ms 到 300ms）。动画拖得太久会显得迟钝，也耽误给用户的反馈。

## 各主题都要试 {#test-across-themes}

若你的应用同时支持浅色和深色主题，自定义样式在两种主题下都要试一遍。用 `ThemeVariant` 资源为各主题提供不同的值：

```xml
<Style Selector="Border.card">
    <Setter Property="Background">
        <Setter.Value>
            <SolidColorBrush x:Key="CardBackground">
                <SolidColorBrush.Color>
                    <OnPlatform Default="White" />
                </SolidColorBrush.Color>
            </SolidColorBrush>
        </Setter.Value>
    </Setter>
</Style>
```

也可以使用定义在 `App.axaml` 中的主题变体资源：

```xml
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.ThemeDictionaries>
            <ResourceDictionary x:Key="Light">
                <Color x:Key="CardColor">#FFFFFF</Color>
            </ResourceDictionary>
            <ResourceDictionary x:Key="Dark">
                <Color x:Key="CardColor">#1E1E1E</Color>
            </ResourceDictionary>
        </ResourceDictionary.ThemeDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

## 另请参阅 {#see-also}

- [Styles](/docs/styling/styles)
- [样式类](/docs/styling/style-classes)
- [样式选择器](/docs/styling/style-selectors)
- [控件主题](/docs/styling/control-themes)
- [主题变体](/docs/styling/theme-variants)
- [共享样式](/docs/styling/sharing-styles)
