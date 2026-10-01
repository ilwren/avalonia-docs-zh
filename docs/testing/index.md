---
id: index
title: 测试
---

Avalonia 支持多种测试策略，各有各的用武之地。把它们搭配起来，就能构成一套分层的测试体系，覆盖视图模型逻辑、控件行为、视觉输出乃至端到端的用户流程。

## 测试策略 {#testing-strategies}

| 策略 | 测什么 | 速度 | Requires UI |
|---|---|---|---|
| **单元测试** | 视图模型逻辑、服务、转换器 | Fast | No |
| **无头测试** | 控件、布局、数据绑定、输入 | Fast | 不需要（进程内运行） |
| **视觉回归测试** | 渲染出的像素输出 | Medium | 不需要（无头 + Skia） |
| **Appium UI 测试** | 完整应用、平台集成、无障碍 | Slow | 需要（真实窗口） |

### 单元测试 {#unit-tests}

对不依赖 Avalonia 控件的代码，写标准的 .NET 单元测试即可。视图模型、值转换器、服务和业务逻辑都能用 xUnit、NUnit 或 MSTest 测试，无需任何 Avalonia 专属配置。

```csharp
[Fact]
public void ViewModel_Increments_Count()
{
    var vm = new MainViewModel();
    vm.IncrementCommand.Execute(null);
    Assert.Equal(1, vm.Count);
}
```

### 无头测试 {#headless-tests}

[无头平台](/docs/testing/setting-up-the-headless-platform)不开窗口，在内存中跑起 Avalonia 完整的控件树、布局引擎、样式和数据绑定，你可以通过辅助方法模拟键盘和鼠标输入。要测控件行为、数据绑定、焦点管理和命令执行，选它就对了。

Avalonia 为 [xUnit](/docs/testing/headless-xunit) 和 [NUnit](/docs/testing/headless-nunit) 提供了集成包，配置的活儿它们都替你办了。

```csharp
[AvaloniaFact]
public void TextBox_Accepts_Input()
{
    var textBox = new TextBox();
    var window = new Window { Content = textBox };
    window.Show();

    textBox.Focus();
    window.KeyTextInput("Hello");

    Assert.Equal("Hello", textBox.Text);
}
```

### 视觉回归测试 {#visual-regression-tests}

在无头模式下启用 Skia 渲染器，你就能把渲染出的帧捕获为位图，再与基准图比对，从而揪出控件渲染、主题和布局中意料之外的视觉变化。配置细节见[捕获最后一帧渲染结果](/docs/testing/setting-up-the-headless-platform#visual-regression-testing)。

### Appium UI 测试 {#appium-ui-tests}

[Appium](/docs/testing/ui-testing-with-appium) 会在真实窗口中启动你编译好的应用，并通过平台的无障碍树来驱动它。这样测的是一整条链路：原生窗口系统、菜单、焦点、平台专属行为和无障碍支持。Appium 测试虽慢，却能验证应用在用户眼中是否真的好用。

Avalonia 自身也用 Appium 在 Windows 和 macOS 上测试框架。

## 该选哪种方式 {#choosing-the-right-approach}

- **先从单元测试起步**，覆盖视图模型和服务。它们快、稳，还不用特别配置。
- **再补上无头测试**，覆盖那些依赖 Avalonia 属性系统、布局或输入处理的控件行为。
- **若应用中有自定义控件或主题、像素级的正确性要紧**，就再加上视觉回归测试。
- **关键用户流程、平台专属特性和无障碍验证，交给 Appium 测试。**

## 另请参阅 {#see-also}

- [无头测试平台](/docs/testing/setting-up-the-headless-platform)：输入模拟、帧捕获与异步处理。
- [用 XUnit 做无头测试](/docs/testing/headless-xunit)：XUnit 集成配置。
- [用 NUnit 做无头测试](/docs/testing/headless-nunit)：NUnit 集成配置。
- [用 Appium 做 UI 测试](/docs/testing/ui-testing-with-appium)：借助真实窗口做端到端测试。
