---
id: animations
title: 动画
description: Avalonia 中各类动画概览：关键帧动画、过渡与组合动画。
doc-type: overview
---

import KeyframeDiagram from '/img/concepts/ui-concepts/animations/animation-keyframe.png';

Avalonia 提供三类动画：

| 类型 | 说明 | 适用场景 |
|---|---|---|
| [Keyframe Animations](/docs/graphics-animation/keyframe-animations) | 沿时间轴、借由多个关键帧改变一个或多个属性。 | 由样式选择器触发的复杂多步动画。 |
| [Control Transitions](/docs/graphics-animation/control-transitions) | 在某个属性的值发生变化时为它加动画。 | 为属性变化（不透明度、颜色、尺寸）提供顺滑的视觉反馈。 |
| [Composition Animations](/docs/graphics-animation/composition-animations) | 由代码驱动、运行在渲染线程上的动画。 | 对性能敏感、或需要从 C# 中编程控制的动画。 |

此外，[页面过渡](/docs/graphics-animation/page-transitions)负责为 `TransitioningContentControl`、`Carousel` 等控件的内容切换加动画。

## 关键帧动画 {#keyframe-animations}

最简单的关键帧动画，就是定义起点（0%）和终点（100%）两个关键帧，让某个属性值在指定时长内完成变化。

<Image light={KeyframeDiagram} alt="Diagram showing a keyframe animation timeline with start and end cue points" position="center" maxWidth={400} cornerRadius="true"/>

两个关键帧之间的属性值由缓动函数插值得出，默认是线性插值。

### 快速示例 {#quick-example}

```xml
<Border Background="Blue" Width="100" Height="100">
    <Border.Styles>
        <Style Selector="Border">
            <Style.Animations>
                <Animation Duration="0:0:1" IterationCount="INFINITE"
                           PlaybackDirection="Alternate">
                    <KeyFrame Cue="0%">
                        <Setter Property="Opacity" Value="1.0" />
                    </KeyFrame>
                    <KeyFrame Cue="100%">
                        <Setter Property="Opacity" Value="0.3" />
                    </KeyFrame>
                </Animation>
            </Style.Animations>
        </Style>
    </Border.Styles>
</Border>
```

这会做出一个永不停歇的呼吸式不透明度动画，在全不透明和半透明之间来回变化。

完整语法和更多示例请参阅[关键帧动画](/docs/graphics-animation/keyframe-animations)。

## 控件过渡 {#control-transitions}

过渡会在属性值发生变化时自动为它加动画，无需手写关键帧就能获得顺滑的视觉反馈：

```xml
<Button Content="Hover me" Background="Blue">
    <Button.Transitions>
        <Transitions>
            <BrushTransition Property="Background" Duration="0:0:0.3" />
            <DoubleTransition Property="Opacity" Duration="0:0:0.2" />
        </Transitions>
    </Button.Transitions>
</Button>
```

过渡的种类和配置请参阅[控件过渡](/docs/graphics-animation/control-transitions)。

## 组合动画 {#composition-animations}

组合动画是一套更底层、由代码驱动、运行在渲染线程上的方案。当你需要编程控制、或追求渲染线程级的性能时就用它：

```csharp
var visual = ElementComposition.GetElementVisual(myControl);
var compositor = visual.Compositor;

var animation = compositor.CreateVector3KeyFrameAnimation();
animation.Duration = TimeSpan.FromMilliseconds(400);
animation.InsertKeyFrame(0f, new Vector3D(-200, 0, 0));
animation.InsertKeyFrame(1f, new Vector3D(0, 0, 0));

visual.StartAnimation("Offset", animation);
```

完整 API、隐式动画和集成方式请参阅[组合动画](/docs/graphics-animation/composition-animations)。

## 触发动画 {#triggering-animations}

在 XAML 中定义的关键帧动画，其触发行为取决于样式选择器：

- **无条件选择器**（比如 `Style Selector="Border"`）：控件进入视觉树时动画开始。
- **条件选择器**（比如 `Style Selector="Border:pointerover"`）：选择器条件成立时（比如指针悬停在边框上）动画播放，条件不再成立时停止。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <UserControl.Styles>
    <Style Selector="Border:pointerover">
      <Style.Animations>
        <Animation Duration="0:0:2">
            <KeyFrame Cue="100%">
                <Setter Property="ScaleTransform.ScaleX" Value="1.5" />
                <Setter Property="ScaleTransform.ScaleY" Value="1.5" />
            </KeyFrame>
        </Animation>
      </Style.Animations>
    </Style>
  </UserControl.Styles>

  <Border Width="100" Height="100" Background="blue" />
</UserControl>
```

</XamlPreview>

:::info
默认情况下，由样式施加的关键帧动画会在控件实际不可见时暂停，控件重新可见后恢复。参见[播放行为](/docs/graphics-animation/keyframe-animations#playback-behavior)。
:::

## 动画设置 {#animation-settings}

关键帧动画支持下列配置项：

| 设置项 | 说明 | 示例 |
|---|---|---|
| `Duration` | 一个周期要走多久。 | `0:0:1` (1 second) |
| `Delay` | 开始之前先等多久。 | `0:0:0.5` |
| `Easing` | 关键帧之间的插值曲线。 | `CubicEaseInOut` |
| `FillMode` | 动画结束时如何收场。 | `Forward`, `Backward`, `Both`, `None` |
| `IterationCount` | 重复播放的次数，填 `infinite` 表示永远循环。 | `3`, `INFINITE` |
| `PlaybackBehavior` | 控件被隐藏时是否暂停动画。 | `Normal`, `Reverse`, `Alternate`, `AlternateReverse` |
| `PlaybackDirection` | 播放方向。 | `Auto`, `Always`, `OnlyIfVisible` |

各个选项的详细说明请参阅[动画设置](/docs/graphics-animation/animation-settings)，全部可用的缓动类型请参阅[缓动函数](/docs/graphics-animation/easing-functions)。

## 另请参阅 {#see-also}

- [关键帧动画](/docs/graphics-animation/keyframe-animations)：完整的关键帧动画语法和示例。
- [控件过渡](/docs/graphics-animation/control-transitions)：为属性变化加动画。
- [组合动画](/docs/graphics-animation/composition-animations)：由代码驱动、跑在渲染线程上的动画。
- [页面过渡](/docs/graphics-animation/page-transitions)：为内容切换加动画。
