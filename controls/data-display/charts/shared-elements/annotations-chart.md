---
id: annotations-chart
title: 标注
description: 为图表添加参考线、区间带、图形和文字，用来标出阈值、里程碑或值得关注的区域。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFeaturesAnnotation from '/img/controls/charts/charts-annotations.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

标注让你能用参考线、区间带、图形和自定义文字为图表补充背景信息，很适合标出阈值、里程碑，或某段值得关注的区域。

<Image light={chartsFeaturesAnnotation} maxWidth={400} position="center" cornerRadius="true" alt="Chart with annotation overlays including a horizontal threshold line, a shaded comfort zone band, and a custom text label." />

## 适用场景 {#when-to-use}

- **阈值**：在绩效图上画一条「目标线」或「上限线」。
- **里程碑**：在时间线上标出几个关键日期。
- **区域高亮**：为某一段取值范围铺上「危险区」或「舒适区」的底色。

## 代码示例 {#code-example}

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="ShapesChart" Height="250">
                        <CartesianChart.HorizontalAxis>
                            <NumericalAxis Title="X" Minimum="0" Maximum="10" />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis Title="Y" Minimum="0" Maximum="100" />
                        </CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <ScatterSeries Title="Points" ItemsSource="{Binding ShapeData}"
                                                    CategoryPath="X" ValuePath="Y" MarkerSize="8" />
                        </CartesianChart.Series>
                        <CartesianChart.Annotations>
                            <!-- Highlight Region -->
                            <RectangleAnnotation X="0.6" Y="60" Width="0.2" Height="20"
                                                          Stroke="Blue" Label="Region A">
                                <RectangleAnnotation.Fill>
                                    <SolidColorBrush Color="#280000FF" />
                                </RectangleAnnotation.Fill>
                            </RectangleAnnotation>
                            <!-- Circle of Interest -->
                            <EllipseAnnotation X="0.3" Y="30" RadiusX="0.05" RadiusY="5"
                                                        Stroke="Orange" Label="Cluster">
                                <EllipseAnnotation.Fill>
                                    <SolidColorBrush Color="#28FFA500" />
                                </EllipseAnnotation.Fill>
                            </EllipseAnnotation>
                            <!-- Trend Arrow -->
                            <ArrowLineAnnotation X1="0.3" Y1="35" X2="0.7" Y2="65"
                                                          Stroke="Purple" StrokeThickness="2" ShowEndArrow="True" Label="Growth" />
                        </CartesianChart.Annotations>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
public record Point(double X, double Y);

public ObservableCollection<Point> ShapeData { get; } = new()
{
    new(3, 30),
    new(7, 70)
};
```

## 坐标体系 {#coordinate-system}

标注的坐标以坐标轴空间为准。在类别轴上，横向取值使用从零开始的类别槽位索引；在连续横轴上，横向取值使用该轴的值域，比如数值或 `DateTime` 刻度。纵向取值一律使用纵轴的值域。

图形的尺寸同样以坐标轴单位计量。在对数轴或带刻度断裂的轴上，同样的数据增量会因起点不同而对应不同的像素尺寸。自定义标注渲染器定位时应使用 `CartesianAnnotationRenderContext.DataXToPixel` 和 `DataYToPixel`，涉及起点的尺寸换算则应使用 `DeltaXToPixelsAt(origin, value)` 或 `DeltaYToPixelsAt(origin, value)`。

## 公共属性（LineAnnotation） {#common-properties-lineannotation}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | 参考线所在的坐标轴空间取值。水平线取纵轴的值，垂直线取横轴的值。 | `0` |
| `Orientation` | `Horizontal` or `Vertical`. | `Horizontal` |
| `Stroke` | 标注线的颜色。 | `Gray` |
| `StrokeThickness` | 标注线的粗细。 | `1.0` |
| `DashStyle` | 标注线所用的虚线样式。 | `null` |
| `Foreground` | 标签文字所用的画刷。为 `null` 时，在支持的场合下标注会回落到 `Stroke`。 | `null` |
| `FontSize` | 标注标签所用的字号。 | `12.0` |
| `Label` | 显示在参考线旁的文字。 | `null` |

## 常用属性（`BandAnnotation`） {#common-properties-bandannotation}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `FromValue` | 区间带起始处的坐标轴空间取值。水平带取纵轴的值，垂直带取横轴的值。 | `0` |
| `ToValue` | 区间带结束处的坐标轴空间取值。 | `0` |
| `Orientation` | `Horizontal` or `Vertical`. | `Horizontal` |
| `Fill` | 填充阴影区域所用的画刷。 | `null` |
| `Foreground` | 区间带标签文字所用的画刷。为 `null` 时，在支持的场合下标注会回落到 `Stroke`。 | `null` |
| `FontSize` | 区间带标签所用的字号。 | `12.0` |
| `Label` | 显示在区间带内部的文字。 | `null` |

## 公共属性（TextAnnotation） {#common-properties-textannotation}

放置在图表区指定坐标处的一条文字标注。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `X` | 横轴取值。类别轴使用从零开始的类别槽位索引。 | `0` |
| `Y` | 纵轴取值。 | `0` |
| `Text` | 该标注所显示的文字。 | `null` |
| `Foreground` | 文字填充所用的画刷。 | `null` |
| `FontSize` | 文字所用的字号。 | `12.0` |
| `Stroke` | 可选的文字描边画刷。只有显式设置了 `Stroke` 才会绘制文字描边。 | `Gray` |
| `StrokeThickness` | 可选的文字描边粗细。只有显式设置了 `Stroke` 时才生效。 | `1.0` |
| `Opacity` | 标注的不透明度。 | `1.0` |

## 常用属性（`RectangleAnnotation`） {#common-properties-rectangleannotation}

放置在图表区指定坐标处的一个矩形标注。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `X` | 左边缘的横轴取值。类别轴使用从零开始的类别槽位索引。 | `0` |
| `Y` | 下边缘的纵轴取值。 | `0` |
| `Width` | 宽度，以横轴单位计。 | `0.5` |
| `Height` | 高度，以纵轴单位计。 | `10.0` |
| `Fill` | 填充矩形所用的画刷。 | `null` |
| `CornerRadius` | 圆角矩形的圆角半径。 | `0` |
| `Label` | 显示在矩形中央的文字。 | `null` |
| `Stroke` | 矩形边框的颜色。 | `Gray` |
| `StrokeThickness` | 矩形边框的粗细。 | `1` |
| `Foreground` | 矩形标签文字所用的画刷。 | `null` |
| `FontSize` | 矩形标签所用的字号。 | `12.0` |
| `Opacity` | 标注的不透明度。 | `1.0` |

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Height="250">
    <CartesianChart.Annotations>
        <RectangleAnnotation X="0.2" Y="50" Width="0.3" Height="20"
                                    Stroke="DarkGreen" StrokeThickness="2"
                                    CornerRadius="4" Label="Target Zone">
            <RectangleAnnotation.Fill>
                <SolidColorBrush Color="#3200FF00" />
            </RectangleAnnotation.Fill>
        </RectangleAnnotation>
    </CartesianChart.Annotations>
</CartesianChart>
```

## 常用属性（`EllipseAnnotation`） {#common-properties-ellipseannotation}

放置在图表区指定坐标处的一个椭圆标注。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `X` | 圆心的横轴取值。类别轴使用从零开始的类别槽位索引。 | `0` |
| `Y` | 圆心的纵轴取值。 | `0` |
| `RadiusX` | 横向半径，以坐标轴单位计。 | `0.25` |
| `RadiusY` | 纵向半径，以坐标轴单位计。 | `10.0` |
| `Fill` | 填充椭圆所用的画刷。 | `null` |
| `Label` | 显示在椭圆中央的文字。 | `null` |
| `Stroke` | 椭圆边框的颜色。 | `Gray` |
| `StrokeThickness` | 椭圆边框的粗细。 | `1` |
| `Foreground` | 椭圆标签文字所用的画刷。 | `null` |
| `FontSize` | 椭圆标签所用的字号。 | `12.0` |
| `Opacity` | 标注的不透明度。 | `1.0` |

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Height="250">
    <CartesianChart.Annotations>
        <EllipseAnnotation X="0.5" Y="60" RadiusX="0.15" RadiusY="15"
                                  Stroke="Purple" StrokeThickness="2"
                                  Label="Anomaly">
            <EllipseAnnotation.Fill>
                <SolidColorBrush Color="#32800080" />
            </EllipseAnnotation.Fill>
        </EllipseAnnotation>
    </CartesianChart.Annotations>
</CartesianChart>
```

## 常用属性（`ArrowLineAnnotation`） {#common-properties-arrowlineannotation}

一种线条标注，可在一端或两端加箭头，适合指示方向，或在两个数据点之间牵引视线。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `X1` | 起点的横轴取值。类别轴使用从零开始的类别槽位索引。 | `0` |
| `Y1` | 起点的纵轴取值。 | `0` |
| `X2` | 终点的横轴取值。 | `0` |
| `Y2` | 终点的纵轴取值。 | `0` |
| `ShowStartArrow` | 是否在起点显示箭头。 | `false` |
| `ShowEndArrow` | 是否在终点显示箭头。 | `true` |
| `ArrowSize` | 箭头的大小，单位为像素。 | `8.0` |
| `Label` | 显示在线段中点处的文字。 | `null` |
| `Stroke` | 箭头线的颜色。 | `Gray` |
| `StrokeThickness` | 箭头线的粗细。 | `1` |
| `Foreground` | 箭头标签文字所用的画刷。 | `null` |
| `FontSize` | 箭头标签所用的字号。 | `12.0` |
| `Opacity` | 标注的不透明度。 | `1.0` |

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Height="250">
    <CartesianChart.Annotations>
        <ArrowLineAnnotation X1="0.1" Y1="30" X2="0.6" Y2="80"
                                    Stroke="OrangeRed" StrokeThickness="2"
                                    ShowEndArrow="True" ArrowSize="10"
                                    Label="Upward trend" />
    </CartesianChart.Annotations>
</CartesianChart>
```
