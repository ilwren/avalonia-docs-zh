---
id: architecture
title: Avalonia 架构
description: 控件如何被测量、排列、渲染，又是如何对接各平台后端的。
doc-type: explanation
video:
  src: https://youtu.be/inBjiXfGhoU
  title: 深入 Avalonia 架构 —— 从 Win32 到浏览器，同一条渲染管线
---

本文介绍 Avalonia 的内部架构：控件如何完成测量、排列与渲染，合成器如何调度每一帧，以及各平台后端如何接入渲染管线。

## 整体概览 {#high-level-overview}

Avalonia 采用分层设计，每一层只依赖它下面的层：

| 层 | 职责 |
|---|---|
| **Controls** | 面向用户的控件（Button、TextBox、DataGrid）、数据绑定、模板、样式 |
| **Layout** | 测量/排列系统、面板逻辑、滚动 |
| **Visual** | 视觉树、渲染变换、不透明度、裁剪 |
| **Rendering** | 绘图图元（画刷、几何图形、文本）、场景图、合成 |
| **Platform Abstraction** | 窗口管理、输入、剪贴板、文件对话框、GPU 上下文 |
| **Platform Backends** | Win32, Cocoa, X11/Wayland, Android, iOS, Browser (WASM) |

应用代码主要和控件层、布局层打交道；渲染层与平台层则在幕后运转。

## 渲染管线 {#the-rendering-pipeline}

Avalonia 采用保留模式（retained-mode）渲染。控件并不直接把自己画出来，而是通过模板声明自身的视觉结构，再由框架构建出一张场景图，逐帧渲染。

### 一帧的生命周期 {#frame-lifecycle}

每一帧按以下顺序推进：

1. **输入处理**：平台后端投递指针、键盘和触摸事件，事件沿视觉树冒泡和隧道传播。
2. **属性变更**：输入处理程序和定时器触发属性变更，这些变更可能令布局或渲染失效。
3. **布局阶段**：需要重新测量的控件依次走 `Measure` 和 `Arrange`。布局从根节点开始向下遍历，为每个控件确定最终的尺寸与位置。
4. **渲染阶段**：视觉内容已失效的控件通过 `Render(DrawingContext)` 重建自己那部分场景图，框架再把新旧场景做差分比对。
5. **合成阶段**：合成器接过更新后的场景图，向 GPU 后端（Skia 或平台原生合成器）提交绘制调用。

### 布局：测量与排列 {#layout-measure-and-arrange}

Avalonia 沿用了与 WPF、UWP 相同的两阶段布局模型：

- **测量（Measure）**：父级告诉每个子元素可用空间有多大，子元素回报自己期望的尺寸。
- **排列（Arrange）**：父级在可用区域内为每个子元素敲定最终的位置和尺寸。

布局失效会沿树向上传播。当控件的 `Width`、`Margin` 或内容发生变化时，它会调用 `InvalidateMeasure()`，把自己及全部祖先标记为需要重新布局。框架会把这些失效请求合并，因此每帧只跑一次布局。

```csharp
// Custom panel: override MeasureOverride and ArrangeOverride
protected override Size MeasureOverride(Size availableSize)
{
    foreach (var child in Children)
    {
        child.Measure(availableSize);
    }

    return new Size(200, 200); // desired size
}

protected override Size ArrangeOverride(Size finalSize)
{
    foreach (var child in Children)
    {
        child.Arrange(new Rect(child.DesiredSize));
    }

    return finalSize;
}
```

### 场景图与合成 {#scene-graph-and-composition}

布局之后，渲染阶段会构建一张场景图：一棵由绘制指令（填充矩形、绘制文本、应用裁剪等）构成的轻量树。合成器每帧遍历这张图，通过当前的渲染后端向 GPU 发出绘制调用。

Avalonia 支持两种合成模式：

- **软件合成**：用 Skia 在 CPU 上把场景图光栅化，再贴到平台窗口上。这是多数平台的默认方式，哪儿都能跑。
- **GPU 合成**：在平台支持的情况下（例如 Windows 上的 Direct3D、macOS 上的 Metal、Linux 上的 OpenGL/Vulkan），Avalonia 可以直接向 GPU 发出绘制调用，复杂场景下性能更好。

## 平台抽象 {#platform-abstraction}

Avalonia 把所有平台相关代码都藏在接口之后，关键抽象有：

| 接口 | 用途 |
|---|---|
| `IWindowImpl` | 窗口的创建、尺寸、定位与原生边框装饰 |
| `ITopLevelImpl` | 渲染表面、输入投递、缩放 |
| `IClipboard` | 剪贴板读写 |
| `IStorageProvider` | 文件与文件夹选取对话框 |
| `ILauncher` | 用系统默认程序打开 URI 和文件 |
| `IInsetsManager` | 安全区域内边距（刘海、状态栏） |
| `IPlatformSettings` | 主题探测、强调色、动画偏好设置 |
| `IRenderTarget` | 用于渲染的 GPU 表面 |

每个平台后端（Win32、Cocoa、X11、Wayland、Android、iOS、Browser）各自实现这些接口。应用在启动时通过 `AppBuilder` 选定后端：

```csharp
AppBuilder.Configure<App>()
    .UsePlatformDetect() // auto-select based on OS
    .StartWithClassicDesktopLifetime(args);
```

`UsePlatformDetect()` 会自动挑选正确的后端。你也可以为测试或嵌入式场景指定某个后端，或者在 Linux 上主动启用实验性的 [Wayland 后端](/docs/platform-specific-guides/linux#wayland)。

## 属性系统 {#the-property-system}

Avalonia 有一套自己的属性系统，支撑样式、动画、数据绑定和值继承。属性分三类：

- **StyledProperty**：默认的属性类型，支持样式、动画、值继承和数据绑定。控件的属性大多属于这一类。
- **DirectProperty**：由 CLR 字段支撑的轻量属性，比 StyledProperty 快，但不支持样式和动画。适合变化频繁的属性（例如 `TextBox.Text`）。
- **AttachedProperty**：注册到另一个宿主类型上的 StyledProperty，常用于 `Grid.Row`、`DockPanel.Dock` 这类布局属性。

属性值通过一套优先级机制解析，完整的优先级顺序见[属性值优先级](/docs/properties/value-precedence)。

## 样式系统 {#the-styling-system}

Avalonia 用的是借鉴 CSS 的样式系统，而不是 WPF 那种基于资源查找的触发器。样式通过选择器声明，按类型、样式类、伪类和名称匹配控件：

```xml
<Style Selector="Button.primary:pointerover">
    <Setter Property="Background" Value="#818CF8" />
</Style>
```

样式系统按声明顺序求值选择器。多条样式同时命中时，同一属性以靠后的声明为准 —— 和 CSS 的优先级有几分相似，不过 Avalonia 用的是更简单的顺序模型。

控件主题是一类特殊的样式，为某个控件类型提供默认模板和默认属性值。主题通过 `Theme` 属性解析，因此可以按单个控件或按子树切换主题。

## 视觉树与逻辑树 {#the-visual-and-logical-trees}

每个 Avalonia 界面都由两棵并行的树来表示：

- **逻辑树**：在 XAML 或代码中声明出来的控件树。DataContext、资源和属性继承都沿这棵树流动。
- **视觉树**：实际渲染出来的元素树，包含模板展开后的内容。命中测试、渲染和事件路由走的是这棵树。

详细内容请见[视觉树与逻辑树](/docs/fundamentals/visual-and-logical-trees)。

## 线程模型 {#threading-model}

Avalonia 的 UI 操作是单线程的：所有属性变更、布局和渲染都在 UI 线程上进行。后台任务必须通过 `Dispatcher` 把结果调度回 UI 线程：

```csharp
var data = await Task.Run(() => LoadData());
// Back on UI thread automatically with async/await
Items = new ObservableCollection<Item>(data);
```

完整的线程模型请见[线程](/docs/app-development/threading)。

## 另请参阅 {#see-also}

- [跨平台架构](/docs/fundamentals/cross-platform-architecture)：解决方案结构与平台相关代码的组织方式。
- [视觉树与逻辑树](/docs/fundamentals/visual-and-logical-trees)：两棵树各自的作用，以及什么时候该用哪一棵。
- [属性系统](/docs/properties)：StyledProperty、DirectProperty 与 AttachedProperty。
- [线程](/docs/app-development/threading)：Dispatcher 与异步模式。
- [性能优化](/docs/app-development/performance)：布局、渲染和绑定方面的性能建议。
