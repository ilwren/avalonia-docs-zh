---
id: gauge-chart
title: 仪表图
description: 在表盘式仪表上呈现单个数值，带弧形填充和可选的指针。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

仪表图在表盘式弧线上呈现单个数值，并可配指针和格式化的数值文字。

## 适用场景 {#when-to-use}

- **运行仪表板**：用紧凑的表盘展示利用率、负载或健康度。
- **阈值监控**：相比历史走势，更强调当前这一个读数。
- **状态卡片**：以醒目的视觉分量呈现单项指标。

## 代码示例 {#code-example}

### XAML

```xml
<GaugeChart xmlns="https://github.com/avaloniaui" Title="CPU load"
                     Width="220"
                     Height="160"
                     Value="{Binding CpuLoad}"
                     MaxValue="100"
                     ShowNeedle="True" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public double CpuLoad { get; set; } = 67;
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | 仪表所显示的当前值。 | `50.0` |
| `MinValue` | 标尺的最小值。 | `0.0` |
| `MaxValue` | 标尺的最大值。 | `100.0` |
| `ValueBrush` | 数值弧所用的画刷。 | `null` |
| `TrackBrush` | 背景轨道所用的画刷。 | `null` |
| `NeedleBrush` | 指针所用的画刷。 | `null` |
| `ShowNeedle` | 是否绘制指针。 | `true` |
| `StartAngle` | 仪表弧的起始角度，单位为度。 | `135.0` |
| `SweepAngle` | 仪表弧的扫过角度，单位为度。 | `270.0` |
| `TrackThickness` | 轨道弧的粗细。 | `20.0` |
| `ShowValue` | 是否显示格式化后的数值文字。 | `true` |
| `ValueFormat` | Format string used for the value text. | `"{0:F0}"` |

## 另请参阅 {#see-also}

- [Circular gauge](/controls/data-display/charts/gauges/circular-gauge-chart)
- [进度环形图](/controls/data-display/charts/gauges/progress-donut-chart)
