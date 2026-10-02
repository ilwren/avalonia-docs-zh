---
id: control-transitions
title: 设置控件过渡
description: 配置过渡，为 Avalonia 控件的属性变化加上动画。
doc-type: how-to
---

Avalonia 的过渡同样深受 CSS Animations 的启发。它们监听目标属性值的变化，并按设定的参数为这次变化加上动画。任何 `Control` 都能通过 [`Transitions`](/api/avalonia/animation/transitions) 属性定义过渡。

:::note
与[关键帧动画](/docs/graphics-animation/keyframe-animations)不同，过渡在控件被隐藏时不会暂停。
:::

## 基本用法 {#basic-usage}

```xml
<Window xmlns="https://github.com/avaloniaui">
    <Window.Styles>
        <Style Selector="Rectangle.red">
            <Setter Property="Height" Value="100"/>
            <Setter Property="Width" Value="100"/>
            <Setter Property="Fill" Value="Red"/>
            <Setter Property="Opacity" Value="0.5"/>
        </Style>
        <Style Selector="Rectangle.red:pointerover">
            <Setter Property="Opacity" Value="1"/>
        </Style>
    </Window.Styles>

    <Rectangle Classes="red">
        <Rectangle.Transitions>
            <Transitions>
                <DoubleTransition Property="Opacity" Duration="0:0:0.2"/>
            </Transitions>
        </Rectangle.Transitions>
    </Rectangle>

</Window>
```

上面的例子会监听 `Rectangle` 的 `Opacity` 属性：一旦取值变化，就用 2 秒钟从旧值平滑过渡到新值。

过渡也可以写在任意样式里：用一个 `Setter` 以 `Transitions` 为目标属性，并把过渡装进一个 `Transitions` 对象中，像这样：

```xml
<Window xmlns="https://github.com/avaloniaui">
    <Window.Styles>
        <Style Selector="Rectangle.red">
            <Setter Property="Height" Value="100"/>
            <Setter Property="Width" Value="100"/>
            <Setter Property="Fill" Value="Red"/>
            <Setter Property="Opacity" Value="0.5"/>
            <Setter Property="Transitions">
                <Transitions>
                    <DoubleTransition Property="Opacity" Duration="0:0:0.2"/>
                </Transitions>
            </Setter>
        </Style>
        <Style Selector="Rectangle.red:pointerover">
            <Setter Property="Opacity" Value="1"/>
        </Style>
    </Window.Styles>

    <Rectangle Classes="red"/>

</Window>
```

每个过渡都有 `Property`、`Delay`、`Duration` 三项，外加一个可选的 `Easing` 属性。

`Property` 指的是过渡要监听并施加动画的目标属性。

`Delay` 指的是过渡施加到目标上之前要等多久。

`Duration` 指的是过渡播放的时长。

完整的缓动函数清单请参阅[缓动函数页面](/docs/graphics-animation/easing-functions)。

被动画的属性是什么类型，就必须用对应类型的过渡：

| 过渡动画 | 属性类型 |
|---|---|
| `BoolTransition` | `bool` |
| `BoxShadowsTransition` | `BoxShadows` |
| `BrushTransition` | `IBrush` |
| `ColorTransition` | `Color` |
| `CornerRadiusTransition` | `CornerRadius` |
| `DoubleTransition` | `double` |
| `FloatTransition` | `float` |
| `IntegerTransition` | `int` |
| `PointTransition` | `Point` |
| `SizeTransition` | `Size` |
| `ThicknessTransition` | `Thickness` |
| `TransformOperationsTransition` | `ITransform` |
| `VectorTransition` | `Vector` |

## 为渲染变换加过渡 {#transitioning-render-transforms}

用类 CSS 语法施加在控件上的渲染变换是可以加过渡的。下面的例子展示了一个边框，指针悬停在它上面时它会旋转 45 度：

```xml title='XAML'
<Border Width="100" Height="100" Background="Red">
    <Border.Styles>
        <Style Selector="Border">
            <Setter Property="RenderTransform" Value="rotate(0)"/>
        </Style>
        <Style Selector="Border:pointerover">
            <Setter Property="RenderTransform" Value="rotate(45deg)"/>
        </Style>
    </Border.Styles>
    <Border.Transitions>
        <Transitions>
            <TransformOperationsTransition Property="RenderTransform" Duration="0:0:1"/>
        </Transitions>
    </Border.Transitions>
</Border>
```

```csharp title='C#'
new Border
{
    Width = 100,
    Height = 100,
    Background = Brushes.Red,
    Styles =
    {
        new Style(x => x.OfType<Border>())
        {
            Setters =
            {
                new Setter(
                    Border.RenderTransformProperty,
                    TransformOperations.Parse("rotate(0)"))
            },
        },
        new Style(x => x.OfType<Border>().Class(":pointerover"))
        {
            Setters =
            {
                new Setter(
                    Border.RenderTransformProperty,
                    TransformOperations.Parse("rotate(45deg)"))
            },
        },
    },
    Transitions = new Transitions
    {
        new TransformOperationsTransition
        {
            Property = Border.RenderTransformProperty,
            Duration = TimeSpan.FromSeconds(1),
        }
    }
};
```

可用的过渡有：

| 过渡动画   | 示例                                    | 可用单位             |
| ------------ | ----------------------------------------- | ---------------------------- |
| `translate`  | `translate(10px)`, `translate(0px, 10px)` | `px`                         |
| `translateX` | `translateX(10px)`                        | `px`                         |
| `translateY` | `translateY(10px)`                        | `px`                         |
| `scale`      | `scale(10)`, `scale(0, 10)`               |                              |
| `scaleX`     | `scaleX(10)`                              |                              |
| `scaleY`     | `scaleY(10)`                              |                              |
| `skew`       | `skew(90deg)`, `skew(0, 90deg)`           | `deg`, `grad`, `rad`, `turn` |
| `skewX`      | `skewX(90deg)`                            | `deg`, `grad`, `rad`, `turn` |
| `skewY`      | `skewY(90deg)`                            | `deg`, `grad`, `rad`, `turn` |
| `rotate`     | `rotate(90deg)`                           | `deg`, `grad`, `rad`, `turn` |
| `matrix`     | `matrix(1,2,3,4,5,6)`                     |                              |

:::info
Avalonia 也支持 `RotateTransform`、`ScaleTransform` 这类 WPF 风格的渲染变换，但它们没法加过渡。若想给渲染变换加过渡，请一律使用类 CSS 的写法。
:::

## 另请参阅 {#see-also}

- [关键帧动画](/docs/graphics-animation/keyframe-animations)：多步关键帧动画。
- [动画设置](/docs/graphics-animation/animation-settings)：时长、延迟、重复次数与播放方向。
- [缓动函数](/docs/graphics-animation/easing-functions)：全部可用的缓动函数。
