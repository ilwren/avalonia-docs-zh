---
id: custom-font-how-to
title: 如何添加自定义字体
description: 以静态资源或嵌入式字体集合的方式，为 Avalonia 应用添加自定义字体。
doc-type: how-to
---

本指南带你用两种办法为 Avalonia 应用添加自定义字体：作为静态资源，以及作为嵌入式字体集合。

## 前置条件 {#prerequisites}

- 一个 Avalonia 项目。本指南通篇以 [Google Fonts 示例项目](https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/GoogleFonts) 为例，但这些步骤同样适用于你自己的项目。
- 一个字体文件（`.ttf` 或 `.otf`）。本指南用的是 [Nunito](https://fonts.google.com/specimen/Nunito)。

## 把字体文件加入项目 {#add-the-font-files-to-your-project}

1. 把你的字体文件复制到项目中的 **Assets/Fonts** 目录。
2. 打开 `.csproj` 文件，确认该目录已被包含为 `AvaloniaResource`：

```xml title="MyApp.csproj"
<AvaloniaResource Include="Assets\**" />
```

这样字体文件就会嵌入构建输出，Avalonia 在运行时才找得到它们。若你已有一条覆盖 **Assets** 文件夹的 `AvaloniaResource` 条目，就不必再加一条了。

## 方案 A：把字体当作静态资源 {#option-a-use-the-font-as-a-static-resource}

这种办法把字体声明为一个具名的 XAML 资源。

### 声明字体资源 {#declare-the-font-resource}

1. Open **App.axaml**.
2. 按[字体 URI 格式](/docs/styling/custom-fonts#font-uri-format)，在 `<Application.Resources>` 中加入一个 [`FontFamily`](/api/avalonia/media/fontfamily) 资源：

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApp.App"
             RequestedThemeVariant="Default">
    <Application.Styles>
        <FluentTheme />
    </Application.Styles>

    <Application.Resources>
        <FontFamily x:Key="NunitoFont">avares://MyApp/Assets/Fonts#Nunito</FontFamily>
    </Application.Resources>
</Application>
```

把 `MyApp` 换成你的程序集名称，把 `Nunito` 换成字体内部的字族名。

### 套用字体 {#apply-the-font}

3. 打开一个 XAML 视图（比如 **MainWindow.axaml**）。
4. 用 `StaticResource` 标记扩展设置 `FontFamily` 特性：

```xml title="MainWindow.axaml"
<TextBlock Text="Hello in Nunito"
           FontSize="24"
           FontFamily="{StaticResource NunitoFont}" />
```

5. 构建并运行应用，文字应当以你的自定义字体显示。

凡是带 `FontFamily` 属性的控件都能设置 `FontFamily` 特性，所以 `TextBlock`、`Button`、`TextBox` 等控件都能用上你的自定义字体。

## 方案 B：使用嵌入式字体集合 {#option-b-use-an-embedded-font-collection}

这种办法把一整个字体目录注册到自定义的 URI 方案下，让你无需资源键、直接按名字引用字体。

### 创建字体集合类 {#create-the-font-collection-class}

1. 往项目里新增一个 C# 文件（比如 **MyFontCollection.cs**）。
2. 定义一个继承 `EmbeddedFontCollection` 的类：

```csharp title="MyFontCollection.cs"
using System;
using Avalonia.Media.Fonts;

public sealed class MyFontCollection : EmbeddedFontCollection
{
    public MyFontCollection() : base(
        new Uri("fonts:MyFonts", UriKind.Absolute),
        new Uri("avares://MyApp/Assets/Fonts", UriKind.Absolute))
    {
    }
}
```

第一个 URI（`fonts:MyFonts`）是你将在 XAML 中使用的方案和键，第二个 URI 指向存放字体文件的资产目录。请把 `MyApp` 换成你的程序集名称。

### 注册集合 {#register-the-collection}

3. Open **Program.cs**.
4. 用 `AppBuilder.ConfigureFonts` 注册这个集合：

```csharp title="Program.cs"
using Avalonia;
using System;

class Program
{
    [STAThread]
    public static void Main(string[] args) => BuildAvaloniaApp()
        .StartWithClassicDesktopLifetime(args);

    public static AppBuilder BuildAvaloniaApp() =>
        AppBuilder.Configure<App>()
            .UsePlatformDetect()
            .ConfigureFonts(fontManager =>
            {
                fontManager.AddFontCollection(new MyFontCollection());
            })
            .LogToTrace();
}
```

### 套用字体 {#apply-the-font-1}

5. 打开一个 XAML 视图（比如 **MainWindow.axaml**）。
6. 按 `{scheme}:{collection-key}#{font-family-name}` 的格式设置 `FontFamily` 特性：

```xml title="MainWindow.axaml"
<TextBlock Text="Hello in Nunito"
           FontSize="24"
           FontFamily="fonts:MyFonts#Nunito" />
```

7. 构建并运行应用，文字应当以你的自定义字体显示。

想用同一集合中的另一款字体，改一下 `#` 后面的名字即可。例如写成 `fonts:MyFonts#Roboto`，就会从同一个 **Assets/Fonts** 目录加载 Roboto 字体。

## 另请参阅 {#see-also}

- [自定义字体](/docs/styling/custom-fonts)
- [Assets](/docs/fundamentals/including-assets)
