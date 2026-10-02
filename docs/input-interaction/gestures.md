---
id: gestures
title: 手势
description: 内置手势事件、手势识别器，以及触摸、触控笔和鼠标输入的自定义手势处理。
doc-type: overview
---

Avalonia 采用统一的指针事件体系。鼠标、触摸和触控笔输入都走同一套 `PointerPressed`、`PointerMoved`、`PointerReleased` 事件，而不是每种设备各有一套事件类型。指针事件告诉你硬件做了什么：某个按键按下了，某根手指移动了。

手势则是架在指针事件之上的更高层抽象，表达的是用户*想做什么*：轻点、捏合缩放、滚动。

Avalonia 提供两类手势：

**内置手势事件**涵盖了最常见的交互：

| 事件 | 说明 |
|---|---|
| `Tapped` | 指针在控件上按下又松开。 |
| `DoubleTapped` | 在平台规定的双击时限和距离阈值内，于同一位置轻点了两次。 |
| `Holding` | 指针按下后不动地保持住。需要用 `InputElement.IsHoldingEnabled` 为每个控件单独启用。 |

**手势识别器**负责辨认更复杂的多指或方向性模式。把它们添加到控件的 `GestureRecognizers` 集合里，它们就会盯着该控件的指针事件、从中识别特定模式：

| 识别器 | 说明 |
|---|---|
| [`PinchGestureRecognizer`](/docs/input-interaction/gestures/pinch-gesture-recognizer) | 两个指针相向或相背移动，用于捏合缩放。 |
| [`PullGestureRecognizer`](/docs/input-interaction/gestures/pull-gesture-recognizer) | 指针从控件边缘朝某个方向拖动，用于下拉刷新。 |
| [`ScrollGestureRecognizer`](/docs/input-interaction/gestures/scroll-gesture-recognizer) | 拖动指针以横向、纵向或双向滚动内容。 |
| [`SwipeGestureRecognizer`](/docs/input-interaction/gestures/swipe-gesture-recognizer) | 快速的方向性拖动，用于离散的翻页式交互。会给出速度数据，便于做对速度敏感的过渡。 |

## 挂上手势识别器 {#attaching-a-gesture-recognizer}

手势识别器可以在 XAML 或代码隐藏中添加到控件上：

```xml
<Image Stretch="UniformToFill" Name="image" Source="/image.jpg">
  <Image.GestureRecognizers>
    <PinchGestureRecognizer />
  </Image.GestureRecognizers>
</Image>
```

```csharp title='C#'
image.GestureRecognizers.Add(new PinchGestureRecognizer());
```

挂好之后，识别器就会盯着控件的指针事件，一旦识别出匹配的模式便引发对应的手势事件。每个识别器都会引发一个开始事件（比如 `InputElement.PinchEvent`）和一个结束事件（比如 `InputElement.PinchEndedEvent`）。

## 订阅手势事件 {#subscribing-to-gesture-events}

手势识别器的事件都是路由事件，用 `AddHandler` 订阅：

```csharp title='C#'
image.AddHandler(InputElement.PinchEvent, (sender, args) =>
{
    var scale = args.Scale;
    // Handle pinch
});
```

若你的处理程序已经把这个手势处理妥当，可以把它标记为已处理，阻止它继续向上冒泡：

```csharp title='C#'
args.Handled = true;
```

## 按住手势 {#holding-gesture}

与 `Tapped` 和 `DoubleTapped` 不同，`Holding` 手势必须设置 `InputElement.IsHoldingEnabled` 附加属性，为每个控件单独启用：

```xml
<Border InputElement.IsHoldingEnabled="True" Holding="OnHolding" />
```

按住的时长由 `TopLevel` 上的 `PlatformSettings.HoldWaitDuration` 决定。时长一到就会触发一次 `Holding` 事件，此时 `HoldingState.Started`；指针松开时再触发一次，此时 `HoldingState.Completed`。若按住期间开始了新手势、或按下了第二个指针，则触发时为 `HoldingState.Canceled`。

若想让鼠标指针（而不只是触摸）也能触发按住手势，请设置 `InputElement.IsHoldWithMouseEnabled`：

```xml
<Border InputElement.IsHoldingEnabled="True"
        InputElement.IsHoldWithMouseEnabled="True"
        Holding="OnHolding" />
```

## 同时使用多个手势识别器 {#combining-multiple-gesture-recognizers}

同一个控件上可以挂多个手势识别器。比如要让一张图片既能捏合缩放又能平移：

```xml
<Image Name="image" Source="/image.jpg">
  <Image.GestureRecognizers>
    <PinchGestureRecognizer />
    <ScrollGestureRecognizer CanHorizontallyScroll="True"
                              CanVerticallyScroll="True" />
  </Image.GestureRecognizers>
</Image>
```

挂上多个识别器后，它们各自独立地盯着控件的指针事件。但同一时刻只能有一个识别器处于活动状态：某个识别器捕获了手势之后，其余识别器在该手势结束前都无法激活。

## 按指针类型过滤 {#pointer-type-filtering}

内置的手势识别器对所有指针类型（鼠标、触摸、触控笔）一视同仁。若应用要给不同输入设备安排不同行为，这就成了问题。比如绘图应用可能想用触控笔作画，用触摸来平移和缩放。

要区分输入设备，请查看指针事件参数中的 `PointerType`：

```csharp title='C#'
private void OnPointerPressed(object? sender, PointerPressedEventArgs e)
{
    var pointerType = e.Pointer.Type;

    if (pointerType == PointerType.Pen)
    {
        // Handle drawing
    }
    else if (pointerType == PointerType.Touch)
    {
        // Handle pan/zoom navigation
    }
}
```

由于内置识别器并不按指针类型过滤，那些需要按设备区分手势的场景（比如把触摸留给平移缩放、把触控笔留给绘画），就得自己写一个手势识别器。

## 自定义手势识别器 {#custom-gesture-recognizers}

要写一个自定义手势识别器，请继承 `GestureRecognizer` 并重写它的指针跟踪方法。这样你就能完全掌控捕获哪些指针事件、如何识别手势，以及引发哪些事件。

```csharp title='C#'
public class TouchOnlyPinchRecognizer : GestureRecognizer
{
    protected override void PointerPressed(PointerPressedEventArgs e)
    {
        if (e.Pointer.Type != PointerType.Touch)
            return;

        // Track touch contacts for pinch detection
    }

    protected override void PointerMoved(PointerEventArgs e)
    {
        // Calculate pinch scale from tracked contacts
    }

    protected override void PointerReleased(PointerReleasedEventArgs e)
    {
        // End gesture tracking
    }
}
```

自定义识别器的挂载方式与内置的别无二致：

```xml
<Image Name="image" Source="/image.jpg">
  <Image.GestureRecognizers>
    <local:TouchOnlyPinchRecognizer />
  </Image.GestureRecognizers>
</Image>
```

需要参考实现的话，请看 GitHub 上的[内置手势识别器源码](https://github.com/AvaloniaUI/Avalonia/tree/master/src/Avalonia.Base/Input/GestureRecognizers)。

## 另请参阅 {#see-also}

- [指针事件](/docs/input-interaction/pointer)：手势所依托的底层指针事件。
- [路由事件](/docs/input-interaction/routed-events)：事件如何在元素树中传播。
