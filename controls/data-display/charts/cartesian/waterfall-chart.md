---
id: waterfall-chart
title: 瀑布图
description: 随着数值的增减展示累计结果，适合呈现一连串正负变化如何改变初始值。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianWaterfall from '/img/controls/charts/charts-cartesian-waterfall.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

瀑布图随着数值的增减展示累计结果。要弄清一个初始值如何被一连串中间的正负数值所影响，用它正合适。

<Image light={chartsCartesianWaterfall} maxWidth={400} position="center" cornerRadius="true" alt="Waterfall chart with floating bars showing sequential positive and negative changes to a running total." />

## 适用场景 {#when-to-use}
- **财务分析**：呈现一段时期内的损益表。
- **库存追踪**：展示库存水平如何随着入库和出库而变化。
- **流程步骤**：刻画一连串变量的累积效应。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="WaterfallChartSample" Title="Quarterly P&amp;L Analysis" Height="300" ShowLegend="False">
                        <CartesianChart.HorizontalAxis><CategoryAxis /></CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis><NumericalAxis /></CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <WaterfallSeries Title="P&amp;L"
                                                      ItemsSource="{Binding WaterfallData}"
                                                      CategoryPath="Category" ValuePath="Value"
                                                      TotalCategory="Net Income" />
                        </CartesianChart.Series>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record WaterfallFinancialPoint(string Category, double Value);

public ObservableCollection<WaterfallFinancialPoint> WaterfallData { get; } = new()
{
    new("Revenue", 500.0),
    new("COGS", -200.0),
    new("Marketing", -50.0),
    new("R&D", -80.0),
    new("Admin", -40.0),
    new("Net Income", 130.0)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 各次变化的集合。 | `null` |
| `CategoryPath` | 指向标签/类别的路径。 | `null` |
| `ValuePath` | 指向变化值（正或负）的路径。 | `null` |
| `PositiveBrush` | 正向变化所用的画刷。 | Theme-dependent |
| `NegativeBrush` | 负向变化所用的画刷。 | Theme-dependent |
| `TotalBrush` | 总计（末根）条形所用的画刷。 | Theme-dependent |
| `BarWidth` | 每根条形的宽度，以可用类别槽位的比例表示。 | `0.7` |
| `ShowConnectorLines` | 是否在相邻条形之间绘制连接线。 | `true` |
| `TotalCategory` | 表示最终总计的那个类别名称。 | `null` |
