---
id: usercontrol
title: UserControl
description: 一个基类，用于按预先编排好的 XAML 布局创建可复用的组合控件。
doc-type: reference
---

import UserControlStyledProperty from '/static/img/controls/usercontrol/user-control-styled-property.png';

[`UserControl`](/api/avalonia/controls/usercontrol) 是一个 [ContentControl](/controls/data-display/contentcontrol)，它把一组控件按预先编排好的布局组合起来复用。总体而言，要在应用内部造一个可复用的[自定义控件](/docs/custom-controls/)，这是最快的途径。最常见的场景是应用中反复出现的视图或页面，比如设置面板或用户资料卡片。

## 何时使用 `UserControl` {#when-to-use-usercontrol}

在 MVVM 应用中，`UserControl` 是创建视图的标准做法。应用里的每个视图通常都是一个 `UserControl` 子类，并配一个对应的视图模型。

如果你需要的是一个能换皮、跨应用复用的通用控件，请改用[模板化控件](/docs/custom-controls/templated-controls)。如果你需要的控件外观独特、Avalonia [内置控件](/controls/) 里没有，请改用[自绘控件](/docs/custom-controls/custom-drawn-controls)。

## 基本示例 {#basic-example}

### 做一个确认视图 {#creating-a-confirmation-view}

下面的例子做了一个简单的确认视图。这里用 `UserControl` 作为容器，把 [`StackPanel`](/controls/layout/panels/stackpanel)、[`TextBlock`](/controls/data-display/text-display/textblock) 和 [`Button`](/controls/input/buttons/button) 控件组合在一起。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
    <StackPanel Margin="20" Spacing="12">
        <TextBlock Text="Are you sure?"
                   HorizontalAlignment="Center"/>
        <StackPanel Orientation="Horizontal"
                    HorizontalAlignment="Center"
                    Spacing="12">
            <Button Content="Yes" />
            <Button Content="No" />
        </StackPanel>
    </StackPanel>
</UserControl>
```

</XamlPreview>

## 添加代码隐藏 {#adding-code-behind}

在真实项目里，上面演示的这个确认视图通常会单独放在一个名为 `ConfirmationView.axaml` 的 XAML 文件中。要给它加上事件处理、[样式化属性](/docs/custom-controls/defining-properties#styled-properties) 等功能，就得再配一个同名的代码隐藏文件 `ConfirmationView.axaml.cs`。为此需要在 `UserControl` 上设置 `x:Class`，把 XAML 文件与代码中的类关联起来。

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             x:Class="UserControlExample.ConfirmationView">
    <!-- Same control composition as above -->
</UserControl>
```

关于代码隐藏的更多内容，请参阅[代码隐藏](/docs/fundamentals/code-behind)。

### 处理事件 {#handling-events}

下面的例子加上了事件处理逻辑，让确认视图里的「是 / 否」按钮能响应点击。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
    <StackPanel Margin="20" Spacing="12">
        <TextBlock Text="Are you sure?"
                   HorizontalAlignment="Center"/>
        <StackPanel Orientation="Horizontal"
                    HorizontalAlignment="Center"
                    Spacing="12">
            <Button Content="Yes" Click="OnClick" />
            <Button Content="No" Click="OnClick" />
        </StackPanel>
    </StackPanel>
</UserControl>
```

```csharp
using Avalonia.Controls;
using Avalonia.Interactivity;

public partial class ConfirmationView : UserControl
{

    private void OnClick(object? sender, RoutedEventArgs args)
    {
        if (sender is Button button)
        {
            button.Content = "Clicked!";
        }
    }
}

```

</XamlPreview>

### 添加样式化属性 {#adding-a-styled-property}

下面的例子创建了一个名为 `Title` 的样式化属性，用于在 `ConfirmationView` 顶部显示一个可变、可绑定的标题。

:::warning
该样式化属性声明在根 `UserControl` 元素上。要在绑定中用到它，就必须引用那个元素。下面的示例中，`root` 以 `ConfirmationView.axaml` 高亮标出，演示具体写法。
:::

关于绑定到数据上下文的更多内容，请参阅[数据上下文](/docs/data-binding/data-context)。

<br />
<Image light={UserControlStyledProperty} maxWidth={400} position="center" cornerRadius="true" alt="An app window displaying the title text 'Quit the application', which is shown next to the same text coded in a XAML file." />
<br />

<Tabs>

<TabItem value="mainwindow" label="MainWindow.axaml">

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:vm="using:UserControlExample.ViewModels"
        xmlns:local="clr-namespace:UserControlExample"
        x:Class="UserControlExample.Views.MainWindow"
        x:DataType="vm:MainWindowViewModel"
        Title="UserControlExample">

    <local:ConfirmationView Title="Quit the application" />

</Window>
```

</TabItem>

<TabItem value="usercontrol-xaml" label="ConfirmationView.axaml">

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="UserControlExample.ConfirmationView"
             // highlight-next-line
             x:Name="root">

    <StackPanel Margin="20" Spacing="12">
            // highlight-next-line
            <TextBlock Text="{Binding #root.Title}"
                       HorizontalAlignment="Center"
                       FontWeight="Bold" />
            <TextBlock Text="Are you sure?"
                       HorizontalAlignment="Center"/>
            <StackPanel Orientation="Horizontal"
                        HorizontalAlignment="Center"
                        Spacing="12">
                <Button Content="Yes" />
                <Button Content="No" />
            </StackPanel>
        </StackPanel>
    
</UserControl>
```

</TabItem>

<TabItem value="usercontrol-codebehind" label="ConfirmationView.axaml.cs">

```csharp
using Avalonia;
using Avalonia.Controls;

namespace UserControlExample;

public partial class ConfirmationView : UserControl
{
    public ConfirmationView()
    {
        InitializeComponent();
    }
    
    public static readonly StyledProperty<string?> TitleProperty =
        AvaloniaProperty.Register<ConfirmationView, string?>(nameof(Title));
    
    public string? Title
    {
        get => GetValue(TitleProperty);
        set => SetValue(TitleProperty, value);
    }
}
```

</TabItem>

</Tabs>

## 复用用户控件 {#reusing-a-user-control}

要在另一个视图里复用同一个用户控件，先用 `xmlns` 在 `Window` 或任意容器上引用它所在的命名空间，然后[用你为它设定的 `x:Class`](#adding-code-behind) 创建新的实例。

下面演示如何复用上述示例中的那个 `ConfirmationView`：

<Tabs>

<TabItem value="usercontrol" label="UserControl">

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             // highlight-next-line
             x:Class="UserControlExample.ConfirmationView">
    <!-- Same control composition as above -->
</UserControl>
```

</TabItem>

<TabItem value="window" label="Window">

```xml
<Window xmlns:local="clr-namespace:UserControlExample">
    <local:ConfirmationView />
</Window>
```

</TabItem>

</Tabs>

## 另请参阅 {#see-also}

- [ContentControl](/controls/data-display/contentcontrol)
- [创建自定义控件](/docs/custom-controls/)
- [模板化控件](/docs/custom-controls/templated-controls)
- [自绘控件](/docs/custom-controls/custom-drawn-controls)
- [UserControl API 参考](/api/avalonia/controls/usercontrol)
- [GitHub 上的 `UserControl.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/UserControl.cs)
