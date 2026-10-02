---
id: drawingimage
title: DrawingImage
description: 一个把矢量图形渲染成 IImage 的控件，它基于 Avalonia 的 Drawing 对象，让你完全用 XAML 定义与分辨率无关的图标和图形。
doc-type: reference
---

[`DrawingImage`](/api/avalonia/media/drawingimage) 把矢量图形渲染成 `IImage`，于是凡是能用位图的地方都能用它。它不从文件里读像素，而是绘制由 Avalonia [`Drawing`](/api/avalonia/media/drawing) 系列类定义的形状、路径等矢量内容。

当你需要缩放不失真、与分辨率无关的图标或图形，或者想完全用 XAML 定义图像而不依赖外部资产文件时，它正合适。

## Drawing 的类型 {#drawing-types}

`DrawingImage` 在它的 `Drawing` 属性中包裹一个 `Drawing` 对象。Avalonia 提供了四种具体的 drawing 类型：

| 类型 | 用途 |
| :--- | :--- |
| `GeometryDrawing` | 填充和/或描边一个 `Geometry` 形状 |
| `ImageDrawing` | 在一个矩形区域内渲染位图图像 |
| `GlyphRunDrawing` | 用前景画刷渲染一段字形 |
| [`DrawingGroup`](/api/avalonia/media/drawinggroup) | 把多个 drawing 合为一个，并可附带变换、裁剪和不透明度 |

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `Drawing` | `Drawing` | 要渲染的矢量绘制内容 |
| `Viewbox` | `Rect` | 要显示的那部分绘制区域（矩形），单位为设备无关像素 |

## 示例 {#examples}

### 简单的矢量图标 {#simple-vector-icon}

下面的例子用 `GeometryDrawing` 画了一个带深绿描边的绿色圆：

```xml title="XAML"
<Image Width="64" Height="64">
  <Image.Source>
    <DrawingImage>
      <GeometryDrawing Brush="Green" Geometry="M 32,0 A 32,32 0 1 1 32,64 A 32,32 0 1 1 32,0 Z">
        <GeometryDrawing.Pen>
          <Pen Brush="DarkGreen" Thickness="2" />
        </GeometryDrawing.Pen>
      </GeometryDrawing>
    </DrawingImage>
  </Image.Source>
</Image>
```

### 组合多个 drawing {#combining-multiple-drawings}

用 `DrawingGroup` 可以把多个形状组合成一张图。下面的例子画了一个简单的房子图标：

```xml title="XAML"
<Image Width="100" Height="100">
  <Image.Source>
    <DrawingImage>
      <DrawingGroup>
        <!-- Roof -->
        <GeometryDrawing Brush="Brown" Geometry="M 10,50 L 50,10 L 90,50 Z" />
        <!-- Walls -->
        <GeometryDrawing Brush="Beige" Geometry="M 20,50 L 20,90 L 80,90 L 80,50 Z">
          <GeometryDrawing.Pen>
            <Pen Brush="Gray" Thickness="1" />
          </GeometryDrawing.Pen>
        </GeometryDrawing>
        <!-- Door -->
        <GeometryDrawing Brush="SaddleBrown" Geometry="M 40,60 L 40,90 L 60,90 L 60,60 Z" />
      </DrawingGroup>
    </DrawingImage>
  </Image.Source>
</Image>
```

### 作为资源使用 {#using-as-a-resource}

你可以把 `DrawingImage` 定义成资源，在整个应用里引用。这样图标定义集中在一处，还能在多个控件中复用：

```xml title="XAML"
<UserControl.Resources>
  <DrawingImage x:Key="CheckIcon">
    <GeometryDrawing Brush="Green" Geometry="M 2,5 L 4,7 L 8,3" >
      <GeometryDrawing.Pen>
        <Pen Brush="Green" Thickness="1" LineCap="Round" LineJoin="Round" />
      </GeometryDrawing.Pen>
    </GeometryDrawing>
  </DrawingImage>
</UserControl.Resources>

<Image Source="{StaticResource CheckIcon}" Width="24" Height="24" />
```

### `DrawingImage` 与位图图像的取舍 {#drawingimage-vs-bitmap-images}

以下情况请用 `DrawingImage`：

- 需要与分辨率无关、任意尺寸都干净利落的图形
- 图标完全用 XAML 定义，不依赖外部文件
- 需要动态图形，画刷或几何图形要绑定到数据

如果内容是照片或预先绘制好的美术素材，请用位图图像（`Image.Source` 搭配资产路径）。

## 实用提示 {#practical-notes}

- **Viewbox 裁剪。** 设置 `Viewbox` 属性后，只会渲染绘制内容中指定的那块矩形。把若干图标打包进一个 `DrawingGroup`、每次只显示其中一块时，这招很好用。
- **性能。** 由于 `DrawingImage` 每次绘制都会重新渲染矢量内容，上百个几何图形的复杂绘制可能比同等位图更慢。精细的美术素材不妨预先渲染成 `RenderTargetBitmap`。
- **数据绑定。** 绘制内容中的 `Brush`、`Geometry`、`Pen` 属性都可以绑定到视图模型的值，由此得到完全动态、随应用状态变化的矢量图形。
- **无障碍。** `DrawingImage` 本身不会向辅助技术暴露文字内容。如果图形承载了含义，请在父级 `Image` 控件上设置无障碍名称或说明。

## 另请参阅 {#see-also}

- [Image](/controls/media/image)
- [PathIcon](/controls/media/pathicon)
- [Brushes](/docs/graphics-animation/brushes)
- [DrawingImage API 参考](/api/avalonia/media/drawingimage)
- [GeometryDrawing API 参考](/api/avalonia/media/geometrydrawing)
- [DrawingGroup API 参考](/api/avalonia/media/drawinggroup)
- [GitHub 上的 `DrawingImage.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Media/DrawingImage.cs)
