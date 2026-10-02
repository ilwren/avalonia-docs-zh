---
id: legend-chart
title: 图例
description: 用标签和颜色标识图表中的各个数据系列，支持多种摆放位置和排列方向，并可交互式开关系列。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFeaturesLegend from '/img/controls/charts/charts-legend-right.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

图例组件帮用户分辨图表中的各个数据系列。它可以摆在图表区周围，样式也能调成与应用主题一致。

<Image light={chartsFeaturesLegend} maxWidth={400} position="center" cornerRadius="true" alt="Chart with a legend panel showing color-coded series names positioned beside the chart area." />

## 适用场景 {#when-to-use}
- **多系列图表**：只要显示了不止一个系列，它就不可或缺。
- **交互式开关**：需要让用户点击图例项来显示/隐藏某个系列时。
- **复杂图示**：帮助说明颜色或图案所代表的含义（比如饼图或地图中）。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="RightLegendSample"
                        IsTooltipEnabled="True"
                        Title="Right Aligned"
                        Height="250"
                        ShowLegend="True"
                        LegendPosition="Right"
                        LegendAlignment="Center"
                        ToggleSeriesVisibility="True">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <AreaSeries Title="Revenue"
                           ItemsSource="{Binding Data1}" />
        <AreaSeries Title="Profit"
                           ItemsSource="{Binding Data3}" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> Data1 { get; } = new()
{
    10, 20, 30, 40, 50
};

public ObservableCollection<int> Data3 { get; } = new()
{
    5, 15, 10, 20, 10
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ShowLegend` | 开关图例的可见性。 | `false` |
| `LegendPosition` | `None`, `Top`, `Bottom`, `Left`, `Right`, or `Floating`. | `None` |
| `LegendAlignment` | `Near`, `Center`, or `Far`. | `Center` |
| `LegendOffset` | 作用于浮动图例的像素偏移量。 | `0,0` |
| `ToggleSeriesVisibility` | 允许点击图例来开关系列或类别的可见性。`ShapeMap`、`CalendarHeatmapChart`、`WaffleChart` 这类刻度图例会把该值强制为 `false`。 | `true` |

## Legend 控件的属性 {#legend-control-properties}

`ChartLegend` 是各图表共用的可复用图例控件。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Items` | 要显示的图例项集合。 | `null` |
| `Orientation` | 图例条目的排列方向，`Horizontal` 或 `Vertical`。 | `Vertical` |
| `MarkerSize` | 每个图例标记的大小，单位为像素。 | `12.0` |
| `ItemSpacing` | 图例项之间的间距，单位为像素。 | `8.0` |

## 图例项模型 {#legend-item-model}

图例条目由 `ChartLegendItem` 表示。内置系列会自动创建图例项，并挑选与所渲染系列样式相称的标记形状，比如折线、色带、蜡烛、雷达、OHLC 或点数图标记。自定义系列可以重写 `CreateLegendItem` 来改变标记、来源对象或开关行为。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Text` | 图例项所显示的文字。 | `null` |
| `Fill` | 标记的填充画刷。 | `null` |
| `Stroke` | 标记的描边画刷。 | `null` |
| `SecondaryFill` | 复合标记（比如金融标记或色带）所用的第二填充画刷。 | `null` |
| `SecondaryStroke` | 复合标记（比如金融标记或色带）所用的第二描边画刷。 | `null` |
| `MarkerShape` | 标记形状：`Rectangle`、`Circle`、`Line`、`Candlestick`、`Band`、`Radar`、`Ohlc` 或 `PointAndFigure`。 | `Rectangle` |
| `IsVisible` | 该图例项所代表的可见性状态。 | `true` |
| `SeriesIndex` | 关联的系列索引。 | `0` |
| `Source` | 该图例项所代表的系列、技术指标或图表元素。 | `null` |
| `ToggleAction` | 图例项被切换时调用的可选动作。 | `null` |

## 事件 {#events}

| 事件 | 说明 |
| :--- | :--- |
| `LegendItemClicked` | 图例项切换其关联对象的可见性之后触发。事件数据提供被点击的 `Item` 和 `IsNowVisible`。 |

## 另请参阅 {#see-also}

- [图表导出](/controls/data-display/charts/shared-elements/export-chart)
- [Markers](/controls/data-display/charts/shared-elements/markers-chart)
