---
id: icicle-chart
title: Icicle chart
description: Visualizes hierarchical data as adjacent rectangles per level, showing parent-child relationships for taxonomy and structural analysis.
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalIcicle from '/img/controls/charts/charts-hierarchical-icicle.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Icicle charts visualize hierarchical data using rectangles placed side by side. Each level in the hierarchy's depth is represented by a row or column, showing parent-child relationships across levels.

<Image light={chartsHierarchicalIcicle} maxWidth={400} position="center" cornerRadius="true" alt="Icicle chart showing hierarchical levels as adjacent rectangular rows where width represents relative value." />

## 适用场景 {#when-to-use}
- **Structural analysis**: Inspecting codebases, directory structures, or large taxonomies.
- **Performance profiling**: Visualizing call stacks or execution paths.
- **Relationship discovery**: Finding the root cause of leaf-node values within a large tree.

## 代码示例 {#code-example}

### XAML
```xml
<IcicleChart xmlns="https://github.com/avaloniaui" Name="IcicleChartSample" Title="File System" Height="300"
                      ItemsSource="{Binding IcicleData}"
                      ValuePath="Size"
                      LabelPath="Name" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record TreeMapItem(string Name, double Size);

public ObservableCollection<TreeMapItem> IcicleData { get; } = new()
{
    new("src", 60),
    new("tests", 25),
    new("docs", 15)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | The hierarchical data source. | `null` |
| `ValuePath` | Property name determining rectangle width. | `null` |
| `LabelPath` | Property name for the text label. | `null` |
| `ChildrenPath` | Path to the collection of child nodes. | `null` |
| `Orientation` | 图表的方向，`Horizontal` 或 `Vertical`。 | `Vertical` |
| `TileGap` | Gap between adjacent rectangles. | `1.0` |
