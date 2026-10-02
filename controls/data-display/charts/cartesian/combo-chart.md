---
id: combo-chart
title: 组合图
description: 在共享的类别轴上组合多种笛卡尔系列，并可选地支持次 Y 轴。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

`ComboChart` 是 `CartesianChart` 的一个变体，用于把 `BarSeries`、`LineSeries`、`AreaSeries` 等多种系列类型放在同一条横轴上。当图表本身需要对外提供一条可选的次 Y 轴时，就用它。

## 适用场景 {#when-to-use}

- **混合视觉编码**：在同一张图中组合条形、折线或面积。
- **双刻度对比**：把次要指标画在独立的 Y 轴上。
- **共享类别**：让多种系列类型对齐到同一组类别标签。

## 代码示例 {#code-example}

### XAML

```xml
<ComboChart xmlns="https://github.com/avaloniaui" Title="Revenue and margin"
                     Height="320"
                     ShowLegend="True"
                     ShowSecondaryAxis="True">
    <ComboChart.HorizontalAxis>
        <CategoryAxis Title="Month" />
    </ComboChart.HorizontalAxis>
    <ComboChart.VerticalAxis>
        <NumericalAxis Title="Revenue ($K)" />
    </ComboChart.VerticalAxis>
    <ComboChart.SecondaryVerticalAxis>
        <NumericalAxis Title="Margin (%)" />
    </ComboChart.SecondaryVerticalAxis>
    <ComboChart.Series>
        <BarSeries Title="Revenue"
                            ItemsSource="{Binding MonthlyMetrics}"
                            CategoryPath="Month"
                            ValuePath="Revenue" />
        <LineSeries Title="Margin"
                             ItemsSource="{Binding MonthlyMetrics}"
                             CategoryPath="Month"
                             ValuePath="MarginPercent"
                             YAxisPosition="Secondary" />
    </ComboChart.Series>
</ComboChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
public record MonthlyMetric(string Month, double Revenue, double MarginPercent);

public ObservableCollection<MonthlyMetric> MonthlyMetrics { get; } = new()
{
    new("Jan", 120, 18),
    new("Feb", 145, 21),
    new("Mar", 138, 19),
    new("Apr", 166, 24)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Series` | 图表中所渲染的笛卡尔系列内容集合。 | 空集合 |
| `HorizontalAxis` | 各混合系列所用的主横轴。 | `null` |
| `VerticalAxis` | 各混合系列所用的主纵轴。 | `null` |
| `ShowSecondaryAxis` | 是否在右侧显示次 Y 轴。 | `false` |
| `SecondaryVerticalAxis` | 可选的次纵轴，供设为 `YAxisPosition.Secondary` 的系列使用。 | `null` |

## 注释支持情况 {#notes}

- 系列按声明顺序渲染。
- 要让某个系列对齐次 Y 轴，把该系列设为 `YAxisPosition="Secondary"` 即可。
- `BarWidth`、`MarkerShape`、`FillOpacity` 等属性请查阅各系列自己的页面。

## 另请参阅 {#see-also}

- [条形图](/controls/data-display/charts/cartesian/bar-chart)
- [折线图](/controls/data-display/charts/cartesian/line-chart)
- [面积图](/controls/data-display/charts/cartesian/area-chart)
- [坐标轴定制](/controls/data-display/charts/shared-elements/axis-customization-chart)
