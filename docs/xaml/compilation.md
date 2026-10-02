---
id: compilation
title: XAML 编译
---

Avalonia 用 XamlX 编译器在构建时处理 `.axaml` 文件。与 WPF（默认在运行时解释 XAML）不同，Avalonia 在构建期就把 XAML 编译成 IL 代码，因此启动更快、二进制更小，还能在编译期发现错误。

## XAML 编译是怎么回事 {#how-xaml-compilation-works}

构建 Avalonia 项目时，XamlX 编译器会：

1. 解析每个 `.axaml` 文件。
2. 解析其中所有的类型引用、命名空间和属性名。
3. 校验属性赋值与类型转换。
4. 生成直接构建视觉树的 IL 代码，运行时不再需要解析 XML。

也就是说，在 WPF 里要到运行时才暴露的许多错误，在 Avalonia 中编译阶段就被拦下了。

## 编译绑定 {#compiled-bindings}

数据绑定默认用反射在运行时解析属性路径。编译绑定则在构建期就把路径解析好，好处是：

- **构建期校验**：属性名写错会直接变成编译错误。
- **性能更好**：运行时没有反射开销。
- **兼容 AOT**：Native AOT 发布必须用它。

### 按控件启用编译绑定 {#enabling-compiled-bindings-per-control}

用 `x:DataType` 声明数据类型，再用 `x:CompileBindings` 启用编译：

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:vm="using:MyApp.ViewModels"
             x:DataType="vm:MainViewModel"
             x:CompileBindings="True">
    <!-- This binding is validated at compile time -->
    <TextBlock Text="{Binding UserName}" />
</UserControl>
```

若 `MainViewModel` 上并没有 `UserName`，构建就会报错失败。

### 在整个项目范围内启用编译绑定 {#enabling-compiled-bindings-project-wide}

在 `.csproj` 文件中加上这个属性，编译绑定就成了默认行为：

```xml
<PropertyGroup>
    <AvaloniaUseCompiledBindingsByDefault>true</AvaloniaUseCompiledBindingsByDefault>
</PropertyGroup>
```

开了这个设置之后，所有绑定都必须有 `x:DataType` 声明。个别确实需要运行时解析的绑定，可以用 [`ReflectionBinding`](/api/avalonia/data/reflectionbinding) 退出编译绑定：

```xml
<TextBlock Text="{ReflectionBinding DynamicProperty}" />
```

### 在嵌套元素上使用 x:DataType {#xdatatype-on-nested-elements}

在模板或嵌套作用域内可以改变数据类型：

```xml
<ListBox ItemsSource="{Binding Orders}">
    <ListBox.ItemTemplate>
        <DataTemplate x:DataType="vm:OrderViewModel">
            <TextBlock Text="{Binding OrderNumber}" />
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

## 构建期报错示例 {#build-time-error-examples}

有了 XAML 编译绑定，下面这些常见笔误都会变成构建错误：

| 错误写法 | 报错信息 |
|---|---|
| `{Binding UserNam}` (typo) | Cannot resolve property 'UserNam' on type 'MainViewModel' |
| Missing `x:DataType` | Cannot use compiled binding without a DataType |
| 属性类型不匹配 | Cannot assign 'string' to property of type 'int' |

## Native AOT 相关注意事项 {#native-aot-considerations}

以 Native AOT 为目标时必须使用编译绑定，因为基于反射的绑定在缺少完整运行时的情况下可能失效。请确认：

1. `.csproj` 中的 `AvaloniaUseCompiledBindingsByDefault` 已设为 `true`。
2. 所有绑定都有对应的 `x:DataType` 声明。
3. 代码里不再残留 `ReflectionBinding` 的用法（或者已经加上了恰当的裁剪器注解加以保护）。

关于 AOT 发布的更多细节，请见 [Native AOT](/docs/deployment/native-aot)。

## 过时与实验性 API 的诊断 {#obsolete-and-experimental-diagnostics}

XAML 编译器能识别类型和成员上的 `[Obsolete]` 与 `[Experimental]` 特性。当你在 XAML 中使用被标记为过时或实验性的类型、属性或事件时，编译器会带上相应的诊断编号和说明发出警告（若是 `[Obsolete]` 且 `error: true`，则直接报错）。

举例来说，若某个控件库把一个类型标记为实验性：

```csharp
[Experimental("MYLIB0001")]
public class PreviewPanel : Control { }
```

在 XAML 中使用它就会产生一条构建警告：

```text
warning MYLIB0001: 'PreviewPanel' is for evaluation purposes only and is subject to change or removal in future updates.
  --> Views/MainView.axaml(8,6)
```

同样，在 XAML 中使用标记了 `[Obsolete("Use NewProperty instead")]` 的成员，构建时会发出 `AVLN2001` 警告，而不是悄无声息地编译过去。

如有需要，可以在项目文件中屏蔽这些诊断：

```xml
<PropertyGroup>
    <NoWarn>$(NoWarn);MYLIB0001</NoWarn>
</PropertyGroup>
```

## XAML 编译问题排查 {#troubleshooting-xaml-compilation}

### XAML 文件中的构建错误 {#build-errors-in-xaml-files}

XAML 编译错误会连同文件名和行号一起出现在 IDE 的错误列表和构建输出中：

```text
error AVLN2000: Unable to resolve property 'Naem' on type 'MyApp.ViewModels.PersonViewModel'
  --> Views/PersonView.axaml(12,34)
```

### 为动态场景屏蔽报错 {#suppressing-errors-for-dynamic-scenarios}

若某些场景确实需要运行时解析的绑定（例如绑定到 `dynamic` 或 `ExpandoObject`），请使用 `ReflectionBinding`：

```xml
<TextBlock Text="{ReflectionBinding SomeDynamicProperty}" />
```

### 设计时数据类型 {#design-time-data-types}

为了让 XAML 预览器和 IntelliSense 正常工作，请务必设置 `x:DataType`。在支持的 IDE 中，它还能为绑定路径提供自动补全。

```xml
<UserControl x:DataType="vm:MainViewModel">
    <!-- IDE provides IntelliSense for binding paths -->
    <TextBox Text="{Binding SearchText}" />
</UserControl>
```

## 另请参阅 {#see-also}

- [编译绑定](/docs/data-binding/compiled-bindings)：编译绑定的详细参考。
- [Avalonia XAML](/docs/fundamentals/avalonia-xaml)：XAML 基础。
- [x: 指令](/docs/xaml/directives)：x:CompileBindings、x:DataType 等指令的完整参考。
- [Native AOT](/docs/deployment/native-aot)：AOT 发布指南。
