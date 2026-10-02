---
id: setting-up-the-headless-platform
title: Headless Testing Platform
---

无头平台让 Avalonia 不开可见窗口也能运行，很适合在 CI/CD 环境或没有显示器的机器上做自动化测试。它提供完整的 Avalonia 控件树、布局、样式和数据绑定，只是把真实的窗口系统和渲染后端换成了内存中的实现。

:::tip[不只是用来测试]
无头平台在测试之外也大有用处。如果你需要在没有可见窗口的情况下渲染控件（比如服务端生成图片、导出 PDF 或批量处理），可按[视觉回归测试](#visual-regression-testing)中的做法用 `UseHeadlessDrawing = false` 启用 Skia 渲染器，这样就能在内存中跑通一整条渲染管线。另见[在 Docker 中以无头方式运行](/docs/deployment/docker#using-the-headless-platform-instead)。
:::

## 模拟用户输入 {#simulating-user-input}

无头平台没有真实的输入设备，所以输入要靠 `Window` 上的扩展方法来模拟。这些方法会触发与真实输入完全相同的事件。

### 键盘输入 {#keyboard-input}

| 方法 | 说明 |
|---|---|
| `Window.KeyPress(Key, RawInputModifiers, PhysicalKey, string?)` | 模拟按下某个键。 |
| `Window.KeyRelease(Key, RawInputModifiers, PhysicalKey, string?)` | 模拟松开某个键。 |
| `Window.KeyPressQwerty(PhysicalKey, RawInputModifiers)` | 按 QWERTY 布局映射模拟按下某个键。 |
| `Window.KeyReleaseQwerty(PhysicalKey, RawInputModifiers)` | 按 QWERTY 布局映射模拟松开某个键。 |
| `Window.KeyTextInput(string)` | 模拟文本输入（与按下/松开按键无关）。往 `TextBox` 这类控件里打字时用它。 |

### 鼠标输入 {#mouse-input}

| 方法 | 说明 |
|---|---|
| `Window.MouseDown(Point, MouseButton, RawInputModifiers)` | 在指定位置模拟按下鼠标按键。 |
| `Window.MouseUp(Point, MouseButton, RawInputModifiers)` | 模拟松开鼠标按键。 |
| `Window.MouseMove(Point, MouseButton, RawInputModifiers)` | 模拟鼠标移动。 |
| `Window.MouseWheel(Point, Vector, RawInputModifiers)` | 模拟鼠标滚轮滚动。 |

### 拖放 {#drag-and-drop}

| 方法 | 说明 |
|---|---|
| `Window.DragDrop(Point, RawDragEventType, DataObject, DragDropEffects, RawInputModifiers)` | 模拟来自外部的拖放操作（例如用户把文件从操作系统拖进你的应用）。 |

## 常见的测试套路 {#common-test-patterns}

### 测试按钮点击 {#testing-a-button-click}

```csharp
[AvaloniaTest]
public void Button_Click_Updates_ViewModel()
{
    var vm = new MyViewModel();
    var button = new Button
    {
        Command = vm.IncrementCommand,
        HorizontalAlignment = HorizontalAlignment.Stretch,
        VerticalAlignment = VerticalAlignment.Stretch
    };
    var window = new Window { Width = 100, Height = 100, Content = button };
    window.Show();

    window.MouseDown(new Point(50, 50), MouseButton.Left);
    window.MouseUp(new Point(50, 50), MouseButton.Left);

    Assert.Equal(1, vm.Count);
}
```

:::tip
你也可以用 `button.RaiseEvent(new RoutedEventArgs(Button.ClickEvent))` 直接触发事件。这样很省事，但不会执行绑定的命令。若想通过键盘测试命令，请先 `button.Focus()` 再 `window.KeyReleaseQwerty(PhysicalKey.Space, RawInputModifiers.None)`。
:::

### 测试文本输入 {#testing-text-input}

```csharp
[AvaloniaTest]
public void TextBox_Accepts_Text_Input()
{
    var textBox = new TextBox();
    var window = new Window { Content = textBox };
    window.Show();

    textBox.Focus();
    window.KeyTextInput("Hello World");

    Assert.Equal("Hello World", textBox.Text);
}
```

### 测试数据绑定 {#testing-data-binding}

```csharp
[AvaloniaTest]
public void TextBox_Binds_To_ViewModel()
{
    var vm = new MyViewModel { Name = "Alice" };
    var textBox = new TextBox
    {
        [!TextBox.TextProperty] = new Binding("Name")
    };
    var window = new Window
    {
        DataContext = vm,
        Content = textBox
    };
    window.Show();

    Assert.Equal("Alice", textBox.Text);

    // Simulate user editing the text
    textBox.Focus();
    textBox.Text = "Bob";

    Assert.Equal("Bob", vm.Name);
}
```

### 测试键盘快捷键 {#testing-keyboard-shortcuts}

```csharp
[AvaloniaTest]
public void Ctrl_S_Triggers_Save()
{
    var saved = false;
    var window = new Window();
    window.KeyBindings.Add(new KeyBinding
    {
        Gesture = new KeyGesture(Key.S, KeyModifiers.Control),
        Command = ReactiveCommand.Create(() => saved = true)
    });
    window.Show();

    window.KeyPress(Key.S, RawInputModifiers.Control, PhysicalKey.S, "s");
    window.KeyRelease(Key.S, RawInputModifiers.Control, PhysicalKey.S, "s");

    Assert.True(saved);
}
```

### 测试加载了 XAML 的视图 {#testing-a-view-with-loaded-xaml}

在无头测试中，你可以直接实例化自己真实的视图：

```csharp
[AvaloniaTest]
public void MainView_Shows_Welcome_Message()
{
    var vm = new MainViewModel();
    var view = new MainView { DataContext = vm };
    var window = new Window { Content = view };
    window.Show();

    var textBlock = window.FindControl<TextBlock>("WelcomeText");
    Assert.Equal("Welcome to Avalonia!", textBlock?.Text);
}
```

## 冲刷异步操作 {#flushing-async-operations}

Avalonia 中有些操作是异步的（窗口尺寸变化、布局过程、延迟派发的 dispatcher 任务）。如果你刚设完属性就断言，改动可能还没生效。

可以用 `Dispatcher.UIThread.RunJobs()` 把 dispatcher 队列冲刷干净：

```csharp
var window = new Window();
window.Show();

window.Width = 100;
window.Height = 100;

Dispatcher.UIThread.RunJobs();

Assert.Equal(new Size(100, 100), window.ClientSize);
```

你还可以强制渲染计时器走一拍，这在测试动画或依赖渲染的行为时很有用：

```csharp
AvaloniaHeadlessPlatform.ForceRenderTimerTick();
```

:::tip
输入辅助方法和 `CaptureRenderedFrame` 内部已经调用了这些，所以用它们时不必手动冲刷。
:::

## 视觉回归测试 {#visual-regression-testing}

无头平台默认使用一个不产生像素的假绘图后端。你可以启用 Skia 渲染器，捕获渲染出的帧并与基准图比对。

### 启用 Skia 渲染器 {#enabling-the-skia-renderer}

```csharp title="App.axaml.cs"
public static AppBuilder BuildAvaloniaApp() => AppBuilder.Configure<TestApplication>()
    .UseSkia()
    .UseHeadless(new AvaloniaHeadlessPlatformOptions
    {
        UseHeadlessDrawing = false
    });
```

### 捕获一帧 {#capturing-a-frame}

```csharp
var window = new Window
{
    Content = new TextBlock { Text = "Hello World" }
};
window.Show();

var frame = window.CaptureRenderedFrame();
frame.Save("output.png");
```

`CaptureRenderedFrame` 返回一个 `WriteableBitmap`。你可以把它锁定并读取像素数据，在内存中直接比对。

### 与基准图比对 {#comparing-against-a-baseline}

视觉回归测试的常见套路是：渲染控件、保存输出，再与一张已知正确的参考图逐像素比对：

```csharp
[AvaloniaTest]
public void Border_Renders_Correctly()
{
    var control = new Border
    {
        Width = 100,
        Height = 100,
        Background = Brushes.Blue,
        BorderBrush = Brushes.Black,
        BorderThickness = new Thickness(2),
        CornerRadius = new CornerRadius(8)
    };
    var window = new Window { Content = control };
    window.Show();

    var actual = window.CaptureRenderedFrame();

    // Compare against a baseline image stored in your test project
    var expected = new Bitmap("expected/Border_Renders_Correctly.png");
    AssertImagesMatch(expected, actual, tolerance: 0.02);
}

private static void AssertImagesMatch(Bitmap expected, WriteableBitmap actual,
    double tolerance)
{
    // Implement pixel comparison logic, or use an image comparison library
}
```

:::tip
Avalonia 自己的[渲染测试套件](https://github.com/AvaloniaUI/Avalonia/tree/master/tests/Avalonia.RenderTests)就是这么做的。每个测试渲染一个控件、把输出存为 PNG，再按可配置的误差容限与基准图比对。
:::

## 脱离 UI 测试视图模型 {#testing-view-models-without-ui}

实现了 `INotifyPropertyChanged` 或用了 `ReactiveUI` 的视图模型，用普通单元测试就能测，不需要无头平台。只有当测试牵涉 Avalonia 控件、布局或输入时，才用得上无头平台。

```csharp
// No [AvaloniaTest] needed, just a regular [Fact]
[Fact]
public void ViewModel_Increments_Count()
{
    var vm = new MainViewModel();

    vm.IncrementCommand.Execute(null);

    Assert.Equal(1, vm.Count);
}
```

## 手动配置 {#manual-setup}

:::caution
这属于进阶用法。多数情况下请直接用 [XUnit](/docs/testing/headless-xunit) 或 [NUnit](/docs/testing/headless-nunit) 集成，配置的活儿它们都替你办了。
:::

### 安装包 {#install-packages}

你需要两个包：
- [Avalonia.Headless](https://www.nuget.org/packages/Avalonia.Headless)（已包含 Avalonia）
- [Avalonia.Themes.Fluent](https://www.nuget.org/packages/Avalonia.Themes.Fluent)（无头控件也需要一套主题）

:::tip
无头平台并不挑主题，你可以把 `FluentTheme` 换成任何其他主题。
:::

### 搭建应用 {#setup-application}

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="Tests.App">
  <Application.Styles>
    <FluentTheme />
  </Application.Styles>
</Application>
```

```csharp title="App.axaml.cs"
using Avalonia;
using Avalonia.Headless;

public class App : Application
{
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }
}
```

### 跑一次无头会话 {#run-a-headless-session}

```csharp title="Program.cs"
using Avalonia.Controls;
using Avalonia.Headless;

using var session = HeadlessUnitTestSession.StartNew(typeof(App));

await session.Dispatch(() =>
{
    var textBox = new TextBox();
    var window = new Window { Content = textBox };
    window.Show();

    textBox.Focus();
    window.KeyTextInput("Hello World");

    if (textBox.Text != "Hello World")
        throw new Exception("Text input failed");
}, CancellationToken.None);
```

## 另请参阅 {#see-also}

- [用 XUnit 做无头测试](/docs/testing/headless-xunit)：基于 `[AvaloniaFact]` 的 XUnit 集成。
- [用 NUnit 做无头测试](/docs/testing/headless-nunit)：基于 `[AvaloniaTest]` 的 NUnit 集成。
- [用 Appium 做 UI 测试](/docs/testing/ui-testing-with-appium)：借助真实的应用窗口做端到端测试。
- [Avalonia 的测试套件](https://github.com/AvaloniaUI/Avalonia/tree/master/tests)：Avalonia 是怎么测自己的。
