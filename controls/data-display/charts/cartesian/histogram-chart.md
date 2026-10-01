---
id: histogram-chart
title: 直方图
description: 把连续数据分入若干区间，并显示每个区间内数据点的频数，用以揭示单一变量的分布。
doc-type: reference
tags:
  - avalonia pro
---

import chartsStatisticalHistogram from '/img/controls/charts/charts-statistical-histogram.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

直方图把连续数据分入一个个「区间」，并显示每个区间内数据点的频数。要搞清楚单一变量的分布，少不了它。

<Image light={chartsStatisticalHistogram} maxWidth={400} position="center" cornerRadius="true" alt="Histogram chart grouping continuous data into bins showing the frequency distribution of values." />

## 适用场景 {#when-to-use}
- **年龄分布**：呈现落在各个年龄段的用户有多少。
- **性能日志**：分析系统响应时间的频数分布。
- **质量管控**：评估产品尺寸或重量的离散程度。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="HistogramSample" Title="Score Distribution" Height="250">
                        <CartesianChart.HorizontalAxis><CategoryAxis /></CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis><NumericalAxis /></CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <HistogramSeries ItemsSource="{Binding HistogramData}" ValuePath="Score" BinCount="10" />
                        </CartesianChart.Series>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
using System;
using System.Linq;

public record HistogramItem(double Score);

public ObservableCollection<HistogramItem> HistogramData { get; } = CreateScores();

private static ObservableCollection<HistogramItem> CreateScores()
{
    var random = new Random(42);

    return new ObservableCollection<HistogramItem>(
        Enumerable.Range(0, 50)
            .Select(_ => new HistogramItem(50 + random.NextDouble() * 50)));
}
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 原始数据点的集合。 | `null` |
| `ValuePath` | 指向待分区间的数值属性的路径。 | `null` |
| `BinCount` | 要划分出多少根条形（区间）。 | `10` |
| `BinWidth` | （可选）每个区间的显式宽度；设置后会覆盖 BinCount。 | `null` |
| `Fill` | 频数条形所用的画刷。 | Theme-dependent |
| `BarWidth` | 每根直方图条形的宽度，以区间宽度的比例表示。 | `0.9` |
| `BarCornerRadius` | 直方图条形的圆角半径。 | `CornerRadius(2,2,0,0)` |
