---
id: radar-chart
title: 雷达图
description: 在径向轴上比较多个类别的多项定量变量，用来呈现画像和多维度的表现对比。
doc-type: reference
tags:
  - avalonia pro
---

import chartsRadialRadar from '/img/controls/charts/charts-radial-radar.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

雷达图在若干类别上比较多项定性变量。要呈现不同对象在共同指标上的「画像」或特征轮廓，它被广泛采用。

<Image light={chartsRadialRadar} maxWidth={400} position="center" cornerRadius="true" alt="Radar chart with two overlapping polygons comparing multi-dimensional skill scores across radial axes." />

## 适用场景 {#when-to-use}
- **能力评估**：比较员工或运动员各自的长短板。
- **产品对标**：从价格、品质、功能等方面比较不同产品。
- **表现画像**：呈现多个侧面的指标（比如网站的 SEO、速度、安全性）。

## 代码示例 {#code-example}

### XAML

```xml
<RadarChart xmlns="https://github.com/avaloniaui" Name="RadarChartSample" Title="Team Skills" Height="350" IsTooltipEnabled="True"
                                         AxisLabels="{Binding RadarLabels}">
                        <RadarChart.Series>
                            <RadarSeries Title="Player A" ItemsSource="{Binding RadarSeries1}" FillOpacity="0.3" ShowMarkers="True" />
                            <RadarSeries Title="Player B" ItemsSource="{Binding RadarSeries2}" FillOpacity="0.3" ShowMarkers="True" />
                        </RadarChart.Series>
                     </RadarChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
// Axis labels mapped to categories
public ObservableCollection<string> RadarLabels { get; } = new()
{
    "Speed", "Power", "Agility", "Defense", "Stamina", "Technique"
};

// Values for the axes in order
public ObservableCollection<double> RadarSeries1 { get; } = new() { 80, 90, 70, 60, 85, 75 };
public ObservableCollection<double> RadarSeries2 { get; } = new() { 60, 70, 85, 80, 65, 90 };
```

## 常用属性（`RadarChart`） {#common-properties-radarchart}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `AxisCount` | 图表周围显示的轴数。 | `5` |
| `ShowGridLines` | 是否绘制同心的雷达网格。 | `true` |
| `GridLevels` | 同心网格的圈数。 | `5` |
| `AxisLabels` | 为每条轴显示的标签。 | `null` |
| `IsHighlightEnabled` | 为雷达数据点启用图表级的悬停高亮。 | `false` |

## 常用属性（`RadarSeries`） {#common-properties-radarseries}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 雷达各轴上的数值。 | `null` |
| `Title` | 参与者/实体的名称（用于图例）。 | `null` |
| `MaxValue` | 用于缩放该系列的最大值。 | `100.0` |
| `Fill` | 多边形区域所用的画刷。为 `null` 时，图表采用系列调色板的画刷并套用 `FillOpacity`。 | `null` |
| `Stroke` | 多边形边框所用的画刷。为 `null` 时，图表采用系列调色板的画刷。 | `null` |
| `FillOpacity` | 填充多边形区域所用的不透明度。 | `0.3` |
| `ShowMarkers` | 开关各轴交点处的数据点。 | `true` |
| `MarkerSize` | 各轴交点处标记的大小。 | `6` |
