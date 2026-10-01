---
id: custom-flyout
title: Custom Flyout
description: 如何通过扩展 PopupFlyoutBase 做一个自定义浮出控件。
doc-type: how-to
---

import CustomFlyoutDemo from '/img/custom-controls/custom-flyout-demo.gif';

本例演示如何派生 `PopupFlyoutBase` 做一个自定义 `Flyout` 控件。自定义浮出控件可以呈现一块自成一体、用途灵活的界面，按需弹出并依附于你指定的目标控件。它几乎能装下任何内容，从图片到可交互的表单都行。

<Image light={CustomFlyoutDemo} alt="A minimal app in which a button labeled 'Show image' is clicked and displays a simple bitmap image." position="center" maxWidth={400} cornerRadius="true"/>

## 编写自定义 `Flyout` 类 {#creating-a-custom-flyout-class}

1. 往项目里添加一个派生自 [`PopupFlyoutBase`](/api/avalonia/controls/primitives/popupflyoutbase) 的 C# 类。
2. 重写抽象方法 `CreatePresenter()`。这样你就能把默认的呈现器换成任何你想用来显示自定义 `Flyout` 内容的控件。本例用的是标准的 `FlyoutPresenter`。
3. 指定呈现器要承载的内容。这里选的是 `Image`。

```csharp title="MyImageFlyout.cs"
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.Primitives;
using Avalonia.Media;
using Avalonia.Metadata;

namespace CustomFlyoutDemo;

public class MyImageFlyout : PopupFlyoutBase
{
    public static readonly StyledProperty<IImage> ImageProperty =
        AvaloniaProperty.Register<MyImageFlyout, IImage>(nameof(Image));
    
    [Content]
    public IImage Image
    {
        get => GetValue(ImageProperty);
        set => SetValue(ImageProperty, value);
    }

    protected override Control CreatePresenter()
    {
        return new FlyoutPresenter
        {
            Content = new Image
            {
                Width = 240,
                Height = 160,
                [!Avalonia.Controls.Image.SourceProperty] = this[!ImageProperty]
            }
        };
    }
}
```

:::caution
`PopupFlyoutBase` 是提供弹出行为和 `CreatePresenter()` 方法的基类。Avalonia 内置的 [`Flyout` 控件](/controls/layout/containers/flyout)用的也是这个基类。

**不要**用 `FlyoutBase`。它是抽象类，派生自它会导致编译失败。
:::

## 显示与关闭 {#showing-and-dismissing}

- 显示 `Flyout`：调用 `ShowAt`，并把它要依附的控件传进去。
- 关闭 `Flyout`：调用 `Hide`。

```csharp
// Show the flyout programmatically and have it anchored to a button
var flyout = new MyImageFlyout { Image = MyPicture };
flyout.ShowAt(targetButton);

// Dismiss the flyout programmatically
flyout.Hide();
```

## 处理事件 {#handling-events}

基类 `PopupFlyoutBase` 暴露了 `Opened` 和 `Closed` 两个事件，订阅它们即可对显示状态的变化作出反应。

```csharp
flyout.Opened += (s, e) => { /* flyout is now visible */ };
flyout.Closed += (s, e) => { /* flyout was dismissed */ };
```

关于路由事件的更多内容，请参阅[事件概述](/docs/events)。

## 在 XAML 中使用 {#using-in-xaml}

1. 在文件顶部为你的自定义浮出类声明 XML 命名空间。
2. 把这个自定义浮出控件（`MyImageFlyout`）作为附加属性赋给支持它的控件，比如 `Button`。
3. 指定自定义浮出控件的内容。本例中 `MyPicture` 是定义在 `Application.Resources` 里的静态资源。

这样做出来的浮出控件遵循 `PopupFlyoutBase` 的默认行为：点「Show image」按钮会显示图片，再点窗口中图片以外的任何地方则将其关闭。

```xml title="MainWindow.axaml"
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:local="using:CustomFlyoutDemo"
        x:Class="CustomFlyoutDemo.MainWindow">
    <Button Content="Show image"
            HorizontalAlignment="Center"
            VerticalAlignment="Center">
        <Button.Flyout>
            <local:MyImageFlyout Image="{StaticResource MyPicture}" />
        </Button.Flyout>
    </Button>
    
</Window>
```

关于资源用法的更多内容，请参阅[资源概述](/docs/app-development/resources)。

## 呈现可交互的内容 {#displaying-interactive-content}

浮出控件不止能被动展示内容，你完全可以在呈现器里放按钮、文本输入框和其他可交互控件。

下面是一个更进阶的自定义 `Flyout` 示例：一个确认浮出控件，显示「Confirm」按钮，用户点击时触发 `Confirmed` 事件。

```csharp
public class ConfirmFlyout : PopupFlyoutBase
{
    public event EventHandler? Confirmed;

    protected override Control CreatePresenter()
    {
        var confirmButton = new Button { Content = "Confirm" };
        confirmButton.Click += (s, e) =>
        {
            Confirmed?.Invoke(this, EventArgs.Empty);
            Hide();
        };

        return new FlyoutPresenter
        {
            Content = new StackPanel
            {
                Spacing = 8,
                Children =
                {
                    new TextBlock { Text = "Are you sure?" },
                    confirmButton
                }
            }
        };
    }
}
```

## 另请参阅 {#see-also}

- [Flyout](/controls/layout/containers/flyout)：内置浮出控件的参考。
- [定义属性](/docs/custom-controls/defining-properties)：给你的浮出类添加样式化属性、直接属性和附加属性。
- [定义事件](/docs/custom-controls/defining-events)：给你的浮出类添加路由事件。
- [创建自定义控件](/docs/custom-controls)：各类自定义控件概览。
