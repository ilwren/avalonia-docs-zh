---
id: gauge-chart
title: Gauge chart
description: Displays a single value on a dial-style gauge with an arc fill and optional needle.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Gauge charts render a single value on a dial-style arc, with optional needle and formatted value text.

## 适用场景 {#when-to-use}

- **Operational dashboards**: Show utilization, load, or health in a compact dial.
- **Threshold monitoring**: Emphasize a single current reading over time history.
- **Status cards**: Present one metric with strong visual weight.

## 代码示例 {#code-example}

### XAML

```xml
<GaugeChart xmlns="https://github.com/avaloniaui" Title="CPU load"
                     Width="220"
                     Height="160"
                     Value="{Binding CpuLoad}"
                     MaxValue="100"
                     ShowNeedle="True" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public double CpuLoad { get; set; } = 67;
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | Current value displayed by the gauge. | `50.0` |
| `MinValue` | 标尺的最小值。 | `0.0` |
| `MaxValue` | 标尺的最大值。 | `100.0` |
| `ValueBrush` | Brush used for the value arc. | `null` |
| `TrackBrush` | Brush used for the background track. | `null` |
| `NeedleBrush` | Brush used for the needle. | `null` |
| `ShowNeedle` | Whether to draw the needle. | `true` |
| `StartAngle` | Start angle of the gauge arc in degrees. | `135.0` |
| `SweepAngle` | Sweep angle of the gauge arc in degrees. | `270.0` |
| `TrackThickness` | Thickness of the track arc. | `20.0` |
| `ShowValue` | Whether to display the formatted value text. | `true` |
| `ValueFormat` | Format string used for the value text. | `"{0:F0}"` |

## 另请参阅 {#see-also}

- [Circular gauge](/controls/data-display/charts/gauges/circular-gauge-chart)
- [Progress donut chart](/controls/data-display/charts/gauges/progress-donut-chart)
