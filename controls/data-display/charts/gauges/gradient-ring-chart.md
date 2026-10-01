---
id: gradient-ring-chart
title: Gradient ring chart
description: Draws multiple concentric progress rings, each representing a labeled value relative to a shared maximum.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Gradient ring charts render several concentric progress rings with one ring per item, so grouped status indicators can be compared in a compact view.

## 适用场景 {#when-to-use}

- **Multi-metric status**: Show several progress measures in one compact control.
- **Capability dashboards**: Compare completion or health across a small set of categories.
- **Circular summaries**: Replace a stack of progress donuts when values share the same scale.

## 代码示例 {#code-example}

### XAML

```xml
<GradientRingChart xmlns="https://github.com/avaloniaui" Title="Release readiness"
                            Width="280"
                            Height="280"
                            ItemsSource="{Binding RingMetrics}"
                            LabelPath="Label"
                            ValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record RingMetric(string Label, double Value);

public ObservableCollection<RingMetric> RingMetrics { get; } = new()
{
    new("API", 86),
    new("UI", 72),
    new("Docs", 64)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | Collection of ring items. | `null` |
| `LabelPath` | Path to the item label. | `null` |
| `ValuePath` | Path to the numeric value. | `null` |
| `MaxValue` | Shared maximum value used for normalization. | `100.0` |
| `RingThickness` | Thickness of each ring. | `15.0` |
| `RingGap` | Gap between adjacent rings. | `8.0` |
| `ShowLabels` | Whether to show the legend labels. | `true` |
| `ShowValues` | Whether to show numeric values. | `true` |

## 另请参阅 {#see-also}

- [Progress donut chart](/controls/data-display/charts/gauges/progress-donut-chart)
- [Gauge chart](/controls/data-display/charts/gauges/gauge-chart)
