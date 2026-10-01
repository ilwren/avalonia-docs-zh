---
id: candlestick-chart
title: K 线图
description: 用蜡烛形状的符号展示每个周期的开盘价、最高价、最低价和收盘价，用于金融市场的价格分析。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFinancialCandlestick from '/img/controls/charts/charts-financial-candlestick.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

K 线图用来刻画证券、衍生品或货币的价格随时间的变动。每根蜡烛展示某一周期的开盘价、最高价、最低价和收盘价。

<Image light={chartsFinancialCandlestick} maxWidth={400} position="center" cornerRadius="true" alt="Candlestick chart showing OHLC price data with green bullish and red bearish candles over several trading periods." />

## 适用场景 {#when-to-use}
- **行情分析**：呈现价格波动和市场情绪。
- **技术分析**：辨识锤子线、十字星、吞没形态等 K 线形态。
- **高低点追踪**：展示一个周期内价格波动的完整区间。

## 代码示例 {#code-example}

### XAML
```xml
<FinancialChart xmlns="https://github.com/avaloniaui" Name="CandlestickChartSample" Title="Stock Price (ACME)" Height="300">
    <FinancialChart.Series>
        <CandlestickSeries ItemsSource="{Binding CandlestickData}"
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

public ObservableCollection<FinancialPoint> CandlestickData { get; } = new(GenerateFinancialData(50));

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
| `UpFill` | `Close >= Open` 时蜡烛的填充画刷。 | `#4CAF50` |
| `DownFill` | `Close < Open` 时蜡烛的填充画刷。 | `#F44336` |
| `UpStroke` | `Close >= Open` 时蜡烛的轮廓画刷。 | `#4CAF50` |
| `DownStroke` | `Close < Open` 时蜡烛的轮廓画刷。 | `#F44336` |
| `CandleWidth` | 每根蜡烛的宽度，以可用槽位的比例表示。 | `0.8` |

## 另请参阅 {#see-also}

- [金融图表](/controls/data-display/charts/financial/financial-chart)
- [OHLC 图](/controls/data-display/charts/financial/ohlc-chart)
