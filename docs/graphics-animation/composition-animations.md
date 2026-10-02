---
id: composition-animations
title: 组合动画
description: 用 Avalonia 的组合动画 API 编写由代码驱动、跑在渲染线程上的动画。
doc-type: explanation
---

组合动画是一套由代码驱动、直接运行在渲染线程上的动画系统。它让你能精细地控制视觉属性，动画既顺滑又高性能，还不占用 UI 线程。

这套 API 与 UWP/WinUI 的 Composition 层相仿。当你需要编程控制动画、追求渲染线程级的性能，或者要动画化 XAML 关键帧动画搞不定的属性时，就用它。

## 何时该用组合动画 {#when-to-use-composition-animations}

| | Keyframe Animations | Control Transitions | Composition Animations |
|---|---|---|---|
| **定义位置** | XAML | XAML | C# 代码 |
| **触发方式** | 样式选择器 | 属性值变化 | `StartAnimation()` 或隐式的属性变化 |
| **运行线程** | UI 线程 | UI 线程 | 渲染线程 |
| **最适合** | 由样式驱动的多步动画 | 为属性变化提供顺滑反馈 | 对性能敏感、或需要编程控制的动画 |

有下列需求时请选择组合动画：

- 从代码中为视觉元素加动画（比如响应滚动位置、手势或数据变化）
- 让动画跑在渲染线程上，以求最佳顺滑度
- 使用基于表达式或基于物理的动画逻辑

至于由样式驱动的场景，[关键帧动画](/docs/graphics-animation/keyframe-animations)和[控件过渡](/docs/graphics-animation/control-transitions)更简单也更对路。

## 核心概念 {#core-concepts}

### CompositionVisual 与 Compositor {#compositionvisual-and-compositor}

每个 Avalonia 控件在渲染线程上都有一个对应的 [`CompositionVisual`](/api/avalonia/rendering/composition/compositionvisual)，用 `ElementComposition.GetElementVisual()` 即可取得：

```csharp
var visual = ElementComposition.GetElementVisual(myControl);
```

[`Compositor`](/api/avalonia/rendering/composition/compositor) 是用来创建动画和动画集合的工厂对象，从任意 `CompositionVisual` 都能取到它：

```csharp
var compositor = visual.Compositor;
```

所有动画对象都必须由目标视觉元素所关联的那个 `Compositor` 创建。

### Animatable Properties

`CompositionVisual` 上可以动画化的属性有：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Offset` | `Vector3D` | 该视觉元素在 X、Y、Z 方向上的位置偏移。 |
| `Opacity` | `float` | 该视觉元素的不透明度（0.0 到 1.0）。 |
| `Size` | `Vector` | 该视觉元素的宽和高。 |

## 显式动画 {#explicit-animations}

显式动画在你对某个视觉元素调用 `StartAnimation()` 时才运行。你自己定义关键帧、设定时长，并手动启动动画。

### 滑入示例 {#slide-in-example}

这个例子让控件在 400 毫秒内从左侧滑入：

```csharp
var visual = ElementComposition.GetElementVisual(myControl);
var compositor = visual.Compositor;

var animation = compositor.CreateVector3KeyFrameAnimation();
animation.Duration = TimeSpan.FromMilliseconds(400);
animation.InsertKeyFrame(0f, new Vector3D(-200, 0, 0));
animation.InsertKeyFrame(1f, new Vector3D(0, 0, 0));

visual.StartAnimation("Offset", animation);
```

关键帧的进度取值从 `0f`（起点）到 `1f`（终点）。要做多步动画，可以在 0 到 1 之间的任意位置插入中间关键帧。

### 淡入示例 {#fade-in-example}

```csharp
var visual = ElementComposition.GetElementVisual(myControl);
var compositor = visual.Compositor;

var animation = compositor.CreateScalarKeyFrameAnimation();
animation.Duration = TimeSpan.FromMilliseconds(300);
animation.InsertKeyFrame(0f, 0f);
animation.InsertKeyFrame(1f, 1f);

visual.StartAnimation("Opacity", animation);
```

## 隐式动画 {#implicit-animations}

隐式动画会在映射的属性发生变化时自动触发。你不必调用 `StartAnimation()`，只需给视觉元素赋一个 `ImplicitAnimationCollection`。此后只要其中某个被映射的属性一变，对应的动画就会跑起来。

### 平滑移位示例 {#smooth-repositioning-example}

这个例子让控件的 `Offset` 每次变化时，位置都平滑地动过去：

```csharp
var visual = ElementComposition.GetElementVisual(myControl);
var compositor = visual.Compositor;

var offsetAnimation = compositor.CreateVector3KeyFrameAnimation();
offsetAnimation.Duration = TimeSpan.FromMilliseconds(300);
offsetAnimation.Target = "Offset";
offsetAnimation.InsertExpressionKeyFrame(1f, "this.FinalValue");

var implicitAnimations = compositor.CreateImplicitAnimationCollection();
implicitAnimations["Offset"] = offsetAnimation;

visual.ImplicitAnimations = implicitAnimations;
```

表达式关键帧 `"this.FinalValue"` 告诉动画：从当前值插值到属性刚被设成的那个新值。于是无论起止位置具体是多少，这段动画都能复用。

同一个集合里可以映射多个属性：

```csharp
var opacityAnimation = compositor.CreateScalarKeyFrameAnimation();
opacityAnimation.Duration = TimeSpan.FromMilliseconds(200);
opacityAnimation.Target = "Opacity";
opacityAnimation.InsertExpressionKeyFrame(1f, "this.FinalValue");

implicitAnimations["Opacity"] = opacityAnimation;
```

## 借附加属性在 XAML 中使用 {#integrating-with-xaml-via-attached-properties}

想以声明方式使用组合动画，就把这套初始化逻辑包进一个附加属性里，这样你就能从 XAML 样式中施加组合行为。

### 附加属性 {#attached-property}

```csharp
public class CompositionAnimationHelper : AvaloniaObject
{
    public static readonly AttachedProperty<bool> SmoothOffsetProperty =
        AvaloniaProperty.RegisterAttached<CompositionAnimationHelper, Visual, bool>(
            "SmoothOffset");

    public static bool GetSmoothOffset(Visual element) =>
        element.GetValue(SmoothOffsetProperty);

    public static void SetSmoothOffset(Visual element, bool value) =>
        element.SetValue(SmoothOffsetProperty, value);

    static CompositionAnimationHelper()
    {
        SmoothOffsetProperty.Changed.AddClassHandler<Visual>((element, args) =>
        {
            if (args.NewValue is true)
            {
                element.AttachedToVisualTree += (_, _) =>
                {
                    var visual = ElementComposition.GetElementVisual(element);
                    if (visual == null) return;
                    var compositor = visual.Compositor;

                    var animation = compositor.CreateVector3KeyFrameAnimation();
                    animation.Duration = TimeSpan.FromMilliseconds(300);
                    animation.Target = "Offset";
                    animation.InsertExpressionKeyFrame(1f, "this.FinalValue");

                    var implicit = compositor.CreateImplicitAnimationCollection();
                    implicit["Offset"] = animation;
                    visual.ImplicitAnimations = implicit;
                };
            }
        });
    }
}
```

### XAML 用法 {#xaml-usage}

```xml
<Style Selector="ListBoxItem">
    <Setter Property="local:CompositionAnimationHelper.SmoothOffset" Value="True" />
</Style>
```

如此一来，每当列表重排或增删项时，每个 `ListBoxItem` 都会平滑地动到新位置。

## API 参考 {#api-reference}

| Type / Member | 说明 |
|---|---|
| `ElementComposition.GetElementVisual(Visual)` | 返回某个控件的 `CompositionVisual`。 |
| `CompositionVisual` | 表示某个控件在渲染线程上的视觉元素。 |
| `Compositor` | 创建动画对象和集合对象的工厂。 |
| `CreateScalarKeyFrameAnimation()` | 为 `float` 类型的属性（比如 `Opacity`）创建动画。 |
| `CreateVector3KeyFrameAnimation()` | 为 `Vector3D` 类型的属性（比如 `Offset`）创建动画。 |
| `InsertKeyFrame(float progress, T value)` | 在指定进度（0.0 到 1.0）处添加一个关键帧。 |
| `InsertExpressionKeyFrame(float progress, string expression)` | 添加一个基于表达式的关键帧（比如 `"this.FinalValue"`）。 |
| `StartAnimation(string property, CompositionAnimation animation)` | 在指定名称的属性上启动一段显式动画。 |
| `ImplicitAnimationCollection` | 把属性名映射到动画，属性一变就自动播放。 |
| `CompositionVisual.ImplicitAnimations` | 获取或设置某个视觉元素的隐式动画集合。 |

## 另请参阅 {#see-also}

- [Keyframe Animations](/docs/graphics-animation/keyframe-animations)
- [Control Transitions](/docs/graphics-animation/control-transitions)
- [Custom Rendering](/docs/graphics-animation/custom-rendering)
