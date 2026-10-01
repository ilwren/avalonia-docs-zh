---
id: performance
title: 性能优化
description: 用虚拟化、高效布局、编译型绑定和性能剖析来优化 Avalonia 应用的性能。
doc-type: how-to
---

本指南介绍 Avalonia 应用常见的性能考量，以及保持界面流畅的若干技巧。

## UI 虚拟化 {#ui-virtualization}

显示大型集合时，虚拟化能保证只为可见项创建和渲染控件。有些控件默认就支持虚拟化，比如 [`ListBox`](/controls/data-display/collections/listbox)。

### 虚拟化的运作原理 {#how-virtualization-works}

虚拟化面板不会为集合中的每一项都创建控件，而是只为可见项创建。用户滚动时，移出屏幕的控件会被回收复用给新进入视野的项。

### 确认虚拟化真的生效了 {#ensuring-virtualization-is-active}

虚拟化要求高度是受限的。如果某项处在一个会给它无限高度的控件里，虚拟化就会失效。

```xml
<!-- DON'T: StackPanel gives infinite height, disabling virtualization -->
<StackPanel>
    <ListBox ItemsSource="{Binding LargeCollection}" />
</StackPanel>

<!-- DO: Grid row with * constrains height -->
<Grid RowDefinitions="*">
    <ListBox ItemsSource="{Binding LargeCollection}" />
</Grid>

<!-- DO: DockPanel fill area constrains height -->
<DockPanel>
    <TextBlock DockPanel.Dock="Top" Text="Items" />
    <ListBox ItemsSource="{Binding LargeCollection}" />
</DockPanel>
```

### 用缓冲系数让滚动更顺滑 {#buffer-factor-for-smooth-scrolling}

`VirtualizingStackPanel` 提供了 `BufferFactor` 属性，可在可见视口之外额外保留一部分已实例化的项。这能减少滚动过程中的回收频率，从而消除卡顿——在移动设备上效果尤为明显。

```xml
<ListBox ItemsSource="{Binding LargeCollection}">
    <ListBox.ItemsPanel>
        <ItemsPanelTemplate>
            <VirtualizingStackPanel BufferFactor="1" />
        </ItemsPanelTemplate>
    </ListBox.ItemsPanel>
</ListBox>
```

`BufferFactor` 设为 `1` 时，会在可见区域的上下各多实例化一个视口高度的项。默认值是 `0`（不留缓冲）。值越大越费内存，但滚动越顺滑。

### 高度不一的项 {#variable-height-items}

`VirtualizingStackPanel` 是针对「所有项等高」的集合优化的。面板按项数来估算滚动范围，因此项高参差不齐的集合会导致滚动条跳动和布局重算。如果你的项高度差异很大，可以考虑这几种办法：

- **统一高度。**给所有项设定固定的 `Height` 或 `MinHeight`，让虚拟化面板能准确算出滚动范围。内容超出估算尺寸时，让它裁剪或在内部滚动。
- **把层级数据拍平。**与其在虚拟化列表里嵌套展开器，不如把树拍平成带缩进层级的单层列表，这样虚拟化面板就能直接管理行。`TreeView` 内部用的正是这种办法。
- **限制已实例化的项数。**如果虚拟化实在做不到（比如带展开器的复杂属性网格），那就限制同时存在的控件数量：只加载可见部分，等用户展开或滚动时再按需创建更多项。

### 降低控件模板的复杂度 {#reducing-control-template-complexity}

[`TextBox`](/controls/input/text-input/textbox) 这类复杂控件的视觉树很深，包含边框、滚动视图和水印层。一旦你创建了很多个，模板实例化和测量就会主宰启动耗时。

**平时用轻量控件显示，交互时再换。**比如用 `TextBlock`（视觉树极简）来展示数值，只在用户点击编辑时才换成 `TextBox`：

```csharp
// In your DataTemplate code-behind or custom control
var display = new TextBlock { Text = field.Value };
display.PointerPressed += (s, e) =>
{
    var editor = new TextBox { Text = field.Value };
    editor.LostFocus += (s2, e2) =>
    {
        field.Value = editor.Text;
        parent.Children.Remove(editor);
        parent.Children.Add(display);
    };
    parent.Children.Remove(display);
    parent.Children.Add(editor);
};
```

**给重型控件重做模板。**如果非得到处使用 `TextBox`，那就写一个精简版控件主题，去掉不必要的视觉元素（比如水印、清除按钮、滚动视图），以降低视觉树深度：

```xml
<ControlTheme x:Key="LightTextBox" TargetType="TextBox">
    <Setter Property="Template">
        <ControlTemplate>
            <Border Background="{TemplateBinding Background}"
                    BorderBrush="{TemplateBinding BorderBrush}"
                    BorderThickness="{TemplateBinding BorderThickness}">
                <TextPresenter Name="PART_TextPresenter"
                               Text="{TemplateBinding Text}"
                               CaretBrush="{TemplateBinding CaretBrush}" />
            </Border>
        </ControlTemplate>
    </Setter>
</ControlTheme>
```

再把它套用到那些用不上全部功能的控件上：

```xml
<TextBox Theme="{StaticResource LightTextBox}" Text="{Binding Value}" />
```

## 布局优化 {#layout-optimization}

### 避免层层嵌套 {#avoiding-deep-nesting}

每多一层嵌套，就多一轮测量和排列。能拍平的布局就尽量拍平：

```xml
<!-- Avoid: deeply nested layout -->
<StackPanel>
    <Border>
        <StackPanel>
            <Border>
                <TextBlock Text="Hello" />
            </Border>
        </StackPanel>
    </Border>
</StackPanel>

<!-- Prefer: flat layout -->
<StackPanel>
    <TextBlock Text="Hello" Margin="8" />
</StackPanel>
```

### 用 Grid 取代嵌套的 StackPanel {#replacing-nested-stack-panels-with-grids}

一个带行列定义的 `Grid` 比若干层嵌套的 `StackPanel` 更高效：

```xml
<!-- Instead of nested StackPanels -->
<Grid ColumnDefinitions="Auto,*" RowDefinitions="Auto,Auto,Auto" RowSpacing="4">
    <TextBlock Grid.Row="0" Grid.Column="0" Text="Name:" />
    <TextBox Grid.Row="0" Grid.Column="1" Text="{Binding Name}" />
    <TextBlock Grid.Row="1" Grid.Column="0" Text="Email:" />
    <TextBox Grid.Row="1" Grid.Column="1" Text="{Binding Email}" />
</Grid>
```

### 尽量少触发 `InvalidateArrange` 和 `InvalidateMeasure` {#minimizing-invalidatearrange-and-invalidatemeasure}

影响布局的属性变化（比如 `Width`、`Height`、`Margin`、`Padding`）会触发布局重算。能批量改就批量改：

```csharp
// Set multiple properties together; Avalonia batches layout
// passes within a single dispatcher operation automatically.
myControl1.Width = 100;
myControl2.Height = 200;
```

## 渲染性能 {#rendering-performance}

### 用 `IsVisible` 隐藏用不到的控件 {#hiding-unused-controls-with-isvisible}

对那些按条件显示的内容，设置 `IsVisible="False"` 能省下不少开销：控件会同时退出布局和渲染。布局系统会跳过该控件及其整棵子树的测量与排列，渲染器也不会绘制它。

此外，隐藏控件默认还会暂停它及其子树上正在播放的[关键帧动画](/docs/graphics-animation/keyframe-animations#playback-behavior)，免得界面空闲时动画还在不停唤醒 CPU。

```xml
<Panel>
    <StackPanel IsVisible="{Binding ShowDetails}">
        <!-- Complex content: only measured and rendered when visible -->
    </StackPanel>
</Panel>
```

如果你只想在视觉上隐藏控件、同时保留它占的布局空间，请改用 `Opacity="0"`。`Opacity="0"` 的元素仍然参与布局、仍可接收输入，其关键帧动画也会继续播放。

### 审慎使用 `ClipToBounds` {#using-cliptobounds-judiciously}

`ClipToBounds="True"` 会创建一个裁剪层。只有当子内容确实会超出控件边界时才用它。

### 降低命中测试的开销 {#reducing-hit-testing-cost}

指针事件发生时，Avalonia 会遍历视觉树并逐个测试元素。若某个控件的子元素极多，这种线性遍历会让「点击」到「收到事件」之间出现肉眼可察的延迟。

给不需要指针交互的元素设置 `IsHitTestVisible="False"`。对象众多的场景，可以考虑基于覆盖层的命中测试策略或自定义渲染。相关模式与代码示例参见[命中测试：元素众多时的性能](/docs/graphics-animation/hit-testing#performance-with-many-elements)。

透明元素同样参与命中测试。若某个透明控件不需要指针交互，设置 `IsHitTestVisible="False"` 把它排除在命中测试之外。

```xml
<Border Background="Transparent" IsHitTestVisible="False">
    <!-- Overlay that should not capture clicks -->
</Border>
```

### 降低视觉复杂度 {#reducing-visual-complexity}

- 尽量少用 `BoxShadow` 效果，每一个都会额外增加一轮渲染。
- 避免让半透明元素相互重叠。
- 把 `Opacity` 设在父元素上，而不是逐个设在子元素上。

### 位图缓存 {#bitmap-cache}

对于渲染代价高但很少变化的视觉内容，可以用 `BitmapCache` 把它们栅格化到一张位图表面上。控件及其子元素只渲染一次到中间位图，之后的帧都复用这张位图，直到内容发生变化。

```xml
<Border BoxShadow="0 4 8 0 #40000000" CornerRadius="8">
    <Border.CacheMode>
        <BitmapCache RenderAtScale="1" />
    </Border.CacheMode>
    <!-- Complex content rendered once and cached -->
</Border>
```

#### `BitmapCache` 的属性 {#bitmapcache-properties}

| 属性 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `RenderAtScale` | `double` | `1` | 缓存位图的分辨率倍数。大于 1 可提升质量；小于 1 则以画质换内存；设为 0 表示关闭缓存。 |
| `SnapsToDevicePixels` | `bool` | `false` | 把缓存位图对齐到设备像素边界，让文字和线条渲染得更锐利。 |
| `EnableClearType` | `bool` | `false` | 在缓存表面内启用 `ClearType` 次像素文本渲染。不启用的话，缓存中的文字会使用灰度抗锯齿。 |

文字密集的内容，建议开启 `SnapsToDevicePixels` 和 `EnableClearType` 之后再缓存。

```xml
<Border>
    <Border.CacheMode>
        <BitmapCache SnapsToDevicePixels="True" EnableClearType="True" />
    </Border.CacheMode>
    <TextBlock Text="Cached text with ClearType rendering" />
</Border>
```

### 位图插值模式 {#bitmap-interpolation-mode}

对不需要高质量缩放的图片，用较低的插值模式即可：

```xml
<Image Source="avares://MyApp/Assets/thumbnail.png"
       RenderOptions.BitmapInterpolationMode="LowQuality" />
```

### GPU 资源缓存大小 {#gpu-resource-cache-size}

Avalonia 默认使用带 GPU 加速的 Skia。Skia 会为纹理等 GPU 表面维护一份资源缓存，默认上限约 28 MB。如果你的应用要处理大图、瓦片集或大量缓存视觉内容，超出缓存上限的图片每帧都得重新上传到 GPU，画面就会发卡。

在启动时配置 `SkiaOptions` 即可调高缓存上限：

```csharp
AppBuilder.Configure<App>()
    .UsePlatformDetect()
    .With(new SkiaOptions
    {
        MaxGpuResourceSizeBytes = 256 * 1024 * 1024 // 256 MB
    });
```

请按目标硬件选择合适的数值。多数集成显卡至少有 2 GB 共享内存，所以桌面应用取 256 MB 或 512 MB 都很稳妥；移动设备可能要调低一些。

### 按区域裁剪脏矩形 {#region-dirty-rect-clipping}

内容变化时，Avalonia 只重绘屏幕上受影响的（即「脏」的）区域，而不是整帧。[`CompositionOptions.UseRegionDirtyRectClipping`](/api/avalonia/rendering/composition/compositionoptions) 借助区域（region）实现更精确的脏矩形跟踪，代价是渲染过程要多花一些 CPU 时间。

从 Avalonia 12.1 起，这个选项**默认关闭**，以免拖累帧率。

要启用区域裁剪，必须在启动时于 `CompositionOptions` 中显式设置 `UseRegionDirtyRectClipping = true`。在某些没有 GPU 加速的目标平台上（比如[嵌入式 Linux](/docs/platform-specific-guides/embedded-linux)或其他软件渲染的设备），少画一点比裁剪本身的开销更划算，这时启用它就很有意义。

```csharp
AppBuilder.Configure<App>()
    .UsePlatformDetect()
    .With(new CompositionOptions
    {
        UseRegionDirtyRectClipping = true
    });
```

启用区域裁剪后，`MaxDirtyRects` 限定每帧最多跟踪多少个脏矩形，默认是 `8`。把它设为 0 或负数，则跳过 Avalonia 自己的跟踪，直接使用底层绘图上下文的区域支持。

## 数据绑定性能 {#data-binding-performance}

### 编译绑定 {#compiled-bindings}

编译型绑定在编译期就解析好属性路径，免去了运行时反射。[从 Avalonia 12 起它默认启用](/docs/avalonia12-breaking-changes#compiled-bindings-are-enabled-by-default)。

### 避免没必要的绑定 {#avoiding-unnecessary-bindings}

那些永远不变的属性，直接写静态值，别用绑定：

```xml
<!-- Unnecessary binding for a constant -->
<TextBlock Text="{Binding AppTitle}" />

<!-- Better: static resource or literal -->
<TextBlock Text="{StaticResource AppTitle}" />
<TextBlock Text="My Application" />
```

### 静态数据用一次性绑定 {#using-one-time-bindings-for-static-data}

如果某个值只设一次、此后不再变化，用 `OneTime` 模式即可省去持续的变更跟踪：

```xml
<TextBlock Text="{Binding Version, Mode=OneTime}" />
```

## Collections

### 中小型列表用 `ObservableCollection` {#using-observablecollection-for-small-to-medium-lists}

`ObservableCollection<T>` 能高效地把单个项的增删通知给界面。

### 批量更新 {#batching-large-updates}

一次要添加很多项时，与其逐项添加，不如直接替换整个集合：

```csharp
// Slow: triggers UI update for each add
foreach (var item in newItems)
    Items.Add(item);

// Faster: single collection replacement
Items = new ObservableCollection<Item>(newItems);
OnPropertyChanged(nameof(Items));
```

### 增量加载 {#incremental-loading}

如果你不得不在没有虚拟化的情况下创建大量控件（比如属性网格或检查器面板），一次性全加上去会在测量阶段阻塞 UI 线程。正确做法是分批添加，每批之间把控制权让回调度器，界面才不会卡住：

```csharp
private async Task LoadItemsIncrementally(IList<ItemViewModel> items, Panel container)
{
    const int batchSize = 50;

    for (int i = 0; i < items.Count; i += batchSize)
    {
        var batch = items.Skip(i).Take(batchSize);
        foreach (var item in batch)
        {
            container.Children.Add(CreateControl(item));
        }

        // Yield to the UI thread so the frame can render
        await Dispatcher.UIThread.Yield(DispatcherPriority.Background);
    }
}
```

批大小要足够让第一轮就填满可见区域，这样用户能立刻看到内容，剩下的项再逐步加载。

### 大型响应式集合用 `DynamicData` {#using-dynamicdata-for-large-reactive-collections}

对于需要频繁排序、筛选或做复杂变换的集合，[DynamicData](https://github.com/reactivemarbles/DynamicData) 提供了经过优化的响应式管线，能把界面更新降到最少。

## 异步与线程 {#async-and-threading}

### 别占着 UI 线程 {#keeping-the-ui-thread-free}

把繁重的计算挪到后台线程：

```csharp
var data = await Task.Run(() => LoadLargeDataSet());
Items = new ObservableCollection<Item>(data);
```

### 为快速输入做防抖 {#debouncing-rapid-input}

在「边打边搜」这类场景里，给输入加上防抖，免得每敲一个键就跑一次昂贵的操作：

```csharp
this.WhenAnyValue(x => x.SearchText)
    .Throttle(TimeSpan.FromMilliseconds(300))
    .Subscribe(text => ApplyFilter(text));
```

### 用 `DispatcherPriority.Background` 推迟处理 {#using-dispatcherprioritybackground-for-deferred-work}

把低优先级的更新安排到 UI 线程空闲时再执行：

```csharp
Dispatcher.UIThread.Post(() =>
{
    // Low priority work
    UpdateStatistics();
}, DispatcherPriority.Background);
```

## Profiling

### Avalonia DevTools

在调试版本中按 **F12** 可打开 DevTools，其中的 **Performance** 标签页会显示帧耗时信息。

### dotTrace 与 dotMemory {#dottrace-and-dotmemory}

JetBrains 的性能剖析工具同样适用于 Avalonia 应用，可以用它们找出热点路径和内存泄漏。

### 诊断浮层 {#diagnostic-overlays}

在 `App.axaml.cs` 中启用 FPS 浮层：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    // Add FPS overlay in debug builds
#if DEBUG
    this.AttachDevTools();
#endif
}
```

## 另请参阅 {#see-also}

- [线程模型](/docs/app-development/threading)：UI 线程与 Dispatcher 的用法。
- [编译型绑定](/docs/data-binding/compiled-bindings)：编译期绑定校验与性能。
- [集合视图](/docs/data-binding/collection-views)：高效地筛选和排序集合。
- [命中测试](/docs/graphics-animation/hit-testing)：命中测试的机制，以及元素众多时的性能。
