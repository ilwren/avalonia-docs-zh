---
id: bubble-map-chart
title: 气泡地图
description: 在地理区域上叠加大小成比例的圆，同时呈现位置和数值的量级。
doc-type: reference
tags:
  - avalonia pro
---

import chartsMapsBubble from '/img/controls/charts/charts-maps-bubble.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

气泡地图用大小不等的圆来表示各地理区域上的数值，做法是以 `ShapeMap` 为底，在 `ShapeLayer` 之上叠加一层 `BubbleLayer`。这样一来，位置和数值大小在同一视图中一览无余。

<Image light={chartsMapsBubble} maxWidth={400} position="center" cornerRadius="true" alt="Bubble map overlaying circles of varying sizes on geographic regions to represent city activity levels." />

## 适用场景 {#when-to-use}
- **事件分布**：标出事发地点及其规模（比如地震、促销活动）。
- **城市统计**：比较各座城市的人口或活跃程度。
- **全球指标**：呈现国家级数据，气泡大小即代表数值。

## 代码示例 {#code-example}

### XAML
```xml
<ShapeMap xmlns="https://github.com/avaloniaui" Name="BubbleSample" Title="Major Cities by Population" Height="400" ShowLegend="True" LegendPosition="Bottom">
                        <ShapeMap.Layers>
                            <ShapeLayer GeoJson="{Binding WorldGeoJson}"
                                                 GeoJsonIdPath="ISO_A2"
                                                 LowBrush="#E3F2FD"
                                                 HighBrush="#E3F2FD"
                                                 StrokeThickness="0.3" />
                            <BubbleLayer LatitudePath="Lat"
                                                  LongitudePath="Lon"
                                                  SizePath="Population"
                                                  LabelPath="City"
                                                  MinBubbleSize="6"
                                                  MaxBubbleSize="45"
                                                  Fill="#B4F44336"
                                                  ShowLabels="True"
                                                  ItemsSource="{Binding CityBubbles}">
                                <BubbleLayer.TooltipTemplate>
                                    <DataTemplate>
                                        <StackPanel Spacing="4">
                                            <TextBlock Text="{Binding City}" FontWeight="Bold"/>
                                            <TextBlock Text="{Binding Population, StringFormat='Pop: {0:N1}M'}"/>
                                        </StackPanel>
                                    </DataTemplate>
                                </BubbleLayer.TooltipTemplate>
                            </BubbleLayer>
                        </ShapeMap.Layers>
                    </ShapeMap>
```

### 数据模型（C#） {#data-model-c}

请确保 GeoJSON 文件已包含在项目中，并且运行时可以在指定的相对路径下找到它。

```csharp
using System.IO;

public record CityData(string City, double Lat, double Lon, double Population);

public string WorldGeoJson { get; } =
    File.ReadAllText("Resources/ne_110m_world.geojson");

public CityData[] CityBubbles { get; } = new CityData[]
{
    new("Tokyo", 35.7, 139.7, 37.4),
    new("Delhi", 28.6, 77.2, 32.9),
    new("Shanghai", 31.2, 121.5, 29.2),
    new("São Paulo", -23.5, -46.6, 22.4),
    new("Mexico City", 19.4, -99.1, 21.9),
    new("Cairo", 30.0, 31.2, 21.3),
    new("Mumbai", 19.1, 72.9, 21.0),
    new("Beijing", 39.9, 116.4, 20.9),
    new("New York", 40.7, -74.0, 18.8),
    new("London", 51.5, -0.1, 9.5),
    new("Paris", 48.9, 2.3, 11.1),
    new("Sydney", -33.9, 151.2, 5.4)
};
```

## 公共属性：`ShapeLayer` {#common-properties-shapelayer}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `GeoJson` | GeoJSON 数据。 | `null` |
| `Source` | GeoJSON 数据源的 URI。 | `null` |
| `GeoJsonIdPath` | GeoJSON 数据的唯一 ID。 | `null` |
| `ItemsSource` | 包含地图各区域的数据集合。 | `null` |
| `RegionPath` | 把数据关联到 GeoJSON 坐标的属性。 | `null` |
| `ValuePath` | 把数据关联到区域数值的属性。 | `null` |
| `MinValue` | 颜色归一化的最小值。 | `0.0` |
| `MaxValue` | 颜色归一化的最大值。 | `100.0` |
| `LowBrush` | 代表数据最小值的颜色。 | `#E3F2FD` |
| `HighBrush` | 代表数据最大值的颜色。 | `#1565C0` |
| `Stroke` | 区域轮廓的颜色。 | `null` |
| `StrokeThickness` | 区域轮廓的粗细。 | `0.5` |
| `ShowLabels` | 是否在区域上显示标签。 | `false` |
| `LabelPath` | 标签文本的路径。 | `null` |
| `LabelForeground` | 区域标签所用的画刷。 | `null` |
| `SelectionMode` | 区域的选择模式。可用 `None`、`Single`、`SingleDeselect` 或 `Multiple`。 | `None` |
| `SelectionBrush` | 选中区域的颜色。 | `#FFC107` |
| `SelectionStroke` | 选中区域轮廓的颜色。 | `null` |
| `SelectionStrokeThickness` | 选中区域轮廓的粗细。 | `2.0` |
| `SelectedItem` | 当前选中的区域。 | `null` |
| `HoverBrush` | 区域被悬停时所用的画刷。 | `White`，不透明度 30% |

## 公共属性：`BubbleLayer` {#common-properties-bubblelayer}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 气泡的数据源。 | `null` |
| `LatitudePath` | 纬度坐标所对应的属性路径。 | `null` |
| `LongitudePath` | 经度坐标所对应的属性路径。 | `null` |
| `SizePath` | 气泡的大小。 | `null` |
| `PointBrushPath` | 可选的属性路径，为每个气泡提供画刷或颜色。 | `null` |
| `ShowLabels` | 是否在气泡上显示标签。 | `true` |
| `LabelPath` | 标签的内容。 | `null` |
| `MinBubbleSize` | 气泡最小半径。 | `8.0` |
| `MaxBubbleSize` | 气泡最大半径。 | `40.0` |
| `Fill` | 气泡的颜色。 | `null` |
| `Stroke` | 气泡轮廓的颜色。 | `null` |
