---
id: slope-chart
title: 斜率图
description: 比较多个实体在恰好两个时间点或两个类别之间的数值，凸显谁上升、谁下降、谁原地不动。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsSlope from '/img/controls/charts/charts-statistical-slope.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

斜率图比较多个实体在两个时间点（或两个类别）上的情况。要呈现两种状态之间名次或数值的变化，它最为合适。

<Image light={chartsAnalyticsSlope} maxWidth={400} position="center" cornerRadius="true" alt="Slope chart comparing entity values between two time points with labeled lines showing which increased or decreased." />

## 适用场景 {#when-to-use}
- **前后对比**：展示某项政策或事件对不同群体的影响。
- **名次变动**：呈现产品人气在两个季度之间的此消彼长。
- **两种状态对比**：凸显哪些实体有所改善、哪些有所下滑。

## 代码示例 {#code-example}

### XAML
```xml
<SlopeChart xmlns="https://github.com/avaloniaui" Name="SlopeChartSample"
                                         Title="Before vs After"
                                         Height="300"
                                         LabelPath="Label"
                                         StartValuePath="Before"
                                         EndValuePath="After"
                                         IsCurved="True"
                                         ShowGridLines="True"
                                         ShowXAxis="True"
                                         ItemsSource="{Binding SlopeData}" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record SlopeItem(string Label, double Before, double After);

public ObservableCollection<SlopeItem> SlopeData { get; } = new()
{
    new("Sales", 100.0, 150.0),
    new("Cost", 80.0, 70.0),
    new("Profit", 20.0, 80.0)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 要作比较的项的集合。 | `null` |
| `LabelPath` | 指向实体名称的路径。 | `null` |
| `StartValuePath` | 指向左侧第一个数值的路径。 | `null` |
| `EndValuePath` | 指向右侧第二个数值的路径。 | `null` |
| `StartLabel` | 左侧显示的标签。 | `"Before"` |
| `EndLabel` | 右侧显示的标签。 | `"After"` |
| `StrokeThickness` | 连线的粗细。 | `2.0` |
| `MarkerSize` | 每条线首尾标记点的大小。 | `8.0` |
| `ShowLabels` | 开关首尾两端的数值标签。 | `true` |
| `IsCurved` | 用曲线代替直线作为连线。 | `false` |
| `ShowGridLines` | 是否为起止位置绘制参考线。 | `false` |
| `ShowXAxis` | 是否绘制底部坐标轴，并把两侧标签移到图表下方。 | `false` |
| `IsHighlightEnabled` | 为斜率连线启用悬停高亮。 | `false` |
