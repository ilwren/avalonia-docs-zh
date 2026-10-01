---
id: beeswarm-plot-chart
title: Beeswarm plot chart
description: Displays individual observations per category as non-overlapping dots, preserving point density without full jitter noise.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Beeswarm plots arrange points within each category to avoid overlap while preserving the distribution of individual observations.

## 适用场景 {#when-to-use}

- **Raw observation display**: Show every point instead of only summary statistics.
- **Category comparison**: Compare spread and clustering across groups.
- **Distribution detail**: Reveal dense stacks that a plain scatter plot would hide.

## 代码示例 {#code-example}

### XAML

```xml
<BeeswarmPlotChart xmlns="https://github.com/avaloniaui" Title="Test scores by group"
                                    Height="300"
                                    ItemsSource="{Binding BeeswarmData}"
                                    CategoryPath="Category"
                                    ValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record BeeswarmPoint(string Category, double Value);

public ObservableCollection<BeeswarmPoint> BeeswarmData { get; } = new()
{
    new("A", 62),
    new("A", 65),
    new("B", 74),
    new("B", 79)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | Collection of observations. | `null` |
| `CategoryPath` | Path to the grouping category. | `null` |
| `ValuePath` | 指向数值的路径。 | `null` |
| `PointRadius` | Radius of each point. | `5.0` |
| `Fill` | Brush used to fill points. | `null` |
| `Stroke` | Brush used for point outlines. | `null` |
| `StrokeThickness` | Thickness of point outlines. | `1.0` |
| `ShowCategoryLabels` | Whether to draw category labels. | `true` |
| `ShowAxes` | Whether to draw the value axis. | `true` |

## 另请参阅 {#see-also}

- [Strip plot chart](/controls/data-display/charts/statistical/strip-plot-chart)
- [Violin plot](/controls/data-display/charts/statistical/violin-plot-chart)
