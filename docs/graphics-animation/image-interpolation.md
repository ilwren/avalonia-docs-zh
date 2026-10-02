---
id: image-interpolation
title: 图像插值
description: 在 Avalonia 中缩放图片时，如何控制图像插值的质量。
doc-type: how-to
---

在 Avalonia 中显示图片时——尤其是把图片缩放到与其原始分辨率不同的尺寸时——渲染质量取决于所用的插值模式。本指南介绍如何在你的 Avalonia 应用中控制图像插值。

## 默认表现 {#default-behavior}

自 Avalonia 11 起，默认插值模式为 `LowQuality`。这个设置以性能优先，但缩放图片时画面可能不够平滑，把图片显示得远小于原始尺寸时尤为明显。

## 插值模式 {#interpolation-modes}

Avalonia 支持下列位图插值模式：

| 模式 | 说明 |
| :--- | :--- |
| `None` | 不作插值，像素直接渲染，不做平滑 |
| `LowQuality` | 基础插值（默认），性能优先 |
| `MediumQuality` | 在速度与质量之间取得平衡的插值 |
| `HighQuality` | 平滑插值，缩小图片时效果最好 |

## 设置插值模式 {#setting-the-interpolation-mode}

### 按控件设置 {#per-control-setting}

你可以用 `RenderOptions.BitmapInterpolationMode` 附加属性为单个控件设置插值模式：

```xml
<Image Source="assets/myimage.png" 
       RenderOptions.BitmapInterpolationMode="HighQuality" />
```

它也可以设在容器上：

```xml
<Border RenderOptions.BitmapInterpolationMode="HighQuality">
    <Image Source="assets/myimage.png" />
</Border>
```

### 常见用法 {#common-use-cases}

1. **图标显示**：显示被缩小的图标时，用 `HighQuality` 插值可以避免锯齿边缘：
```xml
<Button>
    <Image Source="assets/icon.png" 
           Width="16" 
           Height="16"
           RenderOptions.BitmapInterpolationMode="HighQuality" />
</Button>
```

2. **图片画廊**：对画质要求较高的图片画廊：
```xml
<ItemsControl RenderOptions.BitmapInterpolationMode="HighQuality">
    <ItemsControl.ItemTemplate>
        <DataTemplate>
            <Image Source="{Binding ImagePath}" />
        </DataTemplate>
    </ItemsControl.ItemTemplate>
</ItemsControl>
```

## 边缘模式（抗锯齿） {#edge-mode-antialiasing}

Avalonia 默认会对图片做抗锯齿，于是图片旋转、缩放或落在次像素偏移上时，边缘依然平滑。这由 `RenderOptions.EdgeMode` 附加属性控制。

若要让某个控件强制呈现锯齿化（锐利、像素感）的边缘，把 `EdgeMode` 设为 `Aliased`：

```xml
<!-- Smooth edges (default) -->
<Image Source="assets/photo.png"
       RenderTransform="rotate(15)" />

<!-- Aliased edges (no antialiasing) -->
<Image Source="assets/sprite.png"
       RenderOptions.EdgeMode="Aliased"
       RenderTransform="rotate(15)" />
```

| 模式 | 说明 |
|---|---|
| `Unspecified` | 渲染器采用默认行为（抗锯齿）。 |
| `Aliased` | 关闭抗锯齿。适合像素画，或任何需要锐利、不作平滑的边缘的场合。 |

`EdgeMode` 对非图片的渲染（形状、边框）同样有效。把它设在父元素上即可作用于全部子元素：

```xml
<Border RenderOptions.EdgeMode="Aliased">
    <!-- All content inside renders without antialiasing -->
</Border>
```

## 性能考量 {#performance-considerations}

出于性能考虑，插值模式被设计成按控件设置。高质量插值更吃算力，所以请参考下面的取舍建议：

- 以下情形请用 `HighQuality`：
  - 徽标之类的重要界面元素
  - 画质要紧的缩小图片
  - 照片画廊，或以图片为主的界面
  
- 下列情形用默认的 `LowQuality` 即可：
  - 背景图片
  - 画质无关紧要的装饰性元素
  - 对性能敏感的应用

## 做一个全局设置 {#creating-a-global-setting}

Avalonia 没有内置设置全局插值模式的办法，但你可以自定义一个附加属性或行为，在整个应用范围内统一管理。下面是一种思路：

```csharp
public static class GlobalImageOptions
{
    public static readonly AttachedProperty<BitmapInterpolationMode> InterpolationModeProperty =
        AvaloniaProperty.RegisterAttached<Image, BitmapInterpolationMode>(
            "InterpolationMode",
            typeof(GlobalImageOptions),
            defaultValue: BitmapInterpolationMode.HighQuality);

    public static void SetInterpolationMode(Image image, BitmapInterpolationMode value)
    {
        image.SetValue(RenderOptions.BitmapInterpolationModeProperty, value);
    }
}
```

然后在 XAML 中：

```xml
<Style Selector="Image">
    <Setter Property="(local:GlobalImageOptions.InterpolationMode)"
            Value="HighQuality" />
</Style>
```

## 拿到最佳效果的几点建议 {#tips-for-best-results}

1. **资产准备**：
   - 按图片的预期显示尺寸提供合适分辨率的素材
   - 重要资产不妨准备多个分辨率版本
   - 尽可能使用矢量格式（SVG），获得分辨率无关的图形

2. **布局考量**：
   - 留意原始图片尺寸与显示尺寸之间的差距
   - 用合适的容器和布局面板来管理图片缩放
   - 可以考虑把 `UniformToFill` 或 `Uniform` 拉伸模式与高质量插值搭配使用

3. **测试**：
   - 在不同屏幕密度下测试图片渲染效果
   - 确认对大量图片启用高质量插值后对性能的影响
   - 检查不同插值设置下的内存占用

## 另请参阅 {#see-also}

- [文本选项](/docs/graphics-animation/text-options)：通过 `TextOptions` 调节文本渲染质量。
