---
id: dot-plot-chart
title: 点图
description: 把数据点画成沿坐标轴排布的小圆点，适合比较各类别的数值或呈现频数分布。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

点图把每个数据点画成一个简单的圆点，这样既能跨类别比较数值，又没有条形那么重的视觉分量。

## 适用场景 {#when-to-use}
- **数值对比**：在多个类别之间比较各自的数值，又不像条形图那样拥挤。
- **频数分布**：展示数据集中各个取值出现的频繁程度。
- **小数据集**：当每个数据点的精确位置比整体形态更重要时。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Employee Ratings" Height="250">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <DotPlotSeries Title="Ratings"
                                ItemsSource="{Binding RatingData}"
                                CategoryPath="Department"
                                ValuePath="Score"
                                DotSize="12"
                                ShowConnectorLines="True" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record RatingItem(string Department, double Score);

public ObservableCollection<RatingItem> RatingData { get; } = new()
{
    new("Engineering", 4.5),
    new("Marketing", 3.8),
    new("Sales", 4.1),
    new("Support", 3.5),
    new("Design", 4.3)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例中显示的系列名称。 | `null` |
| `ItemsSource` | 要显示的数据项集合。 | `null` |
| `CategoryPath` | 指向 X 轴所用属性的路径。 | `null` |
| `ValuePath` | 指向 Y 轴所用属性的路径。 | `null` |
| `Fill` | 填充圆点所用的颜色/画刷。 | Theme-dependent |
| `Stroke` | 圆点的轮廓颜色。 | `Transparent` |
| `DotSize` | 每个圆点的大小，单位为像素。 | `10` |
| `ShowConnectorLines` | 是否显示连接各圆点的连线。 | `false` |
| `ConnectorThickness` | 连线的粗细。 | `1` |

## 另请参阅 {#see-also}

- [散点图](/controls/data-display/charts/cartesian/scatter-chart)
- [棒棒糖图](/controls/data-display/charts/cartesian/lollipop-chart)
- [条形图](/controls/data-display/charts/cartesian/bar-chart)
