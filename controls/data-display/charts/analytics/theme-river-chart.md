---
id: theme-river-chart
title: 主题河流图
description: 在笛卡尔图表中堆叠若干居中的 StackedAreaSeries，拼出一张主题河流图。
doc-type: reference
tags:
  - avalonia pro
---

import chartsAnalyticsThemeriver from '/img/controls/charts/charts-flow-themeriver.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

主题河流图呈现各类别随时间的消长。在 `Avalonia.Controls.Charts` 中，这种版面可以通过在 `CartesianChart` 内组合多个 `StackedAreaSeries` 来搭建。

<Image light={chartsAnalyticsThemeriver} maxWidth={400} position="center" cornerRadius="true" alt="Theme river chart with stacked organic stream bands showing how category volumes flow and change over time." />

## 适用场景 {#when-to-use}
- **话题趋势**：呈现新闻或社交媒体中各主题热度随时间的变化。
- **资源调配**：展示预算或人力在各项目之间的流动。
- **使用规律**：追踪各类网络流量的体量。

## 代码示例 {#code-example}

### XAML
```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="ThemeRiverSample" Title="Data Stream" Height="400"
                                           ShowLegend="True" LegendPosition="Bottom">
                        <CartesianChart.Series>
                            <!-- Dummy Series (Transparent Spacer for Wiggle/Centering) -->
                            <StackedAreaSeries Title="" ItemsSource="{Binding ThemeRiverDummy}"
                                                      CategoryPath="Category" ValuePath="Value"
                                                      StackGroup="River"
                                                      Fill="Transparent"
                                                      StrokeThickness="0" />

                            <!-- Visible Data Series -->
                            <StackedAreaSeries Title="Stream A" ItemsSource="{Binding ThemeRiverSeriesA}"
                                                      CategoryPath="Category" ValuePath="Value"
                                                      StackGroup="River"
                                                      Fill="#FF6B6B" Stroke="#E05555" StrokeThickness="1" />

                            <StackedAreaSeries Title="Stream B" ItemsSource="{Binding ThemeRiverSeriesB}"
                                                      CategoryPath="Category" ValuePath="Value"
                                                      StackGroup="River"
                                                      Fill="#4ECDC4" Stroke="#3EBDB4" StrokeThickness="1" />

                            <StackedAreaSeries Title="Stream C" ItemsSource="{Binding ThemeRiverSeriesC}"
                                                      CategoryPath="Category" ValuePath="Value"
                                                      StackGroup="River"
                                                      Fill="#FFE66D" Stroke="#EED55D" StrokeThickness="1" />
                        </CartesianChart.Series>

                        <CartesianChart.HorizontalAxis>
                             <CategoryAxis ShowGridLines="False" />
                        </CartesianChart.HorizontalAxis>

                        <CartesianChart.VerticalAxis>
                             <NumericalAxis ShowGridLines="False" IsVisible="False" />
                        </CartesianChart.VerticalAxis>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}
```csharp
using System.Collections.Generic;

public class ThemeRiverViewModel
{
    public List<ThemeRiverItem> ThemeRiverDummy { get; } = new();
    public List<ThemeRiverItem> ThemeRiverSeriesA { get; } = new();
    public List<ThemeRiverItem> ThemeRiverSeriesB { get; } = new();
    public List<ThemeRiverItem> ThemeRiverSeriesC { get; } = new();

    public ThemeRiverViewModel()
    {
        GenerateThemeRiverData();
    }

    private void GenerateThemeRiverData()
    {
        const int count = 30;
        const double center = 50.0;

        for (var i = 0; i < count; i++)
        {
            var category = $"T{i}";
            var streamA = 10 + 5 * System.Math.Sin(i * 0.3);
            var streamB = 15 + 8 * System.Math.Sin(i * 0.5 + 1);
            var streamC = 12 + 6 * System.Math.Cos(i * 0.4);
            var offset = center - (streamA + streamB + streamC) / 2;

            ThemeRiverDummy.Add(new ThemeRiverItem { Category = category, Value = offset });
            ThemeRiverSeriesA.Add(new ThemeRiverItem { Category = category, Value = streamA });
            ThemeRiverSeriesB.Add(new ThemeRiverItem { Category = category, Value = streamB });
            ThemeRiverSeriesC.Add(new ThemeRiverItem { Category = category, Value = streamC });
        }
    }
}

public class ThemeRiverItem
{
    public string Category { get; set; } = string.Empty;
    public double Value { get; set; }
}
```

## 常用属性（`StackedAreaSeries`） {#common-properties-stackedareaseries}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例中显示的系列名称。 | `null` |
| `ItemsSource` | 单条河流的数据点集合。 | `null` |
| `CategoryPath` | 用作横向类别或时间分桶的属性。 | `null` |
| `ValuePath` | 决定河流宽窄的属性。 | `null` |
| `StackGroup` | 相关面积系列共用的堆叠分组。 | `null` |
| `Fill` | 河流面积所用的画刷。 | Theme-dependent |
| `Stroke` | 河流轮廓所用的画刷。 | Theme-dependent |
