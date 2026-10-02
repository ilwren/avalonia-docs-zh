---
id: bitmap-blend-modes
title: 位图混合模式
description: 用位图混合模式控制 Avalonia 渲染时像素如何叠加。
doc-type: reference
---

import BlendModeCat from '/img/reference/animations-and-graphics/bitmap-blend-modes/Cat.jpg';
import BlendModeOverlayColor from '/img/reference/animations-and-graphics/bitmap-blend-modes/Overlay-Color.png';

import BlendModeOverlay from '/img/reference/animations-and-graphics/bitmap-blend-modes/Overlay.png';
import BlendModePlus from '/img/reference/animations-and-graphics/bitmap-blend-modes/Plus.png';
import BlendModeSaturation from '/img/reference/animations-and-graphics/bitmap-blend-modes/Saturation.png';
import BlendModeScreen from '/img/reference/animations-and-graphics/bitmap-blend-modes/Screen.png';
import BlendModeSoftLight from '/img/reference/animations-and-graphics/bitmap-blend-modes/SoftLight.png';
import BlendModeColor from '/img/reference/animations-and-graphics/bitmap-blend-modes/Color.png';
import BlendModeColorBurn from '/img/reference/animations-and-graphics/bitmap-blend-modes/ColorBurn.png';
import BlendModeColorDodge from '/img/reference/animations-and-graphics/bitmap-blend-modes/ColorDodge.png';
import BlendModeDarken from '/img/reference/animations-and-graphics/bitmap-blend-modes/Darken.png';
import BlendModeDifference from '/img/reference/animations-and-graphics/bitmap-blend-modes/Difference.png';
import BlendModeExclusion from '/img/reference/animations-and-graphics/bitmap-blend-modes/Exclusion.png';
import BlendModeHardLight from '/img/reference/animations-and-graphics/bitmap-blend-modes/HardLight.png';
import BlendModeHue from '/img/reference/animations-and-graphics/bitmap-blend-modes/Hue.png';
import BlendModeLighten from '/img/reference/animations-and-graphics/bitmap-blend-modes/Lighten.png';
import BlendModeLuminosity from '/img/reference/animations-and-graphics/bitmap-blend-modes/Luminosity.png';
import BlendModeMultiply from '/img/reference/animations-and-graphics/bitmap-blend-modes/Multiply.png';
import BlendModeNothing from '/img/reference/animations-and-graphics/bitmap-blend-modes/Nothing.png';

import BlendModeA from '/img/reference/animations-and-graphics/bitmap-blend-modes/A.png';
import BlendModeB from '/img/reference/animations-and-graphics/bitmap-blend-modes/B.png';

import BlendModeDestination from '/img/reference/animations-and-graphics/bitmap-blend-modes/Destination.png';
import BlendModeDestinationAtop from '/img/reference/animations-and-graphics/bitmap-blend-modes/DestinationAtop.png';
import BlendModeDestinationIn from '/img/reference/animations-and-graphics/bitmap-blend-modes/DestinationIn.png';
import BlendModeDestinationOut from '/img/reference/animations-and-graphics/bitmap-blend-modes/DestinationOut.png';
import BlendModeDestinationOver from '/img/reference/animations-and-graphics/bitmap-blend-modes/DestinationOver.png';
import BlendModeSource from '/img/reference/animations-and-graphics/bitmap-blend-modes/Source.png';
import BlendModeSourceAtop from '/img/reference/animations-and-graphics/bitmap-blend-modes/SourceAtop.png';
import BlendModeSourceIn from '/img/reference/animations-and-graphics/bitmap-blend-modes/SourceIn.png';
import BlendModeSourceOut from '/img/reference/animations-and-graphics/bitmap-blend-modes/SourceOut.png';
import BlendModeSourceOver from '/img/reference/animations-and-graphics/bitmap-blend-modes/SourceOver.png';
import BlendModeXor from '/img/reference/animations-and-graphics/bitmap-blend-modes/Xor.png';

把位图绘制到屏幕上时，Avalonia 允许你指定使用哪种混合模式。混合模式改变的是「把新像素（源）画到既有像素（目标）之上」时所做的运算。

目前 Avalonia 把合成模式和像素混合模式都放在同一个名为 `BitmapBlendingMode` 的枚举里。

合成模式枚举主要描述新像素如何依据 alpha 通道与屏幕上现有像素相互作用，可用来做出「饼干模子」式的抠形、排除区域或遮罩等效果。

像素混合模式则规定新颜色如何与现有颜色相互作用，可用于特效、调整色相，或做更复杂的图像合成。

各种混合模式的效果和背后的数学原理，可以参考[维基百科上的混合模式条目](https://en.wikipedia.org/wiki/Blend_modes)。

:::info
混合模式的支持情况取决于渲染后端。Skia 渲染器支持下面列出的全部混合模式。
:::

## 默认表现 {#default-behavior}

默认混合模式是 `SourceOver`：依据 alpha 通道，用新值整体替换像素值。绝大多数应用叠加两张图片时用的都是这种标准方式。

## 怎么用 {#how-to-use-it}

在 XAML 中，你可以指定渲染 Image 控件时采用哪种混合模式。下面的例子会在一只超可爱的猫咪照片上叠一层颜色：

```xml
<Panel>
    <Image Source="./Cat.jpg"/>
    <Image Source="./Overlay-Color.png" BlendMode="Multiply"/>
</Panel>
```

若你在写自定义用户控件，想用代码以某种混合模式绘制位图，只需在控件的渲染选项中设置 `BitmapBlendingMode`：

``` csharp
// Inside the "Render" method, draw the bitmap like this:

using (context.PushRenderOptions(RenderOptions with { BitmapBlendingMode = BitmapBlendingMode.Multiply }))
{
    context.DrawImage(source, sourceRect, destRect);
}
```

## 位图混合模式一览 {#bitmap-blend-mode-gallery}

Avalonia 渲染时支持下列位图混合模式：

### 像素混合模式 {#pixel-blend-modes}

像素混合模式只影响颜色，不考虑 alpha 通道。

示例中用到的是这两张图：

| 可爱猫咪底图（目标） | 色轮叠加图（源） |
|:---:|:---:|
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Cat.jpg" alt="Cat photo used as destination image" width="180"/> | <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Overlay-Color.png" alt="Color wheel overlay used as source image" width="180"/> |

下面是 Avalonia 目前支持的全部取值

| 预览 | 枚举值 | 说明 |
|---|---|---|
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Nothing.png" alt="Preview of Unspecified blend mode" width="180"/> | `Unspecified` | 即 `SourceOver` —— 默认行为。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Plus.png" alt="Preview of Plus blend mode" width="180"/> | `Plus` | 显示源图与目标图之和。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Screen.png" alt="Preview of Screen blend mode" width="180"/> | `Screen` | 把目标色与源色各自取补后相乘，再对结果取补。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Overlay.png" alt="Preview of Overlay blend mode" width="180"/> | `Overlay` | 视目标色的取值，对颜色作正片叠底或滤色处理。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Darken.png" alt="Preview of Darken blend mode" width="180"/> | `Darken` | 在目标色和源色中取较暗者。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/HardLight.png" alt="Preview of Lighten blend mode" width="180"/> | `Lighten` | 在目标色和源色中取较亮者。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/ColorDodge.png" alt="Preview of ColorDodge blend mode" width="180"/> | `ColorDodge` | 加深目标色，以映出源色。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/ColorBurn.png" alt="Preview of ColorBurn blend mode" width="180"/> | `ColorBurn` | 视源色的取值，对颜色作正片叠底或滤色处理。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/HardLight.png" alt="Preview of HardLight blend mode" width="180"/> | `HardLight` | 视源色的取值，把颜色调暗或调亮。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/SoftLight.png" alt="Preview of SoftLight blend mode" width="180"/> | `SoftLight` | 用两种颜色中较亮的减去较暗的。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Difference.png" alt="Preview of Difference blend mode" width="180"/> | `Difference` | 效果类似 Difference 模式，但对比度更低。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Exclusion.png" alt="Preview of Exclusion blend mode" width="180"/> | `Exclusion` | 源色与目标色相乘，结果取代目标|
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Multiply.png" alt="Preview of Multiply blend mode" width="180"/> | `Multiply` | 取源色的色相，配上目标色的饱和度和明度，合成新颜色。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Hue.png" alt="Preview of Hue blend mode" width="180"/> | `Hue` | 取源色的色相，配上目标色的饱和度和明度，合成新颜色。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Saturation.png" alt="Preview of Saturation blend mode" width="180"/> | `Saturation` | 取源色的饱和度，配上目标色的色相和明度，合成新颜色。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Color.png" alt="Preview of Color blend mode" width="180"/> | `Color` | 取源色的色相和饱和度，配上目标色的明度，合成新颜色。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Luminosity.png" alt="Preview of Luminosity blend mode" width="180"/> | `Luminosity` | 取源色的明度，配上目标色的色相和饱和度，合成新颜色。 |

### 合成混合模式 {#composition-blend-modes}

合成混合模式只影响 alpha 通道，不动颜色。

示例中用到的是这两张图：

| 「A」底图（目标） | 「B」叠加图（源） |
|:---:|:---:|
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/A.png" alt="Image A used as destination for composition examples" width="180"/> | <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/B.png" alt="Image B used as source for composition examples" width="180"/> |

下面是 Avalonia 目前支持的全部取值。请注意这组演示对 alpha 通道很敏感，所以网页背景会从图片中透出来。

| 预览 | 枚举值 | 说明 |
|---|---|---|
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Source.png" alt="Preview of Source composition mode" width="180"/> | `Source` | 只保留源。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/SourceOver.png" alt="Preview of SourceOver composition mode" width="180"/> | `SourceOver` | 即 `Unspecified` —— 默认行为，源叠在目标之上。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/SourceIn.png" alt="Preview of SourceIn composition mode" width="180"/> | `SourceIn` | 源与目标重叠的部分取代目标。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/SourceOut.png" alt="Preview of SourceOut composition mode" width="180"/> | `SourceOut` | 只保留源落在目标之外的部分。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/SourceAtop.png" alt="Preview of SourceAtop composition mode" width="180"/> | `SourceAtop` | 源中与目标重叠的部分取代目标。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Xor.png" alt="Preview of Xor composition mode" width="180"/> | `Xor` | 保留源与目标互不重叠的区域并把它们合并。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/Destination.png" alt="Preview of Destination composition mode" width="180"/> | `Destination` | 只保留目标。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/DestinationOver.png" alt="Preview of DestinationOver composition mode" width="180"/> | `DestinationOver` | 目标叠在源之上。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/DestinationIn.png" alt="Preview of DestinationIn composition mode" width="180"/> | `DestinationIn` | 目标中与源重叠的部分取代源。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/DestinationOut.png" alt="Preview of DestinationOut composition mode" width="180"/> | `DestinationOut` | 只保留目标落在源之外的部分。 |
| <img src="/img/reference/animations-and-graphics/bitmap-blend-modes/DestinationAtop.png" alt="Preview of DestinationAtop composition mode" width="180"/> | `DestinationAtop` | 目标中与源重叠的部分取代源。 |

## 另请参阅 {#see-also}

- [画刷](/docs/graphics-animation/brushes)：用于填充和描边的各类画刷。
- [绘制图形](/docs/graphics-animation/drawing-graphics)：形状、几何与图形系统。
- [自定义渲染](/docs/graphics-animation/custom-rendering)：用 `DrawingContext` 作画。
