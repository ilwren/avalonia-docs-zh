---
id: venn-diagram-chart
title: 韦恩图
description: 呈现集合之间的重叠与交集数值，适合比较成员归属和共有部分。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

韦恩图展示各集合如何相互重叠、哪些区域是各自独有的，以及每块交集各占多少。

## 适用场景 {#when-to-use}

- **集合对比**：呈现产品受众、功能或实验之间的重叠。
- **共有成员**：凸显各自独有和彼此交叠的部分。
- **选择式操作**：让用户查看或选中图中的某个区域。

## 代码示例 {#code-example}

### XAML

```xml
<VennDiagramChart xmlns="https://github.com/avaloniaui" Title="Audience overlap"
                                   Height="320"
                                   ItemsSource="{Binding VennItems}"
                                   IsSelectionEnabled="True" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public ObservableCollection<VennItem> VennItems { get; } = new()
{
    new() { Name = "Newsletter", Sets = ["A"], Value = 45 },
    new() { Name = "Webinars", Sets = ["B"], Value = 30 },
    new() { Name = "Customers", Sets = ["A", "B"], Value = 18 }
};
```

## 常用属性（`VennDiagramChart`） {#common-properties-venndiagramchart}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | `VennItem` 区域的集合。 | `null` |
| `IsSelectionEnabled` | 各区域是否可选。 | `false` |
| `SelectionMode` | 选择行为。 | `SingleDeselect` |
| `SelectionBrush` | 选中区域所用的画刷。 | Theme-dependent |
| `SelectionStroke` | 选中区域所用的描边。 | `null` |
| `SelectionStrokeThickness` | 选中区域所用的描边粗细。 | `2.0` |
| `SelectedIndex` | 选中区域的索引；未选中任何区域时为 `-1`。 | `-1` |

## 常用属性（`VennItem`） {#common-properties-vennitem}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Sets` | 集合标识符的集合，比如 `["A"]` 或 `["A", "B"]`。 | 空集合 |
| `Value` | 该集合或交集所代表的数值。 | `0.0` |
| `Name` | 可选的区域标签。 | `null` |
| `Fill` | 该区域可选的填充画刷。 | `null` |

## 另请参阅 {#see-also}

- [圆堆积图](/controls/data-display/charts/hierarchy/circle-packing-chart)
- [议席图](/controls/data-display/charts/comparison/parliament-chart)
