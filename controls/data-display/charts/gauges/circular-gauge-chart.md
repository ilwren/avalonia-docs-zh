---
id: circular-gauge-chart
title: 圆形仪表图
description: 以车速表式的径向刻度呈现单个数值，适合实时监控和目标追踪类仪表板。
doc-type: reference
tags:
  - avalonia pro
---

import chartsGaugesCircular from '/img/controls/charts/charts-gauges-circular.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

圆形仪表图在径向刻度上呈现单个数值。对于高度概括的仪表板指标，这种「车速表」式的视觉形式直观好懂，堪称标配。

<Image light={chartsGaugesCircular} maxWidth={400} position="center" cornerRadius="true" alt="Circular gauge chart in a speedometer style with a needle pointing to the current value on a radial scale." />

## 适用场景 {#when-to-use}
- **实时监控**：展示 CPU、内存或网络占用。
- **目标追踪**：呈现距离目标还有多远（比如销售额指标）。
- **物理量模拟**：表示速度、压力等实际传感器的读数。

## 代码示例 {#code-example}

### XAML
```xml
<WrapPanel Orientation="Horizontal" HorizontalAlignment="Center">
    <CircularGaugeChart xmlns="https://github.com/avaloniaui" Value="72" Width="220" Height="220" Title="CPU" Margin="10" />
    <CircularGaugeChart Value="45" Width="220" Height="220" Title="Memory" Margin="10" />
    <CircularGaugeChart Value="88" Width="220" Height="220" Title="Disk" Margin="10" />
</WrapPanel>
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | 要显示的当前值。 | `0.0` |
| `MinValue` | 标尺的最小值。 | `0.0` |
| `MaxValue` | 标尺的最大值。 | `100.0` |
| `ShowValue` | 是否显示数值。 | `true` |
| `ValueFormat` | 所显示数值的格式字符串。 | `"{0:F0}"` |
| `StartAngle` | 仪表弧的起始角度，单位为度。 | `135.0` |
| `SweepAngle` | 仪表弧的扫过角度，单位为度。 | `270.0` |
| `TrackBrush` | 仪表轨道所用的画刷。 | `null` |
| `ValueBrush` | 已填充的数值弧所用的画刷。 | `null` |
| `NeedleBrush` | 指针所用的画刷。 | `null` |
| `TrackThickness` | 轨道弧的粗细。 | `10.0` |
| `MajorTickCount` | 主刻度线的数量。 | `5` |
| `TickPosition` | 刻度线相对轨道的位置。 | `Cross` |
| `LabelPosition` | 刻度标签绘制在哪里，`Inside` 或 `Outside`。 | `Inside` |

## 刻度位置 {#tick-position}

`TickPosition` 把刻度线画在轨道上。

| 值 | 说明 |
| :--- | :--- |
| `Cross` | 跨越整条轨道，从内缘往里 10 像素处一直到外缘。默认值。 |
| `Inside` | 自轨道内缘向内延伸。 |
| `Outside` | 自轨道外缘向外延伸。 |

尺寸紧凑的仪表会把数值读数缩进表盘内部。若文字实在放不下，则移到弧线未扫过的空白处。

## 另请参阅 {#see-also}

- [仪表图](/controls/data-display/charts/gauges/gauge-chart)
- [进度环形图](/controls/data-display/charts/gauges/progress-donut-chart)
