---
id: animation-settings
title: 动画设置
description: 关键帧动画的各项配置，包括缓动、填充模式和播放方式。
doc-type: reference
---

import LinearEasingScreenshot from '/img/reference/animations-and-graphics/animation-settings/linear-easing.png';
import BackEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/back-ease-in.png';
import BackEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/back-ease-in-out.png';
import BackEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/back-ease-out.png';
import BounceEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/bounce-ease-in.png';
import BounceEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/bounce-ease-in-out.png';
import BounceEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/bounce-ease-out.png';
import CircularEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/circular-ease-in.png';
import CircularEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/circular-ease-in-out.png';
import CircularEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/circular-ease-out.png';
import CubicEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/cubic-ease-in.png';
import CubicEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/cubic-ease-in-out.png';
import CubicEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/cubic-ease-out.png';
import ElasticEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/elastic-ease-in.png';
import ElasticEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/elastic-ease-in-out.png';
import ElasticEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/elastic-ease-out.png';
import ExponentialEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/exponential-ease-in.png';
import ExponentialEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/exponential-ease-in-out.png';
import ExponentialEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/exponential-ease-out.png';
import QuadraticEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/quadratic-ease-in.png';
import QuadraticEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/quadratic-ease-in-out.png';
import QuadraticEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/quadratic-ease-out.png';
import QuarticEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/quartic-ease-in.png';
import QuarticEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/quartic-ease-in-out.png';
import QuarticEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/quartic-ease-out.png';
import QuinticEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/quintic-ease-in.png';
import QuinticEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/quintic-ease-in-out.png';
import QuinticEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/quintic-ease-out.png';
import SineEaseInScreenshot from '/img/reference/animations-and-graphics/animation-settings/sine-ease-in.png';
import SineEaseInOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/sine-ease-in-out.png';
import SineEaseOutScreenshot from '/img/reference/animations-and-graphics/animation-settings/sine-ease-out.png';

本节介绍 `Animation` 的播放过程可以怎样定制。

## 缓动函数 {#easing-functions}

缓动函数描述的是：在整段动画时间里，被动画的属性从起始值变到结束值的快慢节奏。`Avalonia.Animation.Easings` 提供了下列缓动函数：

| 默认值                                                       |
|---------------------------------------------------------------|
| `LinearEasing`<br/><Image light={LinearEasingScreenshot} alt="Graph showing linear easing curve" position="center" maxWidth={400} cornerRadius="true"/> |

| 缓入（Ease-In）                                                                 | 缓出（Ease-Out）                                                                  | 缓入缓出（Ease-In-Out）                                                                   |
|-------------------------------------------------------------------------|---------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| `SineEaseIn`<br/><Image light={SineEaseInScreenshot} alt="Graph showing SineEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/>               | `SineEaseOut`<br/><Image light={SineEaseOutScreenshot} alt="Graph showing SineEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/>               | `SineEaseInOut`<br/><Image light={SineEaseInOutScreenshot} alt="Graph showing SineEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/>               |
| `QuadraticEaseIn`<br/><Image light={QuadraticEaseInScreenshot} alt="Graph showing QuadraticEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/>     | `QuadraticEaseOut`<br/><Image light={QuadraticEaseOutScreenshot} alt="Graph showing QuadraticEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/>     | `QuadraticEaseInOut`<br/><Image light={QuadraticEaseInOutScreenshot} alt="Graph showing QuadraticEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/>     |
| `CubicEaseIn`<br/><Image light={CubicEaseInScreenshot} alt="Graph showing CubicEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/>             | `CubicEaseOut`<br/><Image light={CubicEaseOutScreenshot} alt="Graph showing CubicEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/>             | `CubicEaseInOut`<br/><Image light={CubicEaseInOutScreenshot} alt="Graph showing CubicEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/>             |
| `QuarticEaseIn`<br/><Image light={QuarticEaseInScreenshot} alt="Graph showing QuarticEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/>         | `QuarticEaseOut`<br/><Image light={QuarticEaseOutScreenshot} alt="Graph showing QuarticEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/>         | `QuarticEaseInOut`<br/><Image light={QuarticEaseInOutScreenshot} alt="Graph showing QuarticEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/>         |
| `QuinticEaseIn`<br/><Image light={QuinticEaseInScreenshot} alt="Graph showing QuinticEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/>         | `QuinticEaseOut`<br/><Image light={QuinticEaseOutScreenshot} alt="Graph showing QuinticEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/>         | `QuinticEaseInOut`<br/><Image light={QuinticEaseInOutScreenshot} alt="Graph showing QuinticEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/>         |
| `ExponentialEaseIn`<br/><Image light={ExponentialEaseInScreenshot} alt="Graph showing ExponentialEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/> | `ExponentialEaseOut`<br/><Image light={ExponentialEaseOutScreenshot} alt="Graph showing ExponentialEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/> | `ExponentialEaseInOut`<br/><Image light={ExponentialEaseInOutScreenshot} alt="Graph showing ExponentialEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/> |
| `CircularEaseIn`<br/><Image light={CircularEaseInScreenshot} alt="Graph showing CircularEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/>       | `CircularEaseOut`<br/><Image light={CircularEaseOutScreenshot} alt="Graph showing CircularEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/>       | `CircularEaseInOut`<br/><Image light={CircularEaseInOutScreenshot} alt="Graph showing CircularEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/>       |
| `BackEaseIn`<br/><Image light={BackEaseInScreenshot} alt="Graph showing BackEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/>               | `BackEaseOut`<br/><Image light={BackEaseOutScreenshot} alt="Graph showing BackEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/>               | `BackEaseInOut`<br/><Image light={BackEaseInOutScreenshot} alt="Graph showing BackEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/>             |
| `ElasticEaseIn`<br/><Image light={ElasticEaseInScreenshot} alt="Graph showing ElasticEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/>         | `ElasticEaseOut`<br/><Image light={ElasticEaseOutScreenshot} alt="Graph showing ElasticEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/>         | `ElasticEaseInOut`<br/><Image light={ElasticEaseInOutScreenshot} alt="Graph showing ElasticEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/>         |
| `BounceEaseIn`<br/><Image light={BounceEaseInScreenshot} alt="Graph showing BounceEaseIn curve" position="center" maxWidth={400} cornerRadius="true"/>           | `BounceEaseOut`<br/><Image light={BounceEaseOutScreenshot} alt="Graph showing BounceEaseOut curve" position="center" maxWidth={400} cornerRadius="true"/>           | `BounceEaseInOut`<br/><Image light={BounceEaseInOutScreenshot} alt="Graph showing BounceEaseInOut curve" position="center" maxWidth={400} cornerRadius="true"/>           |

此外，你也可以派生 `Easing` 来自定义缓动，或者给 `SplineEasing`、`SpringEasing` 传入参数来调配。

## 填充模式 {#fill-mode}

`Animation` 的 `FillMode` 特性决定了：动画结束之后、以及两次播放之间的延迟期内，被动画的属性该保持什么值。

| 值      | 说明                                                                                               |
|------------|-----------------------------------------------------------------------------------------------------------|
| `None`     | 动画结束后不保留末值；若动画有延迟，首值也不会提前生效。 |
| `Forward`  | 动画结束后保留最后一个插值结果。                                     |
| `Backward` | 若动画有延迟，延迟期间显示第一个插值结果。                                        |
| `Both`     | 同时具备 `Forward` 和 `Backward` 两种行为。                                                  |

## 播放方向 {#playback-direction}

`PlaybackDirection` 决定 `Animation` 怎么播。默认是正向播放，即沿缓动函数的曲线从左往右走。

| 值              | 说明                                             |
|--------------------|---------------------------------------------------------|
| `Normal`           | （默认）正向播放。                       |
| `Reverse`          | 反向播放。           |
| `Alternate`        | 先正向播，再反向播。 |
| `AlternateReverse` | 先反向播，再正向播。 |

## 播放行为 {#playback-behavior}

默认情况下，当目标控件实际不可见时，关键帧动画会暂停；控件重新可见后，动画从暂停处接着播。

这么做是为了避免为用户根本看不见的动画唤醒 CPU。控件自身的 `IsVisible` 为 `false`，或者它的某个祖先被隐藏时，该控件就算实际不可见。

| 值           | 说明             |
| ----------------| ----------------------- |
| `Auto`          | （默认）控件实际不可见时动画暂停。但用 `RunAsync` 启动的动画、以及含有 `IsVisible="True"` 关键帧的动画，无论可见与否都照常播放。 |
| `Always`        | 动画始终播放，与是否可见无关。 |
| `OnlyIfVisible` | 只要控件实际不可见，动画就一定暂停——哪怕它是用 `RunAsync` 启动的。 |

## 重复次数 {#iteration-count}

`Animation` 元素上的 `IterationCount` 设定动画重播多少次。这个设置有两种写法：

| 值      | 说明                                      |
|------------|--------------------------------------------------|
| `N`        | 其中 N 为整数，表示播放 N 次，N 可以为零。 |
| `infinite` | 无限重复。                                  |

## 另请参阅 {#see-also}

- [关键帧动画](/docs/graphics-animation/keyframe-animations)：在 XAML 中定义关键帧动画。
- [控件过渡](/docs/graphics-animation/control-transitions)：用过渡为属性变化加动画。
- [缓动函数](/docs/graphics-animation/easing-functions)：全部可用的缓动函数。
