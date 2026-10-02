---
id: spline-area-chart
title: 样条面积图
description: 在平滑的样条曲线下方填充区域，兼具样条图的流畅线条和面积图对体量的强调。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

样条面积图在平滑插值曲线的下方填充出一片区域。它把样条曲线的流畅美感与面积填充对体量的强调结合起来，让趋势格外醒目。

## 适用场景 {#when-to-use}
- **平滑趋势**：数据连续变化、用平滑插值更能体现其走势时。
- **强调体量**：用曲线下方的填充区域凸显数值的量级。
- **时间序列**：呈现随时间缓缓变化的数据，比如营收或流量。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Website Traffic" Height="250">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <SplineAreaSeries Title="Visitors"
                                   ItemsSource="{Binding SplineAreaSeriesData}"
                                   FillOpacity="0.4"
                                   SplineTension="0.3" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public ObservableCollection<int> SplineAreaSeriesData { get; } = new()
{
    1200, 1400, 1100, 1600, 1800, 1500, 2000
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例中显示的系列名称。 | `null` |
| `ItemsSource` | 要显示的数据项集合。 | `null` |
| `CategoryPath` | 指向 X 轴所用属性的路径。 | `null` |
| `ValuePath` | 指向 Y 轴所用属性的路径。 | `null` |
| `Fill` | 填充区域所用的颜色/画刷。 | Theme-dependent |
| `Stroke` | 样条曲线轮廓的颜色。 | `Transparent` |
| `FillOpacity` | 填充区域的不透明度（0.0 到 1.0）。 | `0.5` |
| `SplineTension` | 样条曲线的张力（0.0 到 1.0）。值越小曲线转折越锐利，值越大则越平滑。 | `0.25` |

## 另请参阅 {#see-also}

- [面积图](/controls/data-display/charts/cartesian/area-chart)
- [样条图](/controls/data-display/charts/cartesian/spline-chart)
- [折线图](/controls/data-display/charts/cartesian/line-chart)
