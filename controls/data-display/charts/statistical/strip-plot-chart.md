---
id: strip-plot-chart
title: 带状散点图
description: 按类别呈现各个观测值，并施加可控的抖动偏移，适合比较原始取值并叠加均值线。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

带状散点图把每个类别中的所有观测值都画出来，用抖动偏移减少重叠，并可叠加均值线来标示中心位置。

## 适用场景 {#when-to-use}

- **展示原始样本**：把每个点都画出来，而不只给出四分位数或平均值。
- **类别离散度**：比较各组数值聚得紧还是散得开。
- **混合视图**：把原始观测值与一条简单的均值参考线结合起来。

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
| `ItemsSource` | 观测值的集合。 | `null` |
| `CategoryPath` | 指向分组类别的路径。 | `null` |
| `ValuePath` | 指向数值的路径。 | `null` |
| `PointRadius` | 每个点的半径。 | `4.0` |
| `JitterAmount` | 在每个类别内部施加的横向抖动系数。 | `0.3` |
| `Fill` | 填充数据点所用的画刷。 | `null` |
| `Stroke` | 数据点轮廓所用的画刷。 | `null` |
| `StrokeThickness` | 数据点轮廓的粗细。 | `0.5` |
| `PointOpacity` | 所绘数据点的不透明度。 | `0.7` |
| `ShowCategoryLabels` | 是否绘制类别标签。 | `true` |
| `ShowAxes` | 是否绘制数值轴。 | `true` |
| `ShowMeanLine` | 是否为每个类别绘制均值线。 | `true` |

## 另请参阅 {#see-also}

- [蜂群图](/controls/data-display/charts/statistical/beeswarm-plot-chart)
- [箱线图](/controls/data-display/charts/statistical/boxplot-chart)
