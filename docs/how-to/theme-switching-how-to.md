---
id: theme-switching-how-to
title: "操作指南：在浅色与深色主题间切换"
description: 实现浅色/深色主题切换、保存用户的选择，并编写随主题而变的资源。
doc-type: how-to
---

本指南演示如何实现浅色/深色主题切换、保存用户的偏好，以及编写能在主题变化时自动响应的资源。

## 全局设置主题 {#setting-the-theme-globally}

在 `App.axaml` 文件中设置 `RequestedThemeVariant`，即可在应用层面覆盖系统默认值：

```xml title="App.axaml"
<Application RequestedThemeVariant="Dark">
    <Application.Styles>
        <FluentTheme />
    </Application.Styles>
</Application>
```

`RequestedThemeVariant` 属性接受三种取值：

- `Default` 跟随操作系统主题。
- `Light` 强制使用浅色主题。
- `Dark` 强制使用深色主题。

## 在运行时切换主题 {#switching-themes-at-runtime}

要在代码中换主题，请设置当前 `Application` 实例上的 `RequestedThemeVariant`：

```csharp
if (Application.Current is { } app)
{
    app.RequestedThemeVariant = ThemeVariant.Dark;
}
```

### 视图模型中的切换命令 {#toggle-command-in-a-view-model}

你可以把 `ToggleSwitch` 绑定到视图模型的属性，让用户在浅色和深色模式之间切换。下面的例子用了 MVVM Community Toolkit 的源生成器：

```csharp title="SettingsViewModel.cs"
public partial class SettingsViewModel : ObservableObject
{
    [ObservableProperty]
    private bool _isDarkMode;

    partial void OnIsDarkModeChanged(bool value)
    {
        if (Application.Current is { } app)
        {
            app.RequestedThemeVariant = value ? ThemeVariant.Dark : ThemeVariant.Light;
        }
    }
}
```

```xml title="SettingsView.axaml"
<ToggleSwitch IsChecked="{Binding IsDarkMode}"
              OnContent="Dark" OffContent="Light" />
```

### 三选一：浅色、深色、跟随系统 {#three-way-selection-light-dark-system}

若你想再给用户一个跟随操作系统偏好的选项，可以用一个带三个条目的 `ComboBox`，把选择结果映射到 `ThemeVariant.Default`：

```csharp title="SettingsViewModel.cs"
public partial class SettingsViewModel : ObservableObject
{
    [ObservableProperty]
    private string _themeChoice = "System";

    partial void OnThemeChoiceChanged(string value)
    {
        if (Application.Current is not { } app) return;

        app.RequestedThemeVariant = value switch
        {
            "Light" => ThemeVariant.Light,
            "Dark" => ThemeVariant.Dark,
            _ => ThemeVariant.Default // Follow system
        };
    }
}
```

```xml title="SettingsView.axaml"
<ComboBox SelectedItem="{Binding ThemeChoice}">
    <ComboBoxItem Content="System" />
    <ComboBoxItem Content="Light" />
    <ComboBoxItem Content="Dark" />
</ComboBox>
```

## 保存主题选择 {#persisting-the-theme-choice}

要让用户的主题偏好在应用重启后依然有效，请在退出时保存、启动时恢复。下面的例子在 `App.axaml.cs` 重写中载入已保存的偏好：

```csharp title="App.axaml.cs"
public override void OnFrameworkInitializationCompleted()
{
    // Load saved theme
    var settings = new SettingsService().Load();
    RequestedThemeVariant = settings.Theme switch
    {
        "Light" => ThemeVariant.Light,
        "Dark" => ThemeVariant.Dark,
        _ => ThemeVariant.Default
    };

    base.OnFrameworkInitializationCompleted();
}
```

一份完整的、可用来读写用户偏好的 `SettingsService` 实现，请参阅[数据持久化操作指南](/docs/how-to/data-persistence-how-to)。

## 用 ThemeDictionaries 定义随主题而变的颜色 {#theme-aware-colors-with-themedictionaries}

你可以定义随当前主题自动变化的资源：在 `Application.Resources` 里放一个 `ResourceDictionary.ThemeDictionaries` 块，其中分别以 `Light` 和 `Dark` 为键放两本字典：

```xml title="App.axaml"
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.ThemeDictionaries>
            <ResourceDictionary x:Key="Light">
                <SolidColorBrush x:Key="CardBackground" Color="#FFFFFF" />
                <SolidColorBrush x:Key="CardBorder" Color="#E5E7EB" />
                <SolidColorBrush x:Key="TextPrimary" Color="#111827" />
            </ResourceDictionary>
            <ResourceDictionary x:Key="Dark">
                <SolidColorBrush x:Key="CardBackground" Color="#1F2937" />
                <SolidColorBrush x:Key="CardBorder" Color="#374151" />
                <SolidColorBrush x:Key="TextPrimary" Color="#F9FAFB" />
            </ResourceDictionary>
        </ResourceDictionary.ThemeDictionaries>
    </ResourceDictionary>
</Application.Resources>
```

用 `DynamicResource` 引用这些资源，主题一变它们就会更新：

```xml
<Border Background="{DynamicResource CardBackground}"
        BorderBrush="{DynamicResource CardBorder}"
        BorderThickness="1" CornerRadius="8" Padding="16">
    <TextBlock Text="Theme-aware card" Foreground="{DynamicResource TextPrimary}" />
</Border>
```

:::tip
主题变体相关的资源请一律用 `DynamicResource`，而不是 `StaticResource`。`StaticResource` 在加载时解析一次就定下了，用户切换主题后不会更新。
:::

## 用 ThemeVariantScope 混用主题 {#themevariantscope-for-mixed-themes}

你可以用 `ThemeVariantScope` 为界面的某一部分强制指定主题。当你希望窗口的某块区域不受全局设置影响、始终保持固定主题时，这很有用：

```xml
<StackPanel Spacing="16">
    <!-- This section uses light theme regardless of global setting -->
    <ThemeVariantScope RequestedThemeVariant="Light">
        <Border Background="{DynamicResource SystemRegionColor}" Padding="16" CornerRadius="8">
            <TextBlock Text="Always light theme" />
        </Border>
    </ThemeVariantScope>

    <!-- This section uses dark theme -->
    <ThemeVariantScope RequestedThemeVariant="Dark">
        <Border Background="{DynamicResource SystemRegionColor}" Padding="16" CornerRadius="8">
            <TextBlock Text="Always dark theme" />
        </Border>
    </ThemeVariantScope>
</StackPanel>
```

## 判断当前主题 {#detecting-the-current-theme}

你可以通过 `ActualThemeVariant` 属性在运行时查看当前的主题变体。当某些逻辑无法用 XAML 表达时（比如挑选平台专属的资产），这就派上用场了：

```csharp
if (Application.Current is { } app)
{
    var currentTheme = app.ActualThemeVariant;

    if (currentTheme == ThemeVariant.Dark)
    {
        // Dark mode specific logic
    }
}
```

## 响应主题变化 {#responding-to-theme-changes}

订阅 `ActualThemeVariantChanged` 事件，即可在主题变化时作出响应。这适合用来更新非 XAML 的资源，比如图表配色、地图瓦片，或者第三方控件的配置：

```csharp
if (Application.Current is { } app)
{
    app.ActualThemeVariantChanged += (sender, args) =>
    {
        var isDark = app.ActualThemeVariant == ThemeVariant.Dark;
        // Update chart colors, map tiles, and similar resources
    };
}
```

## 自定义主题变体 {#custom-theme-variants}

除了 `Light` 和 `Dark`，你还可以定义自己的具名主题变体。创建一个新的 `ThemeVariant`，并指定一个回退变体，供 Avalonia 在你没有显式定义某些资源时使用：

```csharp
public static class MyThemeVariants
{
    public static readonly ThemeVariant HighContrast = new("HighContrast", ThemeVariant.Light);
}
```

然后用 x:Static 指令，添加一条以你的自定义变体为键的 `ThemeDictionary` 条目：

```xml
<ResourceDictionary.ThemeDictionaries>
    <ResourceDictionary x:Key="{x:Static my:MyThemeVariants.HighContrast}">
        <SolidColorBrush x:Key="CardBackground" Color="Black" />
        <SolidColorBrush x:Key="TextPrimary" Color="Yellow" />
    </ResourceDictionary>
</ResourceDictionary.ThemeDictionaries>
```

要启用自定义变体，像用内置变体那样把它赋给 `RequestedThemeVariant` 即可：

```csharp
app.RequestedThemeVariant = HighContrast;
```

## 另请参阅 {#see-also}

- [主题变体](/docs/styling/theme-variants)：主题变体机制的完整参考。
- [资源字典](/docs/app-development/resource-dictionary)：资源查找与合并的运作方式。
- [主题](/docs/styling/themes)：`FluentTheme` 与 `SimpleTheme` 的配置。
- [数据持久化操作指南](/docs/how-to/data-persistence-how-to)：跨会话保存设置。
