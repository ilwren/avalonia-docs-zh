---
id: gradients
title: 渐变
description: 如何用 LinearGradientBrush、RadialGradientBrush 和 ConicGradientBrush 在 Avalonia UI 中做出颜色过渡。
doc-type: reference
---

渐变画刷能在两种或多种颜色之间平滑过渡。凡是接受画刷的地方都能用它们，包括 `Background`、`Foreground`、`BorderBrush`、`Fill` 和 `Stroke`。Avalonia 提供三种渐变画刷：

| 画刷 | 说明 |
|---|---|
| [`LinearGradientBrush`](/api/avalonia/media/lineargradientbrush) | 沿一条直线过渡颜色。 |
| [`RadialGradientBrush`](/api/avalonia/media/radialgradientbrush) | 从中心点向外、以椭圆形式过渡颜色。 |
| [`ConicGradientBrush`](/api/avalonia/media/conicgradientbrush) | 绕中心点扫掠过渡颜色。 |

所有渐变画刷都共有 `GradientStops` 集合和 `SpreadMethod` 属性。下面先分别介绍三种画刷，再讲它们共通的概念。

## 线性渐变画刷 {#linear-gradient-brush}

`LinearGradientBrush` 沿一条由起点和终点定义的直线混合颜色。

### 基本语法 {#basic-syntax}

```xml
<LinearGradientBrush StartPoint="0%,0%" EndPoint="100%,0%">
    <GradientStop Color="#FF6B6B" Offset="0.0"/>
    <GradientStop Color="#4ECDC4" Offset="1.0"/>
</LinearGradientBrush>
```

### `StartPoint` and `EndPoint`

这两个属性决定渐变的方向。取值可以写成百分比（比如 `"0%,50%"`），也可以写成边界框内的绝对坐标点（比如 `"10,15"`）。

常见的方向写法：

| 方向 | `StartPoint` | `EndPoint` |
|---|---|---|
| 水平（从左到右） | `0%,50%` | `100%,50%` |
| 垂直（从上到下） | `50%,0%` | `50%,100%` |
| 对角（从左上到右下） | `0%,0%` | `100%,100%` |

### 水平渐变 {#horizontal-gradient}

```xml
<LinearGradientBrush StartPoint="0%,50%" EndPoint="100%,50%">
    <GradientStop Color="#FF6B6B" Offset="0.0"/>
    <GradientStop Color="#4ECDC4" Offset="1.0"/>
</LinearGradientBrush>
```

### 垂直渐变 {#vertical-gradient}

```xml
<LinearGradientBrush StartPoint="50%,0%" EndPoint="50%,100%">
    <GradientStop Color="#A8E6CF" Offset="0.0"/>
    <GradientStop Color="#3D84A8" Offset="1.0"/>
</LinearGradientBrush>
```

### 多色渐变 {#multi-color-gradient}

多加几个 [`GradientStop`](/api/avalonia/media/gradientstop) 元素，就能做出经由多种颜色的过渡。调整各自的 `Offset` 取值即可控制每种颜色出现在哪里：

```xml
<LinearGradientBrush StartPoint="0%,50%" EndPoint="100%,50%">
    <GradientStop Color="#FF6B6B" Offset="0.0"/>
    <GradientStop Color="#FF8E53" Offset="0.3"/>
    <GradientStop Color="#FF5E3A" Offset="0.6"/>
    <GradientStop Color="#4ECDC4" Offset="1.0"/>
</LinearGradientBrush>
```

### 常见用法 {#common-use-cases}

#### 按钮背景 {#button-background}

```xml
<Button>
    <Button.Background>
        <LinearGradientBrush StartPoint="0%,0%" EndPoint="0%,100%">
            <GradientStop Color="#4CAF50" Offset="0.0"/>
            <GradientStop Color="#45A049" Offset="1.0"/>
        </LinearGradientBrush>
    </Button.Background>
</Button>
```

#### 面板背景 {#panel-background}

```xml
<Border CornerRadius="8">
    <Border.Background>
        <LinearGradientBrush StartPoint="0%,0%" EndPoint="100%,100%">
            <GradientStop Color="#FF9A9E" Offset="0.0"/>
            <GradientStop Color="#FAD0C4" Offset="0.5"/>
            <GradientStop Color="#FFD1FF" Offset="1.0"/>
        </LinearGradientBrush>
    </Border.Background>
</Border>
```

## 径向渐变画刷 {#radial-gradient-brush}

`RadialGradientBrush` 以椭圆形式，从中心点向外混合颜色。

### 基本语法 {#basic-syntax-1}

```xml
<RadialGradientBrush GradientOrigin="50%,50%" Center="50%,50%" RadiusX="50%" RadiusY="50%">
    <GradientStop Color="Yellow" Offset="0.0"/>
    <GradientStop Color="Red" Offset="1.0"/>
</RadialGradientBrush>
```

### 关键属性 {#key-properties}

| 属性 | 说明 |
|---|---|
| `Center` | 最外层椭圆的中心，以边界框的百分比表示，默认为 `50%,50%`。 |
| `GradientOrigin` | 渐变起始处（最内侧颜色）的位置，默认与 `Center` 相同。 |
| `RadiusX`, `RadiusY` | 椭圆的水平和垂直半径，默认均为 `50%`。 |

把 `GradientOrigin` 设成与 `Center` 不同的值，渐变就会偏离中心，这很适合模拟光照效果：

```xml
<RadialGradientBrush GradientOrigin="30%,30%" Center="50%,50%">
    <GradientStop Color="White" Offset="0.0"/>
    <GradientStop Color="#3D84A8" Offset="1.0"/>
</RadialGradientBrush>
```

### 椭圆形渐变 {#elliptical-gradient}

给 `RadiusX` 和 `RadiusY` 设不同的值，即可做出非正圆的渐变：

```xml
<RadialGradientBrush Center="50%,50%" RadiusX="80%" RadiusY="40%">
    <GradientStop Color="#A8E6CF" Offset="0.0"/>
    <GradientStop Color="#3D84A8" Offset="1.0"/>
</RadialGradientBrush>
```

## 锥形渐变画刷 {#conic-gradient-brush}

`ConicGradientBrush` 绕中心点扫掠着铺开颜色，效果就像一张色轮。

### 基本语法 {#basic-syntax-2}

```xml
<ConicGradientBrush Center="50%,50%" Angle="0">
    <GradientStop Color="Red" Offset="0.0"/>
    <GradientStop Color="Yellow" Offset="0.25"/>
    <GradientStop Color="Green" Offset="0.5"/>
    <GradientStop Color="Blue" Offset="0.75"/>
    <GradientStop Color="Red" Offset="1.0"/>
</ConicGradientBrush>
```

### 关键属性 {#key-properties-1}

| 属性 | 说明 |
|---|---|
| `Center` | 扫掠的中心，默认为 `50%,50%`。 |
| `Angle` | 起始角度，单位为度，自正上方起顺时针计量，默认为 `0`。 |

要让扫掠首尾无缝衔接，把最后一个 `GradientStop` 的颜色设成与第一个相同即可。

## 渐变的共通概念 {#shared-gradient-concepts}

### `GradientStop` elements

每个渐变画刷都含有一个或多个 `GradientStop` 元素，每个渐变停靠点都定义了 `Color` 和 `Offset`：

| 属性 | 说明 |
|---|---|
| `Color` | 任意合法的颜色值（十六进制、具名颜色、`rgb()`、`hsl()` 等）。 |
| `Offset` | `0.0` 到 `1.0` 之间的值，表示在渐变上的位置。 |

若省略 `Offset`，Avalonia 会把各停靠点均匀铺开。两个停靠点取同一个偏移时，得到的不是平滑过渡，而是一道硬边。

### `SpreadMethod`

`SpreadMethod` 决定渐变没铺满整片区域时该怎么办（比如 `LinearGradientBrush` 的起点和终点都落在边界框内部）。

| 值 | 行为 |
|---|---|
| `Pad` (default) | 用两端的颜色延展开去，填满剩余空间。 |
| `Reflect` | 渐变反向重复。 |
| `Repeat` | 渐变从头开始重复。 |

```xml
<LinearGradientBrush StartPoint="0%,50%" EndPoint="50%,50%" SpreadMethod="Reflect">
    <GradientStop Color="#08AEEA" Offset="0.0"/>
    <GradientStop Color="#2AF598" Offset="1.0"/>
</LinearGradientBrush>
```

### `Opacity`

所有渐变画刷都从 `Brush` 继承了 `Opacity` 属性。把它设成 `0.0`（完全透明）到 `1.0`（完全不透明）之间的值，整个渐变就会半透明：

```xml
<LinearGradientBrush StartPoint="0%,50%" EndPoint="100%,50%" Opacity="0.5">
    <GradientStop Color="#FF6B6B" Offset="0.0"/>
    <GradientStop Color="#4ECDC4" Offset="1.0"/>
</LinearGradientBrush>
```

若你想让各个颜色各自透明，请在 `Color` 的取值里带上 alpha 通道（比如 `#80FF6B6B`）。

### 在代码隐藏中创建渐变 {#creating-gradients-in-code-behind}

需要动态生成渐变画刷时，可以在 C# 中把它搭出来：

```csharp
var brush = new LinearGradientBrush
{
    StartPoint = new RelativePoint(0, 0.5, RelativeUnit.Relative),
    EndPoint = new RelativePoint(1, 0.5, RelativeUnit.Relative),
    GradientStops =
    {
        new GradientStop(Color.Parse("#FF6B6B"), 0.0),
        new GradientStop(Color.Parse("#4ECDC4"), 1.0)
    }
};

myBorder.Background = brush;
```

`RadialGradientBrush` 和 `ConicGradientBrush` 的写法同理。

## 完整示例 {#full-example}

<XamlPreview>

```xml
<StackPanel Spacing="16" Margin="16" xmlns="https://github.com/avaloniaui">
    <!-- Horizontal gradient -->
    <Border Height="80" CornerRadius="8">
        <Border.Background>
            <LinearGradientBrush StartPoint="0%,50%" EndPoint="100%,50%">
                <GradientStop Color="#FF6B6B" Offset="0.0"/>
                <GradientStop Color="#FF8E53" Offset="0.3"/>
                <GradientStop Color="#FF5E3A" Offset="0.6"/>
                <GradientStop Color="#4ECDC4" Offset="1.0"/>
            </LinearGradientBrush>
        </Border.Background>
        <TextBlock Text="Horizontal"
                   HorizontalAlignment="Center"
                   VerticalAlignment="Center"
                   Foreground="White"/>
    </Border>

    <!-- Vertical gradient -->
    <Border Height="80" CornerRadius="8">
        <Border.Background>
            <LinearGradientBrush StartPoint="50%,0%" EndPoint="50%,100%">
                <GradientStop Color="#A8E6CF" Offset="0.0"/>
                <GradientStop Color="#3D84A8" Offset="0.5"/>
                <GradientStop Color="#46CDCF" Offset="1.0"/>
            </LinearGradientBrush>
        </Border.Background>
        <TextBlock Text="Vertical"
                   HorizontalAlignment="Center"
                   VerticalAlignment="Center"
                   Foreground="White"/>
    </Border>

    <!-- Radial gradient -->
    <Border Height="80" CornerRadius="8">
        <Border.Background>
            <RadialGradientBrush GradientOrigin="30%,30%">
                <GradientStop Color="White" Offset="0.0"/>
                <GradientStop Color="#3D84A8" Offset="1.0"/>
            </RadialGradientBrush>
        </Border.Background>
        <TextBlock Text="Radial"
                   HorizontalAlignment="Center"
                   VerticalAlignment="Center"
                   Foreground="White"/>
    </Border>

    <!-- Conic gradient -->
    <Border Height="80" CornerRadius="8">
        <Border.Background>
            <ConicGradientBrush Center="50%,50%">
                <GradientStop Color="#FF6B6B" Offset="0.0"/>
                <GradientStop Color="#4ECDC4" Offset="0.5"/>
                <GradientStop Color="#FF6B6B" Offset="1.0"/>
            </ConicGradientBrush>
        </Border.Background>
        <TextBlock Text="Conic"
                   HorizontalAlignment="Center"
                   VerticalAlignment="Center"
                   Foreground="White"/>
    </Border>
</StackPanel>
```

</XamlPreview>

## 另请参阅 {#see-also}

- [画刷](/docs/graphics-animation/brushes)：全部画刷类型概览，`SolidColorBrush` 和平铺画刷也包括在内。
- [效果](/docs/graphics-animation/effects)：盒阴影、裁剪与不透明度遮罩。
- [形状与几何](/docs/graphics-animation/shapes-and-geometries)：绘制可用渐变画刷填充的各种形状。
- [自定义渲染](/docs/graphics-animation/custom-rendering)：用 `DrawingContext` 做底层绘制，其中可直接使用渐变画刷。
