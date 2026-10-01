---
id: index
title: 虚拟键盘概述
tags:
  - avalonia pro
  - avalonia enterprise
---

虚拟键盘组件为 Avalonia 应用提供一个屏幕键盘。它面向触摸设备和自助终端等没有实体键盘的场景，让用户可以通过触屏或鼠标点击来输入文字。

:::info
该组件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 及以上版本。
:::

虚拟键盘组件包含下列类：

- [`VirtualKeyboardScope`](/controls/input/text-input/virtualkeyboard/virtualkeyboardscope)：容器控件，负责管理键盘的显示隐藏和输入法。
- [`VirtualKeyboard`](/controls/input/text-input/virtualkeyboard/virtualkeyboard-control)：真正的键盘控件，可以手动摆放。
- `VirtualKeyboardInputMethod`：代表一种具体的输入法或键盘布局。

## 快速上手 {#getting-started}

1. 运行 `dotnet add package` 安装 `Avalonia.Controls.VirtualKeyboard` NuGet 包。

```bash
dotnet add package Avalonia.Controls.VirtualKeyboard
```

2. 在可执行项目文件（`.csproj`）中填入你的 Avalonia 许可证密钥。密钥可以在 [Avalonia 门户](https://portal.avaloniaui.net)中获取。

```xml
<ItemGroup>
  <AvaloniaUILicenseKey Include="YOUR_LICENSE_KEY" />
</ItemGroup>
```

:::tip
对于多项目解决方案，可以把许可证密钥放进[环境变量](https://learn.microsoft.com/en-us/visualstudio/msbuild/how-to-use-environment-variables-in-a-build)或[共享 props 文件](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory?view=vs-2022#directorybuildprops-example)，免得到处重复。
:::

3. 在 `App.axaml` 文件中用 `StyleInclude` 引用 `VirtualKeyboard` 的 Fluent 主题，这会带入正确呈现虚拟键盘所需的资源。

```xml
<Application.Styles>
   <StyleInclude Source="avares://Avalonia.Controls.VirtualKeyboard/Themes/Fluent.axaml"/>
   <!-- other styles -->
</Application.Styles>
```

关于安装 Avalonia Pro 控件的更多内容，请参阅[安装 Avalonia Pro](/tools/installing-avalonia-pro)。

## 基本用法 {#basic-usage}

### Using VirtualKeyboardScope (Recommended)

给应用加上虚拟键盘最省事的办法是使用 `VirtualKeyboardScope` 控件：文本输入控件获得焦点时，它会自动显示和隐藏键盘：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d" d:DesignWidth="600" d:DesignHeight="600"
        Width="600" Height="600"
        x:Class="YourNamespace.YourWindow"
        Title="Virtual Keyboard Sample">
    <VirtualKeyboardScope InputMethods="en-US:kbd:standard, de:kbd:standard, ja:ime:kana">
        <StackPanel>
            <TextBlock>Hello world!</TextBlock>
            <TextBox PlaceholderText="Type here"/>
        </StackPanel>
    </VirtualKeyboardScope>
</Window>
```

### Using VirtualKeyboard Directly

若需要更精细的控制，可以直接使用 `VirtualKeyboard` 控件，并指定目标输入元素。

无论当前焦点在哪里，输入都会送往指定的 `Target` 元素。

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Virtual Keyboard Sample"
        Width="400" Height="600">
    <StackPanel>
        <TextBox x:Name="InputBox" Width="300" Margin="10"/>
        <VirtualKeyboard Target="{Binding ElementName=InputBox}" 
                           InputMethods="en-US:kbd:standard, de:kbd:standard, ja:ime:kana"
                           Margin="10"/>
    </StackPanel>
</Window>
```

## 管理输入法 {#managing-input-methods}

虚拟键盘支持多种输入法和键盘布局。指定要包含哪些输入法的做法如下：

### XAML

```xml
<VirtualKeyboardScope InputMethods="en-US:kbd:standard, de:kbd:standard, ja:ime:kana">
    <!-- Your content here -->
</VirtualKeyboardScope>
```

### C#

```csharp
// Get all available input methods for specific languages
var inputMethods = new List<VirtualKeyboardInputMethod>
{
    VirtualKeyboardInputMethod.GetInputMethodsForLanguage("en-US").First(),
    VirtualKeyboardInputMethod.GetInputMethodsForLanguage("de").First(),
    VirtualKeyboardInputMethod.GetInputMethodsForLanguage("ja").First()
};

// Assign to the VirtualKeyboardScope
myKeyboardScope.InputMethods = inputMethods;
```

### 获取输入法 {#retrieving-input-methods}

```csharp
// Get all supported languages
var languages = VirtualKeyboardInputMethod.GetSupportedLanguages();

// Get input methods for a specific language
var englishInputMethods = VirtualKeyboardInputMethod.GetInputMethodsForLanguage("en-US");

// Get a specific input method by ID
var japaneseKana = VirtualKeyboardInputMethod.GetInputMethodById("ja:ime:kana");
```

## 输入法标识符 {#input-method-identifiers}

受支持的输入法及其标识符列表，请参阅[虚拟键盘控件](/controls/input/text-input/virtualkeyboard/virtualkeyboard-control#input-methods)页面。

## RIME 输入法引擎 {#rime-input-method-engine}

虚拟键盘支持用 [RIME](https://rime.im/) 输入法引擎输入中文。RIME 支持以独立插件包的形式提供。

安装与配置说明请参阅 [`VirtualKeyboard` 控件参考](/controls/input/text-input/virtualkeyboard/virtualkeyboard-control#rime-input-method-engine)。

## 文本输入选项 {#text-input-options}

通过 `TextInputOptions` 附加属性，可以为不同的输入字段定制虚拟键盘的行为：

```xml
<TextBox TextInputOptions.ContentType="Email" 
         TextInputOptions.ReturnKeyType="Search" />
```

`ContentType` 的可选值：
- `Normal`
- `Email`
- `Url`
- `Digits`

`ReturnKeyType` 的可选值：
- `Default`
- `Done`
- `Go`
- `Next`
- `Previous`
- `Return`
- `Search`
- `Send`

## 另请参阅 {#see-also}

- [VirtualKeyboard 控件](/controls/input/text-input/virtualkeyboard)
- [VirtualKeyboardScope 控件](/controls/input/text-input/virtualkeyboard/virtualkeyboardscope)
