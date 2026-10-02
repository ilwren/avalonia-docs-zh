---
id: coded-ui
title: 纯代码构建界面
description: 完全用 C# 或 F# 构建 Avalonia 应用，不写任何 XAML 文件。
doc-type: explanation
video:
  src: https://youtu.be/cOzQDVuzLV8?
  title: 纯 C# 构建 Avalonia 界面 —— 不需要 XAML
---

Avalonia 并不强制使用 XAML。你可以只用 C#、F# 或任何 .NET 语言构建完整的应用。XAML 能表达的控件、布局、样式、绑定和动画，在代码中都有等价的 API。

这是因为 Avalonia XAML 最终会被编译成 IL（中间语言）—— 和 C# 以及其他所有 .NET 语言编译出来的是同一种 IL。XAML 只是描述对象图的一种方式；如果你更愿意用 C#、F# 或别的 .NET 语言直接把这张对象图搭出来，完全没问题。

## 什么时候该选纯代码 {#when-to-choose-code-only}

XAML 和纯代码之间怎么选，很大程度上是个人偏好 —— 两者运行结果完全相同，而且可以在同一个应用里自由混用。

话虽如此，还是得了解其中的现实权衡。Avalonia 脱胎于 WPF，绝大多数资料、教程、社区问答和开发者经验都默认你在用 XAML。选择纯代码路线意味着：

- 网上能找到的示例大多是 XAML 写的，你得自己把它们翻译成所选语言。
- 不用 XAML 的开发者群体更小，遇到纯代码相关的问题时，求助会费些功夫。
- XAML 预览器、设计时数据这类工具，都是围绕 XAML 工作流打造的。

纯代码开发完全可行，但就借力现有知识与资源生态而言，它并不是阻力最小的那条路。

## 搭起一个纯代码应用 {#bootstrapping-a-code-only-application}

纯代码的 Avalonia 应用一个 `.axaml` 文件都不需要。最简单的做法是用 `AppBuilder` 配合一个手写的启动委托：

```csharp title='Program.cs'
using Avalonia;
using Avalonia.Controls;
using Avalonia.Themes.Fluent;

class Program
{
    public static void Main(string[] args)
    {
        AppBuilder.Configure<Application>()
                  .UsePlatformDetect()
                  .Start(AppMain, args);
    }

    static void AppMain(Application app, string[] args)
    {
        app.Styles.Add(new FluentTheme());

        var window = new Window
        {
            Title = "Hello from Code",
            Width = 400,
            Height = 300,
            Content = new TextBlock
            {
                Text = "No XAML here.",
                FontSize = 24,
                HorizontalAlignment = Avalonia.Layout.HorizontalAlignment.Center,
                VerticalAlignment = Avalonia.Layout.VerticalAlignment.Center,
            }
        };

        window.Show();
        app.Run(window);
    }
}
```

项目文件同样极简：

```xml title='MyApp.csproj'
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <OutputType>Exe</OutputType>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Avalonia" Version="12.0.0" />
    <PackageReference Include="Avalonia.Desktop" Version="12.0.0" />
    <PackageReference Include="Avalonia.Themes.Fluent" Version="12.0.0" />
  </ItemGroup>
</Project>
```

这就够了。不需要 `App.axaml`，不需要 `MainWindow.axaml`，也没有任何生成代码。

### 使用应用程序生命周期 {#using-application-lifetimes}

如果应用需要更细致地管理窗口（比如多窗口应用要在最后一个窗口关闭时退出），就用 `ClassicDesktopStyleApplicationLifetime` 代替简单的 `Start` 委托：

```csharp title='Program.cs'
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Themes.Fluent;

class Program
{
    public static void Main(string[] args)
    {
        var lifetime = new ClassicDesktopStyleApplicationLifetime
        {
            Args = args,
            ShutdownMode = ShutdownMode.OnLastWindowClose,
        };

        AppBuilder.Configure<Application>()
            .UsePlatformDetect()
            .AfterSetup(builder => builder.Instance?.Styles.Add(new FluentTheme()))
            .SetupWithLifetime(lifetime);

        lifetime.MainWindow = new MainAppWindow();
        lifetime.Start(args);
    }
}
```

:::info
生命周期各选项的完整说明，请见[应用程序生命周期](/docs/fundamentals/application-lifetimes)。
:::

## 创建控件 {#creating-controls}

每个 Avalonia 控件都能在代码中直接实例化并配置。C# 的对象初始化器与 XAML 的属性特性几乎一一对应：

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
<TabItem value="csharp" label="C# Code" default>

```csharp
var button = new Button
{
    Content = "Click Me",
    FontSize = 18,
    HorizontalAlignment = HorizontalAlignment.Center,
    Background = Brushes.SteelBlue,
    Foreground = Brushes.White,
};
```

</TabItem>
<TabItem value="xaml" label="XAML Equivalent">

```xml
<Button Content="Click Me"
        FontSize="18"
        HorizontalAlignment="Center"
        Background="SteelBlue"
        Foreground="White" />
```

</TabItem>
</Tabs>

## 构建布局 {#building-layouts}

代码中的布局遵循与 XAML 相同的父子模型：创建一个布局面板，往里添加子元素，再把它指定为窗口或其他控件的内容。

```csharp
var stack = new StackPanel
{
    Spacing = 12,
    Margin = new Thickness(20),
};

stack.Children.Add(new TextBlock { Text = "Name:", FontSize = 16 });
stack.Children.Add(new TextBox { PlaceholderText = "Enter your name" });
stack.Children.Add(new Button { Content = "Submit" });

window.Content = stack;
```

网格布局则先定义行和列，再用附加属性摆放子元素：

```csharp
var grid = new Grid
{
    RowDefinitions = RowDefinitions.Parse("Auto,*,Auto"),
    ColumnDefinitions = ColumnDefinitions.Parse("200,*"),
};

var header = new TextBlock { Text = "Header", FontSize = 24 };
Grid.SetColumnSpan(header, 2);
grid.Children.Add(header);

var sidebar = new ListBox();
Grid.SetRow(sidebar, 1);
grid.Children.Add(sidebar);

var content = new TextBlock { Text = "Main content area" };
Grid.SetRow(content, 1);
Grid.SetColumn(content, 1);
grid.Children.Add(content);
```

## 处理事件 {#handling-events}

用标准的 C# 事件处理程序或 lambda 表达式接上事件：

```csharp
var count = 0;
var label = new TextBlock { Text = "Clicks: 0" };

var button = new Button { Content = "Click Me" };
button.Click += (sender, args) =>
{
    count++;
    label.Text = $"Clicks: {count}";
};
```

需要更复杂地处理路由事件时：

```csharp
button.AddHandler(Button.ClickEvent, (sender, args) =>
{
    // Handle the event
    args.Handled = true;
}, Avalonia.Interactivity.RoutingStrategies.Bubble);
```

## 应用样式 {#applying-styles}

你可以用代码创建样式，并把它添加到控件层次结构的任意一级：

```csharp
var style = new Style(x => x.OfType<Button>())
{
    Setters =
    {
        new Setter(Button.FontSizeProperty, 16.0),
        new Setter(Button.PaddingProperty, new Thickness(12, 8)),
        new Setter(Button.BackgroundProperty, Brushes.DarkSlateBlue),
        new Setter(Button.ForegroundProperty, Brushes.White),
    }
};

window.Styles.Add(style);
```

## 在代码中做数据绑定 {#data-binding-from-code}

不写 XAML 也能把控件属性绑定到数据源。最简单的方式是用基于字符串的绑定路径：

```csharp
var textBox = new TextBox();
var label = new TextBlock();

// Bind the label text to the textbox text
label.Bind(TextBlock.TextProperty,
    new ReflectionBinding("Text") { Source = textBox });
```

### 编译绑定 {#compiled-bindings}

想要类型安全、编译期校验并有完整 IntelliSense 支持的绑定，就用 `CompiledBinding.Create`。它接收的是 LINQ 表达式而非字符串路径，属性名写错在运行前就会被编译器拦下：

```csharp
// Bind to a view model property with type safety
var binding = CompiledBinding.Create<MyViewModel, string>(
    expression: vm => vm.Title
);
textBlock.Bind(TextBlock.TextProperty, binding);

// With an explicit source and two-way mode
var binding = CompiledBinding.Create(
    source: viewModel,
    expression: vm => vm.Title,
    mode: BindingMode.TwoWay
);
textBox.Bind(TextBox.TextProperty, binding);
```

编译绑定支持属性访问、嵌套属性、索引器、类型转换、逻辑取反以及 `AvaloniaProperty` 访问，性能也优于基于反射的字符串绑定。

### 响应式写法 {#reactive-patterns}

你也可以用 `GetObservable` 和 `GetBindingObservable` 来实现响应式写法：

```csharp
textBox.GetObservable(TextBox.TextProperty).Subscribe(newText =>
{
    // React to text changes
});
```

:::info
在代码中绑定的完整说明，请见[在代码中绑定](/docs/data-binding/binding-from-code)。
:::

## 自定义绘制 {#custom-drawing}

如果应用需要直接绘制图形（数据可视化、游戏、仿真等），可以用 `Canvas` 配合形状控件，或者自己实现渲染逻辑：

```csharp
var canvas = new Canvas { Background = Brushes.Black };

// Add shapes to the canvas
var circle = new Ellipse
{
    Width = 100,
    Height = 100,
    Fill = Brushes.CornflowerBlue,
};
Canvas.SetLeft(circle, 150);
Canvas.SetTop(circle, 100);
canvas.Children.Add(circle);

// Draw lines
var line = new Line
{
    StartPoint = new Point(0, 0),
    EndPoint = new Point(200, 200),
    Stroke = Brushes.White,
    StrokeThickness = 2,
};
canvas.Children.Add(line);
```

## 线程方面的注意事项 {#threading-considerations}

从后台线程更新界面时，请使用 `Dispatcher.UIThread`：

```csharp
var label = new TextBlock { Text = "Waiting..." };

_ = Task.Run(async () =>
{
    // Do work on a background thread
    await Task.Delay(2000);

    // Update the UI on the UI thread
    Dispatcher.UIThread.Post(() =>
    {
        label.Text = "Done!";
    });
});
```

:::info
完整的线程指引请见[线程](/docs/app-development/threading)。
:::

## F# 与 Avalonia.FuncUI {#f-and-avaloniafuncui}

F# 特别适合纯代码界面开发。作为一门表达式优先的函数式语言，F# 有着强大的类型推断、描述嵌套结构时的轻量语法，还能借助计算表达式、管道和可区分联合等特性原生地构建领域专用语言。

C# 靠构造对象、赋值属性来搭界面，F# 则能把同样的树表达成纯粹的数据组合。写出来的东西与其说是在「拼装」界面，不如说是在「描述」界面。

[Avalonia.FuncUI](https://github.com/fsprojects/Avalonia.FuncUI) 是一个社区库，为 F# 开发者带来了受 Elm 启发的完全函数式架构。它提供：

- 一套声明式领域专用语言（DSL），把视图构建为不可变的描述。
- Elm/MVU（Model-View-Update）架构，状态不可变，靠消息传递驱动。
- 通过可组合的 F# API 完整覆盖每一个 Avalonia 控件。

```fsharp title='F# with Avalonia.FuncUI'
let view (state: State) (dispatch: Msg -> unit) =
    DockPanel.create [
        DockPanel.children [
            Button.create [
                Button.dock Dock.Bottom
                Button.onClick (fun _ -> dispatch Increment)
                Button.content "Click me"
            ]
            TextBlock.create [
                TextBlock.dock Dock.Top
                TextBlock.fontSize 48.0
                TextBlock.text (string state.Count)
            ]
        ]
    ]
```

### 纯代码界面：C# 与 F# 之比较 {#c-compared-to-f-for-coded-ui}

两种语言都足以胜任纯代码的 Avalonia 应用开发，怎么选取决于使用手感和个人偏好。

**F# 在纯代码界面上的长处：**

- 几乎一切皆表达式，组合界面树时感觉自然而直接。
- 计算表达式和管道让你能构建出近似「界面小语言」的 API。
- 不可变性与代数数据类型，天然契合响应式、消息传递的架构。
- 类型推断让泛型密集的组合代码依然清爽易读。

**C# 在纯代码界面上的长处：**

- 学习资料、第三方库和社区支持的生态都更庞大。
- 对象初始化器语法在配置常规控件时足够顺手。
- 对绝大多数 .NET 开发者来说更熟悉。
- 无需任何包装层即可访问全部 Avalonia API。

C# 做纯代码界面并没有本质上的短板，只是面向对象的出身让它在表达深度嵌套、层层组合的界面树时显得啰嗦，而 F# 恰恰就是为这种形状的代码而生的。如果你愿意学 F#，Avalonia.FuncUI 大概能提供 .NET 生态中最舒服的纯代码开发体验。

如果你更偏好 C#，精心设计一套 builder 风格的 API 也能大幅减少样板代码。本文通篇展示的纯代码写法，应付绝大多数应用已经绰绰有余。

## 另请参阅 {#see-also}

- [Avalonia XAML](/docs/fundamentals/avalonia-xaml)
- [Code-behind](/docs/fundamentals/code-behind)
- [应用程序生命周期](/docs/fundamentals/application-lifetimes)
- [在代码中绑定](/docs/data-binding/binding-from-code)
- [在代码中创建数据模板](/docs/data-templates/creating-data-templates-in-code)
- [实战：不用 XAML 构建完整应用](/docs/how-to/coded-ui-how-to)
