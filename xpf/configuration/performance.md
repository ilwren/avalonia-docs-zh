---
id: performance
title: Performance Optimization
---

## 用 ReadyToRun 缩短启动时间 {#reducing-startup-time-with-readytorun}

ReadyToRun（R2R）编译会把程序集预先编译成本机代码，XPF 应用从中受益颇多。微软发布的 WPF 库通常已做过 R2R 预编译，而 XPF 的库默认没有。

在你的 `.csproj` 中启用 ReadyToRun：

```xml
<PropertyGroup>
    <PublishReadyToRun>true</PublishReadyToRun>
</PropertyGroup>
```

然后带上运行时标识符发布：

```bash
dotnet publish -r linux-x64 -c Release
```

这能显著缩短应用的启动时间，在 Linux 嵌入式设备上尤其明显。

:::note
在 Linux 上，ReadyToRun 可能改变原生 `.so` 库的解析方式。细节请见 [Linux：原生库解析](/xpf/platforms/linux#native-library-resolution-with-readytorun)。
:::

## 渲染性能 {#rendering-performance}

### 配置 Skia 与合成选项 {#configuring-skia-and-composition-options}

XPF 以 Skia 作为渲染引擎。你可以在[自定义初始化](/xpf/configuration/customizing-initialization)中通过 `SkiaOptions` 和 `CompositionOptions` 调优渲染性能：

```csharp
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Skia;
using AvaloniaUI.Xpf;

AppBuilder.Configure<AvaloniaUI.Xpf.Helpers.DefaultXpfAvaloniaApplication>()
    .UsePlatformDetect()
    .With(new SkiaOptions
    {
        MaxGpuResourceSizeBytes = 512 * 1024 * 1024 // 512 MB GPU resource cache
    })
    .With(new CompositionOptions
    {
        UseRegionDirtyRectClipping = true
    })
    .WithAvaloniaXpf()
    .SetupWithLifetime(new ClassicDesktopStyleApplicationLifetime
    {
        ShutdownMode = ShutdownMode.OnExplicitShutdown
    });
```

- `MaxGpuResourceSizeBytes`：增大 GPU 纹理缓存，对于视觉元素众多的应用可减少重复上传。
- `UseRegionDirtyRectClipping`：只渲染屏幕上发生变化的区域，局部更新时性能更好。

### 模糊效果 {#blur-effects}

模糊效果（`BlurEffect`、带模糊的 `DropShadowEffect`）在 Skia 中相当吃算力。复杂界面一旦开启模糊，帧率可能从 60fps 掉到 30fps 甚至更低。若你在意渲染性能：

- 能去掉模糊就去掉，去不掉也尽量把模糊半径调小
- 考虑用纯色背景代替亚克力/模糊效果
- 尽早在你的目标硬件上实测

## 动态加载 XAML {#dynamic-xaml-loading}

`XamlReader.Load` 会在运行时解析并实例化 XAML。面对大型 XAML 文档，它可能把 UI 线程阻塞好几秒。这是与 WPF 共有的根本性限制。

改善动态 XAML 性能的几种思路：

- **把 XAML 预编译进程序集**：若 XAML 内容在构建期就已确定，可以把它编译进一个单独的程序集，运行时再动态加载。编译后的 XAML（BAML）比直接解析原始 XAML 快得多。
- **把大 XAML 拆小**：把大型 XAML 文档切成若干小块，分批加载。
- **在后台线程加载**：在后台线程上解析 XAML 字符串，再到 UI 线程上实例化出对象树。

:::note
BAML（编译后的 XAML）加载性能最好，但没有受支持的公开 API 可用来生成独立的 BAML 文件，所以还是把 XAML 编译进程序集吧。
:::

## 嵌入高性能内容 {#embedding-high-performance-content}

对于性能吃紧的渲染场景（比如实时仪表、音频可视化或 3D 内容），不妨用 [AvaloniaHost](/xpf/interop/embedding-avalonia-in-xpf) 在 XPF 应用中嵌入 Avalonia 控件。Avalonia 的 `CompositionCustomVisuals` API 允许直接在合成线程上渲染，彻底绕开 WPF 的 dispatcher。

OpenGL 内容可参考 [OpenGL 示例](https://github.com/AvaloniaUI/Avalonia-XPF-Samples/tree/master/src/OpenGLSample)，它演示了如何用 `ICompositionGpuInterop` 在 XPF 窗口中嵌入 OpenGL 渲染。
