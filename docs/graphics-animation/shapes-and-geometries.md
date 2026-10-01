---
id: shapes-and-geometries
title: 形状与几何
description: 在 Avalonia 中绘制二维矢量图形所用的形状控件与几何类型。
doc-type: reference
---

Avalonia 既提供了绘制常见二维矢量图形的形状控件，也提供了一套几何系统，用来描述路径、裁剪和命中测试所需的复杂轮廓。

## 形状控件 {#shape-controls}

形状控件是直接摆进 XAML 布局里的视觉元素。它们参与布局，也能接收指针事件。

### Rectangle

```xml
<Rectangle Width="100" Height="60"
           Fill="SteelBlue" Stroke="DarkBlue" StrokeThickness="2" />
```

| 属性 | 说明 |
|---|---|
| `RadiusX`, `RadiusY` | 圆角矩形的圆角半径。 |

```xml
<Rectangle Width="100" Height="60" Fill="Coral"
           RadiusX="10" RadiusY="10" />
```

### Ellipse

```xml
<Ellipse Width="100" Height="80"
         Fill="MediumPurple" Stroke="Indigo" StrokeThickness="2" />
```

把 `Width` 和 `Height` 设成相等的 `Ellipse` 就是一个圆。

### Line

```xml
<Line StartPoint="0,0" EndPoint="200,100"
      Stroke="Red" StrokeThickness="2" />
```

### Polyline

绘制首尾相接的若干线段，但不闭合图形：

```xml
<Polyline Points="0,0 50,50 100,0 150,50 200,0"
          Stroke="Green" StrokeThickness="2" />
```

### Polygon

与 `Polyline` 类似，只是图形会自动闭合：

```xml
<Polygon Points="50,0 100,100 0,100"
         Fill="Gold" Stroke="DarkGoldenRod" StrokeThickness="1" />
```

`Polyline` 和 `Polygon` 都支持 `FillRule` 属性，用来控制自相交的图形该如何填充：

- `EvenOdd`（默认）：重叠区域交替填充，从而形成镂空。
- `NonZero`：无论是否重叠，所有封闭区域一律填充。

```xml
<Polygon Points="50,0 61,35 98,35 68,57 79,91 50,70 21,91 32,57 2,35 39,35"
         Fill="Orange" FillRule="EvenOdd" />
```

### Path

最百搭的形状控件，用 `Geometry` 来定义自己的轮廓：

```xml
<!-- Using mini-language -->
<Path Data="M 10,10 L 100,10 L 100,100 Z"
      Fill="LightBlue" Stroke="Navy" StrokeThickness="1" />

<!-- Using PathGeometry -->
<Path Fill="Orange">
    <Path.Data>
        <PathGeometry>
            <PathFigure StartPoint="0,0" IsClosed="True">
                <LineSegment Point="100,0" />
                <LineSegment Point="100,100" />
            </PathFigure>
        </PathGeometry>
    </Path.Data>
</Path>
```

## 形状的通用属性 {#common-shape-properties}

所有形状都继承自 `Shape`，共有以下属性：

| 属性 | 说明 |
|---|---|
| `Fill` | 绘制内部填充的画刷。 |
| `Stroke` | 绘制轮廓的画刷。 |
| `StrokeThickness` | 轮廓的粗细，单位为设备无关像素。 |
| `StrokeDashArray` | 一组 `double` 值，定义虚线的样式。 |
| `StrokeDashOffset` | 起笔时在虚线样式中的偏移量。 |
| `StrokeLineCap` | 线端的端点样式：`Flat`、`Round` 或 `Square`。 |
| `StrokeJoin` | 拐角处的连接样式：`Miter`、`Bevel` 或 `Round`。 |
| `StrokeMiterLimit` | 尖角连接改为斜切的比例上限。当尖角长度除以描边粗细超过这个值时，连接方式就从锐利的尖角切换为斜切。默认为 `10`，仅在 `StrokeJoin` 为 `Miter` 时生效。 |
| `Stretch` | 形状如何填满分配给它的空间：`None`、`Fill`、`Uniform`、`UniformToFill`。 |

### 虚线 {#dashed-lines}

```xml
<Line StartPoint="0,0" EndPoint="200,0"
      Stroke="Black" StrokeThickness="2"
      StrokeDashArray="5,3" />

<Rectangle Width="150" Height="80" Fill="Transparent"
           Stroke="Gray" StrokeThickness="1"
           StrokeDashArray="4,2,1,2" />
```

## 几何类型 {#geometry-types}

几何是对二维形状的数学描述。它们比形状控件轻量，供 `Path.Data`、`Clip` 和 `OpacityMask` 使用。

### RectangleGeometry

```xml
<Path Fill="LightCoral">
    <Path.Data>
        <RectangleGeometry Rect="0,0,100,60" />
    </Path.Data>
</Path>
```

### EllipseGeometry

```xml
<Path Fill="LightGreen">
    <Path.Data>
        <EllipseGeometry Center="50,40" RadiusX="50" RadiusY="40" />
    </Path.Data>
</Path>
```

### LineGeometry

```xml
<Path Stroke="Red" StrokeThickness="2">
    <Path.Data>
        <LineGeometry StartPoint="0,0" EndPoint="100,50" />
    </Path.Data>
</Path>
```

### PathGeometry

最灵活的几何类型，由图形（figure）和线段（segment）组成：

```xml
<PathGeometry>
    <PathFigure StartPoint="10,50" IsClosed="True" IsFilled="True">
        <LineSegment Point="100,50" />
        <ArcSegment Point="100,150" Size="50,50"
                    SweepDirection="Clockwise" />
        <LineSegment Point="10,150" />
    </PathFigure>
</PathGeometry>
```

### 线段类型 {#segment-types}

| 线段 | 说明 |
|---|---|
| `LineSegment` | 画一条直线到某点。 |
| `ArcSegment` | 画一段椭圆弧。 |
| `BezierSegment` | 画一条三次贝塞尔曲线（两个控制点）。 |
| `QuadraticBezierSegment` | 画一条二次贝塞尔曲线（一个控制点）。 |
| `PolyLineSegment` | 画一串首尾相接的直线。 |
| `PolyBezierSegment` | 画一串首尾相接的三次贝塞尔曲线。每三个点依次表示第一个控制点、第二个控制点和终点。 |

### CombinedGeometry

用集合运算把两个几何合到一起：

```xml
<Path Fill="CornflowerBlue">
    <Path.Data>
        <CombinedGeometry GeometryCombineMode="Exclude">
            <CombinedGeometry.Geometry1>
                <EllipseGeometry Center="50,50" RadiusX="50" RadiusY="50" />
            </CombinedGeometry.Geometry1>
            <CombinedGeometry.Geometry2>
                <EllipseGeometry Center="80,50" RadiusX="50" RadiusY="50" />
            </CombinedGeometry.Geometry2>
        </CombinedGeometry>
    </Path.Data>
</Path>
```

| CombineMode | 结果 |
|---|---|
| `Union` | 两个几何中任意一个覆盖到的区域。 |
| `Intersect` | 两个几何共同覆盖的区域。 |
| `Exclude` | 在第一个几何内、但不在第二个几何内的区域。 |
| `Xor` | 只被其中一个几何覆盖、而非两者都覆盖的区域。 |

### GeometryGroup

把多个几何合并成单个几何：

```xml
<Path Fill="Salmon" Stroke="DarkRed" StrokeThickness="1">
    <Path.Data>
        <GeometryGroup FillRule="EvenOdd">
            <EllipseGeometry Center="50,50" RadiusX="50" RadiusY="50" />
            <EllipseGeometry Center="50,50" RadiusX="25" RadiusY="25" />
        </GeometryGroup>
    </Path.Data>
</Path>
```

`FillRule` 决定重叠区域如何填充：
- `EvenOdd`：重叠区域交替填充（形成镂空）。
- `NonZero`：所有封闭区域一律填充。

## 路径迷你语言 {#path-mini-language}

`Path` 的 `Data` 属性接受 SVG 风格的路径数据字符串。这套紧凑语法很适合描述复杂形状。

### Commands

| 命令 | 参数 | 说明 |
|---|---|---|
| `M` / `m` | `x,y` | 移动到某点（绝对 / 相对） |
| `L` / `l` | `x,y` | 画线到某点 |
| `H` / `h` | `x` | 水平线 |
| `V` / `v` | `y` | 垂直线 |
| `C` / `c` | `x1,y1 x2,y2 x,y` | 三次贝塞尔曲线 |
| `S` / `s` | `x2,y2 x,y` | 平滑三次贝塞尔曲线 |
| `Q` / `q` | `x1,y1 x,y` | 二次贝塞尔曲线 |
| `T` / `t` | `x,y` | 平滑二次贝塞尔曲线 |
| `A` / `a` | `rx,ry rotation large-arc sweep x,y` | 椭圆弧 |
| `Z` / `z` | | 闭合路径 |

大写命令用绝对坐标，小写命令用相对坐标。

### 示例 {#examples}

```xml
<!-- Triangle -->
<Path Data="M 50,0 L 100,100 L 0,100 Z" Fill="Gold" />

<!-- Rounded rectangle path -->
<Path Data="M 10,0 H 90 A 10,10 0 0 1 100,10 V 50 A 10,10 0 0 1 90,60 H 10 A 10,10 0 0 1 0,50 V 10 A 10,10 0 0 1 10,0 Z"
      Fill="LightSkyBlue" />

<!-- Heart shape -->
<Path Data="M 50,30 A 20,20 0 0 1 90,30 A 20,20 0 0 1 50,80 A 20,20 0 0 1 10,30 A 20,20 0 0 1 50,30 Z"
      Fill="Red" />

<!-- Star -->
<Path Data="M 50,0 L 61,35 L 98,35 L 68,57 L 79,91 L 50,70 L 21,91 L 32,57 L 2,35 L 39,35 Z"
      Fill="Orange" />
```

## 用代码构建几何 {#building-geometry-from-code}

用 `StreamGeometryContext` 以编程方式构建几何：先调用 `StreamGeometry.Open()` 拿到一个上下文，再用它的各个绘制方法来描述图形：

```csharp
var geometry = new StreamGeometry();

using (var ctx = geometry.Open())
{
    ctx.BeginFigure(new Point(10, 50), isFilled: true);
    ctx.LineTo(new Point(100, 50));
    ctx.ArcTo(
        new Point(100, 150),
        new Size(50, 50),
        rotationAngle: 0,
        isLargeArc: false,
        SweepDirection.Clockwise);
    ctx.LineTo(new Point(10, 150));
    ctx.EndFigure(isClosed: true);
}
```

### StreamGeometryContext 的方法 {#streamgeometrycontext-methods}

| 方法 | 说明 |
|---|---|
| `BeginFigure(Point, bool isFilled = true)` | 在指定点开始一个新图形。把 `isFilled` 设为 `false` 可得到不填充的开放路径。 |
| `LineTo(Point, bool isStroked = true)` | 画一条直线到某点。 |
| `ArcTo(Point, Size, double, bool, SweepDirection, bool isStroked = true)` | 画一段椭圆弧到某点。 |
| `CubicBezierTo(Point, Point, Point, bool isStroked = true)` | 用两个控制点和一个终点画一条三次贝塞尔曲线。 |
| `QuadraticBezierTo(Point, Point, bool isStroked = true)` | 用一个控制点和一个终点画一条二次贝塞尔曲线。 |
| `EndFigure(bool isClosed)` | 结束当前图形。把 `isClosed` 设为 `true` 即可闭合形状。 |

在任意线段上把 `isStroked` 设为 `false`，该段就不画轮廓，但依然计入几何形状。这适合做部分描边的路径。

```csharp
using (var ctx = geometry.Open())
{
    ctx.BeginFigure(new Point(0, 0), isFilled: false);
    ctx.LineTo(new Point(50, 0));              // Stroked
    ctx.LineTo(new Point(100, 0), isStroked: false); // Gap (not stroked)
    ctx.LineTo(new Point(150, 0));             // Stroked
    ctx.EndFigure(isClosed: false);
}
```

## 几何的方法 {#geometry-methods}

所有 `Geometry` 对象都提供用于命中测试和变换的方法：

| 方法 | 说明 |
|---|---|
| `FillContains(Point)` | 若该点位于几何的填充区域内，返回 `true`。 |
| `StrokeContains(Pen, Point)` | 若该点落在用指定画笔描出的几何轮廓上，返回 `true`。 |
| `GetWidenedGeometry(Pen)` | 返回一个新几何，表示用指定画笔为当前几何描边所覆盖的区域。这适合用来做轮廓化的形状。 |
| `GetFlattenedPathGeometry()` | 返回一个简化后的 `PathGeometry`，其中的曲线用直线段近似表示。 |

```csharp
var ellipse = new EllipseGeometry { Center = new Point(50, 50), RadiusX = 40, RadiusY = 40 };
var pen = new Pen(Brushes.Black, 10);

// Get the outline of the stroked ellipse as a geometry
var outlined = ellipse.GetWidenedGeometry(pen);
```

## 把几何当作资源来用 {#using-geometries-as-resources}

把几何定义为资源，便于在整个应用中复用：

```xml
<Application.Resources>
    <StreamGeometry x:Key="CheckmarkIcon">M 4,8.5 L 8,12.5 L 16,4</StreamGeometry>
    <StreamGeometry x:Key="CloseIcon">M 4,4 L 16,16 M 16,4 L 4,16</StreamGeometry>
</Application.Resources>

<Path Data="{StaticResource CheckmarkIcon}" Stroke="Green" StrokeThickness="2" />
```

`StreamGeometry` 是一种轻量、不可变的几何，针对性能作了优化，适合用于图标路径和其他静态形状。

## 另请参阅 {#see-also}

- [绘制图形](/docs/graphics-animation/drawing-graphics)：Avalonia 图形系统概览。
- [画刷](/docs/graphics-animation/brushes)：填充画刷与描边画刷。
- [效果](/docs/graphics-animation/effects)：盒阴影、裁剪与不透明度遮罩。
- [添加图标](/docs/graphics-animation/adding-icons)：使用图标字体和矢量图标。
