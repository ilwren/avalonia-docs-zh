---
id: network-chart
title: 网络图
description: 以静态版面呈现节点和边，适合基础设施图、依赖树和结构固定的图示。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFlowNetwork from '/img/controls/charts/charts-flow-network.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

网络图提供节点与边的概览视图。它比力导向图更简单、更静态，适合结构固定的图示。

<Image light={chartsFlowNetwork} maxWidth={400} position="center" cornerRadius="true" alt="Network chart with labeled nodes connected by edges showing static relationships in a structural diagram." />

## 适用场景 {#when-to-use}
- **基础设施图**：呈现各台服务器及其连接。
- **路由表**：梳理网络节点之间的路径。
- **依赖树**：呈现系统中各模块之间的关系。

## 代码示例 {#code-example}

### XAML
```xml
<NetworkChart xmlns="https://github.com/avaloniaui" Name="NetworkChartSample" Title="Social Network" Height="350"
                       Nodes="{Binding NetworkNodes}"
                       Edges="{Binding NetworkEdges}" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<NetworkNode> NetworkNodes { get; } = new()
{
    new() { Id = "A", Label = "Alice", X = 0, Y = 0 },
    new() { Id = "B", Label = "Bob", X = 0, Y = 0 },
    new() { Id = "C", Label = "Charlie", X = 0, Y = 0 },
    new() { Id = "D", Label = "David", X = 0, Y = 0 },
    new() { Id = "E", Label = "Eve", X = 0, Y = 0 }
};

public ObservableCollection<NetworkEdge> NetworkEdges { get; } = new()
{
    new() { Source = "A", Target = "B", Weight = 2 },
    new() { Source = "A", Target = "C", Weight = 1 },
    new() { Source = "B", Target = "D", Weight = 3 },
    new() { Source = "C", Target = "E", Weight = 1 },
    new() { Source = "D", Target = "E", Weight = 2 },
    new() { Source = "B", Target = "E", Weight = 1 }
};
```

`NetworkChart` 直接使用 `NetworkNode` 和 `NetworkEdge` 对象，因此标签和权重定义在这些类型上，不必再额外设置属性路径。

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Nodes` | 图节点的集合。 | `null` |
| `Edges` | 图的边的集合。 | `null` |
