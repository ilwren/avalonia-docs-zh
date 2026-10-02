---
id: hilo-chart
title: 高低图
description: 用竖线表示每个周期的最高价和最低价，不含开收盘价，专注呈现价格波动。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFinancialHilo from '/img/controls/charts/charts-financial-hilo.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

高低图只显示某一周期的最高价和最低价。略去开盘价和收盘价之后，它更专注于呈现整体的价格波动与区间。

<Image light={chartsFinancialHilo} maxWidth={400} position="center" cornerRadius="true" alt="Hilo chart showing daily price ranges as vertical lines connecting high and low values over a date range." />

## 适用场景 {#when-to-use}
- **波动分析**：突出最高价与最低价之间的跨度。
- **支撑与压力**：找出行情难以突破的关键价位。
- **简化的交易视图**：想要比 OHLC 图或 K 线图更清爽的替代方案时。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="HiloChartSample" Title="Price Range" Height="300">
    <CartesianChart.HorizontalAxis>
        <DateTimeAxis LabelFormat="MM/dd" Title="Date" />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis LabelFormat="N0" Title="Price" />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <HiloSeries ItemsSource="{Binding HiloData}"
                             HighPath="High" LowPath="Low"
                             CategoryPath="Date"
                             Stroke="#2196F3" StrokeThickness="3" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
using System;

public record FinancialPoint(DateTime Date, double Open, double High, double Low, double Close);

public ObservableCollection<FinancialPoint> HiloData { get; } = new(GenerateFinancialData(30));

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
| `HighPath` | 指向最高价属性的路径。 | `null` |
| `LowPath` | 指向最低价属性的路径。 | `null` |
| `CategoryPath` | 指向日期/类别属性的路径。 | `null` |
| `Stroke` | 竖向区间线的颜色。 | Theme-dependent |
| `StrokeThickness`| 价格线的粗细。 | `2` |
