---
id: word-cloud-chart
title: 词云
description: 按词频或重要程度改变字号来呈现文本数据，为定性内容提供一目了然的视觉摘要。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsWordCloud from '/img/controls/charts/charts-analytics-word-cloud.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

词云按词频或重要程度改变字号来呈现文本数据，让定性内容或热门话题一目了然。

<Image light={chartsAnalyticsWordCloud} maxWidth={400} position="center" cornerRadius="true" alt="Word cloud displaying words at varying font sizes based on frequency, with more prominent words appearing larger." />

## 适用场景 {#when-to-use}
- **搜索趋势**：呈现查询日志中最常见的关键词。
- **情感分析**：凸显客户评价中的高频词。
- **内容概括**：展示一篇长文或文档的主要主题。

## 代码示例 {#code-example}

### XAML
```xml
<WordCloudChart xmlns="https://github.com/avaloniaui" Title="Popular Topics" Height="300"
                                             ItemsSource="{Binding WordCloudData}"
                                             WordPath="Word" WeightPath="Count"/>
```

### 数据模型（C#） {#data-model-c}
```csharp
public record WordItem(string Word, double Count);

public ObservableCollection<WordItem> WordCloudData { get; } = new()
{
    new("Technology", 80),
    new("Innovation", 65),
    new("Digital", 55),
    new("Cloud", 50),
    new("AI", 70),
    new("Data", 60),
    new("Security", 45),
    new("Mobile", 40),
    new("Development", 35),
    new("Analytics", 30),
    new("Performance", 25),
    new("User", 45),
    new("Interface", 40)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 词语与权重数据的集合。 | `null` |
| `WordPath` | 实际词语文本所对应的属性名。 | `null` |
| `WeightPath` | 决定字号的数值属性。 | `null` |
| `MinFontSize` | 最小字号，单位为像素。 | `12.0` |
| `MaxFontSize` | 最大字号，单位为像素。 | `48.0` |
| `MaxWords` | 最多渲染多少个词。 | `50` |
| `RotateWords` | 是否允许部分词语竖排旋转。 | `true` |
