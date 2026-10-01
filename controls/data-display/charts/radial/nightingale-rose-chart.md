---
id: nightingale-rose-chart
title: 南丁格尔玫瑰图
description: 一种各扇段角度相等、半径不等的极坐标面积图，适合在环形版面中比较各类别的量级。
doc-type: reference
tags:
  - avalonia pro
---

import chartsRadialRose from '/img/controls/charts/charts-radial-rose.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

南丁格尔玫瑰图是一种极坐标面积图，各扇段角度相等而半径不等。当你想用环形形式取代条形图、同时每个类别仍只有一个数值时，它很合用。

<Image light={chartsRadialRose} maxWidth={400} position="center" cornerRadius="true" alt="Nightingale rose chart with stacked sub-segments in each circular slice comparing composition across cyclical categories." />

## 适用场景 {#when-to-use}
- **季节性概览**：比较同一项指标在各月份或各季度的表现。
- **类别对比**：不借助笛卡尔坐标轴也能呈现相对量级。
- **环形仪表板**：当各类别本身构成一个循环时，采用径向版面。

## 代码示例 {#code-example}

### XAML
```xml
<NightingaleRoseChart xmlns="https://github.com/avaloniaui" Name="NightingaleRoseSample"
                               Title="Monthly Sales"
                               Height="350"
                               ShowLabels="True"
                               ItemsSource="{Binding NightingaleData}"
                               ValuePath="Value"
                               LabelPath="Label" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record RadialPoint(string Label, double Value);

public ObservableCollection<RadialPoint> NightingaleData { get; } = new()
{
    new("Jan", 120.0), new("Feb", 180.0), new("Mar", 160.0),
    new("Apr", 200.0), new("May", 280.0), new("Jun", 350.0),
    new("Jul", 380.0), new("Aug", 340.0), new("Sep", 250.0),
    new("Oct", 180.0), new("Nov", 140.0), new("Dec", 160.0)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 各扇段的集合。 | `null` |
| `ValuePath` | 每个扇段的半径量值。 | `null` |
| `LabelPath` | 每个扇段的类别标签。 | `null` |
| `InnerRadiusFactor` | 内半径比例，取 `0.0` 时得到一张实心的玫瑰图。 | `0.0` |
| `ShowLabels` | 是否显示扇段标签。 | `true` |
| `ShowValues` | 是否在标签旁一并显示数值。 | `false` |
| `IsHighlightEnabled` | 为各扇段启用悬停高亮。 | `false` |
