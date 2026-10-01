---
id: spiral-timeline-chart
title: 螺旋时间线
description: 把时间序列卷成一条螺线，在同一张图里同时呈现长期走势和反复出现的周期规律。
doc-type: reference
tags:
  - avalonia pro
---

import chartsTimelineSpiral from '/img/controls/charts/charts-timeline-spiral.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

螺旋时间线适合呈现那些既有明显先后顺序、又带周期规律的数据。把时间轴卷成螺线之后，长期趋势和短期往复都能看得清楚。

<Image light={chartsTimelineSpiral} maxWidth={400} position="center" cornerRadius="true" alt="Spiral timeline chart wrapping chronological data into an outward spiral to show both long-term trends and cyclical patterns." />

## 适用场景 {#when-to-use}

- **长周期数据**：呈现数十年间逐年的气候变化。
- **系统日志**：发现服务器活动在数周或数月间的规律。
- **生理节律**：呈现睡眠模式或活动周期随时间的变化。

## 代码示例 {#code-example}

### XAML

```xml
<SpiralTimeline xmlns="https://github.com/avaloniaui" Name="SpiralTimelineSample"
                                             Title="Annual Events"
                                             Height="400"
                                             ItemsSource="{Binding SpiralEvents}"
                                             ValuePath="Value"
                                             LabelPath="Event" />
```

### 数据模型（C#） {#data-model-c}

```csharp
using System;

public record SpiralEvent(DateTime Date, string Event, double Value);

public ObservableCollection<SpiralEvent> SpiralEvents { get; } = new()
{
    new(new DateTime(2024, 1, 1), "New Year", 1.0),
    new(new DateTime(2024, 3, 20), "Spring", 2.0),
    new(new DateTime(2024, 6, 21), "Summer", 3.0),
    new(new DateTime(2024, 9, 22), "Autumn", 2.0),
    new(new DateTime(2024, 12, 21), "Winter", 1.0)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 螺线上各数据点的集合。 | `null` |
| `DatePath` | 指向时间属性的路径。 | `null` |
| `ValuePath` | 决定数据点大小/颜色的数值属性。 | `null` |
| `LabelPath` | 指向各数据点文本标签的路径。 | `null` |
| `Turns` | 螺线的圈数。 | `3.0` |
| `InnerRadius` | 螺线的内半径。 | `30.0` |
| `MarkerSize` | 数据点标记的大小。 | `8.0` |
