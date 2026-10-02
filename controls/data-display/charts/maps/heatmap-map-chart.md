---
id: heatmap-map-chart
title: 热力地图
description: 用颜色渐变呈现各地理坐标上的数据密度，最适合在地图上标出活跃热点和聚集区域。
doc-type: reference
tags:
  - avalonia pro
---

import chartsMapsHeatmap from '/img/controls/charts/charts-maps-gradient.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

热力地图用带 `HeatmapLayer` 的 `ShapeMap` 来呈现各地理坐标上的数据密度。要标出活动聚集的热点，用它很合适。

<Image light={chartsMapsHeatmap} maxWidth={400} position="center" cornerRadius="true" alt="Geographic heatmap using a color gradient to show data density hot spots and concentration areas across regions." />

## 适用场景 {#when-to-use}
- **用户活跃度**：呈现手机应用用户在地理上最活跃的区域。
- **事件上报**：标出犯罪、交通事故或断网故障的热点区域。
- **环境密度**：呈现物种或污染物的聚集情况。

## 代码示例 {#code-example}

### XAML
```xml
<ShapeMap xmlns="https://github.com/avaloniaui" Name="HeatmapSample" Title="Global Earthquake Activity" Height="400" ShowLegend="False">
                        <ShapeMap.Layers>
                            <ShapeLayer GeoJson="{Binding WorldGeoJson}"
                                                 GeoJsonIdPath="ISO_A2"
                                                 LowBrush="#F5F5F5"
                                                 HighBrush="#F5F5F5"
                                                 Stroke="#E0E0E0"
                                                 StrokeThickness="0.3" />
                            <HeatmapLayer LatitudePath="Lat"
                                                   LongitudePath="Lon"
                                                   IntensityPath="Magnitude"
                                                   MaxIntensity="9.0"
                                                   Radius="50"
                                                   LowBrush="#4000FF00"
                                                   MediumBrush="#CCFFFF00"
                                                   HighBrush="#FFFF0000"
                                                   ItemsSource="{Binding EarthquakeData}">
                                <HeatmapLayer.TooltipTemplate>
                                    <DataTemplate>
                                        <StackPanel Spacing="4">
                                            <TextBlock Text="Earthquake" FontWeight="Bold"/>
                                            <TextBlock Text="{Binding Magnitude, StringFormat='Magnitude: {0:N1}'}"/>
                                        </StackPanel>
                                    </DataTemplate>
                                </HeatmapLayer.TooltipTemplate>
                            </HeatmapLayer>
                        </ShapeMap.Layers>
                    </ShapeMap>
```

### 数据模型（C#） {#data-model-c}

请确保 GeoJSON 文件已包含在项目中，并且运行时可以在指定的相对路径下找到它。

```csharp
using System.IO;

public record EarthquakeItem(double Lat, double Lon, double Magnitude);

public string WorldGeoJson { get; } =
    File.ReadAllText("Resources/ne_110m_world.geojson");

public EarthquakeItem[] EarthquakeData { get; } = new EarthquakeItem[]
{
    new(38.3, 142.4, 9.1),
    new(35.0, 135.8, 6.9),
    new(34.4, 135.3, 6.1),
    new(3.3, 95.9, 9.1),
    new(-0.8, 99.8, 7.6),
    new(-7.5, 110.4, 6.3),
    new(-36.1, -72.9, 8.8),
    new(-33.4, -70.6, 6.5),
    new(34.2, -118.4, 6.7),
    new(37.9, -122.3, 6.9),
    new(36.2, -120.2, 5.8),
    new(61.3, -149.9, 7.1),
    new(57.8, -152.4, 7.9),
    new(28.2, 84.7, 7.8),
    new(37.2, 37.0, 7.8),
    new(38.0, 38.5, 7.5),
    new(-41.5, 174.8, 6.3),
    new(-42.7, 173.0, 7.8),
    new(42.4, 13.4, 6.2),
    new(15.5, 120.8, 7.7),
    new(19.4, -99.4, 7.1),
    new(33.4, 46.0, 7.3)
};
```

## 常用属性（`HeatmapLayer`） {#common-properties-heatmaplayer}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 要渲染的地理点集合。 | `null` |
| `LatitudePath` | 纬度数值所对应的属性名。 | `Latitude` |
| `LongitudePath` | 经度数值所对应的属性名。 | `Longitude` |
| `IntensityPath` | 强度数值所对应的属性名。 | `Intensity` |
| `Radius` | 每个热点的基准半径，单位为像素。 | `40.0` |
| `MaxIntensity` | 用于归一化的最大强度。 | `100.0` |
| `LowBrush` | 低强度数值所用的画刷。 | `#0000FF00` |
| `MediumBrush` | 中等强度数值所用的画刷。 | `#FFFF00` |
| `HighBrush` | 高强度数值所用的画刷。 | `#FF0000` |
