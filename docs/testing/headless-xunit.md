---
id: headless-xunit
title: 用 XUnit 做无头测试
description: 用 XUnit 测试框架为 Avalonia 应用搭建并运行无头 UI 测试。
doc-type: how-to
---

## Preparation 

本页假设你已经创建好 XUnit 项目。
若还没有，请先按 XUnit 的 “Getting Started” 和 “Installation” 操作：https://xunit.net/docs/getting-started/netfx/visual-studio.

## 安装包 {#install-packages}

除 XUnit 相关包外，你还需要再装两个包：
- [Avalonia.Headless.XUnit](https://www.nuget.org/packages/Avalonia.Headless.XUnit)，它同时也带上了 Avalonia。
- [Avalonia.Themes.Fluent](https://www.nuget.org/packages/Avalonia.Themes.Fluent)，因为哪怕是无头控件也需要一套主题。

:::tip
无头平台并不挑主题，你完全可以把 FluentTheme 换成别的。
:::

## 搭建应用 {#setup-application}

和任何 Avalonia 应用一样，这里也要创建 `Application` 实例并应用主题。用无头平台时，这套配置与普通 Avalonia 应用相差无几，大多可以照搬。

```xml title=App.axaml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="Tests.App">
  <Application.Styles>
    <FluentTheme />
  </Application.Styles>
</Application>
```

代码如下：

```csharp title=App.axaml.cs
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

:::note
`BuildAvaloniaApp` 方法通常定义在 Program.cs 文件里，但 NUnit/XUnit 测试没有这个文件，所以改为定义在 `App` 中。
:::

## 初始化 XUnit 测试 {#initialize-xunit-tests}

`[AvaloniaTestApplication]` 特性把当前项目中的测试与指定的应用关联起来。每个项目只需在任意一个文件中声明一次。

```csharp
[assembly: AvaloniaTestApplication(typeof(TestAppBuilder))]

public class TestAppBuilder
{
    public static AppBuilder BuildAvaloniaApp() => AppBuilder.Configure<App>()
        .UseHeadless(new AvaloniaHeadlessPlatformOptions());
}
```

## 测试隔离级别 {#test-isolation-level}

默认情况下，每个测试都会重建 Application 和 Dispatcher（即 `PerTest` 隔离）。测试套件一大，这就显得慢了。若想让整个程序集里的所有测试共用一个 Application 实例，请加上 `[AvaloniaTestIsolation]` 特性：

```csharp
[assembly: AvaloniaTestApplication(typeof(TestAppBuilder))]
[assembly: AvaloniaTestIsolation(AvaloniaTestIsolationLevel.PerAssembly)]
```

| 层级 | 行为 |
|---|---|
| `PerTest` | 每个测试都重建 Application 和 Dispatcher（默认）。测试之间完全隔离。 |
| `PerAssembly` | 整个程序集内的所有测试共用一个 Application 和 Dispatcher。更快，但测试之间会共享状态。 |

:::caution
采用 `PerAssembly` 隔离时，测试之间会共享 Application 状态。请在测试之间清理好全局状态（样式、资源、静态属性），免得互相干扰。并发执行测试是不支持的。
:::

## Example

```csharp
[AvaloniaFact]
public void Should_Type_Text_Into_TextBox()
{
    // Setup controls:
    var textBox = new TextBox();
    var window = new Window { Content = textBox };

    // Open window:
    window.Show();

    // Focus text box:
    textBox.Focus();

    // Simulate text input:
    window.KeyTextInput("Hello World");

    // Assert:
    Assert.Equal("Hello World", textBox.Text);
}
```

请用 `[AvaloniaFact]` 取代常用的 `[Fact]` 特性，因为它会准备好 UI 线程。同理，`[Theory]` 也有对应的 `[AvaloniaTheory]` 特性。

## 另请参阅 {#see-also}

- [可用于 XUnit 的示例应用](https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/Testing/TestableApp.Headless.XUnit)
- [Headless Testing Platform](/docs/testing/setting-up-the-headless-platform)
- [用 NUnit 做无头测试](/docs/testing/headless-nunit)
- [用 Appium 做 UI 测试](/docs/testing/ui-testing-with-appium)