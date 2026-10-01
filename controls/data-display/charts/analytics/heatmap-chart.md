---
id: heatmap-chart
title: 热力图
description: 用二维矩阵中带颜色编码的单元格表示数值，凸显其中的规律、相关性和异常值。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsHeatmap from '/img/controls/charts/charts-analytics-heatmap.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

热力图用带颜色编码的单元格表示二维矩阵中的数值，把两个维度上的规律、相关性和异常值凸显出来。

<Image light={chartsAnalyticsHeatmap} maxWidth={400} position="center" cornerRadius="true" alt="Heatmap chart showing a 2D matrix of color-coded cells representing data values across rows and columns." />

## 适用场景 {#when-to-use}
- **相关性矩阵**：呈现各变量之间的关联。
- **密度分布**：展示两个类别交叉处的频次或强度。
- **矩阵数据**：需要呈现行列交叉点上的数值时。

## 代码示例 {#code-example}

### XAML
```xml
<HeatmapChart xmlns="https://github.com/avaloniaui" Title="Correlation Matrix" Height="300"
                       ItemsSource="{Binding HeatmapData}"
                       RowPath="Row" ColumnPath="Col" ValuePath="Val"/>
```

### 数据模型（C#） {#data-model-c}
```csharp
using System;

public record HeatmapItem(string Row, string Col, double Val);

public ObservableCollection<HeatmapItem> HeatmapData { get; } = CreateHeatmapData();

private static ObservableCollection<HeatmapItem> CreateHeatmapData()
{
    var data = new ObservableCollection<HeatmapItem>();
    const int size = 10;

    for (var row = 0; row < size; row++)
    {
        for (var column = 0; column < size; column++)
        {
            var value = Math.Abs(Math.Sin(row * 0.5) * Math.Cos(column * 0.5) * 100);
            if (row == column)
            {
                value = 100;
            }

            data.Add(new($"R{row + 1}", $"C{column + 1}", value));
        }
    }

    return data;
}
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 图表标题。 | `null` |
| `ItemsSource` | 表示矩阵数据的集合。 | `null` |
| `RowPath` | 指向行标识属性的路径。 | `null` |
| `ColumnPath` | 指向列标识属性的路径。 | `null` |
| `ValuePath` | 指向单元格数值属性的路径。 | `null` |
| `LowBrush` | 最低值所用的画刷。 | `#E3F2FD` |
| `HighBrush` | 最高值所用的画刷。 | `#1565C0` |
| `ShowLabels` | 是否在每个单元格内显示数值。 | `true` |
| `CellGap` | 单元格之间的间隙大小。 | `2.0` |
| `CellCornerRadius` | 每个单元格的圆角半径。 | `CornerRadius(4)` |
| `LabelFontSize` | 行标签、列标签和单元格数值所用的字号。 | `11.0` |
| `LabelForeground` | 行列标签所用的画刷。单元格数值会自动采用与背景对比度合适的文字颜色。 | `null` |
| `IsHighlightEnabled` | 为热力图单元格启用悬停高亮。 | `false` |
