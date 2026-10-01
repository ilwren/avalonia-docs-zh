---
id: heikin-ashi-chart
title: 平均 K 线图
description: 改良版 K 线图，用取平均后的 OHLC 值过滤市场噪声，相比标准 K 线能呈现更平滑的趋势方向。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFinancialHeikinashi from '/img/controls/charts/charts-financial-heikin.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

平均 K 线图（Heikin-Ashi）是日本蜡烛图的一种变体。它用改良公式计算开、高、低、收四个价格，以滤除市场噪声，呈现更为平滑的趋势方向。

<Image light={chartsFinancialHeikinashi} maxWidth={400} position="center" cornerRadius="true" alt="Heikin-Ashi chart with smoothed candlesticks using averaged OHLC values to show market trend direction." />

## 适用场景 {#when-to-use}
- **辨识趋势**：在波动更小的图上找出行情趋势的起点和终点。
- **波段交易**：在震荡行情中辨识回调与反转。
- **长期分析**：抹平日间价格起伏，看清大局。

## 代码示例 {#code-example}

### XAML
```xml
<HeikinAshiChart xmlns="https://github.com/avaloniaui" Name="HeikinAshiChartSample" Title="Smoothed Price Trend" Height="300"
                                              ItemsSource="{Binding HeikinAshiData}"
                                              HighPath="High" LowPath="Low"
                                              OpenPath="Open" ClosePath="Close"
                                              DatePath="Date" />
```

### 数据模型（C#） {#data-model-c}
```csharp
using System;

public record FinancialPoint(DateTime Date, double Open, double High, double Low, double Close);

public ObservableCollection<FinancialPoint> HeikinAshiData { get; } = new(GenerateFinancialData(40));

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
| `ItemsSource` | 价格数据的数据源。 | `null` |
| `OpenPath` | 开盘价的路径。 | `null` |
| `ClosePath` | 收盘价的路径。 | `null` |
| `HighPath` | 最高价的路径。 | `null` |
| `LowPath` | 最低价的路径。 | `null` |
| `DatePath` | 每一项所对应日期或时间值的路径。 | `null` |
| `BullishBrush` | 阳线的颜色。 | `0x4C, 0xAF, 0x50` (Green) |
| `BearishBrush` | 阴线的颜色。 | `0xF4, 0x43, 0x36` (Red) |
| `CandleWidth` | 蜡烛宽度，以可用槽位宽度的比例表示，取值从 `0` 到 `1`。 | `0.7` |
