---
id: resources
title: 资源概述
description: 定义、引用并管理可复用的 XAML 资源、合并字典与主题变体。
doc-type: overview
---

Avalonia 中的资源是在 XAML 里定义、可在整个应用中共享的可复用对象。画刷、颜色、粗细值、字符串和样式通常都会定义成资源，以保证视觉一致、便于维护。

## 定义资源 {#defining-resources}

资源存放在 `ResourceDictionary` 集合中，你可以在任意元素的 `Resources` 属性上声明它。每个资源都必须有 `x:Key`：

```xml
<Application.Resources>
    <SolidColorBrush x:Key="PrimaryBrush" Color="#6366F1" />
    <SolidColorBrush x:Key="DangerBrush" Color="#EF4444" />
    <x:Double x:Key="DefaultSpacing">8</x:Double>
    <Thickness x:Key="PagePadding">24,16</Thickness>
</Application.Resources>
```

资源可以定义在树的任意层级上：

| 层级 | 作用范围 |
|---|---|
| `Application.Resources` | 整个应用中随处可用 |
| `Window.Resources` | 在该窗口内可用 |
| `UserControl.Resources` | 在该用户控件内可用 |
| 任意控件的 `.Resources` | 在该控件及其后代中可用 |
| `Style.Resources` | 仅在该样式块内可用 |

## 使用资源 {#using-resources}

### StaticResource

`StaticResource` 在 XAML 加载时做一次性查找：

```xml
<Button Background="{StaticResource PrimaryBrush}" />
<StackPanel Spacing="{StaticResource DefaultSpacing}" />
```

若找不到该资源，运行时会抛出异常。

### DynamicResource

`DynamicResource` 会持续关注变化，一旦资源的值在运行时改变（比如切换主题），就会自动更新：

```xml
<TextBlock Foreground="{DynamicResource SystemAccentColor}" />
<Border Background="{DynamicResource WindowBackgroundBrush}" />
```

### 各自适用的场景 {#when-to-use-each}

| 用法 | 适用情形 |
|---|---|
| `StaticResource` | 资源值在运行时永远不变。查找略快一些。 |
| `DynamicResource` | 资源可能发生变化（切换主题、用户偏好、运行时更新）。 |

:::tip
需要随主题变化的颜色、画刷和尺寸，用 `DynamicResource`；数据模板、转换器等保持不变的结构性资源，用 `StaticResource`。
:::

## 资源查找顺序 {#resource-lookup-order}

引用资源时，Avalonia 会从引用所在的元素出发，沿逻辑树向上查找：

1. 该元素自己的 `Resources` 字典
2. 该层级上的合并字典
3. 父元素的 `Resources`（及其合并字典）
4. 继续沿逻辑树往上
5. 各层级上的样式资源
6. `Application.Resources` 及其合并字典
7. 主题资源

第一个匹配到的即告胜出。也就是说，离使用点越近的资源定义，会覆盖更上层的定义。

## 合并字典 {#merged-dictionaries}

你可以把资源分散到不同文件中，再合并进任意 `ResourceDictionary`：

```xml title="Resources/Colors.axaml"
<ResourceDictionary xmlns="https://github.com/avaloniaui"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <SolidColorBrush x:Key="PrimaryBrush" Color="#6366F1" />
    <SolidColorBrush x:Key="SecondaryBrush" Color="#8B5CF6" />
</ResourceDictionary>
```

```xml title="App.axaml"
<Application.Resources>
    <ResourceDictionary>
        <ResourceDictionary.MergedDictionaries>
            <ResourceInclude Source="/Resources/Colors.axaml" />
            <ResourceInclude Source="/Resources/Sizes.axaml" />
        </ResourceDictionary.MergedDictionaries>
        <!-- Additional inline resources -->
        <x:String x:Key="AppName">My Application</x:String>
    </ResourceDictionary>
</Application.Resources>
```

### MergeResourceInclude 与 ResourceInclude 的区别 {#mergeresourceinclude-vs-resourceinclude}

| 类型 | 行为 |
|---|---|
| `ResourceInclude` | 创建一个独立的资源字典作用域，属于标准的资源文件引入方式。 |
| `MergeResourceInclude` | 把资源直接合并进父字典，使用起来就跟内联定义的一样。 |

## 主题变体资源 {#theme-variant-resources}

用 `ThemeDictionaries` 为浅色和深色主题定义不同的资源值：

```xml
<ResourceDictionary>
    <ResourceDictionary.ThemeDictionaries>
        <ResourceDictionary x:Key="Light">
            <SolidColorBrush x:Key="CardBackground" Color="White" />
            <SolidColorBrush x:Key="CardForeground" Color="#1A1A1A" />
        </ResourceDictionary>
        <ResourceDictionary x:Key="Dark">
            <SolidColorBrush x:Key="CardBackground" Color="#2D2D2D" />
            <SolidColorBrush x:Key="CardForeground" Color="#FAFAFA" />
        </ResourceDictionary>
    </ResourceDictionary.ThemeDictionaries>
</ResourceDictionary>
```

引用主题变体资源时请用 `DynamicResource`，这样主题切换时它们才会随之更新：

```xml
<Border Background="{DynamicResource CardBackground}">
    <TextBlock Foreground="{DynamicResource CardForeground}" Text="Hello" />
</Border>
```

## 在代码中访问资源 {#accessing-resources-from-code}

Avalonia 提供四种以编程方式访问资源的方法：

```csharp
// Direct dictionary access (does not search merged dictionaries or parent elements)
var brush = (SolidColorBrush)this.Resources["PrimaryBrush"];

// Search merged dictionaries at the current level only
if (this.TryGetResource("PrimaryBrush", this.ActualThemeVariant, out var result))
{
    // result contains the resource value
}

// Search the full logical tree (most common usage)
if (this.TryFindResource("PrimaryBrush", this.ActualThemeVariant, out var found))
{
    // found contains the resource value from anywhere in the tree
}

// Observable for runtime changes
myBorder.Bind(Border.BackgroundProperty,
    this.GetResourceObservable("PrimaryBrush"));
```

| 方法 | 查找合并字典 | 查找父元素 |
|---|---|---|
| `Resources["key"]` | No | No |
| `TryGetResource` | Yes | No |
| `TryFindResource` | Yes | Yes |
| `GetResourceObservable` | Yes | 是（并会持续关注变化） |

## 在运行时更新资源 {#updating-resources-at-runtime}

你可以在代码中修改资源，动态改变应用的外观：

```csharp
// Update a resource (DynamicResource references update automatically)
Application.Current!.Resources["PrimaryBrush"] =
    new SolidColorBrush(Colors.Red);
```

只有 `DynamicResource` 引用会响应运行时的资源变化，`StaticResource` 引用则保持最初的取值。

## 另请参阅 {#see-also}

- [资源字典](/docs/app-development/resource-dictionary)：创建和组织资源字典的分步指南。
- [主题变体](/docs/styling/theme-variants)：随主题变化的资源是怎么工作的。
- [样式](/docs/styling/styles)：在样式定义中使用资源。
- [共享样式](/docs/styling/sharing-styles)：组织并共享样式资源。
