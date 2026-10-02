---
id: kagi-chart
title: 卡吉图
description: 不依赖时间轴，用竖线追踪价格走势，只有当价格超过设定的反转幅度时才改变方向。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFinancialKagi from '/img/controls/charts/charts-financial-kagi.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

卡吉图（Kagi）不依赖时间轴，用竖线追踪价格走势。只有当价格达到一定的反转幅度时，它才改变方向（以及线条粗细）。

<Image light={chartsFinancialKagi} maxWidth={400} position="center" cornerRadius="true" alt="Kagi chart with thick and thin vertical lines changing direction only when price reverses by a set amount." />

## 适用场景 {#when-to-use}
- **纯粹的价格行为**：只盯价格变化，不理会时间和成交量。
- **突破辨识**：借助「阳线」（粗）和「阴线」（细）发现反转。
- **跟随趋势**：滤掉那些没达到反转阈值的小幅波动。

## 代码示例 {#code-example}

### XAML
```xml
<KagiChart xmlns="https://github.com/avaloniaui" Name="KagiChartSample" Title="Trend Reversal" Height="300"
                                        ReversalAmount="4"
                                        ItemsSource="{Binding KagiData}"
                                        ValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}
```csharp
using System;

public record KagiPoint(double Value);

public ObservableCollection<KagiPoint> KagiData { get; } = new(CreateKagiData());

private static IEnumerable<KagiPoint> CreateKagiData()
{
    var price = 100.0;
    var random = new Random(123);

    for (var i = 0; i < 100; i++)
    {
        price += (random.NextDouble() - 0.5) * 4;
        yield return new KagiPoint(price);
    }
}
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 原始价格点的集合。 | `null` |
| `ValuePath` | 表示价格的属性。 | `null` |
| `ReversalAmount`| 触发方向翻转所需的最小价格变动。 | `1.0` |
| `YangBrush` | 阳线段所用的画刷。（涨破前高） | `Green` |
| `YinBrush` | 阴线段所用的画刷。（跌破前低） | `Red` |
| `StrokeThickness` | 基础线条粗细。 | `2.0` |
