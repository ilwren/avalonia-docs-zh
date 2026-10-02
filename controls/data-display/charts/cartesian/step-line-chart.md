---
id: step-line-chart
title: 阶梯折线图
description: 用横线和竖线以阶梯状连接数据点，表示数值在各区间之间保持不变。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianStepline from '/img/controls/charts/charts-cartesian-stepline.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

阶梯折线图用横线和竖线连接数据点，形成阶梯状的走势。要展现在离散时点上发生的变化，它很合适。

<Image light={chartsCartesianStepline} maxWidth={400} position="center" cornerRadius="true" alt="Step line chart connecting data points with horizontal and vertical segments as values change at numeric intervals." />

## 适用场景 {#when-to-use}
- **价格变动**：呈现利率、价格档位或库存水平。
- **离散跃迁**：数值在相邻数据点之间保持不变时。
- **数字信号**：表示二值或基于状态的数据。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="StepLineChart" Title="Step Line Chart" Height="250">
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis />
                        </CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <StepLineSeries Title="Price" ItemsSource="{Binding StepLineSeriesData}" Stroke="Teal" StrokeThickness="2" MarkerSize="6"  ShowMarkers="True"/>
                        </CartesianChart.Series>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> StepLineSeriesData { get; } =
    new() { 100, 100, 120, 120, 120, 140, 140, 160 };
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 系列名称。 | `null` |
| `ItemsSource` | 数据项的集合。 | `null` |
| `CategoryPath` | 指向 X 轴数值所用属性的路径。 | `null` |
| `ValuePath` | 指向 Y 轴数值所用属性的路径。 | `null` |
| `Stroke` | 阶梯线的颜色。 | Theme-dependent |
| `StrokeThickness` | 线条的粗细。 | `2` |
| `ShowMarkers` | 是否在每个数据点处显示标记。只有它为 `true` 时，标记的样式设置才看得出效果。 | `false` |
| `MarkerSize` | 标记的大小，单位为像素。 | `6` |
| `MarkerShape` | 标记的形状，比如 `Circle` 或 `Square`。 | `Circle` |
| `MarkerFill` | 填充标记所用的画刷。 | `null` |
| `MarkerStroke` | 标记轮廓所用的画刷。 | `null` |
| `MarkerStrokeThickness` | 标记轮廓的粗细。为 `NaN` 时，使用系列的 `StrokeThickness`。 | `NaN` |
| `StepMode` | `HorizontalFirst`, `VerticalFirst`, or `Center`. | `HorizontalFirst` |
