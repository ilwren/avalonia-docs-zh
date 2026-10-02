---
id: point-and-figure-chart
title: 点数图
description: 用一列列 X 和 O 表示价格变动，略去时间维度，专注于趋势反转。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFinancialPointandfigure from '/img/controls/charts/charts-financial-point-figure.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

点数图（Point and Figure，P&F）用一列列 X 和 O 分别表示价格的上涨和下跌。它滤掉了时间和细小的价格变化，只盯纯粹的价格走势与趋势反转。

<Image light={chartsFinancialPointandfigure} maxWidth={400} position="center" cornerRadius="true" alt="Point and figure chart with columns of X marks for rising prices and O marks for falling prices filtering out time." />

## 适用场景 {#when-to-use}
- **长期趋势**：呈现宏观经济或跨年度的市场变迁。
- **支撑/压力**：辨识清晰的供需区间。
- **价格目标**：用传统的点数图计数法推算目标价位。

## 代码示例 {#code-example}

### XAML
```xml
<FinancialChart xmlns="https://github.com/avaloniaui" Name="PointAndFigureChartSample" Title="Trend Analysis" Height="300">
    <FinancialChart.Series>
        <PointAndFigureSeries ItemsSource="{Binding PointAndFigureData}"
                                       HighPath="High"
                                       LowPath="Low"
                                       OpenPath="Open"
                                       ClosePath="Close"
                                       DatePath="Date"
                                       BoxSize="2.0"
                                       ReversalAmount="3" />
    </FinancialChart.Series>
</FinancialChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
using System;

public record FinancialPoint(DateTime Date, double Open, double High, double Low, double Close);

public ObservableCollection<FinancialPoint> PointAndFigureData { get; } = new(GenerateFinancialData(100));

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
| `ItemsSource` | 价格数据的集合。 | `null` |
| `DatePath` | 指向横轴所用日期或时间值的路径。取值可以是 `DateTime`、`DateTimeOffset`，或可解析的日期字符串。 | `null` |
| `HighPath` | 指向用于构建上涨列的最高价的路径。 | `null` |
| `LowPath` | 指向用于构建下跌列的最低价的路径。 | `null` |
| `ClosePath` | 指向收盘价的路径，用作起始价位和代表值。未设置时使用 `ValuePath`。 | `null` |
| `BoxSize` | 一个 X 或 O 所代表的价格变动幅度。必须是有限值且大于 `0`；过小的取值会在内部被调大，以免生成过多方格。 | `1.0` |
| `ReversalAmount` | 另起一列所需的方格数。小于 `1` 的取值一律按 `1` 处理。 | `3` |
| `XBrush` | X 标记所用的画刷。 | `Green` |
| `OBrush` | O 标记所用的画刷。 | `Red` |

点数图只采用 `High`、`Low`、`Close` 均为有限值的源数据点来绘制。
