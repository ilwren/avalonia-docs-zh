---
id: index
title: 事件总览
description: 理解路由事件在 Avalonia 元素树中的传播方式。
doc-type: overview
---

Avalonia 采用了一套类似 WPF 的路由事件系统。路由事件会在[控件树](/docs/fundamentals/visual-and-logical-trees)中传播（也就是「路由」），父元素因此能够处理子元素引发的事件。Avalonia 的输入、交互和控件行为都建立在这个机制之上。借助路由事件，多个控件可以响应同一个事件，事件处理逻辑也可以集中到视觉树上层某个公共位置。

## 主要特性 {#key-features}

- **事件路由：** 路由事件既可以沿树向上传播（冒泡），也可以沿树向下传播（隧道），于是不同层级的控件都有机会处理同一个事件。这让事件处理更灵活，也更容易集中管理。

- **事件处理程序：** 路由事件靠事件处理程序来响应。处理程序既可以挂在特定控件上，也可以挂在视觉树的上层，统一处理来自多个控件的事件。

- **已处理标记：** 路由事件带有 `Handled` 属性，可以把事件标记为已处理，从而阻止它继续传播。这让你能对事件处理做精细的控制。

- **路由策略：** Avalonia 为路由事件支持多种路由策略，如冒泡、隧道和直接路由。策略决定了各控件接收并处理事件的先后顺序。

## 事件路由策略 {#event-routing-strategies}

每个路由事件都有一种路由策略，决定它如何在元素树中传播：

| 策略 | 方向 | 说明 |
|---|---|---|
| `Bubble` | 由子到父 | 事件先在源元素上触发，然后逐级向上穿过各个父级，直到抵达根。这是最常用的策略。 |
| `Tunnel` | 由父到子 | 事件先在根元素上触发，再沿树向下传到源元素。隧道事件通常用于预览/拦截场景。 |
| `Direct` | 仅源元素 | 事件只在源元素上触发，不在树中传播。 |

多种策略可以组合。比如很多输入事件采用 `Tunnel | Bubble`：事件先从根向下隧道传播，再从源元素向上冒泡回去。

```csharp
RoutedEvent.Register<MyControl, RoutedEventArgs>(
    nameof(MyEvent), RoutingStrategies.Tunnel | RoutingStrategies.Bubble);
```

### 冒泡示例 {#bubble-example}

当用户点击 `Window` 里 `StackPanel` 中的一个 `Button` 时：

```text
Window          ← event arrives here last (bubble)
  └─ StackPanel ← event arrives here second
       └─ Button ← event starts here (source)
```

### 隧道示例 {#tunnel-example}

同一棵树上的隧道事件：

```text
Window          ← event starts here first (tunnel)
  └─ StackPanel ← event arrives here second
       └─ Button ← event arrives here last (source)
```

## 处理路由事件 {#handling-routed-events}

### 在 XAML 中 {#in-xaml}

把事件名当作特性来挂接事件处理程序：

```xml
<Button Click="OnButtonClick" Content="Click me" />
```

```csharp
private void OnButtonClick(object? sender, RoutedEventArgs e)
{
    // sender is the Button that was clicked
    // e.Source is the original source of the event
}
```

### 在代码中 {#in-code}

使用 `AddHandler` 和 `RemoveHandler`：

```csharp
myButton.AddHandler(Button.ClickEvent, OnButtonClick);

// Later, to unsubscribe:
myButton.RemoveHandler(Button.ClickEvent, OnButtonClick);
```

### 在父元素上处理冒泡事件 {#handling-bubbled-events-on-a-parent}

由于事件会沿树向上冒泡，你可以在父元素上处理子元素的事件：

```xml
<StackPanel Tapped="OnStackPanelTapped">
    <Button Content="Button 1" />
    <Button Content="Button 2" />
    <Button Content="Button 3" />
</StackPanel>
```

```csharp
private void OnStackPanelTapped(object? sender, TappedEventArgs e)
{
    // sender is the StackPanel (where the handler is attached)
    // e.Source is the specific Button that was tapped
    if (e.Source is Button button)
    {
        Debug.WriteLine($"Tapped: {button.Content}");
    }
}
```

## 把事件标记为已处理 {#marking-events-as-handled}

设置 `e.Handled = true` 可以让事件停止继续路由：

```csharp
private void OnButtonClick(object? sender, RoutedEventArgs e)
{
    e.Handled = true; // Prevents parent handlers from receiving this event
}
```

若你希望连已被标记为已处理的事件也能收到，请使用 `handledEventsToo` 参数：

```csharp
myPanel.AddHandler(Button.ClickEvent, OnButtonClick, RoutingStrategies.Bubble, handledEventsToo: true);
```

## `RoutedEventArgs` 的属性 {#routedeventargs-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Source` | `object?` | 最初引发该事件的元素。 |
| `Handled` | `bool` | 该事件是否已被处理。设为 `true` 即可终止路由。 |
| `Route` | `RoutingStrategies` | 当前的路由阶段（`Tunnel`、`Bubble` 或 `Direct`）。 |
| `RoutedEvent` | `RoutedEvent` | 正在引发的那个路由事件。 |

## 注册自定义路由事件 {#registering-custom-routed-events}

在你的控件中定义一个自定义路由事件：

```csharp
public class MyControl : Control
{
    public static readonly RoutedEvent<RoutedEventArgs> ValueChangedEvent =
        RoutedEvent.Register<MyControl, RoutedEventArgs>(
            nameof(ValueChanged),
            RoutingStrategies.Bubble);

    public event EventHandler<RoutedEventArgs>? ValueChanged
    {
        add => AddHandler(ValueChangedEvent, value);
        remove => RemoveHandler(ValueChangedEvent, value);
    }

    protected virtual void OnValueChanged()
    {
        RaiseEvent(new RoutedEventArgs(ValueChangedEvent));
    }
}
```

### 自定义事件参数 {#custom-event-args}

若事件需要携带额外数据，请创建一个 `RoutedEventArgs` 的子类：

```csharp
public class ValueChangedEventArgs : RoutedEventArgs
{
    public ValueChangedEventArgs(RoutedEvent routedEvent, double oldValue, double newValue)
        : base(routedEvent)
    {
        OldValue = oldValue;
        NewValue = newValue;
    }

    public double OldValue { get; }
    public double NewValue { get; }
}
```

## 类处理程序 {#class-handlers}

类处理程序让你能统一响应某个类型所有实例上的事件 —— 它们先于实例处理程序运行，通常在静态构造函数中注册。

类处理程序常用来为自定义控件定义默认的事件响应。更多内容请见[为自定义控件定义事件](/docs/custom-controls/defining-events)。

## 下一步 {#next-steps}

- [路由事件](/docs/input-interaction/routed-events)：路由事件系统的详细参考。
- [生命周期事件](/docs/events/lifecycle-events)：控件创建、加载与销毁期间触发的事件。
- [输入事件](/docs/events/input-events)：指针、键盘与手势事件。
- [添加交互](/docs/input-interaction/adding-interactivity)：处理用户交互的实用指南。
