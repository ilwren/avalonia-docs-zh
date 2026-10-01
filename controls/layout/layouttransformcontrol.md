---
id: layouttransformcontrol
title: LayoutTransformControl
description: 一个 decorator 控件，为单个子元素应用参与布局的变换（旋转、缩放、倾斜），使父面板按变换后的边界来测量和排列。
doc-type: reference
---

[`LayoutTransformControl`](/api/avalonia/controls/layouttransformcontrol) 为其子元素应用参与布局的变换（旋转、缩放、倾斜）。`RenderTransform` 只改变控件的绘制方式、不影响周围布局，而 [`LayoutTransformControl`](/api/avalonia/controls/layouttransformcontrol) 则会让父面板按变换后的边界来测量和排列。

这意味着旋转后的控件会把相邻控件妥妥地挤开，缩放后的控件在 `StackPanel` 或 `Grid` 中也会占据相应大小的空间。

## 常用属性 {#common-properties}

| 属性 | 类型 | 说明 |
| :--- | :--- | :--- |
| `LayoutTransform` | `ITransform` | 布局期间要应用的变换，支持 `RotateTransform`、`ScaleTransform`、`SkewTransform`、`TransformGroup` 和 `MatrixTransform` |
| `UseRenderTransform` | `bool` | 为 `true` 时，改用 `RenderTransform` 应用变换，不再单独走一遍布局。默认值为 `false` |
| `Child` | `Control` | 要变换的子控件（继承自 `Decorator`） |
| `Padding` | `Thickness` | 子元素四周的内边距（继承自 `Decorator`） |

## `LayoutTransform` vs. `RenderTransform`

| | `LayoutTransformControl` | `RenderTransform` |
| :--- | :--- | :--- |
| 是否影响布局 | 是，同级元素会按变换后的边界重新排布 | 否，同级元素无视该变换 |
| 性能 | 变换改变时重新测量并重新排列 | 轻量，由 GPU 加速 |
| 适用场景 | 周围内容必须顾及变换后的尺寸 | 只做动画或视觉微调，不想影响布局 |

## 示例 {#examples}

### 旋转控件 {#rotating-a-control}

下面把一个按钮旋转 45 度。父级 `StackPanel` 会为旋转后的边界留出空间，因此下方的文字不会被盖住：

<XamlPreview>

```xml title="XAML"
<StackPanel Spacing="8" HorizontalAlignment="Center" xmlns="https://github.com/avaloniaui">
  <LayoutTransformControl>
    <LayoutTransformControl.LayoutTransform>
      <RotateTransform Angle="45" />
    </LayoutTransformControl.LayoutTransform>
    <Button Content="Rotated 45°" />
  </LayoutTransformControl>
  <TextBlock Text="This text is positioned below the rotated button." />
</StackPanel>
```

</XamlPreview>

### 缩放控件 {#scaling-a-control}

可以把控件放大到两倍，同时布局依然正确：

```xml title="XAML"
<LayoutTransformControl>
  <LayoutTransformControl.LayoutTransform>
    <ScaleTransform ScaleX="2" ScaleY="2" />
  </LayoutTransformControl.LayoutTransform>
  <TextBlock Text="Double size" />
</LayoutTransformControl>
```

### 组合多个变换 {#combining-transforms}

用 `TransformGroup` 可以同时应用多个变换：

```xml title="XAML"
<LayoutTransformControl>
  <LayoutTransformControl.LayoutTransform>
    <TransformGroup>
      <ScaleTransform ScaleX="1.5" ScaleY="1.5" />
      <RotateTransform Angle="30" />
    </TransformGroup>
  </LayoutTransformControl.LayoutTransform>
  <Border Background="LightBlue" Padding="12">
    <TextBlock Text="Scaled and rotated" />
  </Border>
</LayoutTransformControl>
```

### 绑定角度 {#binding-the-angle}

把旋转角度绑定到滑块，就能交互式地调节：

```xml title="XAML"
<StackPanel Spacing="12">
  <Slider x:Name="AngleSlider" Minimum="0" Maximum="360" Value="0" />
  <LayoutTransformControl HorizontalAlignment="Center">
    <LayoutTransformControl.LayoutTransform>
      <RotateTransform Angle="{Binding #AngleSlider.Value}" />
    </LayoutTransformControl.LayoutTransform>
    <Border Background="LightCoral" Padding="16">
      <TextBlock Text="Drag the slider to rotate" />
    </Border>
  </LayoutTransformControl>
</StackPanel>
```

## 实用提示 {#practical-notes}

- **性能**：由于每次变换改变都会让 `LayoutTransformControl` 走一整轮测量和排列，请避免高频地对它的 `LayoutTransform` 做动画。若需要跟得上帧率的流畅动画（比如旋转的加载图标），请改用 `RenderTransform`。
- **嵌套**：`LayoutTransformControl` 可以嵌进另一个 `LayoutTransformControl`。各自独立测量自己的子元素，于是变换沿布局树逐层向外叠加。
- **`UseRenderTransform`**：把该属性设为 `true` 后，变换将通过 `RenderTransform` 应用，而不再单独走一遍布局。当你图的是用 `LayoutTransform` 语法声明变换的便利、又不需要周围控件重新排布时，这很合适。
- **裁剪**：会裁剪子元素的父容器（比如设了 `ClipToBounds="True"` 的 `Border`）可能把变换后的边界裁掉。请确保父容器有足够空间完整显示变换后的区域。

## 另请参阅 {#see-also}

- [Decorator](/controls/layout/decorator)
- [Border](/controls/layout/containers/border)
- [Viewbox](/controls/layout/containers/viewbox)
- [Transforms](/docs/graphics-animation/transforms)
- [LayoutTransformControl API 参考](/api/avalonia/controls/layouttransformcontrol)
- [GitHub 上的 `LayoutTransformControl.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/LayoutTransformControl.cs)
