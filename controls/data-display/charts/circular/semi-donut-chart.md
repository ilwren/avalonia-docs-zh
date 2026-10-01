---
id: semi-donut-chart
title: 半环形图
description: 在 180 度的弧上呈现占比数据，常用于仪表板中的进度表和摘要指标，不必占满整个圆。
doc-type: reference
tags:
  - avalonia pro
---

import chartsPieSemidonut from '/img/controls/charts/charts-pie-semidonut.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

半环形图在 180 度的弧上呈现数据。在仪表板设计中，它尤其常用于衡量进度，或在局促的空间里展示摘要指标。

<Image light={chartsPieSemidonut} maxWidth={400} position="center" cornerRadius="true" alt="Semi-donut chart displayed as a 180-degree arc with colored segments and a center label showing a summary metric." />

## 适用场景 {#when-to-use}
- **KPI 进度表**：呈现单项指标相对目标或总量的完成情况。
- **Dashboard headers**: Providing a quick summary of a category at the top of a page.
- **Angular comparison**: Comparing parts of a whole where a full circle isn't needed or desired.

## 代码示例 {#code-example}

### XAML
```xml
<SemiDonutChart xmlns="https://github.com/avaloniaui" Name="SemiDonutChartSample" Height="200"
                         ItemsSource="{Binding SemiDonutChartData}"
                         ValuePath="Value"
                         LabelPath="Label"
                         CenterValue="$980"
                         CenterLabel="Total Revenue" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record SemiDonutPoint(string Label, double Value);

public ObservableCollection<SemiDonutPoint> SemiDonutChartData { get; } = new()
{
    new("Product A", 450),
    new("Product B", 320),
    new("Product C", 210)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | The data source for the segments. | `null` |
| `ValuePath` | Property path for values. | `null` |
| `LabelPath` | Property path for labels. | `null` |
| `InnerRadiusFactor`| The ratio of the inner radius (hole size) to the outer radius (0.0 to 1.0). | `0.6` |
| `CenterLabel` | Label text displayed in the center of the arc. | `null` |
| `CenterValue` | Value text displayed in the center. | `null` |
| `GapAngle` | Gap angle between segments in degrees. | `2.0` |
| `IsHighlightEnabled` | Enables hover highlighting for segments. | `false` |
