---
id: timeline-chart
title: 事件时间线图
description: 沿时间轴按先后顺序呈现一连串事件，把已发生或已排定的事项交代得一清二楚。
doc-type: reference
tags:
  - avalonia pro
---

import chartsTimelineHorizontal from '/img/controls/charts/charts-timeline-event.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

事件时间线图按时间先后呈现一连串事件，在一条固定的时间轴上把已发生或已排定的事项交代得一清二楚。

<Image light={chartsTimelineHorizontal} maxWidth={400} position="center" cornerRadius="true" alt="Event timeline chart displaying chronological milestones as labeled markers along a horizontal time axis." />

## 适用场景 {#when-to-use}

- **历史记录**：呈现里程碑、产品发布或人生大事。
- **审计轨迹**：按顺序呈现系统日志或用户操作。
- **纵向时间线**：移动端或按列排布的版面用它最合适。

## 代码示例 {#code-example}

### XAML

```xml
<EventTimelineChart xmlns="https://github.com/avaloniaui" Name="EventTimelineSample"
                                                 Title="Product Launches"
                                                 Height="300"
                                                 ItemsSource="{Binding TimelineEvents}"
                                                 DatePath="Date"
                                                 LabelPath="Event" />
```

### 数据模型（C#） {#data-model-c}

```csharp
using System;

public record TimelineEvent(DateTime Date, string Event);

public ObservableCollection<TimelineEvent> TimelineEvents { get; } = new()
{
    new(new DateTime(2024, 1, 15), "v1.0 Release"),
    new(new DateTime(2024, 4, 10), "v2.0 Beta"),
    new(new DateTime(2024, 7, 20), "v2.0 Release"),
    new(new DateTime(2024, 10, 5), "v3.0 Preview"),
    new(new DateTime(2024, 12, 1), "v3.0 Release")
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 事件的集合。 | `null` |
| `DatePath` | 指向 `DateTime` 属性的路径。 | `null` |
| `LabelPath` | 指向事件说明的路径。 | `null` |
| `DescriptionPath` | 指向较长补充文字的可选路径。 | `null` |
| `BrushPath` | 为每一项提供画刷或颜色值的可选路径。 | `null` |
| `MarkerSize` | 事件标记的大小。 | `12.0` |
| `StrokeThickness` | 主时间轴的粗细。 | `2.0` |
| `Orientation` | 图表的方向，`Horizontal` 或 `Vertical`。 | `Horizontal` |
