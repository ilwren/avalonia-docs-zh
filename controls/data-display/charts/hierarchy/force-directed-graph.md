---
id: force-directed-graph
title: 力导向图
description: 借助物理模拟排布网络节点，揭示复杂互联数据中的簇群和结构关系。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFlowForceDirected from '/img/controls/charts/charts-flow-force-directed.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

力导向图借助物理模拟来排布网络节点，有助于揭示复杂互联数据中的簇群和结构关系。

<Image light={chartsFlowForceDirected} maxWidth={400} position="center" cornerRadius="true" alt="Force-directed graph with nodes and connecting edges arranged by physics simulation to reveal clusters." />

## 适用场景 {#when-to-use}
- **社交网络**：呈现好友关系、关注关系或社群结构。
- **知识图谱**：展示概念、实体或研究论文之间的关联。
- **系统架构**：梳理各微服务及其通信链路。

## 代码示例 {#code-example}

### XAML
```xml
<ForceDirectedGraph xmlns="https://github.com/avaloniaui" Name="ForceGraphSample" Title="Network Graph" Height="400"
                             NodesSource="{Binding ForceNodes}"
                             EdgesSource="{Binding ForceEdges}"
                             NodeIdPath="Id"
                             NodeLabelPath="Label"
                             EdgeSourcePath="Source"
                             EdgeTargetPath="Target" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record GraphNode(string Id, string Label);
public record GraphEdge(string Source, string Target);

public ObservableCollection<GraphNode> ForceNodes { get; } = new()
{
    new("N1", "Main"),
    new("N2", "Server 1"),
    new("N3", "Server 2"),
    new("N4", "Client A"),
    new("N5", "Client B"),
    new("N6", "DB")
};

public ObservableCollection<GraphEdge> ForceEdges { get; } = new()
{
    new("N1", "N2"),
    new("N1", "N3"),
    new("N2", "N6"),
    new("N3", "N6"),
    new("N2", "N4"),
    new("N3", "N5")
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `NodesSource` | 节点的集合。 | `null` |
| `EdgesSource` | 连接的集合。 | `null` |
| `NodeIdPath` | 各节点标识所对应的属性路径。 | `null` |
| `NodeLabelPath` | 各节点标签所对应的属性路径。 | `null` |
| `EdgeSourcePath` | 各条边起点标识所对应的属性路径。 | `null` |
| `EdgeTargetPath` | 各条边终点标识所对应的属性路径。 | `null` |
| `NodeRadius` | 节点圆的半径。 | `20.0` |
| `RepulsionForce` | 节点之间斥力的强度。 | `5000.0` |
| `AttractionForce` | 沿边的引力强度。 | `0.01` |
| `IsAnimationEnabled` | 是否运行模拟以及布局过渡动画。 | `true` |
