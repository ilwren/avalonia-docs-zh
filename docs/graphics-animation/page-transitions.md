---
id: page-transitions
title: 设置页面过渡
description: 在 Avalonia 中用 CrossFade、PageSlide、CompositePageTransition 或自定义过渡，为视图之间的切换加动画。
doc-type: how-to
---

import CustomPageTransitionScreenshot from '/img/guides/ui-development/graphics/custom-page-transition.webp';

页面过渡为两个视图之间的切换加动画，通常与 `TransitioningContentControl`、`Carousel` 这类控件搭配使用。Avalonia 提供两种内置过渡，也支持把它们组合起来或自己写一个。

要指定过渡，在宿主控件上设置 `PageTransition` 属性：

```xml title='XAML'
<TransitioningContentControl PageTransition="{StaticResource MyTransition}"
                              Content="{Binding CurrentPage}" />
```

## [`CrossFade`](/api/avalonia/animation/crossfade)

`CrossFade` 通过动画化不透明度，让当前视图淡出、新视图淡入。如果你想要一种含蓄、不带方向感、又对任何内容都适用的过渡，选它准没错。

```xml title='XAML'
<CrossFade Duration="0:00:00.500" />
```

```csharp title='C#'
var transition = new CrossFade(TimeSpan.FromMilliseconds(500));
```

:::tip
`CrossFade` 很适合标签页式的导航——那里本就没有天然的前后方向。若各视图高度相差悬殊，交叉淡入淡出还能避免滑动带来的突兀跳动。
:::

## [`PageSlide`](/api/avalonia/animation/pageslide)

`PageSlide` 让旧视图滑出、新视图滑入，`Orientation` 属性决定滑动的轴向（默认水平）。这种过渡传达出方向感，特别适合向导式流程或有先后次序的页面。

```xml title='XAML'
<PageSlide Duration="0:00:00.500" Orientation="Vertical" />
```

```csharp title='C#'
var transition = new PageSlide(TimeSpan.FromMilliseconds(500),
                                PageSlide.SlideAxis.Vertical);
```

:::tip
传给过渡的 `forward` 参数控制滑动方向。向后导航时（比如按下「返回」按钮），把这个参数设为 `false`，滑动方向就会自动反过来。
:::

## [`CompositePageTransition`](/api/avalonia/animation/compositepagetransition)

`CompositePageTransition` 把两种或更多过渡合成一个效果，各个子过渡并行播放。下面的例子让视图斜向滑动（水平和垂直滑动叠加），同时还做交叉淡入淡出：

```xml title='XAML'
<CompositePageTransition>
    <CrossFade Duration="0:00:00.500" />
    <PageSlide Duration="0:00:00.500" Orientation="Horizontal" />
    <PageSlide Duration="0:00:00.500" Orientation="Vertical" />
</CompositePageTransition>
```

```csharp title='C#'
var transition = new CompositePageTransition();
transition.PageTransitions.Add(new CrossFade(TimeSpan.FromMilliseconds(500)));
transition.PageTransitions.Add(new PageSlide(TimeSpan.FromMilliseconds(500),
    PageSlide.SlideAxis.Horizontal));
transition.PageTransitions.Add(new PageSlide(TimeSpan.FromMilliseconds(500),
    PageSlide.SlideAxis.Vertical));
```

:::note
请让各个子过渡的 `Duration` 保持一致，好让它们同起同落。时长不一致可能导致一个过渡先结束而留下视觉瑕疵。
:::

## 怎么挑过渡 {#choosing-the-right-transition}

| 过渡动画 | 适用场景 | 注释支持情况 |
|---|---|---|
| `CrossFade` | 标签页、设置面板，以及就地变化的内容 | 含蓄、无方向感 |
| `PageSlide` (horizontal) | 向导步骤、前进/后退导航 | 传达出先后次序 |
| `PageSlide` (vertical) | 展开区块、逐层下钻导航 | 暗示层级关系 |
| `CompositePageTransition` | 丰富、有层次的效果 | 可任意组合上述几种 |

## 自定义页面过渡 {#custom-page-transitions}

当内置过渡都不合你的设计时，可以实现 `IPageTransition` 接口做一个自己的。这个接口只有一个方法：

```csharp title='C#'
public Task Start(Visual? from, Visual? to, bool forward,
                  CancellationToken cancellationToken)
{
    // Animate from the old view (from) to the new view (to).
}
```

`from` 和 `to` 参数都可能为 `null`（比如控件首次加载时就没有要退场的视图）。`forward` 参数表明导航方向，你可以据此反转自己的动画。请务必尊重 `cancellationToken`，好让用户在过渡结束前再次导航时，Avalonia 能取消这段过渡。

下面这个例子先把旧视图纵向压扁，再把新视图展开：

```csharp title='C#'
using Avalonia.VisualTree;

public class CustomTransition : IPageTransition
{
    public CustomTransition() { }

    public CustomTransition(TimeSpan duration)
    {
        Duration = duration;
    }

    public TimeSpan Duration { get; set; }

    public async Task Start(Visual from, Visual to, bool forward,
                            CancellationToken cancellationToken)
    {
        if (cancellationToken.IsCancellationRequested)
        {
            return;
        }

        var tasks = new List<Task>();
        var scaleYProperty = ScaleTransform.ScaleYProperty;

        if (from != null)
        {
            var animation = new Animation
            {
                FillMode = FillMode.Forward,
                Children =
                {
                    new KeyFrame
                    {
                        Setters = { new Setter { Property = scaleYProperty, Value = 1d } },
                        Cue = new Cue(0d)
                    },
                    new KeyFrame
                    {
                        Setters = { new Setter { Property = scaleYProperty, Value = 0d } },
                        Cue = new Cue(1d)
                    }
                },
                Duration = Duration
            };
            tasks.Add(animation.RunAsync(from, cancellationToken));
        }

        if (to != null)
        {
            to.IsVisible = true;
            var animation = new Animation
            {
                FillMode = FillMode.Forward,
                Children =
                {
                    new KeyFrame
                    {
                        Setters = { new Setter { Property = scaleYProperty, Value = 0d } },
                        Cue = new Cue(0d)
                    },
                    new KeyFrame
                    {
                        Setters = { new Setter { Property = scaleYProperty, Value = 1d } },
                        Cue = new Cue(1d)
                    }
                },
                Duration = Duration
            };
            tasks.Add(animation.RunAsync(to, cancellationToken));
        }

        await Task.WhenAll(tasks);

        if (from != null && !cancellationToken.IsCancellationRequested)
        {
            from.IsVisible = false;
        }
    }
}
```

<Image light={CustomPageTransitionScreenshot} alt="Animation showing a custom page transition that shrinks and expands views vertically" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [动画](/docs/graphics-animation/animations)：Avalonia 中各类动画概览。
- [关键帧动画](/docs/graphics-animation/keyframe-animations)：多步关键帧动画。
- [控件过渡](/docs/graphics-animation/control-transitions)：为属性变化加动画。
- [在视图之间导航](/docs/how-to/navigation-how-to)：切换视图的常见套路。
