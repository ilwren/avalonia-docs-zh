---
id: coded-ui-how-to
title: "操作指南：不写 XAML 构建完整应用"
description: 只用 C#、不写任何 XAML 文件，构建一个功能完整的 Avalonia 应用。
doc-type: how-to
---

本指南带你只用 C#、一个 XAML 文件都不写，构建一个功能完整的 Avalonia 应用。你将做出一个简单的计数器应用，其中的样式、布局、事件处理和数据绑定全部出自代码。

## 前置条件 {#prerequisites}

- .NET 10 SDK 或更高版本
- 一个文本编辑器或 IDE（Visual Studio、Rider 或 VS Code）

## 第 1 步：创建项目 {#step-1-create-the-project}

新建一个控制台应用并添加 Avalonia 包：

```bash
dotnet new console -n CodedUIApp
cd CodedUIApp
dotnet add package Avalonia --version 12.0.0
dotnet add package Avalonia.Desktop --version 12.0.0
dotnet add package Avalonia.Themes.Fluent --version 12.0.0
```

此时你的 `.csproj` 应该是这样：

```xml title='CodedUIApp.csproj'
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

注意这里没有 `Avalonia.Markup.Xaml` 包——你用不上它。

## 第 2 步：引导应用启动 {#step-2-bootstrap-the-application}

把 `Program.cs` 的内容替换为：

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
        // Apply the Fluent theme so controls look polished
        app.Styles.Add(new FluentTheme());

        var window = new CounterWindow();
        window.Show();
        app.Run(window);
    }
}
```

`Start` 方法接受一个委托，它会在 Avalonia 完全初始化之后运行。在这个委托内部，你能拿到 `Application` 实例，可以添加主题、创建窗口并启动事件循环。

## 第 3 步：搭建窗口 {#step-3-build-the-window}

新建一个名为 `CounterWindow.cs` 的文件：

```csharp title='CounterWindow.cs'
using Avalonia;
using Avalonia.Controls;
using Avalonia.Layout;
using Avalonia.Media;

class CounterWindow : Window
{
    private readonly TextBlock _countLabel;
    private int _count;

    public CounterWindow()
    {
        Title = "Counter App (No XAML)";
        Width = 400;
        Height = 300;
        WindowStartupLocation = WindowStartupLocation.CenterScreen;

        _countLabel = new TextBlock
        {
            Text = "0",
            FontSize = 48,
            HorizontalAlignment = HorizontalAlignment.Center,
        };

        var incrementButton = new Button
        {
            Content = "Increment",
            FontSize = 18,
            HorizontalAlignment = HorizontalAlignment.Center,
            HorizontalContentAlignment = HorizontalAlignment.Center,
            Width = 160,
        };
        incrementButton.Click += OnIncrementClick;

        var decrementButton = new Button
        {
            Content = "Decrement",
            FontSize = 18,
            HorizontalAlignment = HorizontalAlignment.Center,
            HorizontalContentAlignment = HorizontalAlignment.Center,
            Width = 160,
        };
        decrementButton.Click += OnDecrementClick;

        var resetButton = new Button
        {
            Content = "Reset",
            FontSize = 14,
            HorizontalAlignment = HorizontalAlignment.Center,
        };
        resetButton.Click += (_, _) =>
        {
            _count = 0;
            _countLabel.Text = "0";
        };

        var buttonRow = new StackPanel
        {
            Orientation = Orientation.Horizontal,
            HorizontalAlignment = HorizontalAlignment.Center,
            Spacing = 12,
            Children = { incrementButton, decrementButton },
        };

        Content = new StackPanel
        {
            VerticalAlignment = VerticalAlignment.Center,
            Spacing = 20,
            Children =
            {
                _countLabel,
                buttonRow,
                resetButton,
            },
        };
    }

    private void OnIncrementClick(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
    {
        _count++;
        _countLabel.Text = _count.ToString();
    }

    private void OnDecrementClick(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
    {
        _count--;
        _countLabel.Text = _count.ToString();
    }
}
```

运行应用：

```bash
dotnet run
```

你应该会看到一个窗口，里面有一个大大的计数显示和三个按钮，分别用来加一、减一和归零。

## 第 4 步：添加自定义样式 {#step-4-add-custom-styles}

加上用代码写的样式，让外观更好看些。修改构造函数，在设置内容之前先套用样式：

```csharp title='CounterWindow.cs (add to constructor, before Content assignment)'
// Style all buttons in this window
Styles.Add(new Avalonia.Styling.Style(x => x.OfType<Button>())
{
    Setters =
    {
        new Avalonia.Styling.Setter(Button.PaddingProperty, new Thickness(16, 8)),
        new Avalonia.Styling.Setter(Button.CornerRadiusProperty, new CornerRadius(8)),
    }
});
```

加入窗口 `Styles` 集合的样式会作用于该窗口内所有匹配的控件，效果与写在 XAML 的 `<Window.Styles>` 块里完全一样。

## 第 5 步：加入数据绑定 {#step-5-add-data-binding}

场景更复杂时，你可以在代码里用数据绑定，而不是直接改控件属性。下面演示如何把控件绑定到视图模型：

```csharp title='CounterViewModel.cs'
using System.ComponentModel;
using System.Runtime.CompilerServices;

class CounterViewModel : INotifyPropertyChanged
{
    private int _count;

    public int Count
    {
        get => _count;
        set
        {
            if (_count != value)
            {
                _count = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(CountText));
            }
        }
    }

    public string CountText => Count.ToString();

    public void Increment() => Count++;
    public void Decrement() => Count--;
    public void Reset() => Count = 0;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
```

然后把标签绑定到视图模型。你既可以用基于字符串的绑定，也可以用编译绑定。编译绑定是类型安全的，编译期就会校验，而且 IntelliSense 支持完整：

```csharp title='CounterWindow.cs (updated constructor, string-based)'
var viewModel = new CounterViewModel();
DataContext = viewModel;

_countLabel.Bind(TextBlock.TextProperty, new Avalonia.Data.Binding("CountText"));

incrementButton.Click += (_, _) => viewModel.Increment();
decrementButton.Click += (_, _) => viewModel.Decrement();
resetButton.Click += (_, _) => viewModel.Reset();
```

```csharp title='CounterWindow.cs (updated constructor, compiled binding)'
var viewModel = new CounterViewModel();
DataContext = viewModel;

_countLabel.Bind(TextBlock.TextProperty,
    CompiledBinding.Create<CounterViewModel, string>(
        expression: vm => vm.CountText));

incrementButton.Click += (_, _) => viewModel.Increment();
decrementButton.Click += (_, _) => viewModel.Decrement();
resetButton.Click += (_, _) => viewModel.Reset();
```

这样就把界面逻辑与呈现分离开了，你用代码照样享受到 XAML 那套 MVVM 的好处。采用编译绑定的那个版本还能在构建时就抓出属性名写错的问题，而不是到运行时悄无声息地失效。

## 第 6 步：加入网格布局 {#step-6-add-a-grid-layout}

界面一大起来，你可能想要更精细的布局掌控。下面这个例子把简单的 `StackPanel` 换成了 `Grid`：

```csharp
var grid = new Grid
{
    RowDefinitions = RowDefinitions.Parse("*,Auto,Auto"),
    ColumnDefinitions = ColumnDefinitions.Parse("*,*"),
    Margin = new Thickness(20),
};

// Counter display spans both columns
Grid.SetColumnSpan(_countLabel, 2);
grid.Children.Add(_countLabel);

// Buttons in the second row
Grid.SetRow(incrementButton, 1);
Grid.SetColumn(incrementButton, 0);
grid.Children.Add(incrementButton);

Grid.SetRow(decrementButton, 1);
Grid.SetColumn(decrementButton, 1);
grid.Children.Add(decrementButton);

// Reset button spans both columns in the third row
Grid.SetRow(resetButton, 2);
Grid.SetColumnSpan(resetButton, 2);
grid.Children.Add(resetButton);

Content = grid;
```

## 第 7 步：加入自定义绘制（可选） {#step-7-add-custom-drawing-optional}

需要直接渲染的应用，可以用 `Canvas` 配合各种形状控件：

```csharp title='DrawingWindow.cs'
using System;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.Shapes;
using Avalonia.Media;

class DrawingWindow : Window
{
    private readonly Canvas _canvas;

    public DrawingWindow()
    {
        Title = "Code-Only Drawing";
        Width = 640;
        Height = 480;
        _canvas = new Canvas { Background = Brushes.Black };
        Content = _canvas;
        Resized += OnResized;
    }

    private void OnResized(object? sender, WindowResizedEventArgs e)
    {
        _canvas.Children.Clear();

        double cx = Width / 2;
        double cy = Height / 2;
        double radius = Math.Min(Width, Height) * 0.35;
        int segments = 80;

        for (int i = 0; i < segments; i++)
        {
            double angle1 = 2 * Math.PI * i / segments;
            double angle2 = 2 * Math.PI * (i + 1) / segments;

            _canvas.Children.Add(new Line
            {
                StartPoint = new Point(cx + radius * Math.Cos(angle1),
                                       cy + radius * Math.Sin(angle1)),
                EndPoint = new Point(cx + radius * Math.Cos(angle2),
                                     cy + radius * Math.Sin(angle2)),
                Stroke = Brushes.CornflowerBlue,
                StrokeThickness = 2,
            });
        }
    }
}
```

## 多窗口应用 {#multi-window-applications}

对于有多个窗口的应用，请用 `ClassicDesktopStyleApplicationLifetime` 来管理应用退出：

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
            .AfterSetup(b => b.Instance?.Styles.Add(new FluentTheme()))
            .SetupWithLifetime(lifetime);

        lifetime.MainWindow = new CounterWindow();
        lifetime.Start(args);
    }
}
```

你可以在代码的任何地方打开新窗口：

```csharp
var secondWindow = new DrawingWindow();
secondWindow.Show();
```

设为 `ShutdownMode.OnLastWindowClose` 后，应用只有在所有已打开的窗口都关闭之后才会退出。

## 小结 {#summary}

本指南表明：你完全可以不写一行 XAML，照样构建出结构清晰、功能完整的 Avalonia 应用。关键套路如下：

| 关注点 | 纯代码的做法 |
|---|---|
| Bootstrap | `AppBuilder.Configure<Application>().UsePlatformDetect().Start(delegate)` |
| Theme | `app.Styles.Add(new FluentTheme())` |
| Controls | 用对象初始化器实例化 |
| Layout | 把子元素添加到面板（`StackPanel`、`Grid`、`DockPanel`）中 |
| 事件 | 用 `+=` 或 lambda 挂上处理程序 |
| Styles | 创建 `Style` 对象并加入 `Styles` 集合 |
| Binding | `control.Bind(property, new ReflectionBinding(...))` or `CompiledBinding.Create(expression)` |
| Drawing | `Canvas` 搭配 `Line`、`Ellipse`、`Rectangle` 等形状 |
| Multi-window | `ClassicDesktopStyleApplicationLifetime` with `ShutdownMode` |

:::tip
想更深入地了解这些套路背后的概念，请参阅[纯代码 UI](/docs/fundamentals/coded-ui)。
:::

## 另请参阅 {#see-also}

- [纯代码构建界面](/docs/fundamentals/coded-ui)
- [应用程序生命周期](/docs/fundamentals/application-lifetimes)
- [在代码中绑定](/docs/data-binding/binding-from-code)
- [在代码中创建数据模板](/docs/data-templates/creating-data-templates-in-code)
- [Threading](/docs/app-development/threading)
