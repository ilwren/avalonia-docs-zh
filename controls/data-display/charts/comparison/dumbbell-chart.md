---
id: dumbbell-chart
title: 哑铃图
description: 用一条连线和两个标记点连接每个类别的两个数值，适合作前后对比或高低值对比。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

哑铃图为每个类别连接两个标记点，让人一眼看清低值与高值之间的差距。

## 适用场景 {#when-to-use}

- **前后对比**：比较同一指标在两个时间点上的取值。
- **区间审视**：展示每个类别两个相关数值之间的跨度。
- **目标与实际**：把实测值与基准值配对呈现。

## 代码示例 {#code-example}

### XAML

```xml
<DumbbellChart xmlns="https://github.com/avaloniaui" Title="Planned vs actual"
                        Height="300"
                        ItemsSource="{Binding PlannedVsActual}"
                        LabelPath="Label"
                        LowValuePath="Planned"
                        HighValuePath="Actual" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record RangeComparison(string Label, double Planned, double Actual);

public ObservableCollection<RangeComparison> PlannedVsActual { get; } = new()
{
    new("Team A", 42, 55),
    new("Team B", 38, 41),
    new("Team C", 50, 62)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 对比项的集合。 | `null` |
| `LowValuePath` | 指向较低值或第一个值的路径。 | `null` |
| `HighValuePath` | 指向较高值或第二个值的路径。 | `null` |
| `LabelPath` | 指向类别标签的路径。 | `null` |
| `LowBrush` | 第一个标记点所用的画刷。 | `#2196F3` |
| `HighBrush` | 第二个标记点所用的画刷。 | `#4CAF50` |
| `ConnectorBrush` | 连接线所用的画刷。 | `#9E9E9E` |
| `MarkerSize` | 标记点大小，单位为像素。 | `12.0` |
| `ConnectorThickness` | 连接线的粗细。 | `3.0` |
| `Orientation` | 版面方向，`Horizontal` 或 `Vertical`。 | `Horizontal` |
| `IsHighlightEnabled` | 为哑铃项启用悬停高亮。 | `false` |

## 另请参阅 {#see-also}

- [斜率图](/controls/data-display/charts/analytics/slope-chart)
- [双向条形图](/controls/data-display/charts/comparison/diverging-bar-chart)
