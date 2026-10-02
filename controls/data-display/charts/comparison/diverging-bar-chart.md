---
id: diverging-bar-chart
title: 双向条形图
description: 条形从基准线向左右两侧延伸，用来比较正负数值或对立的反馈。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

双向条形图把基准线放在中间，数值由同一个原点向相反方向延伸。

## 适用场景 {#when-to-use}

- **情感分化**：以零为中心展示正面和负面的反馈。
- **偏差视图**：比较相对基准线的超额与不足。
- **平衡对比**：不必画两张图，就能凸显方向上的差异。

## 代码示例 {#code-example}

### XAML

```xml
<DivergingBarChart xmlns="https://github.com/avaloniaui" Title="Net sentiment"
                            Height="300"
                            ItemsSource="{Binding SentimentData}"
                            LabelPath="Label"
                            ValuePath="Score" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record SentimentPoint(string Label, double Score);

public ObservableCollection<SentimentPoint> SentimentData { get; } = new()
{
    new("Product A", 24),
    new("Product B", -12),
    new("Product C", 8)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 待比较项的集合。 | `null` |
| `ValuePath` | 指向相对基准线所绘数值的路径。 | `null` |
| `LabelPath` | 指向类别标签的路径。 | `null` |
| `Baseline` | 中心基准值。 | `0.0` |
| `PositiveBrush` | 高于基准线的数值所用的画刷。 | `null` |
| `NegativeBrush` | 低于基准线的数值所用的画刷。 | `null` |
| `BarHeight` | 条形高度，以行高的比例表示。 | `0.7` |
| `ShowValues` | 是否在条形内部绘制数值标签。 | `true` |
| `IsHighlightEnabled` | 为条形启用悬停高亮。 | `false` |

## 另请参阅 {#see-also}

- [条形图](/controls/data-display/charts/cartesian/bar-chart)
- [镜像条形图](/controls/data-display/charts/comparison/mirror-bar-chart)
