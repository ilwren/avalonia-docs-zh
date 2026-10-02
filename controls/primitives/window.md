---
id: window
title: Window
description: 一个顶层内容控件，代表操作系统窗口，带标题栏、图标以及关闭/最小化/最大化等窗口外框。
doc-type: reference
---

[`Window`](/api/avalonia/controls/window) 是一个顶层 [`ContentControl`](/controls/data-display/contentcontrol)，代表一个操作系统窗口。它提供标题栏、图标和系统外框（关闭、最小化、最大化按钮）——这些正是用户对桌面应用的期待。

一般不会直接创建 `Window` 的实例，而是为应用需要的每一种窗口各写一个 `Window` 子类。

:::tip
`Window` 只在桌面平台（Windows、macOS、Linux）上可用。如果你的目标是移动端或浏览器，请改用 [`UserControl`](/controls/primitives/usercontrol) 搭配导航框架。
:::

## 常用属性 {#common-properties}

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `Title` | `string` | 标题栏中显示的文字。 |
| `Icon` | `WindowIcon` | 标题栏和任务栏中显示的图标。 |
| `SizeToContent` | `SizeToContent` | 控制窗口是否自动调整大小以适应内容：横向、纵向，或两者皆是。 |
| `WindowState` | `WindowState` | 获取或设置窗口处于 `Normal`、`Minimized`、`Maximized` 还是 `FullScreen` 状态。 |
| `CanResize` | `bool` | 获取或设置用户能否调整窗口大小。 |
| `ShowInTaskbar` | `bool` | 获取或设置窗口是否出现在操作系统任务栏中。 |
| `Topmost` | `bool` | 获取或设置窗口是否始终置于其他窗口之上。 |
| `WindowDecorations` | `WindowDecorations` | 控制窗口外框（标题栏与边框）。设为 `None` 可得到无边框窗口。 |
| `ExtendClientAreaToDecorationsHint` | `bool` | 为 `true` 时，内容会延伸进标题栏区域，从而可以自定义窗口外框。 |

## 显示、隐藏与关闭窗口 {#show-hide-and-close-a-window}

调用 `Show` 方法即可显示窗口：

```csharp
var window = new MyWindow();
window.Show();
```

调用 `Close` 即可关闭窗口，效果与用户点击窗口的关闭按钮相同：

```csharp
window.Close();
```

:::warning
窗口一旦关闭就无法再次显示，对已关闭的窗口调用 `Show` 会抛出异常。如果之后还要再显示同一个窗口，请用 `Hide` 而不是 `Close`。
:::

```csharp
window.Hide();

// You can show the window again later.
window.Show();
```

另请参阅[阻止窗口关闭](#prevent-a-window-from-closing)。

## 以对话框方式显示窗口 {#show-a-window-as-a-dialog}

调用 `ShowDialog` 可以把窗口显示为模态对话框。该方法要求传入一个所有者窗口，好让系统知道对话框归属于哪个窗口：

```csharp
// "this" is the current Window instance.
// You can also obtain the main window from
// Application.ApplicationLifetime cast to IClassicDesktopStyleApplicationLifetime.
var ownerWindow = this;
var dialog = new MyWindow();
dialog.ShowDialog(ownerWindow);
```

`ShowDialog` 返回一个 `Task`，因此可以 `await` 它，直到对话框关闭：

```csharp
var dialog = new MyWindow();
await dialog.ShowDialog(ownerWindow);
```

### 从对话框返回结果 {#return-a-result-from-a-dialog}

给 `Close` 方法传入一个值，对话框就能返回结果；调用方则通过泛型的 `ShowDialog<T>` 重载读取它：

```csharp
public class MyDialog : Window
{
    public MyDialog()
    {
        InitializeComponent();
    }

    private void OkButton_Click(object? sender, EventArgs e)
    {
        Close("OK Clicked!");
    }
}
```

```csharp
var dialog = new MyDialog();

// The result is a string, so use ShowDialog<string>.
var result = await dialog.ShowDialog<string>(ownerWindow);
```

## 阻止窗口关闭 {#prevent-a-window-from-closing}

处理 `Closing` 事件并设置 `e.Cancel = true`，即可阻止窗口关闭：

```csharp
window.Closing += (s, e) =>
{
    e.Cancel = true;
};
```

一种常见做法是把窗口隐藏而不是关闭，这样之后还能再把它显示出来：

```csharp
window.Closing += (s, e) =>
{
    ((Window)s!).Hide();
    e.Cancel = true;
};
```

## 实用提示 {#practical-notes}

- **启动窗口。** 应用的主窗口通常在 `App.axaml.cs` 中设定：在 `IClassicDesktopStyleApplicationLifetime` 上给 `MainWindow` 赋值。详见[主窗口](/docs/fundamentals/main-window)。
- **多窗口。** 想开几个窗口就开几个：新建实例并调用 `Show` 即可。各个窗口在同一个应用内独立运行。
- **定位。** 用 `Position` 属性（类型为 `PixelPoint`）设置窗口的屏幕坐标，或把 `WindowStartupLocation` 设为 `CenterScreen` 或 `CenterOwner`。
- **关闭行为。** 最后一个窗口关闭时，应用默认随之退出。可以在应用生存期上设置 `ShutdownMode` 来改变这一行为。

## 另请参阅 {#see-also}

- [主窗口](/docs/fundamentals/main-window)
- [窗口管理](/docs/app-development/window-management)
- [操作指南：使用窗口](/docs/how-to/window-how-to)
- [`ContentControl`](/controls/data-display/contentcontrol)
- [`UserControl`](/controls/primitives/usercontrol)
- [`Window` 源码（GitHub）](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Window.cs)
- [`Window` API 参考](/api/avalonia/controls/window)