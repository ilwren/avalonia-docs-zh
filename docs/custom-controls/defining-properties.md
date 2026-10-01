---
id: defining-properties
title: 为自定义控件定义属性
sidebar_label: 定义属性
description: 在 Avalonia 自定义控件上定义样式化属性、直接属性或附加属性。
doc-type: how-to
---

import DefiningPropertyPreviewScreenshot from '/img/custom-controls/defining-property-preview.png';
import DataValidationCustomControl from '/img/custom-controls/data-validation-custom-control.png';

编写自定义控件时，你可以给它加下列几类属性。本文逐一介绍每种属性的注册和用法，帮你为自己的控件挑对类型。

1. [样式化属性](#styled-properties)：由 Avalonia 的样式系统赋值。
2. [直接属性](#direct-properties)：有一个 C# 后备字段，支持数据绑定。
3. [附加属性](#attached-properties)：承载在单独的容器类中，再于 XAML 中配置。

## 样式化属性 {#styled-properties}

样式化属性的值存在 Avalonia 属性系统里，而不是后备字段中。因此它能参与样式、动画和值优先级的运作。若你希望使用者能为该属性设样式或加动画，就选样式化属性。

:::info
关于在 Avalonia 中使用样式的更多内容，请参阅[样式](/docs/styling/styles)指南。
:::

### 命名约定 {#naming-conventions}

静态字段必须遵循 `[PropertyName]Property` 的命名范式，比如 `BackgroundProperty`、`FontWeightProperty`。Avalonia 正是靠这一约定自动把 XAML 特性映射到属性上。

不遵守这一命名约定，编译时可能报出 "Unable to find suitable setter or adder for property" 错误。

```csharp title="C#"
public static readonly StyledProperty<double> CornerRadiusProperty = ...
```

```xml title="XAML"
<local:MyControl CornerRadius="8" />
```

### 注册样式化属性 {#registering-a-styled-property}

注册样式化属性的步骤：

1. 添加一个 `StyledProperty<T>` 类型的 `static readonly` 字段。
2. 用 `AvaloniaProperty.Register` 方法来注册。
3. 提供一对 CLR getter 和 setter，分别调用 `GetValue` 和 `SetValue`。

下面的例子注册了一个默认值为 `0.0` 的 `CornerRadius` 样式化属性：

```csharp
public class MyControl : Control
{
    public static readonly StyledProperty<double> CornerRadiusProperty =
        AvaloniaProperty.Register<MyControl, double>(nameof(CornerRadius), defaultValue: 0.0);

    public double CornerRadius
    {
        get => GetValue(CornerRadiusProperty);
        set => SetValue(CornerRadiusProperty, value);
    }
}
```

:::warning
CLR 属性的 getter/setter **只应**调用 `GetValue` 和 `SetValue`，别在里面塞别的逻辑——因为有些属性变更压根不走 CLR 属性这条路。
:::

`Register` 方法接受下列可选参数：

| 参数 | 说明 |
|---|---|
| `name` | 属性名，必须与 CLR 属性名一致。 |
| `defaultValue` | 属性的默认值。 |
| `inherits` | 该值是否沿视觉树向下继承。 |
| `defaultBindingMode` | 默认绑定模式（`OneWay`、`TwoWay`、`OneTime` 或 `OneWayToSource`）。 |
| `validate` | 一个函数，对应当拒绝的值返回 `false`。 |
| `coerce` | 一个函数，在值被真正应用之前对其作出调整。 |

### 复用已有的样式化属性 {#reusing-an-existing-styled-property}

如果你想用的属性已由别的控件定义过（比如 `Border` 上的 `Background`），就不必重新注册，用 `AddOwner` 即可。这样一来两者共用同一个属性标识，针对该属性的样式对所有共用它的控件都生效。

```csharp
public class MyCustomControl : Control
{
    public static readonly StyledProperty<IBrush?> BackgroundProperty =
        Border.BackgroundProperty.AddOwner<MyCustomControl>();

    public IBrush? Background
    {
        get => GetValue(BackgroundProperty);
        set => SetValue(BackgroundProperty, value);
    }
}
```

### 为自定义属性设样式 {#styling-a-custom-property}

样式化属性一经注册，使用者就能在 XAML 中选中它并设置样式。下面的例子通过样式设置了某个自定义控件的 `Background`：

<Tabs>

<TabItem value="xaml" label="MainWindow.axaml">

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:cc="using:AvaloniaCCExample.CustomControls"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d" d:DesignWidth="800" d:DesignHeight="450"
        x:Class="AvaloniaCCExample.MainWindow"
        Title="Avalonia Custom Control">

  <Window.Styles>
    <Style Selector="cc|MyCustomControl">
      <Setter Property="Background" Value="Yellow"/>
    </Style>
  </Window.Styles>

  <cc:MyCustomControl Height="200" Width="300"/>

</Window>
```

</TabItem>

<TabItem value="csharp" label="MyCustomControl.cs">

```csharp
using Avalonia;
using Avalonia.Controls;
using Avalonia.Media;

namespace AvaloniaCCExample.CustomControls
{
    public class MyCustomControl : Control
    {
        public static readonly StyledProperty<IBrush?> BackgroundProperty =
            Border.BackgroundProperty.AddOwner<MyCustomControl>();

        public IBrush? Background
        {
            get { return GetValue(BackgroundProperty); }
            set { SetValue(BackgroundProperty, value); }
        }

        public sealed override void Render(DrawingContext context)
        {
            if (Background != null)
            {
                var renderSize = Bounds.Size;
                context.FillRectangle(Background, new Rect(renderSize));
            }
            base.Render(context);
        }
    }
}
```

</TabItem>

</Tabs>

<Image light={DefiningPropertyPreviewScreenshot} alt="Preview of a custom control with a defined property" position="center" maxWidth={400} cornerRadius="true"/>

## 直接属性 {#direct-properties}

直接属性由一个常规 C# 字段支撑。它不参与样式和动画，但支持数据绑定和变更通知。下列情形适合用直接属性：

- 你需要一个**只读**属性。（样式化属性没法做成只读。）
- 你想要**更好的性能**。（直接属性的值是从字段直接读取的。）
- 你想要一个**不可被设样式**的属性。

### 注册直接属性 {#registering-a-direct-property}

使用 `AvaloniaProperty.RegisterDirect`，并提供指向后备字段的 getter 和 setter 委托：

```csharp
public class MyControl : Control
{
    public static readonly DirectProperty<MyControl, string?> StatusProperty =
        AvaloniaProperty.RegisterDirect<MyControl, string?>(
            nameof(Status),
            o => o.Status,
            (o, v) => o.Status = v);

    private string? _status;

    public string? Status
    {
        get => _status;
        set => SetAndRaise(StatusProperty, ref _status, value);
    }
}
```

:::warning
CLR setter 中请一律使用 `SetAndRaise`，不要直接给后备字段赋值。`SetAndRaise` 一次调用就同时完成了更新字段和触发属性变更通知两件事。对直接属性调用 `SetValue` 会抛异常。
:::

### 只读的直接属性 {#read-only-direct-properties}

要做只读属性，注册时省去 setter 委托，并把 CLR setter 保持为 `private`：

```csharp
public class MyControl : Control
{
    public static readonly DirectProperty<MyControl, bool> IsActiveProperty =
        AvaloniaProperty.RegisterDirect<MyControl, bool>(
            nameof(IsActive),
            o => o.IsActive);

    private bool _isActive;

    public bool IsActive
    {
        get => _isActive;
        private set => SetAndRaise(IsActiveProperty, ref _isActive, value);
    }
}
```

## 样式化属性与直接属性的对比 {#styled-vs-direct-properties}

| 行为 | 样式化属性 | 直接属性 |
|---|---|---|
| 参与样式 | Yes | No |
| 参与动画 | Yes | No |
| 支持取值优先级 | Yes | 否（只有单一取值） |
| 可继承取值 | Yes | No |
| 支持强制转换 | Yes | No |
| 性能 | 需查属性存储 | 直接访问字段 |
| 可以只读 | No | Yes |

## 响应属性变化 {#responding-to-property-changes}

无论样式化属性还是直接属性，都可以在控件中重写 `OnPropertyChanged` 来响应属性值的变化。

下面这个例子演示如何响应背景变化：[让视觉失效](/docs/custom-controls/custom-drawn-controls#manual-invalidation)，从而刷新成新的背景。

```csharp
protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change)
{
    base.OnPropertyChanged(change);

    if (change.Property == BackgroundProperty)
    {
        // Invalidate the visual so the control repaints with the new background.
        InvalidateVisual();
    }
}
```

## 数据校验支持 {#data-validation-support}

数据校验让控件能在检测到所绑定的属性无效时显示错误。

从 [Avalonia v12](/docs/avalonia12-breaking-changes) 起，用 `enableDataValidation: true` 注册的属性会自动报告校验错误。（也就是说，旧版 Avalonia 中那种重写 `UpdateDataValidation` 去调用 `DataValidationErrors.SetError` 的写法不再需要了。）

给自定义控件加上数据校验的步骤：

1. 注册属性时带上 `enableDataValidation: true`。
2. 把自定义控件包进 [`DataValidationErrors`](/api/avalonia/controls/datavalidationerrors) 控件，错误才能显示给用户看。
3. 视需要为 `:error` 伪类设置样式，让数据无效时控件的外观有所变化。

关于 Avalonia 数据校验的整体介绍，请参阅[数据绑定中的校验](/docs/data-binding/binding-validation)。

### 为属性启用数据校验 {#enabling-data-validation-on-a-property}

`enableDataValidation` 对[样式化属性](#styled-properties)和[直接属性](#direct-properties)都适用。无论你是用 `Register` 注册新属性，还是用 `AddOWner` 复用已有属性，设置方式都一样。

:::warning
你必须给该属性设置 `BindingMode.TwoWay`，因为数据校验正是靠把值回传给绑定源来工作的。
:::

```csharp
public static readonly StyledProperty<int> ValueProperty =
    AvaloniaProperty.Register<QuantityStepper, int>(nameof(Value),
        defaultValue: 1,
        // highlight-next-line
        defaultBindingMode: BindingMode.TwoWay,
        enableDataValidation: true);
```

### 用 `DataValidationErrors` 显示错误 {#displaying-errors-with-datavalidationerrors}

要把数据校验错误显示给用户，请把自定义控件包进 [`DataValidationErrors`](/api/avalonia/controls/datavalidationerrors) 控件。`DataValidationErrors` 是一个 `ContentControl`，它提供了处理错误状态的附加属性。

对[用户控件](/controls/primitives/usercontrol)，把 `DataValidationErrors` 放进 `<UserControl>` 中使用；对[模板化控件](/docs/custom-controls/templated-controls)，则放进 `<ControlTemplate>` 中。

```xml
<ControlTemplate> / <UserControl>
  <DataValidationErrors>
    <!-- your control's visuals -->
  </DataValidationErrors>
</ControlTemplate> / </UserControl>
```

控件存在错误期间，`DataValidationErrors` 会置上 `:error` 伪类。用 `Style` 选中这个伪类，即可定制控件处于错误状态时的外观。

<Tabs>

<TabItem value="usercontrol" label="User control example">

```xml
<UserControl.Styles>
    <Style Selector="local|MyCustomControl:error Border#Frame">
        <Setter Property="BorderBrush" Value="Red" />
    </Style>
</UserControl.Styles>
```

</TabItem>

<TabItem value="templatedcontrol" label="Templated control example">

```xml
<ControlTheme>
    <Style Selector="^:error /template/ Border#PART_Border">
        <Setter Property="BorderBrush" Value="Red" />
    </Style>
</ControlTheme>
```

</TabItem>

</Tabs>

### 数据校验示例 {#data-validation-example}

下面的例子做了一个 `QuantitySelector` 控件，用 **+** 和 **-** 按钮设置数值。数据校验启用在 `Value` 这个样式化属性上，它表示选择器当前的数字，绑定到一个会拒绝 1–10 范围之外数量的视图模型。一旦设成无效值就会触发错误状态：边框变红，并显示一条错误消息。

<Image light={DataValidationCustomControl} maxWidth={250} cornerRadius="true" position="center" alt="A numeric selector showing the number 11. The selector is highlighted in yellow and a text error message is shown underneath." />
<br />

<Tabs>

<TabItem value="custom-control-xaml" label="QuantitySelector.axaml">

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:local="using:ValidationDemo"
             x:Class="ValidationDemo.QuantitySelector"
             x:Name="root">

    <UserControl.Styles>
        <!-- Set the default color in Styles, not in the control itself.
             Colors set directly in the control override the :error style. -->
        <Style Selector="Border#Frame">
            <Setter Property="BorderBrush" Value="Gray" />
        </Style>
        <!-- Set the :error pseudoclass on the QuantitySelector. -->
        <Style Selector="local|QuantitySelector:error Border#Frame">
            <Setter Property="BorderBrush" Value="Red" />
        </Style>
    </UserControl.Styles>

    <DataValidationErrors Owner="{Binding #root}">
       <!-- Custom control layout goes inside DataValidationErrors. -->
       <Border x:Name="Frame" BorderThickness="1"
                CornerRadius="4" Padding="4">
           <StackPanel Orientation="Horizontal" Spacing="8">
                <Button Content="-" Click="DecreaseButtonClick" Width="32"/>
                <TextBlock Text="{Binding #root.Value}"
                           MinWidth="24" TextAlignment="Center"
                           VerticalAlignment="Center"/>
               <Button Content="+" Click="IncreaseButtonClick" Width="32"/>
            </StackPanel>
       </Border>
    </DataValidationErrors>

</UserControl>
```

</TabItem>

<TabItem value="custom-control-code-behind" label="QuantitySelector.axaml.cs">

```csharp
using Avalonia;
using Avalonia.Controls;
using Avalonia.Data;
using Avalonia.Interactivity;

namespace ValidationDemo;

public partial class QuantitySelector : UserControl
{
    public QuantitySelector()
    {
        InitializeComponent();
    }
    
    // Register Value as a new styled property.

    public static readonly StyledProperty<int> ValueProperty =
        AvaloniaProperty.Register<QuantitySelector, int>(
            nameof(Value),
            defaultValue: 1,
            defaultBindingMode: BindingMode.TwoWay,
            enableDataValidation: true);

    // Provide a getter and setter for Value.
    public int Value
    {
        get => GetValue(ValueProperty);
        set => SetValue(ValueProperty, value);
    }
    
    // Create events for the buttons to decrease or increase Value.
    private void DecreaseButtonClick(object? sender, RoutedEventArgs e)
    {
        Value--;
    }

    private void IncreaseButtonClick(object? sender, RoutedEventArgs e)
    {
        Value++;
    }
}
```

</TabItem>

<TabItem value="view-model" label="MainWindowViewModel.cs">

```csharp
using System;
using System.Collections;
using System.ComponentModel;

namespace ValidationDemo.ViewModels;

// View model implements INotifyPropertyChanged and INotifyDataErrorInfo to process data validation.
public partial class MainWindowViewModel : ViewModelBase, INotifyPropertyChanged, INotifyDataErrorInfo
{
    private int _quantity = 1;

    // Tell the binding to read the property for errors. 
    public int Quantity
    {
        get => _quantity;
        set
        {
            if (_quantity == value)
                return;

            _quantity = value;
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Quantity)));

            ErrorsChanged?.Invoke(this, new DataErrorsChangedEventArgs(nameof(Quantity)));
        }
    }

    // Define error conditions and the error message to display.
    public bool HasErrors => _quantity is < 1 or > 10;

    public IEnumerable GetErrors(string? propertyName)
    {
        if (propertyName == nameof(Quantity) && HasErrors)
            return new[] { "Quantity must be between 1 and 10." };

        return Array.Empty<string>();
    }

    public event PropertyChangedEventHandler? PropertyChanged;
    public event EventHandler<DataErrorsChangedEventArgs>? ErrorsChanged;
}
```

</TabItem>

<TabItem value="main-window" label="MainWindow.axaml">

```xml
<!-- Ensure DataType is coming from the view model where Quantity is defined. -->
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:vm="using:ValidationDemo.ViewModels"
        xmlns:local="using:ValidationDemo"
        x:Class="ValidationDemo.Views.MainWindow"
        x:DataType="vm:MainWindowViewModel"
        Title="ValidationDemo">

    <!-- Put the custom control in the main window and bind Value to Quantity. -->
    <StackPanel Margin="20" Spacing="8">
        <TextBlock Text="Quantity (1-10 only):"/>
        <local:QuantitySelector Value="{Binding Quantity}" />
    </StackPanel>

</Window>

```

</TabItem>

</Tabs>

## 附加属性 {#attached-properties}

附加属性住在自己的容器类里，并在 XAML 中配置到兼容的控件上。于是你可以拥有一些不属于自定义控件自身控件类的额外属性。举个例子，你可能想用附加属性让子元素在父级自定义控件内指定自己的布局位置。（实战例子见[自定义面板](/docs/custom-controls/custom-panel#adding-an-attached-property)。）

### 命名约定 {#naming-conventions-1}

- 和样式化属性一样，附加属性的静态字段也遵循 `[PropertyName]Property` 的命名范式。
- name 参数只写 `[PropertyName]`（不带 `Property` 后缀）。

### 注册附加属性 {#registering-an-attached-property}

1. 添加一个继承自 `AvaloniaObject` 的新容器类。
2. 用 `AvaloniaProperty.RegisterAttached` 方法注册这个附加属性。
3. 提供一对 CLR getter 和 setter，分别调用 `GetValue` 和 `SetValue`。
4. 按需进一步定义该属性的行为。

下面的例子在独立文件 `DimExtensions.cs` 中创建了一个名为 `IsDimmed` 的附加属性。它是个布尔属性，为 `True` 时把控件按 50% 不透明度渲染。

```csharp title="DimExtensions.cs"
using Avalonia;
using Avalonia.Controls;

namespace MyApp;

// Attached properties live in a container class that inherits from AvaloniaObject.
public class DimExtensions : AvaloniaObject
{
    // Register the attached property. The type arguments are:
    //    <owner class, type it can be set on, value type>.
    public static readonly AttachedProperty<bool> IsDimmedProperty =
        AvaloniaProperty.RegisterAttached<DimExtensions, Control, bool>("IsDimmed");

    // Provide static getter and setter. The XAML system finds these by name.
    public static void SetIsDimmed(Control element, bool value) =>
        element.SetValue(IsDimmedProperty, value);

    public static bool GetIsDimmed(Control element) =>
        element.GetValue(IsDimmedProperty);

    // React when the value changes.
    static DimExtensions()
    {
        IsDimmedProperty.Changed.AddClassHandler<Control>((control, _) =>
            control.Opacity = GetIsDimmed(control) ? 0.5 : 1.0);
    }
}
```

### 在 XAML 中使用附加属性 {#using-the-attached-property-in-xaml}

先在 XAML 中声明命名空间，然后用点号写法设置附加属性。

下面的例子把上一节的 `IsDimmed` 附加属性用在了两个按钮上。第二个按钮因为被设了 `IsDimmed=True`，所以以半透明渲染。

```xml title="MainWindow.axaml"
<StackPanel>
    <Button Content="Normal" />
    <Button Content="Dimmed" local:DimExtensions.IsDimmed="True" />
</StackPanel>
```

## 常见问题 {#common-pitfalls}

- **名字对不上。**传给 `Register` 的 `name` 实参必须与 CLR 属性名完全一致，对不上就会在运行时报错。
- **对直接属性用 `SetValue`。**直接属性必须用 `SetAndRaise`，调用 `SetValue` 会抛出 `InvalidOperationException`。
- **给样式化属性加后备字段。**样式化属性的值存在 Avalonia 属性系统中，你若从本地字段读取，拿到的就是过期数据。请始终使用 `GetValue` 和 `SetValue`。
- **忘了调用 `base.OnPropertyChanged`。**重写 `OnPropertyChanged` 时，务必先调用基类实现，框架才能处理这次变更。

## 另请参阅 {#see-also}

- [Avalonia 属性系统](/docs/properties)：样式化属性、直接属性和附加属性的完整参考。
- [属性值优先级](/docs/properties/value-precedence)：Avalonia 如何在相互竞争的属性值之间作裁决。
- [元数据与回调](/docs/properties/metadata-and-callbacks)：默认值、强制转换和校验。
- [数据绑定中的校验](/docs/data-binding/binding-validation)：视图模型可用的几种校验方式，以及如何定制错误的呈现。
- [定义事件](/docs/custom-controls/defining-events)：给自定义控件添加路由事件。
- [创建自定义控件](/docs/custom-controls)：可以添加属性的各类自定义控件概览。
