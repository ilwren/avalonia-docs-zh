---
id: pyramid-chart
title: 金字塔图
description: 以层层堆叠的三角形版面同时体现层级与规模，常用于人口结构和销售管道的可视化。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsPyramid from '/img/controls/charts/charts-analytics-pyramid.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

金字塔图是堆叠面积图或条形图的一种，同时体现层级与规模。呈现人口结构和销售管道时，它是经典之选。

<Image light={chartsAnalyticsPyramid} maxWidth={400} position="center" cornerRadius="true" alt="Pyramid chart with stacked triangular segments representing hierarchical population or pipeline data." />

## 适用场景 {#when-to-use}
- **人口金字塔**：展示某地区的年龄与性别分布。
- **销售管道**：呈现从线索到成交的漏斗。
- **生物层级**：展示生态系统中的能量流动或物种分布。

## 代码示例 {#code-example}

### XAML
```xml
<PyramidChart xmlns="https://github.com/avaloniaui" Title="Population Distribution" Height="300"
                       ItemsSource="{Binding PyramidData}"
                       LabelPath="Age" ValuePath="Value"/>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record PyramidItem(string Age, double Value);

public ObservableCollection<PyramidItem> PyramidData { get; } = new()
{
    new("0-14", 15),
    new("15-24", 12),
    new("25-54", 40),
    new("55-64", 18),
    new("65+", 15)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 数据层的集合。 | `null` |
| `ValuePath` | 每一层的量值。 | `null` |
| `LabelPath` | 每一层的文字说明。 | `null` |
| `SegmentGap` | 各层之间的垂直距离。 | `2.0` |
| `ShowLabels` | 是否在各段上显示标签。 | `true` |
| `ShowValues` | 是否在图表上显示数值。 | `true` |
| `IsHighlightEnabled` | 为金字塔各段启用悬停高亮。 | `false` |
