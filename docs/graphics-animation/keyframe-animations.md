---
id: keyframe-animations
title: 使用关键帧动画
description: 在 XAML 中定义关键帧动画，沿时间轴改变控件属性。
doc-type: how-to
---

import AnimationKeyframeDiagram from '/img/guides/ui-development/graphics/animation-keyframe.png';
import KeyframeFadeScreenshot from '/img/guides/ui-development/graphics/keyframe-fade.gif';
import KeyframeCompositeAnimationScreenshot from '/img/guides/ui-development/graphics/keyframe-composite-animation.gif';
import LinearEasingScreenshot from '/img/guides/ui-development/graphics/linear-easing.gif';
import BounceEaseInScreenshot from '/img/guides/ui-development/graphics/bounce-ease-in.gif';

关键帧动画能让一个或多个控件属性沿时间轴变化。关键帧写在 _Avalonia UI_ 样式里，沿动画的**持续时间**布置若干**节点（cue）**，在各个时间点上给出属性的中间值。

<Image light={AnimationKeyframeDiagram} alt="Diagram showing keyframe animation timeline with cue points" position="center" maxWidth={400} cornerRadius="true"/>
<br />

关键帧之间的属性值按**缓动函数**的曲线取值，默认的缓动函数是直线插值。

动画被触发后开始播放，可以播任意次，也能正反两个方向播。此外还可以延迟开始，或让它重复。

在 Avalonia 中，关键帧动画是用样式来定义的，更多内容请参阅[样式](/docs/styling/styles)。

## 为一个属性加动画 {#animating-a-property}

要给控件定义单属性动画（比如颜色渐变）：

1.  在你选定的层级上建一个样式集合。
2.  往集合里加一条样式，选择器指向目标控件。
3.  加一个 `Setter` 来指定你想让动画改变的属性，比如下例中的 `Fill`。
4.  为动画本身加上 `Style.Animations` 标签。
5.  加一个 `Animation` 标签并设置它的 `Duration` 特性，格式为 `"Hours:Minutes:Seconds"`。
6.  定义动画的各个关键帧。下例用的是 0% 和 100% 两个节点。
7. 每个关键帧都需要有自己的 `Setter` 来指定填充不透明度的取值。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <UserControl.Styles>
    <Style Selector="Rectangle.blue">
      <Setter Property="Fill" Value="Blue"/>
        <Style.Animations>
          <Animation Duration="0:0:3"
                     IterationCount="infinite"> 
            <KeyFrame Cue="0%">
              <Setter Property="Opacity" Value="0.0"/>
            </KeyFrame>
            <KeyFrame Cue="100%">
              <Setter Property="Opacity" Value="1.0"/>
            </KeyFrame>
          </Animation>
        </Style.Animations>
    </Style>
  </UserControl.Styles>

  <Rectangle Classes="blue" Width="100" Height="100"/>
</UserControl>
```

</XamlPreview>

## 同时为两个属性加动画 {#animate-two-properties}

这个例子演示如何在同一条时间轴上为两个属性加动画：这次蓝色矩形一边淡出一边旋转。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <UserControl.Styles>
    <Style Selector="Rectangle.blue">
      <Setter Property="Fill" Value="Blue"/>
        <Style.Animations>
          <Animation Duration="0:0:3"
                     IterationCount="infinite">
            <KeyFrame Cue="0%">
              <Setter Property="Opacity" Value="0.0"/>
              <Setter Property="RotateTransform.Angle" Value="0.0"/>
            </KeyFrame>
            <KeyFrame Cue="100%"> 
              <Setter Property="Opacity" Value="1.0"/>
              <Setter Property="RotateTransform.Angle" Value="90.0"/>
            </KeyFrame>
          </Animation> 
        </Style.Animations>
    </Style>
  </UserControl.Styles>

  <Rectangle Classes="blue" Width="100" Height="100"/>
</UserControl>
```

</XamlPreview>

## 配置动画 {#configuring-animation}

### Delay

设置 `Delay` 特性即可让动画延迟一段时间再开始。

```xml
<Animation Duration="0:0:1"
           Delay="0:0:1"> 
    ...
</Animation>
```

### Repeat

设置 `IterationCount` 特性即可让动画重复指定次数，或无限重复。

```xml
<!-- Repeat 5 times -->
<Animation IterationCount="5">
    ...
</Animation>

<!-- Repeat indefinitely -->
<Animation IterationCount="infinite">
    ...
</Animation>
```

### 播放方向 {#playback-direction}

动画默认正向播放，沿缓动函数的曲线从左往右走。设置 `PlaybackDirection` 特性可以改变这一行为。

```xml
<Animation Duration="0:0:1" PlaybackDirection="Reverse">
    ...
</Animation>
```

`PlaybackDirection` 的完整取值清单，请参阅[动画设置参考](/docs/graphics-animation/animation-settings#playback-direction)。

### 填充模式 {#fill-mode}

动画的填充模式特性决定了：动画播完之后、以及两次播放的间隙里，被设置的属性该保持什么值。

```xml
<Animation IterationCount="9" FillMode="Backward">
    ...
</Animation>
```

`FillMode` 的完整取值清单，请参阅[动画设置参考](/docs/graphics-animation/animation-settings#fill-mode)。

### 播放行为 {#playback-behavior}

默认情况下，当目标控件实际不可见时，关键帧动画会暂停；控件重新可见后，动画从暂停处接着播。

设置 `PlaybackBehavior` 特性即可改变这一行为。

```xml
<Animation Duration="0:0:1" IterationCount="infinite" PlaybackBehavior="Always">
    ...
</Animation>
```

`PlaybackBehavior` 的完整取值清单，请参阅[动画设置参考](/docs/graphics-animation/animation-settings#playback-behavior)。

:::info
这套播放行为只适用于关键帧动画，[控件过渡](/docs/graphics-animation/control-transitions)和[组合动画](/docs/graphics-animation/composition-animations)不受影响。
:::

### 缓动函数 {#easing-functions}

缓动函数定义了动画过程中属性随时间变化的方式。

<Image light={LinearEasingScreenshot} alt="Graph showing linear easing function" position="center" maxWidth={400} cornerRadius="true"/>
<br />

默认的缓动函数是线性的（见上）。在 `Easing` 特性中填上目标函数的名字即可换成别的曲线。比如要用 'bounce ease in'（见下）：

```xml
<Animation Duration="0:0:1"
           Delay="0:0:1"
           // highlight-next-line
           Easing="BounceEaseIn"> 
    ...
</Animation>
```

<Image light={BounceEaseInScreenshot} alt="Graph showing bounce ease-in easing function" position="center" maxWidth={400} cornerRadius="true"/>
<br />

你也可以自己写一个缓动函数类，然后这样套用：

```xml
<Animation Duration="0:0:1"
           Delay="0:0:1">
    <Animation.Easing>
        <local:YourCustomEasingClassHere/>
    </Animation.Easing> 
    ...
</Animation>
```

完整的缓动函数清单请参阅[缓动函数页面](/docs/graphics-animation/easing-functions)。

## 从代码隐藏中运行动画 {#running-animations-from-code-behind}

若想更深入地掌控动画的生命周期，可以把动画定义成 `Resource`，这样在代码隐藏中就能用上它。

把动画定义为资源时，必须给它设置 `x:Key` 以便被引用到，同时还要设置 `x:SetterTargetType` 来指定目标控件。

```xml
<Window xmlns="https://github.com/avaloniaui">
    <Window.Resources>
        // highlight-start
        <Animation x:Key="ResourceAnimation"
                   x:SetterTargetType="Rectangle"
        // highlight-end
                   Duration="0:0:3"> 
            <KeyFrame Cue="0%">
                <Setter Property="Opacity" Value="0.0"/>
            </KeyFrame>
            <KeyFrame Cue="100%">
                <Setter Property="Opacity" Value="1.0"/>
            </KeyFrame>
        </Animation>
    </Window.Resources>

    <Rectangle x:Name="Rect" />
</Window>
```

上面定义的 `ResourceAnimation` 现在可以在代码隐藏的处理程序中取用了。

```csharp
var animation = (Animation)this.Resources["ResourceAnimation"];
// Running XAML animation on the Rect control. 
await animation.RunAsync(Rect);
```

`RunAsync` 返回一个任务，动画结束时该任务完成。若动画无限重复，这个任务就永远不会结束，除非（1）`RunAsync` 方法被 `CancellationToken` 取消，或者（2）目标控件从视觉树中分离。

## 另请参阅 {#see-also}

- [动画设置](/docs/graphics-animation/animation-settings)：时长、延迟、重复次数与播放方向。
- [缓动函数](/docs/graphics-animation/easing-functions)：全部可用的缓动函数。
- [控件过渡](/docs/graphics-animation/control-transitions)：用过渡为属性变化加动画。
- [PlaybackBehavior](/api/avalonia/animation/playbackbehavior)：基于可见性控制播放的 API 参考。