---
id: notification
title: WindowNotificationManager
description: 一套 toast 风格的通知弹出系统，在窗口内指定位置显示临时消息。
doc-type: reference
---

[`WindowNotificationManager`](/api/avalonia/controls/notifications/windownotificationmanager) 提供了一套内置的通知弹出系统，会在窗口内指定位置显示 toast 风格的消息。你可以用它告知用户某项操作已完成，或提示警告、错误等事件，同时不阻塞用户与界面其余部分的交互。

## 常用属性 {#useful-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Position` | `NotificationPosition` | 通知出现的位置。可选 `TopLeft`、`TopCenter`、`TopRight`、`BottomLeft`、`BottomCenter`、`BottomRight`，默认 `TopRight`。 |
| `MaxItems` | `int` | 同时可见的通知数量上限，默认 `5`。 |

## 通知对象的属性 {#notification-properties}

内置的 `Notification` 类提供以下属性：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Title` | `string` | 通知的标题文字。 |
| `Message` | `string` | 通知的正文文字。 |
| `Type` | `NotificationType` | 严重级别：`Information`、`Success`、`Warning` 或 `Error`。 |
| `Expiration` | `TimeSpan` | 通知自动消失前的停留时长。设为 `TimeSpan.Zero` 则必须由用户手动关闭。 |

## 准备工作 {#setting-up}

在窗口中注册一个 `WindowNotificationManager`，通常写在代码隐藏里，或者通过视图模型持有的引用来访问：

```csharp
public partial class MainWindow : Window
{
    private WindowNotificationManager _notificationManager;

    public MainWindow()
    {
        InitializeComponent();

        _notificationManager = new WindowNotificationManager(this)
        {
            Position = NotificationPosition.BottomRight,
            MaxItems = 3
        };
    }
}
```

若你偏好标记式写法，也可以在 XAML 中声明 `WindowNotificationManager`：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="MyApp.MainWindow">
    <Panel>
        <WindowNotificationManager x:Name="NotificationManager"
                                   Position="TopRight"
                                   MaxItems="5" />
        <!-- Your other content here -->
    </Panel>
</Window>
```

随后在代码隐藏中取用这个管理器：

```csharp
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        var manager = this.FindControl<WindowNotificationManager>("NotificationManager");
    }
}
```

## 显示通知 {#showing-a-notification}

用一个 `Notification` 对象调用 `Show`：

```csharp
_notificationManager.Show(new Notification(
    "File saved",
    "Your document has been saved successfully.",
    NotificationType.Success,
    TimeSpan.FromSeconds(3)));
```

若省略 `Expiration` 参数，通知会采用默认的停留时长。想让通知一直显示到用户手动关闭，就传入 `TimeSpan.Zero`：

```csharp
_notificationManager.Show(new Notification(
    "Action required",
    "Please review the pending changes before continuing.",
    NotificationType.Warning,
    TimeSpan.Zero));
```

## 通知类型 {#notification-types}

用 `NotificationType` 枚举表达严重级别，内置主题会为每种类型套用不同的配色：

```csharp
// Informational (default blue)
_notificationManager.Show(new Notification("Info", "Operation started.", NotificationType.Information));

// Success (green)
_notificationManager.Show(new Notification("Done", "Upload complete.", NotificationType.Success));

// Warning (yellow/orange)
_notificationManager.Show(new Notification("Warning", "Disk space is low.", NotificationType.Warning));

// Error (red)
_notificationManager.Show(new Notification("Error", "Connection failed.", NotificationType.Error));
```

## 用代码关闭通知 {#closing-notifications-programmatically}

你可以在代码中关掉某一条通知，也可以清空全部通知：

```csharp
var notification = new Notification("Processing", "Working...", NotificationType.Information, TimeSpan.Zero);
_notificationManager.Show(notification);

// Close a specific notification
_notificationManager.Close(notification);

// Clear all active notifications
_notificationManager.CloseAll();
```

当一项耗时操作完成、你想把进度通知换成结果通知时，这招很好使：

```csharp
var progressNotification = new Notification(
    "Uploading",
    "Sending files to the server...",
    NotificationType.Information,
    TimeSpan.Zero);

_notificationManager.Show(progressNotification);

// Later, when the upload finishes:
_notificationManager.Close(progressNotification);
_notificationManager.Show(new Notification(
    "Upload complete",
    "All files have been sent successfully.",
    NotificationType.Success,
    TimeSpan.FromSeconds(3)));
```

## 自定义通知内容 {#custom-notification-content}

实现 `INotification` 即可提供自定义的通知数据：

```csharp
public class CustomNotification : INotification
{
    public string Title { get; set; }
    public string Message { get; set; }
    public NotificationType Type { get; set; }
    public TimeSpan Expiration { get; set; }
    public string ActionText { get; set; }
    public Action OnAction { get; set; }

    public Action? OnClose { get; set; }
    public Action? OnClick { get; set; }
}
```

自定义通知的显示方式和前面完全一样：

```csharp
_notificationManager.Show(new CustomNotification
{
    Title = "New message",
    Message = "You have a new message from support.",
    Type = NotificationType.Information,
    Expiration = TimeSpan.FromSeconds(5),
    ActionText = "View",
    OnAction = () => NavigateToMessages()
});
```

## Positioning

设置 `Position` 来控制通知出现的位置：

```csharp
// Top-right corner (default)
_notificationManager.Position = NotificationPosition.TopRight;

// Bottom-center (useful for mobile-style toasts)
_notificationManager.Position = NotificationPosition.BottomCenter;
```

可选的六个位置是：

| 位置 | 说明 |
|---|---|
| `TopLeft` | 窗口左上角。 |
| `TopCenter` | 顶边，水平居中。 |
| `TopRight` | 窗口右上角（默认）。 |
| `BottomLeft` | 窗口左下角。 |
| `BottomCenter` | 底边，水平居中。 |
| `BottomRight` | 窗口右下角。 |

## MVVM 写法 {#mvvm-pattern}

把通知管理器包装成一个服务对外暴露，视图模型就能在不直接引用界面类型的前提下弹出通知：

```csharp
public interface INotificationService
{
    void ShowInfo(string title, string message);
    void ShowSuccess(string title, string message);
    void ShowWarning(string title, string message);
    void ShowError(string title, string message);
}

public class NotificationService : INotificationService
{
    private readonly WindowNotificationManager _manager;

    public NotificationService(WindowNotificationManager manager)
    {
        _manager = manager;
    }

    public void ShowInfo(string title, string message) =>
        _manager.Show(new Notification(title, message, NotificationType.Information));

    public void ShowSuccess(string title, string message) =>
        _manager.Show(new Notification(title, message, NotificationType.Success));

    public void ShowWarning(string title, string message) =>
        _manager.Show(new Notification(title, message, NotificationType.Warning));

    public void ShowError(string title, string message) =>
        _manager.Show(new Notification(title, message, NotificationType.Error));
}
```

在应用启动时注册该服务，再把它注入到需要显示通知的视图模型中：

```csharp
public class MyViewModel
{
    private readonly INotificationService _notifications;

    public MyViewModel(INotificationService notifications)
    {
        _notifications = notifications;
    }

    public void SaveDocument()
    {
        // Perform save logic...
        _notifications.ShowSuccess("Saved", "Your document has been saved.");
    }
}
```

## 另请参阅 {#see-also}

- [如何显示通知与 toast](/docs/how-to/notifications-how-to)
- [Popup](/controls/feedback/popup)
- [ToolTip](/controls/feedback/tooltip)
