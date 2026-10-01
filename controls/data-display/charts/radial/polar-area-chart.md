---
id: polar-area-chart
title: 极坐标面积图
description: 与饼图相似，但用扇段半径而非角度表示数值，每个类别在环形轴上占据相同的角度。
doc-type: reference
tags:
  - avalonia pro
---

import chartsRadialPolararea from '/img/controls/charts/charts-radial-polar.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

极坐标面积图（又称鸡冠花图）与饼图相似，只是改用扇段的半径而非角度来表示数值，各扇段的角度都相同。

<Image light={chartsRadialPolararea} maxWidth={400} position="center" cornerRadius="true" alt="Polar area chart with equal-angle segments of varying radius representing seasonal magnitude values in a circular layout." />

## 适用场景 {#when-to-use}
- **周期性走势**：呈现季节性数据或风向规律。
- **类别排序**：在环形版面中比较众多类别的量级。
- **历史分析**：呈现死亡原因随时间变化的那张经典图表，用的就是它。

## 代码示例 {#code-example}

### XAML
```xml
<PolarAreaChart xmlns="https://github.com/avaloniaui" Name="PolarAreaChartSample" Title="Skill Levels" Height="300"
                                             ItemsSource="{Binding PolarChartData}"
                                             LabelPath="Label" ValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record RadialPoint(string Label, double Value);

public ObservableCollection<RadialPoint> PolarChartData { get; } = new()
{
    new("Speed", 85),
    new("Strength", 70),
    new("Agility", 60),
    new("Intellect", 75),
    new("Stamina", 90),
    new("Spirit", 65)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 各扇段的集合。 | `null` |
| `ValuePath` | 决定扇区半径的属性。 | `null` |
| `LabelPath` | 表示扇区名称的属性。 | `null` |
| `ShowLabels` | 是否为各扇段显示标签。 | `true` |
| `LabelFontSize` | 各段标签所用的字号。 | `11.0` |
| `LabelForeground` | 扇段标签所用的画刷。为 `null` 时，图表采用当前生效的标签前景色。 | `null` |
| `StartAngle` | 首个扇段的起始角度，单位为度。 | `-90.0` |
| `Stroke` | 各扇段的轮廓画刷。为 `null` 时，图表使用白色轮廓。 | `null` (white) |
| `StrokeThickness` | 扇段轮廓的粗细。 | `1.0` |
| `IsHighlightEnabled` | 为极坐标面积扇段启用悬停高亮。 | `false` |
