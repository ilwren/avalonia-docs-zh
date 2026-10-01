---
id: mekko-chart
title: Mekko 图
description: 把宽度不等的柱子与堆叠分段结合起来，同时比较总规模和内部构成。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Mekko 图又称马赛克图（Marimekko），用柱子的不同宽度和各堆叠段的高度，在一张图里同时比较市场规模与构成。

## 适用场景 {#when-to-use}

- **市场格局**：同时比较各类别的份额和内部细分构成。
- **组合构成**：展示各组的总规模及其细分明细。
- **多维对比**：用一张图取代「宽度图 + 堆叠条形图」两张图。

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
| `ItemsSource` | Mekko 柱的集合。 | `null` |
| `CategoryPath` | 指向柱标签的路径。 | `null` |
| `WidthPath` | 指向决定柱宽那个数值的路径。 | `null` |
| `SegmentsPath` | 指向各柱分段集合的路径。 | `null` |
| `ColumnGap` | 柱与柱之间的间隙。 | `2.0` |
| `ShowLabels` | 是否显示柱标签。 | `true` |
| `ShowPercentages` | 是否在各分段内部绘制百分比标签。 | `true` |

## 另请参阅 {#see-also}

- [堆叠条形图](/controls/data-display/charts/cartesian/stacked-bar-chart)
- [条形图](/controls/data-display/charts/cartesian/bar-chart)
