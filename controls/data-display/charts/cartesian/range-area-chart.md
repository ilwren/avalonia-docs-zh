---
id: range-area-chart
title: 区间面积图
description: 为每个类别绘制一条连接高低值的填充带，适合呈现不确定性、价格区间或气温范围。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianRangearea from '/img/controls/charts/charts-cartesian-rangearea.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

区间面积图为每个类别绘制一条连接高、低两个数值的填充带，可用来呈现不确定性、价格区间、气温变化等各类范围数据。

<Image light={chartsCartesianRangearea} maxWidth={400} position="center" cornerRadius="true" alt="Range area chart with a filled band between high and low temperature values across days of the week." />

## 适用场景 {#when-to-use}
- **误差范围**：展示均值周围的置信区间或误差范围。
- **价格区间**：用一个系列同时呈现每日的最高价和最低价。
- **气温范围**：展示一段时期内的最低温与最高温。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="RangeAreaChart" Title="Range Area Chart" Height="250">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <AreaRangeSeries Title="Temperature Range"
                                ItemsSource="{Binding RangeAreaData}"
                                LowPath="Low"
                                HighPath="High"
                                CategoryPath="Category"
                                Fill="#7EE91E63"
                                Stroke="DeepPink"
                                StrokeThickness="2" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record CategoryRangePoint(string Category, double Low, double High);

public ObservableCollection<CategoryRangePoint> RangeAreaData { get; } = new()
{
    new("Jan", 5, 15),
    new("Feb", 8, 18),
    new("Mar", 12, 25),
    new("Apr", 18, 30),
    new("May", 22, 35),
    new("Jun", 20, 32),
    new("Jul", 15, 28)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 系列名称。 | `null` |
| `ItemsSource` | 区间数据点的集合。 | `null` |
| `CategoryPath` | 指向 X 轴类别属性的路径。 | `null` |
| `HighPath` | 指向最大值属性的路径。 | `null` |
| `LowPath` | 指向最小值属性的路径。 | `null` |
| `Fill` | 填充两点之间区域所用的画刷。 | Theme-dependent |
| `Stroke` | 边界线所用的画刷。 | Theme-dependent |
| `ShowLines` | 是否绘制上下边界线。 | `true` |
| `FillOpacity` | 高低值之间填充带的不透明度。 | `0.5` |
