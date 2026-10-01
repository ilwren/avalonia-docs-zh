---
id: data-context
title: 数据上下文
description: 理解 DataContext 如何为绑定提供默认数据源，以及它在控件树中的继承方式。
doc-type: explanation
---

import DataContextOverviewDiagram from '/img/concepts/data-concepts/data-context/data-context-overview.png';
import DataContextTreeSearchDiagram from '/img/concepts/data-concepts/data-context/data-context-tree-search.png';
import DataContextGreetingBindingScreenshot from '/img/concepts/data-concepts/data-context/data-context-greeting.png';
import DataContextPreviewerScreenshot from '/img/concepts/data-concepts/data-context/data-context-previewer.png';

Avalonia 做数据绑定时，必须先找到一个可供绑定的应用对象。这个「去哪儿找」，就由**数据上下文**来表示。

<Image light={DataContextOverviewDiagram} alt="Diagram showing how data context connects controls to view model properties" position="center" maxWidth={400} cornerRadius="true"/>

Avalonia 中每个控件都有 `DataContext` 属性，内置控件、用户控件和窗口概莫能外。

绑定时，Avalonia 会从声明绑定的那个控件开始，沿逻辑控件树逐级向上查找，直到找到可用的数据上下文为止。

<Image light={DataContextTreeSearchDiagram} alt="Diagram showing data context inheritance through the control tree" position="center" maxWidth={400} cornerRadius="true"/>

这意味着窗口内的控件可以使用窗口的数据上下文；或者像上面那样，窗口里某个控件内部的控件，同样能用上窗口的数据上下文。

:::info
关于 Avalonia 中的控件树，以及如何在运行时查看它们，请见[控件树](/docs/custom-controls/control-trees)。
:::

## Example

用 _Avalonia MVVM Application_ 模板新建一个项目，就能看到窗口的数据上下文是怎么设置的。打开 **App.axaml.cs** 文件查看代码：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
    {
        desktop.MainWindow = new MainWindow
        {
            DataContext = new MainWindowViewModel(),
        };
    }

    base.OnFrameworkInitializationCompleted();
}
```

被设为窗口数据上下文的那个对象，可以在 **MainWindowViewModel.cs** 文件中找到：

```csharp
public class MainWindowViewModel : ViewModelBase
{
    public string Greeting => "Welcome to Avalonia!";
}
```

在主窗口文件 **MainWindow.axaml** 中可以看到，窗口的内容区里有一个 `TextBlock`，它的 `Text` 属性绑定到了 `Greeting` 属性。

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:vm="using:AvaloniaMVVMApplication2.ViewModels"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d" d:DesignWidth="800" d:DesignHeight="450"
        x:Class="AvaloniaMVVMApplication2.Views.MainWindow"
        Icon="/Assets/avalonia-logo.ico"
        Title="AvaloniaMVVMApplication2">

    <Design.DataContext>
        <vm:MainWindowViewModel/>
    </Design.DataContext>

    <TextBlock Text="{Binding Greeting}" HorizontalAlignment="Center" VerticalAlignment="Center"/>

</Window>
```

项目运行时，数据绑定器从该文本块出发沿逻辑控件树向上查找，在主窗口这一级找到了数据上下文。于是绑定的文字显示为：

<Image light={DataContextGreetingBindingScreenshot} alt="App window showing a greeting bound from the data context" position="center" maxWidth={400} cornerRadius="true"/>

## 设计时数据上下文 {#design-time-data-context}

你可能注意到了，项目第一次编译之后，预览窗格里也显示出了那句问候语。

<Image light={DataContextPreviewerScreenshot} alt="Design-time preview showing bound data context values" position="center" maxWidth={400} cornerRadius="true"/>

Avalonia 也能为控件设置仅在设计时生效的数据上下文。这很实用 —— 你在调整布局和样式时，预览窗格里能看到贴近真实的数据。

在 XAML 中可以看到设计时数据上下文是这样设置的：

```xml
<Design.DataContext>
    <vm:MainWindowViewModel/>
</Design.DataContext>
```

:::tip
关于设计时数据上下文的详细用法，请见 [XAML 预览与设计时设置](/docs/app-development/xaml-preview-and-design-settings)。
:::

:::info
要再往下聊数据绑定，就得先有 MVVM 模式的基础了。MVVM 模式的概念介绍请见 [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)。
:::

## 另请参阅 {#see-also}

- [数据绑定入门](/docs/data-binding/introduction-to-data-binding)：数据绑定总览。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定路径、模式与转换器。
- [XAML 预览与设计时设置](/docs/app-development/xaml-preview-and-design-settings)：设计时数据上下文的配置方法。
