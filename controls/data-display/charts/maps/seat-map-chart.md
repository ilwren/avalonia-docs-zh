---
id: seat-map-chart
title: 非地理地图（座位图）
description: 用 ShapeMap 控件配上自定义 GeoJSON，呈现座位表、平面图、可交互场馆布局等非地理版面。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

ShapeMap 控件能处理非地理坐标系，因此特别适合用来做飞机座位表、楼层平面图、剧院座次这类自定义版面。

## 适用场景 {#when-to-use}
- **订座**：交通工具或场馆的交互式座位表。
- **设施管理**：在建筑平面图之上呈现数据。
- **交互式图示**：打造可点击、数据驱动的自定义形状版面。

## 代码示例 {#code-example}

### XAML
```xml
<ShapeMap xmlns="https://github.com/avaloniaui" Name="SeatMapSample" Title="Aircraft Seating Layout">
    <ShapeMap.Layers>
        <ShapeLayer GeoJson="{Binding SeatMapGeoJson}"
                             GeoJsonIdPath="id"
                             RegionPath="SeatNumber"
                             ValuePath="Class"
                             ItemsSource="{Binding SeatMapData}"
                             SelectionMode="Multiple"
                             SelectedItems="{Binding SelectedSeats}" />
    </ShapeMap.Layers>
</ShapeMap>
```

### 数据模型（C#） {#data-model-c}

请确保 GeoJSON 文件已包含在项目中，并且运行时可以在指定的相对路径下找到它。

```csharp
using System.IO;

public record SeatInfo(string SeatNumber, string Class, decimal Price, string Status);

public string SeatMapGeoJson { get; } =
    File.ReadAllText("Resources/seat-map.geojson");

public ObservableCollection<SeatInfo> SeatMapData { get; } = new()
{
    new("1A", "Business", 500m, "Available"),
    new("1B", "Business", 500m, "Available"),
    new("10C", "Economy", 150m, "Available"),
    new("10D", "Economy", 150m, "Available")
};

public ObservableCollection<SeatInfo> SelectedSeats { get; } = new();
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `GeoJson` | 表示该版面的自定义 GeoJSON。 | `null` |
| `RegionPath` | 用于把数据与形状匹配起来的属性。 | `null` |
| `ValuePath` | 用于按状态给形状着色的属性。 | `null` |
| `SelectionMode` | `None`, `Single`, `SingleDeselect`, or `Multiple`. | `None` |
| `SelectedItems` | 绑定到选中的数据项。 | `null` |
*（注：座位图通过自定义 GeoJSON 来渲染非地理形状）*
