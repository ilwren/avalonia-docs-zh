---
id: shape-map-chart
title: 形状地图
description: 从 GeoJSON 渲染任意地理形状或自定义形状，是各类专用地图和交互式自定义区域图示的基础。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

Shape Map 控件可以呈现任意地理形状或自定义形状。它是各类专用地图的基础，开发者可以在其上自定义区域和交互。

## 适用场景 {#when-to-use}
- **自定义区域**：呈现标准地图集未涵盖的区域（比如特定的邮编辖区）。
- **实物布局**：把数据映射到示意图上（比如一块硬件电路板或厂房平面）。
- **交互式图示**：打造高性能的交互式形状系统。

## 代码示例 {#code-example}

### XAML

```xml
<ShapeMap xmlns="https://github.com/avaloniaui" Title="Regional Analysis" Height="400">
    <ShapeMap.Layers>
        <ShapeLayer GeoJson="{Binding AreaGeoJson}"
                             ItemsSource="{Binding AreaData}"
                             RegionPath="AreaId" />
    </ShapeMap.Layers>
</ShapeMap>
```

### 数据模型（C#） {#data-model-c}

请确保 GeoJSON 文件已包含在项目中，并且运行时可以在指定的相对路径下找到它们。

```csharp
using System.IO;

public record AreaInfo(string AreaId, string Status);

public string AreaGeoJson { get; } =
    File.ReadAllText("Resources/custom-areas.geojson");

public string WorldGeoJson { get; } =
    File.ReadAllText("Resources/ne_110m_world.geojson");

public ObservableCollection<AreaInfo> AreaData { get; } = new()
{
    new("A1", "Active"), new("A2", "Maintenance"), new("B1", "Active")
};

public record OfficeLocation(double Lat, double Lon, string Name);

public ObservableCollection<OfficeLocation> Offices { get; } = new()
{
    new(40.7128, -74.0060, "New York"),
    new(51.5074, -0.1278, "London"),
    new(35.6762, 139.6503, "Tokyo")
};

public record Route(double FromLat, double FromLon, double ToLat, double ToLon, double Passengers);

public ObservableCollection<Route> Routes { get; } = new()
{
    new(40.7128, -74.0060, 51.5074, -0.1278, 95),
    new(34.0522, -118.2437, 35.6762, 139.6503, 85)
};

public record Segment(string Category, double Amount);

public record RegionalPoint(double Lat, double Lon, ObservableCollection<Segment> Segments);

public ObservableCollection<RegionalPoint> RegionalData { get; } = new()
{
    new(40.7128, -74.0060, new ObservableCollection<Segment>
    {
        new("Tech", 45),
        new("Finance", 30),
        new("Retail", 25)
    }),
    new(51.5074, -0.1278, new ObservableCollection<Segment>
    {
        new("Tech", 30),
        new("Finance", 50),
        new("Retail", 20)
    })
};
```

## 公共属性（ShapeMap） {#common-properties-shapemap}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Layers` | 按顺序渲染的 `MapLayer` 实例集合。 | 空集合 |

## 公共属性（ShapeLayer） {#common-properties-shapelayer}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `GeoJson` | 各形状的几何数据。 | `null` |
| `Source` | 用于加载 GeoJSON 数据的 URI 源。 | `null` |
| `GeoJsonIdPath` | GeoJSON 中用作区域标识的属性名。 | `null` |
| `ItemsSource` | 代表各形状的数据项。 | `null` |
| `RegionPath` | 把数据与形状 ID 匹配起来的键属性。 | `null` |
| `ValuePath` | 绑定到各形状的数值所对应的属性名。 | `null` |
| `MinValue` | 用于归一化的最小值。 | `0.0` |
| `MaxValue` | 用于归一化的最大值。 | `100.0` |
| `LowBrush` | 数据最小值所用的画刷。 | `#E3F2FD` |
| `HighBrush` | 数据最大值所用的画刷。 | `#1565C0` |
| `Stroke` | 形状轮廓所用的画刷。 | `null` |
| `StrokeThickness` | 形状轮廓的粗细。 | `0.5` |
| `ShowLabels` | 是否为形状绘制标签。 | `false` |
| `LabelPath` | 形状标签所用的属性名。 | `null` |
| `LabelForeground` | 形状标签所用的画刷。 | `null` |
| `IsSelectionEnabled` | 是否启用形状选择。 | `true` |
| `SelectedItem` | 单选场景下当前选中的项。 | `null` |
| `SelectedItems` | 多选场景下选中项的集合。 | `null` |
| `SelectionMode` | 该图层的选择行为。 | `None` |
| `SelectionBrush` | 选中形状所用的画刷。 | `#FFC107` |
| `SelectionStroke` | 选中形状所用的轮廓画刷。 | `null` |
| `SelectionStrokeThickness` | 选中形状所用的轮廓粗细。 | `2.0` |
| `HoverBrush` | 形状被悬停时所用的画刷。 | `White @ 30% opacity` |
| `ColorMappings` | 可选的显式颜色映射规则，作用于各形状。 | 空集合 |
| `Legend` | 与该图层关联的可选图例。 | `null` |

## 公共属性（MapLegend） {#common-properties-maplegend}

`MapLegend` 显示由地图图层生成的图例项，比如显式的 `ShapeLayer.ColorMappings`。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Source` | 用于生成图例项的地图图层。 | `null` |
| `Orientation` | 图例条目的排列方向，`Horizontal` 或 `Vertical`。 | `Vertical` |
| `ItemTemplate` | 渲染每个图例项所用的可选模板。 | `null` |
| `Items` | 由源图层生成的只读 `AvaloniaList<LegendItem>`。 | 空集合 |

## 地图图层 {#map-layers}

除了 `ShapeLayer`，Shape Map 还支持几种特化图层，都可以加进 `Layers` 集合。每种图层在地图上渲染不同类型的叠加内容。

`ShapeMap.Layers` 可以绑定到 `IList<MapLayer>`。若该列表实现了 `INotifyCollectionChanged`，运行时增删图层会同步刷新渲染、命中测试和生成的图例。

`MarkerLayer.Markers`、`VectorLayer.Arcs`、`HeatmapLayer.ItemsSource` 等图层集合属性，只要其集合源实现了 `INotifyCollectionChanged`，同样会触发地图更新。把图层集合属性整个换成一个新列表，则会把该图层重新绑定到新的数据源。

### MarkerLayer

在地理坐标处渲染一个个点标记。标记既可以手工定义，也可以绑定到数据源。

#### 常用属性（`MarkerLayer`） {#common-properties-markerlayer}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Markers` | 手工定义的 `MapMarker` 对象集合。 | 空集合 |
| `ItemsSource` | 用于自动生成标记的数据源。 | `null` |
| `LatitudePath` | 指向数据源项中纬度值的属性路径。 | `null` |
| `LongitudePath` | 指向数据源项中经度值的属性路径。 | `null` |
| `LabelPath` | 指向数据源项中标签值的属性路径。 | `null` |
| `MarkerSize` | 每个标记的默认大小，单位为像素。 | `10.0` |
| `MarkerType` | 标记的默认形状：`Circle`、`Diamond`、`Triangle`、`Rectangle` 或 `Pin`。 | `Circle` |
| `Fill` | 标记的默认填充画刷。 | `Red` |
| `Stroke` | 标记的默认描边画刷。 | `White` |
| `IsVisible` | 该图层是否可见。 | `true` |
| `Opacity` | 该图层的不透明度。 | `1.0` |
| `TooltipTemplate` | 工具提示所用的数据模板。 | `null` |

#### XAML

```xml
<ShapeMap xmlns="https://github.com/avaloniaui" Title="Office Locations" Height="400">
    <ShapeMap.Layers>
        <ShapeLayer GeoJson="{Binding WorldGeoJson}" />
        <MarkerLayer ItemsSource="{Binding Offices}"
                              LatitudePath="Lat" LongitudePath="Lon"
                              LabelPath="Name" MarkerSize="12"
                              MarkerType="Pin" Fill="DodgerBlue" />
    </ShapeMap.Layers>
</ShapeMap>
```

### LineLayer

在成对的地理点之间渲染连接线。线的粗细可以随数据值变化，连线可以画成直线或曲线。

#### 常用属性（`LineLayer`） {#common-properties-linelayer}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 包含连接项的数据源。 | `null` |
| `FromLatitudePath` | 起点纬度所对应的属性路径。 | `null` |
| `FromLongitudePath` | 起点经度所对应的属性路径。 | `null` |
| `ToLatitudePath` | 终点纬度所对应的属性路径。 | `null` |
| `ToLongitudePath` | 终点经度所对应的属性路径。 | `null` |
| `ValuePath` | 连线数值所对应的属性路径（影响粗细）。 | `null` |
| `Stroke` | 连接线所用的画刷。 | `#2196F3` |
| `MinLineThickness` | 线条最小粗细。 | `1.0` |
| `MaxLineThickness` | 线条最大粗细。 | `6.0` |
| `IsCurved` | 是否画成曲线（贝塞尔）而非直线。 | `true` |
| `ShowEndpoints` | 是否在两端各画一个圆点。 | `true` |
| `IsVisible` | 该图层是否可见。 | `true` |
| `Opacity` | 该图层的不透明度。 | `1.0` |
| `TooltipTemplate` | 工具提示所用的数据模板。 | `null` |

#### XAML

```xml
<ShapeMap xmlns="https://github.com/avaloniaui" Title="Flight Routes" Height="400">
    <ShapeMap.Layers>
        <ShapeLayer GeoJson="{Binding WorldGeoJson}" />
        <LineLayer ItemsSource="{Binding Routes}"
                            FromLatitudePath="FromLat" FromLongitudePath="FromLon"
                            ToLatitudePath="ToLat" ToLongitudePath="ToLon"
                            ValuePath="Passengers" IsCurved="True"
                            MinLineThickness="1" MaxLineThickness="5" />
    </ShapeMap.Layers>
</ShapeMap>
```

### VectorLayer

用地理坐标在地图上渲染几何图形（线、弧、圆、多边形和折线）。这些图形通过图层的各个集合来定义。

#### 常用属性（`VectorLayer`） {#common-properties-vectorlayer}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Lines` | `MapLine` 对象的集合。 | 空集合 |
| `Arcs` | `MapArc` 对象的集合。 | 空集合 |
| `Circles` | `MapCircle` 对象的集合。 | 空集合 |
| `Polygons` | `MapPolygon` 对象的集合。 | 空集合 |
| `Polylines` | `MapPolyline` 对象的集合。 | 空集合 |
| `IsLineAnimationEnabled` | 是否为线条绘制过程播放动画。 | `true` |
| `IsVisible` | 该图层是否可见。 | `true` |
| `Opacity` | 该图层的不透明度。 | `1.0` |
| `TooltipTemplate` | 工具提示所用的数据模板。 | `null` |

#### XAML

```xml
<ShapeMap xmlns="https://github.com/avaloniaui" Title="Territory Boundaries" Height="400">
    <ShapeMap.Layers>
        <ShapeLayer GeoJson="{Binding WorldGeoJson}" />
        <VectorLayer IsLineAnimationEnabled="True">
            <VectorLayer.Circles>
                <MapCircle Latitude="48.8566" Longitude="2.3522"
                                    Radius="20" StrokeThickness="2">
                    <MapCircle.Fill>
                        <SolidColorBrush Color="#402196F3" />
                    </MapCircle.Fill>
                </MapCircle>
            </VectorLayer.Circles>
            <VectorLayer.Lines>
                <MapLine FromLatitude="40.7128" FromLongitude="-74.006"
                                  ToLatitude="51.5074" ToLongitude="-0.1278"
                                  StrokeThickness="2" />
            </VectorLayer.Lines>
        </VectorLayer>
    </ShapeMap.Layers>
</ShapeMap>
```

### PieChartMapLayer

在指定的地理坐标处绘制饼图。每张饼图呈现该地点各项数值的构成。

#### 常用属性（`PieChartMapLayer`） {#common-properties-piechartmaplayer}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 数据源，其中各项带有地理坐标和数值分段。 | `null` |
| `LatitudePath` | 纬度坐标所对应的属性路径。 | `null` |
| `LongitudePath` | 经度坐标所对应的属性路径。 | `null` |
| `ValuesPath` | 指向各数据项内部分段对象集合的属性路径。 | `null` |
| `ValuePath` | 指向各分段对象内部数值的属性路径。 | `null` |
| `LabelPath` | 指向各分段对象内部标签的属性路径。 | `null` |
| `PieSize` | 饼图的直径，单位为像素。 | `30.0` |
| `Palette` | 饼图扇区所用的调色板。 | 内置的 8 色调色板 |
| `IsVisible` | 该图层是否可见。 | `true` |
| `Opacity` | 该图层的不透明度。 | `1.0` |
| `TooltipTemplate` | 工具提示所用的数据模板。 | `null` |

#### XAML

```xml
<ShapeMap xmlns="https://github.com/avaloniaui" Title="Regional Sales Breakdown" Height="400">
    <ShapeMap.Layers>
        <ShapeLayer GeoJson="{Binding WorldGeoJson}" />
        <PieChartMapLayer ItemsSource="{Binding RegionalData}"
                                   LatitudePath="Lat" LongitudePath="Lon"
                                   ValuesPath="Segments" ValuePath="Amount"
                                   LabelPath="Category" PieSize="40" />
    </ShapeMap.Layers>
</ShapeMap>
```

## 另请参阅 {#see-also}

- [分级统计地图](/controls/data-display/charts/maps/choropleth-map-chart)
- [气泡地图](/controls/data-display/charts/maps/bubble-map-chart)
- [Heatmap](/controls/data-display/charts/maps/heatmap-map-chart)
