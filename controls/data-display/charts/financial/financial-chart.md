---
id: financial-chart
title: 金融图表
description: 承载 K 线、OHLC 等金融系列的容器图表，提供共享坐标轴和价格网格。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

`FinancialChart` 是 `CandlestickSeries`、`OhlcSeries` 等金融系列的宿主控件，为这些系列提供共享的价格网格、坐标轴和横向类别布局。`MovingAverageSeries` 这类兼容的叠加系列可以在同一套日期与价格坐标空间中绘制。

## 适用场景 {#when-to-use}

- **承载金融系列**：在专门的图表容器中组合一个或多个基于价格的系列。
- **交易视图**：让不同类型的系列复用同一套金融坐标轴和价格网格。
- **系列对比**：把兼容的金融系列叠加到同一条横轴上。

## 代码示例 {#code-example}

### XAML

```xml
<FinancialChart xmlns="https://github.com/avaloniaui" Title="Commodity futures" Height="300">
    <FinancialChart.Series>
        <OhlcSeries ItemsSource="{Binding OhlcData}"
                             DatePath="Date"
                             OpenPath="Open"
                             HighPath="High"
                             LowPath="Low"
                             ClosePath="Close" />
    </FinancialChart.Series>
</FinancialChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
using System;

public record FinancialPoint(DateTime Date, double Open, double High, double Low, double Close);

public ObservableCollection<FinancialPoint> OhlcData { get; } = new(GenerateFinancialData(30));

private static IEnumerable<FinancialPoint> GenerateFinancialData(int count)
{
    var date = DateTime.Today.AddDays(-count);
    var price = 100.0;
    var random = new Random(42);

    for (var i = 0; i < count; i++)
    {
        var open = price;
        var close = open + (random.NextDouble() - 0.5) * 5;
        var high = Math.Max(open, close) + random.NextDouble() * 2;
        var low = Math.Min(open, close) - random.NextDouble() * 2;

        yield return new FinancialPoint(date.AddDays(i), open, high, low, close);
        price = close;
    }
}
```

金融系列的日期值可以是 `DateTime`、`DateTimeOffset`，或能被解析为日期的字符串。

当 `HorizontalAxis` 是 `DateTimeAxis` 时，它的最小值、最大值和标签格式会套用到金融日期域上。金融图表让可见的各交易周期保持等宽槽位，而不是按实际日历时长决定横向距离。

自定义叠加系列只要实现 `IFinancialChartOverlaySeries`，就能在金融图表的坐标空间中绘制。若叠加的数值也应参与价格轴范围的计算，还需实现 `IFinancialChartOverlayBoundsProvider`。`FinancialOverlayRenderContext` 提供金融数据、日期到索引的映射、可见价格范围、已解析的画刷，以及 `TryDateToX`、`ValueToY`、`TryValueToPoint` 等辅助方法。

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Series` | 图表中所渲染的金融系列及兼容叠加系列的内容集合。 | 空集合 |
| `HorizontalAxis` | 用于日期或类别位置的横轴。 | `null` |
| `VerticalAxis` | 用于价格数值的纵轴。 | `null` |
| `GridLineBrush` | 坐标轴未指定自己的网格线画刷时，网格线所用的默认画刷。 | `null` |
| `AxisBrush` | 轴线和刻度所用的画刷。 | `null` |
| `PlotAreaBackground` | 绘图区可选的背景画刷。 | `null` |
| `IsHighlightEnabled` | 当系列自身未启用时，为金融数据点启用悬停高亮。 | `false` |

## 另请参阅 {#see-also}

- [K 线图](/controls/data-display/charts/financial/candlestick-chart)
- [OHLC 图](/controls/data-display/charts/financial/ohlc-chart)
- [趋势线图](/controls/data-display/charts/shared-elements/trendline-chart)
