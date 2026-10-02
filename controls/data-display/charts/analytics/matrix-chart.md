---
id: matrix-chart
title: 矩阵图
description: 用网格呈现两组类别之间的布尔关系，标出每个行列交叉点上某项特性或状态是否存在。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsMatrix from '/img/controls/charts/charts-analytics-matrix.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

矩阵图用网格呈现两组类别之间的布尔关系。要表达「某项特性、状态或权限在行列交叉处是否存在」，它再合适不过。

<Image light={chartsAnalyticsMatrix} maxWidth={400} position="center" cornerRadius="true" alt="Matrix chart showing a grid of dots sized or colored by value at row and column intersections." />

## 适用场景 {#when-to-use}
- **相关性表格**：呈现众多变量之间的关联。
- **排班概览**：把人员与日期对应起来，标出可用时段或事件。
- **属性对比**：呈现哪些特性（列）适用于哪些产品（行）。

## 代码示例 {#code-example}

### XAML
```xml
<MatrixChart xmlns="https://github.com/avaloniaui" Title="Fruit Attributes" Height="300"
                                          ItemsSource="{Binding MatrixData}"
                                          ColumnLabels="{Binding MatrixColumns}"
                                          RowLabelPath="Attribute" ValuesPath="Values"
                                          CellSize="28" CellGap="25"/>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record MatrixItem(string Attribute, bool[] Values);

public ObservableCollection<string> MatrixColumns { get; } = new()
{
    "Grape", "Banana", "Orange", "Apple"
};

public ObservableCollection<MatrixItem> MatrixData { get; } = new()
{
    new("Good for juicing", new[] { false, true, true, true }),
    new("Good for smoothies", new[] { true, true, false, true }),
    new("Good for baking", new[] { true, false, true, true }),
    new("Good for jam", new[] { true, false, false, true }),
    new("Good for salads", new[] { true, false, true, true })
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 行数据的集合。 | `null` |
| `RowLabelPath` | 指向行标签属性的路径。 | `null` |
| `ColumnLabels` | 显示在顶部的列标签列表。 | `null` |
| `ValuesPath` | 指向该行各单元格布尔值的路径。 | `null` |
| `CellSize` | 每个矩阵单元格的直径。 | `30.0` |
| `CellGap` | 单元格之间的间隙。 | `2.0` |
| `TrueBrush` | `true` 值所用的画刷。 | `null` |
| `FalseBrush` | `false` 值所用的画刷。 | `null` |
| `ShowFilledCircles` | `true` 值是用实心填充还是只描边。 | `true` |
| `ShowRowLabels` | 是否为每一行显示标签。 | `true` |
| `ShowColumnLabels` | 是否为每一列显示标签。 | `true` |
| `LabelFontSize` | 行列标签所用的字号。 | `11.0` |
| `IsHighlightEnabled` | 为矩阵单元格启用悬停高亮。 | `false` |
