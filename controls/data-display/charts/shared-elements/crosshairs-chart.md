---
id: crosshairs-chart
title: 十字准线
description: 随光标在图表上移动的交互式参考线，让数据点与坐标轴标签精确对齐，便于读取精确数值。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFeaturesCrosshairs from '/img/controls/charts/charts-custom-crosshairs.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

十字准线是随用户光标移动的交互式参考线。在高精度图表中，它能帮用户把数据点与坐标轴标签对齐。

十字准线标签沿用坐标轴已配置的格式。连续横轴、对数轴、刻度断裂和次纵轴都会如实反映在所显示的坐标标签中。

<Image light={chartsFeaturesCrosshairs} maxWidth={400} position="center" cornerRadius="true" alt="Line chart with interactive crosshair guide lines following the cursor to align data points with axis coordinates." />

## 适用场景 {#when-to-use}
- **金融图表**：在 K 线图上精确定位某个价格和时点。
- **工程数据**：在数据密集的折线图上读取数值。
- **科研图表**：把某个波峰或波谷与坐标对齐。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="CustomCrosshairChart" Height="300"
                                             CrosshairMode="Both"
                                             ShowCrosshairLabels="True"
                                             CrosshairStroke="DodgerBlue"
                                             CrosshairStrokeThickness="3"
                                             CrosshairLabelBackground="DodgerBlue"
                                             CrosshairLabelForeground="White"
                                             CrosshairLabelFontSize="14">
                        <CartesianChart.CrosshairDashStyle>
                            <DashStyle Dashes="10, 5" Offset="0" />
                        </CartesianChart.CrosshairDashStyle>
                        <CartesianChart.Series>
                            <LineSeries Title="Series 2" ItemsSource="{Binding CrosshairData}"
                                                 Stroke="DodgerBlue" StrokeThickness="2"
                                                 MarkerSize="6" MarkerFill="DodgerBlue"
                                                 MarkerShape="Square"  ShowMarkers="True"/>
                        </CartesianChart.Series>
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis Title="Category" />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis Title="Value" />
                        </CartesianChart.VerticalAxis>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<double> CrosshairData { get; } = new()
{
    18.5, 21.2, 24.8, 22.1, 19.7, 23.4, 26.1
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `CrosshairMode` | `None`, `Vertical`, `Horizontal`, or `Both`. | `None` |
| `ShowCrosshairLabels` | 开关坐标轴上的数值标签。 | `true` |
| `CrosshairStroke` | 参考线所用的画刷。为 `null` 时，使用暗灰色画刷。 | `null` |
| `CrosshairStrokeThickness` | 参考线的粗细。 | `1.0` |
| `CrosshairDashStyle` | 参考线的虚线样式。为 `null` 时，图表采用 `4,4` 虚线样式。 | `null` |
| `CrosshairLabelBackground` | 十字准线标签背后所用的画刷。为 `null` 时，使用半透明的深色画刷。 | `null` |
| `CrosshairLabelForeground` | 十字准线标签文字所用的画刷。为 `null` 时，使用白色。 | `null` |
| `CrosshairLabelFontSize` | 十字准线标签的字号。 | `10.0` |
