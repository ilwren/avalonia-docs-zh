---
id: sunburst-chart
title: 旭日图
description: 以同心环呈现层级数据：每一环代表一个层级，各扇段表示该节点在其父节点中所占的比例。
doc-type: reference
tags:
  - avalonia pro
---

import chartsHierarchicalSunburst from '/img/controls/charts/charts-hierarchical-sunburst.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

旭日图用一圈圈同心环来呈现层级数据。每一环代表层级中的一层，最内圈即根层级。

<Image light={chartsHierarchicalSunburst} maxWidth={400} position="center" cornerRadius="true" alt="Sunburst chart with concentric rings where each ring represents a hierarchy level and segments show proportions." />

## 适用场景 {#when-to-use}
- **嵌套数据**：呈现层数众多的复杂层级。
- **节省空间**：需要一种比树状图更紧凑的替代形式时。
- **逐层下钻**：清晰展示每一层级上各部分的构成。

## 代码示例 {#code-example}

### XAML
```xml
<SunburstChart xmlns="https://github.com/avaloniaui" Name="SunburstChartSample"
                        Title="Organization Structure"
                        Height="350"
                        ItemsSource="{Binding SunburstData}"
                        ValuePath="Size"
                        LabelPath="Name"
                        ChildrenPath="Children" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public class SunburstNode
{
    public string Name { get; set; } = string.Empty;
    public double Size { get; set; }
    public ObservableCollection<SunburstNode> Children { get; set; } = new();

    public SunburstNode(string name, double size = 0)
    {
        Name = name;
        Size = size;
    }
}

public ObservableCollection<SunburstNode> SunburstData { get; } = new()
{
    new SunburstNode("Engineering", 40)
    {
        Children = new()
        {
            new SunburstNode("Frontend", 15)
            {
                Children = new()
                {
                    new SunburstNode("React", 8),
                    new SunburstNode("Angular", 7)
                }
            },
            new SunburstNode("Backend", 18),
            new SunburstNode("DevOps", 7)
        }
    },
    new SunburstNode("Sales", 30)
    {
        Children = new()
        {
            new SunburstNode("Pro", 18),
            new SunburstNode("SMB", 12)
        }
    },
    new SunburstNode("Marketing", 20)
    {
        Children = new()
        {
            new SunburstNode("Digital", 12),
            new SunburstNode("Brand", 8)
        }
    },
    new SunburstNode("HR", 10)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 图表标题。 | `null` |
| `ItemsSource` | 根层级数据项的集合。 | `null` |
| `ValuePath` | 指向表示扇段大小那个属性的路径。 | `null` |
| `LabelPath` | 指向扇段标签属性的路径。 | `null` |
| `ChildrenPath` | 指向子项集合的路径。 | `null` |
| `InnerRadiusFactor` | 中心孔洞的相对大小，取值从 `0.0` 到 `1.0`。 | `0.2` |
| `RingThickness` | 每一环的粗细。 | `40.0` |
| `GapAngle` | 各扇段之间的间隔角度。 | `2.0` |
| `IsHighlightEnabled` | 为各扇段启用悬停高亮。 | `false` |
| `IsSelectionEnabled` | 是否启用数据点选择。 | `false` |
| `SelectionMode` | 选择模式，比如 `None`、`Single`、`SingleDeselect` 或 `Multiple`。 | `SingleDeselect` |
| `SelectionBrush` | 高亮选中扇段所用的画刷。 | `FromRgb(49, 74, 110)` |
| `SelectionStroke` | 勾勒选中扇段轮廓所用的画刷。 | 采用主题默认值。 |
| `SelectionStrokeThickness` | 选中扇段轮廓的粗细。 | `2.0` |
| `SelectedIndex` | 选中数据点的索引。 | `-1` |
