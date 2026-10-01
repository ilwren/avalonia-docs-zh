---
id: radial-line-chart
title: Radial line chart
description: Plots data points on a polar coordinate system connected by lines, suitable for showing how a variable fluctuates across cyclical or directional categories.
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Radial line charts plot data points on a `PolarChart` and connect them with lines, as defined by a `PolarLineSeries`. They are ideal for showing how a single variable fluctuates across cyclical categories.

## 适用场景 {#when-to-use}
- **Daily activity**: Mapping heart rate or energy levels across 24 hours.
- **Directional data**: Visualizing readings from a 360-degree sensor.
- **Symmetry analysis**: Checking for patterns and balance in multi-variate profiles.

## 代码示例 {#code-example}

### XAML
```xml
<PolarChart xmlns="https://github.com/avaloniaui" Title="Hourly Activity" Height="350">
    <PolarChart.Series>
        <PolarLineSeries ItemsSource="{Binding RadialPoints}"
                                  AnglePath="Angle"
                                  RadiusPath="Radius"
                                  ShowMarkers="True" />
    </PolarChart.Series>
</PolarChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record ActivityPoint(double Angle, double Radius);

public ObservableCollection<ActivityPoint> RadialPoints { get; } = new()
{
    new(0, 10),
    new(60, 25),
    new(120, 45),
    new(180, 30),
    new(240, 60),
    new(300, 15)
};
```

## 公共属性：`PolarLineSeries` {#common-properties-polarlineseries}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | The collection of points to connect. | `null` |
| `AnglePath` | Path of the angle (X). | `null` |
| `RadiusPath` | Path of the radius (Y). | `null` |
| `ShowMarkers` | Whether to show markers at each data point. | `false` |
| `MarkerSize` | Size of the markers. | `8.0` |
| `IsClosed` | Whether the first and last data points are connected. | `false` |
