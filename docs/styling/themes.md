---
id: themes
title: 主题
---

import FluentThemeNormalScreenshot from '/img/concepts/ui-concepts/styling/fluent-theme-normal.png';
import FluentThemeForestScreenshot from '/img/concepts/ui-concepts/styling/fluent-theme-forest.png';
import SimpleThemeScreenshot from '/img/concepts/ui-concepts/styling/simple-theme.png';

在 Avalonia 中，主题是面向内置控件的一整套[控件主题](/docs/styling/control-themes)与[主题资源](/docs/styling/theme-variants)。

## 官方主题 {#official-themes}

Avalonia 内置了两套主题：

### Fluent 主题 {#fluent-theme}

- [Fluent 主题](#fluent)是一套现代主题，灵感来自[微软的 Fluent 设计体系](https://en.wikipedia.org/wiki/Fluent_Design_System)。

### Simple 主题 {#simple-theme}

- [Simple 主题](#simple)极简轻量，内置样式很有限。

## 社区主题 {#community-themes}

社区开发的主题也有不少，成熟度各异。

### Material.Avalonia 

- [Material.Avalonia](https://github.com/AvaloniaCommunity/Material.Avalonia) 是一套现代主题，灵感来自[谷歌的 Material 设计体系](https://m3.material.io/)。

### Semi.Avalonia

- [Semi.Avalonia](https://github.com/irihitech/Semi.Avalonia) 的灵感来自 [Semi Design](https://semi.design/en-US)
  
### Classic.Avalonia

- [Classic.Avalonia](https://github.com/BAndysc/Classic.Avalonia) 是一套怀旧主题，灵感来自 Windows 9x 系列的设计。

## Fluent

Avalonia 的 Fluent 主题灵感源自微软的 Fluent 设计体系——一套用于打造美观、可交互界面的设计准则与组件。Fluent 设计体系讲究现代而清爽的观感、顺滑的动画和符合直觉的交互，能在各平台之间给出一致且精致的外观，同时又借助 Avalonia 的样式系统为开发者留足了发挥余地。

<Image light={FluentThemeNormalScreenshot} alt="Fluent theme" position="center" maxWidth={400} cornerRadius="true" />

### 怎么用 {#how-to-use}

首先，安装 [Avalonia.Themes.Fluent](https://www.nuget.org/packages/Avalonia.Themes.Fluent/) NuGet 包。

:::info
关于如何添加 NuGet 包，请参阅 [Visual Studio](https://learn.microsoft.com/en-us/nuget/quickstart/install-and-use-a-package-in-visual-studio) 或 [Rider](https://www.jetbrains.com/help/rider/Using_NuGet.html) 的文档。
:::

然后在 `Application` 类中引入该主题：

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="AvaloniaApplication.App">
  <Application.Styles>
    // highlight-start
    <FluentTheme />
    // highlight-end
  </Application.Styles>
</Application>
```

:::note
若你需要指定深色或浅色变体，请见[主题变体](/docs/styling/theme-variants)。
:::

### 调整主题密度 {#changing-theme-density}

Fluent 主题预置了两套密度变体。
要切换到更紧凑的观感，请设置 `DensityStyle` 属性：

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="AvaloniaApplication.App">
  <Application.Styles>
    // highlight-start
    <FluentTheme DensityStyle="Compact" />
    // highlight-end
  </Application.Styles>
</Application>
```

### 自定义配色方案 {#creating-custom-color-palettes}

`FluentTheme` 虽然为深色和浅色变体内置了资源，但你可以覆盖这些变体的基础调色板。
当你想沿用同一套主题、只换配色时，这就很有用。

做法是为每个变体定义自定义的 `ColorPaletteResources`：

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="AvaloniaApplication.App">
  <Application.Styles>
    <FluentTheme>
    // highlight-start
      <FluentTheme.Palettes>
        <!-- Palette for Light theme variant -->
        <ColorPaletteResources x:Key="Light" Accent="Green" RegionColor="White" ErrorText="Red" />
        <!-- Palette for Dark theme variant -->
        <ColorPaletteResources x:Key="Dark" Accent="DarkGreen" RegionColor="Black" ErrorText="Yellow" />
      </FluentTheme.Palettes>
    // highlight-end
    </FluentTheme>
  </Application.Styles>
</Application>
```

`ColorPaletteResources` 有许多颜色属性，可为每个变体单独覆盖。你只需重新定义想改的那几项，其余的照旧取默认值。上面的例子只覆盖了寥寥几种颜色。

若未覆盖 `Accent`，Avalonia 会在可用时取系统的强调色。
`Accent` 支持绑定，可在运行时更改；出于性能考虑，调色板的其他属性只在启动时读取一次，此后便固定不变。

你也可以在代码隐藏中构造调色板，但规矩照旧：只有 `Accent` 能动态更新。

:::note
FluentTheme 只支持 Dark 和 Light 两种主题变体，无法为自定义变体定义调色板。
:::

### 用在线编辑器自定义配色方案 {#creating-custom-color-palettes-with-online-editor}

微软的 Fluent 主题编辑器已被移植到 Avalonia，可配合 `FluentTheme` 使用。
[Avalonia 主题编辑器](https://theme.xaml.live/)支持以下功能：

1. 分别编辑 Light 与 Dark 变体的调色板颜色。
2. 预览当前调色板。
3. 把当前调色板导出为 XAML 代码，可直接粘进你的 `App.axaml` 文件。
4. 把当前配色存成 json 文件，也可从文件系统中加载。
5. 当调色板中颜色对比度偏低时自动给出提示。
6. 开箱即用的预设方案。

下图是该 Web 应用中 FluentTheme 搭配 Forest 预设调色板的效果：

<Image light={FluentThemeForestScreenshot} alt="Fluent theme forest palette" position="center" maxWidth={400} cornerRadius="true" />

## Simple

Avalonia 的 Simple 主题走的是极简轻量路线，内置样式很有限，正好为自定义样式打下一块干净的底子。它在视觉和结构上都足够简单，很适合跑在嵌入式设备上的应用。

<Image light={SimpleThemeScreenshot} alt="A screenshot of a user interface, demonstrating the appearances of various UI controls using a simple design theme." position="center" maxWidth={400} cornerRadius="true"/>

### 怎么用 {#how-to-use-1}

首先，安装 [Avalonia.Themes.Simple](https://www.nuget.org/packages/Avalonia.Themes.Simple/) NuGet 包。

:::info
关于如何添加 NuGet 包，请参阅 [Visual Studio](https://learn.microsoft.com/en-us/nuget/quickstart/install-and-use-a-package-in-visual-studio) 或 [Rider](https://www.jetbrains.com/help/rider/Using_NuGet.html) 的文档。
:::

然后在 `Application` 类中引入该主题：

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="AvaloniaApplication.App">
  <Application.Styles>
    // highlight-start
    <SimpleTheme />
    // highlight-end
  </Application.Styles>
</Application>

```

:::note
若你需要指定深色或浅色变体，请见[主题变体](/docs/styling/theme-variants)。
:::

## 另请参阅 {#see-also}

- [控件主题](/docs/styling/control-themes)
- [主题变体](/docs/styling/theme-variants)
- [Styles](/docs/styling/styles)