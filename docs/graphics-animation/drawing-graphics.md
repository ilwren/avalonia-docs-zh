---
id: drawing-graphics
title: 绘制图形
description: Avalonia 二维图形系统概览：形状、几何与动画。
doc-type: overview
---

Avalonia 提供了一套二维图形系统，支持分辨率无关的渲染、形状图元和动画。

## Graphics

Avalonia 带来了一整套丰富、可缩放且灵活的图形能力，好处如下：

* 分辨率无关、设备无关的图形。Avalonia 图形系统的基本度量单位是设备无关像素，它等于 1/96 英寸，与实际屏幕分辨率无关，正是分辨率无关、设备无关渲染的基石。每个设备无关像素都会自动缩放，以匹配所在系统的每英寸点数（dpi）设置。
* 精度更高。Avalonia 的坐标系用双精度浮点数而非单精度来度量，变换和不透明度同样采用双精度表示。
* 完善的图形与动画支持。Avalonia 替你打理好了动画场景，大大简化了图形编程——你不必操心场景处理、渲染循环和双线性插值。此外，它还提供命中测试支持和完整的 alpha 合成支持。
* Skia。Avalonia 默认使用 [Skia 渲染引擎](https://skia.org/)，Google Chrome 与 Chrome OS、Android、Mozilla Firefox 与 Firefox OS 以及许多其他产品背后用的都是它。

## 二维形状与几何 {#2d-shapes-and-geometries}

Avalonia 提供了一套常用的矢量二维形状，比如 `Ellipse`、`Line`、`Path`、`Polygon` 和 `Rectangle`。

```xml
<Canvas Background="Yellow" Width="300" Height="400">
    <Rectangle Fill="Blue" Width="63" Height="41" Canvas.Left="40" Canvas.Top="31">
        <Rectangle.OpacityMask>
            <LinearGradientBrush StartPoint="0%,0%" EndPoint="100%,100%">
                <LinearGradientBrush.GradientStops>
                    <GradientStop Offset="0" Color="Black"/>
                    <GradientStop Offset="1" Color="Transparent"/>
                </LinearGradientBrush.GradientStops>
            </LinearGradientBrush>
        </Rectangle.OpacityMask>     
    </Rectangle>
    <Ellipse Fill="Green" Width="58" Height="58" Canvas.Left="88" Canvas.Top="100"/>
    <Path Fill="Orange" Data="M 0,0 c 0,0 50,0 50,-50 c 0,0 50,0 50,50 h -50 v 50 l -50,-50 Z" Canvas.Left="30" Canvas.Top="250"/>
    <Path Fill="OrangeRed" Canvas.Left="180" Canvas.Top="250">
        <Path.Data>
            <PathGeometry>
                <PathFigure StartPoint="0,0" IsClosed="True">
                    <QuadraticBezierSegment Point1="50,0" Point2="50,-50" />
                    <QuadraticBezierSegment Point1="100,-50" Point2="100,0" />
                    <LineSegment Point="50,0" />
                    <LineSegment Point="50,50" />
                </PathFigure>
            </PathGeometry>
        </Path.Data>
    </Path>
    <Line StartPoint="120,185" EndPoint="30,115" Stroke="Red" StrokeThickness="2"/>
    <Polygon Points="75,0 120,120 0,45 150,45 30,120" Stroke="DarkBlue" StrokeThickness="1" Fill="Violet" Canvas.Left="150" Canvas.Top="31"/>
    <Polyline Points="0,0 65,0 78,-26 91,39 104,-39 117,13 130,0 195,0" Stroke="Brown" Canvas.Left="30" Canvas.Top="350"/>
</Canvas>
```

把鼠标悬停在各个形状上即可看到它们的名字：

<div style={{margin: '24px 0', display: 'flex', justifyContent: 'center'}}>
<svg width="300" height="400" viewBox="0 0 300 400" xmlns="http://www.w3.org/2000/svg" style={{borderRadius: '8px', overflow: 'hidden', border: '1px solid rgba(128,128,128,0.15)'}}>
  <style>{`
    .dg-shape { transition: opacity 0.2s ease; cursor: pointer; }
    .dg-shapes:hover .dg-shape { opacity: 0.3; }
    .dg-shapes:hover .dg-shape:hover { opacity: 1; }
    .dg-label {
      opacity: 0;
      transition: opacity 0.15s ease;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 11px;
      font-weight: 600;
      fill: white;
      paint-order: stroke;
      stroke: rgba(0,0,0,0.75);
      stroke-width: 3.5px;
      stroke-linejoin: round;
      pointer-events: none;
    }
    .dg-shape:hover .dg-label { opacity: 1; }
  `}</style>
  <defs>
    <linearGradient id="dg-opmask" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stopColor="white" stopOpacity="1"/>
      <stop offset="100%" stopColor="white" stopOpacity="0"/>
    </linearGradient>
    <mask id="dg-rmask">
      <rect x="40" y="31" width="63" height="41" fill="url(#dg-opmask)"/>
    </mask>
  </defs>
  {/* Canvas background */}
  <rect width="300" height="400" fill="#FFFF00"/>
  <g className="dg-shapes">
    {/* Rectangle with OpacityMask */}
    <g className="dg-shape">
      <rect x="40" y="31" width="63" height="41" fill="blue" mask="url(#dg-rmask)"/>
      <text className="dg-label" x="71" y="24" textAnchor="middle">Rectangle</text>
    </g>
    {/* Ellipse */}
    <g className="dg-shape">
      <ellipse cx="117" cy="129" rx="29" ry="29" fill="green"/>
      <text className="dg-label" x="117" y="172" textAnchor="middle">Ellipse</text>
    </g>
    {/* Line */}
    <g className="dg-shape">
      <line x1="120" y1="185" x2="30" y2="115" stroke="red" strokeWidth="2"/>
      {/* Invisible wider hit area for easier hovering */}
      <line x1="120" y1="185" x2="30" y2="115" stroke="transparent" strokeWidth="14"/>
      <text className="dg-label" x="82" y="140" textAnchor="middle">Line</text>
    </g>
    {/* Polygon */}
    <g className="dg-shape">
      <polygon points="75,0 120,120 0,45 150,45 30,120" transform="translate(150,31)" fill="violet" stroke="darkblue" strokeWidth="1"/>
      <text className="dg-label" x="225" y="25" textAnchor="middle">Polygon</text>
    </g>
    {/* Path (mini-language) */}
    <g className="dg-shape">
      <path d="M 0,0 c 0,0 50,0 50,-50 c 0,0 50,0 50,50 h -50 v 50 l -50,-50 Z" transform="translate(30,250)" fill="orange"/>
      <text className="dg-label" x="80" y="242" textAnchor="middle">Path</text>
    </g>
    {/* Path (PathGeometry) */}
    <g className="dg-shape">
      <path d="M 0,0 Q 50,0 50,-50 Q 100,-50 100,0 L 50,0 L 50,50 Z" transform="translate(180,250)" fill="orangered"/>
      <text className="dg-label" x="230" y="242" textAnchor="middle">Path</text>
    </g>
    {/* Polyline */}
    <g className="dg-shape">
      <polyline points="0,0 65,0 78,-26 91,39 104,-39 117,13 130,0 195,0" transform="translate(30,350)" fill="none" stroke="brown" strokeWidth="1"/>
      {/* Invisible wider hit area */}
      <polyline points="0,0 65,0 78,-26 91,39 104,-39 117,13 130,0 195,0" transform="translate(30,350)" fill="none" stroke="transparent" strokeWidth="14"/>
      <text className="dg-label" x="127" y="340" textAnchor="middle">Polyline</text>
    </g>
  </g>
</svg>
</div>

## 添加动画 {#add-animations}

Avalonia UI 的动画支持能让控件放大、抖动、旋转、淡入淡出，做出有意思的页面过渡，还能玩出更多花样。Avalonia 采用类 CSS 的动画系统，支持[过渡](/docs/graphics-animation/control-transitions)和[关键帧动画](/docs/graphics-animation/keyframe-animations)。

## 另请参阅 {#see-also}

- [形状与几何](/docs/graphics-animation/shapes-and-geometries)：形状控件与几何类型。
- [画刷](/docs/graphics-animation/brushes)：用于填充和描边的各类画刷。
- [动画](/docs/graphics-animation/animations)：各类动画概览。
