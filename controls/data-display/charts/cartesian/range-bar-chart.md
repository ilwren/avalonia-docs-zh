---
id: range-bar-chart
title: 区间条形图
description: 为每个类别绘制一根从低到高的浮动条形，最适合呈现气温范围、价格区间或任务工期。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

区间条形图为每个类别绘制一根浮动的矩形条，从低值一直延伸到高值。它适合展现数据的范围、区间或带状分布，而不是单个数值。

## 适用场景 {#when-to-use}
- **气温范围**：按天或按月展示每日最低/最高温区间。
- **价格区间**：呈现金融数据的价格范围或置信区间。
- **任务工期**：表示排期或时间线数据中从开始到结束的区间。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Weekly Temperature Range" Height="250">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <RangeBarSeries Title="Temperature"
                                 ItemsSource="{Binding TemperatureData}"
                                 CategoryPath="Day"
                                 LowPath="Min"
                                 HighPath="Max"
                                 BarWidth="0.6"
                                 BarCornerRadius="4" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record TemperatureRange(string Day, double Min, double Max);

public ObservableCollection<TemperatureRange> TemperatureData { get; } = new()
{
    new("Mon", 12, 22),
    new("Tue", 14, 25),
    new("Wed", 10, 18),
    new("Thu", 16, 28),
    new("Fri", 13, 21)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例中显示的系列名称。 | `null` |
| `ItemsSource` | 要显示的数据项集合。 | `null` |
| `CategoryPath` | 指向 X 轴所用属性的路径。 | `null` |
| `LowPath` | 指向低值（最小值）属性的路径。 | `null` |
| `HighPath` | 指向高值（最大值）属性的路径。 | `null` |
| `Fill` | 填充条形所用的颜色/画刷。 | Theme-dependent |
| `Stroke` | 条形的轮廓颜色。 | `Transparent` |
| `BarWidth` | 每根条形的宽度，以类别带宽的比例表示（0.0 到 1.0）。 | `0.7` |
| `BarCornerRadius` | 条形的圆角程度。 | `2` |

## 另请参阅 {#see-also}

- [条形图](/controls/data-display/charts/cartesian/bar-chart)
- [差异图](/controls/data-display/charts/cartesian/variance-chart)
- [组合图](/controls/data-display/charts/cartesian/combo-chart)
