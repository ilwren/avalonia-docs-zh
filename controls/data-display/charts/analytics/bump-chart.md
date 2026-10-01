---
id: bump-chart
title: 凹凸图
description: 呈现名次随时间的升降，关注各类别之间的相对位置，而非绝对数值。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsBump from '/img/controls/charts/charts-statistical-bump.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

凹凸图是折线图的一种变体，专门用来呈现名次随时间的变化。它关注的是各类别之间的相对位置，而非它们的绝对数值。

<Image light={chartsAnalyticsBump} maxWidth={400} position="center" cornerRadius="true" alt="Bump chart showing rank changes over time with smooth curved lines connecting each entity's position across periods." />

## 适用场景 {#when-to-use}
- **人气榜单**：展示歌曲或电影在十大榜单中的起落。
- **市场份额**：呈现各品牌争夺头把交椅的过程。
- **赛事积分榜**：追踪各支队伍在不同阶段的相对表现。

## 代码示例 {#code-example}

### XAML
```xml
<BumpChart xmlns="https://github.com/avaloniaui" Name="BumpChartSample"
                                        Title="Ranking Changes"
                                        Height="300"
                                        NamePath="Name"
                                        RankingsPath="Ranks"
                                        Periods="{Binding BumpPeriods}"
                                        ItemsSource="{Binding BumpData}" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record BumpItem(string Name, int[] Ranks);

public ObservableCollection<BumpItem> BumpData { get; } = new()
{
    new("Java", new[] { 1, 2, 2, 3, 3 }),
    new("C#", new[] { 4, 3, 3, 2, 2 }),
    new("Python", new[] { 2, 1, 1, 1, 1 }),
    new("JS", new[] { 3, 4, 4, 4, 4 })
};

public ObservableCollection<string> BumpPeriods { get; } = new()
{
    "2020", "2021", "2022", "2023", "2024"
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 参与排名的实体集合。 | `null` |
| `NamePath` | 表示实体名称的属性。 | `null` |
| `RankingsPath` | 表示各实体名次序列的属性。 | `null` |
| `Periods` | 沿横轴显示的标签。 | `null` |
| `StrokeThickness` | 名次连线的粗细。 | `3.0` |
| `MarkerSize` | 每个时期上所绘标记点的大小。 | `10.0` |
| `ShowLabels` | 是否在每条线的末端显示实体标签。 | `true` |
| `ShowRankNumbers` | 是否在纵轴上显示名次数字。 | `true` |
