---
id: lollipop-chart
title: 棒棒糖图
description: 把数据画成圆点，再用细杆连到坐标轴上，兼具点图的精确和条形图的视觉落点。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

棒棒糖图把数据点画成圆点，并用细杆延伸到基线。它是条形图的轻量替代品，既减少了视觉上的杂乱，又把数值交代得清清楚楚。

## 适用场景 {#when-to-use}
- **轻量对比**：觉得条形图太「重」、想要更清爽的观感时。
- **类别众多**：并排比较大量类别时，降低墨水与数据的比例。
- **演示汇报**：做出好看的图表，又让重点落在数据点的数值上。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Monthly Sales" Height="250">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <LollipopSeries Title="Sales"
                                 ItemsSource="{Binding MonthlySales}"
                                 CategoryPath="Month"
                                 ValuePath="Amount"
                                 StemThickness="2"
                                 Orientation="Vertical" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record SalesItem(string Month, double Amount);

public ObservableCollection<SalesItem> MonthlySales { get; } = new()
{
    new("Jan", 320),
    new("Feb", 450),
    new("Mar", 280),
    new("Apr", 510),
    new("May", 390)
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
| `StemThickness` | 细杆的粗细。 | `2` |
| `StemBrush` | 细杆所用的画刷。 | `null`（未设置时与 `Fill` 同色。） |
| `Orientation` | 细杆的方向，`Vertical` 或 `Horizontal`。 | `Vertical` |

## 另请参阅 {#see-also}

- [点图](/controls/data-display/charts/cartesian/dot-plot-chart)
- [条形图](/controls/data-display/charts/cartesian/bar-chart)
- [散点图](/controls/data-display/charts/cartesian/scatter-chart)
