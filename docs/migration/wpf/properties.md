---
id: properties
title: 属性
description: 把 WPF 的 DependencyProperty 用法迁移到 Avalonia 的 StyledProperty 与 DirectProperty。
doc-type: migration
---

Avalonia 的属性系统在概念上与 WPF 的 `DependencyProperty` 体系相仿，但 API 更干净、也更强类型。若你熟悉 WPF 的依赖属性，会发现 Avalonia 里大多数概念都还在：样式、数据绑定、动画、值继承和默认值统统经由属性系统实现。主要差别在于注册语法，以及如何响应属性变化。

## 属性类型对照 {#property-types-comparison}

WPF 只有一个 `DependencyProperty` 类，所有场景都用它。Avalonia 把它拆成三种类型，各自针对一类用途作了优化。三者共有一个基类 `AvaloniaProperty`。

| WPF | Avalonia | 适用场景 |
|---|---|---|
| `DependencyProperty` | `StyledProperty` | 参与样式、动画和值继承的属性 |
| `DependencyProperty` (read-only) | `DirectProperty` | 只读属性、对性能敏感的属性，或者包装某个 CLR 后备字段的属性 |
| `DependencyProperty.RegisterAttached` | `AttachedProperty` | 设在子元素上的属性（比如 `Grid.Row`、`DockPanel.Dock`） |

## Registration

### StyledProperty

在 WPF 中，你用一个静态字段加一次 `DependencyProperty.Register` 调用来注册 `DependencyProperty`；在 Avalonia 中，则改用 `AvaloniaProperty.Register<TOwner, TValue>`。

**WPF:**

```csharp
public class MyControl : Control
{
    public static readonly DependencyProperty BackgroundProperty =
        DependencyProperty.Register(
            nameof(Background),
            typeof(Brush),
            typeof(MyControl),
            new PropertyMetadata(Brushes.Transparent));

    public Brush Background
    {
        get => (Brush)GetValue(BackgroundProperty);
        set => SetValue(BackgroundProperty, value);
    }
}
```

**Avalonia:**

```csharp
public class MyControl : Control
{
    public static readonly StyledProperty<IBrush> BackgroundProperty =
        AvaloniaProperty.Register<MyControl, IBrush>(
            nameof(Background),
            defaultValue: Brushes.Transparent);

    public IBrush Background
    {
        get => GetValue(BackgroundProperty);
        set => SetValue(BackgroundProperty, value);
    }
}
```

注意 Avalonia 借助泛型省去了 `GetValue` 调用中的强制转换，而且默认值是作为具名参数传入的，不必再包一层元数据对象。

### DirectProperty

`DirectProperty` 直接读写 CLR 后备字段，不经 Avalonia 属性系统的值存储。因此它很适合只读属性，或者对性能要求极高的属性。WPF 中没有直接对应者，最接近的大概是只读的 `DependencyProperty`。

```csharp
public class MyControl : Control
{
    public static readonly DirectProperty<MyControl, string> StatusProperty =
        AvaloniaProperty.RegisterDirect<MyControl, string>(
            nameof(Status),
            o => o.Status);

    private string _status = "Ready";

    public string Status
    {
        get => _status;
        private set => SetAndRaise(StatusProperty, ref _status, value);
    }
}
```

要点：
- 用 `SetAndRaise` 而不是 `SetValue` 来更新后备字段并引发变更通知。
- getter 访问器 lambda（`o => o.Status`）是必需的，属性系统靠它读取当前值。

### AttachedProperty

附加属性在概念上的用法一致。WPF 用 `DependencyProperty.RegisterAttached`，Avalonia 则用 `AvaloniaProperty.RegisterAttached`。

**WPF:**

```csharp
public class DockPanel : Panel
{
    public static readonly DependencyProperty DockProperty =
        DependencyProperty.RegisterAttached(
            "Dock",
            typeof(Dock),
            typeof(DockPanel),
            new PropertyMetadata(Dock.Left));

    public static Dock GetDock(DependencyObject element)
        => (Dock)element.GetValue(DockProperty);

    public static void SetDock(DependencyObject element, Dock value)
        => element.SetValue(DockProperty, value);
}
```

**Avalonia:**

```csharp
public class DockPanel : Panel
{
    public static readonly AttachedProperty<Dock> DockProperty =
        AvaloniaProperty.RegisterAttached<DockPanel, Control, Dock>(
            "Dock",
            defaultValue: Dock.Left);

    public static Dock GetDock(Control element)
        => element.GetValue(DockProperty);

    public static void SetDock(Control element, Dock value)
        => element.SetValue(DockProperty, value);
}
```

## 属性变更回调 {#property-changed-callbacks}

### WPF 的做法 {#wpf-approach}

在 WPF 中，注册时要在 `PropertyMetadata` 里传一个 `PropertyChangedCallback`：

```csharp
public static readonly DependencyProperty IsActiveProperty =
    DependencyProperty.Register(
        nameof(IsActive),
        typeof(bool),
        typeof(MyControl),
        new PropertyMetadata(false, OnIsActiveChanged));

private static void OnIsActiveChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
{
    var control = (MyControl)d;
    control.UpdateVisualState();
}
```

### Avalonia approaches

Avalonia offers two ways to respond to property changes.

**Option 1: Override `OnPropertyChanged`**

The recommended approach for control authors is to override `OnPropertyChanged` on the control itself:

```csharp
protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change)
{
    base.OnPropertyChanged(change);

    if (change.Property == IsActiveProperty)
    {
        var newValue = change.GetNewValue<bool>();
        UpdateVisualState();
    }
}
```

**Option 2: Class handler via `Changed.AddClassHandler`**

You can also register a static class handler, typically in the control's static constructor. This is similar in spirit to the WPF `PropertyChangedCallback`, but it is registered separately from the property definition:

```csharp
static MyControl()
{
    IsActiveProperty.Changed.AddClassHandler<MyControl>((control, args) =>
    {
        control.UpdateVisualState();
    });
}
```

Both approaches are equivalent in effect. Overriding `OnPropertyChanged` is often cleaner when you need to handle changes to multiple properties in one place.

## 默认值 {#default-values}

In WPF, default values are supplied through a `PropertyMetadata` object:

```csharp
new PropertyMetadata(defaultValue: Brushes.White)
```

In Avalonia, the default value is a named parameter on the `Register` method:

```csharp
AvaloniaProperty.Register<MyControl, IBrush>(
    nameof(Background),
    defaultValue: Brushes.White);
```

If you need to override the default value in a derived class, use `OverrideDefaultValue` in the static constructor of the subclass:

```csharp
static MyDerivedControl()
{
    BackgroundProperty.OverrideDefaultValue<MyDerivedControl>(Brushes.Black);
}
```

## 取值强制转换 {#value-coercion}

In WPF, you supply a `CoerceValueCallback` in the `PropertyMetadata`:

```csharp
new PropertyMetadata(0.0, null, CoerceOpacity)
```

In Avalonia, pass a `coerce` function when registering the property:

```csharp
public static readonly StyledProperty<double> OpacityProperty =
    AvaloniaProperty.Register<MyControl, double>(
        nameof(Opacity),
        defaultValue: 1.0,
        coerce: CoerceOpacity);

private static double CoerceOpacity(AvaloniaObject sender, double value)
{
    return Math.Clamp(value, 0.0, 1.0);
}
```

The coercion function receives the `AvaloniaObject` instance and the proposed value, and returns the corrected value.

## Value precedence

Both WPF and Avalonia use a value precedence system to determine the effective value of a property. The general order (highest to lowest) is:

1. Animation
2. Local value
3. Style triggers / Style setters
4. Template parent
5. Inherited value
6. Default value

For a detailed breakdown of how Avalonia resolves property values, see the [Value Precedence](/docs/properties/value-precedence) page.

## 常见的坑 {#common-gotchas}

### No PropertyMetadata constructor with a default value

In WPF, you often write `new PropertyMetadata(someDefault)`. In Avalonia, there is no `PropertyMetadata` class. Default values are passed directly to `Register` using the `defaultValue:` named parameter.

### SetAndRaise replaces SetValue for DirectProperty

If you register a `DirectProperty`, you must use `SetAndRaise` in the CLR setter instead of `SetValue`. Calling `SetValue` on a `DirectProperty` will throw an exception.

```csharp
// Correct for DirectProperty
public string Status
{
    get => _status;
    private set => SetAndRaise(StatusProperty, ref _status, value);
}
```

### StyledProperty values live in the property system

Unlike `DirectProperty`, a `StyledProperty` does not use a backing field. Values are stored internally by the Avalonia property system. If you try to add a backing field and read from it, you will get stale data. Always use `GetValue` and `SetValue`.

### Use AddOwner instead of OverrideMetadata for shared properties

In WPF, you might call `OverrideMetadata` to reuse an existing `DependencyProperty` in a subclass with different metadata. In Avalonia, the equivalent pattern for sharing a property across unrelated types is `AddOwner`:

```csharp
public static readonly StyledProperty<IBrush> BackgroundProperty =
    Border.BackgroundProperty.AddOwner<MyControl>();
```

This registers the same property on your control type, and you can optionally override the default value at the same time:

```csharp
public static readonly StyledProperty<IBrush> BackgroundProperty =
    Border.BackgroundProperty.AddOwner<MyControl>(
        new StyledPropertyMetadata<IBrush>(Brushes.Gray));
```

## 另请参阅 {#see-also}

- [Avalonia property system](/docs/properties)
- [Value precedence](/docs/properties/value-precedence)
- [Defining properties on custom controls](/docs/custom-controls/defining-properties)
