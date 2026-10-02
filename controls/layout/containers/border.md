---
id: border
title: Border
description: 了解如何用 Border 控件为 Avalonia 控件加上边框、背景、圆角和阴影。
doc-type: reference
---

`Border` 控件为单个子控件加上边框和背景作为装饰，还可以显示圆角。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table><thead><tr><th width="261">Property</th><th>说明</th></tr></thead><tbody><tr><td><code>背景</code></td><td>背景色。</td></tr><tr><td><code>BorderBrush</code></td><td>边框颜色。</td></tr><tr><td><code>BorderThickness</code></td><td>边框线条的粗细。</td></tr><tr><td><code>CornerRadius</code></td><td>四个角统一使用的圆角半径，也可以[写成一组值](#corner-radius-property)。</td></tr><tr><td><code>BoxShadow</code></td><td>[定义阴影](#box-shadows)。</td></tr><tr><td><code>BackgroundSizing</code></td><td>控制背景相对于边框如何渲染。<br />- <code>CenterBorder</code> （默认值，以边框粗细居中对齐）<br />- <code>InnerBorderEdge</code> （填充到边框内沿）<br />- <code>OuterBorderEdge</code> （延伸到边框外沿）</td></tr></tbody></table>

## CornerRadius 属性 {#corner-radius-property}

如果 `CornerRadius` 属性只给一个值，Avalonia 会把它用在子控件的四个角上。

你也可以给一组值，Avalonia 的解读方式如下：

- 给两个值时，按 `CornerRadius="Top Bottom"` 的模式解读：第一个值用于左上角和右上角，第二个值用于右下角和左下角。
- 给四个值时，按 `CornerRadius="TopLeft TopRight BottomRight BottomLeft"` 的模式解读。需要的话，其中一个或多个值可以为零。
- 不允许给三个值。

### Example

下面的例子用 border 控件在布局中营造出「卡片」的观感：

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui">
  <Border Background="Gray"
          BorderBrush="Black"
          BorderThickness="2"
          CornerRadius="3"
          Padding="10" Margin="10">
    <TextBlock>Box 1</TextBlock>
  </Border>
  <Border Background="Gray"
          BorderBrush="Black"
          BorderThickness="2"
          CornerRadius="3"
          Padding="10" Margin="10">
    <TextBlock>Box 2</TextBlock>
  </Border>
</StackPanel>
```

</XamlPreview>

## 阴影 {#box-shadows}

设置 `BoxShadow` 属性即可定义阴影。单个阴影由以下部分组成：

* 一个可选项，表示把阴影画在边框内侧。只要在 `BoxShadow` 属性的值里加上关键字 `inset` 即可启用。
* 两个、三个或四个长度值。（见下文。）
* 一个颜色值。

Avalonia 对这些长度值的解读方式如下：

- 给两个长度值时，依次解读为 `offset-x` 和 `offset-y`。
- 给三个长度值时，依次解读为 `offset-x`、`offset-y` 和 `blur-radius`。
- 给四个长度值时，依次解读为 `offset-x`、`offset-y`、`blur-radius` 和 `spread-radius`。

:::info
用逗号分隔多段阴影定义，就能同时指定多重阴影。
:::

下表按出现顺序说明阴影的各项取值：

<table><thead><tr><th width="203">值</th><th>说明</th></tr></thead><tbody><tr><td><code>inset</code></td><td>默认不指定，此时是外投阴影（看上去盒子浮在内容之上）。把 `inset` 关键字作为 `BoxShadow` 属性的第一个值，即可启用内阴影：阴影画在边框内侧、背景之上、内容之下（看上去内容凹陷在盒子里）。</td></tr><tr><td><code>offset-x</code> </td><td>指定水平偏移距离。负值会把阴影放到元素左侧。</td></tr><tr><td><code>offset-y</code></td><td>指定垂直偏移距离。负值会把阴影放到元素上方。</td></tr><tr><td><code>blur-radius</code></td><td>这个值越大，模糊效果越强，阴影也越大越淡。不允许负值。不指定时默认为零，此时阴影边缘是锐利的。</td></tr><tr><td><code>spread-radius</code></td><td>正值会让阴影向外扩张变大，负值则让阴影收缩。不指定时默认为零，此时阴影与元素同样大小。</td></tr><tr><td><code>color</code></td><td>阴影的颜色。可以写颜色名（如 `Red`）、带 # 前缀的十六进制颜色值（如 `#dadada`），或颜色函数（如 `rgb(13, 110, 253)`、`hsl(215, 98%, 52%)`）。</td></tr></tbody></table>

:::info
若两个偏移值都为零，阴影会落在元素正后方；此时只有设置了 `blur-radius` 和/或 `spread-radius` 才看得到模糊效果。
:::

### Example

下面是一个外投阴影的例子：

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui">
  <Border Background="Gray"
          BorderBrush="Black"
          BorderThickness="2"
          CornerRadius="3"
          BoxShadow="5 5 10 0 DarkGray"
          Padding="10" Margin="40">
    <TextBlock>Box with shadow</TextBlock>
  </Border>
</StackPanel>
```

</XamlPreview>

## 另请参阅 {#see-also}

- [Border API 参考](/api/avalonia/controls/border)
- [GitHub 上的 `Border.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Border.cs)
