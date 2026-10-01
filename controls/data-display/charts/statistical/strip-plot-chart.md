---
id: strip-plot-chart
title: Strip plot chart
description: Displays individual observations per category with controlled jitter, useful for raw-value comparison and mean overlays.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Strip plots show every observation in a category while applying jitter to reduce overlap and optional mean lines to summarize the center.

## 适用场景 {#when-to-use}

- **Raw sample display**: Show every point rather than only quartiles or averages.
- **Category spread**: Compare how tightly or widely values cluster per group.
- **Hybrid views**: Combine raw observations with a simple mean reference line.

## 代码示例 {#code-example}

### XAML

```xml
<StripPlotChart xmlns="https://github.com/avaloniaui" Title="Response times"
                                 Height="300"
                                 ItemsSource="{Binding StripData}"
                                 CategoryPath="Category"
                                 ValuePath="Value"
                                 JitterAmount="0.3"
                                 ShowMeanLine="True" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record StripPoint(string Category, double Value);

public ObservableCollection<StripPoint> StripData { get; } = new()
{
    new("API", 120),
    new("API", 128),
    new("UI", 95),
    new("UI", 102)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | Collection of observations. | `null` |
| `CategoryPath` | Path to the grouping category. | `null` |
| `ValuePath` | 指向数值的路径。 | `null` |
| `PointRadius` | Radius of each point. | `4.0` |
| `JitterAmount` | Horizontal jitter factor applied within each category. | `0.3` |
| `Fill` | Brush used to fill points. | `null` |
| `Stroke` | Brush used for point outlines. | `null` |
| `StrokeThickness` | Thickness of point outlines. | `0.5` |
| `PointOpacity` | Opacity applied to the plotted points. | `0.7` |
| `ShowCategoryLabels` | Whether to draw category labels. | `true` |
| `ShowAxes` | Whether to draw the value axis. | `true` |
| `ShowMeanLine` | Whether to draw a mean line for each category. | `true` |

## 另请参阅 {#see-also}

- [Beeswarm plot chart](/controls/data-display/charts/statistical/beeswarm-plot-chart)
- [Box plot chart](/controls/data-display/charts/statistical/boxplot-chart)
