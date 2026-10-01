---
id: markup-extensions
title: 标记扩展
description: 编写自定义 XAML 标记扩展，在运行时为属性提供取值。
doc-type: how-to
---

<p>{frontMatter.description}</p>

## 关于标记扩展 {#about-markup-extensions}

经典意义上的标记扩展，是指满足以下条件的类：

- 实现 `object? ProvideValue(IServiceProvider?)`
- 可以继承 [`MarkupExtension`](/api/avalonia/markup/xaml/markupextension)（在 Avalonia 中不作要求）
- 在 XAML 中通过 `{ns:Extension ...}` 语法使用

在 Avalonia 中，`ProvideValue` 允许返回**任意**类型。也就是说返回值可以是强类型的，因为它会被直接赋给目标属性。

Avalonia 提供了以下标记扩展：

| MarkupExtension                                                                                  | 赋给属性的内容                                                |
|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| [StaticResource](/docs/app-development/resource-dictionary#static-resource)                    | 一个已存在的带键资源，且不会随资源变化而更新          |
| [DynamicResource](/docs/app-development/resource-dictionary#using-resources)                   | 延迟加载的带键资源，会随资源变化而更新   |
| Binding                                                                                          | 取决于默认的绑定偏好：编译绑定或反射绑定    |
| [CompiledBinding](/docs/data-binding/compiled-bindings#reflectionbinding-and-compiledbinding-markup)       | 基于编译绑定                                        |
| [ReflectionBinding](/docs/data-binding/compiled-bindings#reflectionbinding-and-compiledbinding-markup)   | 基于反射绑定                                      |
| [TemplateBinding](/docs/custom-controls/templated-controls)    | 基于仅在 `ControlTemplate` 内部使用的简化绑定 |
| [OnPlatform](/docs/platform-specific-guides/xaml#onplatform-markup-extension)     | 在指定平台上有条件地生效                       |
| [OnFormFactor](/docs/platform-specific-guides/xaml#onformfactor-markup-extension) | 在指定的外形规格上有条件地生效                         |

## 编译器内建项 {#compiler-intrinsics}

严格来说它们属于 XAML 编译器而非 `MarkupExtension`，但 XAML 写法是一样的。

| 内建项 | 赋给属性的内容   |
|-----------|-----------------------|
| x:True    | `true` literal        |
| x:False   | `false` literal       |
| x:Null    | `null` literal        |
| x:Static  | 静态成员的值   |
| x:Type    | `System.Type` literal |

当目标绑定属性是 `object`、而你需要给它一个布尔值时，`x:True` 和 `x:False` 字面量就派上用场了。这类场景缺少类型信息，直接写 "True" 得到的仍然是 `string`。

```xml
<Button Command="{Binding SetStateCommand}" CommandParameter="{x:True}" />
```

## 编写标记扩展 {#creating-markup-extensions}

继承 `MarkupExtension`，或者提供下列任一签名 —— 它们通过鸭子类型得到支持：

```csharp
T ProvideValue();
T ProvideValue(IServiceProvider provider);
object ProvideValue();
object ProvideValue(IServiceProvider provider);
```

下面是一个用于本地化的标记扩展的基础示例：

```csharp
public class LocExtension
{
    public string Key { get; set; } = "";

    public string ProvideValue(IServiceProvider serviceProvider)
    {
        // Simplified localization lookup
        return LocalizationService.GetString(Key) ?? Key;
    }
}
```

```xml
<TextBlock Text="{local:Loc Key=WelcomeMessage}" />
```

若用强类型而非 `object`，那么 XAML 中构造函数参数、属性或 `ProvideValue` 返回值类型对不上时，你会直接拿到编译错误。而返回 `object` 时，实际返回的类型必须与目标属性类型相符，否则运行时会抛出 `InvalidCastException`。

### Using `IServiceProvider`

传给 `ProvideValue` 的 `IServiceProvider` 暴露了一系列 XAML 上下文服务，扩展借此可以知道自己被用在什么地方。

常用的标准服务包括：

- **`IProvideValueTarget`**：用于访问目标对象和目标属性。
- **`IRootObjectProvider`**：提供 XAML 文档的根对象。

Avalonia 还额外提供了若干 XAML-IL 专有服务：

- **`IAvaloniaXamlIlParentStackProvider`**：暴露 XAML 解析过程中的父对象栈。
- **`IAvaloniaXamlIlXmlNamespaceInfoProvider`**：提供命名空间的元数据。

这些服务并非必需，但对更高级、需要感知上下文的扩展来说不可或缺。

### 接收字面量参数 {#receiving-literal-parameters}

需要参数时，用构造函数按顺序逐个接收。

可选参数或顺序无关的参数则改用属性。也允许多个构造函数混用，包括无参构造函数。

```csharp
public class MultiplyLiteral
{
    private readonly double _first;
    private readonly double _second;
    
    public double? Third { get; set; }

    public MultiplyLiteral(double first, double second)
    {
        _first = first;
        _second = second;
    }

    public double ProvideValue(IServiceProvider provider)
    {
        return First * Second * Third ?? 1;
    }
}
```
```xml
<TextBlock Text="This has FontSize=40" FontSize="{namespace:MultiplyLiteral 10, 8, Third=0.5}" />
```

### 从绑定接收参数 {#receiving-parameters-from-bindings}

一个常见场景是把绑定送来的数据变换一下再写给目标属性。若所有参数都来自绑定，可以创建一个带 `IMultiValueConverter` 的 `MultiBinding` 来实现。

下面的示例中，`MultiplyBinding` 需要两个来自绑定的参数。如果字面量参数和绑定参数需要混用，那么创建一个 `IMultiValueConverter` 就能把字面量作为构造函数参数或 `init` 参数传入。`BindingBase` 虽然 `CompiledBinding` 和 `ReflectionBinding` 都能用，却不接受字面量。

```csharp
public class MultiplyBinding
{
    private readonly BindingBase _first;
    private readonly BindingBase _second;

    public MultiplyBinding(BindingBase first, BindingBase second)
    {
        _first = first;
        _second = second;
    }

    public object ProvideValue()
    {
        var mb = new MultiBinding()
        {
            Bindings = new[] { _first, _second },
            Converter = new FuncMultiValueConverter<double, double>(doubles => doubles.Aggregate(1d, (x, y) => x * y))
        };

        return mb;
    }
}
```

```xml
<TextBlock FontSize="{local:MultiplyBinding {Binding Multiplier}, {Binding Multiplicand}}" 
           Text="MarkupExtension with Bindings!" />
```

:::info
另一种做法是改为返回一个 `IObservable<T>.ToBinding()`。
:::

### 返回值 {#returning-parameters}

Avalonia 的标记扩展模型相当灵活：`ProvideValue` 想返回什么都行。

包括：

- 静态 .NET 对象
- 强类型的 .NET 对象 —— 赋给属性时可在编译期校验
- **Binding** 实例
- **可观察序列（`IObservable<T>`）** —— 用于动态的响应式取值

返回绑定或返回可观察序列的标记扩展都是受支持的，并且能与 Avalonia 的属性系统和数据绑定系统无缝衔接。

若希望一个标记扩展能适配多种目标属性类型，可以把 `ProvideValue` 的方法签名改为返回 `object`，这样每种类型都能单独处理。


```csharp
public object ProvideValue(IServiceProvider provider)
{
    var target = (IProvideValueTarget)provider.GetService(typeof(IProvideValueTarget))!;
    var targetProperty = target.TargetProperty as AvaloniaProperty;
    var targetType = targetProperty?.PropertyType;

    double result = First * Second * (Third ?? 1);

    if (targetType == typeof(double))
        return result;
    else if (targetType == typeof(float))
        return (float)result;
    else if (targetType == typeof(int))
        return (int)result;
    else
        throw new NotSupportedException();
}
```

构造函数同样可以用 `object` 的方式接收参数类型，但代价也一样 —— 原本的编译错误会变成运行时异常。

### MarkupExtension 的属性特性 {#markupextension-property-attributes}

* `[ConstructorArgument]` —— 表明关联属性可由构造函数参数初始化；若使用了该构造函数，则 
    XAML 序列化时应忽略该属性。
* `[MarkupExtensionOption]`、`[MarkupExtensionDefaultOption]` —— 与 `ShouldProvideOption` 配合使用，示例可参考 `OnPlatform` 和 `OnFormFactor` 的源码。

## 选项式标记扩展 {#options-markup-extensions}

`OptionsMarkupExtension` 是一类特殊的标记扩展，专门用来表达类似 switch 的分支。它的意义在于优化 —— 把永远走不到的分支去掉，便于编译器做裁剪。

### `OnPlatform` 标记扩展 {#onplatform-markup-extension}

内置的 `OnPlatform` 标记扩展就是选项式标记扩展的一个例子。它按运行时平台（Windows、macOS、Linux 等）分别定义取值，从而优化分支，只保留与当前编译目标平台相关的那一支。 

举例来说，借助 `OnPlatform`，你可以在 Linux 上使用 `Markdown` 控件，在其他平台上使用 `WebView` 控件。用不上的那个控件会被排除掉，二进制体积随之减小。

### 编写自定义的选项式标记扩展 {#creating-custom-options-markup-extensions}

下面是用 `RuntimeInformation.ProcessArchitecture` 做的一个自定义实现示例。正如例中所示，我们建议使用编译标志，或者那些取值实际恒定的 .NET 运行时 API。

```csharp
public class ArchitectureExtension : IAddChild<On<object>>
{
    [MarkupExtensionOption(nameof(X86))] public object? X86 { get; set; }
    [MarkupExtensionOption(nameof(X64))] public object? X64 { get; set; }
    [MarkupExtensionOption(nameof(Arm))] public object? Arm { get; set; }
    [MarkupExtensionOption(nameof(Arm64))] public object? Arm64 { get; set; }
    [MarkupExtensionOption(nameof(Wasm))] public object? Wasm { get; set; }

    [Content]
    [MarkupExtensionDefaultOption]
    public object? Default { get; set; }

    public static bool ShouldProvideOption(string option)
    {
        var currentArch = RuntimeInformation.ProcessArchitecture;
        return option switch
        {
            nameof(X86) => currentArch == Architecture.X86,
            nameof(X64) => currentArch == Architecture.X64,
            nameof(Arm) => currentArch == Architecture.Arm,
            nameof(Arm64) => currentArch == Architecture.Arm64,
            nameof(Wasm) => currentArch == Architecture.Wasm,
            _ => false,
        };
    }

    // Needed for the compiler.
    public void AddChild(On<object> child) {}
    public object? ProvideValue() => null;
}
```

这个类定义了若干选项，由 `ShouldProvideOption` 静态方法负责选择。随后就可以在 XAML 中这样设置这些选项：

```xml
<Border Background="{local:Architecture Default=White, X64=Green, Arm64=Red, Wasm=Blue}" />
```

在未经优化的 .NET 构建中，上面的例子等价于下面这段代码。

```csharp
border.Background = ArchitectureExtension.ShouldProvideOption("X64") ? Brushes.Green
     : ArchitectureExtension.ShouldProvideOption("Arm64") ? Brushes.Red
     : ArchitectureExtension.ShouldProvideOption("Wasm") ? Brushes.Blue
     : Brushes.White;
```

而针对特定平台架构优化并裁剪之后，它会被精简成这样。

```csharp
border.Background = Brushes.Red; // assuming app was compiled with dotnet publish -r win-arm64;
```

## 另请参阅 {#see-also}

- [数据绑定语法](/docs/data-binding/data-binding-syntax)：Binding 标记扩展参考。
- [编译绑定](/docs/data-binding/compiled-bindings)：CompiledBinding 与 ReflectionBinding 标记。
- [平台相关的 XAML](/docs/platform-specific-guides/xaml)：OnPlatform 与 OnFormFactor 标记扩展。
