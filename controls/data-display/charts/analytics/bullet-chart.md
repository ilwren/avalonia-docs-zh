---
id: bullet-chart
title: 子弹图
description: 在紧凑的横向或纵向标尺上，把单项绩效指标与目标值以及几段定性区间放在一起比较。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

子弹图在紧凑的版面里，把一个主值与目标值以及一段或多段定性区间作对比。

## 适用场景 {#when-to-use}

- **追踪目标**：在仪表板卡片中把实际值与目标值作对比。
- **紧凑摘要**：只有一个指标和一个目标值时，用它取代整张条形图。
- **阈值区间**：在主值背后标出「欠佳」「尚可」「良好」几段区间。

## 代码示例 {#code-example}

### XAML

```xml
<BulletChart xmlns="https://github.com/avaloniaui" Title="Revenue attainment"
                      Width="320"
                      Height="80"
                      Value="{Binding ActualRevenue}"
                      Target="{Binding RevenueTarget}"
                      Ranges="{Binding RevenueBands}" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public double ActualRevenue { get; set; } = 72;
public double RevenueTarget { get; set; } = 85;
public double[] RevenueBands { get; } = [30, 60, 90, 100];
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Value` | 条形所表示的主值。 | `75.0` |
| `Target` | 目标标记的值。 | `85.0` |
| `MinValue` | 标尺的最小值。 | `0.0` |
| `MaxValue` | 标尺的最大值。 | `100.0` |
| `Ranges` | 可选的定性区间边界集合。 | `null` |
| `Orientation` | 图表的方向，`Horizontal` 或 `Vertical`。 | `Horizontal` |
| `ValueBrush` | 主值条形所用的画刷。 | `null` |
| `TargetBrush` | 目标标记所用的画刷。 | `null` |

## 另请参阅 {#see-also}

- [KPI 卡片](/controls/data-display/charts/analytics/kpi-card)
- [线性仪表图](/controls/data-display/charts/gauges/linear-gauge-chart)
