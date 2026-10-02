---
id: icicle-chart
title: 冰柱图
description: 按层级把数据画成一排排相邻的矩形，呈现父子关系，适合分类体系和结构分析。
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalIcicle from '/img/controls/charts/charts-hierarchical-icicle.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

冰柱图用并排的矩形呈现层级数据。层级的每一层深度对应一行或一列，层与层之间的父子关系一目了然。

<Image light={chartsHierarchicalIcicle} maxWidth={400} position="center" cornerRadius="true" alt="Icicle chart showing hierarchical levels as adjacent rectangular rows where width represents relative value." />

## 适用场景 {#when-to-use}
- **结构分析**：审视代码库、目录结构或庞大的分类体系。
- **性能剖析**：呈现调用栈或执行路径。
- **溯源分析**：在一棵大树中追查叶节点数值的根源。

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
| `ItemsSource` | 层级数据源。 | `null` |
| `ValuePath` | 决定矩形宽度的属性名。 | `null` |
| `LabelPath` | 文本标签所对应的属性名。 | `null` |
| `ChildrenPath` | 指向子节点集合的路径。 | `null` |
| `Orientation` | 图表的方向，`Horizontal` 或 `Vertical`。 | `Vertical` |
| `TileGap` | 相邻矩形之间的间隙。 | `1.0` |
