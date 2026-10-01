---
id: renko-chart
title: Renko chart
description: Uses fixed-size bricks to represent price movements, filtering out time and minor volatility to clarify trends and support/resistance levels.
doc-type: reference
tags:
  - avalonia pro
---

import chartsFinancialRenko from '/img/controls/charts/charts-financial-renko.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Renko charts are made of "bricks" that represent a fixed price movement. A new brick is only added if price moves by the specified brick size, filtering out time and minor volatility.

<Image light={chartsFinancialRenko} maxWidth={400} position="center" cornerRadius="true" alt="Renko chart displaying fixed-size green and red bricks representing price movements above a set threshold." />

## 适用场景 {#when-to-use}
- **Support and resistance**: Identifying clear levels where bricks frequently reverse.
- **Trend confirmation**: Spotting persistent bullish/bearish brick sequences.
- **Clean visualization**: Simplifying complex, noisy price data into uniform blocks.

## 代码示例 {#code-example}

### XAML
```xml
<RenkoChart xmlns="https://github.com/avaloniaui" Name="RenkoChartSample" Title="Price Movement" Height="300" BrickSize="5"
                                         ItemsSource="{Binding RenkoData}"
                                         ValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record RenkoPoint(double Value);

public ObservableCollection<RenkoPoint> RenkoData { get; } = new()
{
    new(100), new(105), new(103), new(108), new(115),
    new(112), new(118), new(120), new(115), new(122),
    new(118), new(114), new(110), new(105), new(100)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | The collection of price data. | `null` |
| `BrickSize` | The price movement required for a new brick. | `10.0` |
| `ValuePath` | Property name for the price value. | `null` |
| `UpBrush` | Color for up trends. | `Green` |
| `DownBrush` | Color for down trends. | `Red` |
