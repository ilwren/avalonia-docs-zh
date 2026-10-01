---
id: binding-from-code
title: 如何在代码中绑定
doc-type: how-to
description: 用 C# 代码而非 XAML 来创建和管理数据绑定。
---

## 在代码中创建编译绑定 {#creating-compiled-bindings-from-code}

[`CompiledBinding.Create`](/api/avalonia/data/compiledbinding#create-method) 方法让你能用 LINQ 表达式写出类型安全的绑定。表达式会在编译期接受校验，属性名写错会直接变成编译错误，而不是运行时悄悄失败。

该方法有两个泛型参数：[`DataContext`](/docs/data-binding/data-context) 的类型，以及所选属性的类型。随后它接受一个用于选取目标属性的 lambda 表达式。

举例来说，若某控件的 [`DataContext`](/docs/data-binding/data-context) 是一个 `MyViewModel` 实例，而你想从中选取 `string Title { get; set; }` 属性，可以这样写：

```csharp
var binding = CompiledBinding.Create<MyViewModel, string>(x => x.Title);
```

然后把它绑定到控件上：

```csharp
textBlock.Bind(TextBlock.TextProperty, binding);
```

[`CompiledBinding.Create`](/api/avalonia/data/compiledbinding#create-method) 方法还有若干可选参数，用于调整绑定行为。 

下面的例子从一个显式指定的 `viewModel` 源（而非数据上下文）选取一个单向绑定：

```csharp
var binding = CompiledBinding.Create<MyViewModel, string>(
    expression: vm => vm.Title,
    source: viewModel,
    mode: BindingMode.OneWay);
```

表达式支持嵌套属性、索引器和类型转换：

```csharp
// Nested property
CompiledBinding.Create<MyViewModel, string>(vm => vm.Address.City);

// With a value converter
CompiledBinding.Create<MyViewModel, bool>(
    expression: vm => vm.IsActive,
    converter: new BoolToOpacityConverter(),
    mode: BindingMode.OneWay);
```

也可以写在对象初始化器里：

```csharp
var textBlock = new TextBlock
{
    [!TextBlock.TextProperty] = CompiledBinding.Create<MyViewModel, string>(
        expression: vm => vm.Name),
};
```

这种写法能带来与 XAML 编译绑定同等的性能和安全性，只不过写在 C# 代码中。XAML 的对应写法见[编译绑定](/docs/data-binding/compiled-bindings)。

## 订阅属性变化 {#subscribing-to-property-changes}

调用 [`GetObservable`](/api/avalonia/avaloniaobjectextensions#getobservable-method) 扩展方法即可订阅 [`AvaloniaObject`](/api/avalonia/avaloniaobject) 的属性变化。它返回一个 [`IObservable<T>`](https://learn.microsoft.com/en-us/dotnet/api/system.iobservable-1?view=net-10.0)，可用于监听该属性的变化：

```csharp
var textBlock = new TextBlock();
var text = textBlock.GetObservable(TextBlock.TextProperty);
```

每个可供订阅的属性都有一个名为 `[PropertyName]Property` 的静态只读字段，把它传给 `GetObservable` 就能订阅该属性的变化。

[`IObservable<T>`](https://learn.microsoft.com/en-us/dotnet/api/system.iobservable-1?view=net-10.0)（即 Reactive Extensions，简称 rx）不在本文讨论范围内，但这里给个例子：用返回的可观察序列把变化中的属性值打印到控制台。

```csharp
var textBlock = new TextBlock();
var text = textBlock.GetObservable(TextBlock.TextProperty);
text.Subscribe(value => Console.WriteLine(value + " Changed"));
```

订阅返回的可观察序列时，它会立即推送该属性的当前值，之后每次属性变化再推送新值。如果不想要当前值，可以用 rx 的 `Skip` 运算符：

```csharp
var text = textBlock.GetObservable(TextBlock.TextProperty).Skip(1);
```

另一种办法是订阅 [`AvaloniaObject.PropertyChanged`](/api/avalonia/avaloniaobject#propertychanged-event) 事件 —— 元素上_任何_属性发生变化时它都会触发。

```csharp
textBlock.PropertyChanged += (s, e) =>
{
    if (e.Property == TextBlock.TextProperty)
    {
        Console.WriteLine(e.NewValue + " Changed");
    }
};
```

## 绑定到可观察序列 {#binding-to-an-observable}

用 [`AvaloniaObject.Bind`](/api/avalonia/avaloniaobject#bind-method-1) 方法可以把属性绑定到一个可观察序列：

```csharp
// We use an Rx Subject here so we can push new values using OnNext
var source = new Subject<string>();
var textBlock = new TextBlock();

// Bind TextBlock.Text to source
var subscription = textBlock.Bind(TextBlock.TextProperty, source);

// Set textBlock.Text to "hello"
source.OnNext("hello");
// Set textBlock.Text to "world!"
source.OnNext("world!");

// Terminate the binding
subscription.Dispose();
```

注意 `Bind` 方法会返回一个 `IDisposable`，用它可以终止绑定。如果你一直不调用它，那么当可观察序列通过 `OnCompleted` 或 `OnError` 结束时，绑定会自动终止。

:::note
与 Avalonia 的标准绑定不同，可观察序列不使用弱引用，因此生命周期管理和防泄漏得由你自己负责。
:::

## 在对象初始化器中设置绑定 {#setting-a-binding-in-an-object-initializer}

在对象初始化器里搭好绑定往往很方便，用索引器即可：

```csharp
var source = new Subject<string>();
var textBlock = new TextBlock
{
    Foreground = Brushes.Red,
    MaxWidth = 200,
    [!TextBlock.TextProperty] = CompiledBinding.Create<MyViewModel, string>(x => x.Title),
};
```

索引器在对象初始化器之外同样可用：

```csharp
textBlock2[!TextBlock.TextProperty] = textBlock1[!TextBlock.TextProperty];
```

这种写法唯一的不足是拿不到 `IDisposable`。如果你需要手动终止绑定，就改用 `Bind` 方法。

## 在代码中使用反射绑定 {#using-reflection-bindings-from-code}

在代码中创建反射绑定的写法：

```csharp
var binding = new ReflectionBinding("Name");
```

若想要编译期即受校验的类型安全绑定，请优先选择[编译绑定](#creating-compiled-bindings-from-code)。

## 订阅任意对象上的属性 {#subscribing-to-a-property-on-any-object}

`GetObservable` 方法返回的可观察序列只跟踪单个实例上的属性变化。但如果你是在写控件，可能想实现一个不绑定到具体实例的 `OnPropertyChanged` 方法。

这时可以订阅 [`AvaloniaProperty.Changed`](/api/avalonia/avaloniaproperty) —— 它是一个可观察序列，_任何实例上该属性发生变化时_都会触发。

> 在 WPF 中，这是通过向 `DependencyProperty` 注册方法传入一个静态 `PropertyChangedCallback` 来实现的，但那种方式只允许控件作者注册属性变化回调。

此外还有一个 `AddClassHandler` 扩展方法，能自动把事件路由到你控件上的某个方法。

比如你想监听控件 `Foo` 属性的变化，可以这样写：

```csharp
static MyControl()
{
    FooProperty.Changed.AddClassHandler<MyControl>(FooChanged);
}

private static void FooChanged(MyControl sender, AvaloniaPropertyChangedEventArgs e)
{
    // The 'e' parameter describes what's changed.
}
```

## 查看生效中的绑定 {#inspecting-active-bindings}

用 `BindingOperations.GetBindingExpressionBase` 取出某个属性上正在生效的绑定表达式：

```csharp
var expression = BindingOperations.GetBindingExpressionBase(myTextBlock, TextBlock.TextProperty);
if (expression is not null)
{
    // A binding is active on TextBlock.TextProperty
}
```

这在做诊断时很有用，使用 `UpdateSourceTrigger.Explicit` 时也可以借它调用 `UpdateSource()`。

## 清除绑定 {#clearing-bindings}

如果你留住了 `Bind` 返回的 `IDisposable`，释放它即可终止绑定：

```csharp
var subscription = textBlock.Bind(TextBlock.TextProperty, source);

// Later, remove the binding
subscription.Dispose();
```

如果手上没有 `IDisposable`（比如绑定是通过对象初始化器或 XAML 设置的），就调用 `ClearValue` 移除绑定，属性会回退到[优先级顺序](/docs/properties/value-precedence)中的下一个取值：

```csharp
textBlock.ClearValue(TextBlock.TextProperty);
```

## 另请参阅 {#see-also}

- [数据绑定语法](/docs/data-binding/data-binding-syntax)：XAML 绑定语法参考。
- [编译绑定](/docs/data-binding/compiled-bindings)：编译期受校验的绑定。
- [调试数据绑定](/docs/data-binding/binding-debugging)：排查绑定问题。
- [值优先级](/docs/properties/value-precedence)：Avalonia 如何在多个来源之间决定属性的最终取值。
