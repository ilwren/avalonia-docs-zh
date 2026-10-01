---
id: hexbin-chart
title: Hexbin chart
description: Aggregates dense 2D point clouds into hexagonal bins, useful for visualizing concentration without overplotting.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Hexbin charts group nearby points into hexagons so dense scatter data remains readable even when thousands of points overlap.

## 适用场景 {#when-to-use}

- **Dense scatter data**: Replace unreadable point clouds with density bins.
- **Spatial concentration**: Show where observations cluster in two dimensions.
- **Exploratory analysis**: Reveal hotspots and gradients without smoothing the raw data.

## 代码示例 {#code-example}

### XAML

```xml
<HexbinChart xmlns="https://github.com/avaloniaui" Title="Request concentration"
                              Height="320"
                              ItemsSource="{Binding HexbinData}"
                              XPath="X"
                              YPath="Y"
                              HexRadius="16" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record SamplePoint(double X, double Y);

public ObservableCollection<SamplePoint> HexbinData { get; } = new()
{
    new(12, 20),
    new(14, 22),
    new(13, 21),
    new(28, 35)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | Collection of X and Y points. | `null` |
| `XPath` | Path to the X value. | `null` |
| `YPath` | Path to the Y value. | `null` |
| `HexRadius` | Radius of each hexagon in pixels. | `20.0` |
| `ColorScale` | Color scale used to encode density. | `Blues` |
| `ShowAxes` | Whether to draw the chart axes. | `true` |

## 另请参阅 {#see-also}

- [气泡图](/controls/data-display/charts/bubble/bubble-chart)
- [Contour plot chart](/controls/data-display/charts/statistical/contour-plot-chart)
