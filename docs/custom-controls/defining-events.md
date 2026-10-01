---
id: defining-events
title: 为自定义控件定义事件
sidebar_label: 定义事件
description: 在 Avalonia 自定义控件上定义并触发路由事件。
doc-type: how-to
---

Avalonia 采用路由事件机制：事件在控件树中传播，使得多个控件都有机会响应同一个事件。路由策略有好几种，最常见的是隧道（事件自根部沿控件树向下传播）和冒泡（事件自源头沿控件树向上传播）。

本文讲的是如何为你的控件定义自定义事件。

关于路由事件的更多内容，请参阅[事件概述](/docs/events)。

## 自定义路由事件 {#custom-routed-events}

下面是一个自定义滑块控件的路由事件示例：为控件 `MyCustomSlider` 定义一个名为 `ValueChangedEvent` 的自定义事件。该事件通过 `RoutedEvent` 系统注册，供控件使用者订阅。为方便起见还定义了一个 CLR 事件，这样标准 .NET API 也能用上它。

```csharp
public class MyCustomSlider : Control
{
    public static readonly RoutedEvent<RoutedEventArgs> ValueChangedEvent =
        RoutedEvent.Register<MyCustomSlider, RoutedEventArgs>(nameof(ValueChanged), RoutingStrategies.Direct);

    public event EventHandler<RoutedEventArgs> ValueChanged
    {
        add => AddHandler(ValueChangedEvent, value);
        remove => RemoveHandler(ValueChangedEvent, value);
    }

    protected virtual void OnValueChanged()
    {
        RoutedEventArgs args = new RoutedEventArgs(ValueChangedEvent);
        RaiseEvent(args);
    }
}
```

## 自定义事件参数 {#custom-event-arguments}

如果你的事件需要携带额外数据，可以定制它所接受的参数类型。

接着上一节 `MyCustomSlider` 的 `ValueChangedEvent` 这个例子往下讲：

1. 先创建一个继承自 `RoutedEventArgs` 的自定义类。

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

2. 把事件注册改成使用这个自定义参数类型。

    ```csharp
    public static readonly RoutedEvent<ValueChangedEventArgs> ValueChangedEvent =
        RoutedEvent.Register<MyCustomSlider, ValueChangedEventArgs>(
            nameof(ValueChanged), RoutingStrategies.Bubble);
    ```

3. 同步更新 CLR 事件包装器和触发方法。

    ```csharp
    public event EventHandler<ValueChangedEventArgs> ValueChanged
    {
        add => AddHandler(ValueChangedEvent, value);
        remove => RemoveHandler(ValueChangedEvent, value);
    }

    protected virtual void OnValueChanged(double oldValue, double newValue)
    {
        var args = new ValueChangedEventArgs(ValueChangedEvent, oldValue, newValue);
        RaiseEvent(args);
    }
    ```

## 在 XAML 中处理事件 {#handling-events-in-xaml}

你这个自定义控件的使用者可以直接在 XAML 中订阅该事件，处理程序写在代码隐藏里。

<Tabs>

<TabItem value="xaml" label="XAML">

```xml
<local:MyCustomSlider ValueChanged="OnSliderValueChanged" />
```

</TabItem>

<TabItem value="csharp" label="C#">

```csharp
private void OnSliderValueChanged(object? sender, ValueChangedEventArgs e)
{
    Debug.WriteLine($"Value changed from {e.OldValue} to {e.NewValue}");
}
```

</TabItem>

</Tabs>

## 类处理程序 {#class-handlers}

类处理程序把事件处理逻辑注册在类这一层，而不是逐个实例注册，通常写在静态构造函数中。它们先于实例处理程序被调用，因此会自动作用于该类型的每一个实例。

类处理程序适用于这样一类控件实现：需要在任何实例级处理程序把输入事件标记为已处理之前就先行拦截。一个常见用途，是定义应当作用于该控件所有实例的默认行为。

```csharp
static MyCustomSlider()
{
    ValueChangedEvent.AddClassHandler<MyCustomSlider>((s, e) => s.OnValueChanged(e));
}

private void OnValueChanged(ValueChangedEventArgs e)
{
    // Handle value change for all instances of MyCustomSlider
}
```

## 另请参阅 {#see-also}

- [路由事件](/docs/input-interaction/routed-events)：路由事件的完整参考。
- [事件概述](/docs/events)：路由事件如何在控件树中传播。
- [输入事件](/docs/events/input-events)：内置的输入事件。
- [定义属性](/docs/custom-controls/defining-properties)：给自定义控件添加样式化属性、直接属性和附加属性。
- [创建自定义控件](/docs/custom-controls)：可以挂事件的各类自定义控件概览。
