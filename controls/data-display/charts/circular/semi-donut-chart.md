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
- **仪表板页首**：在页面顶端快速交代某个类别的概况。
- **角度对比**：比较整体中的各部分，而又不必、也不想画满一整个圆。

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
| `ItemsSource` | 各扇段的数据源。 | `null` |
| `ValuePath` | 数值所对应的属性路径。 | `null` |
| `LabelPath` | 标签所对应的属性路径。 | `null` |
| `InnerRadiusFactor`| 内半径（孔洞大小）与外半径之比（0.0 到 1.0）。 | `0.6` |
| `CenterLabel` | 显示在弧心的标签文字。 | `null` |
| `CenterValue` | 显示在弧心的数值文字。 | `null` |
| `GapAngle` | 各扇段之间的间隔角度，单位为度。 | `2.0` |
| `IsHighlightEnabled` | 为各扇段启用悬停高亮。 | `false` |
