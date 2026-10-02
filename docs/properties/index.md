---
id: index
title: Avalonia 属性系统
---

Avalonia 有自己的一套属性系统，是对标准 .NET 属性模型的扩展。Avalonia 属性支持样式、数据绑定、动画、属性值继承和变更通知。要编写自定义控件、要用好这个框架，就得先理解属性系统。

## 属性的种类 {#property-types}

Avalonia 定义了三种属性，各自适用于不同场景：

| Property Type | Base Class | Use Case |
|---|---|---|
| **Styled Property** | `StyledProperty<T>` | 参与样式系统的属性。这是最常用的一种。 |
| **Direct Property** | `DirectProperty<TOwner, TValue>` | 由普通 C# 字段承载、同时向 Avalonia 属性系统暴露以支持绑定的属性。用于性能敏感或只读的属性。 |
| **Attached Property** | `AttachedProperty<T>` | 可以设置在任意 [`AvaloniaObject`](/api/avalonia/avaloniaobject) 上的属性，通常由布局面板使用（例如 `Grid.Row`、`DockPanel.Dock`）。 |

## 样式化属性 {#styled-properties}

`StyledProperty` 是 Avalonia 中的标准属性类型。样式化属性的值存放在 Avalonia 属性系统里（而非支持字段中），因此能够参与样式、动画和取值优先级的运作。

### 注册样式化属性 {#registering-a-styled-property}

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

`Register` 方法接受以下参数：

| 参数 | 说明 |
|---|---|
| `name` | 属性名，必须与 CLR 属性名一致。 |
| `defaultValue` | 属性的默认值。 |
| `inherits` | 属性值是否沿视觉树向下继承。 |
| `defaultBindingMode` | 默认绑定模式（`OneWay`、`TwoWay`、`OneTime`、`OneWayToSource`）。 |
| `validate` | 一个函数，对永远不合法的取值返回 `false`。 |
| `coerce` | 一个在取值生效前对其进行调整的函数（见[元数据与回调](/docs/properties/metadata-and-callbacks)）。 |

### 复用已有的属性 {#reusing-an-existing-property}

如果你需要的属性已由别的控件定义过，就用 `AddOwner` 而不要重新注册一个：

```csharp
public class MyControl : Control
{
    public static readonly StyledProperty<IBrush?> BackgroundProperty =
        Border.BackgroundProperty.AddOwner<MyControl>();

    public IBrush? Background
    {
        get => GetValue(BackgroundProperty);
        set => SetValue(BackgroundProperty, value);
    }
}
```

这样可以保证属性身份唯一，于是针对 `Background` 的样式对所有共用该属性的控件都有效。

## 直接属性 {#direct-properties}

`DirectProperty` 由普通的 C# 字段承载，Avalonia 属性系统通过你提供的 getter 和 setter 委托来读写它。以下情形适合用直接属性：

- 你需要一个不参与样式的属性（例如 `ItemsControl` 上的 `Items`）。
- 你需要一个只读属性。
- 你想避开样式化属性值存储的开销。

### 注册直接属性 {#registering-a-direct-property}

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

:::info
在 setter 中请用 `SetAndRaise`，不要直接给字段赋值。这个方法一次调用就同时更新支持字段并引发属性变更通知。
:::

### 只读的直接属性 {#read-only-direct-properties}

省略 setter 委托即可创建只读属性：

```csharp
public static readonly DirectProperty<MyControl, bool> IsActiveProperty =
    AvaloniaProperty.RegisterDirect<MyControl, bool>(
        nameof(IsActive),
        o => o.IsActive);
```

### 与样式化属性的主要差别 {#key-differences-from-styled-properties}

| 行为 | Styled Property | Direct Property |
|---|---|---|
| 参与样式 | Yes | No |
| 参与动画 | Yes | No |
| 支持取值优先级 | Yes | 否（只有单一取值） |
| 可继承取值 | Yes | No |
| 支持强制转换 | Yes | No |
| 性能 | 需查属性存储 | 直接访问字段 |
| 可以只读 | No | Yes |

## 附加属性 {#attached-properties}

`AttachedProperty` 是一种可以设置在任意 `AvaloniaObject` 上的样式化属性。附加属性通常由父级布局面板定义，设置在它的子元素上。

### 注册附加属性 {#registering-an-attached-property}

```csharp
public class MyPanel : Panel
{
    public static readonly AttachedProperty<int> ColumnProperty =
        AvaloniaProperty.RegisterAttached<MyPanel, Control, int>("Column", defaultValue: 0);

    public static int GetColumn(Control element) => element.GetValue(ColumnProperty);
    public static void SetColumn(Control element, int value) => element.SetValue(ColumnProperty, value);
}
```

### 在 XAML 中使用附加属性 {#using-an-attached-property-in-xaml}

```xml
<local:MyPanel>
    <Button local:MyPanel.Column="1" Content="In column 1" />
</local:MyPanel>
```

## 读取与设置取值 {#getting-and-setting-values}

所有 Avalonia 属性都通过 `AvaloniaObject` 基类来读写：

```csharp
// Get a property value
double radius = myControl.GetValue(MyControl.CornerRadiusProperty);

// Set a property value
myControl.SetValue(MyControl.CornerRadiusProperty, 8.0);

// Clear a property value (revert to default/styled value)
myControl.ClearValue(MyControl.CornerRadiusProperty);
```

## 观察属性变化 {#observing-property-changes}

可以观察某个具体对象上的属性变化：

```csharp
// Subscribe to changes using GetObservable
myControl.GetObservable(MyControl.CornerRadiusProperty)
    .Subscribe(newValue => Console.WriteLine($"CornerRadius changed to {newValue}"));
```

也可以在控件类中重写 `OnPropertyChanged`：

```csharp
protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change)
{
    base.OnPropertyChanged(change);

    if (change.Property == CornerRadiusProperty)
    {
        var oldValue = change.GetOldValue<double>();
        var newValue = change.GetNewValue<double>();
        // React to the change
    }
}
```

## 另请参阅 {#see-also}

- [取值优先级](/docs/properties/value-precedence)：了解 Avalonia 如何在样式、动画和本地取值之间裁决出最终值。
- [元数据与回调](/docs/properties/metadata-and-callbacks)：了解默认值、强制转换与校验。
- [属性值继承](/docs/properties/property-value-inheritance)：了解属性如何从祖先控件继承取值。
- [定义属性](/docs/custom-controls/defining-properties)：为自定义控件添加属性的实用指南。
- [附加属性](/docs/custom-controls/defining-properties#attached-properties)：创建附加属性的实用指南。
