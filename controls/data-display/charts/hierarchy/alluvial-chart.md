---
id: alluvial-chart
title: 冲积图
description: 用在各列节点之间流淌的色带呈现结构随阶段的变迁，与桑基图相仿。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFlowAlluvial from '/img/controls/charts/charts-flow-alluvial.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

冲积图呈现结构随时间或跨类别的变化。它与桑基图相仿，但通常被组织成一列列清晰的纵向节点。

<Image light={chartsFlowAlluvial} maxWidth={400} position="center" cornerRadius="true" alt="Alluvial chart with vertical node columns connected by flowing bands representing categorical transitions between stages." />

## 适用场景 {#when-to-use}
- **流程分析**：追踪事项在各道工序之间的流转。
- **类别流动**：呈现某一类别的成员如何归属到其他类别（比如选民立场的变迁）。
- **结构变迁**：展示某个群体的分组在两个时间点之间如何改变。

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

`AlluvialChart` 使用强类型的 `AlluvialNode` 和 `AlluvialLink` 类。每个节点都要定义 `Id`、`Label`、`Step` 和 `Value`。

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Nodes` | 类别节点（列）的集合。 | `null` |
| `Links` | 节点之间连接的集合。 | `null` |
