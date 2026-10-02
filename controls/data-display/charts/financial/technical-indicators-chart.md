---
id: technical-indicators-chart
title: 图表的技术指标
description: 在笛卡尔图表上叠加 SMA、EMA、WMA、布林带等技术指标，用以分析金融或时间序列数据的趋势与波动。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

技术指标是加在 `CartesianChart` 上的分析性叠加层，帮助辨识数据中的趋势、动能和波动。它们从目标系列算出派生数值，并把结果直接画在图上。指标要加进 `CartesianChart` 的 `TechnicalIndicators` 集合中。

指标沿用目标系列的坐标轴上下文，包括连续横轴，以及目标系列使用 `YAxisPosition="Secondary"` 时的次 Y 轴刻度。

## 适用场景 {#when-to-use}
- **趋势分析**：用简单移动平均（SMA）、指数移动平均（EMA）或加权移动平均（WMA）平滑嘈杂的价格或传感器数据。
- **波动评估**：用布林带呈现移动平均线上下的标准差通道。
- **金融制图**：为 K 线图或 OHLC 图加上标准的技术分析叠加层。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Stock Analysis" Height="400">
    <CartesianChart.Series>
        <CandlestickSeries x:Name="PriceSeries"
                                     ItemsSource="{Binding StockData}"
                                     DatePath="Date"
                                     OpenPath="Open" HighPath="High"
                                     LowPath="Low" ClosePath="Close" />
    </CartesianChart.Series>
    <CartesianChart.TechnicalIndicators>
        <SMAIndicator TargetSeries="{Binding #PriceSeries}"
                               Period="20" Stroke="Orange" StrokeThickness="2" />
        <BollingerBandsIndicator TargetSeries="{Binding #PriceSeries}"
                                          Period="20" StandardDeviations="2"
                                          Stroke="Blue" StrokeThickness="1"
                                          UpperBandStroke="Gray" LowerBandStroke="Gray">
            <BollingerBandsIndicator.BandFill>
                <SolidColorBrush Color="#33808080" />
            </BollingerBandsIndicator.BandFill>
        </BollingerBandsIndicator>
    </CartesianChart.TechnicalIndicators>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record StockPoint(string Date, double Open, double High, double Low, double Close);

public ObservableCollection<StockPoint> StockData { get; } = new()
{
    new("Jan", 100, 110, 95, 105),
    new("Feb", 105, 115, 100, 112),
    new("Mar", 112, 120, 108, 118),
    // ...
};
```

## 常用属性（`ChartTechnicalIndicator`） {#common-properties-charttechnicalindicator}

下列属性为所有技术指标类型所共有。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `TargetSeries` | 计算该指标所依据的 `CartesianSeries`。 | `null` |
| `IsVisible` | 该指标是否可见。 | `true` |
| `Stroke` | 指标主线所用的画刷。 | `Blue` |
| `StrokeThickness` | 指标线的粗细。 | `2.0` |
| `StrokeDashStyle` | 指标线的虚线样式，类型为 `DashStyle?`。 | `null` |
| `StrokeLineCap` | 指标线的线端样式。 | `Round` |
| `StrokeLineJoin` | 指标线的拐角连接样式。 | `Round` |
| `Title` | 在图表图例和工具提示中显示的名称。 | 因指标而异 |

## 常用属性（`SMAIndicator`） {#common-properties-smaindicator}

简单移动平均（SMA）计算前 *n* 个数据点的算术平均值，是最基础的平滑手法。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Period` | 移动平均窗口所取的数据点个数。 | `14` |
| `Title` | 图例与工具提示的标题。 | `"SMA"` |

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Height="250">
    <CartesianChart.Series>
        <LineSeries x:Name="PriceSeries"
                           ItemsSource="{Binding StockData}"
                           ValuePath="Close" />
    </CartesianChart.Series>
    <CartesianChart.TechnicalIndicators>
        <SMAIndicator TargetSeries="{Binding #PriceSeries}"
                             Period="20" Stroke="Orange" StrokeThickness="2" />
    </CartesianChart.TechnicalIndicators>
</CartesianChart>
```

## 常用属性（`EMAIndicator`） {#common-properties-emaindicator}

指数移动平均（EMA）给较新的数据点更高的权重，因此比 SMA 对新信息反应更灵敏。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Period` | 计算 EMA 所取的数据点个数。 | `14` |
| `Title` | 图例与工具提示的标题。 | `"EMA"` |

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Height="250">
    <CartesianChart.Series>
        <LineSeries x:Name="PriceSeries"
                           ItemsSource="{Binding StockData}"
                           ValuePath="Close" />
    </CartesianChart.Series>
    <CartesianChart.TechnicalIndicators>
        <EMAIndicator TargetSeries="{Binding #PriceSeries}"
                             Period="12" Stroke="Green" StrokeThickness="2" />
    </CartesianChart.TechnicalIndicators>
</CartesianChart>
```

## 常用属性（`WMAIndicator`） {#common-properties-wmaindicator}

加权移动平均（WMA）按线性递增的方式给数据点分配权重，最新的数据点权重最高。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Period` | 计算 WMA 所取的数据点个数。 | `14` |
| `Title` | 图例与工具提示的标题。 | `"WMA"` |

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Height="250">
    <CartesianChart.Series>
        <LineSeries x:Name="PriceSeries"
                           ItemsSource="{Binding StockData}"
                           ValuePath="Close" />
    </CartesianChart.Series>
    <CartesianChart.TechnicalIndicators>
        <WMAIndicator TargetSeries="{Binding #PriceSeries}"
                             Period="14" Stroke="Purple" StrokeThickness="2" />
    </CartesianChart.TechnicalIndicators>
</CartesianChart>
```

## 常用属性（`BollingerBandsIndicator`） {#common-properties-bollingerbandsindicator}

布林带由一条简单移动平均（中轨）和上下两条标准差通道组成，用于衡量波动性、辨识超买或超卖状态。

在图表图例中显示时，`BollingerBandsIndicator` 会生成一个代表中轨 SMA 的线条项，以及一个代表上下轨的通道项。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Period` | 计算移动平均所取的数据点个数。 | `20` |
| `StandardDeviations` | 上下轨所取的标准差倍数。 | `2.0` |
| `UpperBandStroke` | 上轨线所用的画刷。 | `Gray` |
| `LowerBandStroke` | 下轨线所用的画刷。 | `Gray` |
| `BandFill` | 填充上下轨之间区域所用的画刷。 | Semi-transparent `Gray` |
| `Title` | 图例与工具提示的标题。 | `"Bollinger Bands"` |

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Height="250">
    <CartesianChart.Series>
        <LineSeries x:Name="PriceSeries"
                           ItemsSource="{Binding StockData}"
                           ValuePath="Close" />
    </CartesianChart.Series>
    <CartesianChart.TechnicalIndicators>
        <BollingerBandsIndicator TargetSeries="{Binding #PriceSeries}"
                                        Period="20" StandardDeviations="2"
                                        Stroke="Blue" StrokeThickness="1"
                                        UpperBandStroke="LightGray"
                                        LowerBandStroke="LightGray">
            <BollingerBandsIndicator.BandFill>
                <SolidColorBrush Color="#20808080" />
            </BollingerBandsIndicator.BandFill>
        </BollingerBandsIndicator>
    </CartesianChart.TechnicalIndicators>
</CartesianChart>
```

## 另请参阅 {#see-also}

- [趋势线图](/controls/data-display/charts/shared-elements/trendline-chart)
- [折线图](/controls/data-display/charts/cartesian/line-chart)
- [坐标轴定制](/controls/data-display/charts/shared-elements/axis-customization-chart)
