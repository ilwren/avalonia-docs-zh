---
id: easing-functions
title: 缓动函数
description: Avalonia 中可用的缓动函数，用于控制动画的时间曲线。
doc-type: reference
---

缓动函数控制动画过程中变化的快慢节奏，让运动显得自然。相比匀速（线性）变化，缓动函数通过加速、减速或弹跳，让过渡更有看头。

## 使用缓动函数 {#using-easing-functions}

在关键帧动画的 `KeyFrame` 上指定缓动函数：

```xml
<Border Background="Blue" Width="50" Height="50">
    <Border.Styles>
        <Style Selector="Border">
            <Style.Animations>
                <Animation Duration="0:0:1" IterationCount="Infinite" PlaybackDirection="Alternate">
                    <KeyFrame Cue="0%" KeySpline="0.1,0.9,0.2,1.0">
                        <Setter Property="TranslateTransform.X" Value="0" />
                    </KeyFrame>
                    <KeyFrame Cue="100%">
                        <Setter Property="TranslateTransform.X" Value="300" />
                    </KeyFrame>
                </Animation>
            </Style.Animations>
        </Style>
    </Border.Styles>
</Border>
```

也可以把缓动设在整个 `Animation` 上：

```xml
<Animation Duration="0:0:0.5" Easing="CubicEaseOut">
    <KeyFrame Cue="0%">
        <Setter Property="Opacity" Value="0" />
    </KeyFrame>
    <KeyFrame Cue="100%">
        <Setter Property="Opacity" Value="1" />
    </KeyFrame>
</Animation>
```

`Transitions` 中的属性变化动画同样会用到缓动函数：

```xml
<Border.Transitions>
    <DoubleTransition Property="Opacity" Duration="0:0:0.3" Easing="QuadraticEaseOut" />
</Border.Transitions>
```

## 内置缓动函数 {#built-in-easing-functions}

Avalonia 内置了一整套缓动函数，每个函数都有三种变体：

- **EaseIn**：起步慢，越往后越快
- **EaseOut**：起步快，越往后越慢
- **EaseInOut**：起步慢，中段加速，末尾再慢下来

### Linear

| 名称 | 行为 |
|---|---|
| `LinearEasing` | 匀速，不加速也不减速。 |

### Sine

基于正弦曲线的缓动，运动柔和平顺。

| 名称 | 变体 |
|---|---|
| `SineEaseIn` | 起步慢，逐渐加速 |
| `SineEaseOut` | 起步快，逐渐减速 |
| `SineEaseInOut` | 首尾都慢 |

### Quadratic

基于平方曲线（t^2）的缓动，比正弦略明显一些。

| 名称 | 变体 |
|---|---|
| `QuadraticEaseIn` | 起步慢 |
| `QuadraticEaseOut` | 起步快 |
| `QuadraticEaseInOut` | 首尾都慢 |

### Cubic

基于立方曲线（t^3）的缓动，比平方更戏剧化。

| 名称 | 变体 |
|---|---|
| `CubicEaseIn` | 起步慢 |
| [`CubicEaseOut`](/api/avalonia/animation/easings/cubiceaseout) | 起步快 |
| `CubicEaseInOut` | 首尾都慢 |

### Quartic

基于 t^4 的缓动，加速比立方更猛。

| 名称 | 变体 |
|---|---|
| `QuarticEaseIn` | 起步慢 |
| `QuarticEaseOut` | 起步快 |
| `QuarticEaseInOut` | 首尾都慢 |

### Quintic

基于 t^5 的缓动，是多项式缓动里最凌厉的一档。

| 名称 | 变体 |
|---|---|
| `QuinticEaseIn` | 起步慢 |
| `QuinticEaseOut` | 起步快 |
| `QuinticEaseInOut` | 首尾都慢 |

### Exponential

基于指数曲线的缓动，加速极其陡峭。

| 名称 | 变体 |
|---|---|
| `ExponentialEaseIn` | 起步极慢，随后陡然加速 |
| `ExponentialEaseOut` | 急剧减速，末尾极慢 |
| `ExponentialEaseInOut` | 加速和减速都很急剧 |

### Circular

基于圆弧曲线的缓动，运动感很自然。

| 名称 | 变体 |
|---|---|
| `CircularEaseIn` | 起步慢 |
| `CircularEaseOut` | 起步快 |
| `CircularEaseInOut` | 首尾都慢 |

### Back

先冲过目标再回落稳定，营造「回弹」效果。

| 名称 | 变体 |
|---|---|
| `BackEaseIn` | 先往回拉，再加速前冲 |
| [`BackEaseOut`](/api/avalonia/animation/easings/backeaseout) | 冲过目标后再回落稳定 |
| `BackEaseInOut` | 先回拉，再冲过头，最后稳定 |

### Bounce

模拟在边界处弹跳的效果。

| 名称 | 变体 |
|---|---|
| `BounceEaseIn` | 在开头弹跳 |
| `BounceEaseOut` | 在结尾弹跳 |
| `BounceEaseInOut` | 两端都弹跳 |

### Elastic

模拟弹簧或橡皮筋那样的振荡效果。

| 名称 | 变体 |
|---|---|
| `ElasticEaseIn` | 在开头振荡 |
| [`ElasticEaseOut`](/api/avalonia/animation/easings/elasticeaseout) | 在结尾振荡 |
| `ElasticEaseInOut` | 两端都振荡 |

## 怎么挑缓动函数 {#choosing-an-easing-function}

各类缓动的常见用武之地：

| 场景 | Recommended Easing |
|---|---|
| 淡入/淡出 | `QuadraticEaseOut` or `CubicEaseOut` |
| 面板滑入 | `CubicEaseOut` |
| 面板滑出 | `CubicEaseIn` |
| 按钮按下的反馈 | `QuadraticEaseInOut` |
| 展开/折叠 | `CubicEaseInOut` |
| 通知弹出 | `BackEaseOut` |
| 活泼的弹跳 | `BounceEaseOut` |
| 弹簧般的运动 | `ElasticEaseOut` or `SpringEasing` |
| 不抢眼的悬停效果 | `SineEaseOut` |

## SplineEasing (Custom Cubic Bezier)

若内置函数都不合心意，可以用 `SplineEasing` 自定义缓动曲线：给出四个控制点，定义一条三次贝塞尔曲线：

```xml
<Animation Duration="0:0:0.5">
    <Animation.Easing>
        <SplineEasing X1="0.25" Y1="0.1" X2="0.25" Y2="1.0" />
    </Animation.Easing>
    <KeyFrame Cue="0%">
        <Setter Property="Opacity" Value="0" />
    </KeyFrame>
    <KeyFrame Cue="100%">
        <Setter Property="Opacity" Value="1" />
    </KeyFrame>
</Animation>
```

你也可以用 `KeySpline` 简写、以逗号分隔的数值内联指定样条缓动：

```xml
<KeyFrame Cue="0%" KeySpline="0.25,0.1,0.25,1.0">
    <Setter Property="TranslateTransform.X" Value="0" />
</KeyFrame>
```

这四个值（`X1`、`Y1`、`X2`、`Y2`）定义了一条从 (0,0) 到 (1,1) 的三次贝塞尔曲线的两个控制点，与 CSS 的 `cubic-bezier()` 取值一致。常用预设：

| 曲线 | X1 | Y1 | X2 | Y2 | 等价于 |
|---|---|---|---|---|---|
| ease | 0.25 | 0.1 | 0.25 | 1.0 | CSS `ease` |
| ease-in | 0.42 | 0 | 1.0 | 1.0 | CSS `ease-in` |
| ease-out | 0 | 0 | 0.58 | 1.0 | CSS `ease-out` |
| ease-in-out | 0.42 | 0 | 0.58 | 1.0 | CSS `ease-in-out` |

## SpringEasing

`SpringEasing` 模拟基于物理的弹簧运动。与内置的弹性缓动函数不同，弹簧缓动让你能直接调节弹簧的物理属性：

```xml
<Animation Duration="0:0:1">
    <Animation.Easing>
        <SpringEasing Mass="1" Stiffness="100" Damping="10" InitialVelocity="0" />
    </Animation.Easing>
    <KeyFrame Cue="0%">
        <Setter Property="TranslateTransform.Y" Value="-50" />
    </KeyFrame>
    <KeyFrame Cue="100%">
        <Setter Property="TranslateTransform.Y" Value="0" />
    </KeyFrame>
</Animation>
```

### 弹簧参数 {#spring-parameters}

| 参数 | 说明 | 调大会怎样 |
|---|---|---|
| `Mass` | 弹簧上物体的质量 | 运动更慢、更沉 |
| `Stiffness` | 弹簧的劲度 | 振荡更快，更干脆利落 |
| `Damping` | 让弹簧慢下来的阻尼 | 振荡更少，更快稳定 |
| `InitialVelocity` | 运动的初速度 | 起步的动作更强烈 |

阻尼小则运动更「弹」；阻尼大则进入过阻尼状态，数值不经振荡就逼近目标。

## 自定义缓动函数 {#custom-easing-functions}

继承 `Easing` 并重写 `Ease` 方法，即可做出自定义缓动函数：

```csharp
using Avalonia.Animation.Easings;

public class StepEasing : Easing
{
    public int Steps { get; set; } = 4;

    public override double Ease(double progress)
    {
        return Math.Floor(progress * Steps) / Steps;
    }
}
```

在 XAML 中引用相应命名空间后即可使用这个自定义缓动：

```xml
<Animation Duration="0:0:1">
    <Animation.Easing>
        <local:StepEasing Steps="8" />
    </Animation.Easing>
    <!-- keyframes -->
</Animation>
```

`Ease` 方法接收一个 0.0 到 1.0 的 `progress` 值，表示线性的时间进度，并返回修正后的值（通常也在 0.0 到 1.0 之间，不过像 `BackEaseOut` 和 `ElasticEaseOut` 这类效果是允许冲出这个范围的）。

## 另请参阅 {#see-also}

- [关键帧动画](/docs/graphics-animation/keyframe-animations)：在动画中使用关键帧和缓动。
- [控件过渡](/docs/graphics-animation/control-transitions)：属性变化时的自动过渡。
- [动画设置](/docs/graphics-animation/animation-settings)：时长、延迟、重复次数与播放方向。
