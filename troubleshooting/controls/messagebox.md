---
id: messagebox
title: MessageBox
description: 了解 Avalonia 为什么不内置 MessageBox，以及如何借助第三方库补上消息框功能。
doc-type: troubleshooting
---

Avalonia 没有内置 `MessageBox` 控件。这是有意为之：Avalonia 面向多个平台（桌面、移动、浏览器），而传统的模态消息框并非在哪儿都讲得通。这项功能仍在考虑之中。

进展和讨论请见 GitHub 上的 [MessageBox 功能请求](https://github.com/AvaloniaUI/Avalonia/issues/670)。

## 给你的应用加上消息框功能 {#adding-message-box-functionality-to-your-app}

既然没有原生的 `MessageBox` API，你就得用第三方库或自己写个对话框。下面几步带你用上社区的包：

### 第 1 步：挑一个库 {#step-1-choose-a-library}

看看下面列出的选项，挑一个合你项目胃口的。有的免费开源，有的是商业产品（标有 `$`）。

### 第 2 步：安装 NuGet 包 {#step-2-install-the-nuget-package}

用 .NET CLI 或 IDE 的 NuGet 包管理器安装。比如要装 `MessageBox.Avalonia`：

```bash
dotnet add package MessageBox.Avalonia
```

### 第 3 步：弹出消息框 {#step-3-show-a-message-box}

各个库的 API 不尽相同。下面的例子用 `MessageBox.Avalonia` 弹出一个简单的信息对话框：

```csharp
using MsBox.Avalonia;
using MsBox.Avalonia.Enums;

var box = MessageBoxManager
    .GetMessageBoxStandard("Title", "Hello from Avalonia!", ButtonEnum.Ok);

await box.ShowAsync();
```

若你需要知道用户选了什么（比如确定还是取消），把返回值接住：

```csharp
var result = await box.ShowAsync();

if (result == ButtonResult.Ok)
{
    // Handle confirmation
}
```

### 第 4 步：处理平台差异 {#step-4-handle-platform-differences}

有几种边界情况要留心：

- **浏览器和移动端**：模态对话框的表现未必与桌面端一致。有些库会把对话框内联渲染，而不是另开一个窗口。请在你打算支持的每个平台上都试一遍所选的库。
- **单视图应用**：若你的应用用的是 `SingleViewApplicationLifetime`（移动端和浏览器上很常见），就没法新建 `Window` 来承载对话框。请选用支持叠加层或应用内对话框渲染的库，比如 `DialogHost.Avalonia`。
- **线程**：务必在 UI 线程上弹出对话框。若是从后台线程调用，请用 `Dispatcher.UIThread.InvokeAsync` 派发。

## 第三方 `MessageBox` 实现 {#third-party-messagebox-implementations}

| 库 | 类型 |
|---|---|
| [MessageBox.Avalonia](https://github.com/AvaloniaCommunity/MessageBox.Avalonia) | 免费 / 开源 |
| [DialogHost.Avalonia](https://github.com/AvaloniaUtils/DialogHost.Avalonia) | 免费 / 开源 |
| [Ursa.Avalonia](https://github.com/irihitech/Ursa.Avalonia) | 免费 / 开源 |
| [AtomUI.Avalonia](https://github.com/chinware/AtomUI) | 免费 / 开源 |
| [Actipro Avalonia UI Controls](https://www.actiprosoftware.com/products/controls/avalonia) | Commercial |
| [Eremex Avalonia UI Controls](https://eremexcontrols.net/controls/windows-and-dialogs/messagebox/) | Commercial |

## 自己动手写消息框 {#building-your-own-message-box}

若你不想为此引入第三方依赖，自己写个简单的对话框窗口也不难：

1. 新建一个 `Window`，在 AXAML 中摆好消息内容和按钮。
2. 用 `window.ShowDialog(ownerWindow)` 打开它，它返回一个可以 `await` 的 `Task`。
3. 关闭前给 `Window.Close(result)` 赋值，以此设定对话框结果。

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Confirm"
        Width="300" Height="150"
        WindowStartupLocation="CenterOwner">
    <StackPanel Margin="20" Spacing="16">
        <TextBlock Text="Are you sure?" />
        <StackPanel Orientation="Horizontal" HorizontalAlignment="Right" Spacing="8">
            <Button Content="Yes" Click="OnYesClick" />
            <Button Content="No" Click="OnNoClick" />
        </StackPanel>
    </StackPanel>
</Window>
```

```csharp
public partial class ConfirmDialog : Window
{
    public ConfirmDialog()
    {
        InitializeComponent();
    }

    private void OnYesClick(object? sender, RoutedEventArgs e)
    {
        Close(true);
    }

    private void OnNoClick(object? sender, RoutedEventArgs e)
    {
        Close(false);
    }
}
```

弹出对话框并读取结果：

```csharp
var dialog = new ConfirmDialog();
var result = await dialog.ShowDialog<bool>(this);

if (result)
{
    // User clicked Yes
}
```

This approach only works in desktop applications that use `ClassicDesktopStyleApplicationLifetime`. For single-view apps, you need an overlay-based solution instead.

## 另请参阅 {#see-also}

- [Window 控件](/controls/primitives/window)
- [How to work with dialogs](/docs/how-to/dialogs-how-to)
- [MessageBox feature request (GitHub)](https://github.com/AvaloniaUI/Avalonia/issues/670)
