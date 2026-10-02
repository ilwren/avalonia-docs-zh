---
id: code-behind
title: 代码隐藏
description: 用代码隐藏文件访问控件、设置属性，并处理来自 XAML 的事件。
doc-type: explanation
video:
  src: https://youtu.be/cTreAu0Amyk
  title: '吃透 Avalonia 代码隐藏 —— 分部类、x:Name 与事件接线'
---

import VsSolutionExplorerScreenshot from '/img/concepts/core-concepts/code-behind/vs-solution-explorer.png';

除了 XAML 文件，大多数 Avalonia 控件还配有一个 _代码隐藏_ 文件，通常用 C# 编写。按惯例它的扩展名是 `.axaml.cs`，在 IDE 中一般嵌套显示在 XAML 文件下方。

比如在 Visual Studio 的解决方案资源管理器中，你会看到 `MainWindow.axaml` 文件和它的代码隐藏文件 `MainWindow.axaml.cs`：

<Image light={VsSolutionExplorerScreenshot} alt="Visual Studio solution explorer showing a XAML file with its nested code-behind file" position="center" maxWidth={400} cornerRadius="true"/>

代码隐藏文件里有一个与 XAML 文件同名的 `partial` 类。`partial` 关键字很关键：有了它，Avalonia 的构建工具才能生成一个配套文件，把你命名过的控件接起来并调用 XAML 加载器。例如：

```csharp title='MainWindow.axaml.cs'
using Avalonia.Controls;

namespace AvaloniaApplication1.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }
    }
}
```

注意类名要与 XAML 文件名一致，并且会在窗口元素的 `x:Class` 特性中被引用。`x:Class` 里的全限定名必须带上命名空间。

```xml title='MainWindow.axaml'
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        // highlight-next-line
        x:Class="AvaloniaApplication1.Views.MainWindow">
  ...
</Window>
```

:::tip
如果你改了代码里的类名或命名空间，记得同步改 `x:Class` 特性。两者对不上会导致构建错误或运行时报错。
:::

刚创建出来的代码隐藏文件里只有一个构造函数，其中会调用 `InitializeComponent()` 方法。这行调用用于在运行时加载对应的 XAML，删掉之后界面就不会渲染了。

## 定位控件 {#locating-controls}

写代码隐藏时，经常需要访问 XAML 中定义的控件。

做法是在 XAML 里用 `Name`（或 `x:Name`）特性给目标控件起个名字。Avalonia 的构建工具随后会在你的分部类中生成一个强类型字段，于是就能直接引用该控件了。

下面是一个带命名 `Button` 的 XAML 示例：

```xml title='MainWindow.axaml'
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="AvaloniaApplication5.MainWindow">
  // highlight-next-line
  <Button Name="greetingButton">Hello World</Button>
</Window>
```

现在就可以在代码隐藏中通过自动生成的 `greetingButton` 字段访问这个按钮了：

```csharp title='MainWindow.axaml.cs'
using Avalonia.Controls;

namespace AvaloniaApplication1.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            // highlight-next-line
            greetingButton.Content = "Goodbye Cruel World!";
        }
    }
}
```

:::tip
由于该字段是在构建期生成的，项目编译之前 IDE 可能会报警告。编译一次即可消除。
:::

## 设置属性 {#setting-properties}

在代码隐藏中拿到控件引用之后，就可以读写它的任意属性了。比如修改按钮的 `Background` 属性：

```csharp title='C#'
greetingButton.Background = Brushes.Blue;
```

属性值同样可以读取。想先探明控件当前状态再决定下一步动作时，这很有用：

```csharp title='C#'
if (greetingButton.IsVisible)
{
    greetingButton.Content = "I'm visible!";
}
```

## 处理事件 {#handling-events}

多数带交互的应用都需要响应用户操作，比如点击、按键或指针移动。采用代码隐藏模式时，你在代码隐藏文件里写事件处理方法，再在 XAML 中用事件特性引用它。

例如要处理按钮点击，在 XAML 中添加一个 `Click` 特性，指向代码隐藏里的某个方法：

```xml title='MainWindow.axaml'
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="AvaloniaApplication4.MainWindow">
  <Button Click="GreetingButtonClickHandler">Hello World</Button>
</Window>
```

```csharp title='MainWindow.axaml.cs'
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    public void GreetingButtonClickHandler(object sender, RoutedEventArgs e)
    {
        // code here.
    }
}
```

`sender` 参数是引发该事件的控件，`RoutedEventArgs` 参数则携带着事件如何产生、又如何在视觉树中传播的信息。

事件处理程序也可以在代码中挂接，而不写在 XAML 里。需要动态增删处理程序时，这种方式更合适：

```csharp title='C#'
greetingButton.Click += GreetingButtonClickHandler;
```

:::info
关于事件路由的更多说明，请见[路由事件](/docs/input-interaction/routed-events)。
:::

## 代码隐藏与 MVVM：该怎么选 {#when-to-use-code-behind-vs-mvvm}

代码隐藏适合小型应用、原型，以及动画、焦点管理这类纯视图逻辑。应用规模一大，就该考虑 MVVM 模式了 —— 它把界面逻辑剥离到视图模型中，更易于测试和维护。两者也可以并用：数据与业务逻辑交给 MVVM，视图专属的代码仍放在代码隐藏里。

## 另请参阅 {#see-also}

- [Avalonia XAML](/docs/fundamentals/avalonia-xaml)
- [纯代码构建界面](/docs/fundamentals/coded-ui)
- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)
- [界面组合](/docs/fundamentals/ui-composition)
- [路由事件](/docs/input-interaction/routed-events)
