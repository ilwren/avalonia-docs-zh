---
id: boxplot-chart
title: 箱线图
description: 用箱体加须线的形式概括数据分布，呈现中位数、四分位数和异常值，适合作统计对比。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianBoxplot from '/img/controls/charts/charts-cartesian-boxplot.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

箱线图（又称箱须图）以图形方式概括数据的分布、集中趋势和离散程度，并一并给出四分位数和异常值。

<Image light={chartsCartesianBoxplot} maxWidth={400} position="center" cornerRadius="true" alt="Box plot chart with box-and-whisker symbols per category showing median, quartiles, and outlier data points." />

## 适用场景 {#when-to-use}
- **统计分析**：比较多组数据的分布（比如不同班级的考试成绩）。
- **异常值检测**：找出落在「须线」之外的极端数据点。
- **区间呈现**：一眼看清最小值、最大值、中位数和四分位距。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="BoxPlotSample" Title="Box Plot (Box and Whisker)" Height="250">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <BoxPlotSeries Title="Distribution"
                                ItemsSource="{Binding BoxPlotData}"
                                CategoryPath="Category"
                                MinPath="Min" Q1Path="Q1" MedianPath="Median" Q3Path="Q3" MaxPath="Max"
                                Fill="#7E9C27B0" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record BoxPlotPoint(string Category, double Min, double Q1, double Median, double Q3, double Max);

public ObservableCollection<BoxPlotPoint> BoxPlotData { get; } = new()
{
    new("Q1", 10, 25, 35, 45, 60),
    new("Q2", 15, 30, 42, 55, 70),
    new("Q3", 20, 35, 48, 60, 75),
    new("Q4", 25, 40, 52, 65, 80)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 统计数据点的集合。 | `null` |
| `MinPath` | 指向最小值的路径。 | `null` |
| `MaxPath` | 指向最大值的路径。 | `null` |
| `MedianPath` | 指向中位数的路径。 | `null` |
| `Q1Path` | 指向第一四分位数（第 25 百分位）的路径。 | `null` |
| `Q3Path` | 指向第三四分位数（第 75 百分位）的路径。 | `null` |
| `BoxWidth` | 箱体的宽度，以类别槽位的比例表示。 | `0.6` |
| `MedianStroke` | 箱体内中位数线所用的画刷。 | `null` |
| `WhiskerThickness` | 须线的粗细。 | `1.0` |
| `Fill` | 「箱体」所用的画刷。 | Theme-dependent |
| `Stroke` | 须线和箱体轮廓的颜色。 | Theme-dependent |
