---
id: tornado-chart
title: 龙卷风图
description: 以中线为轴向左右绘制双向横条，常用于敏感性分析和带排名的对比。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

龙卷风图把左右两侧的条形排布在同一条中线两旁，带排名的并排差异因而一目了然。

## 适用场景 {#when-to-use}

- **敏感性分析**：排出哪些变量把结果往左或往右推得最多。
- **情景对比**：在相同类别上比较两个相对的数值。
- **优先级梳理**：先盯住绝对差异最大的那几项。

## 代码示例 {#code-example}

### XAML

```xml
<TornadoChart xmlns="https://github.com/avaloniaui" Title="Sensitivity drivers"
                       Height="320"
                       ItemsSource="{Binding TornadoData}"
                       LabelPath="Factor"
                       LeftValuePath="Downside"
                       RightValuePath="Upside" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record TornadoFactor(string Factor, double Downside, double Upside);

public ObservableCollection<TornadoFactor> TornadoData { get; } = new()
{
    new("Demand", 18, 26),
    new("Price", 12, 20),
    new("Costs", 22, 14)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 各因素或类别的集合。 | `null` |
| `LeftValuePath` | 指向左侧数值的路径。 | `null` |
| `RightValuePath` | 指向右侧数值的路径。 | `null` |
| `LabelPath` | 指向类别标签的路径。 | `null` |
| `LeftBrush` | 左侧条形所用的画刷。 | `#E91E63` |
| `RightBrush` | 右侧条形所用的画刷。 | `#2196F3` |
| `BarHeight` | 条形高度，以行高的比例表示。 | `0.7` |
| `CenterGap` | 两侧之间的间隙。 | `4.0` |
| `IsHighlightEnabled` | 为龙卷风条形启用悬停高亮。 | `false` |

## 另请参阅 {#see-also}

- [镜像条形图](/controls/data-display/charts/comparison/mirror-bar-chart)
- [人口金字塔图](/controls/data-display/charts/comparison/population-pyramid-chart)
