---
id: circle-packing-chart
title: 圆堆积图
description: 用层层嵌套的圆表示层级数据：大圆里套着小圆，每一层的分组与相对大小一目了然。
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalCirclepacking from '/img/controls/charts/charts-hierarchical-circle-packing.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

圆堆积图是矩形树图的一种变体，节点用圆来表示。大圆代表父类别，子类别则以小圆嵌套其中。

<Image light={chartsHierarchicalCirclepacking} maxWidth={400} position="center" cornerRadius="true" alt="Circle packing chart with nested circles where parent categories contain proportionally-sized child circles." />

## 适用场景 {#when-to-use}
- **聚类呈现**：以自然悦目的方式展示分组与子分组。
- **好看的概览**：相比规整的网格，更想用「气泡」形式的仪表板。
- **关系亲疏**：展示同一类别内各条目之间的亲疏远近。

## 代码示例 {#code-example}

### XAML
```xml
<CirclePackingChart xmlns="https://github.com/avaloniaui" Name="CirclePackingChartSample" Title="Package Sizes" Height="350"
                             ItemsSource="{Binding CirclePackingData}"
                             ValuePath="Size"
                             LabelPath="Name" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record TreeMapItem(string Name, double Size);

public ObservableCollection<TreeMapItem> CirclePackingData { get; } = new()
{
    new("Core", 40),
    new("Utils", 25),
    new("UI", 35)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 层级数据源。 | `null` |
| `ValuePath` | 圆的大小/直径。 | `null` |
| `LabelPath` | 显示在气泡内部或附近的文本。 | `null` |
| `ChildrenPath` | 指向各节点子集合的路径。 | `null` |
| `CirclePadding` | 堆积圆之间的内边距。 | `3.0` |
| `Palette` | 各类别所用的自定义画刷集合。 | Auto-generated |
