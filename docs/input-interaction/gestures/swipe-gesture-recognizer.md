---
id: swipe-gesture-recognizer
title: 滑动
doc-type: reference
description: 滑动手势识别器能辨认出用户朝某一方向快速拖动指针的动作，并逐事件给出速度数据，便于实现过渡效果。
---

一个跟踪滑动手势、用于离散翻页交互的手势识别器。`SwipeGestureRecognizer` 会检测用户朝某一方向快速拖动指针的动作，并逐事件给出速度数据，从而支持轮播翻页之类对速度敏感的过渡。与 `ScrollGestureRecognizer` 不同，它不带惯性，也没有连续滚动的物理效果。

当控件需要响应刻意为之的方向性轻扫时（比如在轮播图中翻页），请用 `SwipeGestureRecognizer`。若要的是带惯性的连续平移，请改用 [`ScrollGestureRecognizer`](/docs/input-interaction/gestures/scroll-gesture-recognizer)。

## 使用 SwipeGestureRecognizer {#using-a-swipegesturerecognizer}

通过控件的 `GestureRecognizers` 属性，可以把 `SwipeGestureRecognizer` 挂到控件上。
```xml
<Border Name="swipeArea" Background="Transparent" Height="300">
    <Border.GestureRecognizers>
        <SwipeGestureRecognizer CanHorizontallySwipe="True" />
    </Border.GestureRecognizers>
    <TextBlock Text="Swipe left or right"
               HorizontalAlignment="Center"
               VerticalAlignment="Center" />
</Border>
```

```csharp title='C#'
swipeArea.GestureRecognizers.Add(new SwipeGestureRecognizer
{
    CanHorizontallySwipe = true,
    CanVerticallySwipe = false
});
```

滑动过程中指针每移动一下，`SwipeGestureRecognizer` 就会引发一次 `InputElement.SwipeGestureEvent`；当滑动结束——指针松开或另一个手势开始——时，它会引发 `InputElement.SwipeGestureEndedEvent`。

## 绑定事件 {#binding-events}

把 `SwipeGestureRecognizer` 添加到控件之后，请在代码隐藏中绑定这些事件，既可以写内联处理程序，也可以绑到一个事件函数上：

```csharp title='C#'
swipeArea.AddHandler(InputElement.SwipeGestureEvent, (s, e) => { });
swipeArea.AddHandler(InputElement.SwipeGestureEndedEvent, (s, e) => { });
```

```csharp title='C#'
swipeArea.AddHandler(InputElement.SwipeGestureEvent, OnSwipeGesture);
swipeArea.AddHandler(InputElement.SwipeGestureEndedEvent, OnSwipeGestureEnded);
...
private void OnSwipeGesture(object? sender, SwipeGestureEventArgs e) { }
private void OnSwipeGestureEnded(object? sender, SwipeGestureEndedEventArgs e) { }
```

若你的事件处理程序已经把这个手势处理完毕，可以这样把事件标记为已处理：

```csharp title='C#'
e.Handled = true;
```

## 事件参数 {#event-args}

`SwipeGestureEventArgs` 在手势进行期间引发：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Id` | `int` | 本次手势序列的唯一标识。 |
| `Delta` | `Vector` | 自上一次事件以来的像素增量。 |
| `Velocity` | `Vector` | 当前的滑动速度，单位为像素每秒。 |
| `SwipeDirection` | `SwipeDirection` | 滑动的主方向：`Left`、`Right`、`Up` 或 `Down`。 |

`SwipeGestureEndedEventArgs` 在指针松开时引发：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Id` | `int` | 本次手势序列的唯一标识。 |
| `Velocity` | `Vector` | 指针松开那一刻的滑动速度。 |

## 属性 {#properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 | 默认值 |
|---|---|---|---|
| `CanHorizontallySwipe` | `bool` | 启用对横向（左/右）滑动的跟踪。 | `false` |
| `CanVerticallySwipe` | `bool` | 启用对纵向（上/下）滑动的跟踪。 | `false` |
| `Threshold` | `double` | 指针至少要移动多少像素才算识别出滑动。设为 0 时采用平台默认阈值。 | 0 |
| `IsMouseEnabled` | `bool` | 为 `true` 时，除触摸和触控笔外，鼠标指针事件也能触发滑动手势。 | `false` |
| `IsEnabled` | `bool` | 整体启用或禁用该识别器。 | `true`. |

## 示例 {#examples}

### 检测横向滑动以实现翻页 {#detecting-horizontal-swipes-to-navigate-pages}

```csharp title='C#'
int currentPage = 0;
int totalPages = 5;

swipeArea.AddHandler(InputElement.SwipeGestureEndedEvent, (s, e) =>
{
    if (Math.Abs(e.Velocity.X) > 200) // fast enough flick
    {
        if (e.Velocity.X < 0 && currentPage < totalPages - 1)
            currentPage++;
        else if (e.Velocity.X > 0 && currentPage > 0)
            currentPage--;
    }
});
```

### 纵向滑动检测 {#vertical-swipe-detection}

```xml
<Border Name="verticalSwipeArea" Background="Transparent">
    <Border.GestureRecognizers>
        <SwipeGestureRecognizer CanVerticallySwipe="True" />
    </Border.GestureRecognizers>
</Border>
```

### 启用鼠标支持 {#enabling-mouse-support}

默认情况下只有触摸和触控笔输入会触发滑动手势。桌面场景下可以启用鼠标支持：

```xml
<Border.GestureRecognizers>
    <SwipeGestureRecognizer CanHorizontallySwipe="True"
                            IsMouseEnabled="True" />
</Border.GestureRecognizers>
```

## 另请参阅 {#see-also}

- [API 参考](/api/avalonia/input/gesturerecognizers/swipegesturerecognizer)
- [源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Input/GestureRecognizers/SwipeGestureRecognizer.cs)
- [手势](/docs/input-interaction/gestures)：手势识别器与内置手势事件概览。
- [滚动](/docs/input-interaction/gestures/scroll-gesture-recognizer)：带惯性的连续平移滚动手势。
- [拉拽](/docs/input-interaction/gestures/pull-gesture-recognizer)：用于下拉刷新交互的拉拽手势。
- [捏合](/docs/input-interaction/gestures/pinch-gesture-recognizer)：用于缩放交互的捏合手势。
