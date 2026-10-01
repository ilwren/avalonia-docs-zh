---
id: choropleth-map-chart
title: 分级统计地图
description: 按某个统计变量的高低给各地理区域着色，用来呈现各地的数据密度、人口特征或市场表现。
doc-type: reference
tags:
  - avalonia pro
---

import chartsMapsChoropleth from '/img/controls/charts/charts-maps.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

分级统计地图按统计变量的大小给各地理区域着色。要呈现若干离散区域上的数据密度或走势，用它很合适。

<Image light={chartsMapsChoropleth} maxWidth={400} position="center" cornerRadius="true" alt="Choropleth map shading geographic regions in varying color intensities to represent population density." />

## 适用场景 {#when-to-use}
- **人口特征**：呈现人口密度、收入水平或投票倾向。
- **市场渗透**：呈现各区域的销售表现。
- **环境数据**：按区域展示气候数据或资源分布。

## 代码示例 {#code-example}

### XAML
```xml
<ChoroplethMap xmlns="https://github.com/avaloniaui" Name="ChoroplethSample" Title="Population Density (Wrapper)" Height="400">
                        <ChoroplethMap.DataLayer>
                            <ShapeLayer GeoJson="{Binding WorldGeoJson}"
                                                 GeoJsonIdPath="ISO_A2"
                                                 MinValue="0"
                                                 MaxValue="500"
                                                 RegionPath="Code"
                                                 ValuePath="Density"
                                                 LowBrush="#E3F2FD"
                                                 HighBrush="#1565C0"
                                                 Stroke="#90A4AE"
                                                 ItemsSource="{Binding ShapeLayerData}">
                                <ShapeLayer.TooltipTemplate>
                                    <DataTemplate>
                                        <StackPanel Spacing="4">
                                            <TextBlock Text="{Binding Name}" FontWeight="Bold"/>
                                            <TextBlock Text="{Binding Density, StringFormat='Density: {0:N1} people/km²'}"/>
                                        </StackPanel>
                                    </DataTemplate>
                                </ShapeLayer.TooltipTemplate>
                            </ShapeLayer>
                        </ChoroplethMap.DataLayer>
                    </ChoroplethMap>
```

### 数据模型（C#） {#data-model-c}

请确保 GeoJSON 文件已包含在项目中，并且运行时可以在指定的相对路径下找到它。

```csharp
using System.IO;

public record CountryDensityData(string Code, string Name, double Density);

public string WorldGeoJson { get; } =
    File.ReadAllText("Resources/ne_110m_world.geojson");

public CountryDensityData[] ShapeLayerData { get; } = new CountryDensityData[]
{
    new("IN", "India", 464.0),
    new("BD", "Bangladesh", 1265.0),
    new("JP", "Japan", 347.0),
    new("KR", "S. Korea", 527.0),
    new("NL", "Netherlands", 508.0),
    new("BE", "Belgium", 376.0),
    new("GB", "UK", 275.0),
    new("DE", "Germany", 240.0),
    new("IT", "Italy", 206.0),
    new("FR", "France", 119.0),
    new("CN", "China", 153.0),
    new("US", "USA", 36.0),
    new("CA", "Canada", 4.0),
    new("BR", "Brazil", 25.0),
    new("RU", "Russia", 9.0),
    new("AU", "Australia", 3.0)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `DataLayer` | 用于渲染分级统计区域的标准 `ShapeLayer`。框架会自动创建一个默认图层。 | Auto-created `ShapeLayer` |

## 公共属性（`DataLayer` / `ShapeLayer`） {#common-properties-datalayer-shapelayer}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 区域数据项的集合。 | `null` |
| `GeoJson` | GeoJSON 几何数据源。 | `null` |
| `GeoJsonIdPath` | GeoJSON 中用于标识区域的属性名。 | `ISO_A2` |
| `RegionPath` | `ItemsSource` 中用于关联的属性名。 | `null` |
| `ValuePath` | 决定颜色深浅的数值属性名。 | `null` |
| `MinValue` | 用于颜色归一化的最小值。 | `0.0` |
| `MaxValue` | 用于颜色归一化的最大值。 | `100.0` |
| `LowBrush` | 数据区间低端所用的画刷。 | `#E3F2FD` |
| `HighBrush` | 数据区间高端所用的画刷。 | `#1565C0` |
| `Stroke` | 区域边界所用的画刷。 | `null` |
| `TooltipTemplate` | 地图工具提示所用的数据模板。 | `null` |

## 另请参阅 {#see-also}

- [形状地图](/controls/data-display/charts/maps/shape-map-chart)
- [气泡地图](/controls/data-display/charts/maps/bubble-map-chart)
