---
id: wind-rose-chart
title: Wind rose chart
description: Shows directional frequency distributions as stacked polar sectors, useful for wind, traffic, and directional event analysis.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Wind rose charts group values by direction and stack subcategories such as speed bands within each directional sector.

## 适用场景 {#when-to-use}

- **Meteorology**: Show wind frequency by direction and speed band.
- **Directional events**: Compare traffic, movement, or signal occurrences around a compass.
- **Operational analysis**: Summarize heading-based activity in one compact polar chart.

## 代码示例 {#code-example}

### XAML

```xml
<WindRoseChart xmlns="https://github.com/avaloniaui" Title="Wind distribution"
                                Height="320"
                                ItemsSource="{Binding WindData}"
                                DirectionPath="Direction"
                                SpeedPath="SpeedBand"
                                ValuePath="Frequency" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record WindSample(string Direction, string SpeedBand, double Frequency);

public ObservableCollection<WindSample> WindData { get; } = new()
{
    new("N", "0-10", 12),
    new("N", "10-20", 6),
    new("NE", "0-10", 8)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | Collection of directional observations. | `null` |
| `DirectionPath` | Path to the direction group. | `null` |
| `SpeedPath` | Path to the stacked subgroup within each direction. | `null` |
| `ValuePath` | Path to the numeric value or frequency. | `null` |
| `StartAngle` | Start angle in degrees for the first sector. | `-90.0` |

## 另请参阅 {#see-also}

- [Polar chart](/controls/data-display/charts/radial/polar-chart)
- [Smith chart](/controls/data-display/charts/engineering/smith-chart)
