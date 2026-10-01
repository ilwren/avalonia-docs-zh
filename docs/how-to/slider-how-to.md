---
id: slider-how-to
title: "操作指南：使用 Slider"
description: "学会在 Avalonia UI 中配置 Slider 的取值范围、显示数值、添加刻度、设置朝向，以及绑定到视图模型。"
doc-type: how-to
---

本指南介绍 [`Slider`](/api/avalonia/controls/slider) 的常见场景，包括范围配置、数值显示、刻度线、纵向朝向以及双向数据绑定。

## 带数值显示的基本滑块 {#basic-slider-with-value-display}

把 `TextBlock` 绑定到滑块的 `Value` 属性，就能在滑块旁边显示当前值。用 `StringFormat` 标记可以控制数字的呈现方式：

```xml
<StackPanel Spacing="8">
    <TextBlock Text="{Binding #slider.Value, StringFormat='Volume: {0:F0}%'}" />
    <Slider x:Name="slider" Minimum="0" Maximum="100" Value="50" />
</StackPanel>
```

`#slider` 语法按 `x:Name` 引用控件。这种写法适合快速搭原型，但生产代码还是应当通过视图模型来绑定。

## 绑定到视图模型 {#binding-to-a-view-model}

为了把关注点分清楚，请把 `Value` 绑定到视图模型的属性。`Slider` 的绑定默认就是双向的，所以无论改动来自界面还是代码，两边都能保持同步：

```csharp
public partial class SettingsViewModel : ObservableObject
{
    [ObservableProperty]
    private double _brightness = 75;
}
```

```xml
<Slider Minimum="0" Maximum="100" Value="{Binding Brightness}" />
```

:::tip
若你想在值变化时作出响应（比如保存某项偏好设置），可以在视图模型里加一个 `OnBrightnessChanged` 之类的分部方法，MVVM Toolkit 的源生成器会自动把它造出来。
:::

## 刻度线与吸附 {#tick-marks-and-snapping}

用 `TickFrequency` 配合 `IsSnapToTickEnabled` 可以把取值限制在离散的档位上。当你的业务需要整数时（音量档位、百分比增量、星级评分），这尤其有用：

```xml
<!-- Snaps to multiples of 10 -->
<Slider Minimum="0" Maximum="100"
        TickFrequency="10"
        IsSnapToTickEnabled="True"
        TickPlacement="BottomRight" />
```

[`TickPlacement`](/api/avalonia/controls/tickplacement) 的取值：

| 值 | 说明 |
|---|---|
| `None` | 不显示刻度线（默认）。 |
| `TopLeft` | 刻度在上方（横向）或左侧（纵向）。 |
| `BottomRight` | 刻度在下方（横向）或右侧（纵向）。 |
| `Outside` | 两侧都显示刻度。 |

:::note
只设 `TickFrequency` 而不设 `IsSnapToTickEnabled="True"`，刻度线会画出来，但用户仍可拖到刻度之间的任意值。想要约束输入，这两个属性必须成对使用。
:::

## 小步长与大步长 {#small-and-large-change}

`SmallChange` 和 `LargeChange` 决定键盘操作或点击轨道时数值移动多少。若默认增量对你的取值范围来说太粗或太细，就调整它们：

```xml
<Slider Minimum="0" Maximum="1" Value="0.5"
        SmallChange="0.01"
        LargeChange="0.1" />
```

| 属性 | 触发方式 | 默认值 |
|---|---|---|
| `SmallChange` | 方向键 | 1 |
| `LargeChange` | 点击轨道，或按 Page Up / Page Down | 10 |

若滑块的范围很小（比如 0 到 1），你应当把这两个值都调小，好让键盘用户也能停到每一个有意义的位置上。

## 纵向滑块 {#vertical-slider}

把 [`Orientation`](/api/avalonia/layout/orientation) 属性设为 `Vertical`。你还应当显式设置 `Height`，免得滑块被压扁：

```xml
<Slider Orientation="Vertical" Height="200"
        Minimum="0" Maximum="100" Value="30" />
```

:::tip
使用纵向滑块时，`TopLeft` 的刻度出现在左侧，`BottomRight` 的刻度出现在右侧。若希望最小值在顶部而非底部，请设置 `IsDirectionReversed="True"`。
:::

## 只取整数的滑块 {#integer-only-slider}

要把滑块限制为整数，请把 `TickFrequency` 设为 `1` 并启用吸附，这样小数值就不会跑进你的视图模型：

```xml
<Slider Minimum="1" Maximum="10"
        TickFrequency="1"
        IsSnapToTickEnabled="True"
        Value="{Binding FontSizeChoice}" />
```

由于 `Value` 的类型是 `double`，你的视图模型属性也应当是 `double`。若业务逻辑里需要 `int`，请在绑定之后再转换（比如用 `(int)Math.Round(value)`）。

## 带标签的滑块 {#slider-with-labels}

用 `Grid` 在滑块两侧显示最小值和最大值标签，用户一眼就能看明白取值范围：

```xml
<Grid ColumnDefinitions="Auto,*,Auto" VerticalAlignment="Center">
    <TextBlock Grid.Column="0" Text="0" Margin="0,0,8,0"
               VerticalAlignment="Center" />
    <Slider Grid.Column="1" Minimum="0" Maximum="100" Value="{Binding Level}" />
    <TextBlock Grid.Column="2" Text="100" Margin="8,0,0,0"
               VerticalAlignment="Center" />
</Grid>
```

若这些值是动态设定的，你也可以把标签文字绑定到滑块上同样的 `Minimum` 和 `Maximum` 属性。

## 颜色预览滑块 {#color-preview-slider}

把多个滑块组合起来，做一个 RGB 调色器。每个滑块控制一个通道（0 到 255）并显示当前值：

```xml
<StackPanel Spacing="8">
    <StackPanel Orientation="Horizontal" Spacing="8">
        <TextBlock Text="R" Width="20" VerticalAlignment="Center" />
        <Slider Minimum="0" Maximum="255" Value="{Binding Red}" Width="200" />
        <TextBlock Text="{Binding Red, StringFormat='{}{0:F0}'}" Width="30" />
    </StackPanel>
    <StackPanel Orientation="Horizontal" Spacing="8">
        <TextBlock Text="G" Width="20" VerticalAlignment="Center" />
        <Slider Minimum="0" Maximum="255" Value="{Binding Green}" Width="200" />
        <TextBlock Text="{Binding Green, StringFormat='{}{0:F0}'}" Width="30" />
    </StackPanel>
    <StackPanel Orientation="Horizontal" Spacing="8">
        <TextBlock Text="B" Width="20" VerticalAlignment="Center" />
        <Slider Minimum="0" Maximum="255" Value="{Binding Blue}" Width="200" />
        <TextBlock Text="{Binding Blue, StringFormat='{}{0:F0}'}" Width="30" />
    </StackPanel>
</StackPanel>
```

为了让体验更顺手，不妨给每个滑块设上 `SmallChange="1"` 和 `LargeChange="16"`，让键盘增量契合调色时的常见操作。

## 禁用状态与只读状态 {#disabled-and-read-only-states}

有两种办法可以阻止用户与滑块交互：

```xml
<!-- Fully disabled: grayed-out appearance -->
<Slider IsEnabled="False" Value="60" />

<!-- Visually active but non-interactive -->
<Slider IsHitTestVisible="False" Value="{Binding Progress}" />
```

若想在视觉上表明控件暂不可用，就用 `IsEnabled="False"`；若希望滑块看上去如常、但只作只读指示（比如显示下载进度），则用 `IsHitTestVisible="False"`。

## 为滑块设置样式 {#styling-the-slider}

### 自定义轨道与滑块颜色 {#custom-track-and-thumb-colors}

写样式指向滑块内部的模板部件，即可改写轨道颜色。`PART_DecreaseButton` 负责填充滑块手柄之前的那一段：

```xml
<Slider Value="50">
    <Slider.Styles>
        <Style Selector="Slider /template/ RepeatButton#PART_DecreaseButton">
            <Setter Property="Background" Value="#6366F1" />
        </Style>
    </Slider.Styles>
</Slider>
```

### 更粗的轨道 {#wider-track}

调高轨道高度，既显得更醒目，也更容易点中：

```xml
<Slider.Styles>
    <Style Selector="Slider /template/ Track">
        <Setter Property="Height" Value="8" />
    </Style>
</Slider.Styles>
```

:::note
`PART_DecreaseButton`、`PART_IncreaseButton` 这些模板部件名由默认的 Fluent 主题定义。若你用的是自定义控件模板，部件名可能不同。
:::

## 关键属性速查 {#key-properties-reference}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Minimum` | `double` | 下界，默认值：0。 |
| `Maximum` | `double` | 上界，默认值：100。 |
| `Value` | `double` | 当前值。 |
| `SmallChange` | `double` | 方向键的增量，默认值：1。 |
| `LargeChange` | `double` | 点击轨道或按 Page 键时的增量，默认值：10。 |
| `TickFrequency` | `double` | 刻度线之间的间隔。 |
| `IsSnapToTickEnabled` | `bool` | 把取值吸附到最近的刻度。 |
| `TickPlacement` | `TickPlacement` | 刻度线画在哪一侧。 |
| `Orientation` | `Orientation` | `Horizontal`（默认）或 `Vertical`。 |
| `IsDirectionReversed` | `bool` | 反转数值增大的方向。 |

## 另请参阅 {#see-also}

- [Slider](/controls/input/selectors/slider)：`Slider` 控件的完整属性与事件参考。
- [绑定到控件](/docs/data-binding/binding-to-controls)：用 `#name` 语法把一个控件的属性绑定到另一个控件。
- [数据校验](/docs/app-development/data-validation)：为滑块绑定的属性加上校验规则。
- [无障碍](/docs/app-development/accessibility)：可交互控件在键盘和屏幕阅读器方面的注意事项。
