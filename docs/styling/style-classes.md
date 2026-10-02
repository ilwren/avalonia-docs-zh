---
id: style-classes
title: 样式类
description: 了解如何在 Avalonia 中指定和使用样式类，为控件套上按条件生效的样式。
doc-type: explanation
---

你可以给 Avalonia 控件指定一个或多个*样式类*，用它们来引导样式的选取。样式类通过控件元素上的 `Classes` 特性指定；要指定多个类，用空格分隔即可。

例如，这个按钮同时带有 `h1` 和 `blue` 两个样式类：

```xml
<Button Classes="h1 blue"/>
```

## Pseudoclasses

和 CSS 一样，控件也可以有伪类——这类类由控件自身定义，而非用户指定。选择器中的伪类名总以冒号开头。

比如 `:pointerover` 伪类表示指针当前正悬在控件上（落在其边界内），它类似 CSS 中的 `:hover`。

下面是一个 `:pointerover` 伪类选择器的例子：

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <StackPanel>
    <StackPanel.Styles>
      <Style Selector="Border:pointerover">
        <Setter Property="Background" Value="Red"/>
      </Style>
    </StackPanel.Styles>
    <Border>
      <TextBlock Margin="10">Hover for red background</TextBlock>
    </Border>
  </StackPanel>
</UserControl>
```

</XamlPreview>

这个例子中，伪类选择器改动的是控件模板内部的属性：

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <StackPanel>
    <StackPanel.Styles>
      <Style Selector="Button:pressed /template/ ContentPresenter">
          <Setter Property="TextBlock.Foreground" Value="Red"/>
      </Style>
    </StackPanel.Styles>
   <Button Margin="10">Press for red text</Button>
  </StackPanel>
</UserControl>
```

</XamlPreview>

其他伪类还有按钮的 `:focus`、`:disabled`、`:pressed`，以及复选框的 `:checked`。

:::info
关于伪类的更多细节，请见[伪类](/docs/styling/pseudoclasses)。
:::

## 条件类 {#conditional-classes}

若你想按某个绑定条件添加或移除类，可以用下面这种特殊语法：

```xml
<Button Classes.accent="{Binding IsSpecial}" />
```

## 按条件套样式的套路 {#conditional-styling-patterns}

Avalonia 没有 WPF 那样的触发器。要实现条件样式，请改用样式类、伪类和绑定转换器。

### 依绑定属性切换外观 {#toggle-appearance-based-on-a-bound-property}

先用样式类为各个状态分别定义样式，再按条件绑定这个类：

```xml
<StackPanel>
    <StackPanel.Styles>
        <Style Selector="Border.status-ok">
            <Setter Property="Background" Value="Green" />
        </Style>
        <Style Selector="Border.status-error">
            <Setter Property="Background" Value="Red" />
        </Style>
    </StackPanel.Styles>

    <Border Classes.status-ok="{Binding IsOnline}"
            Classes.status-error="{Binding !IsOnline}"
            Padding="8">
        <TextBlock Text="Service Status" />
    </Border>
</StackPanel>
```

### 非布尔条件请用转换器 {#using-a-converter-for-non-boolean-conditions}

若条件不是简单的布尔值，请使用值转换器：

```xml
<Border Background="{Binding Priority, Converter={StaticResource PriorityToBrushConverter}}" />
```

### 伪类与样式类组合使用 {#combining-pseudo-classes-with-style-classes}

圈定已套样式控件的某些交互状态：

```xml
<StackPanel.Styles>
    <Style Selector="Button.primary">
        <Setter Property="Background" Value="Blue" />
        <Setter Property="Foreground" Value="White" />
    </Style>
    <Style Selector="Button.primary:pointerover">
        <Setter Property="Background" Value="DarkBlue" />
    </Style>
    <Style Selector="Button.primary:pressed">
        <Setter Property="Background" Value="Navy" />
    </Style>
</StackPanel.Styles>
```

### 在自己的控件中定义伪类 {#custom-pseudo-classes-in-your-controls}

为你控件特有的状态定义自定义伪类：

```csharp
public class StatusIndicator : TemplatedControl
{
    public static readonly StyledProperty<bool> IsActiveProperty =
        AvaloniaProperty.Register<StatusIndicator, bool>(nameof(IsActive));

    public bool IsActive
    {
        get => GetValue(IsActiveProperty);
        set => SetValue(IsActiveProperty, value);
    }

    protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change)
    {
        base.OnPropertyChanged(change);
        if (change.Property == IsActiveProperty)
        {
            PseudoClasses.Set(":active", change.GetNewValue<bool>());
        }
    }
}
```

然后用伪类选择器为它写样式：

```xml
<Style Selector="local|StatusIndicator:active">
    <Setter Property="Background" Value="LimeGreen" />
</Style>
```

## 在代码中操作类 {#classes-in-code}

你可以在代码中通过 `Classes` 集合操作样式类：

```csharp
control.Classes.Add("blue");
control.Classes.Remove("red");
control.Classes.Toggle("highlight");

// Check if a class is present
if (control.Classes.Contains("blue"))
{
    // ...
}
```

## 另请参阅 {#see-also}

- [Styles](/docs/styling/styles)
- [Pseudoclasses](/docs/styling/pseudoclasses)
- [样式选择器](/docs/styling/style-selectors)
