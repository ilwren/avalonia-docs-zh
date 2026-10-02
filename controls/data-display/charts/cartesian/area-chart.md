---
id: area-chart
title: 面积图
description: 在折线图的基础上，为折线下方的区域填上颜色或渐变，强调变化随时间的量级。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianArea from '/img/controls/charts/charts-cartesian-area.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

面积图以折线图为基础，坐标轴与折线之间的区域会填上颜色或渐变，用以强调变化随时间的量级。

<Image light={chartsCartesianArea} maxWidth={400} position="center" cornerRadius="true" alt="Area chart showing website traffic data with a gradient fill between the line and the horizontal axis." />

## 适用场景 {#when-to-use}
- **累计总量**：呈现各组成部分如何随时间汇聚成整体。
- **体量**：强调数据点的总量或量级。
- **视觉反差**：比单纯的折线图更有辨识度。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="AreaChart" Title="Area Chart" Height="250">
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis />
                        </CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <AreaSeries Title="Revenue" ItemsSource="{Binding AreaSeriesData}" Fill="#7E4CAF50" Stroke="Green" StrokeThickness="2" />
                        </CartesianChart.Series>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> AreaSeriesData { get; } = new()
{
    120, 150, 135, 180, 165, 200, 185, 220
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 系列名称。 | `null` |
| `ItemsSource` | 数据项的集合。 | `null` |
| `Stroke` | 顶部折线的颜色。 | Theme-dependent |
| `Fill` | 填充折线下方区域所用的画刷。 | Theme-dependent |
| `FillOpacity` | 填充的透明度（0.0 到 1.0）。 | `0.5` |
| `StrokeThickness`| 线条的粗细。 | `2` |
