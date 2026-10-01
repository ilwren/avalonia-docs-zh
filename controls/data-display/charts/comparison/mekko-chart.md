---
id: mekko-chart
title: Mekko chart
description: Combines variable-width columns with stacked segments to compare total size and internal composition.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Mekko charts, also called Marimekko charts, use variable column widths and stacked segment heights to compare market size and composition in one view.

## 适用场景 {#when-to-use}

- **Market structure**: Compare category share and internal segment mix at the same time.
- **Portfolio composition**: Show total size and breakdown per group.
- **Multi-dimensional comparison**: Replace separate width and stacked-bar views with one chart.

## 代码示例 {#code-example}

### XAML

```xml
<MekkoChart xmlns="https://github.com/avaloniaui" Title="Market mix"
                             Height="320"
                             ItemsSource="{Binding MekkoData}"
                             CategoryPath="Category"
                             WidthPath="Width"
                             SegmentsPath="Segments" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record MekkoSegment(string Name, double Value);
public record MekkoColumn(string Category, double Width, ObservableCollection<MekkoSegment> Segments);

public ObservableCollection<MekkoColumn> MekkoData { get; } = new()
{
    new("North", 35, new() { new("Retail", 18), new("Online", 12), new("Partner", 5) }),
    new("South", 25, new() { new("Retail", 10), new("Online", 9), new("Partner", 6) })
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | Collection of Mekko columns. | `null` |
| `CategoryPath` | Path to the column label. | `null` |
| `WidthPath` | Path to the value that controls column width. | `null` |
| `SegmentsPath` | Path to the segment collection for each column. | `null` |
| `ColumnGap` | Gap between columns. | `2.0` |
| `ShowLabels` | Whether to show column labels. | `true` |
| `ShowPercentages` | Whether to draw percentage labels inside segments. | `true` |

## 另请参阅 {#see-also}

- [堆叠条形图](/controls/data-display/charts/cartesian/stacked-bar-chart)
- [条形图](/controls/data-display/charts/cartesian/bar-chart)
