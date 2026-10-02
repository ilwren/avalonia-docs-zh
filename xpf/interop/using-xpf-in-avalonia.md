---
id: using-xpf-in-avalonia
title: 在 Avalonia 中使用 XPF
description: 用 XpfContainer 在既有的 Avalonia 应用中承载兼容 WPF 的 XPF 控件。
doc-type: how-to
---

本指南带你在既有的 Avalonia 应用中嵌入 XPF（兼容 WPF）控件。读完之后，你会有一个通过 `XpfContainer` 包装、渲染在 Avalonia 窗口里的 XPF `UserControl`。

## 前置条件 {#prerequisites}

动手之前，请确认你具备：

- 一个既有的 Avalonia 应用项目。
- 有效的 XPF 许可证，以及 XPF SDK NuGet 源的访问权限。配置细节请见[快速上手](/xpf/getting-started)。

## 第 1 步：改项目文件 {#step-1-update-the-project-file}

把你 Avalonia 应用的 SDK 换成 [XPF SDK](/xpf/getting-started#step-3-use-the-xpf-sdk)：

```xml
<Project Sdk="Xpf.Sdk/1.6.0">
```

接着关掉 XPF 的自动初始化，好让你自己掌控 XPF 子系统何时启动。在项目文件中加上这条属性：

```xml
<PropertyGroup>
  <DisableAutomaticXpfInit>true</DisableAutomaticXpfInit>
</PropertyGroup>
```

:::tip
关掉自动初始化是必须的，因为启动流程归 Avalonia 应用掌管。省了这一步，XPF 可能赶在 Avalonia 就绪之前初始化，从而引发运行时错误。更多细节请见[定制初始化](/xpf/configuration/customizing-initialization)。
:::

## 第 2 步：添加 XPF 应用类 {#step-2-add-an-xpf-application-class}

在项目中添加一个继承自 `System.Windows.Application` 的 `XpfApp` 类。它充当 XPF 的应用对象，是 XPF 资源解析、合并字典等 WPF 基础设施正常工作的前提。

```csharp
using System.Windows;

namespace MyAvaloniaApplication;

/// <summary>
/// Represents the XPF application.
/// </summary>
public partial class XpfApp : Application
{
}
```

:::note
若你的 XPF 控件依赖应用级资源（样式、画刷、转换器），请像在标准 WPF 应用中那样，把它们定义在与该类关联的 `App.xaml` 文件里。
:::

## 第 3 步：初始化 XPF 应用 {#step-3-initialize-the-xpf-application}

在 Avalonia 的 `App.xaml.cs` 文件中，于 `OnFrameworkInitializationCompleted` 内创建一个 `XpfApp` 实例。这件事必须赶在任何 XPF 控件被用到之前完成。

```csharp
public override void OnFrameworkInitializationCompleted()
{
    // highlight-start
    new XpfApp();
    // highlight-end

    // Existing Avalonia initialization here
}
```

请把 `new XpfApp()` 调用放在方法最开头，在设置 `MainWindow` 或 `MainView` 之前。若等 Avalonia 渲染完第一帧才初始化 XPF，初始视图树中的 `XpfContainer` 实例可能加载失败。

## 第 4 步：添加 XPF UserControl {#step-4-add-an-xpf-usercontrol}

创建一个 XPF 的 `UserControl`，把你想承载的、兼容 WPF 的内容放进去。这个控件用的是 WPF 的 XAML 命名空间，而非 Avalonia 的。

```xml
<UserControl x:Class="MyAvaloniaApplication.MyXpfView"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
             xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
             mc:Ignorable="d"
             d:DesignHeight="300" d:DesignWidth="300">
    <Button>Hello XPF!</Button>
</UserControl>
```

```csharp
using System.Windows.Controls;

namespace MyAvaloniaApplication;

public partial class MyXpfView : UserControl
{
    public MyXpfView()
    {
        InitializeComponent();
    }
}
```

:::warning
不要在同一个 XAML 文件里混用 Avalonia 和 WPF 的命名空间。XPF 的 `UserControl` 必须用 WPF 命名空间（`http://schemas.microsoft.com/winfx/2006/xaml/presentation`），而你的 Avalonia 视图必须用 Avalonia 命名空间（`https://github.com/avaloniaui`）。
:::

## 第 5 步：承载 XPF UserControl {#step-5-host-the-xpf-usercontrol}

用 `XpfContainer` 把 XPF 内容承载到 Avalonia 控件中。`XpfContainer` 位于 `PresentationFramework` 程序集的 `Atlantis` 命名空间下。

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:local="clr-namespace:MyAvaloniaApplication"
        // highlight-next-line
        xmlns:xpf="clr-namespace:Atlantis;assembly=PresentationFramework"
        x:Class="MyAvaloniaApplication.MainWindow">
    // highlight-start
    <xpf:XpfContainer>
        <local:MyXpfView/>
    </xpf:XpfContainer>
    // highlight-end
</Window>
```

`XpfContainer` 可以放在 Avalonia 视觉树的任何位置：面板里、选项卡控件里、分栏视图里，或者任何别的布局容器里。

## 排查问题 {#troubleshooting}

| 现象 | 可能的原因 | 解决办法 |
|---|---|---|
| `XpfContainer` 渲染出来一片空白 | 控件加载之前没有实例化 `XpfApp` | 把 `new XpfApp()` 挪到 `OnFrameworkInitializationCompleted` 的最前面 |
| 构建报错，提示找不到 WPF 类型 | 项目 SDK 没有改成 `Xpf.Sdk` | 核对 `.csproj` 中的 `<Project Sdk="Xpf.Sdk/1.6.0">` 那一行 |
| XPF 赶在 Avalonia 就绪之前初始化了 | 没有设置 `DisableAutomaticXpfInit` | 在项目文件中加上 `<DisableAutomaticXpfInit>true</DisableAutomaticXpfInit>` |
| XPF 控件中出现 XAML 命名空间错误 | 混用了 Avalonia 和 WPF 的命名空间 | 确保 XPF 控件只用 WPF 的 XAML 命名空间 |

## 另请参阅 {#see-also}

- [XPF 快速上手](/xpf/getting-started)
- [定制初始化](/xpf/configuration/customizing-initialization)
- [在 XPF 中嵌入 Avalonia](/xpf/interop/embedding-avalonia-in-xpf)
- [集中管理多个 XPF 项目](/xpf/configuration/centralizing-multiple-xpf-projects)
