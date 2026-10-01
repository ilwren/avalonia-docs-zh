---
id: embedded-linux
title: Embedded Linux
description: 借助 framebuffer 或 DRM/KMS 在嵌入式 Linux 设备上运行 Avalonia，并支持显示缩放、屏幕旋转与触摸输入。
doc-type: how-to
---

Avalonia 支持在没有桌面环境的嵌入式 Linux 设备上运行，比如树莓派这类单板计算机、工业面板、自助终端和 POS 机。这种场合下 Avalonia 不经由 X11 之类的窗口系统，而是通过 Linux framebuffer 或 Direct Rendering Manager（DRM）直接向显示硬件渲染。

## 显示输出：framebuffer 还是 DRM {#display-output-framebuffer-vs-drm}

在桌面 Linux 系统上，应用绘制到由合成器（X11 或 Wayland）管理的窗口中。嵌入式设备通常没有合成器，应用得通过两种内核接口之一，把像素直接写进显示硬件。

### Linux framebuffer（`/dev/fb0`） {#linux-framebuffer-devfb0}

Linux framebuffer（fbdev）是两者中较老也较简单的那个接口。它把显示设备暴露成一块可供写入的平坦内存区域：内核把显存映射到用户空间，往这块内存里写什么，屏幕上就显示什么。

**运作原理：**
1. 内核驱动把 GPU 的扫描输出缓冲区映射到 `/dev/fb0`。
2. 应用打开该设备、调用 `mmap()`，拿到指向像素数据的指针。
3. 往那块内存里写 RGB 值，画面会在下一次刷新时更新。

**Advantages:**
- 编程模型简单。
- 几乎所有 Linux 系统都能用，连很老的内核也不例外。
- 不需要 GPU 加速。

**局限：**
- 没有硬件加速渲染（用不了 OpenGL/Vulkan）。
- 默认是单缓冲，更新画面时可能出现肉眼可见的撕裂。
- 同一时刻只能有一个应用使用 framebuffer。
- fbdev 子系统在 Linux 内核中已进入维护模式，新硬件的驱动都转向 DRM 了。

### Direct Rendering Manager (DRM/KMS)

DRM 是 Linux 内核中管理 GPU 和显示控制器的现代子系统。其中的内核模式设置（KMS）组件负责显示配置：分辨率、刷新率，以及当前正在扫描输出的是哪个缓冲区。

**运作原理：**
1. 应用打开 `/dev/dri/card0`（或别的 card 设备）。
2. 它通过 KMS API 查询可用的连接器（HDMI、DSI 等）、编码器和 CRTC。
3. 它分配 GPU 缓冲区（称为 GEM 对象），并建立一个指向该内存的 framebuffer 对象。
4. 它调用 `drmModeSetCrtc` 或 `drmModePageFlip` 把缓冲区显示出来。
5. 双缓冲是内建的：应用往后缓冲区绘制的同时，前缓冲区正在显示，画完再翻页。

**Advantages:**
- 可经由 OpenGL ES 或 Vulkan 做硬件加速渲染（前提是 GPU 支持）。
- 通过页面翻转实现无撕裂显示。
- 支持多平面，可做叠加合成。
- 在 Linux 内核中持续活跃开发，所有现代 SoC 都有驱动。

**局限：**
- API 比 framebuffer 复杂。
- 需要支持 KMS 的 GPU 驱动（所有现代 ARM SoC 都支持，但某些很旧或冷门的硬件可能没有）。

### 该选哪个 {#which-to-choose}

| 考量因素 | Framebuffer | DRM |
|---|---|---|
| 硬件加速 | No | 支持（前提是 GPU 支持） |
| Tearing | Possible | 靠页面翻转做到无撕裂 |
| 内核支持情况 | 维护模式 | 活跃开发中 |
| 配置复杂度 | Lower | Moderate |
| 是否推荐用于新项目 | No | Yes |

**新项目请用 DRM。**framebuffer 接口虽然还能用，但已被视为遗留方案。DRM 性能更好、渲染无撕裂，也是 Linux 内核发展的方向。只有当你的硬件没有支持 KMS 的 GPU 驱动时，才退回去用 framebuffer。

## 单视图应用生命周期 {#the-single-view-application-lifetime}

桌面版 Avalonia 应用使用会创建窗口的 `IClassicDesktopStyleApplicationLifetime`。嵌入式 Linux 上没有窗口管理器，所以 Avalonia 改用 `ISingleViewApplicationLifetime`。这种生命周期会给你一个铺满整个显示区域的根视图。

你的 `App.axaml.cs` 必须同时照顾这两种生命周期，这样应用既能在桌面上跑（便于开发），也能在嵌入式目标设备上跑：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        desktop.MainWindow = new MainWindow();
    else if (ApplicationLifetime is ISingleViewApplicationLifetime singleView)
        singleView.MainView = new MainSingleView();

    base.OnFrameworkInitializationCompleted();
}
```

一个常见套路是：把真正的界面写成一个 `MainView` UserControl，然后让 `MainWindow`（桌面）和 `MainSingleView`（嵌入式）都来承载它。这样你就能在工作站上开发调试，再把同一套界面部署到目标设备。

## 启用 DRM 输出 {#enabling-drm-output}

把 `Avalonia.LinuxFramebuffer` 包添加到你的项目：

```bash
dotnet add package Avalonia.LinuxFramebuffer
```

在 `Program.cs` 中检查是否有 `--drm` 命令行参数，据此启动相应的生命周期：

```csharp
public static int Main(string[] args)
{
    var builder = BuildAvaloniaApp();
    if (args.Contains("--drm"))
    {
        SilenceConsole();
        // Avalonia auto-detects the output card.
        // To specify one explicitly: card: "/dev/dri/card1"
        return builder.StartLinuxDrm(args, card: null, options: new DrmOutputOptions
        {
            Scaling = 1.0,
        });
    }

    return builder.StartWithClassicDesktopLifetime(args);
}

private static void SilenceConsole()
{
    new Thread(() =>
    {
        Console.CursorVisible = false;
        while (true)
            Console.ReadKey(true);
    })
    { IsBackground = true }.Start();
}
```

`SilenceConsole` 方法会接管控制台输入并隐藏光标。不这么做的话，闪烁的文本光标会压在你应用的画面上。

## 显示缩放 {#display-scaling}

`DrmOutputOptions` 上的 `Scaling` 属性控制 DPI 缩放系数，支持小数。举例来说，在 1920x1080 的屏幕上设 `Scaling = 1.5`，控件会显得更大，就像渲染到一块 1280x720 的逻辑表面上一样。

```csharp
return builder.StartLinuxDrm(args, card: null, options: new DrmOutputOptions
{
    Scaling = 1.5,
});
```

要想画面最锐利，请挑一个能把物理分辨率整除成整数的缩放值。对 1920x1080 的屏幕来说，`1.25`（1536x864）和 `1.5`（1280x720）就很合适。算不出整数的值（比如 `1.3`）照样能用，只是边缘会稍欠清晰，因为 `UseLayoutRounding` 无法在所有边界上精确对齐。

## 屏幕方向 {#screen-orientation}

不少嵌入式显示屏是竖装或旋转安装的。若你的 Linux 显示驱动不支持硬件旋转，Avalonia 可以借助 `DrmOutputOptions` 上的 `Orientation` 属性，用软件方式旋转渲染结果。

```csharp
return builder.StartLinuxDrm(args, card: null, options: new DrmOutputOptions
{
    Scaling = 1.0,
    Orientation = SurfaceOrientation.Rotation90,
});
```

可选的取值有：

| 值 | 旋转角度 |
|---|---|
| `SurfaceOrientation.Rotation0` | 不旋转（默认） |
| `SurfaceOrientation.Rotation90` | 顺时针 90 度 |
| `SurfaceOrientation.Rotation180` | 180 degrees |
| `SurfaceOrientation.Rotation270` | 顺时针 270 度 |

触摸输入的坐标会自动按所配置的方向作相应调整。旋转在启动时设定，应用运行期间无法更改。

:::note
旋转借助一块离屏 framebuffer 和一个 OpenGL 着色器来变换画面。用 `Rotation0` 时没有任何性能开销。
:::

## 渲染性能 {#rendering-performance}

嵌入式设备往往靠 framebuffer 做软件渲染，或者用着比桌面弱得多的 GPU。在这类硬件上，每一帧的开销主要花在涂像素上，因此缩小 Avalonia 的重绘面积，收益会比在桌面 GPU 上明显得多。

### 启用区域脏矩形裁剪 {#enabling-region-dirty-rect-clipping}

[`CompositionOptions.UseRegionDirtyRectClipping`](/api/avalonia/rendering/composition/compositionoptions) 会借助区域来更精确地跟踪脏矩形，从而缩小需要重绘的面积，代价是要花些 CPU 去计算裁剪区。

从 Avalonia 12.1 起，该选项**默认关闭**，因为在高性能 GPU 上，多出来的裁剪开销会盖过省下的过度绘制。嵌入式 Linux 正是它可能派上用场的场景之一：GPU 较弱时，少涂的那些像素兴许比裁剪开销更划算。

要启用区域裁剪，必须在启动时于 `CompositionOptions` 中显式设置 `UseRegionDirtyRectClipping = true`。

```csharp
AppBuilder.Configure<App>()
    .UsePlatformDetect()
    .With(new CompositionOptions
    {
        UseRegionDirtyRectClipping = true
    });
```

启用区域裁剪后，`MaxDirtyRects` 决定每帧最多跟踪多少个脏矩形。更多信息请见性能优化指南中的[区域脏矩形裁剪](/docs/app-development/performance#region-dirty-rect-clipping)。

## 验证 DRM 是否配好了 {#verifying-your-drm-setup}

在跑 Avalonia 应用之前，你可以用 `kmscube` 验证 DRM 是否正常：

```bash
sudo apt-get install kmscube
sudo kmscube
```

若屏幕上出现一个旋转的立方体，说明 DRM 工作正常，Avalonia 也就能渲染了。

## 触摸输入 {#touch-input}

嵌入式设备常把触摸屏当作主要输入方式。Avalonia 通过 `libinput` 读取触摸事件，它就在前面列出的必需库里。经由 DRM 运行时，触摸输入自动生效。

若应用需要屏幕键盘（自助终端、POS 系统，或任何没有物理键盘的设备），请看[虚拟键盘](/controls/input/text-input/virtualkeyboard)指南。

## 另请参阅 {#see-also}

- [在树莓派上运行](/docs/platform-specific-guides/embedded-linux/raspberry-pi)——手把手的硬件教程
- [虚拟键盘](/controls/input/text-input/virtualkeyboard)——屏幕键盘支持
- [部署到嵌入式 Linux](/docs/deployment/embedded-linux)
- [桌面 Linux](/docs/platform-specific-guides/linux)——X11 与 Wayland 环境
- [性能优化](/docs/app-development/performance)——渲染、布局与绑定的调优
