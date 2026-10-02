---
id: pareto-chart
title: 帕累托图
description: 依照二八法则，把递减的条形与累计折线结合起来，凸显最关键的那几个因素。
doc-type: reference
tags:
  - avalonia pro
---

import chartsStatisticalPareto from '/img/controls/charts/charts-statistical-pareto.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

帕累托图同时包含条形和折线：各项数值按降序以条形呈现，累计总量则由折线表示。

<Image light={chartsStatisticalPareto} maxWidth={400} position="center" cornerRadius="true" alt="Pareto chart with descending bars and a cumulative percentage line highlighting the most significant factors." />

## 适用场景 {#when-to-use}
- **质量管控**：找出造成缺陷的「关键少数」（二八法则）。
- **资源管理**：锁定哪些类别吃掉了大部分成本。
- **客户服务**：分析哪类投诉最为频繁。

## 代码示例 {#code-example}

### XAML
```xml
<ParetoChart xmlns="https://github.com/avaloniaui" Name="ParetoChartSample"
                                          Title="Defect Analysis"
                                          Height="250"
                                          ValuePath="Count"
                                          LabelPath="Defect"
                                          ItemsSource="{Binding ParetoData}" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record ParetoItem(string Defect, int Count);

public ObservableCollection<ParetoItem> ParetoData { get; } = new()
{
    new("Missing Parts", 45),
    new("Surface Damage", 30),
    new("Wrong Size", 20),
    new("Color Error", 15),
    new("Other", 10)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 类别的集合。 | `null` |
| `ValuePath` | 决定条形高度的属性。 | `null` |
| `LabelPath` | 表示类别名称的属性。 | `null` |
| `BarBrush` | 递减条形所用的画刷。 | `#1976D2` |
| `LineBrush` | 累计百分比折线所用的画刷。 | `#F44336` |
| `BarWidth` | 每根条形的宽度，以类别宽度的比例表示。 | `0.7` |
| `ShowCumulativeLine` | 开关累计百分比折线及其标记点。 | `true` |
| `IsHighlightEnabled` | 为帕累托条形启用悬停高亮。 | `false` |
