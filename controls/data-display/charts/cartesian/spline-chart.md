---
id: spline-chart
title: 样条图
description: 与折线图类似，但用平滑的多项式曲线连接数据点，让趋势看上去更自然流畅。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianSpline from '/img/controls/charts/charts-cartesian-spline.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

样条图与折线图相仿，只是改用平滑的多项式曲线连接数据点，让数据趋势显得更「自然」。

<Image light={chartsCartesianSpline} maxWidth={400} position="center" cornerRadius="true" alt="Spline chart with smooth curved lines connecting temperature data points across time intervals." />

## 适用场景 {#when-to-use}
- **平滑数据**：呈现连续而平缓变化的数据时（比如气温）。
- **美观考量**：相比生硬的折角，更想要圆润专业的观感时。
- **趋势平滑**：帮助看清总体走势，不被折线段的锐利打断。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="SplineChart" Title="Spline Chart" Height="250">
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis />
                        </CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <SplineSeries Title="Temperature" ItemsSource="{Binding SplineSeriesData}" Stroke="Crimson" StrokeThickness="3" MarkerSize="6" MarkerFill="White"  ShowMarkers="True"/>
                        </CartesianChart.Series>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> SplineSeriesData { get; } = new()
{
    15, 18, 22, 28, 32, 35, 33, 28, 22, 17, 12, 10
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 系列名称。 | `null` |
| `ItemsSource` | 数据项的集合。 | `null` |
| `Stroke` | 样条曲线的颜色。 | Theme-dependent |
| `StrokeThickness` | 曲线的粗细。 | `2` |
| `ShowMarkers` | 是否在数据点处显示标记。只有它为 `true` 时，标记的样式设置才看得出效果。 | `false` |
| `MarkerSize` | 标记的大小，单位为像素。 | `6` |
| `MarkerShape` | 标记的形状，比如 `Circle` 或 `Square`。 | `Circle` |
| `MarkerFill` | 填充标记所用的画刷。 | `null` |
| `MarkerStroke` | 标记轮廓所用的画刷。 | `null` |
| `MarkerStrokeThickness` | 标记轮廓的粗细。为 `NaN` 时，使用系列的 `StrokeThickness`。 | `NaN` |
| `SplineTension` | 控制曲线的平滑程度。 | `0.25` |
