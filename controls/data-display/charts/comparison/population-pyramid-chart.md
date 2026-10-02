---
id: population-pyramid-chart
title: 人口金字塔图
description: 按年龄段或其他有序类别，把两组人口分布背靠背地呈现出来。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

人口金字塔图呈现相对的两组分布，最常见的是各年龄段的男性与女性人口。

## 适用场景 {#when-to-use}

- **人口分析**：按性别或地区比较年龄分布。
- **分段对比**：在有序的分段上呈现成对的分布。
- **规划视图**：迅速看出人口集中在年轻还是年长的群体。

## 代码示例 {#code-example}

### XAML

```xml
<PopulationPyramidChart xmlns="https://github.com/avaloniaui" Title="Age distribution"
                                 Height="350"
                                 ItemsSource="{Binding PopulationData}"
                                 AgeLabelPath="AgeGroup"
                                 MaleValuePath="Male"
                                 FemaleValuePath="Female" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record PopulationBand(string AgeGroup, double Male, double Female);

public ObservableCollection<PopulationBand> PopulationData { get; } = new()
{
    new("0-9", 12, 11),
    new("10-19", 14, 13),
    new("20-29", 16, 17)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 人口分段的集合。 | `null` |
| `AgeLabelPath` | 指向分段标签的路径。 | `null` |
| `MaleValuePath` | 指向左侧人口数值的路径。 | `null` |
| `FemaleValuePath` | 指向右侧人口数值的路径。 | `null` |
| `MaleBrush` | 左侧条形所用的画刷。 | `null` |
| `FemaleBrush` | 右侧条形所用的画刷。 | `null` |
| `BarGap` | 相邻条形之间的间隙。 | `2.0` |
| `ShowLabels` | 是否沿中线显示分段标签。 | `true` |
| `LabelFontSize` | 分段标签所用的字号。 | `10.0` |
| `IsHighlightEnabled` | 为人口分段启用悬停高亮。 | `false` |

## 另请参阅 {#see-also}

- [镜像条形图](/controls/data-display/charts/comparison/mirror-bar-chart)
- [龙卷风图](/controls/data-display/charts/comparison/tornado-chart)
