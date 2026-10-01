---
id: gradient-ring-chart
title: 渐变圆环图
description: 绘制多个同心进度环，每一环代表一个带标签的数值，共用同一个最大值作参照。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

渐变圆环图把若干同心进度环画在一起，每一项占一环，于是成组的状态指示能在紧凑的版面中两相比较。

## 适用场景 {#when-to-use}

- **多指标状态**：用一个紧凑的控件展示多项进度。
- **能力仪表板**：比较少数几个类别的完成度或健康度。
- **环形摘要**：当各项数值共用同一刻度时，用它取代一摞进度环形图。

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
| `ItemsSource` | 圆环项的集合。 | `null` |
| `LabelPath` | 指向项标签的路径。 | `null` |
| `ValuePath` | 指向数值的路径。 | `null` |
| `MaxValue` | 用于归一化的共享最大值。 | `100.0` |
| `RingThickness` | 每一环的粗细。 | `15.0` |
| `RingGap` | 相邻圆环之间的间隙。 | `8.0` |
| `ShowLabels` | 是否显示图例标签。 | `true` |
| `ShowValues` | 是否显示数值。 | `true` |

## 另请参阅 {#see-also}

- [进度环形图](/controls/data-display/charts/gauges/progress-donut-chart)
- [仪表图](/controls/data-display/charts/gauges/gauge-chart)
