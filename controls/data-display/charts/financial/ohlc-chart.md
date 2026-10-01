---
id: ohlc-chart
title: OHLC 图
description: 用带左右短横的竖线表示开盘、最高、最低、收盘价，是价格数据的专业标准画法。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFinancialOhlc from '/img/controls/charts/charts-financial-ohlc.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

OHLC 图展示某一周期的开盘价、最高价、最低价和收盘价。它与 K 线图类似，但用带横向短刻度的竖线来表示价格区间和开收盘价。

<Image light={chartsFinancialOhlc} maxWidth={400} position="center" cornerRadius="true" alt="OHLC chart showing open, high, low, and close prices as vertical lines with horizontal tick marks per period." />

## 适用场景 {#when-to-use}
- **交易分析**：呈现价格行为，又没有蜡烛实体那种「厚重感」。
- **市场趋势**：看出特定时间区间内的走势和价格区间。
- **大宗商品/股票追踪**：价格数据的专业标准画法。

## 代码示例 {#code-example}

### XAML
```xml
<FinancialChart xmlns="https://github.com/avaloniaui" Name="OhlcChartSample" Title="Commodity Futures" Height="300">
    <FinancialChart.Series>
        <OhlcSeries ItemsSource="{Binding OhlcData}"
                             HighPath="High" LowPath="Low"
                             OpenPath="Open" ClosePath="Close"
                             DatePath="Date" />
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

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 金融数据点的集合。 | `null` |
| `OpenPath` | 指向「开盘价」属性的路径。 | `null` |
| `HighPath` | 指向「最高价」属性的路径。 | `null` |
| `LowPath` | 指向「最低价」属性的路径。 | `null` |
| `ClosePath` | 指向「收盘价」属性的路径。 | `null` |
| `DatePath` | 指向横轴所用日期或时间值的路径。取值可以是 `DateTime`、`DateTimeOffset`，或可解析的日期字符串。 | `null` |
| `UpStroke` | `Close >= Open` 时柱体的轮廓画刷。 | `#4CAF50` |
| `DownStroke` | `Close < Open` 时柱体的轮廓画刷。 | `#F44336` |
| `StrokeThickness` | 线条的粗细。 | `2.0` |
| `TickWidth` | 开盘和收盘短刻度的长度，单位为像素。 | `6.0` |

## 另请参阅 {#see-also}

- [金融图表](/controls/data-display/charts/financial/financial-chart)
- [K 线图](/controls/data-display/charts/financial/candlestick-chart)
