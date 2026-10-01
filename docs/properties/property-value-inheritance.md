---
id: property-value-inheritance
title: 属性值继承
description: Avalonia 属性如何在视觉树中由父元素向后代传播取值，内置的可继承属性有哪些，以及如何自定义可继承属性。
doc-type: explanation
---

属性值继承，指的是设置在父元素上的属性值会沿视觉树向下传播给后代，后代不必逐个显式设置。`FontSize`、`FontFamily`、`Foreground`、`FlowDirection` 等属性常用到这一机制。

## 运作原理 {#how-it-works}

若某个 Avalonia 属性在注册时带了 `inherits: true`，那么当前元素上没有本地值、样式值或动画值时，属性系统就会沿视觉树向上查看祖先元素。第一个为该属性提供了取值的祖先，就是继承值的来源。

在[取值优先级](/docs/properties/value-precedence)体系中，继承值的优先级最低（仅高于 `Unset`）。子元素上的本地值、样式或动画，总是会覆盖继承来的值。

## 内置的可继承属性 {#built-in-inherited-properties}

Avalonia 中有若干常用属性注册为可继承：

| 属性 | 定义于 | 效果 |
|---|---|---|
| `FontFamily` | [`TextElement`](/api/avalonia/controls/documents/textelement) | 文本控件从父级继承字体族。 |
| `FontSize` | `TextElement` | 文本控件从父级继承字号。 |
| `FontStyle` | `TextElement` | 文本控件继承字体样式（倾斜、常规）。 |
| `FontWeight` | `TextElement` | 文本控件继承字重（加粗、常规）。 |
| `Foreground` | `TextElement` | 文本控件继承前景画刷。 |
| `LetterSpacing` | `TextElement` | 文本控件继承字符间距。 |
| `FlowDirection` | `Visual` | 控件继承从左到右或从右到左的布局方向。 |
| `DataContext` | `StyledElement` | 控件从父级继承数据上下文。 |
| `RequestedThemeVariant` | `ThemeVariantScope` | 控件继承所请求的主题变体（浅色/深色）。 |

## Example

在父元素上设置 `FontSize`，会让所有未自行设置 `FontSize` 的后代文本控件都用上这个值：

```xml
<StackPanel FontSize="18">
    <!-- Inherits FontSize="18" -->
    <TextBlock Text="Large text" />

    <!-- Overrides with its own FontSize -->
    <TextBlock Text="Small text" FontSize="12" />

    <!-- Also inherits FontSize="18" -->
    <Button Content="Large button text" />
</StackPanel>
```

## 创建可继承属性 {#creating-an-inherited-property}

要让自定义属性具备继承能力，注册时设置 `inherits: true`：

```csharp
public class MyControl : Control
{
    public static readonly StyledProperty<bool> IsCompactProperty =
        AvaloniaProperty.Register<MyControl, bool>(
            nameof(IsCompact),
            defaultValue: false,
            inherits: true);

    public bool IsCompact
    {
        get => GetValue(IsCompactProperty);
        set => SetValue(IsCompactProperty, value);
    }
}
```

这样 `MyControl` 的任何后代都能读到 `IsCompact` 的值。若该后代同样是 `MyControl`（或者已为该属性追加了所有权），它就会自动收到继承来的值。

### 让其他类型的后代也能用上该属性 {#making-the-property-available-to-descendants}

要让不同类型的后代也能读取这个可继承属性，它们需要注册所有权：

```csharp
public class MyChildControl : Control
{
    public static readonly StyledProperty<bool> IsCompactProperty =
        MyControl.IsCompactProperty.AddOwner<MyChildControl>();

    public bool IsCompact
    {
        get => GetValue(IsCompactProperty);
        set => SetValue(IsCompactProperty, value);
    }
}
```

## 继承与 `DataContext` {#inheritance-and-datacontext}

`DataContext` 是最重要的可继承属性之一。你在 `Window` 上设置 `DataContext` 之后，该窗口内的所有控件都会继承它：

```csharp
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        DataContext = new MainWindowViewModel();
    }
}
```

```xml
<!-- All controls in the window inherit the DataContext -->
<Window>
    <StackPanel>
        <!-- Binds to MainWindowViewModel.Name -->
        <TextBlock Text="{Binding Name}" />

        <!-- Binds to MainWindowViewModel.Email -->
        <TextBox Text="{Binding Email}" />
    </StackPanel>
</Window>
```

## 另请参阅 {#see-also}

- [属性系统总览](/docs/properties)：属性种类与注册方式总览。
- [取值优先级](/docs/properties/value-precedence)：继承值在优先级序列中的位置。
- [数据上下文](/docs/data-binding/data-context)：DataContext 这个可继承属性如何与数据绑定配合。
