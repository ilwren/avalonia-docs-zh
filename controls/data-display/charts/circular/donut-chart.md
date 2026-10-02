---
id: donut-chart
title: 环形图
description: 饼图的变体，中间留白，常在中心显示总计数值或标签以提高可读性。
doc-type: reference
tags:
  - avalonia pro
---

import chartsPieDonut from '/img/controls/charts/charts-pie-donut.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

环形图是[饼图](/controls/data-display/charts/circular/pie-chart)的一种变体，它的 `InnerRadiusFactor` 不为零。这样的设计让你可以把中心留给总计数值或标签。

<Image light={chartsPieDonut} maxWidth={400} position="center" cornerRadius="true" alt="Donut chart with a blank center hole showing proportional segments of revenue distribution by source." />

## 适用场景 {#when-to-use}
- **占比对比**：与饼图类似，但中心有更多地方放标签或总计。
- **摘要视图**：中心的空白可以用来显示总和或某项关键指标。
- **极简仪表板**：类别不多的「部分与整体」图示，用它效果极佳。

## 代码示例 {#code-example}

### XAML
```xml
<PieChart xmlns="https://github.com/avaloniaui" Name="DonutChartSample" IsTooltipEnabled="True" Title="Revenue Distribution" Height="300" InnerRadiusFactor="0.6">
                         <PieChart.Series>
                            <PieSeries ItemsSource="{Binding DonutChartData}" LabelPath="Value" />
                        </PieChart.Series>
                    </PieChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<double> DonutChartData { get; } = new()
{
    40, 30, 20, 10
};
```

框架中并没有专门的 `DonutChart` 控件。请使用 `PieChart`，并把 `InnerRadiusFactor` 设为大于 `0.0` 的值。

## 常用属性 {#common-properties}

### PieChart

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `InnerRadiusFactor` | 中心孔洞的大小，取值从 `0.0` 到 `1.0`。 | `0.0` |
| `Title` | 显示在圆环上方的图表标题。 | `null` |
| `Palette` | 各扇区所用的自定义画刷集合。 | Theme-dependent |

### PieSeries

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 各数据扇区的集合。 | `null` |
| `LabelPath` | 指向显示在扇区上或扇区旁的文本的路径。 | `null` |
| `ValuePath` | 指向决定扇区大小那个数值的路径。 | `null` |
| `RadiusFactor` | 系列的外半径系数，取值从 `0.0` 到 `1.0`。 | `0.9` |
| `InnerRadiusFactor` | 系列可选的内半径系数。为 `null` 时，采用图表级的取值。 | `null` |
| `StartAngle` | 首个扇区的起始角度，单位为度。 | `-90.0` |
| `ShowLabels` | 是否在扇区上显示标签。 | `true` |
| `LabelPosition` | 扇区标签的位置，`Inside` 或 `Outside`。 | `Inside` |
| `SliceLabelFormat` | 扇区标签所用的格式。 | `Percentage` |
| `LabelFontSize` | 扇区标签所用的字号。 | `11.0` |
| `LabelForeground` | 扇区标签所用的画刷。 | `null` |
