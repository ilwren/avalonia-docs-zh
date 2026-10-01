---
id: bar-chart
title: 条形图
description: 用长度与数值成正比的矩形条来表示数据，便于比较各类别之间的离散数量。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianBar from '/img/controls/charts/charts-cartesian-bar.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

条形图用矩形条表示数据，条的长度与它所代表的数值成正比。

<Image light={chartsCartesianBar} maxWidth={400} position="center" cornerRadius="true" alt="Bar chart with vertical rectangular bars of varying heights comparing quarterly revenue across categories." />

## 适用场景 {#when-to-use}
- **对比**：比较不同类别之间的离散数量。
- **排名**：看出哪些类别数值最高、哪些最低。
- **分类数据**：数据被划分为彼此独立、非连续的若干组时。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="BarChart" Title="Bar Chart" Height="250">
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis />
                        </CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <BarSeries Title="Sales" ItemsSource="{Binding BarSeriesData}" Fill="DodgerBlue" />
                        </CartesianChart.Series>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> BarSeriesData { get; } = new()
{
    150, 180, 165, 190, 175, 200
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例中显示的系列名称。 | `null` |
| `ItemsSource` | 要显示的数据项集合。 | `null` |
| `CategoryPath` | 指向 X 轴所用属性的路径。 | `null` |
| `ValuePath` | 指向 Y 轴所用属性的路径。 | `null` |
| `Fill` | 填充条形所用的颜色/画刷。 | Theme-dependent |
| `Stroke` | 条形的轮廓颜色。 | `Transparent` |
| `ColorByPoint` | 每根条形是否各用调色板中的一种颜色。 | `false` |
| `BarCornerRadius` | 条形的圆角程度。 | `0` |
| `BarWidth` | 每根条形的宽度，以类别带宽的比例表示（0.0 到 1.0）。 | `0.7` |
