---
id: custom-control-library
title: 自定义控件库
description: 如何创建一个装着多个自定义控件的独立类库项目，再在别的项目中引用它、使用这些控件。
doc-type: how-to
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import CustomControlLibraryUsage from '/img/custom-controls/custom-control-library-usage.png';
import NewClassLibraryVS from '/img/custom-controls/new-class-library-vs.png';
import CustomControlSolution from '/img/custom-controls/custom-control-solution.png';

把自定义控件库做成一个独立项目，用来存放多个控件。之后在任意 Avalonia 应用中引用这个库，就能复用其中的控件。

## 创建自定义控件库 {#creating-a-custom-control-library}

1. 先创建一个新的**类库**项目。推荐的几款 IDE（Visual Studio、Visual Studio Code、JetBrains Rider）都带有 .NET 类库模板。
2. 在类库项目中安装 Avalonia。[可以通过 IDE 的 NuGet 包管理界面来装](/docs/get-started/install-avalonia#installing-avalonia-in-an-existing-net-project)。

<Image light={NewClassLibraryVS} maxWidth={250} cornerRadius="true" position="center" alt="A screenshot showing how to start a new .NET class library project in Visual Studio." caption="Example of a .NET class library template in Visual Studio." />
<br />

## 往类库中添加自定义控件 {#adding-custom-controls-to-the-class-library}

一个控件库想装多少控件都行，三种[自定义控件类型](/docs/custom-controls#types-of-custom-controls)也可以混着放。

下面的例子用的是一个名为 `CCLibrary` 的类库，我们会往里添加 [`ConfirmationView`](/controls/primitives/usercontrol#basic-example)、[`ToggleLabel`](/docs/custom-controls/templated-controls) 和 [`CircleControl`](/docs/custom-controls/custom-drawn-controls) 这几个自定义控件。

```text
CCLibrary/
├── CCLibrary.csproj
├── ConfirmationView.axaml
    └── ConfirmationView.axaml.cs
├── ToggleLabel.cs
├── CircleControl.cs
└── Themes/
    └── Generic.axaml
```

### 添加用户控件 {#adding-a-user-control}

`ConfirmationView` 是一个用户控件，设计成可复用的确认对话框。它的做法请看 [`UserControl` 页面](/controls/primitives/usercontrol#basic-example)。

要把它加进 `CCLibrary`，把 XAML 文件（`ConfirmationView.axaml`）和代码隐藏文件（`ConfirmationView.axaml.cs`）一并放进控件库目录即可。

注意两个文件都要使用类库项目的命名空间（本例中是 `CCLibrary`），而不是可执行项目的命名空间。

<Tabs>

<TabItem value="usercontrol-xaml" label="ConfirmationView.axaml">

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             // highlight-next-line
             x:Class="CCLibrary.ConfirmationView"
             x:Name="root">

  <!-- Control's design and layout -->

</UserControl>
```

</TabItem>

<TabItem value="usercontrol-cs" label="ConfirmationView.axaml.cs">

```csharp
using Avalonia;
using Avalonia.Controls;

// highlight-next-line
namespace CCLibrary;

public partial class ConfirmationView : UserControl
{
    public ConfirmationView()
    {
        InitializeComponent();
    }

    // Control's events, logic, properties, etc.
}
```

</TabItem>

</Tabs>

### 添加模板化控件 {#adding-a-templated-control}

`ToggleLabel` 是一个显示文本标签的自定义控件。作为模板化控件，它没有固定外观——外观由控件主题决定，各应用可以各不相同。它的做法请看[模板化控件页面](/docs/custom-controls/templated-controls)。

要把它加进 `CCLibrary`，把 `ToggleLabel.cs` 类文件放进控件库目录即可。

你还可以附带一个默认控件主题，好让这个模板化控件在可执行项目中拿来就能用。与 WPF 一样，惯例是把控件主题集中放进 `Themes` 子目录下的一个资源字典里。若要添加多个模板化控件，每个都需要各自的控件主题。

和上一个例子一样，这两个文件都必须使用类库项目的命名空间（本例中是 `CCLibrary`）。

<Tabs>

<TabItem value="templated-control" label="ToggleLabel.cs">

```csharp
using Avalonia;
using Avalonia.Controls.Primitives;

// highlight-next-line
namespace CCLibrary;

public class ToggleLabel : TemplatedControl
{
    // Control's events, logic, properties, etc.
}
```

</TabItem>

<TabItem value="control-theme" label="Themes/Generic.axaml">

```xml
<ResourceDictionary xmlns="https://github.com/avaloniaui"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    // highlight-next-line
                    xmlns:cc="using:CCLibrary">

  <ControlTheme x:Key="{x:Type cc:ToggleLabel}" TargetType="cc:ToggleLabel">
    <!-- Control's default visual appearance-->
  </ControlTheme>

</ResourceDictionary>
```

</TabItem>

</Tabs>

:::caution
类库中的默认控件主题不会自动生效。若不显式引入那个资源字典，模板化控件就拿不到模板，也就什么都画不出来。详见[使用模板化控件](#using-templated-controls)。
:::

### 添加自绘控件 {#adding-a-custom-drawn-control}

`CircleControl` 这个控件会画一个椭圆，颜色由可配置的 `Fill` 属性决定。它的做法请看[自绘控件页面](/docs/custom-controls/custom-drawn-controls)。它属于自绘控件，也就是自己负责绘制，不需要控件主题。

要把它加进 `CCLibrary`，把单个 `CircleControl.cs` 类文件放进控件库目录即可。和前面的例子一样，该类文件必须使用类库项目的命名空间（本例中是 `CCLibrary`）。

```csharp title="CircleControl.cs"
using System;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;

// highlight-next-line
namespace CCLibrary;

public class CircleControl : Control
{
    // Control's specifications

    public override void Render(DrawingContext context)
    {
        // Control's appearance as drawn by DrawingContext
    }
}
```

## 引用自定义控件库 {#referencing-a-custom-control-library}

要用上控件库里的自定义控件，必须在可执行项目中引用这个类库项目。

下面的例子用一个名为 `AvaloniaCCLib` 的 Avalonia MVVM 项目来演示。这个项目和[上一节](#adding-custom-controls-to-the-class-library)的 `CCLibrary` 一起被放进名为 `MyControlsLibrary` 的解决方案中。

<Image light={CustomControlSolution} alt="A screenshot of a solution containing two projects in Visual Studio." position="center" maxWidth={400} cornerRadius="true"/>

### 添加项目引用 {#adding-a-project-reference}

在可执行项目的项目文件（`AvaloniaCCLib.csproj`）中，添加一条 `ProjectReference`，指向控件库项目文件（`CCLibrary.csproj`）所在的目录路径。

```xml title="AvaloniaCCLib.csproj"
<ItemGroup>
  <ProjectReference Include="..\MyControlsLibrary\CCLibrary.csproj" />
</ItemGroup>
```

### 添加命名空间声明 {#adding-namespace-declarations}

要在可执行项目中使用你的自定义控件，需要在相关 XAML 文件里作命名空间声明。下面的例子选用 `cc` 作为命名空间前缀，于是 `CCLibrary` 里的自定义控件都可以加上 `cc:` 前缀来使用。

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        // highlight-next-line
        xmlns:cc="using:CCLibrary"
        x:Class="AvaloniaCCLib.Views.MainWindow"
        Title="AvaloniaCCLib">
```

### 使用模板化控件 {#using-templated-controls}

模板化控件要在可执行项目中使用，必须有控件模板。若没有可用模板，运行应用时该控件什么也画不出来。

如果你像[上面的 `ToggleLabel` 例子](#adding-a-templated-control)那样为模板化控件附带了默认控件主题，请注意它不会自动生效：你必须把装着该控件主题的资源字典显式合并进可执行项目的 `App.axaml` 中。

做法是使用 `ResourceInclude`，它借助 [`avares://` URI 方案](/docs/fundamentals/including-assets) 在类库项目中定位资源字典文件。下面这个例子用的是前面几节中的 `CCLibrary`。

```xml title="App.axaml"
<Application.Resources>
  <ResourceDictionary>
    <ResourceDictionary.MergedDictionaries>
      // highlight-next-line
      <ResourceInclude Source="avares://CCLibrary/Themes/Generic.axaml" />
    </ResourceDictionary.MergedDictionaries>
  </ResourceDictionary>
</Application.Resources>
```

### 使用用户控件和自绘控件 {#using-user-controls-and-custom-drawn-controls}

用户控件和自绘控件无需任何额外配置。只要项目里引用了控件库、声明了相应的命名空间，二者都能直接在 XAML 中使用。

<Tabs>

<TabItem value="user-control-usage" label="ConfirmationView">

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:vm="using:AvaloniaCCLib.ViewModels"
        // highlight-next-line
        xmlns:cc="using:CCLibrary"
        x:Class="AvaloniaCCLib.Views.MainWindow"
        x:DataType="vm:MainWindowViewModel"
        Title="AvaloniaCCLib">

    // highlight-next-line
    <cc:ConfirmationView />

</Window>
```

</TabItem>

<TabItem value="custom-drawn-control-usage" label="CircleControl">

```xml

<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:vm="using:AvaloniaCCLib.ViewModels"
        // highlight-next-line
        xmlns:cc="using:CCLibrary"
        x:Class="AvaloniaCCLib.Views.MainWindow"
        x:DataType="vm:MainWindowViewModel"
        Title="AvaloniaCCLib">

    <!-- CircleControl from our example has no default width or height.
         These must be set in XAML when adding the control. -->
    // highlight-next-line
    <cc:CircleControl Width="100" Height="100" />

</Window>

```

</TabItem>

</Tabs>

<Image light={CustomControlLibraryUsage} maxWidth={400} cornerRadius="true" position="center" alt="A screenshot showing all three custom controls from the examples in this section in use." caption="All three custom controls from the control library in use together." />
<br />

## XML 命名空间定义 {#xml-namespace-definitions}

在 `.axaml` 文件中引用控件库时，可以使用 URL 标识格式。例如：

```xml
<Window xmlns:cc="https://my.controls.url" />
```

这要求在类库项目的 `AssemblyInfo.cs` 文件中作注册。多个 XML 命名空间可以共用同一个 URL。（[Avalonia 自己](https://github.com/AvaloniaUI/Avalonia/blob/main/src/Avalonia.Controls/Properties/AssemblyInfo.cs)就让大多数包共用 `https://github.com/avaloniaui` 这个 URL。）

```csharp title="AssemblyInfo.cs"
using Avalonia.Metadata;

[assembly: XmlnsDefinition("https://my.controls.url", "My.NameSpace")]
[assembly: XmlnsDefinition("https://my.controls.url", "My.NameSpace.Other")]
```

采用 URL 格式的主要理由，是让多个程序集共享同一个命名空间标识，从而用一个前缀引用到许多个彼此独立的命名空间。

相比之下，`using:` 和 `clr-namespace:` 这两种格式严格一一对应：一个命名空间配一个前缀。好处是它们不需要在程序集信息里做任何注册。

关于在 XAML 中引用自定义类的更多内容，请参阅[引用你自己的类型](/docs/xaml/namespaces#referencing-your-own-types)。

## 另请参阅 {#see-also}

- [创建自定义控件](/docs/custom-controls)：可以打进控件库的各类自定义控件概览。
- [UserControl](/controls/primitives/usercontrol)：用 XAML 加代码隐藏，把现有控件组合成可复用的视图。
- [自定义模板化控件](/docs/custom-controls/templated-controls)：编写外观完全交由控件主题决定的无外观控件。
- [自绘控件](/docs/custom-controls/custom-drawn-controls)：通过重写 `Render` 让控件自己画自己。
- [自定义面板](/docs/custom-controls/custom-panel)：通过重写 `MeasureOverride` 和 `ArrangeOverride` 实现布局面板。
- [定义属性](/docs/custom-controls/defining-properties)：为自定义控件添加样式化属性、直接属性和附加属性。
- [资源字典](/docs/app-development/resource-dictionary)：合并字典是如何跨程序集解析资源的。
