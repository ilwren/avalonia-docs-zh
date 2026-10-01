---
id: notifications-how-to
title: "操作指南：显示通知与 toast"
description: 学会在桌面和移动平台上，于 Avalonia 应用中显示覆盖式通知、toast 消息、状态栏以及系统托盘通知。
doc-type: how-to
---

本指南介绍在 Avalonia 应用中显示通知、toast 消息和状态栏的几种套路。Avalonia 并没有内置的通知控件，你得用 [`ItemsControl`](/api/avalonia/controls/itemscontrol)、`Panel`、`Border` 这些标准布局控件自己搭一个。

## 覆盖式通知面板 {#overlay-notification-panel}

一个常见做法是让通知面板从窗口一角滑进来。你可以用 `ItemsControl` 配合过渡做出这种效果。

### 通知模型 {#notification-model}

```csharp
public partial class NotificationViewModel : ObservableObject
{
    public string Message { get; }
    public string Type { get; } // "info", "success", "error", "warning"

    public NotificationViewModel(string message, string type = "info")
    {
        Message = message;
        Type = type;
    }
}
```

### 通知服务 {#notification-service}

下面这个服务管理着一组活动通知，并负责自动关闭。注意这里必须用 `Dispatcher.UIThread.Post`，因为 `Task.Delay(...).ContinueWith(...)` 之后的代码会在线程池线程上继续执行，而对集合的改动必须调回 UI 线程。

```csharp
public partial class NotificationService : ObservableObject
{
    public ObservableCollection<NotificationViewModel> Notifications { get; } = new();

    public void Show(string message, string type = "info", int durationMs = 3000)
    {
        var notification = new NotificationViewModel(message, type);
        Notifications.Add(notification);

        // Auto-dismiss after the specified duration
        if (durationMs > 0)
        {
            _ = Task.Delay(durationMs).ContinueWith(_ =>
                Dispatcher.UIThread.Post(() => Notifications.Remove(notification)));
        }
    }

    [RelayCommand]
    private void Dismiss(NotificationViewModel notification)
    {
        Notifications.Remove(notification);
    }
}
```

:::tip
若把 `durationMs` 设为 `0`，通知就会一直留在界面上，直到用户主动关闭。这适合那些必须让人确认的错误提示。
:::

### XAML 覆盖层 {#xaml-overlay}

把它放在主窗口根部、作为 `Panel` 的最后一个子元素，这样它就会盖在其他内容之上：

```xml
<Panel>
    <!-- Main content -->
    <ContentControl Content="{Binding CurrentView}" />

    <!-- Notification overlay -->
    <ItemsControl ItemsSource="{Binding Notifications.Notifications}"
                  HorizontalAlignment="Right" VerticalAlignment="Top"
                  Margin="16" MaxWidth="360">
        <ItemsControl.ItemTemplate>
            <DataTemplate>
                <Border Background="#1E1E2E" CornerRadius="8" Padding="12,8"
                        Margin="0,0,0,8" BorderBrush="#333" BorderThickness="1">
                    <Grid ColumnDefinitions="*,Auto">
                        <TextBlock Text="{Binding Message}" TextWrapping="Wrap"
                                   Foreground="White" VerticalAlignment="Center" />
                        <Button Grid.Column="1" Content="x" FontSize="10"
                                Background="Transparent" Foreground="Gray"
                                Padding="4,2" Margin="8,0,0,0"
                                Command="{Binding $parent[ItemsControl].((vm:NotificationService)DataContext).DismissCommand}"
                                CommandParameter="{Binding}" />
                    </Grid>
                </Border>
            </DataTemplate>
        </ItemsControl.ItemTemplate>
    </ItemsControl>
</Panel>
```

:::note
在移动平台（Android 和 iOS）上，不妨把通知放在屏幕顶部，避开虚拟导航按钮。对于有刘海或圆角的设备，请调整 `VerticalAlignment` 和 `Margin` 以照顾安全区域内边距。
:::

### 在视图模型中使用 {#usage-in-a-view-model}

```csharp
public partial class MainViewModel : ObservableObject
{
    public NotificationService Notifications { get; } = new();

    [RelayCommand]
    private async Task SaveAsync()
    {
        await _repository.SaveAsync();
        Notifications.Show("Changes saved successfully.", "success");
    }
}
```

## 简单的状态栏 {#simple-status-bar}

若想要不那么扰人的反馈，可以在窗口底部放一条状态栏：

```xml
<DockPanel>
    <Border DockPanel.Dock="Bottom" Background="#F3F4F6" Padding="8,4">
        <TextBlock Text="{Binding StatusMessage}" FontSize="12" Foreground="Gray" />
    </Border>

    <!-- Main content -->
    <ContentControl Content="{Binding CurrentView}" />
</DockPanel>
```

```csharp
[ObservableProperty]
private string _statusMessage = "Ready";

[RelayCommand]
private async Task LoadDataAsync()
{
    StatusMessage = "Loading...";
    await _dataService.LoadAsync();
    StatusMessage = "Loaded 42 items.";

    // Clear after delay
    await Task.Delay(3000);
    StatusMessage = "Ready";
}
```

:::warning
若用户快速连按多次 `LoadDataAsync`，先前那次调用里的 `Task.Delay` 可能会在新操作还跑着的时候就把状态消息清掉。要避免这一点，请改用 `CancellationTokenSource`，并在每次重入该方法时取消掉上一个。
:::

## 确认横幅 {#confirmation-banner}

重要消息可以用页面顶部的横幅来显示：

```xml
<StackPanel>
    <!-- Banner -->
    <Border Background="#FEF3C7" Padding="12,8"
            IsVisible="{Binding ShowBanner}">
        <Grid ColumnDefinitions="*,Auto">
            <TextBlock Text="{Binding BannerMessage}" Foreground="#92400E"
                       VerticalAlignment="Center" />
            <Button Grid.Column="1" Content="Dismiss"
                    Command="{Binding DismissBannerCommand}"
                    Background="Transparent" Foreground="#92400E" />
        </Grid>
    </Border>

    <!-- Page content -->
    <ContentControl Content="{Binding CurrentPage}" />
</StackPanel>
```

## 托盘图标通知（仅限桌面） {#tray-icon-notifications-desktop-only}

在桌面平台（Windows、macOS、Linux）上，你可以用 `TrayIcon` 控件接入系统托盘：

```xml
<TrayIcon.Icons>
    <TrayIcons>
        <TrayIcon Icon="/Assets/app-icon.ico"
                  ToolTipText="My Application"
                  Command="{Binding ShowWindowCommand}">
            <TrayIcon.Menu>
                <NativeMenu>
                    <NativeMenuItem Header="Show" Command="{Binding ShowWindowCommand}" />
                    <NativeMenuItem Header="Exit" Command="{Binding ExitCommand}" />
                </NativeMenu>
            </TrayIcon.Menu>
        </TrayIcon>
    </TrayIcons>
</TrayIcon.Icons>
```

### 平台注意事项 {#platform-considerations}

| 平台 | 注释支持情况 |
|----------|-------|
| **Windows** | 完整支持托盘图标和气泡通知。图标请用 `.ico` 格式。 |
| **macOS** | 显示在菜单栏中。macOS 的设计规范建议菜单栏图标使用模板图像（单色 PNG）。 |
| **Linux** | 支持程度取决于桌面环境。GNOME、KDE 和 XFCE 一般通过 `libappindicator` 或 `StatusNotifierItem` 协议支持托盘图标。 |
| **Android / iOS / Browser** | 这些平台不支持 `TrayIcon`，请改用应用内的覆盖式通知。 |

## 按类型着色的通知 {#color-coded-notification-types}

你可以用基于样式类的选择器，按通知类型分别设置样式：

```xml
<ItemsControl.ItemTemplate>
    <DataTemplate>
        <Border CornerRadius="8" Padding="12,8" Margin="0,0,0,8"
                Classes.info="{Binding Type, Converter={StaticResource EqualConverter}, ConverterParameter=info}"
                Classes.success="{Binding Type, Converter={StaticResource EqualConverter}, ConverterParameter=success}"
                Classes.error="{Binding Type, Converter={StaticResource EqualConverter}, ConverterParameter=error}">
            <TextBlock Text="{Binding Message}" Foreground="White" />
        </Border>
    </DataTemplate>
</ItemsControl.ItemTemplate>

<ItemsControl.Styles>
    <Style Selector="Border.info">
        <Setter Property="Background" Value="#3B82F6" />
    </Style>
    <Style Selector="Border.success">
        <Setter Property="Background" Value="#22C55E" />
    </Style>
    <Style Selector="Border.error">
        <Setter Property="Background" Value="#EF4444" />
    </Style>
</ItemsControl.Styles>
```

:::tip
不妨在 `info`、`success`、`error` 之外再加一个 `warning` 样式（比如 `#F59E0B`），凑齐四种常见的通知级别。
:::

## 另请参阅 {#see-also}

- [线程](/docs/app-development/threading)：理解如何用 `Dispatcher.UIThread` 把工作调回 UI 线程。
- [TrayIcon](/controls/navigation/trayicon)：桌面平台的系统托盘集成。
- [Flyout](/controls/layout/containers/flyout)：附着在控件上的弹出内容。
- [ToolTip](/controls/feedback/tooltip)：控件的悬停提示。
- [ItemsControl](/docs/how-to/itemscontrol-how-to)：用 `ItemsControl` 处理动态列表。
- [数据模板](/docs/data-templates/introduction-to-data-templates)：自定义通知项的渲染方式。
