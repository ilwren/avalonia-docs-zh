---
id: bubble-cloud-chart
title: 气泡云图
description: 不设坐标轴，把大小不一的气泡自然地簇拥在一起，适合呈现带排名的类别和关注度分布。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

气泡云图把气泡聚成一簇、不依赖坐标轴，主要的数量含义由气泡大小承载。

## 适用场景 {#when-to-use}

- **突出类别**：不必依赖精确的坐标轴，就能看出哪些类别占主导。
- **关注度分布**：在紧凑的画面中托出重要的话题、细分市场或产品。
- **仪表板磁贴**：为条形图或表格提供一种更灵动的替代形式。

## 代码示例 {#code-example}

### XAML

```xml
<BubbleCloud xmlns="https://github.com/avaloniaui" Title="Topic volume"
                      Height="320"
                      ItemsSource="{Binding Topics}"
                      LabelPath="Name"
                      ValuePath="Count" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record TopicBubble(string Name, double Count);

public ObservableCollection<TopicBubble> Topics { get; } = new()
{
    new("Support", 120),
    new("Billing", 75),
    new("Shipping", 55)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 气泡项的集合。 | `null` |
| `LabelPath` | 指向气泡标签的路径。 | `null` |
| `ValuePath` | 指向决定气泡大小那个数值的路径。 | `null` |
| `MinBubbleSize` | 气泡最小半径，单位为像素。 | `30.0` |
| `MaxBubbleSize` | 气泡最大半径，单位为像素。 | `80.0` |
| `IsHighlightEnabled` | 为气泡启用悬停高亮。 | `false` |

## 另请参阅 {#see-also}

- [紧凑气泡图](/controls/data-display/charts/bubble/packed-bubble-chart)
- [词云](/controls/data-display/charts/analytics/word-cloud-chart)
