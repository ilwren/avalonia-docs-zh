---
id: waffle-chart
title: 华夫图
description: 用方格网表示百分比或占比，呈现部分与整体的关系以及目标完成度。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsWaffle from '/img/controls/charts/charts-analytics-waffle.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

华夫图（又称方块饼图）用一片方格网来表示百分比或占比，以网格的形式呈现部分与整体的关系。

<Image light={chartsAnalyticsWaffle} maxWidth={400} position="center" cornerRadius="true" alt="Waffle chart showing a 10x10 grid of squares where filled squares represent a percentage of the total." />

## 适用场景 {#when-to-use}
- **目标完成度**：呈现项目离 100% 的目标还有多远。
- **人口构成**：展示不同群体在总体中的分布。
- **项目追踪**：显示一个迭代周期内已完成任务的百分比。

## 代码示例 {#code-example}

### XAML
```xml
<WrapPanel HorizontalAlignment="Center">
    <WaffleChart xmlns="https://github.com/avaloniaui" Title="Completion" Value="72" Width="150" Height="150" Rows="10" Columns="10" Margin="0,0,20,8" />
    <WaffleChart Title="Progress" Value="45" Width="150" Height="150" Rows="10" Columns="10" Margin="0,0,0,8" />
</WrapPanel>
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | 要显示的当前值。 | `0` |
| `MaxValue` | 用于计算百分比的最大值。 | `100` |
| `Rows` | 华夫网格的行数。 | `10` |
| `Columns` | 华夫网格的列数。 | `10` |
| `FilledBrush` | 已点亮方格所用的画刷。 | Theme-dependent |
| `EmptyBrush` | 未点亮方格所用的画刷。 | Theme-dependent |
| `CellGap` | 华夫格之间的间隙。 | `2.0` |
| `CellCornerRadius` | 华夫格的圆角半径。 | `2.0` |
| `ShowPercentage` | 是否显示百分比文字。 | `true` |
| `Label` | 显示在百分比文字下方的可选标签。 | `null` |
