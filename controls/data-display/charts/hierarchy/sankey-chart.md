---
id: sankey-chart
title: 桑基图
description: 呈现数据、能量或物料在各阶段之间的流动，连接带的宽度与流量成正比。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFlowSankey from '/img/controls/charts/charts-flow-sankey.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

桑基图呈现数据、能量或物料在各阶段之间的流动。连接带的宽度与流量的大小成正比。

<Image light={chartsFlowSankey} maxWidth={400} position="center" cornerRadius="true" alt="Sankey chart showing energy flow between stages with link widths proportional to the quantity transferred." />

## 适用场景 {#when-to-use}
- **能耗审计**：呈现能量如何从来源分配到各处消耗。
- **网站分析**：呈现用户在网站中走过的路径（用户旅程）。
- **预算编制**：追踪资金如何从各收入来源流向各项开支。

## 代码示例 {#code-example}

### XAML
```xml
<SankeyChart xmlns="https://github.com/avaloniaui" Name="SankeySample" Title="Energy Flow" Height="350"
                      ItemsSource="{Binding SankeyData}"
                      SourcePath="Source"
                      TargetPath="Target"
                      ValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record FlowItem(string Source, string Target, double Value);

public ObservableCollection<FlowItem> SankeyData { get; } = new()
{
    new("Solar", "Grid", 40),
    new("Wind", "Grid", 30),
    new("Coal", "Grid", 10),
    new("Grid", "Industry", 30),
    new("Grid", "Residential", 25),
    new("Grid", "Transport", 15),
    new("Grid", "Losses", 10)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 流量数据的集合。 | `null` |
| `SourcePath` | 起点节点所对应的属性名。 | `null` |
| `TargetPath` | 终点节点所对应的属性名。 | `null` |
| `ValuePath` | 流量大小所对应的属性名。 | `null` |
| `NodeWidth` | 每一列节点的宽度。 | `20` |
| `NodePadding` | 同一列中各节点之间的垂直间距。 | `10` |
