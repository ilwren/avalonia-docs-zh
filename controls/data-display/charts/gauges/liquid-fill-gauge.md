---
id: liquid-fill-gauge
title: 液位仪表
description: 在圆形内以动态液面表示百分比，适合展示填充量或容量指标的主题化仪表板。
doc-type: reference
tags:
  - avalonia pro
---

import chartsGaugesLiquid from '/img/controls/charts/charts-gauges-liquid.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

液位仪表是一种带装饰性的圆形仪表，用停在某一高度的「液体」表示百分比。它常用来呈现储罐液位、用水量，或富有主题感的进度。

<Image light={chartsGaugesLiquid} maxWidth={400} position="center" cornerRadius="true" alt="Liquid fill gauge showing a circular container filled with animated liquid to represent a percentage value." />

## 适用场景 {#when-to-use}
- **主题化仪表板**：呈现募资进度、容量占用这类「装满」概念。
- **环保类应用**：展示水位或液体容器的状态。
- **吸引眼球的界面**：为现代应用添一个活泼的动态指标。

## 代码示例 {#code-example}

### XAML
```xml
<WrapPanel Orientation="Horizontal" HorizontalAlignment="Center">
    <LiquidFillGauge xmlns="https://github.com/avaloniaui" Value="35" Width="140" Height="180" Title="CPU Usage" Margin="15" />
    <LiquidFillGauge Value="68" Width="140" Height="180" Title="Memory" Margin="15" />
    <LiquidFillGauge Value="85" Width="140" Height="180" Title="Storage" Margin="15" />
</WrapPanel>
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | 当前值。 | `50.0` |
| `MinValue` | 最小值。 | `0.0` |
| `MaxValue` | 最大值。 | `100.0` |
| `ValueBrush` | 液体部分所用的画刷。 | 渐变 / 随主题而定 |
| `TrackBrush` | 空白背景区域所用的画刷。 | `null` |
| `WaveAmplitude` | 波浪效果的振幅。 | `5.0` |
| `WaveFrequency` | 波浪效果的频率。 | `2.0` |
| `ShowPercentage` | 是否显示百分比文字。 | `true` |
| `IsWaveAnimationEnabled` | 是否让波浪动起来。 | `true` |

## 另请参阅 {#see-also}

- [仪表图](/controls/data-display/charts/gauges/gauge-chart)
- [进度环形图](/controls/data-display/charts/gauges/progress-donut-chart)
