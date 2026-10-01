---
id: stacked-100-percent-bar-chart
title: 百分比堆叠条形图
description: 条形始终铺满 100%，呈现各系列在同一类别中所占的相对比例，而非绝对数值。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

百分比堆叠条形图中的条形总是等高，用来呈现各类别的百分比构成。每一段代表一个系列所占的比例，读者据此可以比较各自的相对贡献。

## 适用场景 {#when-to-use}
- **占比对比**：比较不同类别中各组成部分对整体的贡献。
- **市场份额**：呈现相对市场份额，或各部门的预算分配。
- **调查结果**：展示百分比构成，比如每道题赞成/反对的比例。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Browser Market Share" Height="250">
    <CartesianChart.HorizontalAxis>
        <CategoryAxis />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <Stacked100PercentBarSeries Title="Chrome"
                                              ItemsSource="{Binding ChromeData}"
                                              CategoryPath="Year"
                                              ValuePath="Share"
                                              StackGroup="browsers" />
        <Stacked100PercentBarSeries Title="Firefox"
                                              ItemsSource="{Binding FirefoxData}"
                                              CategoryPath="Year"
                                              ValuePath="Share"
                                              StackGroup="browsers" />
        <Stacked100PercentBarSeries Title="Safari"
                                              ItemsSource="{Binding SafariData}"
                                              CategoryPath="Year"
                                              ValuePath="Share"
                                              StackGroup="browsers" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record BrowserShare(string Year, double Share);

public ObservableCollection<BrowserShare> ChromeData { get; } = new()
{
    new("2022", 65), new("2023", 63), new("2024", 66)
};

public ObservableCollection<BrowserShare> FirefoxData { get; } = new()
{
    new("2022", 20), new("2023", 18), new("2024", 15)
};

public ObservableCollection<BrowserShare> SafariData { get; } = new()
{
    new("2022", 15), new("2023", 19), new("2024", 19)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例中显示的系列名称。 | `null` |
| `ItemsSource` | 要显示的数据项集合。 | `null` |
| `CategoryPath` | 指向 X 轴所用属性的路径。 | `null` |
| `ValuePath` | 指向 Y 轴所用属性的路径。 | `null` |
| `Fill` | 填充条形所用的颜色/画刷。 | Theme-dependent |
| `Stroke` | 条形的轮廓颜色。 | `Transparent` |
| `StackGroup` | 把多个系列合并进同一根堆叠条形所用的分组名称。 | `"default"` |
| `BarWidth` | 每根条形的宽度，以类别带宽的比例表示（0.0 到 1.0）。 | `0.7` |
| `BarCornerRadius` | 条形的圆角程度。 | `0` |

## 另请参阅 {#see-also}

- [条形图](/controls/data-display/charts/cartesian/bar-chart)
- [堆叠条形图](/controls/data-display/charts/cartesian/stacked-bar-chart)
- [组合图](/controls/data-display/charts/cartesian/combo-chart)
