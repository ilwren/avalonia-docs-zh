---
id: process-flow-chart
title: 工序流程图
description: 用 FlowChart 的节点和边呈现业务工作流与决策树。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFlowProcess from '/img/controls/charts/charts-flow-process.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

工序流程图用来呈现系统中的步骤序列、判断分支和逻辑结果。在 `Avalonia.Controls.Charts` 中，它由 `FlowChart`、`FlowNode` 和 `FlowEdge` 实现。

<Image light={chartsFlowProcess} maxWidth={400} position="center" cornerRadius="true" alt="Process flow chart with start, decision, and action nodes connected by directional arrows showing a workflow sequence." />

## 适用场景 {#when-to-use}
- **工作流梳理**：呈现业务流程或审批链路。
- **决策树**：展示故障排查或用户旅程的逻辑路径。
- **系统架构**：梳理各模块或各服务之间的连接。

## 代码示例 {#code-example}

### XAML
```xml
<FlowChart xmlns="https://github.com/avaloniaui" Name="FlowChartSample"
                  Title="Troubleshooting Lamp"
                  Height="400"
                  Nodes="{Binding FlowNodes}"
                  Edges="{Binding FlowEdges}" />
```

### 数据模型（C#） {#data-model-c}
```csharp
using Avalonia.Media;

public ObservableCollection<FlowNode> FlowNodes { get; } = new()
{
    new()
    {
        Id = "start",
        Text = "Lamp doesn't work",
        Shape = FlowShape.RoundedRect,
        X = 300,
        Y = 50,
        Background = Brushes.Salmon,
        Foreground = Brushes.White,
        Width = 200
    },
    new()
    {
        Id = "check_plug",
        Text = "Is lamp plugged in?",
        Shape = FlowShape.Diamond,
        X = 280,
        Y = 150,
        Width = 240,
        Height = 100,
        Background = Brushes.LightBlue
    },
    new()
    {
        Id = "plug_in",
        Text = "Plug in lamp",
        Shape = FlowShape.Rectangle,
        X = 550,
        Y = 170,
        Background = Brushes.LightGreen
    },
    new()
    {
        Id = "check_bulb",
        Text = "Is bulb burned out?",
        Shape = FlowShape.Diamond,
        X = 280,
        Y = 300,
        Width = 240,
        Height = 100,
        Background = Brushes.LightBlue
    },
    new()
    {
        Id = "replace_bulb",
        Text = "Replace bulb",
        Shape = FlowShape.Rectangle,
        X = 550,
        Y = 320,
        Background = Brushes.LightGreen
    },
    new()
    {
        Id = "repair",
        Text = "Buy new lamp",
        Shape = FlowShape.Rectangle,
        X = 300,
        Y = 450,
        Background = Brushes.LightGreen
    }
};

public ObservableCollection<FlowEdge> FlowEdges { get; } = new()
{
    new() { SourceId = "start", TargetId = "check_plug" },
    new() { SourceId = "check_plug", TargetId = "plug_in", Label = "No" },
    new() { SourceId = "check_plug", TargetId = "check_bulb", Label = "Yes" },
    new() { SourceId = "check_bulb", TargetId = "replace_bulb", Label = "Yes" },
    new() { SourceId = "check_bulb", TargetId = "repair", Label = "No" }
};
```

## 常用属性（`FlowChart`） {#common-properties-flowchart}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Nodes` | 表示各道工序的 `FlowNode` 项集合。 | `null` |
| `Edges` | 表示各条连接的 `FlowEdge` 项集合。 | `null` |
| `NodeCornerRadius` | 所绘节点方框的圆角程度。 | `10.0` |
| `Groups` | 可选的 `FlowGroup` 容器集合。 | `null` |
| `FlowEdge.ShowArrow` | 连接末端是否带箭头。 | `true` |
