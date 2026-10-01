---
id: carpet-plot-chart
title: 地毯图
description: 把两个自变量和一个因变量映射到一张倾斜的网格上，适合呈现工程上的权衡曲面。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

地毯图画出一张由等值线交织而成的扭曲网格，借此呈现两个自变量与第三个数值之间的关系。

## 适用场景 {#when-to-use}

- **工程权衡**：把两个设计输入与结果曲面放在一起比较。
- **性能图谱**：呈现效率、压力或温度的工作区间。
- **多变量分析**：考察那些用普通笛卡尔折线图说不清的关系。

## 代码示例 {#code-example}

### XAML

```xml
<CarpetPlot xmlns="https://github.com/avaloniaui" Title="Performance map"
                             Height="320"
                             ItemsSource="{Binding CarpetData}"
                             AAxisPath="Speed"
                             BAxisPath="Load"
                             YAxisPath="Efficiency" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record CarpetPoint(double Speed, double Load, double Efficiency);

public ObservableCollection<CarpetPoint> CarpetData { get; } = new()
{
    new(1000, 20, 62),
    new(1000, 40, 68),
    new(1500, 20, 70),
    new(1500, 40, 74)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 测量点的集合。 | `null` |
| `AAxisPath` | 指向第一个自变量的路径。 | `null` |
| `BAxisPath` | 指向第二个自变量的路径。 | `null` |
| `YAxisPath` | 指向因变量数值的路径。 | `null` |
| `CarpetOffset` | 用于营造地毯效果的视觉偏移系数。 | `0.5` |
| `PlotAreaBackground` | 绘图区可选的背景画刷。 | `null` |

## 另请参阅 {#see-also}

- [三元图](/controls/data-display/charts/engineering/ternary-chart)
- [等值线图](/controls/data-display/charts/statistical/contour-plot-chart)
