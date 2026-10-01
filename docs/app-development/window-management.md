---
id: window-management
title: 窗口管理
description: 在 Avalonia 桌面应用中创建、配置和管理窗口与对话框。
doc-type: overview
---

Avalonia 提供了灵活的窗口系统，既能做单窗口应用，也能做多窗口应用。本文介绍常见的窗口管理套路。

## 创建窗口 {#creating-windows}

窗口通常用 XAML 定义，再配一个代码隐藏类：

```xml title="SecondWindow.axaml"
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="MyApp.SecondWindow"
        Title="Second Window"
        Width="400" Height="300">
    <TextBlock Text="Hello from the second window" />
</Window>
```

```csharp title="SecondWindow.axaml.cs"
public partial class SecondWindow : Window
{
    public SecondWindow()
    {
        InitializeComponent();
    }
}
```

### 打开窗口 {#opening-a-window}

```csharp
var window = new SecondWindow();
window.Show(); // Non-modal: both windows remain interactive
```

### 打开模态对话框 {#opening-a-modal-dialog}

```csharp
var dialog = new SecondWindow();
var result = await dialog.ShowDialog<string>(parentWindow);
// Execution resumes here after the dialog closes
```

对话框打开期间父窗口会被禁用。调用 `ShowDialog` 时，把拥有者窗口作为参数传进去。

### 关闭并返回结果 {#closing-with-a-result}

在对话框中调用 `Close` 并带上一个值，即可设置返回结果：

```csharp
// Inside the dialog
Close("user clicked OK");
```

这个值会从父窗口中的 `ShowDialog<T>` 调用处返回。

## 窗口属性 {#window-properties}

| 属性 | 说明 |
|---|---|
| `Title` | 显示在窗口标题栏上的文字。 |
| `Width`, `Height` | 初始尺寸。 |
| `MinWidth`, `MinHeight` | 允许的最小尺寸。 |
| `MaxWidth`, `MaxHeight` | 允许的最大尺寸。 |
| `WindowStartupLocation` | 窗口出现的位置：`Manual`、`CenterScreen`、`CenterOwner`。 |
| `Position` | 窗口在屏幕坐标系中的位置（当 `WindowStartupLocation` 为 `Manual` 时生效）。 |
| `CanResize` | 用户能否调整窗口大小。 |
| `CanMinimize` | 最小化按钮是否可用，默认为 `true`。 |
| `CanMaximize` | 最大化按钮是否可用，默认为 `true`。当 `CanResize` 为 `false` 时会自动变成 `false`。 |
| `IsDialog` | 只读。用 `ShowDialog` 打开窗口时为 `true`，用 `Show` 打开时为 `false`。 |
| `ShowInTaskbar` | 窗口是否出现在操作系统任务栏中。 |
| `Topmost` | 窗口是否始终置于其他窗口之上。 |
| `WindowState` | 当前状态：`Normal`、`Minimized`、`Maximized`、`FullScreen`。 |
| `WindowDecorations` | 标题栏与边框样式：`Full`、`BorderOnly`、`None`。 |
| `ExtendClientAreaToDecorationsHint` | 把客户区延伸到标题栏区域，以便自绘窗口外框。配合 `WindowDrawnDecorations` 使用，由应用自行绘制装饰。 |
| `Icon` | 显示在标题栏和任务栏上的窗口图标。 |
| `TransparencyLevelHint` | 启用窗口透明效果：`None`、`Transparent`、`AcrylicBlur`、`Mica`。详见[如何使用窗口](/docs/how-to/window-how-to)。 |
| `ClosingBehavior` | 控制拥有者关闭时子窗口的行为：`OwnerAndChildWindows`（默认，子窗口先关闭且可以取消）或 `OwnerWindowOnly`（只检查拥有者自己的 `Closing` 事件）。 |

## 窗口尺寸 {#window-sizing}

### 按内容确定尺寸 {#sizing-to-content}

设置 `SizeToContent` 可让窗口根据内容自行确定大小：

```xml
<Window SizeToContent="WidthAndHeight">
    <StackPanel Margin="20">
        <TextBlock Text="The window will size to fit this content." />
        <Button Content="OK" HorizontalAlignment="Right" Margin="0,10,0,0" />
    </StackPanel>
</Window>
```

| 值 | 行为 |
|---|---|
| `Manual` | 窗口显式使用 `Width` 和 `Height`（默认）。 |
| `Width` | 宽度随内容自适应，高度显式指定。 |
| `Height` | 高度随内容自适应，宽度显式指定。 |
| `WidthAndHeight` | 宽高都随内容自适应。 |

### 保存并恢复窗口位置 {#saving-and-restoring-window-position}

```csharp
protected override void OnOpened(EventArgs e)
{
    base.OnOpened(e);

    // Restore saved position
    if (Settings.WindowLeft >= 0 && Settings.WindowTop >= 0)
    {
        Position = new PixelPoint(Settings.WindowLeft, Settings.WindowTop);
        Width = Settings.WindowWidth;
        Height = Settings.WindowHeight;
    }
}

protected override void OnClosing(WindowClosingEventArgs e)
{
    base.OnClosing(e);

    // Save position
    Settings.WindowLeft = Position.X;
    Settings.WindowTop = Position.Y;
    Settings.WindowWidth = Width;
    Settings.WindowHeight = Height;
}
```

## 多窗口套路 {#multi-window-patterns}

### 跟踪已打开的窗口 {#tracking-open-windows}

```csharp
public static class WindowManager
{
    private static readonly List<Window> _openWindows = new();

    public static IReadOnlyList<Window> OpenWindows => _openWindows;

    public static void Register(Window window)
    {
        _openWindows.Add(window);
        window.Closed += (_, _) => _openWindows.Remove(window);
    }

    public static void CloseAll()
    {
        foreach (var window in _openWindows.ToList())
            window.Close();
    }
}
```

### 从控件找到所属窗口 {#finding-the-parent-window-from-a-control}

```csharp
var topLevel = TopLevel.GetTopLevel(myControl);
if (topLevel is Window window)
{
    // Use window
}
```

或者用扩展方法：

```csharp
var window = myControl.FindAncestorOfType<Window>();
```

## 阻止窗口关闭 {#preventing-window-close}

处理 `Closing` 事件即可拦截关闭动作，把 `e.Cancel = true` 设为 true 就能阻止关闭：

```csharp
protected override void OnClosing(WindowClosingEventArgs e)
{
    base.OnClosing(e);

    if (HasUnsavedChanges)
    {
        e.Cancel = true;
        // Show a save confirmation dialog instead
        _ = ShowSavePromptAsync();
    }
}
```

## 自定义标题栏 {#custom-title-bar}

要做自定义标题栏，先把客户区延伸进窗口装饰区，再用 `WindowDecorationProperties.ElementRole` 标出哪块区域算标题栏：

```xml
<Window ExtendClientAreaToDecorationsHint="True"
        WindowDecorations="None">
    <Grid RowDefinitions="32,*">
        <!-- Custom title bar -->
        <Border Grid.Row="0" Background="#2D2D2D"
                WindowDecorationProperties.ElementRole="TitleBar">
            <TextBlock Text="My App" Foreground="White"
                       VerticalAlignment="Center" Margin="12,0" />
        </Border>
        <!-- Content -->
        <Border Grid.Row="1">
            <TextBlock Text="Window content" />
        </Border>
    </Grid>
</Window>
```

标有 `WindowDecorationProperties.ElementRole="TitleBar"` 的元素支持原生的窗口拖动和双击最大化。放在标题栏区域内的交互控件（按钮、文本框）照常接收输入，不会触发拖动。

关于 `ElementRole` 各个取值的详细说明，请参阅[自定义标题栏操作指南](/docs/how-to/window-how-to#custom-title-bar-with-drag-region)。

## 窗口事件 {#window-events}

| 事件 | 触发时机 |
|---|---|
| `Opened` | 窗口首次显示出来。 |
| `Closing` | 窗口即将关闭，可以取消。 |
| `Closed` | 窗口已关闭。 |
| `Activated` | 窗口获得焦点。 |
| `Deactivated` | 窗口失去焦点。 |
| `PositionChanged` | 窗口被移动。 |
| `Resized` | 窗口尺寸发生变化。 |

## 与屏幕打交道 {#working-with-screens}

`Screens` API 提供已连接显示器的信息，可从任意 `TopLevel` 访问：

```csharp
var screens = TopLevel.GetTopLevel(this)?.Screens;
```

### 查询屏幕 {#querying-screens}

```csharp
// All connected screens
var allScreens = screens.All;

// Primary monitor
var primary = screens.Primary;

// Screen containing a specific window
var currentScreen = screens.ScreenFromWindow(this);

// Screen at a point
var screenAtPoint = screens.ScreenFromPoint(new PixelPoint(500, 300));
```

### 屏幕属性 {#screen-properties}

每个 `Screen` 对象都暴露以下信息：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Bounds` | `PixelRect` | 整块屏幕的边界，单位为像素。 |
| `WorkingArea` | `PixelRect` | 可用区域，不含任务栏和程序坞。 |
| `Scaling` | `double` | DPI 缩放系数（比如 96 DPI 为 1.0，144 DPI 为 1.5）。 |
| `IsPrimary` | `bool` | 是否为主显示器。 |
| `DisplayName` | `string?` | 操作系统报告的显示器名称。 |
| `CurrentOrientation` | `ScreenOrientation` | 屏幕方向（横向、纵向等）。 |

### 响应屏幕变化 {#responding-to-screen-changes}

订阅 `Changed` 事件，即可感知显示器的接入、移除或重新配置：

```csharp
screens.Changed += (sender, args) =>
{
    // Re-evaluate window placement or layout
    var count = screens.All.Count;
};
```

## 平台差异 {#platform-differences}

| 特性 | Windows | macOS | Linux |
|---|---|---|---|
| `Topmost` | Supported | Supported | Supported |
| `TransparencyLevelHint` | 所有层级 | `Transparent` only | 取决于合成器 |
| `WindowDecorations.None` | Supported | Supported | Supported |
| `ExtendClientAreaToDecorationsHint` | Supported | Supported | 支持有限 |
| 模态对话框 | 阻塞父窗口 | macOS 上呈现为 sheet 样式 | 阻塞父窗口 |

## 另请参阅 {#see-also}

- [主窗口](/docs/fundamentals/main-window)：应用的主要窗口。
- [应用生命周期](/docs/fundamentals/application-lifetimes)：应用生命周期如何管理窗口。
