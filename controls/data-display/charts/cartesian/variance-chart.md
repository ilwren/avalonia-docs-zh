---
id: variance-chart
title: 差异图
description: 用条形呈现相对基准线的正负偏差，高于和低于参考线的部分以不同颜色区分。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

差异图绘制从基准值向上、向下延伸的条形，正负偏差分别用不同颜色表示，直观反映数值超出还是不及目标或参考点。

## 适用场景 {#when-to-use}
- **预算分析**：呈现实际与计划支出的差距，超支和结余各有配色。
- **绩效追踪**：呈现各类别 KPI 相对目标的偏离情况。
- **盈亏**：展示相对盈亏平衡点的盈利与亏损。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Monthly Profit/Loss" Height="250">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <VarianceSeries Title="Profit/Loss"
                                 ItemsSource="{Binding ProfitData}"
                                 CategoryPath="Month"
                                 ValuePath="Amount"
                                 Baseline="0"
                                 PositiveBrush="Green"
                                 NegativeBrush="Red"
                                 BarWidth="0.6" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record ProfitItem(string Month, double Amount);

public ObservableCollection<ProfitItem> ProfitData { get; } = new()
{
    new("Jan", 150),
    new("Feb", -80),
    new("Mar", 220),
    new("Apr", -30),
    new("May", 180),
    new("Jun", -120)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例中显示的系列名称。 | `null` |
| `ItemsSource` | 要显示的数据项集合。 | `null` |
| `CategoryPath` | 指向 X 轴所用属性的路径。 | `null` |
| `ValuePath` | 指向 Y 轴所用属性的路径。 | `null` |
| `Baseline` | 划分正负偏差的参考值。 | `0` |
| `PositiveBrush` | 基准线上方条形所用的画刷。 | `null` |
| `NegativeBrush` | 基准线下方条形所用的画刷。 | `null` |
| `BarWidth` | 每根条形的宽度，以类别带宽的比例表示（0.0 到 1.0）。 | `0.6` |
| `BarCornerRadius` | 条形的圆角程度。 | `2` |

## 另请参阅 {#see-also}

- [条形图](/controls/data-display/charts/cartesian/bar-chart)
- [区间条形图](/controls/data-display/charts/cartesian/range-bar-chart)
- [瀑布图](/controls/data-display/charts/cartesian/waterfall-chart)
