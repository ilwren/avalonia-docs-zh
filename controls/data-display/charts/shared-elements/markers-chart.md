---
id: markers-chart
title: 标记
description: 在系列的每个数据点处绘制的符号，便于定位精确坐标，支持多种形状以及自定义大小和颜色。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFeaturesMarkers from '/img/controls/charts/charts-markers.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

标记是绘制在系列各数据点处的符号。它能帮用户定位到数据点的精确坐标，在折线图、样条图这类线条可能很密集的图表上尤其有用。

对 `LineSeries`、`SplineSeries`、`StepLineSeries` 这些笛卡尔折线家族的系列来说，标记需要显式开启。只有先设置 `ShowMarkers="True"`，`MarkerSize`、`MarkerFill`、`MarkerStroke` 等标记样式属性才看得出效果。

<Image light={chartsFeaturesMarkers} maxWidth={400} position="center" cornerRadius="true" alt="Line chart with markers of different shapes drawn at each data point to highlight exact coordinate positions." />

## 适用场景 {#when-to-use}

- **离散数据**：强调折线代表的是一个个实测点。
- **稀疏图表**：让数据点更容易点中，便于弹出工具提示或进行选择。
- **区分类别**：用不同形状（圆形、方形、菱形）区分各个系列。

## 代码示例 {#code-example}

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="AllMarkersChart" Title="Marker Shape Comparison" Height="320" ShowLegend="True" LegendPosition="Bottom" HorizontalAlignment="Stretch">
                        <CartesianChart.Series>
                            <LineSeries Title="Circle" ItemsSource="{Binding CircleMarkerData}"
                                               MarkerShape="Circle" MarkerSize="10"
                                               Stroke="DodgerBlue" MarkerFill="DodgerBlue" StrokeThickness="2"  ShowMarkers="True"/>
                            <LineSeries Title="Square" ItemsSource="{Binding SquareMarkerData}"
                                               MarkerShape="Square" MarkerSize="10"
                                               Stroke="Green" MarkerFill="Green" StrokeThickness="2"  ShowMarkers="True"/>
                            <LineSeries Title="Diamond" ItemsSource="{Binding DiamondMarkerData}"
                                               MarkerShape="Diamond" MarkerSize="12"
                                               Stroke="Orange" MarkerFill="Orange" StrokeThickness="2"  ShowMarkers="True"/>
                            <LineSeries Title="Triangle" ItemsSource="{Binding TriangleMarkerData}"
                                               MarkerShape="Triangle" MarkerSize="10"
                                               Stroke="Purple" MarkerFill="Purple" StrokeThickness="2"  ShowMarkers="True"/>
                            <LineSeries Title="Pentagon" ItemsSource="{Binding PentagonMarkerData}"
                                               MarkerShape="Pentagon" MarkerSize="10"
                                               Stroke="Crimson" MarkerFill="Crimson" StrokeThickness="2"  ShowMarkers="True"/>
                        </CartesianChart.Series>
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis />
                        </CartesianChart.VerticalAxis>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
public ObservableCollection<int> CircleMarkerData { get; } = new() { 20, 35, 25, 40, 30 };
public ObservableCollection<int> SquareMarkerData { get; } = new() { 25, 40, 30, 45, 35 };
public ObservableCollection<int> DiamondMarkerData { get; } = new() { 30, 45, 35, 50, 40 };
public ObservableCollection<int> TriangleMarkerData { get; } = new() { 15, 30, 20, 35, 25 };
public ObservableCollection<int> PentagonMarkerData { get; } = new() { 35, 50, 40, 55, 45 };
```

## 公共属性（作用于 Series） {#common-properties-applied-to-series}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ShowMarkers` | 数据点符号的总开关。折线家族系列默认为 `false`，部分以数据点为主的系列则把它改成 `true`。 | Series-dependent |
| `MarkerSize` | 标记的直径，单位为像素。 | Series-dependent |
| `MarkerShape` | `Circle`, `Square`, `Rectangle`, `Diamond`, `Triangle`, `InvertedTriangle`, `Cross`, `Pentagon`, `VerticalLine`, or `HorizontalLine`. | `Circle` |
| `MarkerFill` | 填充标记内部所用的画刷。 | 系列颜色 |
| `MarkerStroke` | 标记轮廓所用的画刷。 | `null` |
| `MarkerStrokeThickness` | 标记轮廓的粗细。为 `NaN` 时，使用系列的 `StrokeThickness`。 | `NaN` |
