---
id: text-options
title: 文本选项
description: 用 TextOptions 附加属性控制文本的 hinting、像素对齐与渲染模式。
doc-type: reference
---

Avalonia 通过 `TextOptions` 附加属性提供了对文本渲染方式的细致掌控。这些设置会影响控件及其后代中文本的 hinting、像素对齐与渲染模式。

## 属性 {#properties}

| 附加属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `TextOptions.TextRenderingMode` | `TextRenderingMode` | `Auto` | 控制文本使用抗锯齿、ClearType/次像素渲染，还是不作抗锯齿的渲染。 |
| `TextOptions.TextHintingMode` | `TextHintingMode` | `Full` | 控制如何应用字体 hinting。hinting 会微调字形轮廓使之对齐像素网格，让小字号的文本更锐利。 |
| `TextOptions.BaselinePixelAlignment` | `BaselinePixelAlignment` | `Unspecified` | 控制文本基线是否吸附到整像素边界。 |

## TextRenderingMode

| 值 | 说明 |
|---|---|
| `Auto` | 由平台挑选最合适的渲染模式。 |
| `Alias` | 渲染文本时不作抗锯齿。字形锐利但边缘有锯齿，适合像素风字体或极小的文字。 |
| `Antialias` | 以灰度抗锯齿渲染文本。 |
| `SubpixelAntialias` | 以次像素抗锯齿渲染文本（例如 Windows 上的 ClearType）。在 LCD 显示器上能得到最锐利的文字。 |

```xml
<TextBlock Text="Aliased text"
           TextOptions.TextRenderingMode="Alias" />

<TextBlock Text="Subpixel text"
           TextOptions.TextRenderingMode="SubpixelAntialias" />
```

## TextHintingMode

字体 hinting 会微调字形轮廓，使其对齐像素网格。这提升了小字号下的可读性，但也可能扭曲字形。调低或关闭 hinting 能保留字体本来的设计，更适合大号文字或带动画的文字。

| 值 | 说明 |
|---|---|
| `None` | 不作 hinting，字形保持原本的轮廓。最适合大号文字或带动画的文字。 |
| `Slight` | 轻度 hinting，只调整垂直方向的度量，保留字形的水平形态。 |
| `Normal` | 中等强度的 hinting。 |
| `Full` | 完整 hinting（默认）。最大程度对齐像素网格，小字号最锐利。 |

```xml
<!-- Large heading with no hinting for smooth outlines -->
<TextBlock Text="Welcome"
           FontSize="48"
           TextOptions.TextHintingMode="None" />

<!-- Body text with full hinting for maximum readability -->
<TextBlock Text="Read the details below."
           FontSize="14"
           TextOptions.TextHintingMode="Full" />
```

## BaselinePixelAlignment

控制文本基线是否吸附到整像素边界。对齐像素的基线在静态布局中文字更锐利；不对齐则允许次像素定位，可避免文字在动画或平滑滚动时「跳动」。

| 值 | 说明 |
|---|---|
| `Unspecified` | 由平台决定（静态文本通常是对齐的）。 |
| `Aligned` | 基线吸附到最近的像素，最适合静态界面文字。 |
| `Unaligned` | 基线采用次像素定位，最适合带动画或平滑滚动的文字。 |

```xml
<!-- Prevent text snapping during a RenderTransform animation -->
<TextBlock Text="Sliding text"
           TextOptions.BaselinePixelAlignment="Unaligned">
    <TextBlock.RenderTransform>
        <TranslateTransform />
    </TextBlock.RenderTransform>
</TextBlock>
```

## 作用于容器 {#applying-to-a-container}

与 `RenderOptions` 一样，`TextOptions` 也会被子控件继承。把它设在容器上即可作用于其中的全部文本：

```xml
<StackPanel TextOptions.TextHintingMode="None"
            TextOptions.BaselinePixelAlignment="Unaligned">
    <TextBlock Text="All text in this panel" />
    <TextBlock Text="uses no hinting and sub-pixel baselines." />
</StackPanel>
```

## 在代码中设置 {#setting-from-code}

```csharp
TextOptions.SetTextHintingMode(myControl, TextHintingMode.None);
TextOptions.SetBaselinePixelAlignment(myControl, BaselinePixelAlignment.Unaligned);
```

## 另请参阅 {#see-also}

- [图像插值](/docs/graphics-animation/image-interpolation)：通过 `RenderOptions` 调节位图渲染质量。
- [自定义渲染](/docs/graphics-animation/custom-rendering)：使用 Avalonia 渲染 API 作画。
