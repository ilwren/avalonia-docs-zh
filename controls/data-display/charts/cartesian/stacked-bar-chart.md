---
id: stacked-bar-chart
title: 堆叠条形图
description: 把多个数据系列叠进同一根条形，既能比较各类别的总量，也能看清内部构成。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianStackedbar from '/img/controls/charts/charts-cartesian-stackedbar.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

堆叠条形图把多个数据系列叠放在一起，让人既能比较总量，又能看清各组成部分。

<Image light={chartsCartesianStackedbar} maxWidth={400} position="center" cornerRadius="true" alt="Stacked bar chart with colored segments stacked in each bar showing regional sales contributions per quarter." />

## 适用场景 {#when-to-use}
- **部分与整体**：呈现一个较大的类别总量由多少个小部分构成。
- **分类对比**：比较各组的总量，同时看清各自内部的分布。
- **节省版面**：不必为每个数据系列单独画一根条形。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="StackedBarChart" Title="Stacked Bar Chart" Height="250" ShowLegend="True">
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis />
                        </CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <StackedBarSeries Title="Product A" ItemsSource="{Binding StackedBarProductA}" Fill="DodgerBlue" />
                            <StackedBarSeries Title="Product B" ItemsSource="{Binding StackedBarProductB}" Fill="Orange" />
                            <StackedBarSeries Title="Product C" ItemsSource="{Binding StackedBarProductC}" Fill="Green" />
                        </CartesianChart.Series>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> StackedBarProductA { get; } = new()
{
    40, 55, 50, 60, 45, 70
};

public ObservableCollection<int> StackedBarProductB { get; } = new()
{
    30, 35, 40, 45, 35, 50
};

public ObservableCollection<int> StackedBarProductC { get; } = new()
{
    20, 25, 30, 25, 30, 35
};
```

## 常用属性（StackedBarSeries） {#common-properties-stackedbarseries}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例中显示的名称。 | `null` |
| `ItemsSource` | 堆叠中这一部分所用的数据集合。 | `null` |
| `CategoryPath` | 指向各条形共享的类别值的路径。 | `null` |
| `ValuePath` | 指向本系列数值的路径。 | `null` |
| `Fill` | 本系列这一段的背景色。 | Auto-generated |
| `StackGroup` | 用于把相关系列堆叠在一起的标识。 | `"default"` |
| `BarWidth` | 每根条形的宽度，以可用槽位的比例表示。 | `0.7` |
| `BarCornerRadius` | 条形各段的圆角程度。 | `0` |
