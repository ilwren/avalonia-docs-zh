---
id: sparkline-chart
title: 迷你走势图
description: 不带坐标轴的小巧图表，用来在极小的空间里呈现数据走势，适合嵌进表格、仪表板或正文中。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsSparkline from '/img/controls/charts/charts-analytics-sparkline.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

迷你走势图（Sparkline）是一种不带坐标轴和刻度的紧凑图表，用于在卡片、表格单元格、仪表板磁贴这类狭小空间里呈现一组数值的走势。

<Image light={chartsAnalyticsSparkline} maxWidth={400} position="center" cornerRadius="true" alt="Sparkline chart examples showing line, area, bar, and win/loss trends." />

## 适用场景 {#when-to-use}

- **行内走势**：在数据网格或正文段落中呈现数据走势。
- **仪表板摘要**：在一屏之内为众多指标提供高密度的视觉参照。
- **紧凑呈现**：趋势的大致形态比具体数值更重要时。

## 代码示例 {#code-example}

### XAML

```xml
<Grid ColumnDefinitions="Auto,*" RowDefinitions="Auto,Auto,Auto,Auto" Margin="10">
    <TextBlock Text="Line:" VerticalAlignment="Center" Margin="0,0,10,5" />
    <SparklineChart xmlns="https://github.com/avaloniaui" Grid.Column="1" Height="40" SparklineType="Line" ItemsSource="{Binding SparklineData}"/>
    <TextBlock Grid.Row="1" Text="Area:" VerticalAlignment="Center" Margin="0,0,10,5" />
    <SparklineChart Grid.Row="1" Grid.Column="1" Height="40" SparklineType="Area" ItemsSource="{Binding SparklineData}"/>
    <TextBlock Grid.Row="2" Text="Bar:" VerticalAlignment="Center" Margin="0,0,10,5" />
    <SparklineChart Grid.Row="2" Grid.Column="1" Height="40" SparklineType="Bar" ItemsSource="{Binding SparklineData}"/>
    <TextBlock Grid.Row="3" Text="Win/Loss:" VerticalAlignment="Center" Margin="0,0,10,5" />
    <SparklineChart Grid.Row="3" Grid.Column="1" Height="40" SparklineType="WinLoss" ItemsSource="{Binding SparklineWinLossData}"/>
</Grid>
```

### 数据模型（C#） {#data-model-c}

```csharp
public ObservableCollection<double> SparklineData { get; } = new()
{
    5, 10, 8, 15, 12, 20, 18, 25, 22, 30
};

public ObservableCollection<double> SparklineWinLossData { get; } = new()
{
    1, -1, 1, 1, -1, 1, -1, -1, 1, 1
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 走势数据的集合。 | `null` |
| `ValuePath` | 当 `ItemsSource` 中装的是对象而非原始数字时所使用的属性路径。 | `null` |
| `SparklineType` | 迷你走势图的样式：`Line`、`Area`、`Bar` 或 `WinLoss`。 | `Line` |
| `LineBrush` | `Line` 和 `Area` 两种迷你走势图所用的画刷。 | `null`（蓝色，见下方说明） |
| `AreaFill` | 填充 `Area` 迷你走势图区域所用的画刷。 | `null`（半透明蓝色，见下方说明） |
| `BarBrush` | `Bar` 迷你走势图中条形所用的画刷。 | `null`（蓝色，见下方说明） |
| `WinBrush` | `WinLoss` 迷你走势图中正值所用的画刷。 | `null`（绿色，见下方说明） |
| `LossBrush` | Brush used for negative values in `WinLoss` sparklines. | `null`（红色，见下方说明） |
| `ShowMarkers` | Toggles rendering of individual data point markers. | `false` |
| `ShowMinMax` | Highlights the minimum and maximum values. | `true` |
| `StrokeThickness` | Width of the line stroke for `Line` and `Area` sparklines. | `2.0` |

:::note
The `Brush`-type properties default to these colors when set to `null`:

- `LineBrush`: Blue
- `AreaFill`: Blue, at reduced opacity
- `BarBrush`: Same as `LineBrush`, i.e. blue if both are `null`
- `WinBrush`: Green
- `LossBrush`: Red
:::

## 另请参阅 {#see-also}

- [KPI cards](/controls/data-display/charts/analytics/kpi-card)
- [折线图](/controls/data-display/charts/cartesian/line-chart)
