---
id: radial-tree-chart
title: 径向树图
description: 一种层级版面：根节点居中，子节点沿同心环向外辐射，大型树结构用它格外省地方。
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalRadialtree from '/img/controls/charts/charts-hierarchical-radial-tree.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

径向树图呈现层级数据，根节点位于中心，子节点沿同心圆向外辐射。对于大型树结构，这种版面空间利用率极高。

<Image light={chartsHierarchicalRadialtree} maxWidth={400} position="center" cornerRadius="true" alt="Radial tree chart with a root node at the center and child nodes radiating outward in concentric rings." />

## 适用场景 {#when-to-use}
- **目录可视化**：以紧凑的环形把多层文件夹呈现出来。
- **基因图谱**：呈现众多生物实体之间的关系。
- **网络拓扑**：以中心枢纽为起点，梳理网络中的各台设备。

## 代码示例 {#code-example}

### XAML
```xml
<RadialTreeChart xmlns="https://github.com/avaloniaui" Name="RadialTreeChartSample" Title="Taxonomy" Height="400"
                          ItemsSource="{Binding RadialTreeData}"
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

public ObservableCollection<TreeNode> RadialTreeData { get; } = new()
{
    new TreeNode { Name = "Animals", Children = {
        new TreeNode { Name = "Mammals", Children = {
            new TreeNode { Name = "Dog" },
            new TreeNode { Name = "Cat" }
        }},
        new TreeNode { Name = "Birds", Children = {
            new TreeNode { Name = "Eagle" }
        }},
        new TreeNode { Name = "Fish", Children = {
            new TreeNode { Name = "Salmon" }
        }}
    }}
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 居于中心的根节点。 | `null` |
| `ValuePath` | 指向各节点关联数值的路径。 | `null` |
| `LabelPath` | 指向节点文本标签的路径。 | `null` |
| `ChildrenPath` | 指向外层节点集合的路径。 | `null` |
| `NodeSize` | 绘制节点圆点所用的半径。 | `8.0` |
| `LevelSpacing` | 径向各层级之间的理想间距。 | `60.0` |
