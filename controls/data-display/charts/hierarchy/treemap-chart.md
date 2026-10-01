---
id: treemap-chart
title: 矩形树图
description: 把层级数据画成按数值定尺寸的嵌套矩形，适合比较磁盘占用、预算等类别内部的占比。
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalTreemap from '/img/controls/charts/charts-hierarchical-treemap.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

矩形树图把层级数据或扁平数据呈现为一组嵌套矩形。每条分支占一个矩形，大小由其数值决定，内部再铺满更小的子矩形。

<Image light={chartsHierarchicalTreemap} maxWidth={400} position="center" cornerRadius="true" alt="Treemap chart showing nested rectangles sized proportionally to disk usage values for different folders." />

## 适用场景 {#when-to-use}
- **资源占用**：按文件或进程呈现磁盘空间、内存的消耗。
- **占比分析**：比较各类别内部条目的分量。
- **复杂层级**：需要在一个视图里呈现大量层级条目时。

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
| `ValuePath` | 指向表示面积大小那个属性的路径。 | `null` |
| `LabelPath` | 指向标签属性的路径。 | `null` |
| `TileGap` | 矩形之间的间隙。 | `1.0` |
| `IsHighlightEnabled` | 为树图节点启用悬停高亮。 | `false` |
| `IsSelectionEnabled` | 启用节点选择。 | `false` |
| `SelectionMode` | 选择行为，比如 `None`、`Single`、`SingleDeselect` 或 `Multiple`。 | `SingleDeselect` |
| `SelectionBrush` | 高亮选中扇段所用的画刷。 | `FromRgb(49, 74, 110)` |
| `SelectionStroke` | 勾勒选中扇段轮廓所用的画刷。 | 采用主题默认值。 |
| `SelectionStrokeThickness` | 选中扇段轮廓的粗细。 | `2.0` |
| `SelectedIndex` | 主选中节点的索引。 | `-1` |
