---
id: calendar-heatmap-chart
title: 日历热力图
description: 以日历网格展示每天的活跃强度，适合呈现贡献记录、使用情况和习惯打卡。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

日历热力图把每日数值绘制在逐周排布的网格中，类似常见的贡献图和活跃度追踪图。

## 适用场景 {#when-to-use}

- **活跃度追踪**：按天展示提交、登录、锻炼或交易次数。
- **季节性回顾**：一眼看出一年中的淡季和旺季。
- **留存视图**：不必动用完整的时间序列图，就能凸显连续天数和中断。

## 代码示例 {#code-example}

### XAML

```xml
<CalendarHeatmapChart xmlns="https://github.com/avaloniaui" Title="Repository activity"
                               Height="180"
                               ItemsSource="{Binding DailyActivity}"
                               DatePath="Date"
                               ValuePath="Count"
                               WeeksToShow="26" />
```

### 数据模型（C#） {#data-model-c}

```csharp
using System;

public record DailyCount(DateTime Date, double Count);

public ObservableCollection<DailyCount> DailyActivity { get; } = new()
{
    new(DateTime.Today.AddDays(-3), 5),
    new(DateTime.Today.AddDays(-2), 2),
    new(DateTime.Today.AddDays(-1), 7)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 每日活动项的集合。 | `null` |
| `DatePath` | 指向每一项日期值的路径。 | `null` |
| `ValuePath` | 指向强度数值的路径。 | `null` |
| `CellSize` | 每个日格的大小，单位为像素。 | `12.0` |
| `CellGap` | 日格之间的间隙。 | `2.0` |
| `EmptyCellBrush` | 无数值的日期所用的画刷。 | `null` |
| `LowBrush` | 低强度数值所用的画刷。 | `null` |
| `MediumBrush` | 中等强度数值所用的画刷。 | `null` |
| `HighBrush` | 高强度数值所用的画刷。 | `null` |
| `MaxBrush` | 最高强度数值所用的画刷。 | `null` |
| `ShowMonthLabels` | 是否在网格上方显示月份标签。 | `true` |
| `ShowDayLabels` | 是否显示星期标签。 | `true` |
| `LabelFontSize` | 月份标签、星期标签和图例文字所用的字号。 | `10.0` |
| `LabelForeground` | 日历标签和图例所用的画刷。为 `null` 时，图表采用当前生效的标签前景色。 | `null` |
| `WeeksToShow` | 显示多少周。 | `52` |
| `IsHighlightEnabled` | 为日历单元格启用悬停高亮。 | `false` |
| `ReferenceDate` | 可选的结束日期，用作日历的基准点。 | `null` |

## 另请参阅 {#see-also}

- [热力图](/controls/data-display/charts/analytics/heatmap-chart)
- [时间线图](/controls/data-display/charts/scheduling/timeline-chart)
