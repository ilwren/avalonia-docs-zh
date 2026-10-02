---
id: binding-debugging
title: 调试数据绑定
description: 借助 trace 级日志与诊断输出，排查 Avalonia 中的数据绑定错误。
doc-type: how-to
---

## 绑定错误日志 {#binding-error-logging}

Avalonia 会把绑定错误写进 trace 输出。在 Debug 构建下，这些消息会出现在 IDE 的输出窗口或控制台中。下面是一条典型的绑定错误：

```text
[Binding] Error in binding to 'Avalonia.Controls.TextBlock'.'Text': 'Could not find a matching property accessor for 'UserNam' on 'MyApp.ViewModels.MainViewModel'
```

这条消息告诉你：
- 目标控件及其属性（`TextBlock.Text`）
- 出了什么问题（找不到属性 `UserNam`，多半是 `UserName` 拼错了）
- 查找时所依据的源类型（`MainViewModel`）

### 开启详细的绑定日志 {#enabling-verbose-binding-logging}

想看到全部绑定活动（而不只是错误），请在项目的 `Program.cs` 文件中调整日志级别。这样一来，每一次绑定解析、取值变化和回退值的应用都会被记录下来。

```csharp
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .LogToTrace(LogEventLevel.Warning)
        // highlight-next-line
        .LogToTrace(LogEventLevel.Verbose, LogArea.Binding);
```

## 常见的绑定问题 {#common-binding-problems}

### 找不到属性 {#property-not-found}

**现象：** 控件什么都不显示，或者显示的是回退值。日志里出现 “Could not find a matching property accessor.”

**Causes:**
- 绑定路径写错了。
- 数据上下文并不是你以为的那个类型。
- 该属性不是 public 的。

**解决：** 核对属性名。用 [DevTools](#using-avalonia-devtools) 检查 `DataContext`。

### `DataContext` 为 null {#datacontext-is-null}

**现象：** 控件上的所有绑定都取不到值。

**Causes:**
- 数据上下文压根没设置过。
- 数据上下文设到了错误的元素上。
- 某个父控件设了 `DataContext="{Binding SomeProperty}"`，而 `SomeProperty` 为 null。

**解决：** 用 [DevTools](#using-avalonia-devtools) 在控件层级上检查 `DataContext`。

### 绑定模式不匹配 {#binding-mode-mismatch}

**现象：** 界面上的改动传不到视图模型，或者反过来。

**Causes:**
- 该属性的默认绑定模式是 `OneWay`，但你需要的是 `TwoWay`。
- 源属性没有引发 `PropertyChanged`。

**解决：** 显式指定 `Mode=TwoWay`。确认视图模型实现了 `INotifyPropertyChanged`。

```xml
<TextBox Text="{Binding Name, Mode=TwoWay}" />
```

### 编译绑定类型不匹配 {#compiled-binding-type-mismatch}

**现象：** 构建报错 “Cannot resolve property” 或 “Binding path is not valid for type.”

**Causes:**
- `x:DataType` 与实际的 `DataContext` 类型对不上。
- 所声明的数据类型上并没有这个属性。

**解决：** 核对 `x:DataType` 是否与你的视图模型一致。实在需要绕过编译期检查时，可改用反射绑定。

```xml
<TextBlock Text="{ReflectionBinding DynamicProperty}" />
```

### 方法绑定的重载无法确定 {#method-binding-overload-not-resolved}

**现象：** 绑定到重载方法的命令失效。

- 使用编译绑定时，构建报错提示重载无法解析。
- 使用反射绑定时，运行时绑定错误提示重载无法解析。
- 命令执行时抛出运行时异常。

**Causes:**
- 有两个及以上的重载都接受一个参数，且没有一个接受 `object`，因此无从取舍。
- 所有重载都接受两个及以上参数，而方法绑定不支持这种情形。
- 使用编译绑定时，命令参数与方法参数类型不匹配。（编译绑定不会转换 `CommandParameter`。）

**解决：** 去掉相互竞争的重载；或者新增一个只接受单个 `object` 参数的重载（它的匹配优先级更高）。完整的重载解析规则见[直接绑定到方法](/docs/data-binding/binding-to-commands#binding-directly-to-a-method)。

### 转换器返回 `UnsetValue` {#converter-returns-unsetvalue}

**现象：** 绑定用的是回退值，而不是转换后的结果。

**原因：** 你的 `IValueConverter.Convert` 方法返回了 `AvaloniaProperty.UnsetValue` 或 `BindingOperations.DoNothing`。

**解决：** 返回一个真实的值，或者返回 `null`（它触发的是 `TargetNullValue`）。

## Using Avalonia DevTools

在运行中的应用里按 <kbd>F12</kbd> 打开 Avalonia DevTools，然后用 [Elements 工具](/tools/developer-tools/elements-tool) 查看控件属性，或者沿逻辑树找下去确认它的数据上下文。

## 在代码中调试绑定 {#debugging-bindings-in-code}

### 观察绑定取值 {#observing-binding-values}

用 `GetObservable` 实时观察某个属性的取值变化：

```csharp
myTextBlock.GetObservable(TextBlock.TextProperty).Subscribe(value =>
{
    Debug.WriteLine($"TextBlock.Text changed to: {value}");
});
```

### 检查绑定源 {#checking-the-binding-source}

```csharp
// Check what DataContext a control has
Debug.WriteLine($"DataContext type: {myControl.DataContext?.GetType().Name}");
Debug.WriteLine($"DataContext value: {myControl.DataContext}");
```

### 用 `FallbackValue` 做诊断 {#using-fallbackvalue-for-diagnostics}

临时加一个 `FallbackValue`，判断绑定路径是不是失效了：

```xml
<TextBlock Text="{Binding UserName, FallbackValue='BINDING FAILED'}" />
```

如果界面上出现了 “BINDING FAILED”，说明绑定路径写错了，或者数据上下文为 null。

## 编译绑定的诊断 {#compiled-bindings-diagnostics}

编译绑定在编译期就会被校验。路径不合法时你会直接拿到构建错误，而不是运行时悄无声息地失败。

编译绑定不合法时，有两条路可走：

1. 修正 `x:DataType` 声明，让它与实际的数据类型一致。
2. 对那些无法静态解析的动态属性，改用 `ReflectionBinding`。

## 排查清单 {#diagnostic-checklist}

绑定不生效时，按下面这几步查：

1. 翻看输出窗口里有没有绑定错误消息。
2. 打开 [DevTools](#using-avalonia-devtools) 确认控件的数据上下文。
3. 核对属性名是否完全一致（区分大小写）。
4. 确认该属性是 `public` 的，并且带 `get` 访问器。
5. 对于 `TwoWay` 绑定，确认属性带 `set` 访问器，且源实现了 `INotifyPropertyChanged`。
6. 确认 `DataContext` 在绑定求值之前就已经设好了。
7. 加一个 `FallbackValue`，确认问题是否出在路径解析上。
8. 对于编译绑定，确认 `x:DataType` 与实际运行时类型一致。

## 另请参阅 {#see-also}

- [数据绑定语法](/docs/data-binding/data-binding-syntax)：各项绑定参数，含 FallbackValue 与 TargetNullValue。
- [编译绑定](/docs/data-binding/compiled-bindings)：编译期的绑定校验。
- [数据上下文](/docs/data-binding/data-context)：DataContext 如何在控件树中向下流动。
