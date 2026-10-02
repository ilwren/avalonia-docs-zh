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

### Avalonia 的做法 {#avalonia-approaches}

Avalonia 提供了两种响应属性变化的方式。

**Option 1: Override `OnPropertyChanged`**

对控件作者来说，推荐的做法是在控件自身上重写 `OnPropertyChanged`：

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

**方案二：通过 `Changed.AddClassHandler` 注册类处理程序**

你也可以注册一个静态的类处理程序，通常写在控件的静态构造函数里。它在精神上类似 WPF 的 `PropertyChangedCallback`，只是与属性定义分开注册：

```csharp
static MyControl()
{
    IsActiveProperty.Changed.AddClassHandler<MyControl>((control, args) =>
    {
        control.UpdateVisualState();
    });
}
```

两种做法效果等价。若你想把多个属性的变化集中在一处处理，重写 `OnPropertyChanged` 往往更清爽。

## 默认值 {#default-values}

在 WPF 中，默认值通过一个 `PropertyMetadata` 对象提供：

```csharp
new PropertyMetadata(defaultValue: Brushes.White)
```

在 Avalonia 中，默认值是 `Register` 方法上的一个具名参数：

```csharp
AvaloniaProperty.Register<MyControl, IBrush>(
    nameof(Background),
    defaultValue: Brushes.White);
```

若要在派生类中改写默认值，请在子类的静态构造函数里调用 `OverrideDefaultValue`：

```csharp
static MyDerivedControl()
{
    BackgroundProperty.OverrideDefaultValue<MyDerivedControl>(Brushes.Black);
}
```

## 取值强制转换 {#value-coercion}

在 WPF 中，你要在 `PropertyMetadata` 里提供一个 `CoerceValueCallback`：

```csharp
new PropertyMetadata(0.0, null, CoerceOpacity)
```

在 Avalonia 中，注册属性时传入一个 `coerce` 函数即可：

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

强制回调会收到 `AvaloniaObject` 实例和待设的值，并返回修正后的值。

## 值优先级 {#value-precedence}

WPF 和 Avalonia 都用一套值优先级体系来决定属性的最终生效值。大致顺序（由高到低）为：

1. Animation
2. 本地值
3. 样式触发器 / 样式 setter
4. 模板父级
5. 继承值
6. 默认值

想详细了解 Avalonia 如何裁定属性值，请看[值优先级](/docs/properties/value-precedence)页。

## 常见的坑 {#common-gotchas}

### 没有带默认值的 PropertyMetadata 构造函数 {#no-propertymetadata-constructor-with-a-default-value}

在 WPF 中你常写 `new PropertyMetadata(someDefault)`。Avalonia 根本没有 `PropertyMetadata` 类，默认值直接通过具名参数 `defaultValue:` 传给 `Register`。

### DirectProperty 要用 SetAndRaise 而非 SetValue {#setandraise-replaces-setvalue-for-directproperty}

若你注册的是 `DirectProperty`，CLR setter 里必须用 `SetAndRaise` 而不是 `SetValue`。对 `DirectProperty` 调用 `SetValue` 会抛异常。

```csharp
// Correct for DirectProperty
public string Status
{
    get => _status;
    private set => SetAndRaise(StatusProperty, ref _status, value);
}
```

### StyledProperty 的值存在属性系统里 {#styledproperty-values-live-in-the-property-system}

与 `DirectProperty` 不同，`StyledProperty` 不使用后备字段，值由 Avalonia 属性系统在内部保存。若你擅自加个后备字段再从中读取，拿到的会是过时数据。请始终使用 `GetValue` 和 `SetValue`。

### 共享属性请用 AddOwner，而不是 OverrideMetadata {#use-addowner-instead-of-overridemetadata-for-shared-properties}

在 WPF 中，你也许会调用 `OverrideMetadata`，让子类以不同的元数据复用现有的 `DependencyProperty`。在 Avalonia 中，要在互不相关的类型间共享属性，对应的套路是 `AddOwner`：

```csharp
public static readonly StyledProperty<IBrush> BackgroundProperty =
    Border.BackgroundProperty.AddOwner<MyControl>();
```

这会把同一个属性注册到你的控件类型上，同时还可以顺带改写默认值：

```csharp
public static readonly StyledProperty<IBrush> BackgroundProperty =
    Border.BackgroundProperty.AddOwner<MyControl>(
        new StyledPropertyMetadata<IBrush>(Brushes.Gray));
```

## 另请参阅 {#see-also}

- [Avalonia 属性系统](/docs/properties)
- [值优先级](/docs/properties/value-precedence)
- [在自定义控件上定义属性](/docs/custom-controls/defining-properties)
