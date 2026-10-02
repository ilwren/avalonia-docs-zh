---
id: pull-gesture-recognizer
title: 拉拽
---

一个跟踪拉拽手势的手势识别器。所谓拉拽手势，是指指针从控件边缘出发、沿 `PullDirection` 属性所定的某一个特定方向拖动。典型用途是下拉刷新：用户从列表顶部往下拖，触发数据重新加载。

与 [`ScrollGestureRecognizer`](/docs/input-interaction/gestures/scroll-gesture-recognizer) 不同，`PullGestureRecognizer` 面向的是刻意为之的单向交互，而非自由平移。它要求起手的拖动距离更长才会激活，只认一个预设方向上的移动，也不带惯性。这些特点让它很适合那些需要用户意图明确之后才触发的操作。

<div style={{textAlign: 'center', margin: '24px 0'}}>
<svg width="240" height="190" viewBox="0 0 240 190" fill="none" xmlns="http://www.w3.org/2000/svg">
  {/* Trackpad surface */}
  <rect x="20" y="10" width="200" height="140" rx="14"
    fill="currentColor" fillOpacity="0.03"
    stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.12"/>
  <rect x="24" y="14" width="192" height="132" rx="11"
    fill="none"
    stroke="currentColor" strokeWidth="0.5" strokeOpacity="0.06"/>
  {/* Touch point 1: Top to bottom (active 0-22%) */}
  <circle cx="120" r="14"
    fill="currentColor" fillOpacity="0.08"
    stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.35">
    <animate attributeName="cy"
      values="30;30;115;115;30;30"
      keyTimes="0;0.03;0.20;0.22;0.24;1"
      calcMode="spline"
      keySplines="0 0 1 1;0.25 0.1 0.25 1;0 0 1 1;0 0 1 1;0 0 1 1"
      dur="10s" repeatCount="indefinite"/>
    <animate attributeName="opacity"
      values="0;1;1;0;0;0"
      keyTimes="0;0.02;0.20;0.23;0.25;1"
      dur="10s" repeatCount="indefinite"/>
  </circle>
  {/* Touch point 2: Bottom to top (active 25-47%) */}
  <circle cx="120" r="14"
    fill="currentColor" fillOpacity="0.08"
    stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.35">
    <animate attributeName="cy"
      values="130;130;130;40;40;130;130"
      keyTimes="0;0.25;0.28;0.45;0.47;0.49;1"
      calcMode="spline"
      keySplines="0 0 1 1;0 0 1 1;0.25 0.1 0.25 1;0 0 1 1;0 0 1 1;0 0 1 1"
      dur="10s" repeatCount="indefinite"/>
    <animate attributeName="opacity"
      values="0;0;0;1;1;0;0"
      keyTimes="0;0.25;0.27;0.28;0.45;0.48;1"
      dur="10s" repeatCount="indefinite"/>
  </circle>
  {/* Touch point 3: Left to right (active 50-72%) */}
  <circle cy="80" r="14"
    fill="currentColor" fillOpacity="0.08"
    stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.35">
    <animate attributeName="cx"
      values="40;40;40;200;200;40;40"
      keyTimes="0;0.50;0.53;0.70;0.72;0.74;1"
      calcMode="spline"
      keySplines="0 0 1 1;0 0 1 1;0.25 0.1 0.25 1;0 0 1 1;0 0 1 1;0 0 1 1"
      dur="10s" repeatCount="indefinite"/>
    <animate attributeName="opacity"
      values="0;0;0;1;1;0;0"
      keyTimes="0;0.50;0.52;0.53;0.70;0.73;1"
      dur="10s" repeatCount="indefinite"/>
  </circle>
  {/* Touch point 4: Right to left (active 75-97%) */}
  <circle cy="80" r="14"
    fill="currentColor" fillOpacity="0.08"
    stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.35">
    <animate attributeName="cx"
      values="200;200;200;40;40;200;200"
      keyTimes="0;0.75;0.78;0.95;0.97;0.99;1"
      calcMode="spline"
      keySplines="0 0 1 1;0 0 1 1;0.25 0.1 0.25 1;0 0 1 1;0 0 1 1;0 0 1 1"
      dur="10s" repeatCount="indefinite"/>
    <animate attributeName="opacity"
      values="0;0;0;1;1;0;0"
      keyTimes="0;0.75;0.77;0.78;0.95;0.98;1"
      dur="10s" repeatCount="indefinite"/>
  </circle>
  {/* Labels */}
  <text x="120" y="176" textAnchor="middle"
    fill="currentColor" fontSize="13" fontFamily="system-ui, sans-serif">
    <animate attributeName="opacity"
      values="0;0.5;0.5;0;0;0;0;0;0"
      keyTimes="0;0.02;0.20;0.23;0.25;0.50;0.75;0.98;1"
      dur="10s" repeatCount="indefinite"/>
    自上而下
  </text>
  <text x="120" y="176" textAnchor="middle"
    fill="currentColor" fontSize="13" fontFamily="system-ui, sans-serif">
    <animate attributeName="opacity"
      values="0;0;0;0.5;0.5;0;0;0;0"
      keyTimes="0;0.23;0.27;0.28;0.45;0.48;0.50;0.98;1"
      dur="10s" repeatCount="indefinite"/>
    自下而上
  </text>
  <text x="120" y="176" textAnchor="middle"
    fill="currentColor" fontSize="13" fontFamily="system-ui, sans-serif">
    <animate attributeName="opacity"
      values="0;0;0;0.5;0.5;0;0"
      keyTimes="0;0.48;0.52;0.53;0.70;0.73;1"
      dur="10s" repeatCount="indefinite"/>
    自左向右
  </text>
  <text x="120" y="176" textAnchor="middle"
    fill="currentColor" fontSize="13" fontFamily="system-ui, sans-serif">
    <animate attributeName="opacity"
      values="0;0;0;0.5;0.5;0;0"
      keyTimes="0;0.73;0.77;0.78;0.95;0.98;1"
      dur="10s" repeatCount="indefinite"/>
    自右向左
  </text>
</svg>
</div>

## 使用 PullGestureRecognizer {#using-a-pullgesturerecognizer}
通过控件的 `GestureRecognizers` 属性，可以把 PullGestureRecognizer 挂到控件上。
```xml
<Border Width="500"
        Height="500"
        Margin="5"
        Name="border">
  <Border.GestureRecognizers>
    <PullGestureRecognizer PullDirection="TopToBottom"/>
  </Border.GestureRecognizers>
</Border>
```

```csharp title='C#'
border.GestureRecognizers.Add(new PullGestureRecognizer()
            {
                PullDirection = PullDirection.TopToBottom,
            });
```

指针沿预设方向移动的过程中，`PullGestureRecognizer` 会持续引发 `InputElement.PullGestureEvent`；当拉拽结束（指针松开或另一个手势开始）时，则引发 `InputElement.PullGestureEndedEvent`。

监听拉拽手势的控件，应当在 `PullGestureEndedEvent` 触发时把自己的视觉状态复位——除非拉拽距离已越过阈值、触发了既定的动作。举例来说，若用户没拉够距离就松手，下拉刷新指示器就该弹回原位。

### PullDirection
它定义了拉拽的方向，共有 4 个可选值：
* `PullDirection.TopToBottom`：从上边缘开始，向下拉
* `PullDirection.BottomToTop`：从下边缘开始，向上拉
* `PullDirection.LeftToRight`：从左边缘开始，向右拉
* `PullDirection.RightToLeft`：从右边缘开始，向左拉

## 绑定事件 {#binding-events}
把 PullGestureRecognizer 添加到控件之后，你需要在代码隐藏中绑定这些事件，既可以写内联处理程序，也可以绑到一个事件函数上：
```csharp title='C#'
image.AddHandler(InputElement.PullGestureEvent, (s, e) => { });
image.AddHandler(InputElement.PullGestureEndedEvent, (s, e) => { });
```
```csharp title='C#'
image.AddHandler(InputElement.PullGestureEvent, Image_PullGesture);
image.AddHandler(InputElement.PullGestureEndedEvent, Image_PullGestureEnded);
...
private void Image_PullGesture(object? sender, PullGestureEventArgs e) { }
private void Image_PullGestureEnded(object? sender, PullGestureEndedEventArgs e) { }
```
若你的事件处理程序已经把这个手势处理完毕，可以这样把事件标记为已处理：
```csharp title='C#'
e.Handled = true;
```

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table>
    <thead>
      <tr>
        <th width="266">Property</th>
        <th>说明</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>PullDirection</td>
        <td>定义拉拽手势的方向。 </td>
      </tr>
    </tbody>
  </table>


## 更多信息 {#more-information}

:::info
在 _GitHub_ 上查看源码

[`PullGestureRecognizer.cs`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Input/GestureRecognizers/PullGestureRecognizer.cs)

[`PullGestureEventArgs.cs`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Input/PullGestureEventArgs.cs)
:::

## 另请参阅 {#see-also}

- [手势](/docs/input-interaction/gestures)：手势识别器与内置手势事件概览。
- [滚动手势识别器](/docs/input-interaction/gestures/scroll-gesture-recognizer)：用于平移内容的滚动手势。
- [捏合手势识别器](/docs/input-interaction/gestures/pinch-gesture-recognizer)：用于缩放交互的捏合手势。
