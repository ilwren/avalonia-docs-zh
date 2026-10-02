---
id: effects
title: 效果
description: Avalonia 控件可用的视觉效果：盒阴影、裁剪与不透明度遮罩。
doc-type: explanation
---

Avalonia 支持各种视觉效果，为控件增添层次感和观赏性。主要有三类：盒阴影、裁剪和不透明度遮罩。

## 阴影 {#box-shadows}

[`Border`](/api/avalonia/controls/border) 和 `ContentPresenter` 上的 [`BoxShadow`](/api/avalonia/media/boxshadow) 属性可为元素添加投影或内阴影，语法沿用 CSS box-shadow 的那一套。

### 基本语法 {#basic-syntax}

```xml
<Border BoxShadow="5 5 10 0 #80000000" CornerRadius="8"
        Background="White" Padding="20">
    <TextBlock Text="Shadow" />
</Border>
```

阴影的各项参数依次为：`offsetX offsetY blur spread color`。

| 参数 | 说明 |
|---|---|
| `offsetX` | 水平偏移，正值把阴影往右推。 |
| `offsetY` | 垂直偏移，正值把阴影往下推。 |
| `blur` | 模糊半径，值越大阴影越柔和，不能为负。 |
| `spread` | 扩散半径，正值让阴影变大，负值让它收缩。 |
| `color` | 阴影颜色。十六进制值（`#80000000`）、具名颜色（`Gray`）和颜色函数（`rgba(0,0,0,0.5)`、`hsla(0,0%,0%,0.3)`）都认。 |

### 在阴影中使用颜色函数 {#color-functions-in-shadows}

带逗号的颜色函数（比如 `rgba()` 和 `hsla()`）完全可用，在多重阴影定义中也不例外：

```xml
<Border BoxShadow="0 4 8 0 rgba(0,0,0,0.3), 0 2 4 0 rgba(0,0,0,0.1)"
        CornerRadius="8" Background="White" Padding="20">
    <TextBlock Text="RGBA shadows" />
</Border>
```

### 内阴影 {#inset-shadows}

在阴影定义前加上 `inset`，阴影就画在元素内部：

```xml
<Border BoxShadow="inset 0 2 4 0 #40000000" CornerRadius="8"
        Background="#F0F0F0" Padding="20">
    <TextBlock Text="Inset shadow" />
</Border>
```

### 多重阴影 {#multiple-shadows}

多条阴影定义之间用逗号分隔：

```xml
<Border BoxShadow="0 2 4 0 #20000000, 0 8 16 0 #10000000"
        CornerRadius="12" Background="White" Padding="24">
    <TextBlock Text="Layered shadows" />
</Border>
```

### 常见的阴影写法 {#common-shadow-patterns}

```xml
<!-- Subtle elevation -->
<Border BoxShadow="0 1 3 0 #20000000" />

<!-- Medium elevation -->
<Border BoxShadow="0 4 6 -1 #20000000, 0 2 4 -2 #20000000" />

<!-- High elevation -->
<Border BoxShadow="0 10 15 -3 #20000000, 0 4 6 -4 #20000000" />

<!-- Glow effect -->
<Border BoxShadow="0 0 20 5 #4060A0FF" />

<!-- Inset pressed effect -->
<Border BoxShadow="inset 0 2 4 0 #40000000" />
```

### 在代码中使用盒阴影 {#box-shadows-in-code}

```csharp
myBorder.BoxShadow = BoxShadows.Parse("0 4 8 0 #40000000");
```

## BlurEffect

任意 `Visual` 上的 [`Effect`](/api/avalonia/media/effect) 属性都接受效果对象。`BlurEffect` 会给整个元素施加高斯模糊：

```xml
<Border Background="SteelBlue" Padding="20" CornerRadius="8">
    <Border.Effect>
        <BlurEffect Radius="10" />
    </Border.Effect>
    <TextBlock Text="Blurred content" Foreground="White" />
</Border>
```

| 属性 | 说明 |
|---|---|
| `Radius` | 模糊半径，单位为像素。值越大模糊越强，默认为 5。 |

## DropShadowEffect

`DropShadowEffect` 借助 `Effect` 属性在整个视觉元素背后加一层阴影。这与 `BoxShadow` 不同——后者只作用于 `Border` 元素。

```xml
<TextBlock Text="Shadow Text" FontSize="24">
    <TextBlock.Effect>
        <DropShadowEffect OffsetX="3" OffsetY="3"
                          BlurRadius="5" Color="Black" Opacity="0.5" />
    </TextBlock.Effect>
</TextBlock>
```

| 属性 | 说明 |
|---|---|
| `OffsetX` | 阴影的水平偏移，单位为像素，默认约 3.5。 |
| `OffsetY` | 阴影的垂直偏移，单位为像素，默认约 3.5。 |
| `BlurRadius` | 阴影的模糊半径，默认为 5。 |
| `Color` | 阴影颜色，默认为 `Black`。 |
| `Opacity` | 阴影不透明度，取值 0.0 到 1.0，默认为 1.0。 |

### DropShadowDirectionEffect

另一种写法：用方向和距离代替显式偏移量：

```xml
<Border Background="White" Padding="20" CornerRadius="8">
    <Border.Effect>
        <DropShadowDirectionEffect ShadowDepth="5" Direction="315"
                                    BlurRadius="10" Color="Black" Opacity="0.3" />
    </Border.Effect>
    <TextBlock Text="Directional shadow" />
</Border>
```

| 属性 | 说明 |
|---|---|
| `ShadowDepth` | 阴影与元素之间的距离，默认为 5。 |
| `Direction` | 表示阴影方向的角度（0–360 度），默认为 315（右下方）。 |
| `BlurRadius` | 阴影的模糊半径，默认为 5。 |
| `Color` | 阴影颜色，默认为 `Black`。 |
| `Opacity` | 阴影不透明度，默认为 1.0。 |

:::info
`Effect`（BlurEffect、DropShadowEffect）适用于任意视觉元素，文字和图片也包括在内；`BoxShadow` 只能用在 `Border` 和 `ContentPresenter` 控件上，但画矩形阴影时性能更好。
:::

## Clipping

任意控件上的 `ClipToBounds` 属性都会裁掉超出元素边界的子内容。

```xml
<Border Width="100" Height="100" ClipToBounds="True" CornerRadius="50">
    <Image Source="avares://MyApp/Assets/photo.png"
           Stretch="UniformToFill" />
</Border>
```

这会裁出圆角边框的形状，从而做出圆形图片。

### Clip 属性 {#clip-property}

要自定义裁剪形状，请配合 `Geometry` 使用 `Clip` 属性：

```xml
<Image Source="avares://MyApp/Assets/photo.png" Width="200" Height="200">
    <Image.Clip>
        <EllipseGeometry Rect="0,0,200,200" />
    </Image.Clip>
</Image>
```

任何几何类型都能用来裁剪：

```xml
<Image Source="avares://MyApp/Assets/photo.png" Width="200" Height="200">
    <Image.Clip>
        <PathGeometry>
            <PathFigure StartPoint="100,0" IsClosed="True">
                <LineSegment Point="200,80" />
                <LineSegment Point="160,200" />
                <LineSegment Point="40,200" />
                <LineSegment Point="0,80" />
            </PathFigure>
        </PathGeometry>
    </Image.Clip>
</Image>
```

## OpacityMask

`OpacityMask` 属性用一个画刷逐像素控制透明度，只有遮罩画刷的 alpha 通道起作用：黑色区域完全可见，透明区域则被隐去。

```xml
<!-- Fade from top to bottom -->
<Image Source="avares://MyApp/Assets/photo.png" Width="200" Height="200">
    <Image.OpacityMask>
        <LinearGradientBrush StartPoint="0%,0%" EndPoint="0%,100%">
            <GradientStop Color="Black" Offset="0" />
            <GradientStop Color="Black" Offset="0.5" />
            <GradientStop Color="Transparent" Offset="1" />
        </LinearGradientBrush>
    </Image.OpacityMask>
</Image>
```

### 径向淡出 {#radial-fade}

```xml
<Border Width="200" Height="200" Background="SteelBlue">
    <Border.OpacityMask>
        <RadialGradientBrush>
            <GradientStop Color="Black" Offset="0" />
            <GradientStop Color="Transparent" Offset="1" />
        </RadialGradientBrush>
    </Border.OpacityMask>
</Border>
```

## Opacity

任意 `Visual` 上的 `Opacity` 属性控制该元素及其全部子元素的整体透明度：

```xml
<Border Opacity="0.5" Background="Red" Padding="20">
    <TextBlock Text="Semi-transparent" />
</Border>
```

取值从 `0.0`（完全透明）到 `1.0`（完全不透明）。与 `OpacityMask` 不同，它对整个元素一视同仁。

### IsVisible 与 Opacity 的区别 {#isvisible-vs-opacity}

| 办法 | 对布局的影响 | 交互 | 动画 |
| --- | --- | --- | --- |
| `IsVisible="False"` | 元素被移出布局。 | 无法接收输入。 | [关键帧动画](/docs/graphics-animation/keyframe-animations)默认暂停。 |
| `Opacity="0"` | 元素依然占着位置。 | 仍可接收指针和键盘输入。 | [关键帧动画](/docs/graphics-animation/keyframe-animations)继续播放。 |

## 为效果加动画 {#animating-effects}

盒阴影和不透明度都可以用过渡来加动画：

```xml
<Border Background="White" CornerRadius="8" Padding="20"
        BoxShadow="0 2 4 0 #20000000">
    <Border.Transitions>
        <Transitions>
            <BoxShadowsTransition Property="BoxShadow" Duration="0:0:0.2" />
            <DoubleTransition Property="Opacity" Duration="0:0:0.2" />
        </Transitions>
    </Border.Transitions>
    <Border.Styles>
        <Style Selector="Border:pointerover">
            <Setter Property="BoxShadow" Value="0 8 16 0 #30000000" />
        </Style>
    </Border.Styles>
    <TextBlock Text="Hover for shadow" />
</Border>
```

## 另请参阅 {#see-also}

- [画刷](/docs/graphics-animation/brushes)：全部画刷类型，渐变画刷和图片画刷也包括在内。
- [绘制图形](/docs/graphics-animation/drawing-graphics)：形状、几何与路径数据。
- [变换](/docs/graphics-animation/transforms)：元素的旋转、缩放、倾斜与平移。
- [控件过渡](/docs/graphics-animation/control-transitions)：为属性变化加动画。
