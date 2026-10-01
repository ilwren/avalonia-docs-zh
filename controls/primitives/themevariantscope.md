---
id: themevariantscope
title: ThemeVariantScope
description: 一个基础控件，用于为视觉树的某一部分覆盖当前生效的主题变体（浅色或深色）。
doc-type: reference
---

[`ThemeVariantScope`](/api/avalonia/controls/themevariantscope) 控件为视觉树的某一部分覆盖当前生效的主题变体（浅色或深色）。放进 `ThemeVariantScope` 里的所有控件都会采用指定的变体，与应用或窗口的设置无关。当你希望界面的一部分采用与整体不同的主题时，它正好派上用场。

## 常见用法 {#common-use-cases}

- 让侧边栏或某个面板始终以深色呈现，而应用其余部分用浅色。
- 在设置页面上并排预览两种主题变体。
- 在布局中营造明暗对比的区域，突出重点。

## 常用属性 {#useful-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `RequestedThemeVariant` | `ThemeVariant` | 该作用域内要应用的主题变体，取值为 `Light`、`Dark`、`Default`。设为 `Default` 则恢复为继承而来的变体。 |
| `ActualThemeVariant` | `ThemeVariant` | 只读。该作用域内当前实际生效的主题变体。 |

## 基本示例 {#basic-example}

你可以让界面的一部分强制使用浅色主题，而窗口其余部分用深色主题：

```xml
<Window RequestedThemeVariant="Dark">
    <StackPanel Spacing="8" Margin="16">
        <Button Content="Dark-themed button" />

        <ThemeVariantScope RequestedThemeVariant="Light">
            <StackPanel Spacing="8">
                <Button Content="Light-themed button" />
                <TextBox PlaceholderText="Light-themed input" />
            </StackPanel>
        </ThemeVariantScope>
    </StackPanel>
</Window>
```

## 并排预览主题 {#side-by-side-theme-preview}

一种常见用法是同时展示两种主题变体，比如在主题设置页面上：

```xml
<Grid ColumnDefinitions="*,*" Margin="16">
    <ThemeVariantScope Grid.Column="0" RequestedThemeVariant="Light">
        <Border Background="{DynamicResource SystemControlBackgroundAltHighBrush}"
                Padding="16" CornerRadius="8">
            <StackPanel Spacing="8">
                <TextBlock Text="Light Theme" FontWeight="SemiBold" />
                <Button Content="Sample Button" />
                <CheckBox Content="Sample Checkbox" IsChecked="True" />
                <Slider Value="60" />
            </StackPanel>
        </Border>
    </ThemeVariantScope>

    <ThemeVariantScope Grid.Column="1" RequestedThemeVariant="Dark">
        <Border Background="{DynamicResource SystemControlBackgroundAltHighBrush}"
                Padding="16" CornerRadius="8">
            <StackPanel Spacing="8">
                <TextBlock Text="Dark Theme" FontWeight="SemiBold" />
                <Button Content="Sample Button" />
                <CheckBox Content="Sample Checkbox" IsChecked="True" />
                <Slider Value="60" />
            </StackPanel>
        </Border>
    </ThemeVariantScope>
</Grid>
```

## 恢复为继承的变体 {#resetting-to-the-inherited-variant}

设为 `RequestedThemeVariant="Default"` 即可清除覆盖，转而继承父作用域的变体：

```xml
<ThemeVariantScope RequestedThemeVariant="Light">
    <StackPanel>
        <!-- These use the Light variant -->
        <Button Content="Light" />

        <ThemeVariantScope RequestedThemeVariant="Default">
            <!-- These inherit from the window/application -->
            <Button Content="Inherited" />
        </ThemeVariantScope>
    </StackPanel>
</ThemeVariantScope>
```

## 嵌套作用域 {#nesting-scopes}

`ThemeVariantScope` 控件可以嵌套，从而划分出多个主题区域。每个作用域各自独立解析变体，因此子作用域会覆盖父作用域的设置：

```xml
<ThemeVariantScope RequestedThemeVariant="Dark">
    <!-- Everything here uses the dark variant -->
    <StackPanel Spacing="8">
        <Button Content="Dark button" />

        <ThemeVariantScope RequestedThemeVariant="Light">
            <!-- This region switches to light -->
            <Button Content="Light button inside dark scope" />
        </ThemeVariantScope>
    </StackPanel>
</ThemeVariantScope>
```

## 随主题变化的资源 {#theme-aware-resources}

定义在 `ThemeDictionaries` 中的资源会响应 `ThemeVariantScope`。每个作用域各自独立解析变体，因此同一个 `DynamicResource` 键出现在不同作用域里时，可能返回不同的值：

```xml
<Window.Resources>
    <ResourceDictionary>
        <ResourceDictionary.ThemeDictionaries>
            <ResourceDictionary x:Key="Light">
                <SolidColorBrush x:Key="CardBrush">White</SolidColorBrush>
            </ResourceDictionary>
            <ResourceDictionary x:Key="Dark">
                <SolidColorBrush x:Key="CardBrush">#1E1E1E</SolidColorBrush>
            </ResourceDictionary>
        </ResourceDictionary.ThemeDictionaries>
    </ResourceDictionary>
</Window.Resources>
```

```xml
<ThemeVariantScope RequestedThemeVariant="Light">
    <!-- Uses White -->
    <Border Background="{DynamicResource CardBrush}" />
</ThemeVariantScope>

<ThemeVariantScope RequestedThemeVariant="Dark">
    <!-- Uses #1E1E1E -->
    <Border Background="{DynamicResource CardBrush}" />
</ThemeVariantScope>
```

## 在代码中设置变体 {#setting-the-variant-from-code}

在代码隐藏中设置 `RequestedThemeVariant`，即可在运行时切换变体：

```csharp
myScope.RequestedThemeVariant = ThemeVariant.Dark;
```

也可以把该属性绑定到视图模型，让用户自己动态切换主题：

```xml
<ThemeVariantScope RequestedThemeVariant="{Binding SelectedTheme}">
    <ContentControl Content="{Binding CurrentPage}" />
</ThemeVariantScope>
```

```csharp
public class MainViewModel : ViewModelBase
{
    private ThemeVariant _selectedTheme = ThemeVariant.Default;

    public ThemeVariant SelectedTheme
    {
        get => _selectedTheme;
        set => this.RaiseAndSetIfChanged(ref _selectedTheme, value);
    }
}
```

## 另请参阅 {#see-also}

- [主题变体](/docs/styling/theme-variants)：浅色/深色主题支持与主题词典的完整指南。
- [如何切换主题](/docs/how-to/theme-switching-how-to)：在应用中实现主题切换。
- [资源](/docs/app-development/resources)：资源系统概览。
