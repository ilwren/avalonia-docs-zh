---
id: headless-testing
title: Headless Testing
---

## 概述 {#overview}

WPF 的单元测试向来是件麻烦事。最常见的办法是跑一整套基于自动化的重量级端到端测试，既慢，又把测试锁死在 Windows 上。

与其走自动化测试，不如先试试无头测试——它又快又可移植。
由于 XPF 与 Avalonia 同根同源，WPF 应用同样能用上无头测试。

:::tip
有一个带无头测试的完整 [CalculatorDemo 示例](https://github.com/AvaloniaUIOU/CalculatorDemo)。需要访问这个仓库的话，请找支持团队。
:::

:::note
关于无头平台和 Avalonia 扩展的更详尽文档，请见[用 XUnit 做无头测试](/docs/testing/headless-xunit)和[用 NUnit 做无头测试](/docs/testing/headless-nunit)。弄懂无头测试在 Avalonia 中的运作方式，对 XPF/WPF 同样大有裨益。
:::

## 配置测试项目 {#configuring-the-testing-project}

XPF/Avalonia 的无头测试支持 `XUnit`、`NUnit` 和 `MSTest`。
测试项目中需要引入集成用的 nuget 包：

```xml
<ItemGroup>
    <PackageReference Include="Avalonia.Headless.XUnit" Version="$(XpfAvaloniaVersion)" />
    or
    <PackageReference Include="Avalonia.Headless.NUnit" Version="$(XpfAvaloniaVersion)" />
</ItemGroup>
```

`$(XpfAvaloniaVersion)` 是 `Xpf.Sdk` 中预定义的常量，测试项目里同样要设置它。若你手动指定了最新的 `PackageReference` 版本，这一步可以省掉。

测试项目要通过运行时校验，还需要 `AvaloniaUI.Xpf.LicenseKey`。若想知道这个密钥从哪儿来，请见[快速上手](/xpf/getting-started)页。

```xml
<ItemGroup>
    <RuntimeHostConfigurationOption Include="AvaloniaUI.Xpf.LicenseKey" Value="--Insert your key here--"/>
</ItemGroup>
```

## （可选）配置测试用的应用 {#optional-configuring-the-testing-application}

与 Avalonia 无头测试类似，你可以为项目配置跨平台的 `AppBuilder`。
不配的话，无头平台就用默认参数，这可能限制你在 XPF 下的测试体验。
注意，若你已经按[定制初始化](/xpf/configuration/customizing-initialization)文档为 XPF 应用重写了 AppBuilder，那套初始化代码可以直接复用，只需在链式调用末尾加上 `.UseHeadless()`。

```csharp
[assembly: AvaloniaTestApplication(typeof(TestAppBuilder))]

public class TestAppBuilder
{
    // XPF specific: add .WithAvaloniaXpf() and use DefaultXpfAvaloniaApplication which has preconfigured default themes.
    public static AppBuilder BuildAvaloniaApp() => AppBuilder.Configure<DefaultXpfAvaloniaApplication>()
        .WithAvaloniaXpf()
        .UseSkia()
        .UseHeadless(new AvaloniaHeadlessPlatformOptions
        {
            // Set to false to enable capturing rendered frames
            UseHeadlessDrawing = false
        });
}
```

## 编写测试 {#writing-tests}

测试与 XPF 应用跑在同一个进程里，因此发送各种事件、读取应用的各种输出都方便得很。
和普通 WPF 应用一样，一切都得从一个 Window 开始——它可以在同一个测试方法里创建，也可以从准备方法（NUnit 的 `[SetUp]` 方法或 XUnit 的构造函数）中复用。

:::note
NUnit 的 [Test] 和 [Theory] 要换成 [AvaloniaTest] 和 [AvaloniaTheory]，
XUnit 的 [Fact] 则要换成 [AvaloniaFact]。
:::

一个最基础的 NUnit 测试长这样：

```csharp
[AvaloniaTest]
public void Should_Be_Able_To_Raise_Event()
{
    var window = new MainWindow();
    window.Show();
    var button = window.ClickingButton;

    Assert.That(button.Content, Is.EqualTo("Click me"));

    button.RaiseEvent(new RoutedEventArgs(ButtonBase.ClickEvent, button));

    Assert.That(button.Content, Is.EqualTo("Click count: 1"));
}
```

其中按钮的逻辑如下：

```csharp
private int _clickCount = 0;
private void ClickingButton_OnClick(object sender, RoutedEventArgs e)
{
    ClickingButton.Content = "Click count: " + (++_clickCount).ToString();
}
```

:::tip
要在测试项目中访问 `ClickingButton`，你要么在 XAML 里给控件设上 `x:FieldModifier="public"`，要么给主项目加一个 `[assembly: InternalsVisibleTo("YourTestProject")]` 特性。
:::

## 使用 Avalonia 的无头扩展 {#accessing-avalonia-headless-extensions}

Avalonia 提供了模拟点击和键盘输入的无头扩展，省得你去伪造 WPF 事件。

这些扩展只对 Avalonia 的 Window 可用，WPF 的 Window 上用不了。
好在无头测试中是能拿到 Avalonia Window 的：

```csharp
// Get Avalonia window and send text input to currently focused control.
var avWindow = XpfWpfAbstraction.GetAvaloniaWindowForWindow(xpfWindow);
avWindow.KeyTextInput("Hello");
```

与 Avalonia 集成的更多细节，请见 [Avalonia 互操作](/xpf/interop/embedding-avalonia-in-xpf#accessing-avalonia-features)。

## （可选）在 WPF 应用/项目上使用 XPF 无头测试 {#optional-using-xpf-headless-testing-with-wpf-appproject}

只有启动项目必须用 Xpf.Sdk 测试。
换句话说，你完全可以把控件放在一个普通的 “net8.0-windows” 项目里，再从 XPF 无头项目中引用它们。

若你有一个共享控件库想做无头测试，或者手头是普通的 Windows WPF 应用、只想要无头测试而不打算全面改用 XPF，这招就很管用。

使用步骤都一样，只是还得把测试项目的 TargetFramework 设为 `net8.0-windows`，并把 `EnableWindowsTargeting` 设为 true（只有当你要在 Linux/macOS 机器上跑它时才需要）。

## MSTest 支持 {#mstest-support}

MSTest 项目的配置大同小异，只是要多做几步：

1. 在测试项目的 `.csproj` 中把 `DisableAutomaticXpfInit` 设为 `true`：
   ```xml
   <PropertyGroup>
       <DisableAutomaticXpfInit>true</DisableAutomaticXpfInit>
   </PropertyGroup>
   ```

2. 配置好无头 AppBuilder，并用 `[AvaloniaTestMethod]` 取代 `[TestMethod]`：
   ```csharp
   [assembly: AvaloniaTestApplication(typeof(TestAppBuilder))]

   public class TestAppBuilder
   {
       public static AppBuilder BuildAvaloniaApp() => AppBuilder
           .Configure<DefaultXpfAvaloniaApplication>()
           .WithAvaloniaXpf()
           .UseSkia()
           .UseHeadless(new AvaloniaHeadlessPlatformOptions
           {
               UseHeadlessDrawing = false
           });
   }
   ```

## 测试隔离 {#test-isolation}

若测试时灵时不灵（比如报 `TaskScheduler` 错误，或者测试之间状态互相串味），请按程序集配置测试隔离：

```csharp
[assembly: AvaloniaTestApplication(typeof(TestAppBuilder), AvaloniaTestIsolationLevel.PerAssembly)]
```

这样 Avalonia 运行时就只在每个测试程序集中初始化一次，而不是每个测试都来一遍，从而避免测试清理与初始化之间的竞态。

## 在 CI 中运行测试 {#running-tests-in-ci}

在 Linux 的 CI 环境中跑 XPF 无头测试时：

- 确认测试项目中配好了许可证密钥（见[快速上手](/xpf/getting-started#step-4-add-your-licence-key)）
- 使用无头模式时不需要显示服务器
- 若出现 `XOpenDisplay failed` 错误，请确认 `DisableAutomaticXpfInit` 已设为 `true`，且无头 AppBuilder 配置无误

## 另请参阅 {#see-also}

- [用 XUnit 做无头测试](/docs/testing/headless-xunit)
- [用 NUnit 做无头测试](/docs/testing/headless-nunit)
- [搭建无头平台](/docs/testing/setting-up-the-headless-platform)