---
id: window-how-to
title: "操作指南：使用窗口"
description: 尺寸、位置、对话框、多窗口应用、启动行为与系统边框选项。
doc-type: how-to
---

本指南介绍 Window 的常见场景：尺寸、位置、对话框、多窗口应用、启动行为与系统边框。

## 设置窗口的尺寸与位置 {#setting-window-size-and-position}

### 启动时固定尺寸 {#fixed-size-on-startup}

```xml
<Window Width="800" Height="600"
        WindowStartupLocation="CenterScreen">
```

### 最小与最大尺寸 {#minimum-and-maximum-size}

```xml
<Window MinWidth="400" MinHeight="300"
        MaxWidth="1920" MaxHeight="1080">
```

### 启动位置 {#startup-location}

| 值 | 说明 |
|---|---|
| `Manual` | 由 `Position` 属性指定位置。 |
| `CenterScreen` | 在主屏幕上居中。 |
| `CenterOwner` | 在所有者窗口上居中（适用于对话框）。 |

## 显示一个对话框窗口 {#showing-a-dialog-window}

用 `ShowDialog<T>` 打开模态对话框并取回结果：

```csharp
var dialog = new SettingsWindow();
var result = await dialog.ShowDialog<bool>(this);
if (result)
{
    // User confirmed
}
```

调用 `Close` 并传入一个值即可返回结果：

```csharp
// In the dialog window
private void OnOkClick(object sender, RoutedEventArgs e)
{
    Close(true);
}

private void OnCancelClick(object sender, RoutedEventArgs e)
{
    Close(false);
}
```

## 获取父窗口 {#getting-the-parent-window}

在任意控件中都可以使用 `TopLevel.GetTopLevel`：

```csharp
var topLevel = TopLevel.GetTopLevel(this);
if (topLevel is Window window)
{
    await new MyDialog().ShowDialog<bool>(window);
}
```

## Preventing Window Close

处理 `Closing` 事件即可拦截关闭操作：

```csharp
protected override void OnClosing(WindowClosingEventArgs e)
{
    if (HasUnsavedChanges)
    {
        e.Cancel = true;
        // Show save prompt
    }
    base.OnClosing(e);
}
```

## Window State (Minimize, Maximize, Restore)

```csharp
// Programmatically control window state
window.WindowState = WindowState.Maximized;
window.WindowState = WindowState.Minimized;
window.WindowState = WindowState.Normal;
```

```xml
<Button Content="Maximize" Command="{Binding MaximizeCommand}" />
```

```csharp
[RelayCommand]
private void Maximize()
{
    if (Application.Current?.ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
    {
        var window = desktop.MainWindow;
        window.WindowState = window.WindowState == WindowState.Maximized
            ? WindowState.Normal
            : WindowState.Maximized;
    }
}
```

## 禁用最小化与最大化按钮 {#disabling-minimize-and-maximize-buttons}

用 `CanMinimize` 和 `CanMaximize` 控制标题栏上这些按钮是否可用：

```xml
<Window CanMinimize="False" CanMaximize="False">
```

当 `CanResize` 为 `false` 时，`CanMaximize` 会自动被设为 `false`。

:::note
各平台的表现不尽相同：Windows 上被禁用的按钮会隐藏起来，macOS 上显示为灰色，Linux 上则取决于窗口管理器。
:::

## 隐藏标题栏（无边框窗口） {#hiding-the-title-bar-chromeless-window}

关掉系统装饰，做一个无边框窗口：

```xml
<Window WindowDecorations="None"
        ExtendClientAreaToDecorationsHint="True"
        Background="Transparent"
        TransparencyLevelHint="AcrylicBlur">
```

### 带拖拽区域的自定义标题栏 {#custom-title-bar-with-drag-region}

用 `WindowDecorationProperties.ElementRole` 附加属性把某个元素标记为标题栏拖拽区域，之后拖动和双击最大化的行为由操作系统自动接管：

```xml
<Grid RowDefinitions="32,*">

    <!-- Custom title bar -->
    <Border Grid.Row="0" Background="#1E1E2E"
            WindowDecorationProperties.ElementRole="TitleBar">
        <DockPanel Margin="8,0">
            <TextBlock Text="My App" VerticalAlignment="Center" Foreground="White" />
            <StackPanel DockPanel.Dock="Right" Orientation="Horizontal"
                        HorizontalAlignment="Right">
                <!-- ElementRole must be set per button for some platforms -->
                <Button WindowDecorationProperties.ElementRole="MinimizeButton" Content="_" Click="OnMinimize" />
                <Button WindowDecorationProperties.ElementRole="MaximizeButton" Content="□" Click="OnMaximize" />
                <Button WindowDecorationProperties.ElementRole="CloseButton" Content="✕" Click="OnClose" />
            </StackPanel>
        </DockPanel>
    </Border>

    <!-- Content -->
    <ContentControl Grid.Row="1" Content="Hello world!" />

</Grid>
```

`ElementRole` 属性支持以下取值：

| 值 | 行为 |
|---|---|
| `None` | 不启用任何特殊的窗口边框行为（默认）。 |
| `TitleBar` | 充当可拖动的标题栏区域。 |
| `ResizeN`, `ResizeS`, `ResizeE`, `ResizeW` | 指定边缘的尺寸调整手柄。 |
| `ResizeNE`, `ResizeNW`, `ResizeSE`, `ResizeSW` | 指定角落的尺寸调整手柄。 |

`TitleBar` 区域内的可交互控件（比如按钮）照常接收输入，不会触发窗口拖动。

## 多窗口应用 {#multi-window-application}

从主窗口打开其他窗口：

```csharp
[RelayCommand]
private void OpenNewWindow()
{
    var window = new SecondaryWindow
    {
        DataContext = new SecondaryViewModel()
    };
    window.Show();
}
```

若要一个非模态、但始终浮在所有者之上的窗口：

```csharp
var toolWindow = new ToolWindow();
toolWindow.Show(ownerWindow); // Stays above owner
```

## 保存与恢复窗口位置 {#saving-and-restoring-window-position}

```csharp
protected override void OnOpened(EventArgs e)
{
    base.OnOpened(e);
    var settings = LoadSettings();
    if (settings.WindowWidth > 0)
    {
        Width = settings.WindowWidth;
        Height = settings.WindowHeight;
    }
}

protected override void OnClosing(WindowClosingEventArgs e)
{
    SaveSettings(new AppSettings
    {
        WindowWidth = Width,
        WindowHeight = Height,
        WindowState = WindowState
    });
    base.OnClosing(e);
}
```

## Window Transparency

```xml
<!-- Acrylic blur (platform-dependent) -->
<Window TransparencyLevelHint="AcrylicBlur"
        Background="Transparent">
    <Panel>
        <ExperimentalAcrylicBorder Material="{DynamicResource AcrylicMaterial}" />
        <!-- Content on top of acrylic -->
    </Panel>
</Window>
```

在运行时查看支持哪些透明度级别：

```csharp
var supported = this.ActualTransparencyLevel;
```

若 `ActualTransparencyLevel` 返回的级别低于你请求的，这多半是操作系统的限制，而非配置有误。比如 macOS 和 Linux 对透明的支持更有限，而 Windows 在省电模式下可能会关掉合成器特效。稳妥起见，请设一个颜色不透明、与界面相称的 [`TransparencyBackgroundFallback`](/docs/fundamentals/top-level#transparencybackgroundfallback)，以防用户设备上压根用不了透明。

:::note
Avalonia 目前还不支持 WPF 那种「透明穿透点击」的行为。

若你想用原生平台 API 做一个可穿透点击的透明窗口，请参阅我们关于[原生平台互操作](/docs/app-development/native-interop)的说明。
:::

## Window Icon

```xml
<Window Icon="/Assets/app-icon.ico">
```

也可以在代码中设置：

```csharp
Icon = new WindowIcon(AssetLoader.Open(new Uri("avares://MyApp/Assets/app-icon.ico")));
```

## Key Properties

| 属性 | 类型 | 说明 |
|---|---|---|
| `Title` | `string` | 窗口标题栏上的文字。 |
| `WindowState` | `WindowState` | `Normal`, `Minimized`, `Maximized`, `FullScreen`. |
| `WindowStartupLocation` | `WindowStartupLocation` | `Manual`, `CenterScreen`, `CenterOwner`. |
| `WindowDecorations` | `WindowDecorations` | `Full`, `BorderOnly`, `None`. |
| `CanResize` | `bool` | 用户能否调整窗口大小。 |
| `CanMinimize` | `bool` | 最小化按钮是否可用，默认为 `true`。 |
| `CanMaximize` | `bool` | 最大化按钮是否可用，默认为 `true`。当 `CanResize` 为 `false` 时会自动变成 `false`。 |
| `Topmost` | `bool` | 让窗口始终浮在其他窗口之上。 |
| `ShowInTaskbar` | `bool` | 在操作系统任务栏中显示。 |
| `Icon` | `WindowIcon` | 标题栏和任务栏上的窗口图标。 |
| `TransparencyLevelHint` | `WindowTransparencyLevel` | 请求的透明度：`None`、`Transparent`、`Blur`、`AcrylicBlur`、`Mica`。 |

## See Also

- [Window 控件参考](/controls/primitives/window)：属性表。
- [对话框操作指南](/docs/how-to/dialogs-how-to)：对话框用法与文件选择器。
- [窗口管理](/docs/app-development/window-management)：窗口生命周期。
- [应用生命周期](/docs/fundamentals/application-lifetimes)：桌面与移动端的生命周期模型。
