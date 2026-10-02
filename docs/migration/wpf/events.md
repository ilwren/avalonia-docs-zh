---
id: events
title: 事件
description: WPF 与 Avalonia 在路由事件、隧道机制和事件命名上的差异。
doc-type: migration
---

Avalonia 的事件系统在概念上与 WPF 的路由事件模型相仿：事件既能沿视觉树向上冒泡，也能向下隧道；你既可以注册类处理程序，也可以注册实例处理程序。不过在 API 形态、事件命名以及隧道的处理方式上，二者有几处要紧的区别。本指南讲的就是从 WPF 迁到 Avalonia 时你该知道的那些关键差异。

## 路由事件 {#routed-events}

WPF 和 Avalonia 都支持路由事件，但注册 API 不同：WPF 用 `EventManager.RegisterRoutedEvent`，Avalonia 用 `RoutedEvent.Register`。

```csharp title='WPF'
public static readonly RoutedEvent TapEvent = EventManager.RegisterRoutedEvent(
    "Tap",
    RoutingStrategy.Bubble,
    typeof(RoutedEventHandler),
    typeof(MyControl));
```

```csharp title='Avalonia'
public static readonly RoutedEvent<RoutedEventArgs> TapEvent = RoutedEvent.Register<MyControl, RoutedEventArgs>(
    "Tap",
    RoutingStrategy.Bubble);
```

需要留意的关键差异：

- Avalonia 用的是泛型 `RoutedEvent<TEventArgs>` 类型，事件参数的类型约束更强。
- Avalonia 的注册调用对所有者类型和事件参数类型都使用泛型类型参数，而不是传 `typeof()` 实参。
- 在 Avalonia 中，委托类型由泛型类型参数推断得出，你不必显式指明。

## 类处理程序 {#class-handlers}

在 WPF 中，调用 [EventManager.RegisterClassHandler](https://msdn.microsoft.com/en-us/library/ms597875.aspx) 即可为事件添加类处理程序；在 Avalonia 中，则直接在路由事件实例上调用 `AddClassHandler`。

```csharp title='WPF'
static MyControl()
{
    EventManager.RegisterClassHandler(typeof(MyControl), MyEvent, HandleMyEvent));
}

private static void HandleMyEvent(object sender, RoutedEventArgs e)
{
}
```

```csharp title='Avalonia'
static MyControl()
{
    MyEvent.AddClassHandler<MyControl>((x, e) => x.HandleMyEvent(e));
}

private void HandleMyEvent(RoutedEventArgs e)
{
}
```

注意在 WPF 中类处理程序必须是静态方法，而在 Avalonia 中它不是静态的——通知会自动送到正确的实例上。事件处理程序里惯有的 `sender` 参数在这里也就不必要了，而且一切都保持强类型。

## 隧道事件 {#tunnelling-events}

在 WPF 中，隧道（预览）事件是带 `Preview` 前缀的独立 CLR 事件。比如 `PreviewKeyDown` 就是 `KeyDown` 的隧道版本。它们是两个各自独立、可分别订阅的 CLR 事件。

Avalonia 的路子不同。这里没有单独的 `Preview*` CLR 事件，隧道与冒泡共用同一个 `RoutedEvent` 实例。要订阅隧道阶段，请调用 `AddHandler` 并传入 `RoutingStrategies.Tunnel`。

```csharp title='WPF'
// In WPF, subscribe to the Preview event directly
myControl.PreviewKeyDown += OnPreviewKeyDown;

void OnPreviewKeyDown(object sender, KeyEventArgs e)
{
    // Tunnelling handler
}
```

```csharp title='Avalonia'
// In Avalonia, use AddHandler with RoutingStrategies.Tunnel
myControl.AddHandler(InputElement.KeyDownEvent, OnPreviewKeyDown, RoutingStrategies.Tunnel);

void OnPreviewKeyDown(object? sender, KeyEventArgs e)
{
    // Tunnelling handler
}
```

把这些标志组合起来，还能同时订阅隧道和冒泡两个阶段：

```csharp title='Avalonia'
myControl.AddHandler(
    InputElement.KeyDownEvent,
    OnKeyDown,
    RoutingStrategies.Tunnel | RoutingStrategies.Bubble);
```

## 挂载事件处理程序 {#event-handler-attachment}

### XAML 中的事件处理程序 {#xaml-event-handlers}

在 XAML 中挂事件处理程序，WPF 和 Avalonia 的做法完全相同：

```xml
<Button Click="OnButtonClick" />
```

### 在代码隐藏中使用 AddHandler {#code-behind-with-addhandler}

WPF 的 `AddHandler` 接收路由事件和一个委托；Avalonia 的 `AddHandler` 则还多收几个参数，用于指定路由策略和「已处理事件」的行为。

```csharp title='WPF'
myButton.AddHandler(Button.ClickEvent, new RoutedEventHandler(OnButtonClick));
```

```csharp title='Avalonia'
myButton.AddHandler(Button.ClickEvent, OnButtonClick);
```

### handledEventsToo 参数 {#the-handledeventstoo-parameter}

WPF 和 Avalonia 都支持在事件被标记为已处理之后仍然收到它，这个参数在两个框架中的用法相仿。

```csharp title='WPF'
myControl.AddHandler(
    UIElement.MouseDownEvent,
    new MouseButtonEventHandler(OnMouseDown),
    handledEventsToo: true);
```

```csharp title='Avalonia'
myControl.AddHandler(
    InputElement.PointerPressedEvent,
    OnPointerPressed,
    RoutingStrategies.Bubble,
    handledEventsToo: true);
```

注意在 Avalonia 中，`RoutingStrategies` 参数必须写在 `handledEventsToo` 之前。

## 常见的事件名差异 {#common-event-name-differences}

许多输入事件在 Avalonia 中的名字与 WPF 不同。下表列出最常见的对应关系：

| WPF Event | Avalonia Equivalent | 注释支持情况 |
|---|---|---|
| `MouseLeftButtonDown` | `PointerPressed` | 查看 [`PointerUpdateKind`](/api/avalonia/input/pointerupdatekind) 判断是哪个按键 |
| `MouseLeftButtonUp` | `PointerReleased` | 查看 `PointerUpdateKind` 判断是哪个按键 |
| `MouseRightButtonDown` | `PointerPressed` | 查看 `PointerUpdateKind` 判断是哪个按键 |
| `MouseRightButtonUp` | `PointerReleased` | 查看 `PointerUpdateKind` 判断是哪个按键 |
| `MouseMove` | `PointerMoved` | |
| `MouseEnter` | `PointerEntered` | |
| `MouseLeave` | `PointerExited` | |
| `MouseWheel` | `PointerWheelChanged` | |
| `PreviewKeyDown` | 在 `KeyDownEvent` 上用 `AddHandler` 配 `RoutingStrategies.Tunnel` | 没有单独的 Preview 事件 |
| `PreviewKeyUp` | 在 `KeyUpEvent` 上用 `AddHandler` 配 `RoutingStrategies.Tunnel` | 没有单独的 Preview 事件 |
| `PreviewMouseDown` | 在 `PointerPressedEvent` 上用 `AddHandler` 配 `RoutingStrategies.Tunnel` | 没有单独的 Preview 事件 |

Avalonia 采用以 pointer 为名的事件，因为它支持的输入设备不止鼠标，还包括触摸和触控笔。

## 自定义路由事件 {#custom-routed-events}

定义自定义路由事件时，WPF 和 Avalonia 的注册写法有所不同。下面完整对比了如何定义、注册并引发一个自定义路由事件。

```csharp title='WPF'
public class MyControl : Control
{
    public static readonly RoutedEvent TapEvent = EventManager.RegisterRoutedEvent(
        "Tap",
        RoutingStrategy.Bubble,
        typeof(RoutedEventHandler),
        typeof(MyControl));

    public event RoutedEventHandler Tap
    {
        add => AddHandler(TapEvent, value);
        remove => RemoveHandler(TapEvent, value);
    }

    protected void OnTap()
    {
        RaiseEvent(new RoutedEventArgs(TapEvent));
    }
}
```

```csharp title='Avalonia'
public class MyControl : Control
{
    public static readonly RoutedEvent<RoutedEventArgs> TapEvent = RoutedEvent.Register<MyControl, RoutedEventArgs>(
        "Tap",
        RoutingStrategy.Bubble);

    public event EventHandler<RoutedEventArgs>? Tap
    {
        add => AddHandler(TapEvent, value);
        remove => RemoveHandler(TapEvent, value);
    }

    protected void OnTap()
    {
        RaiseEvent(new RoutedEventArgs(TapEvent));
    }
}
```

主要差异有：

- Avalonia 用泛型 `RoutedEvent<T>` 来保证类型安全。
- Avalonia 中的 CLR 事件包装器用的是 `EventHandler<RoutedEventArgs>`，而不是 `RoutedEventHandler`。
- 注册时用的是泛型类型参数，而不是 `typeof()` 实参。

## 另请参阅 {#see-also}

- [Routed Events Overview](/docs/events)
- [Input Events](/docs/events/input-events)
- [Routed Events Deep Dive](/docs/input-interaction/routed-events)
