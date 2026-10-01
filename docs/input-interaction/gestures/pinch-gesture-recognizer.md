---
id: pinch-gesture-recognizer
title: 捏合
description: 用 PinchGestureRecognizer 跟踪捏合手势，实现缩放交互。
doc-type: reference
---

一个跟踪捏合手势的手势识别器。所谓捏合手势，就是两个指针接触点相向靠拢或相背分开。这在实现捏合缩放交互的控件中很有用。

<div style={{textAlign: 'center', margin: '24px 0'}}>
<svg width="240" height="190" viewBox="0 0 240 190" fill="none" xmlns="http://www.w3.org/2000/svg">
  {/* Trackpad surface */}
  <rect x="20" y="10" width="200" height="140" rx="14"
    fill="currentColor" fillOpacity="0.03"
    stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.12"/>
  <rect x="24" y="14" width="192" height="132" rx="11"
    fill="none"
    stroke="currentColor" strokeWidth="0.5" strokeOpacity="0.06"/>
  {/* Left touch point */}
  <circle cy="80" r="14"
    fill="currentColor" fillOpacity="0.08"
    stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.35">
    <animate attributeName="cx"
      values="108;108;62;62;108;108"
      keyTimes="0;0.06;0.44;0.56;0.94;1"
      calcMode="spline"
      keySplines="0 0 1 1;0.25 0.1 0.25 1;0 0 1 1;0.25 0.1 0.25 1;0 0 1 1"
      dur="5s" repeatCount="indefinite"/>
  </circle>
  {/* Right touch point */}
  <circle cy="80" r="14"
    fill="currentColor" fillOpacity="0.08"
    stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.35">
    <animate attributeName="cx"
      values="132;132;178;178;132;132"
      keyTimes="0;0.06;0.44;0.56;0.94;1"
      calcMode="spline"
      keySplines="0 0 1 1;0.25 0.1 0.25 1;0 0 1 1;0.25 0.1 0.25 1;0 0 1 1"
      dur="5s" repeatCount="indefinite"/>
  </circle>
  {/* Label: Zoom in */}
  <text x="120" y="176" textAnchor="middle"
    fill="currentColor" fontSize="13" fontFamily="system-ui, sans-serif">
    <animate attributeName="opacity"
      values="0.5;0.5;0;0;0.5"
      keyTimes="0;0.46;0.5;0.96;1"
      dur="5s" repeatCount="indefinite"/>
    放大
  </text>
  {/* Label: Zoom out */}
  <text x="120" y="176" textAnchor="middle"
    fill="currentColor" fontSize="13" fontFamily="system-ui, sans-serif">
    <animate attributeName="opacity"
      values="0;0;0.5;0.5;0"
      keyTimes="0;0.46;0.5;0.96;1"
      dur="5s" repeatCount="indefinite"/>
    缩小
  </text>
</svg>
</div>

## 使用 PinchGestureRecognizer {#using-a-pinchgesturerecognizer}
通过控件的 `GestureRecognizers` 属性，可以把 PinchGestureRecognizer 挂到控件上。
```xml
<Image Stretch="UniformToFill"
        Margin="5"
        Name="image"
        Source="/image.jpg">
  <Image.GestureRecognizers>
    <PinchGestureRecognizer/>
  </Image.GestureRecognizers>
</Image>
```

```csharp title='C#'
image.GestureRecognizers.Add(new PinchGestureRecognizer());
```

PinchGestureRecognizer 检测到捏合手势开始时会引发 `InputElement.PinchEvent`；当手势结束——指针松开或另一个手势开始——时会引发 `InputElement.PinchEndedEvent`。
传给 `InputElement.PinchEvent` 事件处理程序的参数中，`Scale` 属性给出的是自手势开始以来的相对缩放比例。

## 绑定事件 {#binding-events}
把 PinchGestureRecognizer 添加到控件之后，你需要在代码隐藏中绑定这些事件，既可以写内联处理程序，也可以绑到一个事件函数上：
```csharp title='C#'
image.AddHandler(InputElement.PinchEvent, (s, e) => { });
image.AddHandler(InputElement.PinchEndedEvent, (s, e) => { });
```
```csharp title='C#'
image.AddHandler(InputElement.PinchEvent, Image_PinchGesture);
image.AddHandler(InputElement.PinchEndedEvent, Image_PinchGestureEnded);
...
private void Image_PinchGesture(object? sender, PinchGestureEventArgs e) { }
private void Image_PinchGestureEnded(object? sender, PinchGestureEndedEventArgs e) { }
```
若你的事件处理程序已经把这个手势处理完毕，可以这样把事件标记为已处理：
```csharp title='C#'
e.Handled = true;
```

## 按指针类型过滤 {#pointer-type-filtering}

`PinchGestureRecognizer` 对所有指针类型（鼠标、触摸、触控笔）都有反应。若你的应用只想让触摸输入触发捏合缩放（比如要把触控笔留给绘画），就得写一个按 `PointerType.Touch` 过滤的[自定义手势识别器](/docs/input-interaction/gestures#custom-gesture-recognizers)。

## 更多信息 {#more-information}

:::info
在 _GitHub_ 上查看源码

[`PinchGestureRecognizer.cs`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Input/GestureRecognizers/PinchGestureRecognizer.cs)

[`PinchEventArgs.cs`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Input/PinchEventArgs.cs)
:::

## 另请参阅 {#see-also}

- [手势](/docs/input-interaction/gestures)：手势识别器与内置手势事件概览。
- [滚动手势识别器](/docs/input-interaction/gestures/scroll-gesture-recognizer)：用于平移内容的滚动手势。
- [下拉手势识别器](/docs/input-interaction/gestures/pull-gesture-recognizer)：用于下拉刷新交互的拉拽手势。
