---
id: spiral-timeline-chart
title: Spiral timeline
description: Wraps a chronological sequence into a spiral to reveal both long-term trends and recurring cyclical patterns within the same visualization.
doc-type: reference
tags:
  - avalonia pro
---

import chartsTimelineSpiral from '/img/controls/charts/charts-timeline-spiral.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Spiral timelines visualize data that has both a strong sequential component and a cyclical pattern. By wrapping the timeline into a spiral, long-term trends and short-term repetitions become visible.

<Image light={chartsTimelineSpiral} maxWidth={400} position="center" cornerRadius="true" alt="Spiral timeline chart wrapping chronological data into an outward spiral to show both long-term trends and cyclical patterns." />

## 适用场景 {#when-to-use}

- **Long-term cyclical data**: Visualizing annual climate changes over several decades.
- **System logs**: Detecting patterns in server activity across weeks or months.
- **Biological rhythms**: Showing sleep patterns or activity cycles over time.

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
| `ItemsSource` | The collection of points on the spiral. | `null` |
| `DatePath` | Path to the chronological property. | `null` |
| `ValuePath` | Numerical property determining point size/color. | `null` |
| `LabelPath` | Path to the text label for each point. | `null` |
| `Turns` | Number of turns in the spiral. | `3.0` |
| `InnerRadius` | Inner radius of the spiral. | `30.0` |
| `MarkerSize` | Size of the data point markers. | `8.0` |
