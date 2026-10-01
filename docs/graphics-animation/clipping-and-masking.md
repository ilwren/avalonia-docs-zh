---
id: clipping-and-masking
title: 裁剪与遮罩
description: 在 Avalonia 中用裁剪和遮罩手法限定内容的可见范围。
doc-type: explanation
---

裁剪把控件或绘制内容的可见区域限定在指定范围内；遮罩则借助不透明度渐变让内容部分隐去。要做异形控件、圆形头像和各类视觉效果，这两招都很好用。

## ClipToBounds

最简单的裁剪，是把子内容限制在父级边界之内。在任意控件上设置 `ClipToBounds="True"` 即可：

```xml
<Border Width="100" Height="100" ClipToBounds="True"
        Background="LightGray">
    <!-- This image extends beyond the border but is clipped -->
    <Image Source="/assets/photo.jpg" Width="200" Height="200" />
</Border>
```

`ClipToBounds` 默认为 `false`，因此内容可以溢出父级。

## Clip 属性 {#clip-property}

`Clip` 属性接受任意 `Geometry`，用来定义非矩形的裁剪区域。

### 圆形裁剪 {#circular-clip}

用椭圆裁剪图片，做出圆形头像：

```xml
<Image Source="/assets/avatar.jpg" Width="100" Height="100"
       Stretch="UniformToFill">
    <Image.Clip>
        <EllipseGeometry Rect="0,0,100,100" />
    </Image.Clip>
</Image>
```

### 圆角矩形裁剪 {#rounded-rectangle-clip}

```xml
<Image Source="/assets/banner.jpg" Width="300" Height="200"
       Stretch="UniformToFill">
    <Image.Clip>
        <RectangleGeometry Rect="0,0,300,200" RadiusX="16" RadiusY="16" />
    </Image.Clip>
</Image>
```

### 自定义形状裁剪 {#custom-shape-clip}

任意形状请用 `PathGeometry`：

```xml
<Image Source="/assets/photo.jpg" Width="200" Height="200"
       Stretch="UniformToFill">
    <Image.Clip>
        <PathGeometry>
            <PathFigure StartPoint="100,0" IsClosed="True">
                <LineSegment Point="200,75" />
                <LineSegment Point="160,200" />
                <LineSegment Point="40,200" />
                <LineSegment Point="0,75" />
            </PathFigure>
        </PathGeometry>
    </Image.Clip>
</Image>
```

### 使用流式几何语法 {#using-stream-geometry-syntax}

那套紧凑的路径迷你语言同样可以用来定义裁剪区域：

```xml
<Image Source="/assets/photo.jpg" Width="200" Height="200">
    <Image.Clip>
        <StreamGeometry>M 100,0 L 200,75 160,200 40,200 0,75 Z</StreamGeometry>
    </Image.Clip>
</Image>
```

## 借 CornerRadius 实现裁剪 {#clipping-with-cornerradius}

`Border` 通过 `CornerRadius` 自带裁剪能力：圆角边框内的内容会被自动裁剪：

```xml
<Border CornerRadius="50" Width="100" Height="100" ClipToBounds="True">
    <Image Source="/assets/avatar.jpg" Stretch="UniformToFill" />
</Border>
```

要做圆形图片，这往往比用 `EllipseGeometry` 裁剪更省事。

## 不透明度遮罩 {#opacity-masking}

用 `OpacityMask` 配合一个画刷，让内容淡出或部分隐去：遮罩画刷透明的地方内容不可见，不透明的地方内容照常显示：

### 渐变淡出 {#gradient-fade}

```xml
<Image Source="/assets/landscape.jpg" Width="400" Height="300">
    <Image.OpacityMask>
        <LinearGradientBrush StartPoint="0%,0%" EndPoint="0%,100%">
            <GradientStop Color="Black" Offset="0" />
            <GradientStop Color="Black" Offset="0.6" />
            <GradientStop Color="Transparent" Offset="1" />
        </LinearGradientBrush>
    </Image.OpacityMask>
</Image>
```

这会让图片底部渐变至透明，做出常见的「淡出」效果。

### 横向淡出 {#horizontal-fade}

```xml
<TextBlock Text="This text fades to the right" FontSize="24">
    <TextBlock.OpacityMask>
        <LinearGradientBrush StartPoint="0%,0%" EndPoint="100%,0%">
            <GradientStop Color="Black" Offset="0" />
            <GradientStop Color="Black" Offset="0.7" />
            <GradientStop Color="Transparent" Offset="1" />
        </LinearGradientBrush>
    </TextBlock.OpacityMask>
</TextBlock>
```

### 径向遮罩 {#radial-mask}

```xml
<Image Source="/assets/photo.jpg" Width="300" Height="300">
    <Image.OpacityMask>
        <RadialGradientBrush>
            <GradientStop Color="Black" Offset="0" />
            <GradientStop Color="Black" Offset="0.5" />
            <GradientStop Color="Transparent" Offset="1" />
        </RadialGradientBrush>
    </Image.OpacityMask>
</Image>
```

这会做出边缘渐隐的暗角效果。

### VisualBrush 遮罩 {#visualbrush-mask}

你可以把 `VisualBrush` 用作不透明度遮罩，从而把内容裁成另一个控件的形状：

```xml
<Image Source="/assets/photo.jpg" Width="300" Height="300">
    <Image.OpacityMask>
        <VisualBrush>
            <VisualBrush.Visual>
                <TextBlock Text="HELLO" FontSize="120" FontWeight="Bold"
                           Foreground="Black" />
            </VisualBrush.Visual>
        </VisualBrush>
    </Image.OpacityMask>
</Image>
```

只有 `TextBlock` 渲染出不透明像素的地方图片才可见，于是做出了文字形状的镂空效果。

## 在自定义控件中裁剪 {#clipping-in-custom-controls}

渲染自定义控件时，你可以用代码施加裁剪：

```csharp
public override void Render(DrawingContext context)
{
    // Push a clip region
    using (context.PushClip(new Rect(10, 10, 80, 80)))
    {
        context.FillRectangle(Brushes.Blue, new Rect(0, 0, 100, 100));
        // Only the portion within (10,10,80,80) is visible
    }
}
```

### 在代码中做几何裁剪 {#geometry-clip-in-code}

```csharp
var ellipse = new EllipseGeometry(new Rect(0, 0, 100, 100));
using (context.PushGeometryClip(ellipse))
{
    context.DrawImage(bitmap, new Rect(0, 0, 100, 100));
}
```

## 另请参阅 {#see-also}

- [形状与几何](/docs/graphics-animation/shapes-and-geometries)：可用作裁剪区域的几何类型。
- [画刷](/docs/graphics-animation/brushes)：可用作不透明度遮罩的各类画刷。
- [自定义渲染](/docs/graphics-animation/custom-rendering)：DrawingContext 参考。
