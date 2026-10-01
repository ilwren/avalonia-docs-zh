---
id: kpi-card
title: KPI 卡片
description: 以聚焦的形式呈现关键业务指标：一个醒目的数值，配上趋势指示和迷你走势图。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsKpi from '/img/controls/charts/charts-analytics-kpi.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

KPI 卡片以聚焦的形式呈现关键业务指标，通常是一个醒目的数值，再配上趋势指示和一条迷你走势图作为参照。

<Image light={chartsAnalyticsKpi} maxWidth={400} position="center" cornerRadius="true" alt="KPI card displaying a large metric value with a trend indicator and a mini sparkline chart for context." />

## 适用场景 {#when-to-use}
- **管理层仪表板**：让人一眼掌握主要业务目标的达成情况。
- **性能监控**：实时追踪活跃用户数、服务器负载等指标。
- **财务概览**：在报表顶部展示营收、支出和增长情况。

## 代码示例 {#code-example}

### XAML
```xml
<WrapPanel Orientation="Horizontal" HorizontalAlignment="Center">
    <KpiCard xmlns="https://github.com/avaloniaui" Title="Revenue" Width="180" Height="160" Margin="10"
                    Value="{Binding Kpi1.Value}" Unit="{Binding Kpi1.Unit}"
                    Delta="{Binding Kpi1.Delta}" Subtitle="{Binding Kpi1.Subtitle}"
                    SparklineData="{Binding Kpi1.SparklineData}" />
    <KpiCard Title="Users" Width="180" Height="160" Margin="10"
                    Value="{Binding Kpi2.Value}" Unit="{Binding Kpi2.Unit}"
                    Delta="{Binding Kpi2.Delta}" Subtitle="{Binding Kpi2.Subtitle}"
                    SparklineData="{Binding Kpi2.SparklineData}" />
    <KpiCard Title="Bounce Rate" Width="180" Height="160" Margin="10"
                    Value="{Binding Kpi3.Value}" Unit="{Binding Kpi3.Unit}"
                    Delta="{Binding Kpi3.Delta}" Subtitle="{Binding Kpi3.Subtitle}"
                    SparklineData="{Binding Kpi3.SparklineData}"
                    NegativeBrush="{Binding Kpi3.NegativeBrush}" />
</WrapPanel>
```

### 数据模型（C#） {#data-model-c}
```csharp
using Avalonia.Media;

public record KpiItem(
    double Value,
    string? Unit,
    double Delta,
    string Subtitle,
    double[] SparklineData,
    IBrush? NegativeBrush = null);

public KpiItem Kpi1 { get; } = new(
    124500,
    "$",
    12.5,
    "vs last month",
    [10.0, 12, 11, 14, 13, 15, 16, 14, 18, 20.0]);

public KpiItem Kpi2 { get; } = new(
    4532,
    null,
    8.2,
    "New users",
    [50.0, 55, 52, 58, 60, 65, 62, 70, 75, 80.0]);

public KpiItem Kpi3 { get; } = new(
    24.5,
    "%",
    -2.1,
    "Bounce rate",
    [30.0, 28, 29, 27, 26, 25, 24, 25, 24, 24.5],
    Brushes.Green);
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | 要显示的主数值。 | `0` |
| `Delta` | 相对上一期的变化值（正或负）。 | `0` |
| `DeltaType` | 变化量的显示方式：`Percentage` 或 `Absolute`。 | `Percentage` |
| `SparklineData` | 迷你图所用的数值数组。 | `null` |
| `Unit` | 数值的后缀（比如「$」「%」「分」）。 | `null` |
| `Subtitle` | 显示在变化量下方的文字。 | `null` |
| `ValueFormat` | 主数值所用的数值格式字符串。 | `"N0"` |
| `PositiveBrush` | 变化量为正时所用的画刷。 | `null`（绿色，见下方说明） |
| `NegativeBrush` | 变化量为负时所用的画刷。 | `null`（红色，见下方说明） |
| `SparklineBrush` | 迷你走势图所用的画刷。 | `null`（蓝色，见下方说明） |
| `ShowSparkline` | 是否显示迷你走势图。 | `true` |

:::note
当 `PositiveBrush`、`NegativeBrush` 或 `SparklineBrush` 为 `null` 时，卡片会回落到内置的强调色：正向变化用绿色，负向变化用红色，走势图用蓝色。
:::
