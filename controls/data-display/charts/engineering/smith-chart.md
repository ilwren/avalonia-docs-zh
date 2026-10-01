---
id: smith-chart
title: 史密斯圆图
description: 在归一化的反射系数网格上呈现复阻抗或复导纳，服务于射频与阻抗匹配分析。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

史密斯圆图把归一化的电阻和电抗绘制在一张专用的圆形网格上，广泛用于射频（RF）、天线和阻抗匹配工作。

## 适用场景 {#when-to-use}

- **射频分析**：呈现阻抗随频率变化的轨迹。
- **匹配网络**：考察设计是在靠近还是远离圆心的匹配点。
- **传输线分析**：在大家熟悉的网格上审视复反射特性。

## 代码示例 {#code-example}

### XAML

```xml
<SmithChart xmlns="https://github.com/avaloniaui" Title="Impedance trace"
                             Height="320"
                             ItemsSource="{Binding ImpedanceData}"
                             ResistancePath="Resistance"
                             ReactancePath="Reactance" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record ImpedancePoint(double Resistance, double Reactance);

public ObservableCollection<ImpedancePoint> ImpedanceData { get; } = new()
{
    new(0.5, -0.3),
    new(0.8, 0.1),
    new(1.2, 0.4)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 阻抗点的集合。 | `null` |
| `ResistancePath` | 指向归一化电阻值的路径。 | `null` |
| `ReactancePath` | 指向归一化电抗值的路径。 | `null` |
| `StrokeThickness` | 所绘轨迹的粗细。 | `2.0` |

## 另请参阅 {#see-also}

- [极坐标图](/controls/data-display/charts/radial/polar-chart)
- [风玫瑰图](/controls/data-display/charts/engineering/wind-rose-chart)
