---
id: scatter-chart
title: 散点图
description: 用两个数值变量把数据点绘成散布的圆点，借以揭示数据集中的相关性、分布和异常值。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianScatter from '/img/controls/charts/charts-cartesian-scatter.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

散点图用圆点表示两个不同数值变量的取值。要展示和比较科学、统计、工程等领域的数值数据，少不了它。

<Image light={chartsCartesianScatter} maxWidth={400} position="center" cornerRadius="true" alt="Scatter chart plotting individual data points as dots across two numeric axes to reveal correlations." />

## 适用场景 {#when-to-use}
- **相关性**：辨识两个变量之间的关系（比如身高与体重）。
- **分布**：呈现数据点的离散与聚集情况。
- **异常检测**：一眼看出远离常规的数据点。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="ScatterChart" Title="Scatter Plot" Height="250">
    <CartesianChart.HorizontalAxis>
        <NumericalAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <ScatterSeries Title="Data Points"
                              ItemsSource="{Binding ScatterSeriesData}"
                              Fill="Purple"
                              MarkerSize="10"
                              MarkerShape="Circle" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> ScatterSeriesData { get; } =
    new() { 25, 45, 35, 55, 40, 60, 50, 70, 55, 75 };
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 系列名称。 | `null` |
| `ItemsSource` | 数据点的集合。 | `null` |
| `CategoryPath` | 类别路径（X 轴）所取的值。 | `null` |
| `ValuePath` | 数值路径（Y 轴）所取的值。 | `null` |
| `ShowMarkers` | 是否显示数据点标记。 | `true` |
| `MarkerSize` | 圆点的大小，单位为像素。 | `8` |
| `MarkerShape` | 圆点的形状，比如 `Circle` 或 `Square`。 | `Circle` |
| `MarkerFill` | 填充标记所用的画刷。为 `null` 时，使用 `Fill`。 | `null` |
| `MarkerStroke` | 标记轮廓所用的画刷。 | `null` |
| `MarkerStrokeThickness` | 标记轮廓的粗细。为 `NaN` 时，使用系列的 `StrokeThickness`。 | `NaN` |
| `Fill` | 散点圆点的颜色。 | Theme-dependent |

## 带连线的散点图变体 {#scatter-line-variant}

`ScatterLineSeries` 在散点图的基础上，在数据点之间画出连线，既保留了散点的清晰可辨，又能看出折线所呈现的趋势。

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="ScatterChart" Title="Scatter Plot" Height="250">
                        <CartesianChart.HorizontalAxis>
                            <NumericalAxis />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis />
                        </CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <ScatterLineSeries Title="Data Points" ItemsSource="{Binding ScatterSeriesData}" Fill="Purple" MarkerSize="10" MarkerShape="Circle" />
                        </CartesianChart.Series>
                    </CartesianChart>
```

### ScatterLineSeries 属性 {#scatterlineseries-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ShowLines` | 是否在各散点之间显示连线。 | `true` |
| `StrokeDashStyle` | 连线的虚线样式。为 `null` 时为实线。 | `null` |
| `ShowMarkers` | 是否显示数据点标记。 | `true` |
| `MarkerSize` | 标记的大小，单位为像素。 | `8` |
| `MarkerShape` | 标记的形状，比如 `Circle` 或 `Square`。 | `Circle` |
| `MarkerFill` | 填充标记所用的画刷。为 `null` 时，使用 `Fill`。 | `null` |
| `MarkerStroke` | 标记轮廓所用的画刷。 | `null` |
| `MarkerStrokeThickness` | 标记轮廓的粗细。为 `NaN` 时，使用系列的 `StrokeThickness`。 | `NaN` |

## 另请参阅 {#see-also}

- [折线图](/controls/data-display/charts/cartesian/line-chart)
- [点图](/controls/data-display/charts/cartesian/dot-plot-chart)
- [组合图](/controls/data-display/charts/cartesian/combo-chart)
