---
id: avalonia12-breaking-changes
title: Avalonia 12 的破坏性变更
description: Avalonia 11 到 12 之间全部破坏性变更的清单，每条都附有迁移指引和代码示例。
doc-type: reference
sidebar_label: 破坏性变更
toc_max_heading_level: 2
---

本文列出 Avalonia 11 与 12 之间的全部破坏性变更，并给出迁移指引和替代方案。


## .NET 支持情况的变化 {#net-support-updated}

Avalonia 12 不再支持 .NET Framework 和 .NET Standard，仅支持 .NET 8 及以上版本，推荐以 .NET 10 为目标。

如果你的项目面向 Android 或 iOS，那就只支持 .NET 10，这是为了与微软对底层 .NET SDK 的支持策略保持一致。

请把 Avalonia 项目升级到受支持的 .NET 版本。

**Example:**

```diff
-<TargetFramework>netstandard2.0</TargetFramework>
+<TargetFramework>net10.0</TargetFramework>
```

PR: [#19869](https://github.com/AvaloniaUI/Avalonia/pull/19869)


## Avalonia 12 版本 {#avalonia-version-12}

Avalonia 的主版本号由 11 升到了 12。

把所有 Avalonia 包引用升级到最新的 12.x 补丁版本——在你惯用的 IDE 里操作，或直接改项目文件都行。  
请从官方的 [GitHub Releases 页面](https://github.com/AvaloniaUI/Avalonia/releases)挑选最新发行版。

**Example:**

```diff
-<PackageReference Include="Avalonia" Version="11.3.12" />
+<PackageReference Include="Avalonia" Version="12.0.0" />
-<PackageReference Include="Avalonia.Themes.Fluent" Version="11.3.12" />
+<PackageReference Include="Avalonia.Themes.Fluent" Version="12.0.0" />
```


## `Avalonia.Diagnostics` 包已移除 {#avaloniadiagnostics-package-removed}

`Avalonia.Diagnostics` 包已被移除。
请改用 [Avalonia Plus](https://avaloniaui.net/pricing) 及以上版本附带的 Dev Tools。

把项目中的 `Avalonia.Diagnostics` 包移除，换成 `AvaloniaUI.DiagnosticsSupport`。  
Avalonia Plus Dev Tools 的安装方法请参阅 [Dev Tools 文档](/tools/developer-tools/installation)。

**Example:**

项目文件：

```diff
-<PackageReference Include="Avalonia.Diagnostics" Version="11.3.12" />
+<PackageReference Include="AvaloniaUI.DiagnosticsSupport" Version="2.2.0" />
```

应用程序文件：

```diff
-AttachDevTools();
+AttachDeveloperTools();
```

PR: [#20332](https://github.com/AvaloniaUI/Avalonia/pull/20332)


## 绑定类层次结构的变化 {#binding-class-hierarchy-changes}

绑定相关的类层次结构变了。XAML 文件中定义的绑定（比如 `{Binding}`）不受影响，但 C# 代码中用到绑定的地方必须改。

`IBinding` 接口已被移除，取而代之的是 [`BindingBase`](/api/avalonia/data/bindingbase) 类。

现在所有类型的绑定都继承自 `BindingBase`：[`ReflectionBinding`](/api/avalonia/data/reflectionbinding)、[`CompiledBinding`](/api/avalonia/data/compiledbinding)、`TemplateBinding` 和 `IndexerBinding`。请相应调整你的代码，别再想当然地认为拿到的 `BindingBase` 实例一定是「标准」绑定。

`Binding` 类为兼容而保留，它始终对应 `ReflectionBinding`。要在代码中创建绑定，请直接使用 `CompiledBinding` 和 `ReflectionBinding` 类。

`InstancedBinding` 类同样已被移除。与之直接对应的是 `BindingExpressionBase`，它表示施加在某个对象和属性上的绑定。

**Example:**
```diff
 public record Item(string Value);

-var reflectionBinding = new Binding("SomeProperty");
 var reflectionBinding = new ReflectionBinding(nameof(Item.Value));

+var compiledBinding = CompiledBinding.Create((Item item) => item.Value);
```

PR: [#19589](https://github.com/AvaloniaUI/Avalonia/pull/19589), [#20439](https://github.com/AvaloniaUI/Avalonia/pull/20439)


## 编译型绑定默认启用 {#compiled-bindings-are-enabled-by-default}

`<AvaloniaUseCompiledBindingsByDefault>` 现在默认为 `true`。  
XAML 代码中凡是用到 `Binding` 的地方，现在都映射到 `CompiledBinding`。

Avalonia 官方模板这几年创建的项目里都显式开了这个开关，所以较新的代码库基本不受影响。但如果你的项目没定义这个开关，那它在旧版本中是 `false`。

我们建议尽可能使用编译型绑定：它比反射绑定性能更好，而且在构建期就会做正确性检查。

PR: [#19712](https://github.com/AvaloniaUI/Avalonia/pull/19712)


## 绑定插件已移除 {#binding-plugins-removed}

绑定插件原本是为绑定添加功能而设计的扩展点。实际上它们对编译型绑定根本不起作用，多数人也压根没用过。 

更糟的是，默认的数据注解校验插件与 `CommunityToolkit.Mvvm` 等流行框架相冲突，用户往往不得不把它关掉。

从 Avalonia v12 起，插件不再可配置，数据注解插件也默认关闭。

PR: [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623)


## 文本整形器可配置 {#configurable-text-shaper}

文本整形器现在可以独立于渲染引擎单独配置。对多数应用而言这一改动是无感的，因为在 `AppBuilder` 上调用 `UsePlatformDetect` 时默认就会用 HarfBuzz。

不过，如果你的项目显式配置了渲染引擎（比如通过 `UseSkia` 指定 Skia），启动时可能会抛出 `InvalidOperationException`，消息为 *No text shaping system configured*。这时需要在 `AppBuilder` 上补一句 `UseHarfBuzz` 调用。

**Example:**

项目文件：

```diff
+<PackageReference Include="Avalonia.HarfBuzz" Version="12.0.0" />
```

应用程序文件：

```diff
 AppBuilder.Configure<App>()
     .UseSkia()
+    .UseHarfBuzz()
```

PR: [#19852](https://github.com/AvaloniaUI/Avalonia/pull/19852)


## 改进了触摸/触控笔下的焦点与选择行为 {#improved-touchpen-focus-and-selection-behavior}

[`SelectingItemsControl`](/api/avalonia/controls/primitives/selectingitemscontrol)（以及 `ListBox`、`ComboBox`、`TabControl` 等派生控件）和 [`TreeView`](/api/avalonia/controls/treeview) 的选择处理已经统一，使各类输入设备下的行为既一致又符合各平台习惯：

- **触摸和触控笔输入**现在在指针抬起（而非按下）时才触发选择，这与各平台的原生惯例一致。于是在可选项上开始滑动或滚动手势时，就不会误改选择了。
- **容器类型**（如 `ListBoxItem`、`TreeViewItem`）现在直接处理选择相关的输入，不再让事件冒泡到父级 `ItemsControl`。原先依赖在 `ItemsControl` 层拦截选择事件的自定义逻辑，必须挪到容器里，或改为重写 `UpdateSelectionFromEvent`。
- 对触摸和触控笔设备而言，**焦点**只在抬起时才改变。

### Obsoleted APIs

`SelectingItemsControl` 上的下列方法已标记为过时，将在未来版本中移除：

| 过时的方法 | 替代方案 |
|---|---|
| `UpdateSelection` | `UpdateSelectionFromEvent` |
| `UpdateSelectionFromEventSource` | `UpdateSelectionFromEvent` |

### 定制选择行为 {#customizing-selection-behavior}

重写 `SelectingItemsControl` 或 `TreeView` 上的 `ShouldTriggerSelection`，即可控制哪些指针或按键事件会触发选择；重写 `UpdateSelectionFromEvent` 则可定制选择如何落实。

静态类 `ItemSelectionEventTriggers` 提供了一组检查修饰键的辅助方法：

| 方法 | 说明 |
|---|---|
| `ShouldTriggerSelection(InputElement, PointerEventArgs)` | 判断某个指针事件是否应当触发选择。 |
| `ShouldTriggerSelection(InputElement, KeyEventArgs)` | 判断某个按键事件是否应当触发选择。 |
| `HasRangeSelectionModifier(InputElement, RoutedEventArgs)` | 检查 Shift 修饰键（范围选择）。 |
| `HasToggleSelectionModifier(InputElement, RoutedEventArgs)` | 检查 Ctrl 修饰键（切换选择）。 |

PR: [#19203](https://github.com/AvaloniaUI/Avalonia/pull/19203), [#19753](https://github.com/AvaloniaUI/Avalonia/pull/19753)


## [`TopLevel`](/api/avalonia/controls/toplevel) changes

为了给高级窗口特性（尤其是模板化自绘窗口装饰和虚拟窗口场景）打好基础，Avalonia v12 做了若干改动：

- 别被名字骗了：`TopLevel`（含 `Window`）对象现在不一定位于视觉层次结构的根部。那些把顶层 `Visual` 强制转换成 `TopLevel` 的代码不再可行。
要拿到 `TopLevel` 实例，请一律调用 `TopLevel.GetTopLevel(Visual)`。
- 以往只由 `TopLevel` 类实现的那些接口，比如 `IInputRoot`、`IRenderRoot`、`ILayoutRoot`、`ITextInputMethodRoot` 和 `IEmbeddableLayoutRoot`，要么已被移除，要么不再可访问，请改用 `TopLevel`。
- 新增了 `IPresentationSource` 接口，它表示视觉树的任意宿主（但它自身不是视觉元素）。调用新的 `GetPresentationSource(Visual)` 扩展方法即可取得这样的实例。

PR: [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624)


## 窗口装饰的变化 {#window-decoration-changes}

Avalonia v12 大改了不使用系统窗口外框时窗口装饰（标题栏、标题按钮、尺寸调整手柄等元素）的绘制方式：

- 新增 [`WindowDrawnDecorations`](/api/avalonia/controls/chrome/windowdrawndecorations) 类，职责是用单个控件提供全部窗口装饰。
- 有了这个新类型，`TitleBar`、`CaptionButtons` 和 `ChromeOverlayLayer` 就都没必要了，已被移除。
- `Window.ExtendClientAreaChromeHints` 属性由若干标志位组成，行为并不总是符合预期。该属性已被移除，请改用 [`WindowDecorations`](/api/avalonia/controls/windowdecorations) 属性配合 `ExtendClientAreaToDecorationsHint`。

PR: [#20770](https://github.com/AvaloniaUI/Avalonia/pull/20770), [#20732](https://github.com/AvaloniaUI/Avalonia/pull/20732), [#20796](https://github.com/AvaloniaUI/Avalonia/pull/20796)


## 剪贴板的变化 {#clipboard-changes}

在更早的版本中，剪贴板支持被重写为基于新的 [`IAsyncDataTransfer`](/api/avalonia/input/iasyncdatatransfer) 接口及相关类型。为了不破坏兼容性，旧的 `IDataObject` 接口当时被保留下来（并标记为过时），充当新系统的垫片。

Avalonia v12 移除了 `IDataObject` 接口，以及所有接受该类型的方法。它的实现 `DataObject` 现在什么也不做了。

`IClipboard` 接口已精简，读取特定格式的方法改以扩展方法形式提供（例如 `TryGetTextAsync` 和 `TryGetFile`）。

`IAsyncDataTransfer` 的用法详见官方[剪贴板文档](/docs/services/clipboard)。

**Example:**
```diff
// Setting a data object on the clipboard
-var data = new DataObject();
-data.Set(DataFormats.Text, "some text");
+var item = new DataTransferItem();
+item.Set(DataFormat.Text, "some text");
+var data = new DataTransfer();
+data.Add(item);

-await clipboard.SetDataObjectAsync(data);
+await clipboard.SetDataAsync(data);
```

**Example:**
```diff
// Reading text from the clipboard
-var text = await clipboard.GetTextAsync();
+var text = await clipboard.TryGetTextAsync();
```

PR: [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521)


## 支持多个 dispatcher {#multiple-dispatchers-support}

严格说这不算破坏性变更：Avalonia v12 现在支持多个 dispatcher，每个线程一个。

对应用程序来说，继续用 `Dispatcher.UIThread` 完全没问题。但库和控件的作者应当开始改用 `AvaloniaObject.Dispatcher` 和 `Dispatcher.CurrentDispatcher` 属性，以便妥善支持多 dispatcher。

`DispatcherTimer` 和 `AvaloniaSynchronizationContext` 现在默认使用当前 dispatcher，而不像旧版那样一律用 UI 线程。请确保这些类型是在正确的线程上实例化的，或者在构造时把目标 dispatcher 传进去。

多个 UI 线程目前仍不支持。

PR: [#18686](https://github.com/AvaloniaUI/Avalonia/pull/18686)


## `Dispatcher.InvokeAsync` 会捕获执行上下文 {#dispatcherinvokeasync-captures-the-execution-context}

这项改动让大多数异步调用的行为更符合预期：`AsyncLocal` 会如期工作，模拟身份和区域文化也会从调用方流过来。  

PR: [#19163](https://github.com/AvaloniaUI/Avalonia/pull/19163)


## `FuncMultiValueConverter` 改为接受 `IReadOnlyList` {#funcmultivalueconverter-accepts-an-ireadonlylist}

转换函数的参数类型从 `IEnumerable<TIn>` 变成了 `IReadOnlyList<TIn>`，于是你可以按索引取值（比如 `values[0]`），不必再转成一个中间集合。由于 `IReadOnlyList<T>` 继承自 `IEnumerable<T>`，大多数只做遍历或用 LINQ 的既有代码不受影响；只有把 lambda 参数类型显式写成 `IEnumerable<TIn>` 的代码需要改。

PR: [#19936](https://github.com/AvaloniaUI/Avalonia/pull/19936)


## `Window.WindowState` 变为直接属性 {#windowwindowstate-is-a-direct-property}

`Window.WindowState` 以前是样式化属性，但它在窗口状态管理中引发了不少麻烦，所以改成了直接属性。

因此，从样式中设置 `WindowState` 不再有效。


## 自定义控件默认启用数据校验 {#data-validation-enabled-by-default-in-custom-controls}

在 v12 之前，带 `enableDataValidation: true` 的 Avalonia 属性必须重写 `UpdateDataValidation` 方法，该属性的数据校验错误才会被报告出来。现在这一切都是自动的了。

那些只是调用 `DataValidationErrors.SetError` 的 `UpdateDataValidation` 重写，应当删掉。

**Example:**
```diff
 public class CustomControl
 {

     public static readonly StyledProperty<string?> CustomProperty = 
         AvaloniaProperty.Register<CustomControl, string?>("Custom", enableDataValidation: true)); 

-    protected override void UpdateDataValidation(AvaloniaProperty property, BindingValueType state, Exception? error)
-    {
-        if (property == CustomProperty)
-        {
-            DataValidationErrors.SetError(this, error);
-        }
-    } 
 }
```

若某个属性需要恢复旧行为，重写 `UpdateDataValidation` 并在处理该属性时不调用基类方法即可。

PR: [#20067](https://github.com/AvaloniaUI/Avalonia/pull/20067)


## 渲染目标与平台表面接口的重构 {#render-target-and-platform-surface-interfaces-reworked}

若干内部渲染接口的结构有所调整：

- `IRenderTarget.CreateDrawingContext` 现在接受一个 `RenderTargetSceneInfo` 参数，不再提供多个重载。
- `IRenderTargetBitmapImpl` 不再继承 `IRenderTarget`，改为继承 `IReadableBitmapImpl`，并带一个更简单的 `CreateDrawingContext()` 方法。
- `IDrawingContextLayerImpl` 不再继承 `IRenderTargetBitmapImpl`，改为直接继承 `IBitmapImpl`。
- 平台表面改用带类型的 `IPlatformRenderSurface` 接口，不再用 `IEnumerable<object>`。
- `ISkiaGpu` 现在是 internal。

若干带版本号的、拆分开的接口已并入其基类型：

- `IRenderTarget2` 和 `IRenderTargetWithProperties` 并入 `IRenderTarget`。
- `IGlPlatformSurfaceRenderTarget2` 和 `IGlPlatformSurfaceRenderTargetWithCorruptionInfo` 并入 `IGlPlatformSurfaceRenderTarget`。
- `ISkiaGpuRenderTarget2` 并入 `ISkiaGpuRenderTarget`。
- `ISkiaGpuWithPlatformGraphicsContext` 并入 `ISkiaGpu`。

此外，alpha 格式的处理也作了归并：

- `ILockedFramebuffer` 现在带有 [`AlphaFormat`](/api/avalonia/platform/alphaformat) 属性。
- `IReadableBitmapImpl` 现在带有 `AlphaFormat?` 属性，取代了原先单独的 `IReadableBitmapWithAlphaImpl` 接口。
- `Bitmap.CopyPixels()` 不再接受 `AlphaFormat` 参数，alpha 格式现在直接从 `ILockedFramebuffer` 读取。
- `LockedFramebuffer` 构造函数要求传入 `AlphaFormat` 参数。

`IPlatformRenderInterfaceContext.CreateOffscreenRenderTarget` 方法的签名由 `(PixelSize, double)` 改为 `(PixelSize, Vector, bool)`：原先的 `double` 缩放系数换成了可分轴缩放的 `Vector`，并新增 `bool` 用于控制文本抗锯齿。该接口还新增了 `MaxOffscreenRenderTargetPixelSize` 属性。

这些改动只影响实现自定义渲染后端、或直接使用平台级渲染接口的代码。使用 `RenderTargetBitmap` 或标准绘图 API 的应用代码不受影响。

PRs: [#20811](https://github.com/AvaloniaUI/Avalonia/pull/20811), [#20556](https://github.com/AvaloniaUI/Avalonia/pull/20556), [#20557](https://github.com/AvaloniaUI/Avalonia/pull/20557), [#20497](https://github.com/AvaloniaUI/Avalonia/pull/20497)

## 文本格式化相关的构造函数有变 {#text-formatting-constructors-modified}

`GenericTextRunProperties`、`TextCollapsingProperties` 和 `TextShaperOptions` 原先都有两个构造函数：一个带 `FontFeatureCollection` 参数，一个不带。

它们已合并为单个构造函数，该参数变为可选。
视你原本用的是哪个重载，可能需要调整实参顺序，因为 `FontFeatureCollection` 现在排在最后。

PR: [#20527](https://github.com/AvaloniaUI/Avalonia/pull/20527)


## 访问键按键面符号触发 {#access-keys-are-triggered-by-symbol}

以前访问键由底层的虚拟键触发，因此带变音符号的字符和数字没法用作访问键。

为了与其他主流 UI 框架以及用户预期保持一致，访问键现在改由键面上印的符号触发。于是带变音符号的字符（如 `_é`）和数字（如 `_2`）都能当访问键用了。

为支持多字节 Unicode 字符，`AccessText.AccessKey` 属性的类型由 `char` 改为 `string?`。读取该属性的代码需要相应调整。

PR: [#20662](https://github.com/AvaloniaUI/Avalonia/pull/20662)


## 字体支持的变化 {#font-support-updated}

为保证各平台上字体加载表现一致，Avalonia v12 内置了自己的字体解析器。

一些既非 TrueType（.ttf）也非 OpenType（.otf）的老旧字体不再受支持，比如年代久远的 Type 1 字体格式（.pfb/.pfm）。

PR: [#19852](https://github.com/AvaloniaUI/Avalonia/pull/19852)


## [`Screen`](/api/avalonia/platform/screen) 变为抽象类 {#screen-is-abstract}

`Screen` 类有好几个内部实现，基类之所以能被构造，纯属历史遗留。

在 Avalonia v12 中它已变为抽象类。请不要构造 `Screen` 类，而应从它的成员中获取现成实例（例如 `Screens.All`、`Screens.Primary`、`Screens.ScreenFromWindow`）。

PR: [#20529](https://github.com/AvaloniaUI/Avalonia/pull/20529)


## [`ResourcesChangedEventArgs`](/api/avalonia/controls/resourceschangedeventargs) 变为结构体 {#resourceschangedeventargs-is-a-struct}

出于性能考虑，`ResourcesChangedEventArgs` 现在是结构体。

多数项目从不构造这个类型的实例，因为它主要是通过 `StyledElement.ResourcesChanged` 事件用到的。
如果你确实构造过 `ResourcesChangedEventArgs`，请改为调用 `ResourceChangedEventArgs.Create`。

PR: [#20576](https://github.com/AvaloniaUI/Avalonia/pull/20576)


## 手势事件挪了位置 {#gesture-events-moved}

原先声明在 `Gestures` 类中的全部附加事件（如 `ScrollGesture`、`Pinch` 等）都已挪到 `InputElement`，于是所有元素默认都能用它们。请把 XAML 文件里的 `Gestures.` 前缀去掉。

`Gestures` 类不再是 public。

示例：

```diff
-<Button Gestures.Pinch="Button_Pinch" />
+<Button Pinch="Button_Pinch" />
```

PR: [#20789](https://github.com/AvaloniaUI/Avalonia/pull/20789)


## 焦点相关的改进 {#focus-improvements}

`InputElement.GotFocus` 和 `InputElement.LostFocus` 事件的参数类型已改为新的 `FocusChangedEventArgs` 类，它能提供更多关于「先前获得焦点」和「当前获得焦点」元素的信息。

请相应更新你的事件处理程序。

示例：
```diff
-private void TextBox_GotFocus(object? sender, GotFocusEventArgs e)
+private void TextBox_GotFocus(object? sender, FocusChangedEventArgs e)

-private void TextBox_LostFocus(object? sender, RoutedEventArgs e)
+private void TextBox_LostFocus(object? sender, FocusChangedEventArgs e)
```

现在所有焦点处理都由 `FocusManager` 类和 `IFocusManager` 接口统管。用到 `KeyboardNavigationHandler.GetNext` 的地方要换成 `FocusManager.GetNextElement`。

PR: [#20859](https://github.com/AvaloniaUI/Avalonia/pull/20859), [#18647](https://github.com/AvaloniaUI/Avalonia/pull/18647), [#20930](https://github.com/AvaloniaUI/Avalonia/pull/20930)


## 不可见控件上的动画会停下来 {#animations-are-stopped-on-invisible-controls}

出于效率考虑，由样式触发的动画在对应控件被隐藏时不再推进帧，这在不少场景下都能降低 CPU 占用。

如有需要，把新增的 `Animation.PlaybackBehavior` 设为 `Always` 即可恢复旧行为。

PR: [#20820](https://github.com/AvaloniaUI/Avalonia/pull/20820)


## Windows

### 移除 Direct2D1 支持 {#direct2d1-support-removed}

Avalonia 不再提供 Direct2D 渲染后端。这个包无人维护，功能和性能也都赶不上 Skia 后端。现在一律推荐使用 Skia 后端。

**Example:**

项目文件：

```diff
-<PackageReference Include="Avalonia.Direct2D1" Version="11.3.12" />
+<PackageReference Include="Avalonia.Skia" Version="12.0.0" />
```

应用程序文件：

```diff
 AppBuilder.Configure<App>()
-    .UseDirect2D1()
+    .UseSkia()
```

PR: [#20132](https://github.com/AvaloniaUI/Avalonia/pull/20132)

### `BinaryFormatter` removed

在旧版本中，Avalonia 在 Windows 上借助 .NET 的 `BinaryFormatter` 对放进剪贴板的任意对象做隐式序列化和反序列化。

微软从好几个 .NET 版本之前就开始建议[不要再用二进制格式化器](https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-migration-guide/)。Avalonia 遵循这一建议，已不再使用它。

你的项目应当用自己选定的机制显式地序列化和反序列化对象（JSON 是个流行的选择）。

PR: [#20455](https://github.com/AvaloniaUI/Avalonia/pull/20455)

### `Window.ExtendClientAreaToDecorationsHint` improved

在 Windows 上，`ExtendClientAreaToDecorationsHint` 属性的若干问题已修复，现在它在所有受支持的场景下都能正常工作。以往流传的各种变通手段（比如在受影响的窗口上增删外边距，尤其是窗口最大化时），现在都应当删掉。

PR: [#20217](https://github.com/AvaloniaUI/Avalonia/pull/20217)


## Android

### 应用初始化方式有变 {#app-initialization-changed}

在 Avalonia 12 中，Android 应用及其 activity 的初始化方式变了，这样后续的 activity 才能正确使用你项目中定义的 `Application` 类。

1. 把你的主 activity 改为继承 [`AvaloniaMainActivity`](/api/avalonia/android/avaloniamainactivity)（非泛型），而不是 `AvaloniaMainActivity<TApp>`（泛型）。
2. 新增一个派生自 `AvaloniaAndroidApplication<TApp>` 的类，并给它加上 `[Android.App.Application]` 特性。

**Example:**

```diff
[Activity]
public class MainActivity :
-AvaloniaMainActivity<App>
+AvaloniaMainActivity
{
}

+[Application]
+public class AndroidApp : AvaloniaAndroidApplication<App>
+{
+    protected AndroidApp(IntPtr javaReference, JniHandleOwnership transfer)
+        : base(javaReference, transfer)
+    {
+    }
+}
```

PR: [#18756](https://github.com/AvaloniaUI/Avalonia/pull/18756)

### [`IActivityApplicationLifetime`](/api/avalonia/controls/applicationlifetimes/iactivityapplicationlifetime) replaces [`ISingleViewApplicationLifetime`](/api/avalonia/controls/applicationlifetimes/isingleviewapplicationlifetime)

Android 现在用 `IActivityApplicationLifetime` 取代 `ISingleViewApplicationLifetime`。新接口提供的是 `MainViewFactory` 属性（一个 `Func<Control>`），而不是单个 `MainView` 实例，因为 Android 可能在应用生命周期内创建多个 activity 实例。

请更新你的 `App.axaml.cs`，先判断 `IActivityApplicationLifetime` 再判断 `ISingleViewApplicationLifetime`：

```diff
 public override void OnFrameworkInitializationCompleted()
 {
     if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
         desktop.MainWindow = new MainWindow();
+    else if (ApplicationLifetime is IActivityApplicationLifetime activityLifetime)
+        activityLifetime.MainViewFactory = () => new MainView();
     else if (ApplicationLifetime is ISingleViewApplicationLifetime singleView)
         singleView.MainView = new MainView();
     base.OnFrameworkInitializationCompleted();
 }
```

iOS、浏览器和嵌入式 Linux 平台仍然需要 `ISingleViewApplicationLifetime` 这项判断。

PR: [#18893](https://github.com/AvaloniaUI/Avalonia/pull/18893)

### 从 `AvaloniaMainActivity` 中移除了 `CreateAppBuilder` 和 `CustomizeAppBuilder` {#removed-createappbuilder-and-customizeappbuilder-from-avaloniamainactivity}

`AvaloniaMainActivity` 上的 `CreateAppBuilder()` 和 `CustomizeAppBuilder(AppBuilder)` 虚方法已被移除。它们此前就标记为过时，框架也不再调用。如上一节所述，应用初始化现在完全交由 `AvaloniaAndroidApplication<TApp>` 负责。

如果你重写过这两个方法，请把相关逻辑挪到你的 `AvaloniaAndroidApplication<TApp>` 子类或 `App` 类中。

PR: [#20715](https://github.com/AvaloniaUI/Avalonia/pull/20715)


## iOS

### 应用初始化方式有变 {#app-initialization-changed-1}

在 Avalonia 12 中，iOS 应用的初始化方式改为采用[「场景」（scene）概念](https://developer.apple.com/documentation/technotes/tn3187-migrating-to-the-uikit-scene-based-life-cycle)——苹果不久之后就会强制要求这么做。

多数应用无需改动代码即可照常工作，但应用初始化完成后 `AvaloniaAppDelegate.Window` 将始终为 `null`，因为窗口现在由场景委托在内部管理。

若你需要访问 `UIWindow`，可重写 `AvaloniaView.MovedToWindow` 方法，在视图被附加上去时捕捉这一时机。

PR: [#20454](https://github.com/AvaloniaUI/Avalonia/pull/20454)


## Browser

### `Avalonia.Browser.Blazor` 包已移除 {#avaloniabrowserblazor-package-removed}

`Avalonia.Browser.Blazor` 包只是从 Avalonia 旧的 Blazor 浏览器后端升级过程中的一个临时过渡。如今 Avalonia 已完全转向基于 WASM（`Avalonia.Browser`）的新后端，该包不再维护，已被移除。

你仍然可以在 Blazor 之上运行 Avalonia——使用受支持的 `Avalonia.Browser` 包及其 `AvaloniaView` 类即可。

PR: [#20105](https://github.com/AvaloniaUI/Avalonia/pull/20105)


## Tizen

### `Avalonia.Tizen` 包已移除 {#avaloniatizen-package-removed}

Tizen 平台因缺少维护者，已不再开箱支持。
详情请阅读 [Moving Tizen Support Out of Main Repository](https://github.com/AvaloniaUI/Avalonia/discussions/19721)。

PR: [#19722](https://github.com/AvaloniaUI/Avalonia/pull/19722)


## Headless

### xUnit.net 与 NUnit 的受支持版本更新 {#xunitnet-and-nunit-supported-versions-updated}

Avalonia 无头平台所支持的底层测试框架已升级到最新版本，你的单元测试可能需要相应调整。
- xUnit.net 的支持版本升到了 3（原为 2）。单元测试的迁移办法请阅读 xUnit.net 的[官方迁移指南](https://xunit.net/docs/getting-started/v3/migration)。
- NUnit 的支持版本升到了 4（原为 3）。单元测试的迁移办法请阅读 NUnit 的[官方迁移指南](https://docs.nunit.org/articles/nunit/release-notes/Nunit4.0-MigrationGuide.html)。

PR: [#20372](https://github.com/AvaloniaUI/Avalonia/pull/20372), [#20481](https://github.com/AvaloniaUI/Avalonia/pull/20481)


## 已移除的成员 {#removed-members}

下列成员在 Avalonia 12 中已被移除，按导致其移除的功能领域分组列出。

### 绑定类层次结构 {#binding-class-hierarchy}

背景请参阅[绑定类层次结构的变化](#binding-class-hierarchy-changes)。

| 已移除的成员 | 替代方案 | PR |
|---|---|---|
| `IBinding` interface | `BindingBase` | [#19589](https://github.com/AvaloniaUI/Avalonia/pull/19589) |
| `InstancedBinding` class | `BindingExpressionBase` | [#19589](https://github.com/AvaloniaUI/Avalonia/pull/19589) |

### 绑定插件 {#binding-plugins}

背景请参阅[绑定插件已移除](#binding-plugins-removed)。请删除所有用到这些类型的代码。

| 已移除的成员 | PR |
|---|---|
| `Avalonia.Data.Core.Plugins.BindingPlugins` | [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623) |
| `Avalonia.Data.Core.Plugins.DataValidationBase` | [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623) |
| `Avalonia.Data.Core.Plugins.ExceptionValidationPlugin` | [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623) |
| `Avalonia.Data.Core.Plugins.IDataValidationPlugin` | [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623) |
| `Avalonia.Data.Core.Plugins.IndeiValidationPlugin` | [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623) |
| `Avalonia.Data.Core.Plugins.IPropertyAccessorPlugin` | [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623) |
| `Avalonia.Data.Core.Plugins.IStreamPlugin` | [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623) |
| `Avalonia.Data.Core.Plugins.PropertyAccessorBase` | [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623) |
| `Avalonia.Data.Core.Plugins.PropertyError` | [#20623](https://github.com/AvaloniaUI/Avalonia/pull/20623) |

### 剪贴板与拖放 {#clipboard-and-drag-drop}

背景请参阅[剪贴板的变化](#clipboard-changes)。

| 已移除的成员 | 替代方案 | PR |
|---|---|---|
| `DataFormats.*` members | `DataFormat.*` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `DataObject.*` members | `DataTransfer` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `DataObjectExtensions` class | `AsyncDataTransferExtensions` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `DragDrop.DoDragDrop` method | `DragDrop.DoDragDropAsync` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `DragEventArgs.Data` property | `DragEventArgs.DataTransfer` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `IDataObject` interface | `IAsyncDataTransfer` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `IClipboard.GetDataAsync` | `IClipboard.TryGetDataAsync` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `IClipboard.GetFormatsAsync` | `ClipboardExtensions.GetDataFormatsAsync` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `IClipboard.GetTextAsync` | `ClipboardExtensions.TryGetTextAsync` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `IClipboard.SetTextAsync` | `ClipboardExtensions.SetTextAsync` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |
| `IClipboard.TryGetInProcessDataObjectAsync` | `IClipboard.TryGetInProcessDataAsync` | [#20521](https://github.com/AvaloniaUI/Avalonia/pull/20521) |

### TopLevel

背景请参阅[`TopLevel` 的变化](#toplevel-changes)。

| 已移除的成员 | 替代方案 | PR |
|---|---|---|
| `IInputRoot` interface | `TopLevel` | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |
| `ITextInputMethodRoot` interface | `TopLevel` | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |
| `IEmbeddedLayoutRoot` interface | `TopLevel` | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |
| `ILayoutRoot` interface | `TopLevel` | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |
| `IRenderRoot` interface | `TopLevel` | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |
| `LayoutManager` class | `ILayoutManager` | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |
| `TopLevel.PlatformSettings` property | `VisualExtensions.GetPlatformSettings` | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |
| `TopLevel.PointerOverElement` property | 删除相关用法 | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |
| `TopLevel.StartRendering/StopRendering` | `EmbeddableControlRoot.StartRendering/StopRendering` | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |
| `VisualExtensions.GetVisualRoot` method | `GetPresentationSource` + `IPresentationSource.RootVisual` | [#20624](https://github.com/AvaloniaUI/Avalonia/pull/20624) |

### 窗口装饰 {#window-decorations}

背景请参阅[窗口装饰的变化](#window-decoration-changes)。

| 已移除的成员 | 替代方案 | PR |
|---|---|---|
| `Chrome.CaptionButtons` class | `WindowDrawnDecorations` | [#20770](https://github.com/AvaloniaUI/Avalonia/pull/20770) |
| `Chrome.TitleBar` class | `WindowDrawnDecorations` | [#20770](https://github.com/AvaloniaUI/Avalonia/pull/20770) |
| `ChromeOverlayLayer` class | `WindowDrawnDecorations` | [#20732](https://github.com/AvaloniaUI/Avalonia/pull/20732) |
| `VisualLayerManager.AdornerLayer` property | `AdornerLayer.GetAdornerLayer` | [#20732](https://github.com/AvaloniaUI/Avalonia/pull/20732) |
| `VisualLayerManager.ChromeOverlayLayer` property | `WindowDrawnDecorations` | [#20732](https://github.com/AvaloniaUI/Avalonia/pull/20732) |
| `VisualLayerManager.LightDismissOverlayLayer` property | 删除相关用法 | [#20732](https://github.com/AvaloniaUI/Avalonia/pull/20732) |
| `VisualLayerManager.OverlayLayer` property | `OverlayLayer.GetOverlayLayer` | [#20732](https://github.com/AvaloniaUI/Avalonia/pull/20732) |
| `Window.ExtendClientAreaChromeHints` property | `Window.WindowDecorations` | [#20770](https://github.com/AvaloniaUI/Avalonia/pull/20770) |
| `SystemDecorations` enum | `WindowDecorations` | [#20796](https://github.com/AvaloniaUI/Avalonia/pull/20796) |
| `ExtendClientAreaChromeHints` enum | `WindowDecorations` | [#20770](https://github.com/AvaloniaUI/Avalonia/pull/20770) |
| `IPopupHostProvider` interface | [`Popup`](/api/avalonia/controls/primitives/popup) | [#20732](https://github.com/AvaloniaUI/Avalonia/pull/20732) |
| `IPopupHost` interface | `Popup` | [#20597](https://github.com/AvaloniaUI/Avalonia/pull/20597) |
| `LightDismissOverlayLayer` class | `VisualLayerManager` | [#20732](https://github.com/AvaloniaUI/Avalonia/pull/20732) |
| `OverlayPopupHost.CreatePopupHost` method | `Popup` | [#20597](https://github.com/AvaloniaUI/Avalonia/pull/20597) |

### 手势事件 {#gesture-events}

背景请参阅[手势事件挪了位置](#gesture-events-moved)。

| 已移除的成员 | 替代方案 | PR |
|---|---|---|
| `Gestures` 类（其全部附加事件） | `InputElement` 上的事件 | [#20789](https://github.com/AvaloniaUI/Avalonia/pull/20789) |

### 焦点处理 {#focus-handling}

背景请参阅[焦点相关的改进](#focus-improvements)。

| 已移除的成员 | 替代方案 | PR |
|---|---|---|
| `GotFocusEventArgs` class | `FocusChangedEventArgs` | [#20859](https://github.com/AvaloniaUI/Avalonia/pull/20859) |
| `KeyboardNavigationHandler` class | `FocusManager` | [#18647](https://github.com/AvaloniaUI/Avalonia/pull/18647) |

### 其他零星移除 {#other-specific-removals}

| 已移除的成员 | 替代方案 | 注释支持情况 | PR |
|---|---|---|---|
| `ResourcesChangedEventArgs.Empty` | `ResourcesChangedEventArgs.Create` | 参见 [`ResourcesChangedEventArgs` 变为结构体](#resourceschangedeventargs-is-a-struct) | [#20576](https://github.com/AvaloniaUI/Avalonia/pull/20576) |
| `TextInputMethodClient.ShowInputPanel` | `InputPaneActivationRequested` event | 直接弹出输入面板在部分平台上行为并不正确 | [#20544](https://github.com/AvaloniaUI/Avalonia/pull/20544) |
| `NativeMenuBar.EnableMenuItemClickForwarding` | 删除相关用法 | 该属性形同虚设 | [#20577](https://github.com/AvaloniaUI/Avalonia/pull/20577) |
| `NativeMenuItemToggleType` enum | `MenuItemToggleType` | 已并入 `MenuItemToggleType` | [#20577](https://github.com/AvaloniaUI/Avalonia/pull/20577) |
| `IGeometryContext2` interface | `IGeometryContext` | `isStroked`/`isFilled` 现在是 `IGeometryContext` 方法上的可选参数 | [#20528](https://github.com/AvaloniaUI/Avalonia/pull/20528) |
| `IWindowImpl.GetWindowsZOrder` | `IWindowingPlatform.GetWindowsZOrder` | 参数类型由 `Span<Window>` 改为 `ReadOnlySpan<IWindowImpl>` | [#20633](https://github.com/AvaloniaUI/Avalonia/pull/20633) |
| `AutoCompleteBox.BindingEvaluator` | 请自行提供实现 | 本属实现细节，却被公开暴露了出来 | [#20596](https://github.com/AvaloniaUI/Avalonia/pull/20596) |
| `CharacterReader` struct | 请自行提供实现 | 本属实现细节，却被公开暴露了出来 | [#19123](https://github.com/AvaloniaUI/Avalonia/pull/19123) |
| `StringTokenizer` struct | 请自行提供实现 | 本属实现细节，却被公开暴露了出来 | [#20544](https://github.com/AvaloniaUI/Avalonia/pull/20544) |
| `Data.Core.PropertyPath` class | 删除相关用法 | 旧版本遗留，已无人使用 | [#19133](https://github.com/AvaloniaUI/Avalonia/pull/19133) |
| `Remote.RemoteServer` class | 删除相关用法 | 遗留产物，且工作不正常 | [#20767](https://github.com/AvaloniaUI/Avalonia/pull/20767) |
| `Remote.RemoteWidget` class | 删除相关用法 | 遗留产物，且工作不正常 | [#20767](https://github.com/AvaloniaUI/Avalonia/pull/20767) |

### 自 Avalonia 11 起即标记为过时 {#obsolete-since-avalonia-11}

下列成员在 Avalonia 11 中已标记为过时，现予移除。

| 已移除的成员 | 替代方案 | PR |
|---|---|---|
| `IInsetsManager.DisplayEdgeToEdge` | `IInsetsManager.DisplayEdgeToEdgePreference` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `CustomAnimatorBase` / `CustomAnimatorBase<T>` | `InterpolatingAnimator<T>` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `CubicBezierEasing` | `SplineEasing` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `AppBuilder.LifetimeOverride` | 改用任意一种预定义的生命周期 | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `AvaloniaObjectExtensions.Bind` | `AvaloniaObject.Bind` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `IActivatableApplicationLifetime` | `Application.Current.TryGetFeature<IActivatableLifetime>` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `ContextMenu.PlacementMode` | `ContextMenu.Placement` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `FileDialog` / `FileSystemDialog` / `SystemDialog` | `IStorageProvider` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `OpenFileDialog` | `IStorageProvider.OpenFilePickerAsync` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `OpenFolderDialog` | `IStorageProvider.OpenFolderPickerAsync` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `SaveFileDialog` | `IStorageProvider.SaveFilePickerAsync` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `ManagedFileDialogExtensions.ShowManagedAsync` | `IStorageProvider.OpenFilePickerAsync` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `ItemContainerGenerator.ContainerFromIndex` | `ItemsControl.ContainerFromIndex` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `ItemContainerGenerator.IndexFromContainer` | `ItemsControl.IndexFromContainer` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `TreeContainerIndex` | `TreeView` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `TreeItemContainerGenerator` | `ItemContainerGenerator` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `ItemsControl.ItemsControlFromItemContaner` | `ItemsControl.ItemsControlFromItemContainer` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `ToggleButton.Checked/Unchecked/Indeterminate` 事件 | `ToggleButton.IsCheckedChanged` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `TabItem.SubscribeToOwnerProperties` | 删除相关用法 | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `BindingPriority.TemplatedParent` | `BindingPriority.Template` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `CompiledBindingPathBuilder.SetRawSource` | `CompiledBinding.Source` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `Color.ToUint32` | `Color.ToUInt32` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `DrawingContext.PushPreTransform/PushPostTransform/PushTransformContainer` | `DrawingContext.PushTransform` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `ImmutableRadialGradientBrush.Radius` | `RadiusX` and `RadiusY` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `IRadialGradientBrush.Radius` | `RadiusX` and `RadiusY` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `RadialGradientBrush.Radius` | `RadiusX` and `RadiusY` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `IApplicationPlatformEvents` | `Application.Current.TryGetFeature<IActivatableLifetime>` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `Popup.PlacementMode` | `Popup.Placement` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `Screen.PixelDensity` | `Screen.Scaling` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `Screen.Primary` | `Screen.IsPrimary` | [#20617](https://github.com/AvaloniaUI/Avalonia/pull/20617) |
| `ICompositionGpuImportedObject.ImportCompeted` | `ImportCompleted` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |
| `IStyleable` interface | `StyledElement` | [#20613](https://github.com/AvaloniaUI/Avalonia/pull/20613) |


## 重命名的成员 {#renamed-members}

| 旧名称 | 新名称 | 注释支持情况 | PR |
|---|---|---|---|
| `PseudolassesExtensions` | `PseudoClassesExtensions` | 拼写修正。该类型通常是从 XAML 隐式使用，或作为 C# 扩展方法使用，因此大多数代码库不受影响。 | [#18717](https://github.com/AvaloniaUI/Avalonia/pull/18717) |
| `X11PlatformOptions.ExterinalGLibMainLoopExceptionLogger` | `ExternalGLibMainLoopExceptionLogger` | 拼写修正。 | [#19128](https://github.com/AvaloniaUI/Avalonia/pull/19128) |
| `TextBox.Watermark` | `TextBox.PlaceholderText` | 旧属性保留，但标记为过时。 | [#20303](https://github.com/AvaloniaUI/Avalonia/pull/20303) |
| `TextBox.UseFloatingWatermark` | `TextBox.UseFloatingPlaceholder` | 旧属性保留，但标记为过时。 | [#20303](https://github.com/AvaloniaUI/Avalonia/pull/20303) |
| `Window.SystemDecorations` | `Window.WindowDecorations` | 旧属性保留，但标记为过时。参见[窗口装饰的变化](#window-decoration-changes)。 | [#20796](https://github.com/AvaloniaUI/Avalonia/pull/20796) |
| `RenderOptions.TextRenderingMode` | `TextOptions.TextRenderingMode` | `TextOptions` 还包含 `TextHintingMode` 和 `BaselinePixelAlignment`。参见[文本选项](/docs/graphics-animation/text-options)。 | [#20107](https://github.com/AvaloniaUI/Avalonia/pull/20107) |
| `TextBlock.LetterSpacing` | `TextElement.LetterSpacing` | 现在它是一个可继承的附加属性，所有模板化控件都能用。写在 `TextBlock` 上的 XAML 保持源码兼容；代码中引用 `TextBlock.LetterSpacingProperty` 的地方请改为 `TextElement.LetterSpacingProperty`。 | [#20141](https://github.com/AvaloniaUI/Avalonia/pull/20141) |

## 另请参阅 {#see-also}

- [Avalonia 12 发行说明](https://github.com/AvaloniaUI/Avalonia/releases)
