---
id: bubble-chart
title: 气泡图
description: 像散点图一样绘制 X、Y 值，再用气泡大小表示第三个数值。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

气泡图在 `CartesianChart` 中使用 `BubbleSeries` 来绘制两个数值维度，每个标记点的大小则由第三个指标决定。

## 适用场景 {#when-to-use}

- **三变量对比**：在一张图里同时呈现 X、Y 和量级之间的关系。
- **投资组合分析**：同时比较价格、利润率和成交量。
- **机会地图**：既靠位置、也靠大小把异常值凸显出来。

## 代码示例 {#code-example}

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Title="Product portfolio" Height="300">
    <CartesianChart.HorizontalAxis>
        <NumericalAxis Title="Price" />
    </CartesianChart.HorizontalAxis>
    <CartesianChart.VerticalAxis>
        <NumericalAxis Title="Revenue" />
    </CartesianChart.VerticalAxis>
    <CartesianChart.Series>
        <BubbleSeries ItemsSource="{Binding BubbleData}"
                               CategoryPath="Price"
                               ValuePath="Revenue"
                               SizePath="Units"
                               Title="Products" />
    </CartesianChart.Series>
</CartesianChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
public record ProductBubble(double Price, double Revenue, double Units);

public ObservableCollection<ProductBubble> BubbleData { get; } = new()
{
    new(15, 120, 40),
    new(22, 180, 65),
    new(30, 140, 25)
};
```

## 常用属性（`BubbleSeries`） {#common-properties-bubbleseries}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 数据点集合。 | `null` |
| `CategoryPath` | 指向 X 轴数值的路径。 | `null` |
| `ValuePath` | 指向 Y 轴数值的路径。 | `null` |
| `SizePath` | 指向决定气泡大小那个数值的路径。 | `null` |
| `MinBubbleSize` | 气泡最小直径，单位为像素。 | `10.0` |
| `MaxBubbleSize` | 气泡最大直径，单位为像素。 | `50.0` |
| `Fill` | 气泡所用的画刷。 | Theme-dependent |
| `Stroke` | 气泡轮廓所用的画刷。 | Theme-dependent |

## 另请参阅 {#see-also}

- [散点图](/controls/data-display/charts/cartesian/scatter-chart)
- [紧凑气泡图](/controls/data-display/charts/bubble/packed-bubble-chart)
