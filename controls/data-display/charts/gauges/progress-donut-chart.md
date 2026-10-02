---
id: progress-donut-chart
title: 进度环形图
description: 环形图的变体，用来呈现朝单一 100% 目标推进的进度，常见于仪表板和健身类应用。
doc-type: reference
tags:
  - avalonia pro
---

import chartsGaugesProgressDonut from '/img/controls/charts/charts-pie-progressdonut.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

进度环形图是环形图的特化变体，专门用来呈现朝单一 100% 目标推进的进度，健身应用和系统仪表板中常常见到。

<Image light={chartsGaugesProgressDonut} maxWidth={400} position="center" cornerRadius="true" alt="Progress donut chart showing a circular arc filling proportionally to represent completion toward a 100% goal." />

## 适用场景 {#when-to-use}
- **目标完成度**：展示用户离目标还有多远。
- **指标摘要**：呈现基于百分比的数据（比如磁盘占用）。
- **KPI 仪表板**：让人一眼看清关键绩效指标。

## 代码示例 {#code-example}

### XAML
```xml
<WrapPanel Orientation="Horizontal" HorizontalAlignment="Center">
    <ProgressDonutChart xmlns="https://github.com/avaloniaui" Value="75" Width="180" Height="180" IsTooltipEnabled="True" Title="Downloads" Margin="10" />
    <ProgressDonutChart Value="42" Width="180" Height="180" IsTooltipEnabled="True" Title="Uploads" Margin="10" />
    <ProgressDonutChart Value="90" Width="180" Height="180" IsTooltipEnabled="True" Title="Active" Margin="10" />
</WrapPanel>
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | 当前值（0 到 MaxValue）。 | `0` |
| `MaxValue` | 最大值。 | `100.0` |
| `ValueBrush` | 进度弧所用的画刷。 | Theme-dependent |
| `TrackBrush` | 圆环空白部分所用的画刷。 | Theme-dependent |
| `RingThickness` | 圆环的宽度。 | `20.0` |
| `StartAngle` | 起始角度，单位为度（-90 表示正上方）。 | `-90.0` |
| `ShowPercentage` | 是否在中心显示百分比。 | `true` |
| `CenterLabel` | 自定义的中心文字（会覆盖百分比）。 | `null` |
| `IsValueAnimationEnabled` | 数值弧变化时是否播放动画。 | `false` |
| `ShowGlow` | 是否在动态数值弧周围绘制辉光效果。 | `false` |
