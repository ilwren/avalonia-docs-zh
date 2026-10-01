---
id: packed-bubble-chart
title: 紧凑气泡图
description: 不设坐标轴，把大小不一的气泡紧密排布在一起，适合在有限空间里按比例比较各类别。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

紧凑气泡图用气泡大小表示各类别的量级，同时把这些圆紧紧地码进同一个画框里。

## 适用场景 {#when-to-use}

- **部分与整体**：不用条形图也能按大小比较各类别。
- **紧凑仪表板**：把众多类别塞进一张方形卡片。
- **以标签为先的比较**：空间允许时，把类别名称直接放进气泡里。

## 代码示例 {#code-example}

### XAML

```xml
<PackedBubbleChart xmlns="https://github.com/avaloniaui" Title="Segment size"
                            Height="320"
                            ItemsSource="{Binding Segments}"
                            LabelPath="Name"
                            ValuePath="Value"
                            ShowLabels="True" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record SegmentBubble(string Name, double Value);

public ObservableCollection<SegmentBubble> Segments { get; } = new()
{
    new("Desktop", 42),
    new("Mobile", 30),
    new("Web", 18)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 气泡项的集合。 | `null` |
| `ValuePath` | 指向决定气泡大小那个数值的路径。 | `null` |
| `LabelPath` | 指向气泡标签的路径。 | `null` |
| `MinBubbleSize` | 气泡最小尺寸，单位为像素。 | `20.0` |
| `MaxBubbleSize` | 气泡最大尺寸，单位为像素。 | `80.0` |
| `ShowLabels` | 空间允许时是否在气泡内部绘制标签。 | `true` |
| `LabelFontSize` | 气泡标签的基准字号。实际渲染尺寸还会受各气泡半径的限制。 | `12.0` |
| `LabelForeground` | 气泡标签所用的画刷。为 `null` 时，标签使用白色。 | `null` |
| `IsHighlightEnabled` | 为气泡启用悬停高亮。 | `false` |

## 另请参阅 {#see-also}

- [气泡云图](/controls/data-display/charts/bubble/bubble-cloud-chart)
- [气泡图](/controls/data-display/charts/bubble/bubble-chart)
