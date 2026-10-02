---
id: ternary-chart
title: 三元图
description: 绘制三者之和恒定的三元组成，适合呈现混合配比、资源分配和三方平衡。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

三元图呈现三组分混合物，图中每个点代表 A、B、C 三者各自所占的比重。

## 适用场景 {#when-to-use}

- **配比分析**：呈现混合料、材料成分或资源分配的构成。
- **三方平衡**：比较那些加起来恒为整体的几个比例。
- **科学分类**：把样本定位到三角形的决策空间中。

## 代码示例 {#code-example}

### XAML

```xml
<TernaryChart xmlns="https://github.com/avaloniaui" Title="Mixture composition"
                               Height="320"
                               ItemsSource="{Binding TernaryData}"
                               APath="Sand"
                               BPath="Silt"
                               CPath="Clay"
                               ALabel="Sand"
                               BLabel="Silt"
                               CLabel="Clay" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public record TernaryPoint(double Sand, double Silt, double Clay);

public ObservableCollection<TernaryPoint> TernaryData { get; } = new()
{
    new(60, 25, 15),
    new(35, 45, 20),
    new(20, 30, 50)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 三元数据点的集合。 | `null` |
| `APath` | 指向第一个组分数值的路径。 | `null` |
| `BPath` | 指向第二个组分数值的路径。 | `null` |
| `CPath` | 指向第三个组分数值的路径。 | `null` |
| `ALabel` | A 轴的标签。 | `null` |
| `BLabel` | B 轴的标签。 | `null` |
| `CLabel` | C 轴的标签。 | `null` |
| `ShowGridLines` | 是否绘制三元网格。 | `true` |
| `DotSize` | 所绘数据点的半径。 | `5.0` |

## 另请参阅 {#see-also}

- [地毯图](/controls/data-display/charts/engineering/carpet-plot-chart)
- [平行坐标图](/controls/data-display/charts/statistical/parallel-coordinates-chart)
