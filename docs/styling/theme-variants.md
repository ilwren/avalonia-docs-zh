---
id: theme-variants
title: 设置主题变体
---

import OverriddenThemeVariant from '/img/guides/ui-development/overridden-theme-variant.png';
import CustomThemeDictionaries from '/img/guides/ui-development/custom-theme-dictionaries.png';

:::tip
由于主题变体与资源系统深度交织，请先弄懂 Avalonia 的[资源](/docs/app-development/resource-dictionary)。
:::

## 引言 {#introduction}

在 Avalonia 中，*主题变体*指的是控件在某套主题下所呈现的那副特定模样。

借助主题变体，你可以做出既美观又统一、还能随用户偏好或系统设置自动调整的界面。比如应用既可以提供白底黑字的浅色变体，也可以提供黑底白字的深色变体；用户选中自己中意的那套，应用的外观便随之调整。

Avalonia 内置的 `SimpleTheme` 和 `FluentTheme` 两套主题无需额外代码即支持 `Dark` 和 `Light` 变体。于是使用内置控件的应用便能随系统偏好动态适配。若要更深入地定制，本页讲解如何定义随变体而异的自定义资源并引用它们。

## 切换当前主题变体 {#switching-current-theme-variant}

默认情况下，Avalonia 沿用系统全局用户偏好所设定的主题变体。
你的应用可以通过两个重要属性掌控主题变体：[ActualThemeVariant](#actualthemevariant-property) 和 [RequestedThemeVariant](#requestedthemevariant-property)。借助它们，你能在应用的不同层级上管理和切换主题变体。

### `ActualThemeVariant` property

只读属性 `ActualThemeVariant` 给出某个控件、窗口或应用当前正在使用的界面主题，也就是实际生效的那个主题变体。
该属性在每个控件上都有，并沿树向下继承。样式系统访问主题字典时也会用到它的值。

### `RequestedThemeVariant` property

`RequestedThemeVariant` 属性让你能覆盖主题变体，为 `Application`、`Window`（`TopLevel`）或 [`ThemeVariantScope`](/api/avalonia/controls/themevariantscope) 指定想要的变体。

若不想沿用系统默认、而要覆盖应用的全局变体：
```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="AvaloniaApplication.App"
    // highlight-start
             RequestedThemeVariant="Dark">
    // highlight-end
  <Application.Styles>
    <FluentTheme />
  </Application.Styles>
</Application>
```

你还可以用 `ThemeVariantScope` 控件为某一棵子树重新设定主题变体。下面的例子中，窗口用的是 Dark 变体，而内部的 `ThemeVariantScope` 把它改成了 Light 变体：

```xml title="MainWindow.axaml"
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x='http://schemas.microsoft.com/winfx/2006/xaml'
        x:Class="AvaloniaApplication.MainWindow"
    // highlight-start
        RequestedThemeVariant="Dark"
    // highlight-end
        Background="Gray">
  <StackPanel Spacing="5" Margin="5">
    <Button Content="Dark button" />
    // highlight-start
    <ThemeVariantScope RequestedThemeVariant="Light">
    // highlight-end
      <Button Content="Light button" />
    </ThemeVariantScope>
  </StackPanel>
</Window>
```

<Image light={OverriddenThemeVariant} alt="A screenshot of two buttons, demonstrating opposite appearances when dark or light theme settings are overridden." position="center" maxWidth={400} cornerRadius="true"/>

要重置 `RequestedThemeVariant` 的值，请设 `RequestedThemeVariant="Default"`。

:::tip
在支持的平台上，改动窗口的 `RequestedThemeVariant` 也会一并影响窗口装饰的变体。
:::

## 定义并引用随变体而异的自定义资源 {#defining-and-referencing-custom-variant-specific-resources}

在 Avalonia 中，随主题变体而异的资源可以借助 `ThemeDictionaries` 属性定义在 `ResourceDictionary` 里。

通常，开发者用 `Light` 或 `Dark` 作为主题变体的键。用 `Default` 作键，则把该主题字典标记为兜底：当在其他主题字典中找不到相应的主题变体或资源键时就用它。

接着上面的例子，我们来加上 `BackgroundBrush` 和 `ForegroundBrush`，让它们在不同主题变体下取不同的值：
```xml title="MainWindow.axaml"
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x='http://schemas.microsoft.com/winfx/2006/xaml'
        x:Class="Sandbox.MainWindow"
        RequestedThemeVariant="Dark"
        Background="Gray">
  <Window.Resources>
    // highlight-start
    <ResourceDictionary>
      <ResourceDictionary.ThemeDictionaries>
        <ResourceDictionary x:Key='Light'>
          <SolidColorBrush x:Key='BackgroundBrush'>SpringGreen</SolidColorBrush>
          <SolidColorBrush x:Key='ForegroundBrush'>Black</SolidColorBrush>
        </ResourceDictionary>
        <ResourceDictionary x:Key='Dark'>
          <SolidColorBrush x:Key='BackgroundBrush'>DodgerBlue</SolidColorBrush>
          <SolidColorBrush x:Key='ForegroundBrush'>White</SolidColorBrush>
        </ResourceDictionary>
      </ResourceDictionary.ThemeDictionaries>
    </ResourceDictionary>
    // highlight-end
  </Window.Resources>
  
  <Window.Styles>
    // highlight-start
    <Style Selector="Button">
      <Setter Property="Background" Value="{DynamicResource BackgroundBrush}" />
      <Setter Property="Foreground" Value="{DynamicResource ForegroundBrush}" />
    </Style>
    // highlight-end
  </Window.Styles>

  <StackPanel Spacing="5" Margin="5">
    <Button Content="Dark button"
            Background="{DynamicResource BackgroundBrush}"
            Foreground="{DynamicResource ForegroundBrush}" />
    <ThemeVariantScope RequestedThemeVariant="Light">
      <Button Content="Light button"
              Background="{DynamicResource BackgroundBrush}"
              Foreground="{DynamicResource ForegroundBrush}" />
    </ThemeVariantScope>
  </StackPanel>
</Window>

```

<Image light={CustomThemeDictionaries} alt="A screenshot of two brightly colored buttons in blue and green." position="center" maxWidth={400} cornerRadius="true"/>

:::caution
定义在 `ThemeDictionaries` 中的资源，只有用 `DynamicResource` 标记扩展才取得到。`StaticResource` 找不到这些资源，除非 `ResourceDictionary` 中非 `ThemeDictionaries` 的部分也存在同名键的资源，否则会在运行时抛出异常。
:::

关于资源用法的更多细节，请见[资源](/docs/app-development/resource-dictionary)页。

## 另请参阅 {#see-also}

- [资源字典](/docs/app-development/resource-dictionary)
- [Styles](/docs/styling/styles)
- [控件主题](/docs/styling/control-themes)
