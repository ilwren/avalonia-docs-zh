---
id: hexbin-chart
title: 六边形分箱图
description: 把密集的二维点云聚合成六边形分箱，既能看出聚集程度，又不会糊成一团。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

六边形分箱图把邻近的点归入一个个六边形，于是成千上万个点彼此重叠时，密集的散点数据依然清晰可读。

## 适用场景 {#when-to-use}

- **密集散点数据**：用密度分箱取代糊成一团的点云。
- **空间聚集**：呈现观测值在二维平面上聚在何处。
- **探索性分析**：不必平滑原始数据，就能看出热点和梯度。

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
| `ItemsSource` | X、Y 点的集合。 | `null` |
| `XPath` | 指向 X 值的路径。 | `null` |
| `YPath` | 指向 Y 值的路径。 | `null` |
| `HexRadius` | 每个六边形的半径，单位为像素。 | `20.0` |
| `ColorScale` | 用于编码密度的色阶。 | `Blues` |
| `ShowAxes` | 是否绘制图表的坐标轴。 | `true` |

## 另请参阅 {#see-also}

- [气泡图](/controls/data-display/charts/bubble/bubble-chart)
- [等值线图](/controls/data-display/charts/statistical/contour-plot-chart)
