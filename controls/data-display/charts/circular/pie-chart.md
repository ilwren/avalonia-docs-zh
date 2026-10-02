---
id: pie-chart
title: 饼图
description: 划分成若干扇形的圆形图表，用来表示数值占比；类别不多的「部分与整体」关系用它最合适。
doc-type: reference
tags:
  - avalonia pro
---

import chartsPie from '/img/controls/charts/charts-pie.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

饼图是划分成若干扇形的圆形图表，用来表示数值的占比。呈现部分与整体的关系时，它效果最好。

<Image light={chartsPie} maxWidth={400} position="center" cornerRadius="true" alt="Pie chart divided into colored sectors showing proportional market share across a small number of categories." />

## 适用场景 {#when-to-use}
- **占比**：呈现各类别相对总量的大小。
- **类别有限**：控制在 2 到 6 个类别之内，可读性最佳。
- **构成**：展示总量如何在各部分之间分配。

## 代码示例 {#code-example}

### XAML
```xml
<PieChart xmlns="https://github.com/avaloniaui" Name="PieChartSample" IsTooltipEnabled="True" Title="Market Share" Height="300">
                        <PieChart.Series>
                            <PieSeries ItemsSource="{Binding PieChartData}" LabelPath="Value" />
                        </PieChart.Series>
                    </PieChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<double> PieChartData { get; } = new()
{
    35, 25, 20, 15, 5
};
```

## 常用属性 {#common-properties}

### PieChart

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `InnerRadiusFactor` | 当某个 `PieSeries` 没有设置自己的内半径时所采用的中心孔洞大小。设为大于 `0.0` 的值即可做出[环形图](/controls/data-display/charts/circular/donut-chart)。 | `0.0` |
| `Palette` | 各扇区所用的自定义画刷集合。 | Auto-generated |

### PieSeries

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 数据项的集合。 | `null` |
| `ValuePath` | 指向扇区数值所用属性的路径。 | `null` |
| `LabelPath` | 指向扇区标签所用属性的路径。 | `null` |
| `RadiusFactor` | 系列的外半径系数，取值从 `0.0` 到 `1.0`。 | `0.9` |
| `InnerRadiusFactor` | 系列可选的内半径系数。为 `null` 时，采用图表级的取值。 | `null` |
| `StartAngle` | 首个扇区的起始角度，单位为度。 | `-90.0` |
| `ShowLabels` | 是否在扇区上显示标签。 | `true` |
| `LabelPosition` | 扇区标签的位置，`Inside` 或 `Outside`。 | `Inside` |
| `SliceLabelFormat` | 扇区标签所用的格式。 | `Percentage` |
| `LabelFontSize` | 扇区标签所用的字号。 | `11.0` |
| `LabelForeground` | 扇区标签所用的画刷。 | `null` |
