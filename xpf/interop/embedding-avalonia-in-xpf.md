---
id: embedding-avalonia-in-xpf
title: 在 XPF 中嵌入 Avalonia
---

## 嵌入 Avalonia 控件 {#embedding-avalonia-controls}

### 第 1 步：添加 Avalonia `UserControl` {#step-1-add-an-avalonia-usercontrol}

在应用中添加一个 Avalonia `UserControl`，用来放你想承载的 Avalonia 内容。例如：

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
             mc:Ignorable="d" d:DesignWidth="800" d:DesignHeight="450"
             x:Class="MyXpfApplication.MyAvaloniaView">
  <Button>Hello Avalonia!</Button>
</UserControl>
```

```csharp
using Avalonia.Controls;

namespace MyXpfApplication;

public partial class MyAvaloniaView : UserControl
{
    public MyAvaloniaView()
    {
        InitializeComponent();
    }
}
```

### 第 2 步：承载 Avalonia `UserControl` {#step-2-host-the-avalonia-usercontrol}

实例化一个 `AvaloniaHost`，把 Avalonia 内容承载到 XPF 控件中：

```xml
<Window x:Class="MyXpfApplication.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        xmlns:local="clr-namespace:MyXpfApplication"
        // highlight-next-line
        xmlns:xpf="clr-namespace:Atlantis;assembly=PresentationCore"
        mc:Ignorable="d"
        Title="MainWindow">
  // highlight-start
  <xpf:AvaloniaHost>
    <local:MyAvaloniaView/>
  </xpf:AvaloniaHost>
  // highlight-end
</Window>
```

## 为 Avalonia 控件设置样式 {#styling-avalonia-controls}

在 XPF 中，只能通过代码隐藏给 Avalonia 控件加 Style。可参照下面的示例。

### XAML 代码 {#xaml-code}

下面这段 XAML 示例演示了如何把 Avalonia 控件（这里是一个 `Button`）嵌进 XPF 的 `Window`：

```xml
<Window
    x:Class="YourNamespace.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:atlantis="clr-namespace:Atlantis;assembly=PresentationCore"
    xmlns:avalonia="clr-namespace:Avalonia.Controls;assembly=Avalonia.Controls"
    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    Title="Avalonia Embedded in XPF"
    Width="800"
    Height="450"
    mc:Ignorable="d">
    <atlantis:AvaloniaHost>
        <!-- Avalonia control within AvaloniaHost -->
        <avalonia:Button Content="Click me" x:Name="myButton" />
    </atlantis:AvaloniaHost>
</Window>
```

### 代码隐藏中的 C# 代码 {#code-behind-c-code}

在代码隐藏文件（`MainWindow.xaml.cs`）中，你可以借助 `Styles` 属性给 Avalonia 控件套样式。下面的 C# 代码演示了如何为 Avalonia 的 `Button` 写一条样式：

```csharp
using Avalonia.Styling;
using System.Linq;
using System.Windows;
using Setter = Avalonia.Styling.Setter;
using Style = Avalonia.Styling.Style;
using Button = Avalonia.Controls.Button;
using SolidColorBrush = Avalonia.Media.SolidColorBrush;

namespace YourNamespace
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        public MainWindow()
        {
            InitializeComponent();

            // Create a style for the Button
            var myButtonStyle = new Style(x => x.OfType<Button>())
            {
                Setters = 
                {
                    new Setter(Button.BackgroundProperty, new SolidColorBrush(Avalonia.Media.Colors.Green)),
                    new Setter(Button.ForegroundProperty, new SolidColorBrush(Avalonia.Media.Colors.Red))
                    // Add more setters as needed
                }
            };

            // Apply the style to the Button
            myButton.Styles.Add(myButtonStyle);
        }

    }
}
```
记得把 “YourNamespace” 换成你项目实际的命名空间。这个例子把嵌在 XPF 中的 Avalonia `Button` 的背景设成绿色、前景设成红色。setter 和其他属性请按你自己的样式需求调整。几步都照做下来，你的 Avalonia 控件就会按样式变了模样。

## 动态添加全局样式 {#adding-global-styles-dynamically}

在代码隐藏中动态为 Avalonia 控件添加全局样式颇为灵活，样式可以在运行时套上去。
用下面这段 C# 代码即可：
```csharp
 // Retrieve the current Avalonia application instance
var avaloniaApp = Avalonia.Controls.Application.Current;

// Dynamically add a global style for Button controls
avaloniaApp.Styles.Add(new StyleInclude()
{
    Source = new Uri("avares://YourNamespace/Styles/CustomStyles.xaml") // Adjust the URI accordingly
});
```
这里的 “CustomStyles.xaml” 就是存放你想全局应用的 Avalonia 样式的那个 XAML 文件。

### 搭配自定义 Avalonia 应用类 {#with-a-custom-avalonia-application}
在更高阶的场景下，你可能想把默认套用的样式整个换成自己的，这就得重新定义 Avalonia Application 了。第一步是关掉 XPF 的自动初始化。
```xml
  <PropertyGroup>
    <DisableAutomaticXpfInit>true</DisableAutomaticXpfInit>
  </PropertyGroup>
```
接着你要新建一个带 XAML 和代码隐藏的 Avalonia Application，把想全局生效的样式写在 XAML 里。

:::note
DevTools 要正常工作，`DataGrid` 主题是必需的。
:::

```xml
 <StyleInclude Source="avares://Avalonia.Controls.DataGrid/Themes/Simple.xaml"/>
```

之后还要再建一个类，由它为你的 XPF 项目初始化 Avalonia。 

```csharp
public class MyXpfAvaloniaInitializer
{
    [ModuleInitializer]
    public static void Init()
    {
        if (Avalonia.Application.Current == null)
        {
            AppBuilder.Configure<MyApp>()
                .UsePlatformDetect()
                .With(new Win32PlatformOptions()
                {
                    // Default to System Dpi Aware. If process has a different awareness set in manifest, that value will be prioritized by the os
                    DpiAwareness = Win32DpiAwareness.SystemDpiAware
                })
                .WithAvaloniaXpf()
                .SetupWithLifetime(new ClassicDesktopStyleApplicationLifetime() { ShutdownMode = Avalonia.Controls.ShutdownMode.OnExplicitShutdown });
        }
    }
}
```

:::note
这里的 `ModuleInitializer` 特性不是必须的。你完全可以在任何地方自行初始化 Avalonia，但要记住一点：Avalonia 的初始化必须赶在 WPF 初始化之前。这一点对用 F# 搭配 XPF 的人尤其有用。
:::

这么一来，你的样式就会作用于整个应用了。

## 用上 Avalonia 的能力 {#accessing-avalonia-features}

有时 WPF 的 API 给不了你想要的功能，这时候往往能找到一个 Avalonia 的 API 来补上这个缺口。

## 取得 Avalonia 窗口 {#getting-the-avalonia-window}

Avalonia 的许多能力都挂在顶层的 `Window` 类上。由于 XPF 的 `Window` 同时也是一个 Avalonia `Window`，你可以用下面这个写法拿到底层的 Avalonia `Window`：

```csharp
if (XpfWpfAbstraction.GetAvaloniaWindowForWindow(xpfWindow) is { } avaloniaWindow)
{
    // You now have an Avalonia Window.
}
```
