---
id: alluvial-chart
title: Alluvial chart
description: Represents structural changes across sequential stages using flowing bands between vertical node columns, similar to a Sankey diagram.
doc-type: reference
tags:
  - avalonia pro
---

import chartsFlowAlluvial from '/img/controls/charts/charts-flow-alluvial.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Alluvial charts represent changes in structure over time or across categories. They are similar to Sankey diagrams but are typically organized into distinct vertical columns.

<Image light={chartsFlowAlluvial} maxWidth={400} position="center" cornerRadius="true" alt="Alluvial chart with vertical node columns connected by flowing bands representing categorical transitions between stages." />

## 适用场景 {#when-to-use}
- **Workflow analysis**: Tracking how items move through sequential process stages.
- **Categorical flow**: Visualizing how members of one category belong to others (e.g., voters' changing affiliations).
- **Structural shifts**: Showing how a population's grouping changes between two points in time.

## 代码示例 {#code-example}

### XAML
```xml
<AlluvialChart xmlns="https://github.com/avaloniaui" Name="AlluvialChartSample" Title="Category Flow" Height="350"
                        Nodes="{Binding AlluvialNodes}"
                        Links="{Binding AlluvialLinks}" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<AlluvialNode> AlluvialNodes { get; } = new()
{
    new() { Id = "Jan", Label = "Jan", Step = 0, Value = 50 },
    new() { Id = "Feb", Label = "Feb", Step = 0, Value = 60 },
    new() { Id = "CatA", Label = "Category A", Step = 1, Value = 55 },
    new() { Id = "CatB", Label = "Category B", Step = 1, Value = 55 }
};

public ObservableCollection<AlluvialLink> AlluvialLinks { get; } = new()
{
    new() { Source = "Jan", Target = "CatA", Value = 30 },
    new() { Source = "Jan", Target = "CatB", Value = 20 },
    new() { Source = "Feb", Target = "CatA", Value = 25 },
    new() { Source = "Feb", Target = "CatB", Value = 35 }
};
```

`AlluvialChart` uses the strongly typed `AlluvialNode` and `AlluvialLink` classes. Each node defines an `Id`, `Label`, `Step`, and `Value`.

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Nodes` | The collection of categorical nodes (columns). | `null` |
| `Links` | The collection of connections between nodes. | `null` |
