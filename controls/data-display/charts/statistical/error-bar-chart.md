---
id: error-bar-chart
title: 误差棒图
description: 为数据点添加误差指示来表现数据的波动，可呈现标准差、置信区间或测量不确定度。
doc-type: reference
tags:
  - avalonia pro
---

import chartsStatisticalErrorbar from '/img/controls/charts/charts-statistical-error.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

误差棒图用来表现数据的波动性，在图上标示出所报告测量值的误差或不确定度。

<Image light={chartsStatisticalErrorbar} maxWidth={400} position="center" cornerRadius="true" alt="Chart with data points and vertical error indicators showing standard deviation ranges for each sample." />

## 适用场景 {#when-to-use}
- **科学研究**：呈现标准差或置信区间。
- **质量管控**：呈现制造过程中的公差范围。
- **调查数据**：标明统计民调的误差幅度。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="ErrorBarChartSample" Title="Measurement Uncertainty" Height="250">
    <CartesianChart.HorizontalAxis><CategoryAxis /></CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis><NumericalAxis /></CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <ErrorBarSeries Title="Measurements"
                                 CategoryPath="Sample"
                                 ValuePath="Value"
                                 ErrorPath="Error"
                                 CapWidth="10"
                                 ShowMarkers="True"
                                 MarkerSize="8"
                                 ItemsSource="{Binding ErrorBarData}" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record ErrorBarItem(string Sample, double Value, double Error);

public ObservableCollection<ErrorBarItem> ErrorBarData { get; } = new()
{
    new("A", 45.0, 5.0),
    new("B", 62.0, 8.0),
    new("C", 38.0, 4.0),
    new("D", 75.0, 10.0),
    new("E", 55.0, 6.0)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 实测数据的集合。 | `null` |
| `ValuePath` | 中心值（均值/中位数）。 | `null` |
| `ErrorPath` | 对称误差量，在数值上下各延伸这么多。 | `null` |
| `LowErrorPath` | 非对称误差棒的下侧误差量。 | `null` |
| `HighErrorPath` | 非对称误差棒的上侧误差量。 | `null` |
| `ErrorMode` | 误差棒画在数值的上方、下方，还是两侧都画。 | `Both` |
| `CapWidth` | 误差棒两端横向封口的宽度。 | `8` |
| `ShowMarkers` | 是否在每个中心值处绘制标记。 | `false` |
| `MarkerSize` | 中心标记的大小。 | `8` |
| `Stroke` | 误差指示线的颜色。 | Theme-dependent |
