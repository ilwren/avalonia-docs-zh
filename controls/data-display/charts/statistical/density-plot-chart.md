---
id: density-plot-chart
title: 密度图
description: 用核密度估计绘出平滑的分布曲线，曲线下方可选填充。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

密度图把数值分布平滑成一条连续曲线，相比原始的散点列表，峰值和离散程度看得更清楚。

## 适用场景 {#when-to-use}

- **分布形态**：考察数据的集中程度、偏态以及是否多峰。
- **更平滑的直方图**：讲同一个故事，但用的是连续曲线。
- **抽样对比**：不必把每个点都画出来，也能呈现数据集的整体形态。

## 代码示例 {#code-example}

### XAML

```xml
<DensityPlotChart xmlns="https://github.com/avaloniaui" Title="Response time density"
                                   Height="300"
                                   ItemsSource="{Binding DensityData}"
                                   ValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record Measurement(double Value);

public ObservableCollection<Measurement> DensityData { get; } = new()
{
    new(12),
    new(15),
    new(18),
    new(19),
    new(24)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 数值样本的集合。 | `null` |
| `ValuePath` | 指向数值样本的路径。 | `null` |
| `Bandwidth` | 核函数带宽。设为 `0.0` 时自动计算。 | `0.0` |
| `FillOpacity` | 曲线下方填充区域的不透明度。 | `0.3` |
| `ShowArea` | 是否填充曲线下方的区域。 | `true` |
| `ShowGridLines` | 是否绘制背景网格线。 | `true` |
| `Stroke` | 密度曲线所用的画刷。 | `null` |

## 另请参阅 {#see-also}

- [直方图](/controls/data-display/charts/cartesian/histogram-chart)
- [小提琴图](/controls/data-display/charts/statistical/violin-plot-chart)
