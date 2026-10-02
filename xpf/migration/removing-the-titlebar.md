---
id: removing-the-titlebar
title: 去掉标题栏
---

XPF 应用默认带有用于窗口管理的标题栏。不过有时你会想把它去掉。本指南带你走一遍这个过程。
本文介绍两种定制窗口外观的路子：用 WPF API，和用 Avalonia API。
用 WPF API 也能去掉标题栏，但 Avalonia API 在标题栏设置上更灵活、掌控力更强，因此推荐走 Avalonia 这条路。

## Using WPF APIs
在 WPF 中，把 `WindowStyle` 属性设为 `None` 即可去掉窗口标题栏。此外你多半还想把 `AllowsTransparency` 属性设为 `True`，连窗口的缩放边框也一并去掉。
```xml
<Window x:Class="YourNamespace.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Your Window Title" Height="350" Width="525"
        WindowStyle="None" AllowsTransparency="True">
    <!-- Your content goes here -->
</Window>
```

:::note
要留意的是，去掉标题栏之后，默认的标题栏功能也就没了，窗口的拖动、缩放和关闭可能都得你自己写控件来实现。
:::

```csharp
using System.Windows;

namespace YourNamespace
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Window_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            DragMove();
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }
    }
}
```

而在 XAML 中，你要这样挂上事件处理程序：

```xml
<Window x:Class="YourNamespace.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Your Window Title" Height="350" Width="525"
        WindowStyle="None" AllowsTransparency="True"
        MouseLeftButtonDown="Window_MouseLeftButtonDown">
    <!-- Your content goes here -->

    <!-- Close button example -->
    <Button Content="X" HorizontalAlignment="Right" VerticalAlignment="Top" Margin="0,5,5,0" Click="CloseButton_Click"/>
</Window>
```

这个例子只是个基础骨架，你得按自己的实际需求和想提供的功能再做调整。

## Using Avalonia APIs

首先找到 `MainWindow.xaml.cs` 文件，然后把下面的代码粘进去就行。

```csharp
protected override void OnSourceInitialized(EventArgs e)
{
    base.OnSourceInitialized(e);

    if (XpfWpfAbstraction.IsRunningOnXpf)
    {
        if (XpfWpfAbstraction.GetAvaloniaWindowForWindow(this) is { } window)
        {
            window.ExtendClientAreaToDecorationsHint = true;
            window.ExtendClientAreaChromeHints = Avalonia.Platform.ExtendClientAreaChromeHints.NoChrome;
        }

    }
}
```
`ExtendClientAreaToDecorationsHint` 负责去掉标题栏，但关闭、最小化和全屏按钮还在。
若连这些也不想要，就得把 `ExtendClientAreaChromeHints` 设为 `NoChrome`。

:::note
请注意，这么设置之后窗口会拖不动，因为 XpfHost 控件上的 `IsHitTestVisible` 被设为了 `True`，点击事件都被它吞了。要解决这个问题，比如可以给它上方加一道外边距，把那块区域留给标题栏。
:::
