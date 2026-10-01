---
id: ridgeline-chart
title: 山脊图
description: 把多条分布曲线按设定的重叠量叠放在一起，适合比较各组或各时期分布形态的变化。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

山脊图把多条面积分布曲线纵向重叠地叠放在一起，便于比较不同组别、时期或情景下分布形态的变化。

## 适用场景 {#when-to-use}

- **分布随时间演变**：比较某个分布从一个时期到另一个时期的位移。
- **分组对比**：把许多条相关的密度型曲线收进同一个紧凑的画框。
- **以形态为先的分析**：更看重轮廓和重叠，而非精确的总量。

## 代码示例 {#code-example}

### XAML

```xml
<RidgelineChart xmlns="https://github.com/avaloniaui" Title="Distribution over time" Height="360">
    <RidgelineChart.Series>
        <AreaSeries Title="2023" ItemsSource="{Binding Series2023}" CategoryPath="X" ValuePath="Y" />
        <AreaSeries Title="2024" ItemsSource="{Binding Series2024}" CategoryPath="X" ValuePath="Y" />
    </RidgelineChart.Series>
</RidgelineChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
public record CurvePoint(double X, double Y);

public ObservableCollection<CurvePoint> Series2023 { get; } = new() { new(0, 4), new(1, 8), new(2, 5) };
public ObservableCollection<CurvePoint> Series2024 { get; } = new() { new(0, 3), new(1, 9), new(2, 6) };
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Series` | `AreaSeries` 分布的内容集合。 | 空集合 |
| `Overlap` | 各系列之间的重叠系数。 | `0.5` |
| `SeriesHeight` | 每条系列色带的目标高度。 | `50.0` |
| `CurveType` | 曲线插值类型。 | `Spline` |

## 另请参阅 {#see-also}

- [面积图](/controls/data-display/charts/cartesian/area-chart)
- [密度图](/controls/data-display/charts/statistical/density-plot-chart)
