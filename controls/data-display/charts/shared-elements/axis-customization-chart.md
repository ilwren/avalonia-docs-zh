---
id: axis-customization-chart
title: 坐标轴定制
description: 定制图表坐标轴：标签旋转、轴线与刻度样式、网格线、多坐标轴，以及数值、类别、日期和对数等轴类型。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFeaturesGridlines from '/img/controls/charts/charts-gridlines-customization.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Avalonia Charts 允许你定制坐标轴的外观，包括标签排布、轴线样式、刻度线、网格线配置，以及多坐标轴支持。

<Image light={chartsFeaturesGridlines} maxWidth={400} position="center" cornerRadius="true" alt="Cartesian chart with customized axes showing gridlines." />

## 适用场景 {#when-to-use}

- **多套刻度**：需要在同一张图上展示两项不同指标时（比如温度和湿度）。
- **分类数据**：坐标轴表示的是一个个离散分组，而非连续数值时。
- **时间序列分析**：为历史数据定制日期格式和刻度间隔。

## 代码示例 {#code-example}

### XAML

```xml
<CartesianChart xmlns="https://github.com/avaloniaui" Name="GridLinesChart" Title="Dashed Major Grid Lines" Height="300">
                        <CartesianChart.HorizontalAxis>
                            <CategoryAxis ShowGridLines="True" GridLineBrush="#BBDEFB" GridLineStrokeThickness="2">
                                <CategoryAxis.GridLineDashStyle>
                                    <DashStyle Dashes="5,5"/>
                                </CategoryAxis.GridLineDashStyle>
                            </CategoryAxis>
                        </CartesianChart.HorizontalAxis>
                        <CartesianChart.VerticalAxis>
                            <NumericalAxis ShowGridLines="True" GridLineBrush="#C8E6C9" GridLineStrokeThickness="2">
                                <NumericalAxis.GridLineDashStyle>
                                    <DashStyle Dashes="10,5"/>
                                </NumericalAxis.GridLineDashStyle>
                            </NumericalAxis>
                        </CartesianChart.VerticalAxis>
                        <CartesianChart.Series>
                            <AreaSeries Title="Data" ItemsSource="{Binding SalesData}" Fill="#7E2196F3" Stroke="#2196F3" />
                        </CartesianChart.Series>
                    </CartesianChart>
```

### 数据模型（C#） {#data-model-c}

```csharp
public ObservableCollection<int> SalesData { get; } = new() { 35, 28, 34, 32, 40, 32, 35 };
```

## 坐标轴公共属性（`NumericalAxis` / `CategoryAxis`） {#common-axis-properties-numericalaxis-categoryaxis}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 坐标轴的文字标题。 | `null` |
| `IsVisible` | 开关整条坐标轴的可见性。 | `true` |
| `TitleFontSize` | 坐标轴标题所用的字号。 | `14.0` |
| `TitleForeground` | 坐标轴标题所用的画刷。 | `null` |
| `ShowLabels` | 是否绘制坐标轴标签。 | `true` |
| `LabelFontSize` | 坐标轴标签所用的字号。 | `12.0` |
| `LabelForeground` | 坐标轴标签所用的画刷。 | `null` |
| `ShowAxisLine` | 是否绘制轴线。 | `true` |
| `AxisLineStroke` | 轴线所用的画刷。为 `null` 时，采用图表的坐标轴画刷。 | `null` |
| `AxisLineStrokeThickness` | 轴线的粗细。 | `1.0` |
| `AxisLineDashStyle` | 轴线的虚线样式。 | `null` |
| `ShowTickLines` | 是否在标签位置绘制刻度线。 | `false` |
| `TickLineLength` | 刻度线的长度，单位为像素。 | `5.0` |
| `TickLineStroke` | 刻度线所用的画刷。为 `null` 时，采用图表的坐标轴画刷。 | `null` |
| `TickLineStrokeThickness` | 刻度线的粗细。 | `1.0` |
| `ShowGridLines` | 显示/隐藏主网格线。 | `true` |
| `ShowMinorGridLines` | 显示/隐藏次网格线。 | `false` |
| `GridLineBrush` | 主网格线所用的画刷。 | `null` |
| `GridLineStrokeThickness` | 主网格线的粗细。 | `1.0` |
| `GridLineDashStyle` | 主网格线的虚线样式。 | `null` |
| `GridLineCap` | 主网格线的线端样式。 | `Flat` |
| `GridLineJoin` | 主网格线的拐角连接样式。 | `Miter` |
| `MinorGridLineBrush` | 次网格线所用的画刷。 | `null` |
| `MinorGridLineStrokeThickness` | 次网格线的粗细。 | `0.5` |
| `MinorGridLineDashStyle` | 次网格线的虚线样式。 | `null` |
| `MinorGridLineCap` | 次网格线的线端样式。 | `Flat` |
| `MinorGridLineJoin` | 次网格线的拐角连接样式。 | `Miter` |
| `LabelFormat` | 标签所用的格式字符串（比如「C0」「N2」「yyyy」）。 | `null` |
| `LabelRotation` | `LabelFitMode` 为 `CustomRotation` 时所采用的自定义旋转角度。 | `0.0` |
| `MinorTickCount` | 两个主刻度之间次刻度的区间数。 | `4` |
| `LabelFitMode` | 标签摆不下时所采取的策略。可选值有 `None`、`Hide`、`Wrap`、`MultipleRows`、`Rotate45`、`Rotate90`、`CustomRotation` 和 `Auto`。 | `None` |

## 坐标轴类型 {#axis-types}

| 坐标轴 | 说明 | 适用于 |
| --- | --- | --- |
| `NumericalAxis` | 连续的数值数据。 | `Minimum`, `Maximum`, `MajorStep`, `MinorStep`, `ScaleBreaks` |
| `CategoryAxis` | 离散的类别。 | `GapLength`, `PlotMode` |
| `DateTimeAxis` | 日期和时间数据。 | `Minimum`, `Maximum`, `MajorStep`, `MajorStepUnit`, `DateFormat` |
| `LogarithmicAxis` | 跨度很大的数据。 | `Minimum`, `Maximum`, `LogBase`, `MajorStep` |

## 刻度断裂 {#scale-breaks}

在 XAML 中内联定义刻度断裂可用 `NumericalAxis.ScaleBreaks`，从视图模型绑定集合则用 `ScaleBreaksSource`。刻度断裂会跳过那些原本会把可见数据挤扁的区间。每个 `ScaleBreak` 定义一段被略去的取值范围，并可设置断裂标记的样式。`End <= Start` 这类无效区间会被忽略，相互重叠或首尾相接的断裂则会先合并，再对坐标轴范围作归一化。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Start` | 被跳过的轴区间的起始值。 | `0.0` |
| `End` | 被跳过的轴区间的结束值。 | `0.0` |
| `Stroke` | 绘制刻度断裂标记所用的画刷。 | `null` |
| `StrokeThickness` | 刻度断裂标记的粗细。 | `1.0` |

## 各类坐标轴的专有属性 {#axis-specific-properties}

| 坐标轴 | 属性 | 说明 | 默认值 |
| :--- | :--- | :--- | :--- |
| `NumericalAxis` | `Minimum` | 明确指定的最小值。为 `null` 时，由图表根据数据自行计算。 | `null` |
| `NumericalAxis` | `Maximum` | 明确指定的最大值。为 `null` 时，由图表根据数据自行计算。 | `null` |
| `NumericalAxis` | `MajorStep` | 主刻度间隔。无效或非正的取值会退回自动步长。 | `null` |
| `NumericalAxis` | `MinorStep` | 次刻度间隔。 | `null` |
| `NumericalAxis` | `ScaleBreaks` | 内联的刻度断裂集合。 | 空集合 |
| `NumericalAxis` | `ScaleBreaksSource` | 设置后将取代 `ScaleBreaks` 的绑定集合。 | `null` |
| `DateTimeAxis` | `Minimum` | 明确指定的起始日期。为 `null` 时，由图表根据数据自行计算。 | `null` |
| `DateTimeAxis` | `Maximum` | 明确指定的结束日期。为 `null` 时，由图表根据数据自行计算。 | `null` |
| `DateTimeAxis` | `MajorStep` | 与 `MajorStepUnit` 搭配使用的主刻度间隔。按月和按年的步长会取整到整数单位。 | `1.0` |
| `DateTimeAxis` | `MajorStepUnit` | `MajorStep` 所用的单位：`Second`、`Minute`、`Hour`、`Day`、`Week`、`Month` 或 `Year`。 | `Day` |
| `DateTimeAxis` | `DateFormat` | 可选的日期标签格式字符串。 | `null` |
| `LogarithmicAxis` | `Minimum` | 明确指定的最小正值。为 `null` 时，由图表根据数据自行计算。 | `null` |
| `LogarithmicAxis` | `Maximum` | 明确指定的最大正值。为 `null` 时，由图表根据数据自行计算。 | `null` |
| `LogarithmicAxis` | `LogBase` | 坐标轴刻度所用的对数底。 | `10.0` |
| `LogarithmicAxis` | `MajorStep` | 主刻度的倍率。为 `null` 时，由坐标轴根据 `LogBase` 自行计算。 | `null` |

## 连续横轴 {#continuous-horizontal-axes}

`CartesianChart` 可以把支持的系列绘制在连续的横向 `NumericalAxis`、`LogarithmicAxis` 或 `DateTimeAxis` 上。只有当每一个可见且非空的系列都支持连续布局、且各横向类别值都能转换成所选的轴类型时，图表才会采用连续横向布局。

支持的笛卡尔系列包括 `LineSeries`、`SplineSeries`、`StepLineSeries`、`AreaSeries`、`SplineAreaSeries`、`AreaRangeSeries`、`ScatterSeries`、`ScatterLineSeries`、`BubbleSeries` 和 `ErrorBarSeries`。`ChartTrendlineSeries` 和 `MovingAverageSeries` 在设置了 `SourceSeries` 时，兼容性随其所属对象而定。

对 `DateTimeAxis` 而言，`CategoryPath` 的取值必须能解析为 `DateTime` 或 `DateTimeOffset`；对 `NumericalAxis` 和 `LogarithmicAxis` 而言，取值必须能解析为有限数值；`LogarithmicAxis` 则要求取值大于 `0`。

只要有一个可见且非空的系列不兼容，图表就会改用类别布局来排布横轴。

## 绘图带 {#plot-bands}

用 `ChartAxis.PlotBands` 可以为横轴或纵轴上的某段区间铺底色。在类别轴上，横轴绘图带的 `Start` 和 `End` 取类别索引；在连续横轴上，则取该轴的值域。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Start` | 阴影区间的起始值。为 `NaN` 时，色带从坐标轴起点开始。 | `NaN` |
| `End` | 阴影区间的结束值。为 `NaN` 时，色带延伸到坐标轴终点。 | `NaN` |
| `Fill` | 填充色带所用的画刷。 | `null` |
| `Stroke` | 色带边框所用的画刷。 | `null` |
| `StrokeThickness` | 色带边框的粗细。 | `0.0` |
| `Opacity` | 色带填充所用的不透明度。 | `0.3` |
| `Text` | 绘制在色带内部的可选文字。 | `null` |
| `Foreground` | 绘图带文字所用的画刷。 | `null` |
| `TextFontSize` | 绘图带文字所用的字号。 | `12.0` |
| `HorizontalTextAlignment` | 文字在色带内的水平对齐方式：`Start`、`Center` 或 `End`。 | `Center` |
| `VerticalTextAlignment` | 文字在色带内的垂直对齐方式：`Start`、`Center` 或 `End`。 | `Center` |
| `IsVisible` | 是否渲染该绘图带。 | `true` |
| `IsRepeating` | 色带是否按固定的坐标轴间隔重复出现。 | `false` |
| `RepeatEvery` | 重复色带之间的坐标轴间隔。启用重复却给了无效取值时，会被置为 `1.0`。 | `NaN` |
| `RepeatUntil` | 重复色带到此坐标轴取值为止。 | `NaN` |
| `RenderAboveSeries` | 是把色带绘制在图表系列之上，而非之后。 | `false` |

## 另请参阅 {#see-also}

- [组合图](/controls/data-display/charts/cartesian/combo-chart)
- [折线图](/controls/data-display/charts/cartesian/line-chart)
