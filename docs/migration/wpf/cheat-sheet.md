---
id: cheat-sheet
title: WPF 到 Avalonia 速查表
description: 一张速查表，把 WPF 的概念、控件和 API 对应到 Avalonia 中的等价物。
doc-type: migration
---

这是给转向 Avalonia 的 WPF 开发者准备的速查表。每一条都给出 WPF 中的概念及其 Avalonia 对应物。

## XAML 命名空间 {#xaml-namespace}

| WPF | Avalonia |
|---|---|
| `xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"` | `xmlns="https://github.com/avaloniaui"` |
| `xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"` | Same |
| `xmlns:local="clr-namespace:MyApp"` | `xmlns:local="using:MyApp"`（推荐）或 `clr-namespace:` |

## 属性系统 {#property-system}

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `DependencyProperty` | `StyledProperty` | 支持样式、动画与继承 |
| `DependencyProperty` (perf-critical) | `DirectProperty` | 更快，但不支持样式和动画 |
| `DependencyProperty.Register()` | `AvaloniaProperty.Register<TOwner, TValue>()` | 泛型注册 |
| `DependencyProperty.RegisterAttached()` | `AvaloniaProperty.RegisterAttached<TValue>()` | 附加属性 |
| `PropertyMetadata` | `StyledPropertyMetadata<T>` | 类型安全的元数据 |
| `CoerceValueCallback` | 通过元数据指定 `CoerceValueCallback` | 概念相同 |
| 元数据中的 `PropertyChanged` 回调 | `Register` 中的 `propertyChanged` 回调 | 直接传入 |

## Styling

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `<Style TargetType="Button">` | `<Style Selector="Button">` | 类 CSS 的选择器 |
| `Style.Triggers` | Pseudo-classes (`:pointerover`, `:pressed`) | Avalonia 中没有触发器 |
| `DataTrigger` | 绑定 + 伪类或转换器 | 见下文 |
| `EventTrigger` | 作用在伪类上的动画 | |
| `VisualStateManager` | Pseudo-classes | `:pointerover`, `:pressed`, `:disabled`, `:checked` |
| `BasedOn="{StaticResource ...}"` | 不需要；选择器本身就能组合 | |
| `Style x:Key="..."` | 样式类：`<Style Selector="Button.primary">` | |
| `Style="{StaticResource ButtonStyle}"` | `Classes="primary"` | |
| `ControlTemplate.Triggers` | 伪类选择器 | |
| `TemplateBinding` | `TemplateBinding` | 概念相同，不过 Avalonia 还支持 `Mode=TwoWay` |
| `{RelativeSource TemplatedParent}` | `{TemplateBinding}` or `$parent[ControlType]` | |

### DataTrigger 的等价写法 {#datatrigger-equivalent}

WPF：
```xml
<DataTrigger Binding="{Binding IsActive}" Value="True">
    <Setter Property="Background" Value="Green" />
</DataTrigger>
```

Avalonia（改用转换器或自定义伪类）：
```xml
<Style Selector="Border.status">
    <Setter Property="Background" Value="Red" />
</Style>
<Style Selector="Border.status[(vm:MyViewModel.IsActive)]">
    <Setter Property="Background" Value="Green" />
</Style>
```

或者用绑定转换器：
```xml
<Border Background="{Binding IsActive, Converter={StaticResource BoolToColorConverter}}" />
```

## 数据绑定 {#data-binding}

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `{Binding Path}` | `{Binding Path}` | 语法相同 |
| `{Binding Path, Mode=TwoWay}` | `{Binding Path, Mode=TwoWay}` | Same |
| `{Binding RelativeSource={RelativeSource Self}}` | `{Binding $self.Property}` | 简写写法 |
| `{Binding RelativeSource={RelativeSource AncestorType=Grid}}` | `{Binding $parent[Grid].Property}` | |
| `{Binding RelativeSource={RelativeSource TemplatedParent}}` | `{TemplateBinding Property}` | |
| `{Binding ElementName=myControl, Path=Text}` | `{Binding #myControl.Text}` | `#name` 语法 |
| `CompiledBinding` | `{CompiledBinding}` or `x:CompileBindings="True"` | 编译期校验 |
| `MultiBinding` | `MultiBinding` | 概念相同 |
| `IValueConverter` | `IValueConverter` | 接口相同 |
| `IMultiValueConverter` | `IMultiValueConverter` | 接口相同 |
| `FallbackValue` | `FallbackValue` | Same |
| `TargetNullValue` | `TargetNullValue` | Same |
| `StringFormat` | `StringFormat` | Same |
| `UpdateSourceTrigger` | 不需要；默认行为就很合理 | TextBox 在文本变化时即更新 |

## Controls

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `Window` | `Window` | Same |
| `UserControl` | `UserControl` | Same |
| `Button` | `Button` | Same |
| `TextBlock` | `TextBlock` | Same |
| `TextBox` | `TextBox` | Same |
| `CheckBox` | `CheckBox` | Same |
| `RadioButton` | `RadioButton` | Same |
| `ComboBox` | `ComboBox` | Same |
| [`ListBox`](/api/avalonia/controls/listbox) | `ListBox` | Same |
| `ListView` | `ListBox` | 改用 ListBox 配 ItemTemplate |
| `TreeView` | `TreeView` | Same |
| `DataGrid` | `DataGrid`（NuGet 包） | 独立的包 |
| `TabControl` | `TabControl` | Same |
| `Expander` | `Expander` | Same |
| `Slider` | `Slider` | Same |
| `ProgressBar` | `ProgressBar` | Same |
| `ToolTip` | `ToolTip` | 附加属性：`ToolTip.Tip` |
| `StatusBar` | 没有直接对应者 | 改用带样式的面板 |
| `Menu` | `Menu` | Same |
| `ContextMenu` | `ContextMenu` | Same |
| `Popup` | `Popup` | Same |
| `ScrollViewer` | `ScrollViewer` | Same |
| `Image` | `Image` | Same |
| [`Border`](/api/avalonia/controls/border) | `Border` | 相同；支持 `BoxShadow` |
| `Viewbox` | `Viewbox` | Same |
| `ContentControl` | `ContentControl` | Same |
| `ItemsControl` | `ItemsControl` | Same |
| `StackPanel` | `StackPanel` | Same |
| `Grid` | `Grid` | 相同；可用 `ColumnDefinitions="Auto,*"` 简写 |
| `DockPanel` | `DockPanel` | Same |
| `WrapPanel` | `WrapPanel` | Same |
| `Canvas` | `Canvas` | Same |
| `UniformGrid` | `UniformGrid` | Same |
| `GroupBox` | [`GroupBox`](/controls/layout/containers/groupbox) | Same |
| `RichTextBox` | 没有内置的对应者 | 改用第三方编辑器 |

## Layout

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `Grid.RowDefinitions="Auto,*"` | 简写相同 | 两者都支持内联写法 |
| `DockPanel.LastChildFill` | `DockPanel.LastChildFill` | Same |
| `HorizontalAlignment` | `HorizontalAlignment` | Same |
| `VerticalAlignment` | `VerticalAlignment` | Same |
| `Margin="10,5"` | `Margin="10,5"` | Same |
| `SharedSizeGroup` | `SharedSizeGroup` | Same |
| `Visibility` (`Visible`/`Collapsed`/`Hidden`) | `IsVisible` (`bool`) | `IsVisible="False"` 等同于 WPF 的 `Collapsed`（从布局中移除）。若要 WPF 中 `Hidden` 的效果（不可见但仍占位），请改用 `Opacity="0"`。 |

## 资源 {#resources}

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `StaticResource` | `StaticResource` | 相同（只解析一次） |
| `DynamicResource` | `DynamicResource` | 相同（会跟踪变化） |
| `MergedDictionaries` | `MergedDictionaries` | Same |
| `ResourceDictionary` | `ResourceDictionary` | Same |
| `ThemeDictionaries` | `ResourceDictionary.ThemeDictionaries` | 浅色/深色变体 |

## 事件 {#events}

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| [`RoutedEvent`](/api/avalonia/interactivity/routedevent) (Bubble) | `RoutedEvent` (Bubble) | Same |
| `RoutedEvent` (Tunnel) | `RoutedEvent` (Tunnel) | Same |
| `Preview*` 事件 | 隧道路由策略 | 用 `AddHandler` 配 `RoutingStrategies.Tunnel` |
| `EventManager.RegisterRoutedEvent` | `RoutedEvent.Register<T, TArgs>` | 泛型注册 |
| `e.Handled = true` | `e.Handled = true` | Same |
| `AddHandler(event, handler, handledEventsToo)` | 签名相同 | Same |
| 类处理程序 | `Event.AddClassHandler<T>()` | 概念相同 |

## Commands

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `ICommand` | `ICommand` | 接口相同 |
| `RoutedCommand` | 没有内置的对应者 | 改用 `ICommand` 的实现 |
| `CommandBinding` | 没有对应者 | 直接绑定命令 |
| `InputBinding` / `KeyBinding` | `KeyBinding` | 概念相同 |
| `RelayCommand`（MVVM 工具包） | `RelayCommand` (CommunityToolkit.Mvvm) | 同一个库照样能用 |

## Templates

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| [`DataTemplate`](/api/avalonia/markup/xaml/templates/datatemplate) | `DataTemplate` | Same |
| `HierarchicalDataTemplate` | `TreeDataTemplate` | 名称不同 |
| `ControlTemplate` | `ControlTemplate` | Same |
| `DataTemplateSelector` | `DataTemplate` with `DataType` | 改用 DataType 匹配 |
| `ContentPresenter` | `ContentPresenter` | Same |
| `ItemsPresenter` | `ItemsPresenter` | Same |
| `PART_` 命名约定 | `PART_` 命名约定 | Same |

## Threading

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `Dispatcher.Invoke()` | `Dispatcher.UIThread.InvokeAsync()` | 默认就是异步的 |
| `Dispatcher.BeginInvoke()` | `Dispatcher.UIThread.Post()` | Fire-and-forget |
| `Dispatcher.CurrentDispatcher` | `Dispatcher.CurrentDispatcher` | Same API |
| `Dispatcher.FromThread()` | `Dispatcher.FromThread()` | Same API |
| `DependencyObject.Dispatcher` | `AvaloniaObject.Dispatcher` | 每个对象各有一个 dispatcher |
| `Dispatcher.CheckAccess()` | `Dispatcher.UIThread.CheckAccess()` | Same |
| `Dispatcher.Yield()` | `Dispatcher.Yield()` | Same API |
| `DispatcherPriority` | `DispatcherPriority` | 枚举相同 |

## Animations

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `Storyboard` | `Animation` | Different API |
| `DoubleAnimation` | 关键帧动画 | 用 `KeyFrame` 配 `Cue` |
| `BeginStoryboard` | 动画声明在 `Style.Animations` 中 | 由伪类触发 |
| `EasingFunction` | `Easing` property | 可用的缓动类型相同 |
| `Transitions` (UWP) | `Transitions` | 属性变化动画 |
| `CompositionTarget.Rendering` | `TopLevel.RequestAnimationFrame()` | UI 线程上的逐帧回调；若需要渲染线程上的回调，另见 `CompositionCustomVisualHandler` |

## Window

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `AllowsTransparency="True"` | `TransparencyLevelHint="Transparent"` | Avalonia 不支持 WPF 那种「透明穿透点击」的行为。 |
| `WindowStyle="None"` | `WindowDecorations="None"` | 去掉标题栏和边框 |
| `ResizeMode` | `CanResize` | 用布尔值而非枚举 |

## Graphics

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `SolidColorBrush` | `SolidColorBrush` | Same |
| `LinearGradientBrush` | `LinearGradientBrush` | Same |
| `RadialGradientBrush` | `RadialGradientBrush` | Same |
| `ImageBrush` | `ImageBrush` | Same |
| [`VisualBrush`](/api/avalonia/media/visualbrush) | `VisualBrush` | Same |
| `DrawingBrush` | 不可用 | Use `VisualBrush` |
| `BitmapEffect` | `Effect` property | `BlurEffect`, `DropShadowEffect` |
| `DropShadowEffect` | `BoxShadow` on `Border` | API 不同，走的是类 CSS 那一套 |
| `RenderTransform` | `RenderTransform` | 相同；并且支持 CSS 简写 |
| `LayoutTransform` | `LayoutTransformControl` | 包进一个控件里 |
| `Clip` | `Clip` | Same |
| `OpacityMask` | `OpacityMask` | Same |
| `Path` | `Path` | 相同；迷你语言也一样 |

## 平台服务 {#platform-services}

| WPF | Avalonia | 注释支持情况 |
|---|---|---|
| `SystemParameters.PrimaryScreenWidth` | `TopLevel.GetTopLevel(this).Screens.Primary.Bounds.Width` | 在任意 `TopLevel` 上通过 [`Screens`](/api/avalonia/controls/screens) 访问 |
| `System.Windows.Forms.Screen.AllScreens` | `TopLevel.GetTopLevel(this).Screens.All` | 返回所有已连接的显示器 |
| `System.Windows.Forms.Screen.PrimaryScreen.WorkingArea` | `TopLevel.GetTopLevel(this).Screens.Primary.WorkingArea` | 不含任务栏/程序坞 |
| `PresentationSource.FromVisual().CompositionTarget.TransformToDevice` | `TopLevel.GetTopLevel(this).Screens.Primary.Scaling` | DPI 缩放系数 |

完整用法请参阅[使用屏幕](/docs/app-development/window-management#working-with-screens)。

## 文件结构 {#file-structure}

| WPF | Avalonia |
|---|---|
| `.xaml` extension | `.axaml` extension |
| `App.xaml` | `App.axaml` |
| `MainWindow.xaml` | `MainWindow.axaml` |
| `.xaml.cs` code-behind | `.axaml.cs` code-behind |
| `.csproj` WPF SDK | `.csproj` Avalonia SDK |

## 常见的坑 {#common-gotchas}

1. **没有触发器**：Avalonia 用伪类和类 CSS 的选择器取代了 WPF 的触发器。请参阅[伪类](/docs/styling/pseudoclasses)。

2. **用样式选择器而非 TargetType**：样式用的是类 CSS 的选择器（`Button.primary:pointerover`），而不是 `TargetType` + `Triggers`。

3. **用 x:Name 而非 Name**：Avalonia XAML 中请用 `x:Name`。`Name` 属性虽然存在，但 `x:Name` 才是标准写法。

4. **绑定路径语法**：用 `#elementName.Property` 代替 `ElementName=elementName, Path=Property`，用 `$parent[Type]` 代替 `RelativeSource AncestorType`。

5. **没有 RoutedCommand**：Avalonia 没有 WPF 那套 `RoutedCommand` 基础设施，请改用 `ICommand` 的实现（推荐 CommunityToolkit.Mvvm）。

6. **DataGrid 是单独的包**：请从 NuGet 安装 `Avalonia.Controls.DataGrid`。

7. **是 TreeDataTemplate 而非 HierarchicalDataTemplate**：名字不同，概念完全一致。

8. **布局变换**：用 `LayoutTransformControl` 包起来，而不是用 `LayoutTransform` 属性。

9. **资产用 avares://**：资源 URI 用的是 `avares://AssemblyName/path`，而非 `pack://application:,,,/`。

10. **默认绑定模式**：有些控件的默认绑定模式与 WPF 不同。若某个绑定没有如期更新，请查一查该控件的文档。

## 另请参阅 {#see-also}

- [从 WPF 迁移](/docs/migration/wpf)：详细的迁移指南。
- [Avalonia 架构](/docs/fundamentals/architecture)：Avalonia 内部是怎么运作的。
- [样式选择器](/docs/styling/style-selectors)：类 CSS 的选择器语法。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：Avalonia 的绑定语法。
