---
id: parliament-chart
title: 议席图
description: 以半圆形版面呈现议席分布，适合表现议会构成和比例代表制结果。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

议席图把座位排成半圆，于是各党派的席位既能看出总数，也能看出空间上的分量对比。

## 适用场景 {#when-to-use}

- **议会构成**：按党派或阵营展示议席分布。
- **董事会构成**：呈现委员会或理事会的成员构成。
- **按比例分配**：用大家熟悉的半圆版面呈现席位分配结果。

## 代码示例 {#code-example}

### XAML

```xml
<ParliamentChart xmlns="https://github.com/avaloniaui" Title="Parliament seats"
                                  Height="320"
                                  TotalSeats="120"
                                  Parties="{Binding Parties}" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public ObservableCollection<ParliamentParty> Parties { get; } = new()
{
    new() { Name = "Alliance", Seats = 46, Color = Colors.SteelBlue },
    new() { Name = "Coalition", Seats = 38, Color = Colors.OrangeRed },
    new() { Name = "Green", Seats = 22, Color = Colors.ForestGreen },
    new() { Name = "Independent", Seats = 14, Color = Colors.Gray }
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `TotalSeats` | 总共要绘制多少个席位。 | `100` |
| `Rows` | 同心席位圈的层数。 | `4` |
| `InnerRadiusFactor` | 半圆的内半径系数。 | `0.4` |
| `SeatGap` | 席位之间的间隙。 | `2.0` |
| `StartAngle` | 半圆左端的起始角度，单位为度。 | `180.0` |
| `EndAngle` | 半圆右端的结束角度，单位为度。 | `0.0` |
| `Parties` | 定义席位分配的 `ParliamentParty` 项集合。 | `null` |

## 常用属性（`ParliamentParty`） {#common-properties-parliamentparty}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Name` | 党派或阵营名称。 | `string.Empty` |
| `Seats` | 分配给该党派的席位数。 | `0` |
| `Color` | 绘制该党派席位所用的颜色。 | `Gray` |

## 另请参阅 {#see-also}

- [饼图](/controls/data-display/charts/circular/pie-chart)
- [Mekko 图](/controls/data-display/charts/comparison/mekko-chart)
