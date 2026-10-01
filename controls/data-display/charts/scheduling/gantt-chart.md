---
id: gantt-chart
title: 甘特图
description: 面向项目管理的专用时间线图表，在横向时间轴上呈现任务工期、起止日期和依赖关系。
doc-type: reference
tags:
  - avalonia pro
---

import chartsTimelineGantt from '/img/controls/charts/charts-timeline-gantt.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

甘特图是项目管理专用的时间线图表，通过呈现任务工期、起止日期和依赖关系来刻画项目排期。

<Image light={chartsTimelineGantt} maxWidth={400} position="center" cornerRadius="true" alt="Gantt chart showing project tasks as horizontal bars on a time axis with start dates, durations, and dependencies." />

## 适用场景 {#when-to-use}
- **项目规划**：找出关键路径和任务重叠。
- **资源管理**：掌握团队成员在各项活动上的投入时段。
- **发布追踪**：呈现一次软件发布的里程碑和截止日期。

## 代码示例 {#code-example}

### XAML
```xml
<GanttChart xmlns="https://github.com/avaloniaui" Name="GanttChartSample" Title="Project Timeline" Height="300"
                     ItemsSource="{Binding GanttTasks}"
                     TaskNamePath="Name"
                     StartPath="Start"
                     EndPath="End"
                     ProgressPath="Progress"
                     BarHeight="0.72"
                     RowHeight="44"
                     BarBrush="#93C5FD"
                     ProgressBrush="#2563EB" />
```

### 数据模型（C#） {#data-model-c}
```csharp
using System;

public record GanttTask(string Name, DateTime Start, DateTime End, double Progress);

public ObservableCollection<GanttTask> GanttTasks { get; } = new()
{
    new("Planning", DateTime.Today, DateTime.Today.AddDays(5), 100),
    new("Design", DateTime.Today.AddDays(3), DateTime.Today.AddDays(10), 80),
    new("Development", DateTime.Today.AddDays(8), DateTime.Today.AddDays(20), 48),
    new("Testing", DateTime.Today.AddDays(18), DateTime.Today.AddDays(25), 18),
    new("Deployment", DateTime.Today.AddDays(24), DateTime.Today.AddDays(28), 0)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 项目任务的集合。 | `null` |
| `StartPath` | 任务开始时间所对应的属性名。 | `null` |
| `EndPath` | 任务结束时间所对应的属性名。 | `null` |
| `TaskNamePath` | 任务标签所对应的属性名。 | `null` |
| `ProgressPath` | 任务进度值所对应的属性名，取值从 `0` 到 `100`。 | `null` |
| `BarHeight` | 每根任务条的高度，以行高的比例表示。 | `0.6` |
| `RowHeight` | 每个任务行的高度，单位为像素。 | `40.0` |
| `BarBrush` | 任务条所用的画刷。 | `#2196F3` |
| `ProgressBrush` | 进度覆盖层所用的画刷。 | `#1565C0` |
