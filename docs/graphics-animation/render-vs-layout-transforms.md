---
id: render-vs-layout-transforms
title: 渲染变换与布局变换
description: Avalonia 中渲染变换与布局变换的区别。
doc-type: explanation
---

Avalonia 提供两种变换控件的方式：渲染变换和布局变换。二者作用于渲染管线的不同阶段，因此视觉效果也不一样。

## 渲染变换 {#render-transforms}

**渲染变换**只改变控件的绘制方式，不影响布局。控件在布局系统中的位置和尺寸保持不变，其他控件也不会为了迁就这个变换而挪位置。

```xml
<StackPanel Spacing="8">
    <Button Content="Normal" />
    <Button Content="Rotated (render)">
        <Button.RenderTransform>
            <RotateTransform Angle="15" />
        </Button.RenderTransform>
    </Button>
    <Button Content="Below" />
</StackPanel>
```

在这个例子里，旋转后的按钮在视觉上压住了相邻按钮，因为布局并没有把旋转算进去。

### RenderTransformOrigin

渲染变换的轴心点。在 Avalonia 中默认是 `50%,50%`（控件中心），这一点与 WPF 不同——WPF 的默认值是 `0%,0%`（左上角）。

```xml
<!-- Rotate around the top-left corner -->
<Border RenderTransformOrigin="0%,0%">
    <Border.RenderTransform>
        <RotateTransform Angle="45" />
    </Border.RenderTransform>
</Border>

<!-- Rotate around the center (default) -->
<Border>
    <Border.RenderTransform>
        <RotateTransform Angle="45" />
    </Border.RenderTransform>
</Border>
```

### 常见的渲染变换类型 {#common-render-transform-types}

| 变换 | 说明 | 示例 |
|---|---|---|
| `RotateTransform` | 旋转控件。 | `<RotateTransform Angle="45" />` |
| `ScaleTransform` | 缩放控件。 | `<ScaleTransform ScaleX="1.5" ScaleY="1.5" />` |
| `TranslateTransform` | 在视觉上平移控件。 | `<TranslateTransform X="10" Y="-5" />` |
| `SkewTransform` | 倾斜控件。 | `<SkewTransform AngleX="15" />` |
| `TransformGroup` | 把多个变换组合起来。 | 见下文。 |

### 组合多个变换 {#combining-transforms}

```xml
<Image Source="/assets/photo.jpg" Width="100" Height="100">
    <Image.RenderTransform>
        <TransformGroup>
            <ScaleTransform ScaleX="1.2" ScaleY="1.2" />
            <RotateTransform Angle="10" />
        </TransformGroup>
    </Image.RenderTransform>
</Image>
```

## 布局变换 {#layout-transforms}

**布局变换**在布局发生之前就改变了控件的尺寸和朝向。父面板看到的是变换之后的尺寸，并据此摆放其他控件，因此不会出现重叠。

用 `LayoutTransformControl` 来施加布局变换：

```xml
<StackPanel Spacing="8">
    <Button Content="Normal" />
    <LayoutTransformControl>
        <LayoutTransformControl.LayoutTransform>
            <RotateTransform Angle="15" />
        </LayoutTransformControl.LayoutTransform>
        <Button Content="Rotated (layout)" />
    </LayoutTransformControl>
    <Button Content="Below (properly positioned)" />
</StackPanel>
```

「Below」按钮被摆在旋转后控件的完整边界之下，二者毫无重叠。

### 布局变换的常见用途 {#common-layout-transform-use-cases}

| 场景 | 为什么要用布局变换 |
|---|---|
| 竖排文字标签 | 旋转后的文字应当占住正确大小的空间。 |
| 经过缩放的内容区 | 相邻面板应当适应缩放后的尺寸。 |
| 旋转过的表单字段 | 标签和输入框应当绕着旋转后的元素排布。 |

```xml
<!-- Vertical text that takes correct space in a horizontal layout -->
<StackPanel Orientation="Horizontal" Spacing="8">
    <LayoutTransformControl>
        <LayoutTransformControl.LayoutTransform>
            <RotateTransform Angle="-90" />
        </LayoutTransformControl.LayoutTransform>
        <TextBlock Text="Vertical Label" />
    </LayoutTransformControl>
    <Border Background="LightBlue" Width="200" Height="100">
        <TextBlock Text="Content area" VerticalAlignment="Center"
                   HorizontalAlignment="Center" />
    </Border>
</StackPanel>
```

## Comparison

| 特性 | Render Transform | Layout Transform |
|---|---|---|
| 是否影响布局 | No | Yes |
| 其他控件会跟着调整 | No | Yes |
| 性能 | 较快（无需重新布局） | 较慢（会触发布局过程） |
| Animatable | Yes | 可以，但每一帧都会引发布局重算 |
| 施加方式 | `RenderTransform` property | `LayoutTransformControl` |
| 默认原点 | Center (50%, 50%) | Center |
| 重叠风险 | Yes | No |

## When to use which

**Use render transforms when:**
- The transform is temporary or animated (hover effects, transitions)
- Performance matters (animations should not trigger layout)
- Overlap with other elements is acceptable or desired
- You are creating visual effects (parallax, bounce, shake)

**Use layout transforms when:**
- Adjacent controls must respect the transformed bounds
- You need rotated text labels that correctly reserve space
- The transform is part of the permanent layout (not animated)
- Overlap would be a visual bug

## Animating transforms

Render transforms are ideal for animation because they do not trigger layout:

```xml
<Border Background="Blue" Width="80" Height="80">
    <Border.Styles>
        <Style Selector="Border:pointerover">
            <Style.Animations>
                <Animation Duration="0:0:0.2">
                    <KeyFrame Cue="100%">
                        <Setter Property="ScaleTransform.ScaleX" Value="1.1" />
                        <Setter Property="ScaleTransform.ScaleY" Value="1.1" />
                    </KeyFrame>
                </Animation>
            </Style.Animations>
        </Style>
    </Border.Styles>
</Border>
```

Avoid animating layout transforms in performance-sensitive scenarios, as each frame triggers a full layout pass.

## 另请参阅 {#see-also}

- [Transforms](/docs/graphics-animation/transforms): Full transform reference.
- [Animations](/docs/graphics-animation/animations): Keyframe and transition animations.
- [Performance](/docs/app-development/performance): Layout performance tips.
