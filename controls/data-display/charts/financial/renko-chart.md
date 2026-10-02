---
id: renko-chart
title: 砖形图
description: 用大小固定的砖块表示价格变动，滤去时间和细微波动，让趋势与支撑/压力位更清晰。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFinancialRenko from '/img/controls/charts/charts-financial-renko.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

砖形图由一块块代表固定价格变动的「砖」组成。只有当价格变动达到指定的砖块大小时才会添一块新砖，时间和细微波动因此被滤掉。

<Image light={chartsFinancialRenko} maxWidth={400} position="center" cornerRadius="true" alt="Renko chart displaying fixed-size green and red bricks representing price movements above a set threshold." />

## 适用场景 {#when-to-use}
- **支撑与压力**：找出砖块频繁反转的关键价位。
- **趋势确认**：发现持续的多头/空头砖块序列。
- **清爽的呈现**：把杂乱嘈杂的价格数据化简为规整的方块。

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
| `ItemsSource` | 价格数据的集合。 | `null` |
| `BrickSize` | 新增一块砖所需的价格变动幅度。 | `10.0` |
| `ValuePath` | 表示价格数值的属性名。 | `null` |
| `UpBrush` | 上涨趋势的颜色。 | `Green` |
| `DownBrush` | 下跌趋势的颜色。 | `Red` |
