---
id: swimlane-chart
title: 泳道图
description: 把任务或流程编入一条条横向泳道，呈现责任归属，以及跨部门、跨角色、跨成员的时序安排。
doc-type: reference
tags:
  - avalonia pro
---

import chartsTimelineSwimlane from '/img/controls/charts/charts-timeline-swimlane.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

泳道图把任务或流程编入一条条清晰的横向或纵向「泳道」，便于呈现跨部门、跨角色的工作流。

<Image light={chartsTimelineSwimlane} maxWidth={400} position="center" cornerRadius="true" alt="Swimlane chart organizing tasks into horizontal lanes by department or role showing ownership and time overlap." />

## 适用场景 {#when-to-use}

- **流程梳理**：呈现一项请求如何在销售、研发和客服之间流转。
- **项目排期**：呈现各项任务由哪位成员负责。
- **跨职能协作**：厘清复杂业务流程中的权责划分。

## 代码示例 {#code-example}

### XAML

```xml
<SwimlaneChart xmlns="https://github.com/avaloniaui" Name="SwimlaneSample"
                                            Title="Process Flow"
                                            Height="350"
                                            ItemsSource="{Binding SwimlaneTasks}"
                                            LanePath="Lane"
                                            TaskNamePath="Task"
                                            StartPath="Start"
                                            EndPath="End"
                                            BrushPath="Brush"
                                            LaneHeight="90"
                                            TaskHeight="34"
                                            TaskSpacing="8"
                                            TaskCornerRadius="8"
                                            LaneSeparatorBrush="{DynamicResource DemoSwimlaneLaneSeparatorBrush}"
                                            LaneBackgroundBrush="{DynamicResource DemoSwimlaneLaneBackgroundBrush}" />
```

### 数据模型（C#） {#data-model-c}

```csharp
using Avalonia.Media;

public record SwimlaneTask(string Lane, string Task, double Start, double End, IBrush? Brush = null);

public ObservableCollection<SwimlaneTask> SwimlaneTasks { get; } = new()
{
    new("Design", "Wireframes", 0, 3, Brushes.DodgerBlue),
    new("Design", "Mockups", 2, 5, Brushes.SteelBlue),
    new("Development", "Frontend", 4, 10, Brushes.SeaGreen),
    new("Development", "Backend", 3, 9, Brushes.MediumSeaGreen),
    new("Testing", "Unit Tests", 6, 10, Brushes.Orange),
    new("Testing", "Integration", 9, 12, Brushes.DarkOrange),
    new("Deployment", "Staging", 11, 13, Brushes.MediumPurple),
    new("Deployment", "Production", 13, 14, Brushes.Purple)
};
```

`StartPath` 和 `EndPath` 需要数值。用你自己的刻度即可，比如天数、小时、迭代点数或序号位置。同一泳道中相互重叠的任务会由 `TaskSpacing` 分行堆叠。

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 任务/条目的集合。 | `null` |
| `LanePath` | 决定该任务归属哪条泳道。 | `null` |
| `TaskNamePath` | 单个任务块的标签。 | `null` |
| `StartPath` | 任务起始数值所对应的属性名。 | `null` |
| `EndPath` | 任务结束数值所对应的属性名。 | `null` |
| `BrushPath` | 用于为每个任务绑定 `IBrush` 或颜色字符串的属性名。 | `null` |
| `LaneHeight` | 每条泳道的高度。 | `80.0` |
| `TaskHeight` | 每根任务条的高度。 | `30.0` |
| `TaskSpacing` | 同一泳道内任务堆叠时的间距。 | `5.0` |
| `LaneSeparatorBrush` | 泳道分隔线所用的画刷。 | `null` |
| `LaneBackgroundBrush` | 泳道交替背景所用的画刷。 | `null` |
| `ShowTaskLabels` | 是否在任务条内部显示标签。 | `true` |
| `TaskCornerRadius` | 任务条的圆角半径。 | `4.0` |

## 另请参阅 {#see-also}

- [甘特图](/controls/data-display/charts/scheduling/gantt-chart)
- [时间线图](/controls/data-display/charts/scheduling/timeline-chart)
