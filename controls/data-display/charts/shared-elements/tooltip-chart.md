---
id: tooltip-chart
title: 工具提示
description: 在悬停时显示数据点的详细信息，并支持用 DataTemplate 自定义提示内容。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFeaturesTooltip from '/img/controls/charts/charts-tooltips.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

用户悬停在数据点上时，工具提示会给出该点的详细信息。它既补足了精度和背景信息，又不会把图表主体弄乱。

笛卡尔图表和金融图表的默认工具提示，会按图表横轴的格式设置来格式化类别和日期值。

<Image light={chartsFeaturesTooltip} maxWidth={400} position="center" cornerRadius="true" alt="Chart with an interactive tooltip popup appearing on hover showing the exact value and category of a data point." />

## 适用场景 {#when-to-use}
- **高密度数据**：在拥挤的折线图或散点图中精确定位数值。
- **补充信息**：显示那些没有映射到坐标轴上的元数据（比如「更新日期」）。
- **悬停交互**：指针停在某个数据点上时，集中展示该点的细节。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="PerSeriesTooltipsChart" Height="250" IsTooltipEnabled="True">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis Title="Quarter" />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis Title="Revenue" />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <BarSeries Title="2023 (Tooltip ON)"
                          ItemsSource="{Binding Series1Data}"
                          IsTooltipEnabled="True" />
        <BarSeries Title="2024 (Tooltip OFF)"
                          ItemsSource="{Binding Series2Data}"
                          IsTooltipEnabled="False" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<double> Series1Data { get; } = new()
{
    120, 150, 180, 200
};

public ObservableCollection<double> Series2Data { get; } = new()
{
    140, 170, 160, 220
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `IsTooltipEnabled` | Global toggle for tooltip visibility. | `true` |
| `TooltipTemplate` | Custom DataTemplate for the tooltip UI (on series). | System default |

## Data item conventions

If the hit data item has a non-empty string property named `TooltipText`, the default tooltip displays that text instead of generated series, category, and value content.

Use `TooltipTemplate` on a series when the tooltip needs custom layout, controls, or multiple bound fields.
