---
id: wind-rose-chart
title: 风玫瑰图
description: 以堆叠的极坐标扇区呈现各方向上的频数分布，适合分析风向、车流和各类方向性事件。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

风玫瑰图按方向归类数值，并在每个方向扇区内堆叠细分类别，比如各档风速。

## 适用场景 {#when-to-use}

- **气象**：按风向和风速档位呈现风的频数。
- **方向性事件**：围绕罗盘比较车流、移动或信号的出现情况。
- **运行分析**：用一张紧凑的极坐标图概括按航向统计的活动。

## 代码示例 {#code-example}

### XAML

```xml
<WindRoseChart xmlns="https://github.com/avaloniaui" Title="Wind distribution"
                                Height="320"
                                ItemsSource="{Binding WindData}"
                                DirectionPath="Direction"
                                SpeedPath="SpeedBand"
                                ValuePath="Frequency" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record WindSample(string Direction, string SpeedBand, double Frequency);

public ObservableCollection<WindSample> WindData { get; } = new()
{
    new("N", "0-10", 12),
    new("N", "10-20", 6),
    new("NE", "0-10", 8)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 方向观测数据的集合。 | `null` |
| `DirectionPath` | 指向方向分组的路径。 | `null` |
| `SpeedPath` | 指向各方向内部堆叠子分组的路径。 | `null` |
| `ValuePath` | 指向数值或频数的路径。 | `null` |
| `StartAngle` | 首个扇区的起始角度，单位为度。 | `-90.0` |

## 另请参阅 {#see-also}

- [极坐标图](/controls/data-display/charts/radial/polar-chart)
- [史密斯圆图](/controls/data-display/charts/engineering/smith-chart)
