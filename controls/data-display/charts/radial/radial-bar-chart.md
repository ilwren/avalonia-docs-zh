---
id: radial-bar-chart
title: 径向条形图
description: 绘制在极坐标系上的条形图，以省地方的环形版面比较各类别或追踪多项目标进度。
doc-type: reference
tags:
  - avalonia pro
---

import chartsRadialBar from '/img/controls/charts/charts-radial-bar.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

径向条形图采用极坐标系，本质上就是画在环形网格上的条形图，既别致又省地方，很适合用来比较各个类别。

<Image light={chartsRadialBar} maxWidth={400} position="center" cornerRadius="true" alt="Radial bar chart with concentric circular bars of varying arc lengths comparing category progress on a polar grid." />

## 适用场景 {#when-to-use}
- **环形对比**：呈现本身带有周期性的数据（比如一天 24 小时）。
- **仪表板信息图**：为带排名的类别制作紧凑的视觉摘要。
- **进度追踪**：把多条目标进度汇总到一个径向版面中呈现。

## 代码示例 {#code-example}

### XAML
```xml
<RadialBarChart xmlns="https://github.com/avaloniaui" Name="RadialBarChartSample" Title="Performance Metrics" Height="350"
                                             ItemsSource="{Binding RadialBarData}"
                                             CategoryPath="Label" ValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record RadialPoint(string Label, double Value);

public ObservableCollection<RadialPoint> RadialBarData { get; } = new()
{
    new("Speed", 85),
    new("Power", 70),
    new("Agility", 60),
    new("Defense", 75),
    new("Stamina", 90)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 分类条目的集合。 | `null` |
| `ValuePath` | 决定条形长度的数值属性。 | `null` |
| `CategoryPath` | 类别标签所对应的属性名。 | `null` |
| `InnerRadiusFactor` | 中心孔洞的相对大小，取值从 `0.0` 到 `1.0`。 | `0.2` |
| `StartAngle` | 起始角度，单位为度。 | `-90.0` |
| `GapAngle` | 条形之间的角度间隔。 | `2.0` |
| `ShowLabels` | 标签是否可见。 | `true` |
| `ShowValues` | 数值是否可见。 | `true` |
| `LabelFontSize` | 类别标签所用的字号。数值标签会小一个像素。 | `10.0` |
| `LabelForeground` | 类别标签所用的画刷。为 `null` 时，图表采用当前生效的标签前景色。 | `null` |
| `IsHighlightEnabled` | 为径向条形启用悬停高亮。 | `false` |
