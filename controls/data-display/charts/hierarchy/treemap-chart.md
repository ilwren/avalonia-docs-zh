---
id: treemap-chart
title: Treemap chart
description: Visualizes hierarchical data as nested rectangles sized by value, useful for comparing proportions within categories such as disk usage or budgets.
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalTreemap from '/img/controls/charts/charts-hierarchical-treemap.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

TreeMap charts visualize hierarchical or flat data as a set of nested rectangles. Each branch is given a rectangle, sized according to its value, and tiled with smaller sub-rectangles.

<Image light={chartsHierarchicalTreemap} maxWidth={400} position="center" cornerRadius="true" alt="Treemap chart showing nested rectangles sized proportionally to disk usage values for different folders." />

## 适用场景 {#when-to-use}
- **Resource usage**: Visualizing disk space or memory consumption by file/process.
- **Proportional analysis**: Comparing the weight of items within categories.
- **Complex hierarchies**: When you need to show many hierarchical items in a single view.

## 代码示例 {#code-example}

### XAML
```xml
<TreeMapChart xmlns="https://github.com/avaloniaui" Name="TreeMapSample" Title="Disk Usage" Height="300"
                       ItemsSource="{Binding TreeMapData}" ValuePath="Size" LabelPath="Name" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record TreeMapItem(string Name, double Size);

public ObservableCollection<TreeMapItem> TreeMapData { get; } = new()
{
    new("Documents", 45),
    new("Photos", 30),
    new("Videos", 50),
    new("Music", 20),
    new("Downloads", 35)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 图表标题。 | `null` |
| `ItemsSource` | 数据项的集合。 | `null` |
| `ValuePath` | Path to the property representing area size. | `null` |
| `LabelPath` | Path to the property for the labels. | `null` |
| `TileGap` | Gap between rectangles. | `1.0` |
| `IsHighlightEnabled` | Enables hover highlighting for treemap nodes. | `false` |
| `IsSelectionEnabled` | Enables node selection. | `false` |
| `SelectionMode` | Selection behavior, such as `None`, `Single`, `SingleDeselect`, or `Multiple`. | `SingleDeselect` |
| `SelectionBrush` | Brush used to highlight selected segments. | `FromRgb(49, 74, 110)` |
| `SelectionStroke` | Brush used to outline selected segments. | Uses theme default. |
| `SelectionStrokeThickness` | Thickness of the outline of selected segments. | `2.0` |
| `SelectedIndex` | Index of the primary selected node. | `-1` |
