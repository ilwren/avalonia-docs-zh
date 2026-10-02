---
id: mindmap-chart
title: 思维导图 / 头脑风暴
description: 围绕一个中心主题排布 FlowChart 的节点和连接，构建出一张思维导图。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFlowMindmap from '/img/controls/charts/charts-flow-mindmap.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

思维导图是一种发散式的图示，从中心主题向外辐射出相关想法和子任务，常用于头脑风暴和项目规划。在 `Avalonia.Controls.Charts` 中，这种版面构建在 `FlowChart` 之上。

<Image light={chartsFlowMindmap} maxWidth={400} position="center" cornerRadius="true" alt="Mindmap diagram radiating outward from a central topic node to connected sub-topics and ideas." />

## 适用场景 {#when-to-use}
- **想法生发**：会议过程中随手记录并梳理思路。
- **项目范围**：理清各个模块及其需求。
- **知识表达**：呈现复杂概念及其相互关联。

## 代码示例 {#code-example}

### XAML
```xml
<FlowChart xmlns="https://github.com/avaloniaui" Name="MindmapSample"
                  Title="Project Alpha Brainstorm"
                  Height="600"
                  Nodes="{Binding MindmapNodes}"
                  Edges="{Binding MindmapEdges}"
                  CornerRadius="20" />
```

### 数据模型（C#） {#data-model-c}
```csharp
using Avalonia.Media;

public ObservableCollection<FlowNode> MindmapNodes { get; } = new()
{
    new()
    {
        Id = "root",
        Text = "Project Alpha",
        X = 350,
        Y = 250,
        Shape = FlowShape.Circle,
        Background = Brushes.MediumPurple,
        Foreground = Brushes.White,
        Width = 120,
        Height = 120
    },
    new()
    {
        Id = "res",
        Text = "Research",
        X = 200,
        Y = 150,
        Shape = FlowShape.RoundedRect,
        Background = Brushes.Salmon,
        Width = 100
    },
    new()
    {
        Id = "re1",
        Text = "User Specs",
        X = 50,
        Y = 100,
        Shape = FlowShape.Rectangle,
        Background = Brushes.Snow,
        Width = 100
    },
    new()
    {
        Id = "re2",
        Text = "Competitors",
        X = 50,
        Y = 200,
        Shape = FlowShape.Rectangle,
        Background = Brushes.Snow,
        Width = 100
    },
    new()
    {
        Id = "des",
        Text = "Design",
        X = 500,
        Y = 150,
        Shape = FlowShape.RoundedRect,
        Background = Brushes.SkyBlue,
        Width = 100
    },
    new()
    {
        Id = "de1",
        Text = "UI/UX",
        X = 650,
        Y = 100,
        Shape = FlowShape.Rectangle,
        Background = Brushes.Snow,
        Width = 100
    },
    new()
    {
        Id = "de2",
        Text = "Architecture",
        X = 650,
        Y = 200,
        Shape = FlowShape.Rectangle,
        Background = Brushes.Snow,
        Width = 100
    },
    new()
    {
        Id = "imp",
        Text = "Implementation",
        X = 350,
        Y = 400,
        Shape = FlowShape.RoundedRect,
        Background = Brushes.LightGreen,
        Width = 120
    },
    new()
    {
        Id = "im1",
        Text = "Frontend",
        X = 250,
        Y = 500,
        Shape = FlowShape.Rectangle,
        Background = Brushes.Snow,
        Width = 100
    },
    new()
    {
        Id = "im2",
        Text = "Backend",
        X = 450,
        Y = 500,
        Shape = FlowShape.Rectangle,
        Background = Brushes.Snow,
        Width = 100
    }
};

public ObservableCollection<FlowEdge> MindmapEdges { get; } = new()
{
    new() { SourceId = "root", TargetId = "res", ShowArrow = false },
    new() { SourceId = "res", TargetId = "re1", ShowArrow = false },
    new() { SourceId = "res", TargetId = "re2", ShowArrow = false },
    new() { SourceId = "root", TargetId = "des", ShowArrow = false },
    new() { SourceId = "des", TargetId = "de1", ShowArrow = false },
    new() { SourceId = "des", TargetId = "de2", ShowArrow = false },
    new() { SourceId = "root", TargetId = "imp", ShowArrow = false },
    new() { SourceId = "imp", TargetId = "im1", ShowArrow = false },
    new() { SourceId = "imp", TargetId = "im2", ShowArrow = false }
};
```

## 常用属性（`FlowChart`） {#common-properties-flowchart}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Nodes` | 表示各主题的 `FlowNode` 项集合。 | `null` |
| `Edges` | 表示各条关系的 `FlowEdge` 项集合。 | `null` |
| `NodeCornerRadius` | 所绘节点方框的圆角程度。 | `10.0` |
| `Groups` | 可选的 `FlowGroup` 容器集合。 | `null` |
| `FlowNode.Shape` | 节点形状，比如 `Rectangle`、`Circle` 或 `Diamond`。 | `Rectangle` |
