---
id: flow-chart
title: 流程图
description: 用节点和有向边呈现工作流与决策树，可选分组和自动布局。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

`FlowChart` 绘制节点、边以及可选的分组，用于工作流、流程地图和决策树。当节点没有指定明确位置时，控件可以自动为它们排布。

## 适用场景 {#when-to-use}

- **流程图示**：绘制一步步的业务或运维流程。
- **决策树**：展示各分支、结果以及带标签的流转条件。
- **系统图**：把相关节点圈进带边界的区域。

## 代码示例 {#code-example}

### XAML

```xml
<FlowChart xmlns="https://github.com/avaloniaui" Title="Troubleshooting"
                            Height="360"
                            Nodes="{Binding FlowNodes}"
                            Edges="{Binding FlowEdges}" />
```

### 数据模型（C#） {#data-model-c}

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

## 常用属性（`FlowChart`） {#common-properties-flowchart}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Nodes` | 图表所渲染的 `FlowNode` 项集合。 | `null` |
| `Edges` | `FlowEdge` 连接的集合。 | `null` |
| `Groups` | 可选的 `FlowGroup` 容器集合。 | `null` |
| `NodeCornerRadius` | 圆角节点形状所用的圆角半径。 | `10.0` |

## 常用属性（`FlowNode`） {#common-properties-flownode}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Id` | 节点的唯一标识，供边和分组引用。 | `null` |
| `Text` | 显示在节点内部的文本。 | `null` |
| `Shape` | 节点形状，比如 `Rectangle` 或 `Diamond`。 | `Rectangle` |
| `X` | 明确指定的 X 坐标。 | `0` |
| `Y` | 明确指定的 Y 坐标。 | `0` |
| `Width` | 节点宽度。 | `120` |
| `Height` | 节点高度。 | `60` |
| `Background` | 节点可选的背景画刷。 | `null` |
| `Foreground` | 节点可选的文字画刷。 | `null` |
| `Icon` | 显示在节点内部的可选图标。 | `null` |

## 常用属性（`FlowEdge`） {#common-properties-flowedge}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `SourceId` | 起点节点的标识。 | `null` |
| `TargetId` | 终点节点的标识。 | `null` |
| `Label` | 可选的边标签。 | `null` |
| `ShowArrow` | 是否绘制箭头。 | `true` |

## 常用属性（`FlowGroup`） {#common-properties-flowgroup}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Id` | 分组的唯一标识。 | `null` |
| `Label` | 为该分组显示的可选标签。 | `null` |
| `Bounds` | 分组容器的明确边界。 | `0,0,0,0` |
| `Background` | 分组可选的背景画刷。 | `null` |
| `BorderBrush` | 分组可选的边框画刷。 | `null` |
| `BorderThickness` | 分组边框的粗细。 | `1.0` |
| `NodeIds` | 归属于该分组的节点 ID 集合。 | `null` |

## 另请参阅 {#see-also}

- [工序流程图](/controls/data-display/charts/hierarchy/process-flow-chart)
- [思维导图](/controls/data-display/charts/hierarchy/mindmap-chart)
