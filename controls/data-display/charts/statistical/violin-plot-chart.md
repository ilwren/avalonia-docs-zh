---
id: violin-plot-chart
title: 小提琴图
description: 把箱线图与核密度估计结合起来，既给出统计摘要，又呈现各类别数据的概率分布形态。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

小提琴图把箱线图与核密度图结合在一起，既给出统计摘要，也呈现数据在各个取值上的概率密度。

## 适用场景 {#when-to-use}

- **深入看分布**：需要知道数据点在哪一段最为密集（密度）时。
- **对比**：既比较多个组别的取值范围（箱线图），也比较各自的形态（密度）。
- **多峰数据**：找出箱线图可能掩盖掉的多峰（多众数）数据。

## 代码示例 {#code-example}

### XAML

```xml
<ViolinPlotChart xmlns="https://github.com/avaloniaui" Name="ViolinPlotSample"
                           Title="Response Times"
                           Height="300"
                           CategoryPath="Group"
                           ValuesPath="DataPoints"
                           ItemsSource="{Binding ViolinSeries}" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record ViolinGroup(string Group, ObservableCollection<double> DataPoints);

public ObservableCollection<ViolinGroup> ViolinSeries { get; } = new()
{
    new("Backend", new() { 12, 15, 12, 18, 25, 30, 12, 14 }),
    new("Frontend", new() { 50, 55, 60, 50, 45, 80, 50, 52 })
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 数据分组的集合。 | `null` |
| `ValuesPath` | 指向各类别数值集合的路径。支持的类型有 `IEnumerable<double>`、`IEnumerable<int>` 和 `double[]`。 | `null` |
| `CategoryPath` | 指向类别名称的路径。 | `null` |
| `ShowMedian` | 是否在内嵌的箱线图中显示中位数线。只有启用了 `ShowBoxPlot` 且该类别至少有五个数值时才生效。 | `true` |
| `ViolinWidth` | 每个小提琴主体的宽度系数。 | `0.8` |
| `Fill` | 小提琴主体所用的画刷。 | `null` |
| `Stroke` | 小提琴轮廓所用的画刷。 | `null` |
| `StrokeThickness` | 小提琴轮廓的粗细。 | `1.5` |
| `ShowBoxPlot` | 是否显示内部的箱线图。只有某个类别至少有五个数值时，才会绘制四分位叠加层。 | `true` |

:::note
当 `Fill` 或 `Stroke` 为 `null` 时，图表会回落到该类别在调色板中的画刷。作为回落值的 `Fill` 会以较低的不透明度绘制。
:::
