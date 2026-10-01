---
id: pointer
title: 指针设备
---

import PointerPressedSampleScreenshot from '/img/concepts/ui-concepts/user-input/pointer-pressed.gif';

Avalonia 基于一层名为「指针设备」的抽象来工作。它可以代表鼠标、触控板、触控笔等各类设备，且不限于此。

检测并响应用户输入，是控件最常干的活儿。Avalonia 的输入系统同时借助[直接事件与路由事件](/docs/input-interaction/routed-events)来支撑文本输入、焦点管理和鼠标定位。

应用的输入需求往往很复杂。为此 Avalonia 提供了一套[命令机制](/docs/input-interaction/adding-interactivity)，把用户的输入动作与响应这些动作的代码分开。

实现了 `ICommandSource` 的控件都有一个 `HotKey` 属性。此外，控件还提供了若干事件，让你能订阅指针的移动、点击和滚轮操作：

| 事件 | 说明 |
|---|---|
| `PointerEntered` | 指针移入控件边界时引发。 |
| `PointerExited` | 指针离开控件边界时引发。 |
| `PointerMoved` | 指针在控件边界内移动时引发。 |
| `PointerPressed` | 指针按键在控件上被按下时引发。 |
| `PointerReleased` | 先前按下的指针按键在控件上松开时引发。 |
| `PointerWheelChanged` | 在控件上使用鼠标滚轮或触控板滚动时引发。 |
| `Tapped` | 指针在控件上按下又松开之后引发。 |
| `DoubleTapped` | 在平台规定的双击阈值内、于同一位置轻点两次后引发。 |
| `Holding` | 指针按下并保持住 `PlatformSettings.HoldWaitDuration` 所定的时长后引发。 |

举个例子，你可以像这样订阅「指针某个按键在控件上被按下」的事件：

```csharp title='C#'
private void PointerPressedHandler (object sender, PointerPressedEventArgs args)
{
    var point = args.GetCurrentPoint(sender as Control);
    var x = point.Position.X;
    var y = point.Position.Y;
    var msg = $"Pointer press at {x}, {y} relative to sender.";
    if (point.Properties.IsLeftButtonPressed)
    {
        msg += " Left button pressed.";
    }
    if (point.Properties.IsRightButtonPressed)
    {
        msg += " Right button pressed.";
    }
    results.Text = msg ;
}
```

```xml title='XAML'
<StackPanel Margin="20" Background="AliceBlue" 
            PointerPressed="PointerPressedHandler" >
  <TextBlock x:Name="results" Margin="5">Ready...</TextBlock>
</StackPanel>
```

<Image light={PointerPressedSampleScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 指针类型 {#pointer-types}

Avalonia 通过 `PointerPoint.Pointer.Type` 属性区分不同类型的输入设备：

| 类型 | 说明 |
|---|---|
| `Mouse` | 标准的鼠标或触控板输入。 |
| `Touch` | 触摸屏输入。 |
| `Pen` | 触控笔输入（数位板、主动式触控笔）。 |

### 触控笔相关属性 {#pen-and-stylus-properties}

当指针类型为 `Pen` 时，`PointerPointProperties` 上还会多出一些属性：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Pressure` | `float` | 压力级别，从 0（无压力）到 1（最大压力）。 |
| `XTilt` | `float` | 笔沿 X 轴的倾斜角。 |
| `YTilt` | `float` | 笔沿 Y 轴的倾斜角。 |
| `Twist` | `float` | 笔绕自身轴线的顺时针旋转角度。 |
| `IsEraser` | `bool` | 笔的橡皮端处于激活状态时为 `true`。 |
| `IsBarrelButtonPressed` | `bool` | 笔身按钮被按住时为 `true`。 |

```csharp
private void OnPointerMoved(object? sender, PointerEventArgs e)
{
    var point = e.GetCurrentPoint(this);

    if (point.Pointer.Type == PointerType.Pen)
    {
        var pressure = point.Properties.Pressure;
        var isEraser = point.Properties.IsEraser;
        // Adjust brush size or tool based on pressure and eraser state
    }
}
```

凡是支持触控笔输入的平台（Windows、macOS，以及使用 X11 的 Linux）都提供这些属性。

## 指针位置 {#pointer-position}

在上面的例子中，指针坐标（`x` 和 `y`）是相对发送方控件原点（左上角）计算的，这里就是那个 stack panel。若你想要相对所在窗口的坐标，可以这样用 `GetCurrentPoint` 方法：

```csharp
var point = args.GetCurrentPoint(this);
```

## 轻点类事件 {#tap-events}

控件还有几个特殊的手势事件：`Tapped`、`DoubleTapped` 和 `Holding`。指针在控件上按下再松开后，就会引发 tapped 事件；在同一位置按下两次，则引发 double tapped。 

指针按住一段设定时长后会引发 holding。按住时长由 `TopLevel` PlatformSettings 中的 `HoldWaitDuration` 属性定义。在控件上设置 `InputElement.IsHoldingEnabled` 附加属性即可启用按住手势。时长一到，控件的 `HoldingEvent` 就会引发，参数的 `HoldingState` 为 `HoldingState.Started`；指针松开时再次引发，此时状态为 `HoldingState.Completed`。若 `Holding` 已经开始、期间又发起了新手势或按下了第二个指针，则 `Holding` 手势被取消，并引发一次状态为 `HoldingState.Canceled` 的 `HoldingEvent`。在控件上设置 `InputElement.IsHoldWithMouseEnabled` 附加属性后，鼠标指针也能发起按住手势。

:::info
注意，第一次与第二次轻点之间允许的最大距离和时间间隔因目标平台而异，触摸设备上通常更宽松。
:::


## 指针捕获 {#pointer-capture}

指针捕获会把后续所有指针事件都送给指定的控件，哪怕指针已经移出该控件的边界。这对拖动操作和滑块类交互来说必不可少。

```csharp
protected override void OnPointerPressed(PointerPressedEventArgs e)
{
    base.OnPointerPressed(e);
    e.Pointer.Capture(this);
}

protected override void OnPointerReleased(PointerReleasedEventArgs e)
{
    base.OnPointerReleased(e);
    e.Pointer.Capture(null); // Release capture
}
```

整个应用中同一时刻只能有一个元素持有指针捕获。若另一个控件捕获了指针，先前那个控件的捕获就会被解除，并收到一个 `PointerCaptureLost` 事件。请处理这个事件，把进行到一半的交互收拾干净：

```csharp
protected override void OnPointerCaptureLost(PointerCaptureLostEventArgs e)
{
    base.OnPointerCaptureLost(e);
    _isDragging = false;
}
```

## 光标管理 {#cursor-management}

### 为控件设置光标 {#setting-the-cursor-on-a-control}

用 `Cursor` 属性改变指针悬停在控件上时的光标：

```xml
<Border Cursor="Hand" Background="LightGray" Padding="20">
    <TextBlock Text="Click me" />
</Border>

<Border Cursor="SizeWestEast" Background="LightBlue" Padding="20">
    <TextBlock Text="Resize horizontally" />
</Border>
```

### 常见的光标类型 {#common-cursor-types}

| 光标 | 说明 |
|---|---|
| `Arrow` | 默认的箭头指针。 |
| `Hand` | 手形指针（表示元素可点击）。 |
| `IBeam` | 文本编辑光标。 |
| `Cross` | Crosshair. |
| `SizeWestEast` | 水平方向调整尺寸。 |
| `SizeNorthSouth` | 垂直方向调整尺寸。 |
| `SizeAll` | 任意方向移动/拖动。 |
| `Wait` | 忙碌指示（沙漏/转圈）。 |
| `AppStarting` | 箭头带小沙漏。 |
| `No` | 禁止（带斜线的圆圈）。 |
| `None` | 隐藏光标。 |

### 在代码中设置光标 {#setting-the-cursor-in-code}

```csharp
myControl.Cursor = new Cursor(StandardCursorType.Hand);
```

### 在拖动过程中改变光标 {#changing-the-cursor-during-drag-operations}

```csharp
private void OnPointerMoved(object? sender, PointerEventArgs e)
{
    if (_isDragging)
    {
        Cursor = new Cursor(StandardCursorType.SizeAll);
    }
}

private void OnPointerReleased(object? sender, PointerReleasedEventArgs e)
{
    _isDragging = false;
    Cursor = Cursor.Default;
}
```

## 更多信息 {#more-information}

指针事件与轻点事件的完整 API 文档，请参阅 [PointerEventArgs API 参考](/api/avalonia/input/pointereventargs)。

## 另请参阅 {#see-also}

- [手势](/docs/input-interaction/gestures)：构建在指针事件之上的更高层手势事件。
- [拖放](/docs/input-interaction/drag-and-drop)：借助指针事件实现的拖放操作。
- [路由事件](/docs/input-interaction/routed-events)：事件如何在元素树中传播。
