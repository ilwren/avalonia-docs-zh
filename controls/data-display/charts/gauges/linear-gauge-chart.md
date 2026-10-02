---
id: linear-gauge-chart
title: 线性仪表图
description: 沿横向或纵向条带呈现数值，便于比较各项指标或展示进度。
doc-type: reference
tags:
  - avalonia pro
---

import chartsGaugesLinear from '/img/controls/charts/charts-gauges-linear-1.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

线性仪表图沿横向或纵向条带呈现数值。要并排比较多项指标，或以省地方的线性形式展示进度，它很合适。

<Image light={chartsGaugesLinear} maxWidth={400} position="center" cornerRadius="true" alt="Linear gauge chart with a horizontal progress bar and scale ticks showing the current value along a numeric range." />

## 适用场景 {#when-to-use}
- **绩效条**：在紧凑的仪表板中比较多项指标。
- **容量指示**：展示存储空间、音量或储罐容量。
- **进度追踪**：在一条直线上呈现一连串目标的达成情况。

## 代码示例 {#code-example}

### XAML
```xml
<StackPanel Spacing="15" Margin="10">
    <LinearGaugeChart xmlns="https://github.com/avaloniaui" Title="Temperature" Value="72" MinValue="0" MaxValue="100" Height="60"
                             NeedleBrush="#F44336">
        <LinearGaugeChart.ValueBrush>
            <LinearGradientBrush StartPoint="0%,0%" EndPoint="100%,0%">
                <GradientStop Offset="0" Color="#4CAF50" />
                <GradientStop Offset="0.5" Color="#FFEB3B" />
                <GradientStop Offset="1" Color="#F44336" />
            </LinearGradientBrush>
        </LinearGaugeChart.ValueBrush>
    </LinearGaugeChart>

    <LinearGaugeChart Title="Humidity" Value="45" MinValue="0" MaxValue="100" Height="60"
                             NeedleBrush="#00BCD4">
        <LinearGaugeChart.ValueBrush>
            <LinearGradientBrush StartPoint="0%,0%" EndPoint="100%,0%">
                <GradientStop Offset="0" Color="#2196F3" />
                <GradientStop Offset="1" Color="#00BCD4" />
            </LinearGradientBrush>
        </LinearGaugeChart.ValueBrush>
    </LinearGaugeChart>

    <LinearGaugeChart Title="Pressure" Value="88" MinValue="0" MaxValue="100" Height="60"
                             NeedleBrush="#E91E63">
        <LinearGaugeChart.ValueBrush>
            <LinearGradientBrush StartPoint="0%,0%" EndPoint="100%,0%">
                <GradientStop Offset="0" Color="#9C27B0" />
                <GradientStop Offset="1" Color="#E91E63" />
            </LinearGradientBrush>
        </LinearGaugeChart.ValueBrush>
    </LinearGaugeChart>
</StackPanel>
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | 要显示的当前值。 | `50.0` |
| `MinValue` | 标尺的最小值。 | `0.0` |
| `MaxValue` | 标尺的最大值。 | `100.0` |
| `Orientation` | 仪表的方向，`Horizontal` 或 `Vertical`。 | `Horizontal` |
| `ShowScale` | 是否显示刻度。 | `true` |
| `TrackBrush` | 轨道的颜色。 | 采用主题默认值。 |
| `NeedleBrush` | 指针的颜色。 | 采用主题默认值。 |
| `ValueBrush` | 数值的颜色。 | 采用主题默认值。 |
| `TrackThickness` | 轨道的粗细。 | `20.0` |
| `Ranges` | 可选的彩色区间集合，绘制在指示器后面。 | `null` |
| `ShowMajorTicks` | 是否显示主刻度。 | `false` |
| `ShowMinorTicks` | 是否显示次刻度。 | `false` |
| `MajorTickInterval` | 主刻度之间的间隔。 | `20.0` |
| `MinorTickCount` | 两个主刻度之间次刻度的个数。 | `4` |
| `TickPosition` | 刻度线相对轨道画在哪里。 | `Above` |
| `LabelPosition` | 刻度标签相对轨道画在哪里。 | `Below` |

## 刻度位置 {#tick-position}

`TickPosition` 把刻度线画在轨道两侧。主刻度长 10 像素，次刻度长 5 像素。

| 值 | 说明 |
| :--- | :--- |
| `Above` | 横向轨道的上方，或纵向轨道的左侧。默认值。 |
| `Below` | 横向轨道的下方，或纵向轨道的右侧。 |
| `Cross` | 在轨道上居中。 |

版面紧张时，仪表会先舍弃刻度所占的空间，再舍弃指示器的空间，最后才丢掉刻度标签，并一路把轨道收细。
