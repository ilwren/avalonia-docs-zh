---
id: metadata-and-callbacks
title: 元数据与回调
---

每个 Avalonia 属性都带有一份元数据，用来控制它的默认值、绑定行为以及可选的强制转换逻辑。你可以在注册属性时指定元数据，也可以在派生类型中覆盖它。

## 样式化属性的元数据 {#styled-property-metadata}

`StyledPropertyMetadata<T>` 类控制着样式化属性的行为：

| 参数 | 类型 | 说明 |
|---|---|---|
| `defaultValue` | `T` | 属性的默认值。当没有任何其他取值来源提供值时使用它。 |
| `defaultBindingMode` | `BindingMode` | 绑定未显式指定模式时所采用的绑定模式。 |
| `coerce` | `Func<AvaloniaObject, T, T>?` | 一个回调，可在取值生效前对其进行调整或施加约束。 |
| `enableDataValidation` | `bool` | 该属性是否参与数据校验。 |

## 默认值 {#default-values}

注册属性时指定默认值：

```csharp
public static readonly StyledProperty<double> OpacityProperty =
    AvaloniaProperty.Register<MyControl, double>(nameof(Opacity), defaultValue: 1.0);
```

### 覆盖默认值 {#overriding-default-values}

派生控件可以改变继承而来的属性的默认值：

```csharp
public class MySpecialButton : Button
{
    static MySpecialButton()
    {
        // Change the default Background for MySpecialButton
        BackgroundProperty.OverrideDefaultValue<MySpecialButton>(Brushes.LightBlue);
    }
}
```

覆盖时也可以提供一整份元数据：

```csharp
static MySpecialButton()
{
    BackgroundProperty.OverrideMetadata<MySpecialButton>(
        new StyledPropertyMetadata<IBrush?>(Brushes.LightBlue));
}
```

:::caution
元数据的覆盖必须在类型的静态构造函数中注册。若在该类型已有实例创建之后再覆盖元数据，行为是未定义的。
:::

## 取值强制转换 {#value-coercion}

强制转换回调会在取值被存储之前对其进行调整。要施加约束时（比如把数字夹到合法区间内）这很有用。

```csharp
public static readonly StyledProperty<double> ProgressProperty =
    AvaloniaProperty.Register<MyControl, double>(
        nameof(Progress),
        defaultValue: 0.0,
        coerce: CoerceProgress);

private static double CoerceProgress(AvaloniaObject sender, double value)
{
    // Clamp between 0 and 100
    return Math.Clamp(value, 0.0, 100.0);
}

public double Progress
{
    get => GetValue(ProgressProperty);
    set => SetValue(ProgressProperty, value);
}
```

强制转换回调会收到 `AvaloniaObject` 实例和待设置的值，并返回调整后的值。只要有效值发生变化，无论来源是本地值、样式还是动画，强制转换都会执行一次。

### 触发重新强制转换 {#triggering-re-coercion}

若你的强制转换逻辑依赖另一个属性，可以在那个属性变化时触发一次重新强制转换：

```csharp
protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change)
{
    base.OnPropertyChanged(change);

    if (change.Property == MaximumProperty)
    {
        // Re-coerce Progress when Maximum changes
        CoerceValue(ProgressProperty);
    }
}
```

## 取值校验 {#value-validation}

校验回调用于拒绝那些对该属性永远不合法的取值。与强制转换不同，校验并不调整取值，而是返回 `true` 表示接受、返回 `false` 表示拒绝。非法取值会抛出异常。

```csharp
public static readonly StyledProperty<int> ColumnSpanProperty =
    AvaloniaProperty.Register<MyControl, int>(
        nameof(ColumnSpan),
        defaultValue: 1,
        validate: v => v > 0);

public int ColumnSpan
{
    get => GetValue(ColumnSpanProperty);
    set => SetValue(ColumnSpanProperty, value);
}
```

把 `ColumnSpan` 设为 `0` 或负数都会抛出异常。

:::info
校验只在注册时设定一次，不能按类型覆盖。若需要按类型或按实例来调整取值，请改用强制转换。
:::

## 响应属性变化 {#responding-to-property-changes}

### Override `OnPropertyChanged`

在自定义控件中响应属性变化，最常见的写法是：

```csharp
protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change)
{
    base.OnPropertyChanged(change);

    if (change.Property == IsExpandedProperty)
    {
        var wasExpanded = change.GetOldValue<bool>();
        var isExpanded = change.GetNewValue<bool>();
        UpdateVisualState(isExpanded);
    }
}
```

### `GetObservable`

从外部代码订阅某个具体对象上的变化：

```csharp
myControl.GetObservable(MyControl.IsExpandedProperty)
    .Subscribe(isExpanded =>
    {
        Console.WriteLine($"IsExpanded is now {isExpanded}");
    });
```

### 类处理程序 {#class-handlers}

注册一个对该类型所有实例都生效的处理程序，通常写在静态构造函数里：

```csharp
static MyControl()
{
    IsExpandedProperty.Changed.AddClassHandler<MyControl>((control, args) =>
    {
        control.OnIsExpandedChanged(args);
    });
}

private void OnIsExpandedChanged(AvaloniaPropertyChangedEventArgs args)
{
    // Handle the change
}
```

## 直接属性的元数据 {#direct-property-metadata}

直接属性使用 `DirectPropertyMetadata<T>`：

| 参数 | 类型 | 说明 |
|---|---|---|
| `unsetValue` | `T` | 属性被清除时所采用的值。对直接属性而言，它就是实际意义上的默认值。 |
| `defaultBindingMode` | `BindingMode` | 默认绑定模式。 |
| `enableDataValidation` | `bool` | 该属性是否参与数据校验。 |

直接属性不支持通过元数据做强制转换或取值校验，请把这些检查写在 CLR 属性的 setter 里：

```csharp
private int _retryCount;

public int RetryCount
{
    get => _retryCount;
    set
    {
        if (value < 0)
            throw new ArgumentOutOfRangeException(nameof(value));
        SetAndRaise(RetryCountProperty, ref _retryCount, value);
    }
}
```

## 另请参阅 {#see-also}

- [属性系统总览](/docs/properties)：属性种类与注册方式总览。
- [取值优先级](/docs/properties/value-precedence)：属性系统如何在多个来源之间裁决取值。
- [属性值继承](/docs/properties/property-value-inheritance)：取值如何沿树向下传播。
