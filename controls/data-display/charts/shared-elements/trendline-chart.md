---
id: trendline-chart
title: 趋势线图
description: 在笛卡尔图表系列上叠加计算得出的趋势线，支持线性、指数、多项式、对数和移动平均等类型。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFeaturesTrendlines from '/img/controls/charts/charts-trendline-1.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

趋势线用在笛卡尔图表中，用来呈现数据的总体走向或规律。它滤掉噪声，把背后的趋势凸显出来，可按线性、多项式、幂函数、指数、对数或移动平均方式拟合。

<Image light={chartsFeaturesTrendlines} maxWidth={400} position="center" cornerRadius="true" alt="Line chart with an overlaid trendline showing a line of best fit." />

## 适用场景 {#when-to-use}

- **销售预测**：依据历史走势推算未来销量。
- **数据平滑**：在波动剧烈的股价或传感器数据中找出规律。
- **绩效评估**：看清吞吐量总体上是在上升还是下降。

## 代码示例 {#code-example}

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Revenue Growth" Height="300">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis Title="Year" />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis Title="Revenue (M)" Minimum="0" />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <LineSeries Title="Revenue"
                           ItemsSource="{Binding LinearData}"
                           CategoryPath="Category"
                           ValuePath="Value"
                           StrokeThickness="2"
                           ShowMarkers="True">
            <LineSeries.Trendlines>
                <Trendline Type="Linear"
                                  Stroke="#E53935"
                                  StrokeThickness="2"
                                  ForwardForecast="1" />
            </LineSeries.Trendlines>
        </LineSeries>
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
public record ChartDataPoint(string Category, double Value);

public ObservableCollection<ChartDataPoint> LinearData { get; } = new()
{
    new("2018", 12),
    new("2019", 15),
    new("2020", 18),
    new("2021", 20),
    new("2022", 25)
};
```

## 常用属性（`Trendline`） {#common-properties-trendline}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Type` | 趋势线所要拟合的数据类型：`Linear`、`Exponential`、`Logarithmic`、`Power`、`Polynomial` 或 `MovingAverage`。 | `Linear` |
| `Stroke` | 绘制趋势线所用的画刷。 | `Gray` |
| `StrokeThickness` | 趋势线的线条粗细。 | `2.0` |
| `StrokeDashStyle` | 趋势线所用的虚线样式。 | `null` |
| `StrokeLineCap` | 趋势线两端的线端样式。 | `Round` |
| `StrokeLineJoin` | 趋势线各段衔接处的拐角连接样式。 | `Round` |
| `IsVisible` | 是否渲染该趋势线。 | `true` |
| `ForwardForecast` | 向前外推多少个单位。 | `0` |
| `BackwardForecast` | 向后外推多少个单位。 | `0` |
| `Period` | 对 `MovingAverage` 而言，参与求平均的数据点个数。 | `2` |
| `PolynomialOrder` | `Type` 为 `Polynomial` 时所用的多项式次数。 | `2` |

## ChartTrendlineSeries

`ChartTrendlineSeries` 是一个独立的系列，通过回归计算绘制趋势线叠加层。它与 `Trendline` 附加属性不同：要直接加进图表的 `Series` 集合，并可通过 `SourceSeries` 引用另一个系列，或使用自己的 `ItemsSource`。

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Explicit Overlay Series" Height="320" ShowLegend="True">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis Title="Index" />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis Title="Value" Minimum="0" />
    </CartesianChart.VerticalAxis>

    <CartesianChart.Series>
        <ScatterSeries x:Name="StandaloneTrendlineSource"
                              Title="Observed Data"
                              ItemsSource="{Binding StandaloneTrendlineData}"
                              CategoryPath="Category"
                              ValuePath="Value"
                              Fill="#455A64"
                              MarkerSize="8" />
        <ChartTrendlineSeries Title="Polynomial Overlay"
                                     SourceSeries="{Binding #StandaloneTrendlineSource}"
                                     TrendlineType="Polynomial"
                                     PolynomialOrder="3"
                                     Stroke="#D32F2F"
                                     StrokeThickness="2.5"
                                     Extend="0.15" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c-1}

```csharp
public record ChartDataPoint(string Category, double Value);

public ObservableCollection<ChartDataPoint> StandaloneTrendlineData { get; } = new()
{
    new("1", 16),
    new("2", 20),
    new("3", 27),
    new("4", 29),
    new("5", 38),
    new("6", 43),
    new("7", 47),
    new("8", 56)
};
```

### `ChartTrendlineSeries` 的属性 {#charttrendlineseries-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `TrendlineType` | 回归类型：`Linear`、`Polynomial`、`Exponential`、`Logarithmic`、`Power` 或 `MovingAverage`。 | `Linear` |
| `PolynomialOrder` | `TrendlineType` 为 `Polynomial` 时所用的多项式次数。 | `2` |
| `Period` | `TrendlineType` 为 `MovingAverage` 时所取的数据点个数。 | `2` |
| `SourceSeries` | 据以计算趋势线的系列。为 `null` 时，直接使用 `ItemsSource`。 | `null` |
| `Extend` | 趋势线在数据范围之外延伸多远，以比例表示（比如 `0.1` 表示 10%）。 | `0` |

## MovingAverageSeries

`MovingAverageSeries` 为金融或时间序列数据显示移动平均叠加层，支持简单（SMA）、指数（EMA）、加权（WMA）和三角（TMA）四种移动平均算法。它既可用在 `CartesianChart` 中，也可作为叠加层用在 `FinancialChart` 中，跟随金融图表的日期与价格坐标。

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Price with Moving Average" Height="300">
    <CartesianChart.Series>
        <LineSeries x:Name="PriceSeries"
                             ItemsSource="{Binding PriceData}"
                             CategoryPath="Date"
                             ValuePath="Close" />
        <MovingAverageSeries Title="SMA (14)"
                                      SourceSeries="{Binding #PriceSeries}"
                                      MovingAverageType="Simple"
                                      Period="14"
                                      Stroke="Orange"
                                      StrokeThickness="2" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c-2}

```csharp
using System;

public record PricePoint(DateTime Date, double Close);

public ObservableCollection<PricePoint> PriceData { get; } = new()
{
    new(new DateTime(2026, 1, 1), 100),
    new(new DateTime(2026, 1, 2), 104),
    new(new DateTime(2026, 1, 3), 101),
    new(new DateTime(2026, 1, 4), 108),
    new(new DateTime(2026, 1, 5), 112)
};
```

### `MovingAverageSeries` 的属性 {#movingaverageseries-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `MovingAverageType` | 计算类型：`Simple`、`Exponential`、`Weighted` 或 `Triangular`。 | `Simple` |
| `Period` | 移动平均窗口所取的数据点个数。 | `14` |
| `SourceSeries` | 据以计算移动平均的系列。为 `null` 时，直接使用 `ItemsSource`。 | `null` |

## 另请参阅 {#see-also}

- [折线图](/controls/data-display/charts/cartesian/line-chart)
- [散点图](/controls/data-display/charts/cartesian/scatter-chart)
- [坐标轴定制](/controls/data-display/charts/shared-elements/axis-customization-chart)
