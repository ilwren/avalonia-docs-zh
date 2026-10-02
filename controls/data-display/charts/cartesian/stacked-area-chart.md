---
id: stacked-area-chart
title: 堆叠面积图
description: 把多个面积系列层层叠放，呈现若干变量如何随时间汇聚成累计总量。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianStackedarea from '/img/controls/charts/charts-cartesian-stackedarea.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

堆叠面积图把多个面积系列层层叠放。要呈现若干变量如何随时间汇成总量，它最为合适。

<Image light={chartsCartesianStackedarea} maxWidth={400} position="center" cornerRadius="true" alt="Stacked area chart with multiple colored layers representing traffic sources stacked to show cumulative total." />

## 适用场景 {#when-to-use}
- **累加**：呈现一段时期内多个类别的总和。
- **构成随时间的变化**：展示总量的构成如何按时间推移而改变。
- **趋势对比**：比较各层之间的相对增长。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="StackedAreaChart" Title="Stacked Area Chart" Height="250" ShowLegend="True">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <StackedAreaSeries Title="Desktop"
                                  ItemsSource="{Binding StackedAreaDesktop}"
                                  Fill="#7E2196F3"
                                  Stroke="DodgerBlue" />
        <StackedAreaSeries Title="Mobile"
                                  ItemsSource="{Binding StackedAreaMobile}"
                                  Fill="#7E4CAF50"
                                  Stroke="Green" />
        <StackedAreaSeries Title="Tablet"
                                  ItemsSource="{Binding StackedAreaTablet}"
                                  Fill="#7EFF9800"
                                  Stroke="Orange" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> StackedAreaDesktop { get; } =
    new() { 500, 480, 520, 510, 490, 530, 550 };

public ObservableCollection<int> StackedAreaMobile { get; } =
    new() { 300, 350, 380, 420, 450, 480, 520 };

public ObservableCollection<int> StackedAreaTablet { get; } =
    new() { 100, 120, 130, 140, 150, 160, 170 };
```

## 常用属性（StackedAreaSeries） {#common-properties-stackedareaseries}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 系列名称。 | `null` |
| `ItemsSource` | 该层所用的数据集合。 | `null` |
| `Fill` | 这一层面积所用的画刷。 | Auto-generated |
| `FillOpacity` | 透明度（0.0 到 1.0）。 | `0.7` |
| `StackGroup` | 堆叠标识。取值相同的系列会叠在一起。 | `"default"` |
