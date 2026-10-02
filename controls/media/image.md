---
id: image
title: Image
---

import ImageUnscaledScreenshot from '/img/controls/image/image-unscaled.png';
import ImageUniformToFillScreenshot from '/img/controls/image/image-uniform-to-fill.png';
import BlendModeMultiply from '/img/reference/animations-and-graphics/bitmap-blend-modes/Multiply.png';

该控件可以显示来自指定图像源的位图。图像源可以是：

* 一个字符串常量，指明某个应用资产；
* 通过（绑定转换器）从绑定的资产名加载而来的位图；
* 也可以直接从内存流加载为位图。  

图像可以用来组成其他控件的内容。比如说，用图像控件就能做出图形化按钮。

图像可以用几种不同的混合模式渲染，不同模式下它与背后内容的相互作用也不同。全部受支持的混合模式及示例图集，请参阅[位图混合模式](/docs/graphics-animation/bitmap-blend-modes)页面。

显示的图像可以调整尺寸和缩放。按默认的缩放设置（两个方向均匀拉伸），图像会被适配到给定的尺寸（宽度和/或高度）。

:::info
图像的缩放设置与 [Viewbox](/controls/layout/containers/viewbox) 的相同。
:::

## 常用属性 {#common-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Source` | `IImage` | 要显示的图像，可以用资产 URI 字符串、`Bitmap` 或 `DrawingImage` 来设置。 |
| `Stretch` | `Stretch` | 图像如何缩放以填满自己的边界，见下表。 |
| `StretchDirection` | `StretchDirection` | 控制图像可以放大、缩小，还是两者都行。 |
| `BlendMode` | `BitmapBlendingMode` | 合成图像时使用的混合模式。 |

### Stretch 的取值 {#stretch-modes}

| 值 | 行为 |
|---|---|
| `None` | 图像按原始尺寸显示。 |
| `Fill` | 图像被拉伸填满边界，不保持宽高比。 |
| `Uniform` | 图像在保持宽高比的前提下缩放至恰好装入边界（默认值）。 |
| `UniformToFill` | 图像在保持宽高比的前提下缩放至填满边界，超出的部分会被裁掉。 |

## 示例 {#examples}

### Basic

下面的例子把一张位图资产载入图像控件，限定了高度和宽度，但缩放设置保持默认。图像本身不是正方形，而宽高却设成了同一个值。例子里还放了一个矩形，好让你看清图像是怎么被缩放的：

```xml
<Panel>
  <Rectangle Height="300" Width="300" Fill="LightGray"/>
  <Image Margin="20" Height="200" Width="200" 
         Source="avares://AvaloniaControls/Assets/pipes.jpg"/>
</Panel>
```

<Image light={ImageUnscaledScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### Stretch

下一个例子引入了 `UniformToFill` 拉伸设置：图像的高度被完整容纳，宽度则被裁掉一部分——否则它会超出指定宽度。这种处理不会让图像变形。

```xml
<Panel>
  <Rectangle Height="300" Width="300" Fill="LightGray"></Rectangle>
  <Image Margin="20" Height="200" Width="200" 
         Stretch="UniformToFill"
         Source="avares://AvaloniaControls/Assets/pipes.jpg"/>
</Panel>
```

<Image light={ImageUniformToFillScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

### BlendMode

这个例子用了两张图像，第二张采用 `Multiply` 混合模式。更多内容请参阅[位图混合模式](/docs/graphics-animation/bitmap-blend-modes)页面。

```xml
<Panel>
    <Image Source="./Cat.jpg"/>
    <Image Source="./Overlay-Color.png" BlendMode="Multiply"/>
</Panel>
```

<Image light={BlendModeMultiply} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [Image API 参考](/api/avalonia/controls/image)
- [GitHub 上的 `Image.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Image.cs)
