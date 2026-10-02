---
id: parallel-coordinates-chart
title: 平行坐标图
description: 把多变量记录画成跨越一组平行轴的折线，适合在众多维度上比较各自的形态。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

平行坐标图把每条记录映射到一列纵轴上，于是多维度的规律和异常值能在同一视图中两相比较。

## 适用场景 {#when-to-use}

- **多变量对比**：比较每个条目在多个数值维度上的表现。
- **规律发现**：在众多指标上发现异常值、簇群和主导形态。
- **模型诊断**：一次性考察各条记录在众多输入上的差异。

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
| `Axes` | `ParallelAxis` 定义的内容集合。 | 空集合 |
| `ItemsSource` | 多变量记录的集合。 | `null` |
| `BrushPath` | 可选路径，为每条折线提供 `IBrush` 或颜色字符串。 | `null` |
| `LegendLabelPath` | 用于图例标签的可选路径。 | `null` |
| `StrokeThickness` | 数据折线的粗细。 | `2.0` |
| `CurveTension` | 曲线的张力取值。 | `0.0` |

## 常用属性（`ParallelAxis`） {#common-properties-parallelaxis}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Header` | 坐标轴标题。 | `null` |
| `ValuePath` | 指向绑定到该轴数值的路径。 | `null` |
| `Minimum` | 坐标轴刻度的最小值。 | `0.0` |
| `Maximum` | 坐标轴刻度的最大值。 | `100.0` |

## 另请参阅 {#see-also}

- [雷达图](/controls/data-display/charts/radial/radar-chart)
- [三元图](/controls/data-display/charts/engineering/ternary-chart)
