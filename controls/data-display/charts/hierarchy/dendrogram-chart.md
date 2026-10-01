---
id: dendrogram-chart
title: 聚类树图
description: 一种树状图，通过展示条目如何逐级合并成分支来呈现层次聚类，常用于统计和生物学分析。
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalDendrogram from '/img/controls/charts/charts-hierarchical-dendrogram.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

聚类树图（Dendrogram）是一种树状图，常用来呈现层次聚类所产生的簇是如何排布的，直观展示条目如何一步步合并成同一条分支。

<Image light={chartsHierarchicalDendrogram} maxWidth={400} position="center" cornerRadius="true" alt="Dendrogram tree diagram showing hierarchical clustering with branches merging from leaf nodes toward the root." />

## 适用场景 {#when-to-use}
- **聚类分析**：呈现统计聚类算法的结果。
- **系统发生树**：展示不同物种之间的演化关系。
- **结构合并**：刻画那些由众多部分出发、最终汇聚成少数几组的数据。

## 代码示例 {#code-example}

### XAML
```xml
<DendrogramChart xmlns="https://github.com/avaloniaui" Name="DendrogramChartSample" Title="Clustering" Height="300"
                          ItemsSource="{Binding DendrogramData}"
                          LabelPath="Name"
                          ChildrenPath="Children" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public class TreeNode
{
    public string Name { get; set; } = string.Empty;
    public ObservableCollection<TreeNode> Children { get; set; } = new();
}

public ObservableCollection<TreeNode> DendrogramData { get; } = new()
{
    new TreeNode { Name = "Root", Children = {
        new TreeNode { Name = "A", Children = {
            new TreeNode { Name = "A1" },
            new TreeNode { Name = "A2" }
        }},
        new TreeNode { Name = "B", Children = {
            new TreeNode { Name = "B1" }
        }}
    }}
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 层次聚类数据。 | `null` |
| `LabelPath` | 表示叶节点或节点名称的属性。 | `null` |
| `ChildrenPath` | 指向嵌套簇项的路径。 | `null` |
| `DistancePath` | 表示簇间距离或合并高度的属性。 | `null` |
| `Orientation` | 图表的方向，`Horizontal` 或 `Vertical`。 | `Horizontal` |
| `LinkStyle` | 连接各项的线条样式，`Elbow` 或 `Straight`。 | `Elbow` |
| `LeafSpacing` | 叶节点之间的间距。 | `25.0` |
