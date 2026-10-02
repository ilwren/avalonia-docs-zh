---
id: table-chart
title: 表格图
description: 把表格数据与内嵌的视觉提示（比如色阶）结合起来，适合既要精确数值又信息密集的报表。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsTable from '/img/controls/charts/charts-analytics-table.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

表格图把传统的表格数据与内嵌的视觉提示结合在一起。当用户既需要精确数值、又想快速作视觉比较时，这类信息密集的报表很适合用它。

<Image light={chartsAnalyticsTable} maxWidth={400} position="center" cornerRadius="true" alt="Table chart displaying rows of data with color-coded indicators for visual comparison." />

## 适用场景 {#when-to-use}
- **产品对比**：在一张网格里展示众多产品的各项特性。
- **财务状况**：展示各个账户，并用颜色标出「健康度」。
- **多指标报表**：用户需要在紧凑的版面中比较多项指标时。

## 代码示例 {#code-example}

### XAML
```xml
<TableChart xmlns="https://github.com/avaloniaui" Title="Product Comparison" Height="400"
                                         ItemsSource="{Binding TableData}"
                                         Columns="{Binding TableColumns}"
                                         RowLabelPath="Product" />
```

### 数据模型（C#） {#data-model-c}
```csharp
using Avalonia.Controls.Charts;
using Avalonia.Media;

public record TableItem(
    string Product,
    double Sales,
    double Price,
    double Sweetness,
    double Juiciness,
    double Acidity);

public ObservableCollection<TableItem> TableData { get; } = new()
{
    new("Apple", 200, 1.2, 6.8, 7.0, 4.5),
    new("Banana", 180, 0.5, 7.0, 8.5, 3.0),
    new("Orange", 150, 1.0, 5.5, 9.0, 6.0),
    new("Grape", 140, 2.5, 6.5, 6.0, 4.0),
    new("Pineapple", 130, 1.8, 6.0, 7.5, 5.0),
    new("Blueberry", 120, 3.0, 5.0, 6.5, 4.0),
    new("Mango", 110, 1.5, 8.5, 8.0, 2.5),
    new("Strawberry", 100, 2.0, 8.0, 5.0, 3.5)
};

public ObservableCollection<TableChartColumn> TableColumns { get; } = new()
{
    new()
    {
        Header = "Avg Sales\n(units/mo)",
        ValuePath = "Sales",
        UseColorScale = true,
        MinValue = 100,
        MaxValue = 200,
        LowBrush = new SolidColorBrush(Color.FromRgb(220, 235, 255)),
        HighBrush = new SolidColorBrush(Color.FromRgb(33, 150, 243))
    },
    new()
    {
        Header = "Avg Price\n($)",
        ValuePath = "Price",
        Format = "C1",
        UseColorScale = true,
        MinValue = 0.5,
        MaxValue = 3.0,
        LowBrush = new SolidColorBrush(Color.FromRgb(255, 235, 220)),
        HighBrush = new SolidColorBrush(Color.FromRgb(255, 152, 0))
    },
    new() { Header = "Sweetness\n(0-10)", ValuePath = "Sweetness" },
    new() { Header = "Juiciness\n(0-10)", ValuePath = "Juiciness" },
    new() { Header = "Acidity\n(0-10)", ValuePath = "Acidity" }
};
```

`Columns` 接受若干 `TableChartColumn` 对象。每一列都可以定义 `Header`、`ValuePath`、`Format`，以及可选的色阶设置。

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 行数据源。 | `null` |
| `RowLabelPath` | 指向左侧行标题列所显示文本的路径。 | `null` |
| `Columns` | 网格各列的配置。 | `null` |
| `RowHeight` | 每个数据行的高度。 | `40.0` |
| `ColumnWidth` | 每个指标列的最小宽度。 | `80.0` |
| `RowLabelWidth` | 行标签列的宽度。 | `100.0` |
| `HeaderHeight` | 表头行的高度。 | `50.0` |
| `ShowGridLines`| 是否显示行列之间的网格线。 | `true` |
| `CellPadding` | 每个表格单元格内部的内边距。 | `5.0` |
| `LabelFontSize` | 表头和单元格数值所用的字号。 | `12.0` |
