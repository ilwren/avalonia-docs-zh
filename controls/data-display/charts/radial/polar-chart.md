---
id: polar-chart
title: 极坐标图
description: 在极坐标系中绘制任意角度和半径的数值，适合呈现螺线、玫瑰线和方向性数据。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

`PolarChart` 可承载一个或多个 `PolarLineSeries`，并用角度加半径（而非笛卡尔坐标轴）来定位每个数据点。

## 适用场景 {#when-to-use}

- **数学曲线**：绘制螺线、玫瑰线、心形线等函数图形。
- **方向性测量**：在整个角度范围内绘制数值。
- **径向分析**：当雷达图那种固定的辐条过于死板时，改用自由角度。

## 代码示例 {#code-example}

### XAML

```xml
<PolarChart xmlns="https://github.com/avaloniaui" Title="Archimedean spiral" Height="300">
    <PolarChart.Series>
        <PolarLineSeries ItemsSource="{Binding SpiralData}"
                                  AnglePath="Angle"
                                  RadiusPath="Radius"
                                  StrokeThickness="2" />
    </PolarChart.Series>
</PolarChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
public record PolarPoint(double Angle, double Radius);

public ObservableCollection<PolarPoint> SpiralData { get; } = new()
{
    new(0, 0),
    new(45, 10),
    new(90, 20),
    new(135, 30)
};
```

## 常用属性（`PolarChart`） {#common-properties-polarchart}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Series` | `PolarLineSeries` 项的内容集合。 | 空集合 |
| `ShowGridLines` | 是否绘制角向和径向网格线。 | `true` |
| `GridLineBrush` | 网格所用的画刷。 | `null` |
| `GridLineStrokeThickness` | 网格线的粗细。 | `1.0` |
| `RadiusAxisMin` | 半径轴的最小值。 | `0.0` |
| `RadiusAxisMax` | 半径轴的最大值。为 `NaN` 时，由图表根据数据自行推算。 | `NaN` |
| `StartAngle` | 视觉上的起始角度，单位为度。 | `-90.0` |
| `IsHighlightEnabled` | 为极坐标数据点启用图表级的悬停高亮。 | `false` |

## 常用属性（`PolarLineSeries`） {#common-properties-polarlineseries}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 极坐标数据点的集合。 | `null` |
| `AnglePath` | 指向角度值（单位为度）的路径。 | `null` |
| `RadiusPath` | 指向半径值的路径。 | `null` |
| `ShowMarkers` | 是否在每个点处绘制标记。 | `false` |
| `MarkerSize` | 标记点大小，单位为像素。 | `8.0` |
| `IsClosed` | 是否把末个点连回首个点。 | `false` |

## 另请参阅 {#see-also}

- [雷达图](/controls/data-display/charts/radial/radar-chart)
- [径向折线图](/controls/data-display/charts/radial/radial-line-chart)
