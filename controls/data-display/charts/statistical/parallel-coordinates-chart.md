---
id: parallel-coordinates-chart
title: Parallel coordinate chart
description: Visualizes multivariate records as lines across parallel axes, useful for comparing patterns across many dimensions.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Parallel coordinate charts map each record across a sequence of vertical axes so multi-dimensional patterns and outliers can be compared in one view.

## 适用场景 {#when-to-use}

- **Multivariate comparison**: Compare several numeric dimensions for each item.
- **Pattern detection**: Spot outliers, clusters, and dominant shapes across metrics.
- **Model diagnostics**: Inspect how records vary across many inputs at once.

## 代码示例 {#code-example}

### XAML

```xml
<ParallelCoordinatesChart xmlns="https://github.com/avaloniaui" Title="Vehicle comparison"
                                           Height="320"
                                           ItemsSource="{Binding Vehicles}">
    <ParallelCoordinatesChart.Axes>
        <ParallelAxis Header="Power" ValuePath="Power" Minimum="0" Maximum="400" />
        <ParallelAxis Header="Range" ValuePath="Range" Minimum="0" Maximum="600" />
        <ParallelAxis Header="Efficiency" ValuePath="Efficiency" Minimum="0" Maximum="100" />
    </ParallelCoordinatesChart.Axes>
</ParallelCoordinatesChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
public record VehicleStats(double Power, double Range, double Efficiency);

public ObservableCollection<VehicleStats> Vehicles { get; } = new()
{
    new(220, 480, 76),
    new(310, 420, 64),
    new(180, 520, 82)
};
```

## 常用属性（`ParallelCoordinatesChart`） {#common-properties-parallelcoordinateschart}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Axes` | Content collection of `ParallelAxis` definitions. | 空集合 |
| `ItemsSource` | Collection of multivariate records. | `null` |
| `BrushPath` | Optional path to an `IBrush` or color string used for each line. | `null` |
| `LegendLabelPath` | Optional path used for legend labels. | `null` |
| `StrokeThickness` | Thickness of the data lines. | `2.0` |
| `CurveTension` | Tension value for curved lines. | `0.0` |

## 常用属性（`ParallelAxis`） {#common-properties-parallelaxis}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Header` | Axis title. | `null` |
| `ValuePath` | Path to the value bound to this axis. | `null` |
| `Minimum` | Minimum value of the axis scale. | `0.0` |
| `Maximum` | Maximum value of the axis scale. | `100.0` |

## 另请参阅 {#see-also}

- [Radar chart](/controls/data-display/charts/radial/radar-chart)
- [Ternary chart](/controls/data-display/charts/engineering/ternary-chart)
