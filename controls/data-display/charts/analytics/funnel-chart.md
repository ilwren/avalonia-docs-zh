---
id: funnel-chart
title: 漏斗图
description: 呈现数据在一条线性流程中逐级递减的过程，便于找出管道中的瓶颈。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsFunnel from '/img/controls/charts/charts-analytics-funnel.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

漏斗图呈现数据从一个阶段流向下一个阶段时逐级递减的过程。用它来找出线性流程中的瓶颈。

<Image light={chartsAnalyticsFunnel} maxWidth={400} position="center" cornerRadius="true" alt="Funnel chart showing progressive reduction of data through sales pipeline stages from leads to closed sales." />

## 适用场景 {#when-to-use}
- **销售管道**：追踪潜在客户从线索到成交的全过程。
- **转化率**：监测网站访客走完结账流程的情况。
- **招聘**：呈现候选人在招聘各环节的分布。

## 代码示例 {#code-example}

### XAML
```xml
<FunnelChart xmlns="https://github.com/avaloniaui" Title="Sales Pipeline" Height="300"
                      ItemsSource="{Binding FunnelData}"
                      LabelPath="Stage" ValuePath="Value"/>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record FunnelItem(string Stage, double Value);

public ObservableCollection<FunnelItem> FunnelData { get; } = new()
{
    new("Visitors", 1000),
    new("Leads", 500),
    new("Qualified", 200),
    new("Proposal", 80),
    new("Closed", 30)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 显示在顶部的名称。 | `null` |
| `ItemsSource` | 流程各阶段的集合。 | `null` |
| `ValuePath` | 指向各阶段数量属性的路径。 | `null` |
| `LabelPath` | 指向阶段名称属性的路径。 | `null` |
| `NeckWidth` | 漏斗「颈部」的宽度，以比例表示（0-1）。 | `0.3` |
| `SegmentGap` | 漏斗各段之间的间隙。 | `2.0` |
| `ShowLabels` | 是否在各段上显示标签。 | `true` |
| `ShowValues` | 是否在图表上显示数值。 | `true` |
| `LabelFontSize` | 各段标签所用的字号。 | `12.0` |
| `LabelForeground` | 各段标签所用的画刷。为 `null` 时，标签使用白色。 | `null` |
| `IsHighlightEnabled` | 为漏斗各段启用悬停高亮。 | `false` |
| `IsSelectionEnabled` | 漏斗各段是否可选。 | `false` |
| `SelectionMode` | 漏斗各段的选择行为。 | `SingleDeselect` |
| `SelectionBrush` | 选中段所用的画刷。 | `#314A6E` |
| `SelectionStroke` | 选中段所用的轮廓画刷。 | `null` |
| `SelectionStrokeThickness` | 选中段所用的轮廓粗细。 | `2.0` |
| `SelectedIndex` | 选中段的索引；未选中任何段时为 `-1`。 | `-1` |
