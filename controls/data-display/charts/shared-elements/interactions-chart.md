---
id: interactions-chart
title: 交互
description: 让用户在数据密集或可交互的图表中缩放、平移、选择、悬停高亮，并借助轨迹球参考线读取数值。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFeaturesZoom from '/img/controls/charts/charts-zoom.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

图表交互让用户可以通过缩放、平移、选择、悬停高亮和轨迹球查看等方式动态探索数据。

<Image light={chartsFeaturesZoom} maxWidth={400} position="center" cornerRadius="true" alt="Chart with interactive zoom and pan controls allowing users to focus on specific regions of a dense dataset." />

## 适用场景 {#when-to-use}
- **大数据呈现**：探索含成千上万个点的折线图。
- **深入分析**：放大到某个时间窗口细看。
- **交互式报表**：把主动权交给用户，让他们聚焦自己关心的部分。
- **悬停查看**：把未悬停的元素调暗，让当前的数据点或分段更显眼。

## 代码示例 {#code-example}

### XAML
```xml
<StackPanel Spacing="15">
    <WrapPanel Orientation="Horizontal">
        <Button Content="Back" Margin="0,0,10,10" />
        <Button Content="Reset" Margin="0,0,10,10" />
        <TextBlock Text="Zoom: X=100%, Y=100%"
                   VerticalAlignment="Center"
                   Margin="0,0,20,10" />
        <CheckBox Name="ShowRangeSelectorCheckBox"
                  Content="Show Range Selector"
                  IsChecked="True"
                  VerticalAlignment="Center"
                  Margin="0,0,0,10" />
    </WrapPanel>

    <CartesianChart xmlns="https://github.com/avaloniaui" Name="ChartXY"
                           Height="350"
                           ZoomMode="XY"
                           IsZoomEnabled="True"
                           IsPanEnabled="True"
                           ShowRangeSelector="{Binding #ShowRangeSelectorCheckBox.IsChecked}">
        <CartesianChart.HorizontalAxis>
            <DateTimeAxis LabelFormat="MMM dd" ShowGridLines="True" />
        </CartesianChart.HorizontalAxis>
        <CartesianChart.VerticalAxis>
            <NumericalAxis LabelFormat="N0" ShowGridLines="True" />
        </CartesianChart.VerticalAxis>
        <CartesianChart.Series>
            <LineSeries ItemsSource="{Binding ZoomData}"
                               CategoryPath="Date"
                               ValuePath="Value"
                               Stroke="#FF9800"
                               StrokeThickness="2" />
        </CartesianChart.Series>
    </CartesianChart>

    <Border BorderBrush="{DynamicResource CardBorderBrush}"
            BorderThickness="1"
            CornerRadius="4"
            Background="{DynamicResource CardBackgroundBrush}">
        <ScrollViewer Height="100">
            <StackPanel Spacing="2" Margin="5">
                <TextBlock Text="Interaction Events:"
                           FontWeight="Bold"
                           FontSize="12"
                           Foreground="{DynamicResource AccentBrush}" />
            </StackPanel>
        </ScrollViewer>
    </Border>
</StackPanel>
```

### 数据模型（C#） {#data-model-c}
```csharp
using System;

public class DateTimePoint
{
    public DateTime Date { get; set; }
    public double Value { get; set; }
}

public ObservableCollection<DateTimePoint> ZoomData { get; } = CreateZoomData();

private static ObservableCollection<DateTimePoint> CreateZoomData()
{
    var data = new ObservableCollection<DateTimePoint>();
    var date = new DateTime(2023, 1, 1);
    var random = new Random(42);
    var value = 100.0;

    for (var i = 0; i < 365; i++)
    {
        value += random.NextDouble() * 10 - 4.5;
        value = Math.Max(50, Math.Min(200, value));
        data.Add(new DateTimePoint { Date = date, Value = value });
        date = date.AddDays(1);
    }

    return data;
}
```

## 常用属性 {#common-properties}

### 缩放与平移 {#zoom-and-pan}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `IsZoomEnabled` | 启用图表的缩放能力。 | `false` |
| `IsPanEnabled` | 启用图表视图的平移（滚动）能力。 | `false` |
| `ZoomMode` | 沿 `X`、`Y` 或 `XY` 轴缩放。 | `XY` |
| `ZoomSensitivity` | 鼠标滚轮缩放的灵敏度，取非负值。`0` 表示禁用滚轮缩放；无效取值会被强制为 `0`。 | `0.1` |
| `ShowRangeSelector` | 显示一个区间选择器控件，用于缩放。 | `true` |
| `ZoomHistoryLimit` | 为「回退上一视图」保留的视口状态上限。设为 `0` 则保留全部已入栈的状态。 | `20` |
| `CanGoBackZoom` | 只读状态，指示 `GoBackZoom()` 能否恢复到上一个视口。 | `false` |

### 区间选择器 {#range-selector}

当 `IsZoomEnabled`、`ShowRangeSelector` 和当前的 `ZoomMode` 有此需要时，`CartesianChart` 会创建内嵌的 `ChartRangeSelector` 控件。若需要一块独立的区间选择区域，请直接使用 `ChartRangeSelector`。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Orientation` | 选择器的方向，`Horizontal` 或 `Vertical`。 | `Horizontal` |
| `Minimum` | 选择器所表示的数据最小值。 | `0.0` |
| `Maximum` | 选择器所表示的数据最大值。 | `100.0` |
| `SelectedMinimum` | 所选区间的起始值。该属性默认双向绑定。 | `0.0` |
| `SelectedMaximum` | 所选区间的结束值。该属性默认双向绑定。 | `100.0` |
| `GripSize` | 可拖动区间手柄的大小，单位为像素。 | `24.0` |
| `PlotAreaOffset` | 用于把选择器轨道对齐到图表绘图区的偏移量。 | `0.0` |
| `SmallChange` | 键盘操作的步进量。 | `1.0` |
| `KeyboardStepRatio` | 设置了比例转换器时，键盘在归一化选择器空间中可选的移动步长。`1.0` 代表整条轨道的长度。未设置时，键盘移动采用 `SmallChange`。 | `null` |
| `ValueToRatio` | 可选的转换器，把数据值换算成归一化的选择器位置。用于非线性坐标轴和刻度断裂。 | `null` |
| `RatioToValue` | 可选的转换器，把归一化的选择器位置换算回数据值。 | `null` |

| 事件 | 说明 |
| :--- | :--- |
| `RangeDragStarted` | 用户开始拖动选择器滑块或手柄时触发。 |
| `RangeDragCompleted` | 当前这次区间拖动结束时触发。 |

### 悬停高亮 {#hover-highlighting}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `IsHighlightEnabled` | 启用悬停高亮。在系列上，悬停某个数据点会把同系列的其他元素调暗；在支持此特性的独立图表上，悬停某个分段或单元格会把该图表中的其他元素调暗。 | `false` |

支持该特性的独立图表包括 `BubbleCloud`、`PackedBubbleChart`、`NightingaleRoseChart`、`RadialBarChart`、`SemiDonutChart`、`SunburstChart`、对比类图表、漏斗图、网格类图表、`TreeMapChart`、`FinancialChart`、`PolarAreaChart`、`PolarChart` 和 `RadarChart`。

### Trackball

指针在绘图区上移动时，`CartesianChart` 可以显示一条轨迹球参考线以及数值工具提示。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `TrackballMode` | 轨迹球参考线模式：`None`、`Vertical` 或 `Horizontal`。 | `None` |
| `TrackballDisplayMode` | 工具提示的显示模式：`FloatAllPoints` 或 `GroupAllPoints`。 | `FloatAllPoints` |
| `TrackballLineStroke` | 轨迹球参考线所用的画刷。为 `null` 时，使用 `DimGray`。 | `null` |
| `TrackballLineStrokeThickness` | 轨迹球参考线的粗细。 | `1.0` |

### Selection

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `IsSelectionEnabled` | 为支持的系列或图表元素启用指针选择。 | `false` |
| `SelectionMode` | 选择行为，比如 `None`、`Single`、`SingleDeselect` 或 `Multiple`。 | `SingleDeselect` |
| `SelectedIndex` | 主选中项的索引，双向绑定；未选中任何项时为 `-1`。 | `-1` |
| `SelectedIndexes` | 多选场景下选中索引的只读快照。 | 空集合 |
| `SelectionBrush` | 选中项所用的画刷。 | `#314A6E` |
| `SelectionStroke` | 选中项可选的轮廓画刷。 | `null` |
| `SelectionStrokeThickness` | 选中项的轮廓粗细。 | `2.0` |

可选择的图表控件和系列都提供选择相关的 API。`SelectionChanging` 在选择生效之前触发，可以在事件数据中改写，也可以直接取消。`SelectionChanged` 则在选择真正变更之后触发。

### 事件与方法 {#events-and-methods}

| 成员 | 说明 |
| :--- | :--- |
| `DataPointClicked` | 数据点被点击时触发。事件数据会提供 `Series`、`DataPointIndex`、`Category`、`Value`，以及原始的 `DataItem`（如果有）。 |
| `DataPointHovered` | 指针移到某个数据点上或离开所有数据点后，经防抖延迟触发。该事件不依赖 `IsHighlightEnabled`——那个属性只控制高亮效果。事件数据提供 `Source` 和 `DataPointIndex`。 |
| `GoBackZoom()` | 恢复到上一个缩放视口；若确实套用了一条历史记录，则返回 `true`。 |
| `ResetZoom()` | 清除当前视口和缩放历史。 |
| `ClearSelection()` | 清除可选择的图表、系列或图层上的当前选择。 |
| `TrySelectDataPoint(index)` | 在可选择的图表或系列上按索引尝试选中某个数据点。 |
| `IsDataPointSelected(index)` | 返回指定索引的数据点当前是否处于选中状态。 |
| `TrySelectItem(item)` | 在 `ShapeLayer` 这类按项选择的控件上尝试选中某个数据项。 |
| `IsItemSelected(item)` | 返回按项选择的控件上某个数据项是否被选中。 |
| `SelectionChanging` | 选择变更之前触发。事件数据提供可改写的 `NewSelection` 和 `NewIndexes`、变更前的 `OldSelection` 和 `OldIndexes`，以及 `Cancel`。 |
| `SelectionChanged` | 选择变更之后触发。事件数据提供 `NewSelection`、`OldSelection`、`NewIndexes` 和 `OldIndexes` 的快照。 |
| `ZoomChanged` | 缩放视口变化时触发。事件数据提供 `Axis`、变更前后的缩放倍数、变更前后的缩放位置，以及可见视口的范围。 |
| `ZoomReset` | 缩放被重置后触发。事件数据提供先前的视口范围和先前的缩放倍数。 |
| `SeriesAdded` | 由 `CartesianChart` 在某个系列被加入其 `Series` 集合后触发。 |
| `SeriesRemoved` | 由 `CartesianChart` 在某个系列从其 `Series` 集合移除后触发。 |

## 交互操作方式 {#interaction-controls}
- **鼠标滚轮**：以光标位置为中心放大/缩小。
- **Ctrl + 拖动**：在图表区内平移。
- **Shift + 拖动**：框选一个矩形，放大到该区域。
- **悬停**：当 `IsHighlightEnabled` 为 `true` 时，高亮当前的数据点或分段。
- **双击**：把缩放和平移重置回默认视图。

图表还支持双指捏合缩放、滚轮缩放和框选缩放。

## 另请参阅 {#see-also}

- [Tooltip](/controls/data-display/charts/shared-elements/tooltip-chart)
- [Crosshairs](/controls/data-display/charts/shared-elements/crosshairs-chart)
- [坐标轴定制](/controls/data-display/charts/shared-elements/axis-customization-chart)
