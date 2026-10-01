---
id: beeswarm-plot-chart
title: 蜂群图
description: 把每个类别中的各个观测值画成互不重叠的点，既保留了数据的疏密，又不像全随机抖动那样嘈杂。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

蜂群图在每个类别内部重新摆放各个点以避免重叠，同时如实保留各观测值的分布。

## 适用场景 {#when-to-use}

- **展示原始观测**：把每个点都画出来，而不只给出汇总统计量。
- **类别对比**：比较各组数据的离散程度和聚集情况。
- **分布细节**：把普通散点图会掩盖掉的密集堆叠显露出来。

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
| `ItemsSource` | 观测值的集合。 | `null` |
| `CategoryPath` | 指向分组类别的路径。 | `null` |
| `ValuePath` | 指向数值的路径。 | `null` |
| `PointRadius` | 每个点的半径。 | `5.0` |
| `Fill` | 填充数据点所用的画刷。 | `null` |
| `Stroke` | 数据点轮廓所用的画刷。 | `null` |
| `StrokeThickness` | 数据点轮廓的粗细。 | `1.0` |
| `ShowCategoryLabels` | 是否绘制类别标签。 | `true` |
| `ShowAxes` | 是否绘制数值轴。 | `true` |

## 另请参阅 {#see-also}

- [带状散点图](/controls/data-display/charts/statistical/strip-plot-chart)
- [小提琴图](/controls/data-display/charts/statistical/violin-plot-chart)
