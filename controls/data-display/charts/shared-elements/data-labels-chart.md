---
id: data-labels-chart
title: 数据标签
description: 把实际数值直接标在图表系列的各元素上，读者不必再凭坐标轴位置去估算。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFeaturesLabels from '/img/controls/charts/charts-datalabel.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

数据标签把实际数值直接标在图表系列上。这样读者无需凭坐标轴位置估算，就能直接比较各个数值。

<Image light={chartsFeaturesLabels} maxWidth={400} position="center" cornerRadius="true" alt="Bar chart with data labels displayed above each quarterly revenue bar." />

## 适用场景 {#when-to-use}
- **演示图表**：以清晰、即时呈现数值为先。
- **小倍数图**：为节省空间而略去坐标轴时。
- **关键里程碑**：凸显那些需要特别留意的数值。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="BasicLabelsChart" Height="250">
                        <CartesianChart.Series>
                            <BarSeries Title="Sales" ItemsSource="{Binding SalesData}"
                                                CategoryPath="Category" ValuePath="Value"
                                                ShowLabels="True" LabelOffset="5"/>
                        </CartesianChart.Series>
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis Title="Quarter" />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis Title="Revenue" />
                        </CartesianChart.VerticalAxis>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record SalesPoint(string Category, double Value);

public ObservableCollection<SalesPoint> SalesData { get; } = new()
{
    new("Q1", 120),
    new("Q2", 150),
    new("Q3", 180),
    new("Q4", 220)
};
```

## 公共属性（位于 Series 上） {#common-properties-on-series}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ShowLabels` | 开关系列各数据点上的数值。 | `false` |
| `LabelFormat` | 字符串格式。`{0}` 是数值，`{1}` 是类别。 | `"{0:N0}"` |
| `LabelFontSize` | 文字大小，单位为像素。 | `12.0` |
| `LabelForeground` | 文字颜色所用的画刷。 | `null` |
| `LabelBackground` | 标签文字背后所用的画刷。 | `null` |
| `LabelCornerRadius` | 标签背景的圆角半径。 | `4` |
| `LabelPadding` | 标签背景内部的内边距。 | `4,2` |
| `LabelOffset` | 标签与数据点之间的距离。 | `10.0` |
