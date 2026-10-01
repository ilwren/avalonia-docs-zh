---
id: ridgeline-chart
title: Ridgeline chart
description: Stacks multiple distributions with controlled overlap, useful for comparing shape changes across groups or time.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Ridgeline charts stack multiple area distributions with vertical overlap so you can compare shape changes across groups, periods, or scenarios.

## 适用场景 {#when-to-use}

- **Distribution over time**: Compare how a distribution shifts from one period to another.
- **Group comparison**: Stack many related density-like curves in one compact frame.
- **Shape-first analysis**: Emphasize contour and overlap more than exact totals.

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
| `Series` | Content collection of `AreaSeries` distributions. | 空集合 |
| `Overlap` | Overlap factor between series. | `0.5` |
| `SeriesHeight` | Target height for each series band. | `50.0` |
| `CurveType` | Curve interpolation type. | `Spline` |

## 另请参阅 {#see-also}

- [面积图](/controls/data-display/charts/cartesian/area-chart)
- [Density plot chart](/controls/data-display/charts/statistical/density-plot-chart)
