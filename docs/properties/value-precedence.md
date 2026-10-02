---
id: value-precedence
title: 属性取值优先级
description: Avalonia 如何借助 BindingPriority 裁决相互竞争的属性取值。
doc-type: explanation
---

当多个来源为同一个属性提供取值时，Avalonia 必须决定谁说了算。比如 `Foreground` 这样的属性，就可能同时收到本地值、样式 setter、动画和继承值的「投票」。属性系统依照 [`BindingPriority` 枚举](/api/avalonia/data/bindingpriority)所定义的固定优先级顺序来裁决。

## 优先级顺序 {#priority-order}

优先级高的取值胜过优先级低的，其中 1 为最高优先级。

| 优先级 | `BindingPriority` 值 | 说明 |
|---|---|---|
| 1 | `Animation` | 由活跃动画施加的取值。 |
| 2 | `LocalValue` | 通过 `SetValue`、XAML 特性或代码直接设置在对象上的取值。 |
| 3 | `StyleTrigger` | 由带条件激活的样式选择器施加的取值，例如伪类（`:pointerover`）、样式类（`.primary`）或属性判断（`[IsChecked=True]`）。 |
| 4 | `Template` | 在控件模板内部设置的取值。 |
| 5 | `Style` | 由始终匹配的样式选择器施加的取值，例如类型选择器（`Button`）或名称选择器（`#saveButton`）。 |
| 6 | `Inherited` | 从逻辑树中某个祖先元素继承来的取值。见[属性值继承](/docs/properties/property-value-inheritance)。 |
| 7 | `Unset` | 未设置任何取值，使用属性的默认值。 |

## 优先级是怎么起作用的 {#how-precedence-works}

当你（通过 `GetValue` 或绑定）请求属性值时，属性系统会按顺序逐级检查各优先级，返回第一个找到的取值。

### `StyleTrigger` vs. `Style`

`StyleTrigger`（优先级 3）和 `Style`（优先级 5）承载的都是来自样式的取值，Avalonia 靠**选择器**来区分二者：运行时有条件匹配的选择器，胜过始终匹配的选择器。实际效果就是，伪类、样式类和属性判断的优先级高于名称选择器和类型选择器。

两个 `StyleTrigger` 取值之间优先级相等，与激活条件的数量、以及激活条件在选择器语法中的位置无关。

### Example

设想一个带 `Foreground` 属性的 `Button`：

```xml
<!-- Application-level style (Priority: Style) -->
<Application.Styles>
    <Style Selector="Button">
        <Setter Property="Foreground" Value="Black" />
    </Style>
    <Style Selector="Button:pointerover">
        <Setter Property="Foreground" Value="Blue" />
    </Style>
</Application.Styles>
```

```xml
<!-- Local value (Priority: LocalValue) -->
<Button Foreground="Red" Content="Click me" />
```

在这种情况下：
- 按钮的 `Foreground` 是**红色**，因为 `LocalValue` 的优先级高于 `Style` 和 `StyleTrigger`。
- 即便指针悬停在按钮上，`Foreground` 依然是**红色** —— `LocalValue`（优先级 2）压过了 `StyleTrigger`（优先级 3）。

如果把本地的 `Foreground="Red"` 特性去掉：
- 按钮的 `Foreground` 默认是**黑色**（来自 `Style` setter）。
- 指针悬停到按钮上时，它变成**蓝色**（来自针对 `:pointerover` 的 `StyleTrigger`）。

## 样式的声明顺序 {#style-declaration-order}

当**同一优先级**上的两个样式指向同一个属性时，后声明的那个胜出：

```xml
<Window.Styles>
    <Style Selector="Button">
        <Setter Property="Background" Value="Blue" />
    </Style>

    <!-- This wins because it is declared later -->
    <Style Selector="Button">
        <Setter Property="Background" Value="Red" />
    </Style>
</Window.Styles>
```

来自不同位置的样式，按它们在逻辑树中出现的顺序求值 —— 从控件自身一路向上到应用。声明在 `UserControl` 上的样式会覆盖 `App.axaml` 中匹配的样式，因为越靠近的作用域求值越靠后。

声明顺序只在**同一优先级内部**用于打破平局。类选择器或属性选择器位于样式触发这一级，因此无论顺序如何，它都胜过单纯的类型选择器。

```xml
<Window.Styles>
    <!-- Style trigger level: this wins, even though it is declared first -->
    <Style Selector="Button.primary">
        <Setter Property="Background" Value="Red" />
    </Style>

    <!-- Style level -->
    <Style Selector="Button">
        <Setter Property="Background" Value="Blue" />
    </Style>
</Window.Styles>

<!-- Red, not Blue -->
<Button Classes="primary" Content="Primary" />
```

## 动画凌驾于一切之上 {#animations-override-everything}

动画的优先级最高。只要动画处于活跃状态，它的取值就压过其他所有来源。这样可以确保视觉过渡不会被样式变化打断。

```xml
<Style Selector="Button:pointerover">
    <Style.Animations>
        <Animation Duration="0:0:0.2">
            <KeyFrame Cue="100%">
                <Setter Property="Opacity" Value="0.8" />
            </KeyFrame>
        </Animation>
    </Style.Animations>
</Style>
```

## 模板优先级 {#template-priority}

`Template`（优先级 4）适用于由 `ControlTemplate` 设置的所有属性。在下面的例子中，`BorderThickness`、`Background` 和 `Padding` 都处于 `Template` 优先级。

`Template` 的优先级高于 `Style`（优先级 5），也就是说这些取值会覆盖名称选择器或类型选择器所设置的值。

```xml
<ControlTemplate>
    <Border BorderThickness="2">
        <Button Background="{DynamicResource ButtonBrush}" Padding="{TemplateBinding Padding}" />
    </Border>
</ControlTemplate>
```

## 在代码中操作优先级 {#working-with-priorities-in-code}

### 清除取值 {#clearing-values}

调用 `ClearValue` 会移除 `LocalValue` 这一优先级上的取值，属性系统随后顺延到下一个可用的取值来源。

```csharp
// Set a local value (red foreground overrides other styles)
myButton.SetValue(Button.ForegroundProperty, Brushes.Red);

// Clear the local value (styles take effect again)
myButton.ClearValue(Button.ForegroundProperty);
```

### 在指定优先级上设置取值 {#setting-values-at-specific-priorities}

在进阶场景下，可以用 `SetValue` 重载在指定优先级上设置取值：

```csharp
myButton.SetValue(Button.ForegroundProperty, Brushes.Red, BindingPriority.Style);
```

这主要供样式系统内部使用。在大多数应用代码中，你设置的都是本地值（调用 `SetValue` 时的默认行为）。

### `SetCurrentValue`

`SetCurrentValue` 方法会在当前最高优先级那一级上设值，而不是在 `LocalValue` 上。当你想更新属性但又不想覆盖样式时，可以用它：

```csharp
// Sets the value without creating a LocalValue entry
myButton.SetCurrentValue(Button.ForegroundProperty, Brushes.Green);
```

### 对数据绑定的影响 {#impact-on-data-binding}

绑定按其来源所在的优先级生效。通过样式创建的绑定作用在 `Style` 或 `StyleTrigger` 一级；直接写在 XAML 中的绑定则作用在 `LocalValue` 一级：

```xml
<!-- This binding operates at LocalValue priority -->
<Button Foreground="{Binding ButtonColor}" />
```

由于 `LocalValue` 绑定压过样式取值（`Style` 和 `StyleTrigger` 都算），XAML 中绑定得到的属性值会覆盖样式设置的任何取值。

如果你希望样式能够覆盖某个属性，就别在 XAML 中给它设值，改用相应层级的样式。

## 另请参阅 {#see-also}

- [属性系统总览](/docs/properties)：Avalonia 属性种类总览。
- [样式](/docs/styling/styles)：如何定义并应用样式。
- [动画](/docs/graphics-animation/animations)：动画与属性之间如何相互影响。
- [样式问题排查](/troubleshooting/ui-development/styles)：解决样式相关的常见问题。
