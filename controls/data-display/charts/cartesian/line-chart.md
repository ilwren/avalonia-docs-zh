---
id: line-chart
title: 折线图
description: 在 X、Y 轴上用直线段连接各数据点，最适合呈现随时间或跨类别的变化趋势。
doc-type: reference
tags:
  - avalonia pro
---

import chartsCartesianLines from '/img/controls/charts/charts-cartesian-lines.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

折线图用 X、Y 轴呈现由直线段连接起来的数据点。要展现随时间或跨类别的趋势，它最为合适。

<Image light={chartsCartesianLines} maxWidth={400} position="center" cornerRadius="true" alt="Line chart connecting data points with straight segments to show monthly sales trends over time." />

## 适用场景 {#when-to-use}
- **时间序列**：呈现数据在连续时间区间上的变化。
- **趋势分析**：辨识上升、下降或反复波动的走势。
- **多系列对比**：用多条折线比较不同类别的走势。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="LineChart" Title="Line Chart" Height="250" ShowLegend="True">
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis />
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis />
                        </CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <LineSeries Title="2023" ItemsSource="{Binding LineSeries2023}" Stroke="DodgerBlue" StrokeThickness="2" MarkerSize="6" MarkerFill="DodgerBlue"  ShowMarkers="True"/>
                            <LineSeries Title="2024" ItemsSource="{Binding LineSeries2024}" Stroke="Orange" StrokeThickness="2" MarkerSize="6" MarkerFill="Orange"  ShowMarkers="True"/>
                        </CartesianChart.Series>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> LineSeries2023 { get; } = new()
{
    45, 52, 48, 60, 55, 70, 65, 75, 68, 80, 72, 85
};

public ObservableCollection<int> LineSeries2024 { get; } = new()
{
    50, 58, 55, 68, 62, 78, 72, 82, 75, 88, 80, 92
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例中显示的系列名称。 | `null` |
| `ItemsSource` | 要显示的数据项集合。 | `null` |
| `CategoryPath` | 指向 X 轴（类别）所用属性的路径。 | `null` |
| `ValuePath` | 指向 Y 轴（数值）所用属性的路径。 | `null` |
| `Stroke` | 折线的颜色。 | Theme-dependent |
| `StrokeThickness` | 折线的粗细。 | `2` |
| `ShowMarkers` | 是否显示各个数据点的标记。只有它为 `true` 时，标记的样式设置才看得出效果。 | `false` |
| `MarkerSize` | 标记的大小，单位为像素。 | `8` |
| `MarkerShape` | 标记的形状，比如 `Circle` 或 `Square`。 | `Circle` |
| `MarkerFill` | 填充标记所用的画刷。为 `null` 时，使用系列的线条颜色。 | `null` |
| `MarkerStroke` | 标记轮廓所用的画刷。 | `null` |
| `MarkerStrokeThickness` | 标记轮廓的粗细。为 `NaN` 时，使用系列的 `StrokeThickness`。 | `NaN` |
