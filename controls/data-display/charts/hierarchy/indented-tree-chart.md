---
id: indented-tree-chart
title: 缩进树图
description: 在图表容器内以文件管理器式的缩进版面呈现层级，支持更丰富的样式和交互。
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalIndentedtree from '/img/controls/charts/charts-hierarchical-tree.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

缩进树图的版面与常见的文件管理器或树视图类似，只是它位于图表容器之中，因而能获得更丰富的样式和交互能力。

<Image light={chartsHierarchicalIndentedtree} maxWidth={400} position="center" cornerRadius="true" alt="Indented tree chart showing a file-explorer-style hierarchy with parent and child nodes offset by indentation." />

## 适用场景 {#when-to-use}
- **文件系统浏览器**：为本地或云端存储打造自定义导航界面。
- **物料清单（BOM）**：呈现制造业中多层级的产品结构。
- **设置/配置**：把层层嵌套的复杂配置项分门别类地呈现出来。

## 代码示例 {#code-example}

### XAML
```xml
<IndentedTreeChart xmlns="https://github.com/avaloniaui" Name="IndentedTreeChartSample" Height="320"
                            ItemsSource="{Binding IndentedTreeData}"
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

public ObservableCollection<TreeNode> IndentedTreeData { get; } = new()
{
    new TreeNode { Name = "src", Children = {
        new TreeNode { Name = "components", Children = {
            new TreeNode { Name = "Button.cs" },
            new TreeNode { Name = "Chart.cs" }
        }},
        new TreeNode { Name = "models", Children = {
            new TreeNode { Name = "User.cs" }
        }},
        new TreeNode { Name = "Program.cs" }
    }},
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 根层级的节点。 | `null` |
| `ValuePath` | 显示在各标签旁边的可选数值。 | `null` |
| `LabelPath` | 条目文本所对应的属性名。 | `null` |
| `ChildrenPath` | 子集合所对应的属性名。 | `null` |
| `IndentSize` | 每一层级的横向缩进量。 | `20.0` |
| `RowHeight` | 每一行的渲染高度。 | `24.0` |
| `ShowLines` | 是否在节点之间显示连接线。 | `true` |
| `ShowIcons` | 是否显示文件夹和叶节点图标。 | `true` |
