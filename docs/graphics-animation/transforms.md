---
id: transforms
title: 变换
description: 用渲染变换和布局变换改变位置、尺寸、旋转与倾斜。
doc-type: explanation
---

变换可以改变视觉元素的位置、尺寸、旋转或倾斜，而不改动它们的布局。Avalonia 既支持渲染变换（在布局之后施加），也支持布局变换（通过 [`LayoutTransformControl`](/api/avalonia/controls/layouttransformcontrol) 在布局过程中施加）。

## RenderTransform

每个 `Visual` 元素都有 `RenderTransform` 属性。它在布局算完之后才施加变换，因此不会影响相邻控件的尺寸和位置。

```xml
<Button Content="Rotated" RenderTransformOrigin="50%,50%">
    <Button.RenderTransform>
        <RotateTransform Angle="15" />
    </Button.RenderTransform>
</Button>
```

### RenderTransformOrigin

`RenderTransformOrigin` 属性用相对坐标定义变换绕之进行的那个点，默认为 `50%,50%`（元素中心）。

```xml
<Image Source="avares://MyApp/Assets/logo.png"
       RenderTransformOrigin="50%,50%">
    <Image.RenderTransform>
        <ScaleTransform ScaleX="1.5" ScaleY="1.5" />
    </Image.RenderTransform>
</Image>
```

## 变换类型 {#transform-types}

### RotateTransform

按指定角度（单位为度）旋转元素。

| 属性 | 说明 |
|---|---|
| `Angle` | 旋转角度，单位为度。正值表示顺时针旋转。 |
| `CenterX`, `CenterY` | 相对 `RenderTransformOrigin` 的额外偏移量，用于确定旋转中心，单位为设备无关像素，默认为 0。 |

```xml
<Border Width="100" Height="100" Background="SteelBlue"
        RenderTransformOrigin="50%,50%">
    <Border.RenderTransform>
        <RotateTransform Angle="45" />
    </Border.RenderTransform>
</Border>
```

### ScaleTransform

在水平、垂直或两个方向上缩放元素。

| 属性 | 说明 |
|---|---|
| `ScaleX` | 水平缩放系数。1.0 为原始大小，2.0 为两倍，0.5 为一半。 |
| `ScaleY` | 垂直缩放系数。 |

```xml
<!-- Double the width, keep the height -->
<TextBlock Text="Stretched" RenderTransformOrigin="50%,50%">
    <TextBlock.RenderTransform>
        <ScaleTransform ScaleX="2" ScaleY="1" />
    </TextBlock.RenderTransform>
</TextBlock>

<!-- Mirror horizontally -->
<Image Source="avares://MyApp/Assets/arrow.png">
    <Image.RenderTransform>
        <ScaleTransform ScaleX="-1" ScaleY="1" />
    </Image.RenderTransform>
</Image>
```

### SkewTransform

沿 X 轴或 Y 轴切变元素。

| 属性 | 说明 |
|---|---|
| `AngleX` | 水平倾斜角度，单位为度。 |
| `AngleY` | 垂直倾斜角度，单位为度。 |

```xml
<Border Width="100" Height="60" Background="Orange"
        RenderTransformOrigin="50%,50%">
    <Border.RenderTransform>
        <SkewTransform AngleX="20" />
    </Border.RenderTransform>
</Border>
```

### TranslateTransform

按指定偏移量移动元素，且不影响布局。

| 属性 | 说明 |
|---|---|
| `X` | 水平偏移量，单位为设备无关像素。 |
| `Y` | 垂直偏移量，单位为设备无关像素。 |

```xml
<TextBlock Text="Shifted" RenderTransformOrigin="50%,50%">
    <TextBlock.RenderTransform>
        <TranslateTransform X="20" Y="-10" />
    </TextBlock.RenderTransform>
</TextBlock>
```

### MatrixTransform

施加由 3x2 矩阵定义的任意二维仿射变换。

| 属性 | 说明 |
|---|---|
| `Matrix` | 格式为 `m11,m12,m21,m22,offsetX,offsetY` 的字符串。 |

```xml
<Border Width="80" Height="80" Background="Purple">
    <Border.RenderTransform>
        <MatrixTransform Matrix="1,0,0.5,1,0,0" />
    </Border.RenderTransform>
</Border>
```

单位矩阵是 `1,0,0,1,0,0`（不作任何变换）。

### TransformGroup

把多个变换合成一个，按书写顺序依次施加。

```xml
<Border Width="100" Height="60" Background="Teal"
        RenderTransformOrigin="50%,50%">
    <Border.RenderTransform>
        <TransformGroup>
            <ScaleTransform ScaleX="1.5" ScaleY="1.5" />
            <RotateTransform Angle="30" />
        </TransformGroup>
    </Border.RenderTransform>
</Border>
```

:::info
`TransformGroup` 中各变换的先后顺序很重要：先缩放后旋转与先旋转后缩放，结果并不相同。
:::

## 简写写法 {#shorthand-syntax}

Avalonia 为 `RenderTransform` 提供了一种类似 CSS 的简写：

```xml
<Border RenderTransform="rotate(45deg)" />
<Border RenderTransform="scale(2, 1)" />
<Border RenderTransform="translate(10px, 20px)" />
<Border RenderTransform="skew(15deg, 0deg)" />
```

多个变换可以串联书写：

```xml
<Border RenderTransform="scale(1.5) rotate(30deg)" />
```

## LayoutTransformControl

`RenderTransform` 不参与布局计算，也就是说相邻控件对这个变换一无所知。若你需要让变换参与布局（比如旋转侧边栏并让相邻内容随之调整），请把元素包进 `LayoutTransformControl`：

```xml
<LayoutTransformControl>
    <LayoutTransformControl.LayoutTransform>
        <RotateTransform Angle="90" />
    </LayoutTransformControl.LayoutTransform>
    <TextBlock Text="Vertical text" />
</LayoutTransformControl>
```

`LayoutTransformControl` 会在施加变换之后再测量和排列子元素，这样父面板就会按变换后的尺寸来分配空间。

## 为变换加动画 {#animating-transforms}

人们常用关键帧动画或过渡来为变换加动画。绑定变换属性即可做出平滑的旋转、缩放或位移效果。

```xml
<Border Width="80" Height="80" Background="Coral"
        RenderTransformOrigin="50%,50%">
    <Border.RenderTransform>
        <RotateTransform x:Name="MyRotation" Angle="0" />
    </Border.RenderTransform>
    <Border.Styles>
        <Style Selector="Border:pointerover">
            <Style.Animations>
                <Animation Duration="0:0:0.3">
                    <KeyFrame Cue="100%">
                        <Setter Property="RotateTransform.Angle" Value="90" />
                    </KeyFrame>
                </Animation>
            </Style.Animations>
        </Style>
    </Border.Styles>
</Border>
```

关于动画的更多内容，请参阅[关键帧动画](/docs/graphics-animation/keyframe-animations)和[控件过渡](/docs/graphics-animation/control-transitions)。

## 在代码中使用变换 {#transforms-in-code}

```csharp
var rotateTransform = new RotateTransform(45);
myBorder.RenderTransform = rotateTransform;
myBorder.RenderTransformOrigin = RelativePoint.Center;

// TransformGroup
var group = new TransformGroup();
group.Children.Add(new ScaleTransform(2, 2));
group.Children.Add(new RotateTransform(30));
myBorder.RenderTransform = group;

// Animate a transform property
rotateTransform.Angle = 90; // Immediate change
```

## 另请参阅 {#see-also}

- [关键帧动画](/docs/graphics-animation/keyframe-animations)：让变换随时间变化。
- [控件过渡](/docs/graphics-animation/control-transitions)：在属性值变化时施加过渡。
- [绘制图形](/docs/graphics-animation/drawing-graphics)：形状与几何。
