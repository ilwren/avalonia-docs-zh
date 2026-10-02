---
id: input-events
title: 输入事件
description: 在 Avalonia 控件中处理指针、键盘和手势输入事件。
doc-type: reference
---

Avalonia 提供了一整套输入事件，用于处理指针（鼠标/触摸/手写笔）、键盘和手势交互。大多数输入事件采用 `Tunnel | Bubble` 组合路由策略，让父元素有机会在输入抵达目标之前先行拦截。

## 指针事件 {#pointer-events}

指针事件把鼠标、触摸和手写笔输入抽象成统一的模型，默认沿视觉树向上冒泡。

| 事件 | 触发时机 |
|---|---|
| `PointerEntered` | 指针进入控件范围。 |
| `PointerExited` | 指针离开控件范围。 |
| `PointerMoved` | 指针在控件内移动。 |
| `PointerPressed` | 在控件上按下指针按键。 |
| `PointerReleased` | 在控件上松开指针按键。 |
| `PointerCaptureLost` | 控件失去指针捕获。 |
| `PointerWheelChanged` | 鼠标滚轮或触控板在控件上滚动。 |

### 处理指针事件 {#handling-pointer-events}

```csharp
protected override void OnPointerPressed(PointerPressedEventArgs e)
{
    base.OnPointerPressed(e);

    var point = e.GetPosition(this); // Position relative to this control
    var properties = e.GetCurrentPoint(this).Properties;

    if (properties.IsLeftButtonPressed)
    {
        // Left button pressed at (point.X, point.Y)
    }
}
```

### `PointerEventArgs` 上的关键属性 {#key-properties-on-pointereventargs}

| Property / Method | 说明 |
|---|---|
| `GetPosition(Visual)` | 返回指针相对于指定视觉元素的位置。 |
| `GetCurrentPoint(Visual)` | 返回一个 `PointerPoint`，其中包含位置和按键状态。 |
| `Pointer` | `Pointer` 实例，做捕获操作时会用到。 |
| `KeyModifiers` | Shift、Control、Alt 或 Meta 键是否处于按下状态。 |

### 指针捕获 {#pointer-capture}

捕获指针之后，后续所有指针事件都会被定向到发起捕获的那个控件，直到捕获被释放：

```csharp
protected override void OnPointerPressed(PointerPressedEventArgs e)
{
    base.OnPointerPressed(e);
    e.Pointer.Capture(this); // Start capturing
}

protected override void OnPointerReleased(PointerReleasedEventArgs e)
{
    base.OnPointerReleased(e);
    e.Pointer.Capture(null); // Release capture
}
```

整个应用在同一时刻只能有一个元素持有指针捕获。这与操作系统的行为一致 —— 一个物理鼠标设备只能对应一个被捕获的元素。当另一个控件（比如弹出窗口中的控件）捕获指针时，先前的捕获即被释放，原控件会收到一个 `PointerCaptureLost` 事件。

## 键盘事件 {#keyboard-events}

键盘事件在当前获得焦点的元素上触发，并沿树向上冒泡。

| 事件 | 触发时机 |
|---|---|
| `KeyDown` | 按下某个键。 |
| `KeyUp` | 松开某个键。 |
| `TextInput` | 收到字符输入（经过输入法处理之后）。 |

### 处理键盘事件 {#handling-keyboard-events}

```csharp
protected override void OnKeyDown(KeyEventArgs e)
{
    base.OnKeyDown(e);

    if (e.Key == Key.Enter)
    {
        // Handle Enter key
        e.Handled = true;
    }

    if (e.Key == Key.C && e.KeyModifiers.HasFlag(KeyModifiers.Control))
    {
        // Handle Ctrl+C
        e.Handled = true;
    }
}
```

### `KeyEventArgs` 上的关键属性 {#key-properties-on-keyeventargs}

| 属性 | 说明 |
|---|---|
| `Key` | 被按下的物理按键（取自 `Key` 枚举）。 |
| `KeyModifiers` | 处于按下状态的修饰键（Control、Shift、Alt、Meta）。 |
| `KeySymbol` | 该次按键产生的字符（若有）。 |

## 隧道（预览）事件 {#tunneling-preview-events}

对于采用 `Tunnel | Bubble` 路由的输入事件，隧道阶段先行发生。你可以通过路由策略参数，在隧道阶段拦截事件：

```csharp
myControl.AddHandler(InputElement.PointerPressedEvent, OnPreviewPointerPressed,
    RoutingStrategies.Tunnel);
```

```csharp
private void OnPreviewPointerPressed(object? sender, PointerPressedEventArgs e)
{
    // This fires before the bubble phase
    // Set e.Handled = true to prevent the event from reaching child elements
}
```

当你想在子控件处理输入之前先在父级拦下它时，这招很好用。

## 手势事件 {#gesture-events}

Avalonia 在原始指针事件之上提供了一组高层手势事件：

| 事件 | 触发时机 |
|---|---|
| `Tapped` | 完成一次快速点按/单击手势。 |
| `DoubleTapped` | 完成一次双击手势。 |
| `Holding` | 检测到长按手势（触摸）。 |

手势事件沿树向上冒泡。更复杂的手势（捏合、下拉、滚动）请见[手势](/docs/input-interaction/gestures)。

```xml
<Border Tapped="OnBorderTapped" Background="LightGray">
    <TextBlock Text="Tap me" />
</Border>
```

```csharp
private void OnBorderTapped(object? sender, TappedEventArgs e)
{
    // Respond to the tap
}
```

## 常见的输入处理套路 {#common-input-patterns}

### 检测拖拽 {#drag-detection}

```csharp
private Point _pressPoint;
private bool _isDragging;

protected override void OnPointerPressed(PointerPressedEventArgs e)
{
    base.OnPointerPressed(e);
    _pressPoint = e.GetPosition(this);
    _isDragging = false;
    e.Pointer.Capture(this);
}

protected override void OnPointerMoved(PointerEventArgs e)
{
    base.OnPointerMoved(e);

    if (e.GetCurrentPoint(this).Properties.IsLeftButtonPressed)
    {
        var currentPoint = e.GetPosition(this);
        var delta = currentPoint - _pressPoint;

        if (!_isDragging && (Math.Abs(delta.X) > 3 || Math.Abs(delta.Y) > 3))
        {
            _isDragging = true;
        }

        if (_isDragging)
        {
            // Handle drag
        }
    }
}

protected override void OnPointerReleased(PointerReleasedEventArgs e)
{
    base.OnPointerReleased(e);
    _isDragging = false;
    e.Pointer.Capture(null);
}
```

### 窗口级的键盘快捷键 {#keyboard-shortcuts-on-a-window}

```csharp
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    protected override void OnKeyDown(KeyEventArgs e)
    {
        base.OnKeyDown(e);

        if (e.Key == Key.S && e.KeyModifiers.HasFlag(KeyModifiers.Control))
        {
            SaveDocument();
            e.Handled = true;
        }
    }
}
```

:::tip
若只是声明式的键盘快捷键，不妨改用 [KeyBindings 与 HotKeys](/docs/input-interaction/keyboard-and-hotkeys)，不必手动处理 `KeyDown`。
:::

## 另请参阅 {#see-also}

- [事件总览](/docs/events)：Avalonia 中路由事件的工作方式。
- [指针输入](/docs/input-interaction/pointer)：指针输入的详细参考。
- [键盘与快捷键](/docs/input-interaction/keyboard-and-hotkeys)：键盘快捷键与按键绑定。
- [手势](/docs/input-interaction/gestures)：触摸与多指手势识别。
- [焦点](/docs/input-interaction/focus)：键盘焦点的工作方式。
