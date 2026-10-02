---
id: ui-testing-with-appium
title: 用 Appium 做 UI 测试
---

Appium 是一个开源自动化框架，它通过应用的无障碍树来驱动程序，模拟点击按钮、输入文字、检查控件状态等真实的用户操作。[无头测试](/docs/testing/setting-up-the-headless-platform)不开窗口、以编程方式模拟输入，Appium 测试则不同：它在真实窗口中启动你编译好的应用，像用户那样与之交互。

这让 Appium 测试很适合做端到端验证、无障碍核查以及平台专属行为的测试。Avalonia 自身也用 Appium 在 Windows 和 macOS 上测试框架本身。

## Appium 与无头测试该怎么选 {#when-to-use-appium-vs-headless}

| 考量点 | 无头测试 | Appium |
|---|---|---|
| Speed | 快（进程内运行，无 GUI） | 较慢（要启动真实应用） |
| Scope | 单元测试与组件测试 | 端到端测试与集成测试 |
| 平台行为 | Simulated | 真实（原生窗口系统、菜单、焦点） |
| 无障碍 | 测不到 | 能测（经由无障碍树驱动） |
| CI/CD | 哪儿都能跑 | 需要显示器（Linux 上可用虚拟显示） |

想对控件逻辑和数据绑定快速拿到反馈，就用无头测试；想验证应用作为一个整体（含原生平台集成）是否工作正常，就用 Appium 测试。

## 前置条件 {#prerequisites}

### Windows

安装 [WinAppDriver](https://github.com/microsoft/WinAppDriver/releases)。它在 Windows 上充当 Appium 服务器，要求 Windows 10 或更高版本。还需在 Windows 设置中启用**开发人员模式**。

### macOS

安装 Appium 和 Mac2 驱动：

```bash
npm install -g appium
appium driver install mac2
```

你还得把无障碍权限授予用来跑测试的终端或 IDE。打开**系统设置 > 隐私与安全性 > 辅助功能**，把你的终端应用加进去。

## 准备项目 {#project-setup}

新建一个 xUnit 测试项目并安装 Appium 客户端：

```bash
dotnet new xunit -n MyApp.UITests
cd MyApp.UITests
dotnet add package Appium.WebDriver
```

## 创建测试 fixture {#creating-a-test-fixture}

fixture 负责管理 Appium 驱动会话：启动你的应用、连上它，并在测试结束后把它拆掉。

```csharp
using OpenQA.Selenium.Appium;
using OpenQA.Selenium.Appium.Windows;
using Xunit;

public class AppFixture : IDisposable
{
    public AppiumDriver Session { get; }

    public AppFixture()
    {
        if (OperatingSystem.IsWindows())
        {
            var options = new AppiumOptions();
            options.AddAdditionalAppiumOption("app", @"path\to\your\MyApp.exe");
            options.AddAdditionalAppiumOption("platformName", "Windows");
            options.AddAdditionalAppiumOption("deviceName", "WindowsPC");
            Session = new WindowsDriver(new Uri("http://127.0.0.1:4723"), options);
        }
        else if (OperatingSystem.IsMacOS())
        {
            var options = new AppiumOptions();
            options.AddAdditionalAppiumOption("platformName", "mac");
            options.AddAdditionalAppiumOption("automationName", "mac2");
            options.AddAdditionalAppiumOption("bundleId", "com.mycompany.myapp");
            Session = new AppiumDriver(new Uri("http://127.0.0.1:4723/wd/hub"), options);
        }
        else
        {
            throw new PlatformNotSupportedException();
        }
    }

    public void Dispose()
    {
        try { Session?.Quit(); } catch { }
    }
}

[CollectionDefinition("Default")]
public class DefaultCollection : ICollectionFixture<AppFixture> { }
```

:::tip
在 macOS 上，请用 `bundleId` 而非文件路径来指明你的应用，并先把应用构建成 `.app` 包。
:::

## 编写测试 {#writing-tests}

测试用 `FindElementByAccessibilityId` 来定位控件。这之所以行得通，是因为 Avalonia 会通过平台的无障碍 API 暴露 `AutomationProperties.AutomationId` 的值（或控件的 `Name`）。

### 给控件设置 AutomationId {#setting-automationid-on-controls}

给控件配上 `AutomationId`，测试才能稳稳地找到它们：

```xml
<Button AutomationProperties.AutomationId="SubmitButton" Content="Submit" />
<TextBox AutomationProperties.AutomationId="NameInput" />
<CheckBox AutomationProperties.AutomationId="AgreeCheckBox" Content="I agree" />
```

### 一个基础测试 {#a-basic-test}

```csharp
using OpenQA.Selenium.Appium;
using Xunit;

[Collection("Default")]
public class ButtonTests
{
    private readonly AppiumDriver _session;

    public ButtonTests(AppFixture fixture)
    {
        _session = fixture.Session;
    }

    [Fact]
    public void Click_Button_Updates_Text()
    {
        var button = _session.FindElement(MobileBy.AccessibilityId("SubmitButton"));
        var output = _session.FindElement(MobileBy.AccessibilityId("OutputText"));

        button.Click();

        Assert.Equal("Submitted", output.Text);
    }
}
```

### 测试复选框状态 {#testing-checkbox-state}

```csharp
[Fact]
public void CheckBox_Toggles_On_Click()
{
    var checkBox = _session.FindElement(MobileBy.AccessibilityId("AgreeCheckBox"));

    // Read initial state via the accessibility attribute
    var initialState = checkBox.GetAttribute("Toggle.ToggleState");
    Assert.Equal("0", initialState); // 0 = unchecked

    checkBox.Click();

    var newState = checkBox.GetAttribute("Toggle.ToggleState");
    Assert.Equal("1", newState); // 1 = checked
}
```

### 测试文本输入 {#testing-text-input}

```csharp
[Fact]
public void TextBox_Accepts_Input()
{
    var textBox = _session.FindElement(MobileBy.AccessibilityId("NameInput"));

    textBox.Clear();
    textBox.SendKeys("Avalonia");

    Assert.Equal("Avalonia", textBox.Text);
}
```

## 平台专属的测试 {#platform-specific-tests}

有些测试只在特定平台上才讲得通（比如 macOS 上的原生菜单测试）。你可以自定义一个特性，在不支持的平台上跳过这些测试：

```csharp
using System.Runtime.InteropServices;
using Xunit;

[Flags]
public enum TestPlatforms
{
    Windows = 0x01,
    MacOS = 0x02,
    Linux = 0x04,
    All = Windows | MacOS | Linux
}

public sealed class PlatformFactAttribute : FactAttribute
{
    public PlatformFactAttribute(TestPlatforms platforms)
    {
        if (!IsSupported(platforms))
        {
            Skip = $"Test is not supported on {RuntimeInformation.OSDescription}";
        }
    }

    private static bool IsSupported(TestPlatforms platforms)
    {
        if (OperatingSystem.IsWindows()) return platforms.HasFlag(TestPlatforms.Windows);
        if (OperatingSystem.IsMacOS()) return platforms.HasFlag(TestPlatforms.MacOS);
        if (OperatingSystem.IsLinux()) return platforms.HasFlag(TestPlatforms.Linux);
        return false;
    }
}
```

把它用在面向特定平台的测试上：

```csharp
[PlatformFact(TestPlatforms.MacOS)]
public void Native_Menu_Shows_App_Name()
{
    // macOS-only test
}
```

## 跨平台辅助方法 {#cross-platform-helpers}

WinAppDriver 与 macOS 驱动在特性名称和元素查找上可能有出入。写几个工具方法，能让测试代码清爽不少：

```csharp
public static class ElementExtensions
{
    public static string GetName(this AppiumElement element)
    {
        if (OperatingSystem.IsWindows())
            return element.GetAttribute("Name");
        return element.GetAttribute("title");
    }

    public static bool? GetIsChecked(this AppiumElement element)
    {
        var value = element.GetAttribute("Toggle.ToggleState")
            ?? element.GetAttribute("value");

        return value switch
        {
            "0" => false,
            "1" => true,
            _ => null // indeterminate
        };
    }
}
```

## 运行测试 {#running-tests}

### Windows

先启动 WinAppDriver（它以本地服务器的形式运行）：

```
"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
```

然后运行你的测试：

```bash
dotnet test
```

### macOS

启动 Appium 服务器：

```bash
appium
```

然后在另一个终端里运行你的测试：

```bash
dotnet test
```

## CI/CD 方面的注意事项 {#cicd-considerations}

- **Windows**：测试开始前 WinAppDriver 必须已在运行。在 CI 中请加一个启动它的准备步骤。
- **macOS**：必须装好 Appium 和 mac2 驱动，并把无障碍权限授予 CI 代理。
- **Linux**：Appium 在 Linux 桌面上没有稳定的驱动。Linux CI 请改用[无头测试](/docs/testing/setting-up-the-headless-platform)。

## 另请参阅 {#see-also}

- [用 XUnit 做无头测试](/docs/testing/headless-xunit)：快速的进程内单元测试。
- [用 NUnit 做无头测试](/docs/testing/headless-nunit)：无头测试的 NUnit 集成。
- [无头平台配置](/docs/testing/setting-up-the-headless-platform)：模拟输入与捕获帧。
- [Avalonia 自己的 Appium 测试](https://github.com/AvaloniaUI/Avalonia/tree/master/tests/Avalonia.IntegrationTests.Appium)：Avalonia 内部使用的测试套件。
- [Appium 文档](https://appium.io/docs/en/latest/)：Appium 官方指南。
