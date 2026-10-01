---
id: flow-chart
title: Flow chart
description: Visualizes workflows and decision trees as nodes and directed edges, with optional grouping and auto-layout.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[Charts](/controls/data-display/charts) are available with [Avalonia Pro](https://avaloniaui.net/pricing).
:::

`FlowChart` renders nodes, edges, and optional groups for workflows, process maps, and decision trees. When nodes have no explicit positions, the control can lay them out automatically.

## 适用场景 {#when-to-use}

- **Process diagrams**: Render step-by-step business or operational flows.
- **Decision trees**: Show branches, outcomes, and labeled transitions.
- **System maps**: Group related nodes into bounded areas.

## Code example

### XAML

```xml
<FlowChart xmlns="https://github.com/avaloniaui" Title="Troubleshooting"
                            Height="360"
                            Nodes="{Binding FlowNodes}"
                            Edges="{Binding FlowEdges}" />
```

### Data model (C#)

```csharp
public ObservableCollection<FlowNode> FlowNodes { get; } = new()
{
    new() { Id = "start", Text = "Lamp off", Shape = FlowShape.RoundedRect },
    new() { Id = "power", Text = "Check power", Shape = FlowShape.Rectangle },
    new() { Id = "done", Text = "Replace bulb", Shape = FlowShape.Diamond }
};

public ObservableCollection<FlowEdge> FlowEdges { get; } = new()
{
    new() { SourceId = "start", TargetId = "power" },
    new() { SourceId = "power", TargetId = "done", Label = "No" }
};
```

## Common properties (`FlowChart`)

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Nodes` | Collection of `FlowNode` items rendered by the chart. | `null` |
| `Edges` | Collection of `FlowEdge` connections. | `null` |
| `Groups` | Optional collection of `FlowGroup` containers. | `null` |
| `NodeCornerRadius` | Corner radius applied to rounded node shapes. | `10.0` |

## Common properties (`FlowNode`)

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Id` | Unique node identifier used by edges and groups. | `null` |
| `Text` | Text displayed inside the node. | `null` |
| `Shape` | Node shape, such as `Rectangle` or `Diamond`. | `Rectangle` |
| `X` | Explicit X position. | `0` |
| `Y` | Explicit Y position. | `0` |
| `Width` | Node width. | `120` |
| `Height` | Node height. | `60` |
| `Background` | Optional background brush for the node. | `null` |
| `Foreground` | Optional text brush for the node. | `null` |
| `Icon` | Optional icon shown inside the node. | `null` |

## Common properties (`FlowEdge`)

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `SourceId` | Source node identifier. | `null` |
| `TargetId` | Target node identifier. | `null` |
| `Label` | Optional edge label. | `null` |
| `ShowArrow` | Whether to draw the arrow head. | `true` |

## Common properties (`FlowGroup`)

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Id` | Unique group identifier. | `null` |
| `Label` | Optional label displayed for the group. | `null` |
| `Bounds` | Explicit bounds of the group container. | `0,0,0,0` |
| `Background` | Optional background brush for the group. | `null` |
| `BorderBrush` | Optional border brush for the group. | `null` |
| `BorderThickness` | Thickness of the group border. | `1.0` |
| `NodeIds` | Collection of node IDs that belong to the group. | `null` |

## 另请参阅 {#see-also}

- [Process flow chart](/controls/data-display/charts/hierarchy/process-flow-chart)
- [Mind map chart](/controls/data-display/charts/hierarchy/mindmap-chart)
