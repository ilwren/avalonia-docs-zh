---
id: arc-diagram-chart
title: 弧线图
description: 一种网络图：节点沿直线排布，连接以弧线绘制，适合呈现有序数据集中的关系。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFlowArc from '/img/controls/charts/charts-flow-arc.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

弧线图是一种网络图，节点沿一条轴线排布，连接则画成弧线，弧的粗细或颜色表示关联的强弱。

<Image light={chartsFlowArc} maxWidth={400} position="center" cornerRadius="true" alt="Arc diagram with nodes arranged on a horizontal axis connected by curved arcs representing relationships between items." />

## 适用场景 {#when-to-use}
- **序列分析**：呈现固定顺序的条目之间的关系（比如书中的各个章节）。
- **依赖关系梳理**：在一条线上呈现调用栈或结构关系。
- **类别邻近度**：在线性数据集中凸显互动密集的簇。

## 代码示例 {#code-example}

### XAML
```xml
<ArcDiagramChart xmlns="https://github.com/avaloniaui" Name="ArcDiagramSample" Title="Connections" Height="300"
                          Nodes="{Binding ArcNodes}"
                          Links="{Binding ArcLinks}"
                          NodeIdPath="Id"
                          NodeLabelPath="Label"
                          SourcePath="Source"
                          TargetPath="Target"
                          LinkValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record ArcNode(string Id, string Label);
public record ArcLink(string Source, string Target, double Value);

public ObservableCollection<ArcNode> ArcNodes { get; } = new()
{
    new("1", "Chapter 1"),
    new("2", "Chapter 2"),
    new("3", "Chapter 3"),
    new("4", "Chapter 4"),
    new("5", "Chapter 5")
};

public ObservableCollection<ArcLink> ArcLinks { get; } = new()
{
    new("1", "2", 1),
    new("1", "3", 3),
    new("2", "4", 2),
    new("3", "5", 4),
    new("2", "5", 1)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Nodes` | 轴线上各项的集合。 | `null` |
| `Links` | 节点之间的关系。 | `null` |
| `NodeIdPath` | 指向各节点唯一标识的路径。 | `null` |
| `NodeLabelPath` | 指向各节点文本的路径。 | `null` |
| `SourcePath` | 指向各连接起点节点标识的路径。 | `null` |
| `TargetPath` | 指向各连接终点节点标识的路径。 | `null` |
| `LinkValuePath` | 决定弧线粗细/大小的路径。 | `null` |
| `NodeSize` | 节点标记的大小。 | `16.0` |
| `ArcThickness` | 连接弧线的基准粗细。 | `2.0` |
| `ArcOpacity` | 连接弧线的不透明度。 | `0.5` |
