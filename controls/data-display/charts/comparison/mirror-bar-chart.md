---
id: mirror-bar-chart
title: 镜像条形图
description: 把两组条形系列以中线为轴背靠背排布，适合人口结构和并排对比。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

镜像条形图把两组条形系列画在中线两侧，于是每个类别都能对称地两相比较。

## 适用场景 {#when-to-use}

- **背靠背对比**：按类别比较两类人群、两个地区或两组产品。
- **人口结构版面**：呈现相对的两组分布，比如各年龄段的男女人数。
- **双向排名**：不必堆叠或分组，就能对照成对的指标。

## 代码示例 {#code-example}

### XAML

```xml
<MirrorBarChart xmlns="https://github.com/avaloniaui" Title="Regional comparison"
                         Height="320"
                         ItemsSource="{Binding MirrorData}"
                         LabelPath="Category"
                         LeftValuePath="West"
                         RightValuePath="East"
                         LeftTitle="West"
                         RightTitle="East" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record MirrorBarItem(string Category, double West, double East);

public ObservableCollection<MirrorBarItem> MirrorData { get; } = new()
{
    new("Q1", 22, 18),
    new("Q2", 28, 24),
    new("Q3", 19, 27)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 镜像对比项的集合。 | `null` |
| `LeftValuePath` | 指向绘制在左侧那个数值的路径。 | `null` |
| `RightValuePath` | 指向绘制在右侧那个数值的路径。 | `null` |
| `LabelPath` | 指向类别标签的路径。 | `null` |
| `LeftBrush` | 左侧条形所用的画刷。 | `#E91E63` |
| `RightBrush` | 右侧条形所用的画刷。 | `#2196F3` |
| `BarHeight` | 条形高度，以行高的比例表示。 | `0.7` |
| `CenterGap` | 镜像两侧之间的间隙。 | `40.0` |
| `LeftTitle` | 左侧的可选标题。 | `null` |
| `RightTitle` | 右侧的可选标题。 | `null` |
| `IsHighlightEnabled` | 为镜像条形启用悬停高亮。 | `false` |

## 另请参阅 {#see-also}

- [人口金字塔图](/controls/data-display/charts/comparison/population-pyramid-chart)
- [龙卷风图](/controls/data-display/charts/comparison/tornado-chart)
