---
id: mosaic-chart
title: 马赛克图
description: 同时用分段的宽度和高度表示各自占总量的比例，呈现两个分类变量之间的关系。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsMosaic from '/img/controls/charts/charts-analytics-mosaic.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

马赛克图（Marimekko）用面积来呈现各类别之间的关系。每个分段的宽度和高度都按其占总量的百分比缩放。

<Image light={chartsAnalyticsMosaic} maxWidth={400} position="center" cornerRadius="true" alt="Mosaic chart with rectangular tiles scaled by both width and height to show proportions across two categorical variables." />

## 适用场景 {#when-to-use}
- **市场细分**：按地区（宽）和产品品类（高）呈现销售额。
- **资源支出**：呈现预算在各部门、各费用类型之间的分配。
- **多因素分析**：弄清两个定性变量如何相互作用。

## 代码示例 {#code-example}

### XAML
```xml
<MosaicChart xmlns="https://github.com/avaloniaui" Title="Sales by Region" Height="300"
                      ItemsSource="{Binding MosaicData}"
                      GroupPath="Region"
                      SubGroupPath="Category"
                      ValuePath="Sales" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record MosaicItem(string Region, string Category, double Sales);

public ObservableCollection<MosaicItem> MosaicData { get; } = new()
{
    new("North", "Electronics", 450),
    new("North", "Clothing", 320),
    new("North", "Home", 210),
    new("South", "Electronics", 380),
    new("South", "Clothing", 410),
    new("South", "Home", 180),
    new("East", "Electronics", 290),
    new("East", "Clothing", 250),
    new("East", "Home", 350),
    new("West", "Clothing", 280),
    new("West", "Home", 150)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 数据分段的集合。 | `null` |
| `GroupPath` | 主类别（决定宽度）。 | `null` |
| `SubGroupPath` | 次类别（决定高度）。 | `null` |
| `ValuePath` | 用于缩放的数值。 | `null` |
