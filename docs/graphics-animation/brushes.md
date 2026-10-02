---
id: brushes
title: 画刷
description: Avalonia 中用于绘制表面的各类画刷：纯色、渐变和平铺画刷。
doc-type: reference
---

画刷决定了 Avalonia 中各个表面如何被绘制。凡是接受 `Brush` 的属性（比如 `Background`、`Foreground`、`BorderBrush`、`Fill` 和 `Stroke`），都能用上本文介绍的任意一种画刷。

## SolidColorBrush

用单一颜色填充区域。这是最常用的画刷类型——当你给某个画刷属性直接赋一个颜色字符串时，用的就是它。

```xml
<Border Background="SteelBlue" />

<!-- Explicit form -->
<Border>
    <Border.Background>
        <SolidColorBrush Color="#4682B4" Opacity="0.8" />
    </Border.Background>
</Border>
```

颜色可以这样写：

| 格式 | 示例 | 说明 |
|---|---|---|
| 具名颜色 | `Red`, `SteelBlue` | 任意标准的 CSS/WPF 颜色名。 |
| `#RRGGBB` | `#4682B4` | Hex RGB. |
| `#AARRGGBB` | `#804682B4` | 十六进制 ARGB（含 alpha）。 |
| `#RGB` | `#F00` | 简写的十六进制 RGB。 |
| `rgb()` | `rgb(70, 130, 180)` | CSS 的 RGB 函数写法，取值 0–255。 |
| `rgba()` | `rgba(70, 130, 180, 0.8)` | 带 alpha 的 CSS RGB（0.0–1.0）。 |
| `hsl()` | `hsl(207, 44%, 49%)` | CSS HSL（色相、饱和度、亮度）。 |
| `hsla()` | `hsla(207, 44%, 49%, 0.8)` | 带 alpha 的 CSS HSL。 |
| `hsv()` | `hsv(207, 61%, 71%)` | HSV（色相、饱和度、明度）。 |
| `hsva()` | `hsva(207, 61%, 71%, 0.8)` | 带 alpha 的 HSV。 |

凡是需要画刷或颜色的地方，这些写法都通用，XAML 特性、样式，以及代码中的 `Brush.Parse()` / `Color.Parse()` 都包括在内。

```xml
<!-- All of these are equivalent -->
<Border Background="SteelBlue" />
<Border Background="#4682B4" />
<Border Background="rgb(70, 130, 180)" />
<Border Background="hsl(207, 44%, 49%)" />
```

### 在代码中创建 {#creating-in-code}

```csharp
var brush = new SolidColorBrush(Colors.SteelBlue);
var brush2 = new SolidColorBrush(Color.Parse("#4682B4"));
var brush3 = Brush.Parse("rgb(70, 130, 180)");
var brush4 = Brush.Parse("hsl(207, 44%, 49%)");
myBorder.Background = brush;
```

`Brush.Parse()` 接受上面列出的全部颜色格式，具名颜色、十六进制值和 CSS 颜色函数都认。

## LinearGradientBrush

用沿一条直线在若干颜色之间过渡的渐变填充区域。关于线性渐变的专题讲解，请参阅[渐变](/docs/graphics-animation/gradients)。

```xml
<Border Height="80" CornerRadius="8">
    <Border.Background>
        <LinearGradientBrush StartPoint="0%,50%" EndPoint="100%,50%">
            <GradientStop Color="#6366F1" Offset="0" />
            <GradientStop Color="#EC4899" Offset="1" />
        </LinearGradientBrush>
    </Border.Background>
</Border>
```

### 关键属性 {#key-properties}

| 属性 | 说明 |
|---|---|
| `StartPoint` | 渐变线的起点，可用相对坐标（`50%,0%`）或绝对坐标。 |
| `EndPoint` | 渐变线的终点。 |
| [`GradientStops`](/api/avalonia/media/gradientstops) | 一组 `GradientStop` 对象，用来定义各个颜色及其位置。 |
| `SpreadMethod` | 渐变如何填充其定义区域之外的空间：`Pad`（默认）、`Reflect` 或 `Repeat`。 |
| `Opacity` | 画刷的整体不透明度（0.0 到 1.0）。 |

### 渐变方向 {#gradient-directions}

```xml
<!-- Horizontal (left to right) -->
<LinearGradientBrush StartPoint="0%,50%" EndPoint="100%,50%">

<!-- Vertical (top to bottom) -->
<LinearGradientBrush StartPoint="50%,0%" EndPoint="50%,100%">

<!-- Diagonal -->
<LinearGradientBrush StartPoint="0%,0%" EndPoint="100%,100%">
```

## RadialGradientBrush

用自中心点向外辐射的渐变填充区域。

```xml
<Ellipse Width="150" Height="150">
    <Ellipse.Fill>
        <RadialGradientBrush GradientOrigin="30%,30%">
            <GradientStop Color="White" Offset="0" />
            <GradientStop Color="#3B82F6" Offset="0.6" />
            <GradientStop Color="#1E3A8A" Offset="1" />
        </RadialGradientBrush>
    </Ellipse.Fill>
</Ellipse>
```

### 关键属性 {#key-properties-1}

| 属性 | 说明 |
|---|---|
| `Center` | 最外层圆的圆心，默认为 `50%,50%`。 |
| `GradientOrigin` | 渐变的原点（焦点）。把它从圆心偏开，就能做出聚光灯一样的效果。 |
| `RadiusX`, `RadiusY` | 最外层渐变圆的水平与垂直半径，默认为 `50%`。 |
| `GradientStops` | 沿半径分布的各个颜色及其位置。 |
| `SpreadMethod` | `Pad`, `Reflect`, or `Repeat`. |

## ConicGradientBrush

用绕中心点旋转扫掠的渐变填充区域，颜色随角度推移而过渡。

```xml
<Ellipse Width="150" Height="150">
    <Ellipse.Fill>
        <ConicGradientBrush Center="50%,50%" Angle="0">
            <GradientStop Color="#EF4444" Offset="0" />
            <GradientStop Color="#F59E0B" Offset="0.25" />
            <GradientStop Color="#22C55E" Offset="0.5" />
            <GradientStop Color="#3B82F6" Offset="0.75" />
            <GradientStop Color="#EF4444" Offset="1" />
        </ConicGradientBrush>
    </Ellipse.Fill>
</Ellipse>
```

### 关键属性 {#key-properties-2}

| 属性 | 说明 |
|---|---|
| `Center` | 锥形渐变的中心点，默认为 `50%,50%`。 |
| `Angle` | 起始角度，单位为度，默认为 `0`。 |
| `GradientStops` | 沿扫掠方向分布的各个颜色及其位置。 |

## ImageBrush

用一张图片来绘制区域。

```xml
<Border Width="200" Height="200">
    <Border.Background>
        <ImageBrush Source="avares://MyApp/Assets/texture.png"
                    Stretch="UniformToFill"
                    TileMode="Tile"
                    SourceRect="0,0,64,64" />
    </Border.Background>
</Border>
```

### 关键属性 {#key-properties-3}

| 属性 | 说明 |
|---|---|
| `Source` | 图片来源，支持 `avares://` URI 和文件路径。 |
| `Stretch` | 图片如何填满区域：`None`、`Fill`、`Uniform`（默认）、`UniformToFill`。 |
| `TileMode` | 图片如何平铺：`None`（默认）、`Tile`、`FlipX`、`FlipY`、`FlipXY`。 |
| `AlignmentX` | 图片在单块平铺区内的水平对齐方式：`Left`、`Center`（默认）、`Right`。 |
| `AlignmentY` | 图片在单块平铺区内的垂直对齐方式：`Top`、`Center`（默认）、`Bottom`。 |
| `SourceRect` | 要取用的源图矩形区域。 |
| `DestinationRect` | 目标区域内的目的矩形。 |
| `Opacity` | 画刷的整体不透明度。 |
| `BitmapInterpolationMode` | 插值质量：`Default`、`LowQuality`、`MediumQuality`、`HighQuality`。 |

### 平铺示例 {#tiling-example}

```xml
<Border Width="300" Height="200">
    <Border.Background>
        <ImageBrush Source="avares://MyApp/Assets/pattern.png"
                    TileMode="Tile"
                    DestinationRect="0,0,32,32" />
    </Border.Background>
</Border>
```

## VisualBrush

用另一个视觉元素的渲染结果来绘制区域。

```xml
<Border Width="200" Height="200" BorderBrush="Gray" BorderThickness="1">
    <Border.Background>
        <VisualBrush Stretch="Uniform" TileMode="Tile"
                     DestinationRect="0,0,50,50">
            <VisualBrush.Visual>
                <TextBlock Text="Avalonia" FontSize="14" Foreground="LightGray"
                           RenderTransform="rotate(45deg)" />
            </VisualBrush.Visual>
        </VisualBrush>
    </Border.Background>
</Border>
```

### 关键属性 {#key-properties-4}

| 属性 | 说明 |
|---|---|
| `Visual` | 作为画刷内容渲染的那个视觉元素。 |
| `Stretch` | 该视觉元素如何填满区域。 |
| `TileMode` | 重复该视觉元素时的平铺模式。 |
| `SourceRect` | 要取用的视觉元素的哪一部分。 |
| `DestinationRect` | 每块平铺区对应的目的矩形。 |

:::info
`VisualBrush` 可以捕获任意控件的视觉外观，用来做倒影效果、水印和预览缩略图都很合适。
:::

## 画刷的通用属性 {#common-brush-properties}

所有画刷类型都具备这些属性：

| 属性 | 说明 |
|---|---|
| `Opacity` | 取值介于 0.0（完全透明）和 1.0（完全不透明）之间。 |
| `Transform` | 施加在画刷坐标上的变换。 |
| `TransformOrigin` | 画刷变换的原点。 |

## OpacityMask

任意控件的 `OpacityMask` 属性都接受一个画刷，用来逐像素控制透明度。遮罩画刷的 alpha 通道决定了控件中每个像素的不透明度。

```xml
<Image Source="avares://MyApp/Assets/photo.png" Width="200" Height="200">
    <Image.OpacityMask>
        <LinearGradientBrush StartPoint="0%,0%" EndPoint="0%,100%">
            <GradientStop Color="Black" Offset="0" />
            <GradientStop Color="Transparent" Offset="1" />
        </LinearGradientBrush>
    </Image.OpacityMask>
</Image>
```

这个例子里，图片从顶部的完全可见渐变到底部的完全透明。遮罩中的颜色值无关紧要，只有 alpha 通道起作用。

## 把画刷当作资源使用 {#using-brushes-as-resources}

把画刷定义成资源，便可在整个应用中复用：

```xml
<Application.Resources>
    <SolidColorBrush x:Key="PrimaryBrush" Color="#6366F1" />
    <LinearGradientBrush x:Key="AccentGradient" StartPoint="0%,0%" EndPoint="100%,100%">
        <GradientStop Color="#6366F1" Offset="0" />
        <GradientStop Color="#EC4899" Offset="1" />
    </LinearGradientBrush>
</Application.Resources>
```

```xml
<Button Background="{StaticResource PrimaryBrush}" />
<Border Background="{DynamicResource AccentGradient}" />
```

## 在代码中使用画刷 {#brushes-in-code}

```csharp
// SolidColorBrush
var solid = new SolidColorBrush(Colors.IndianRed);

// LinearGradientBrush
var linear = new LinearGradientBrush
{
    StartPoint = new RelativePoint(0, 0.5, RelativeUnit.Relative),
    EndPoint = new RelativePoint(1, 0.5, RelativeUnit.Relative),
    GradientStops =
    {
        new GradientStop(Colors.Blue, 0),
        new GradientStop(Colors.Red, 1)
    }
};

// RadialGradientBrush
var radial = new RadialGradientBrush
{
    GradientStops =
    {
        new GradientStop(Colors.White, 0),
        new GradientStop(Colors.Black, 1)
    }
};

myBorder.Background = linear;
```

## 另请参阅 {#see-also}

- [渐变](/docs/graphics-animation/gradients)：线性渐变用法的专题讲解。
- [绘制图形](/docs/graphics-animation/drawing-graphics)：形状与几何。
- [图像插值](/docs/graphics-animation/image-interpolation)：位图渲染的质量设置。
