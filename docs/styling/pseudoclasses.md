---
id: pseudoclasses
title: 伪类
description: 了解如何用 Avalonia 的伪类，依据焦点、悬停、按下等控件状态来套用样式。
doc-type: explanation
---

import CustomPseudoclassScreenshot from '/img/reference/styles/custom-pseudoclass.gif';

Avalonia 的*伪类*与 CSS 中的类似，是由 `Control` 暴露的一些关键字，用来表示控件所处的某种状态。它们用在[样式选择器](/docs/styling/style-selectors)中，按条件为控件套样式。比如 [`Button`](/api/avalonia/controls/button) 被按下时可以有另一副模样，`TextBox` 被禁用时也可以。

伪类状态由 `Control` 的 `PseudoClasses` 属性记录。按照惯例，伪类名以 `:` 开头，比如 `:pointerover` 或 `:pressed`。

## 常用伪类 {#common-pseudoclasses}

下列伪类由 `InputElement` 定义，每个 `Control` 上都有：

| 伪类      | 说明                                                    |
|:-----------------|----------------------------------------------------------------|
| `:disabled`      | 控件已被禁用，无法交互。         |
| `:pointerover`   | 经命中测试判定，指针正悬在控件上。  |
| `:focus`         | 控件持有焦点。                                         |
| `:focus-within`  | 控件持有焦点，或者它的某个后代持有焦点。 |
| `:focus-visible` | 控件持有焦点，并且应当显示视觉标记。      |

各个控件还会定义自己特有的伪类。比如 `CheckBox` 暴露了 `:checked`，`Button` 暴露了 `:pressed`。

## 在选择器中使用伪类 {#using-pseudoclasses-in-selectors}

把伪类追加到选择器后面即可圈定它。下面这条让 `CheckBox` 在选中时显示粗体文字：

```xml
<Window.Styles>
    <Style Selector="CheckBox:checked">
        <Setter Property="FontWeight" Value="Bold" />
    </Style>
</Window.Styles>

<CheckBox Content="Pseudoselectors" />
```

一个控件身上可以同时激活多个伪类，你也可以在一条选择器里圈定多个伪类：

```xml
<Style Selector="Button.red:focus:pointerover">
```

这条选择器圈定的是：带 `red` 样式类、且 `:focus` 和 `:pointerover` 两个伪类都处于激活状态的 `Button` 控件。

## 创建自定义伪类 {#creating-custom-pseudoclasses}

编写自定义控件时，你可以定义自己的伪类来暴露控件状态。给类标注 `[PseudoClasses]` 特性以便 IDE 识别，再用 `PseudoClasses.Set` 切换状态。

:::note
`PseudoClasses` 集合是 `protected` 属性。自定义伪类只能在控件类内部设置，因此必须通过继承来实现。
:::

下面的例子定义了一个 `Button` 子类，它会根据指针落在按钮的哪个区域来设置伪类。

```csharp
[PseudoClasses(":left", ":right", ":middle")]
public class AreaButton : Button
{
    protected override void OnPointerMoved(PointerEventArgs e)
    {
        base.OnPointerMoved(e);
        var pos = e.GetPosition(this);

        if (pos.X < Bounds.Width * 0.25)
            SetAreaPseudoclasses(true, false, false);
        else if (pos.X > Bounds.Width * 0.75)
            SetAreaPseudoclasses(false, true, false);
        else
            SetAreaPseudoclasses(false, false, true);
    }

    protected override void OnPointerExited(PointerEventArgs e)
    {
        base.OnPointerExited(e);
        SetAreaPseudoclasses(false, false, false);
    }

    private void SetAreaPseudoclasses(bool left, bool right, bool middle)
    {
        PseudoClasses.Set(":left", left);
        PseudoClasses.Set(":right", right);
        PseudoClasses.Set(":middle", middle);
    }
}
```

由于 `AreaButton` 派生自 `Button`（一个 `TemplatedControl`），它需要有自己的 `ControlTheme`，这样选择器才能圈定那些新伪类：

```xml
<ControlTheme
    x:Key="{x:Type local:AreaButton}"
    BasedOn="{StaticResource {x:Type Button}}"
    TargetType="local:AreaButton" />
```

控件主题就位后，你就能用嵌套选择器为这些自定义伪类写样式了：

```xml
<Window.Styles>
    <Style Selector="local|AreaButton">
        <Setter Property="Content" Value="Testing Area" />
        <Setter Property="MinWidth" Value="200" />

        <Style Selector="^:left">
            <Setter Property="Content" Value="Left" />
        </Style>
        <Style Selector="^:right">
            <Setter Property="Content" Value="Right" />
        </Style>
        <Style Selector="^:middle">
            <Setter Property="Content" Value="Middle" />
        </Style>
    </Style>
</Window.Styles>

<local:AreaButton />
```

<Image light={CustomPseudoclassScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

自定义控件会自动继承基类的伪类，因此 `AreaButton` 同样会响应 `InputElement` 的 `:pointerover`、`:focus` 等内置伪类。

## 另请参阅 {#see-also}

- [样式选择器](/docs/styling/style-selectors)
- [样式选择器语法](/docs/styling/style-selector-syntax)
- [控件主题](/docs/styling/control-themes)
