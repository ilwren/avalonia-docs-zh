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
| `RadiusX`, `RadiusY` | The horizontal and vertical radius of the outermost gradient circle. Default is `50%`. |
| `GradientStops` | Colors and positions along the radius. |
| `SpreadMethod` | `Pad`, `Reflect`, or `Repeat`. |

## ConicGradientBrush

Fills an area with a gradient that sweeps around a center point, transitioning colors as it rotates.

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
| `Center` | The center point of the conic gradient. Default is `50%,50%`. |
| `Angle` | The starting angle in degrees. Default is `0`. |
| `GradientStops` | Colors and positions around the sweep. |

## ImageBrush

Paints an area with an image.

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
| `Source` | The image source. Supports `avares://` URIs and file paths. |
| `Stretch` | How the image fills the area: `None`, `Fill`, `Uniform` (default), `UniformToFill`. |
| `TileMode` | How the image tiles: `None` (default), `Tile`, `FlipX`, `FlipY`, `FlipXY`. |
| `AlignmentX` | Horizontal alignment of the image within the tile: `Left`, `Center` (default), `Right`. |
| `AlignmentY` | Vertical alignment of the image within the tile: `Top`, `Center` (default), `Bottom`. |
| `SourceRect` | A rectangular region of the source image to use. |
| `DestinationRect` | The destination rectangle within the target area. |
| `Opacity` | Overall opacity of the brush. |
| `BitmapInterpolationMode` | Interpolation quality: `Default`, `LowQuality`, `MediumQuality`, `HighQuality`. |

### Tiling example

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

Paints an area using the rendered output of another visual element.

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
| `Visual` | The visual element to render as the brush content. |
| `Stretch` | How the visual fills the area. |
| `TileMode` | Tiling mode for repeating the visual. |
| `SourceRect` | The portion of the visual to use. |
| `DestinationRect` | The destination rectangle for each tile. |

:::info
`VisualBrush` captures the visual appearance of any control. This is useful for creating reflection effects, watermarks, and preview thumbnails.
:::

## Common brush properties

All brush types share these properties:

| 属性 | 说明 |
|---|---|
| `Opacity` | A value between 0.0 (transparent) and 1.0 (opaque). |
| `Transform` | A transform applied to the brush coordinates. |
| `TransformOrigin` | The origin point for the brush transform. |

## OpacityMask

Any control's `OpacityMask` property accepts a brush that controls per-pixel transparency. The alpha channel of the mask brush determines the opacity of each pixel in the control.

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

In this example, the image fades from fully visible at the top to transparent at the bottom. The color values in the mask do not matter; only the alpha channel is used.

## Using brushes as resources

Define brushes as resources for reuse across your application:

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

## Brushes in code

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

- [Gradients](/docs/graphics-animation/gradients): Focused guide on linear gradient usage.
- [Drawing Graphics](/docs/graphics-animation/drawing-graphics): Shapes and geometries.
- [Image Interpolation](/docs/graphics-animation/image-interpolation): Bitmap rendering quality settings.
