---
id: contour-plot-chart
title: Contour plot chart
description: Displays 2D scalar fields as contour lines and optional filled bands, useful for surfaces, intensity maps, and interpolation.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Contour plots interpolate values across two spatial dimensions and render the result as isolines, filled regions, or both.

## 适用场景 {#when-to-use}

- **Surface estimation**: Visualize a scalar field from scattered measurements.
- **Hotspot analysis**: Reveal peaks, valleys, and gradients in two dimensions.
- **Engineering maps**: Show pressure, temperature, or concentration surfaces.

## 代码示例 {#code-example}

### XAML

```xml
<ContourPlot xmlns="https://github.com/avaloniaui" Title="Temperature field"
                              Height="320"
                              ItemsSource="{Binding ContourData}"
                              XPath="X"
                              YPath="Y"
                              ValuePath="Temperature"
                              ContourLevels="10" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record ContourPoint(double X, double Y, double Temperature);

public ObservableCollection<ContourPoint> ContourData { get; } = new()
{
    new(0, 0, 18),
    new(0, 10, 24),
    new(10, 0, 21),
    new(10, 10, 28)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | Collection of sampled points. | `null` |
| `XPath` | Path to the X coordinate. | `null` |
| `YPath` | Path to the Y coordinate. | `null` |
| `ValuePath` | Path to the scalar value. | `null` |
| `ContourLevels` | Number of contour levels to compute. | `8` |
| `ShowFill` | Whether to fill the contour regions. | `true` |
| `ShowLines` | Whether to draw contour lines. | `true` |

## 另请参阅 {#see-also}

- [Hexbin chart](/controls/data-display/charts/engineering/hexbin-chart)
- [Density plot chart](/controls/data-display/charts/statistical/density-plot-chart)
