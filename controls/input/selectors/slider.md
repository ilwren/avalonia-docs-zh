---
id: slider
title: Slider
description: 一个控件：用户沿轨道拖动滑块，即可在最小值与最大值之间选定一个数值。
doc-type: reference
---

import SliderMaxValueScreenshot from '/img/controls/slider/slider-max-value.gif';

`Slider` 控件用滑块在轨道上的相对位置来表示一个数值，这个位置相对于你所配置的 `Maximum` 和 `Minimum` 而言。

拖动滑块、点击轨道、按方向键、滚动鼠标滚轮，都可以改变数值。凡是需要让用户从连续或分档区间里挑一个值的场合——音量、亮度、缩放比例等等——滑块都派得上用场。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Minimum` | `double` | 设置取值范围的下界，默认值为 `0`。 |
| `Maximum` | `double` | 设置取值范围的上界，默认值为 `100`。 |
| `Value` | `double` | 获取或设置滑块的当前值。 |
| `SmallChange` | `double` | 每按一次方向键，值变化的幅度，默认值为 `1`。 |
| `LargeChange` | `double` | 每点一次轨道或按一次 Page 键，值变化的幅度，默认值为 `10`。 |
| [`Orientation`](/api/avalonia/layout/orientation) | `Orientation` | `Horizontal`（默认）或 `Vertical`。 |

## Example

这个例子通过绑定到控件，把滑块的值显示在它上方的文本块中。

:::info
控件之间如何绑定，请参阅[绑定到控件](/docs/data-binding/binding-to-controls)指南。
:::

这里的最大值和最小值都保持默认（分别是 0 和 100）。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
            Margin="20">
  <TextBlock Text="{Binding #slider.Value}"
              HorizontalAlignment="Center"/>
  <Slider x:Name="slider" />
</StackPanel>
```

</XamlPreview>

## 刻度线与吸附 {#tick-marks-and-snapping}

用 `TickFrequency` 和 `IsSnapToTickEnabled` 可以把滑块限制在离散的档位上。当你希望用户只能选等距的几个值、而不是区间内任意一点时，这很有用。

```xml
<Slider Minimum="0" Maximum="100"
        TickFrequency="10"
        IsSnapToTickEnabled="True"
        TickPlacement="BottomRight" />
```

[`TickPlacement`](/api/avalonia/controls/tickplacement) 属性控制刻度线相对于轨道出现在哪一侧：

| 值 | 说明 |
|---|---|
| `None` | 不显示刻度线（默认）。 |
| `TopLeft` | 刻度线出现在横向滑块的上方，或纵向滑块的左侧。 |
| `BottomRight` | 刻度线出现在横向滑块的下方，或纵向滑块的右侧。 |
| `Outside` | 轨道两侧都出现刻度线。 |

## 纵向滑块 {#vertical-slider}

把 `Orientation` 属性设为 `Vertical`，滑块就会纵向呈现。使用纵向滑块时，记得给它一个明确的 `Height`，好让它有地方施展。

```xml
<Slider Orientation="Vertical" Height="200"
        Minimum="0" Maximum="100" Value="30" />
```

## 反转方向 {#reversing-the-direction}

若希望最大值位于左端（纵向滑块则是底端）而不是右端（或顶端），请把 `IsDirectionReversed` 设为 `True`。

```xml
<Slider Minimum="0" Maximum="100"
        IsDirectionReversed="True" />
```

## 绑定到视图模型 {#binding-to-a-view-model}

可以把 `Value`、`Minimum` 和 `Maximum` 绑定到视图模型的属性上。下面的例子用了 MVVM Community Toolkit 的源生成器：

```xml
<Slider Maximum="{Binding MaxDamage}" Value="{Binding Damage}" />
```

```csharp
[ObservableProperty]
private double _damage;

[ObservableProperty]
private double _maxDamage = 9999;
```

<Image light={SliderMaxValueScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 全部属性 {#all-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Minimum` | `double` | 取值范围的下界，默认值为 `0`。 |
| `Maximum` | `double` | 取值范围的上界，默认值为 `100`。 |
| `Value` | `double` | 滑块的当前值。 |
| `SmallChange` | `double` | 每按一次方向键，值变化的幅度，默认值为 `1`。 |
| `LargeChange` | `double` | 每点一次轨道或按一次 Page 键，值变化的幅度，默认值为 `10`。 |
| `TickFrequency` | `double` | 刻度线之间的间隔。 |
| `IsSnapToTickEnabled` | `bool` | 为 `true` 时，滑块会吸附到最近的刻度上，默认值为 `false`。 |
| `TickPlacement` | `TickPlacement` | 刻度线显示在哪里：`None`、`TopLeft`、`BottomRight` 或 `Outside`。 |
| `Orientation` | `Orientation` | `Horizontal`（默认）或 `Vertical`。 |
| `IsDirectionReversed` | `bool` | 为 `true` 时，反转数值递增的方向，默认值为 `false`。 |

## 另请参阅 {#see-also}

- [NumericUpDown](/controls/input/selectors/numericupdown)
- [ToggleSwitch](/controls/input/selectors/toggleswitch)
- [绑定到控件](/docs/data-binding/binding-to-controls)
- [Slider API Reference](/api/avalonia/controls/slider)
- [`Slider.cs` 在 GitHub 上的源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Slider.cs)
