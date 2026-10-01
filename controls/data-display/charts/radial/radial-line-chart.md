---
id: radial-line-chart
title: 径向折线图
description: 在极坐标系上绘制数据点并以线相连，适合呈现某个变量在周期性或方向性类别上的起伏。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

径向折线图在 `PolarChart` 上绘制数据点并以线相连，具体由 `PolarLineSeries` 定义。要呈现单个变量在周期性类别上的起伏，它最为合适。

## 适用场景 {#when-to-use}
- **日常活动**：呈现 24 小时内的心率或精力水平。
- **方向性数据**：呈现 360 度传感器的读数。
- **对称性分析**：在多变量画像中检查规律与均衡。

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
| `ItemsSource` | 待连接的数据点集合。 | `null` |
| `AnglePath` | 角度（X）的路径。 | `null` |
| `RadiusPath` | 半径（Y）的路径。 | `null` |
| `ShowMarkers` | 是否在每个数据点处显示标记。 | `false` |
| `MarkerSize` | 标记的大小。 | `8.0` |
| `IsClosed` | 首尾两个数据点是否相连。 | `false` |
