---
id: contour-plot-chart
title: 等值线图
description: 用等值线和可选的填充带呈现二维标量场，适合曲面、强度分布和插值结果。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

等值线图在两个空间维度上对数值作插值，并把结果绘制成等值线、填充区域，或二者兼有。

## 适用场景 {#when-to-use}

- **曲面估计**：根据零散的测量点还原出一个标量场。
- **热点分析**：显露二维平面上的峰值、谷值和梯度。
- **工程图谱**：呈现压力、温度或浓度的分布曲面。

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
| `ItemsSource` | 采样点的集合。 | `null` |
| `XPath` | 指向 X 坐标的路径。 | `null` |
| `YPath` | 指向 Y 坐标的路径。 | `null` |
| `ValuePath` | 指向标量值的路径。 | `null` |
| `ContourLevels` | 要计算的等值线层数。 | `8` |
| `ShowFill` | 是否填充等值线之间的区域。 | `true` |
| `ShowLines` | 是否绘制等值线。 | `true` |

## 另请参阅 {#see-also}

- [六边形分箱图](/controls/data-display/charts/engineering/hexbin-chart)
- [密度图](/controls/data-display/charts/statistical/density-plot-chart)
