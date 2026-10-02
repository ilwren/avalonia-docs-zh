---
id: linux
title: Desktop Linux
description: Avalonia 在桌面 Linux 上如何运行，包括实验性的 Wayland 后端、WSL 2 配置，以及基于 AT-SPI2 的无障碍支持。
doc-type: overview
---

## Avalonia 在 Linux 上如何运行 {#how-avalonia-runs-on-linux}

Avalonia 在 Windows 上用 Win32 API，在 macOS 上用自家的原生 Objective-C++ 后端，而在 Linux 上默认面向 X11。只要能装 .NET SDK 且具备 X11、Wayland 或 framebuffer 能力的 Linux 发行版，基本都能跑 Avalonia 应用。

在 Wayland 桌面上，Avalonia 应用默认经由 XWayland 兼容层运行。从 Avalonia 12.1.0 起，你也可以主动启用原生的 [Wayland 后端](#wayland)。

## Wayland

[`Avalonia.Wayland`](https://www.nuget.org/packages/Avalonia.Wayland) 包提供了原生的 Wayland 后端。它直接用 Wayland 协议与合成器通信，不再绕道 XWayland。

该后端支持鼠标、触摸和键盘输入，也支持剪贴板和拖放。渲染经由 EGL 走 OpenGL 或 OpenGL ES，另可选用 [dma-buf 交换链](https://docs.kernel.org/userspace-api/dma-buf-alloc-exchange.html)路径。

:::caution
Wayland 后端尚属实验性质。`UsePlatformDetect()` 不会自动选中它，你必须显式启用。
:::

### 启用 Wayland 后端 {#enabling-the-wayland-backend}

1. 把 `Avalonia.Wayland` 包添加到你的项目：

   ```bash
   dotnet add package Avalonia.Wayland
   ```

2. 在 `Program.cs` 中对你的 [`AppBuilder`](/api/avalonia/appbuilder) 调用 `UseWayland()`：

   ```csharp
   public static AppBuilder BuildAvaloniaApp()
       => AppBuilder.Configure<App>()
           .UseWayland();
   ```

`UseWayland()` 总是初始化 Wayland 后端，且没有自动回退：在没有 Wayland 合成器的环境里，应用根本起不来。若应用还要跑在其他操作系统或 X11 会话上，请有条件地选择后端，比如检查 `WAYLAND_DISPLAY` 环境变量：

```csharp
public static AppBuilder BuildAvaloniaApp()
{
    var builder = AppBuilder.Configure<App>().UsePlatformDetect();

    if (OperatingSystem.IsLinux()
        && Environment.GetEnvironmentVariable("WAYLAND_DISPLAY") is not null)
    {
        builder = builder.UseWayland();
    }

    return builder;
}
```

### 配置项 {#configuration-options}

要配置该后端，请把一个 `WaylandPlatformOptions` 实例传给 `AppBuilder`：

```csharp
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UseWayland()
        .With(new WaylandPlatformOptions
        {
            UseDmabufSwapchain = true
        });
```

| 选项 | 默认值 | 说明 |
|---|---|---|
| `WlDisplayName` | `null` | 要连接的 Wayland 显示（例如 `wayland-0`）。为 `null` 时使用 `WAYLAND_DISPLAY` 环境变量。 |
| `EnableReconnects` | `true` | 连接断开时自动重连到合成器。 |
| `UseDmabufSwapchain` | `null` | GPU 渲染时使用基于 dma-buf 的交换链。为 `null` 时，由后端根据合成器和驱动的能力自行决定。 |
| `GlProfiles` | 从 OpenGL 4.0 一路降到 OpenGL ES 2.0 | 创建 GL 上下文时按优先顺序尝试的 OpenGL 与 OpenGL ES 版本。 |
| `UseGLibMainLoop` | `false` | 让 UI 线程跑在 GLib 主循环上。若你的应用在主线程上用到基于 GLib 的库，请启用它。 |

#### 高级选项 {#advanced-options}

以下选项面向合成器集成、后端测试等特殊场景，一般应用不必设置。

| 选项 | 默认值 | 说明 |
|---|---|---|
| `DisplayFd` | `null` | 一个已打开的 Wayland 显示套接字文件描述符，用它代替按名称连接显示。设置后 `WlDisplayName` 会被忽略，自动重连也会关闭，因为该文件描述符会被 libwayland 消费掉。 |
| `ForceDrawnDecorations` | `false` | 让窗口表现得像合成器从未宣称支持服务端装饰一样，于是始终使用客户端装饰。主要用于在 KWin 这类强制服务端装饰的合成器上做测试。标记为 `[Experimental]`：使用时需要抑制 `AVALONIA_WAYLAND_FORCE_CSD` 编译器诊断。 |
| `ExternalGLibMainLoopExceptionLogger` | `null` | 接收那些因发生在 Avalonia 掌控的运行循环帧之外、本会被忽略的异常。仅在启用 `UseGLibMainLoop` 时有效。 |

### 当前的局限 {#current-limitations}

Wayland 后端目前还缺少若干 KDE 专属集成：全局应用菜单、窗口图标和背后模糊效果。依赖这些特性的应用请继续使用 X11 后端。

## WSL 2（适用于 Linux 的 Windows 子系统） {#wsl-2-windows-subsystem-for-linux}

[WSL 2](https://learn.microsoft.com/en-us/windows/wsl/) 是 Windows 的一项功能，让你不必搭传统虚拟机、也不必双系统，就能在 Windows 上跑一套完整的 Linux 环境。对于想留在 Windows 工作流里构建和测试 Linux 应用的开发者，这很有用。

Avalonia 能在 WSL 2 发行版下运行，但有些在完整桌面发行版上通常预装好的库，这里需要手动安装：

```bash
sudo apt install libice6 libsm6 libfontconfig1
```

## 无障碍 {#accessibility}

在 Linux 上，Avalonia 通过 **AT-SPI2**（辅助技术服务提供方接口）协议把无障碍树暴露给辅助技术。这样 Orca 之类的屏幕阅读器就能发现并操作 Avalonia 控件，包括念出控件名称、朗读文本内容、跟踪焦点变化。

只要 D-Bus 会话总线可用且无障碍服务在运行，AT-SPI2 支持便会自动启用，你的应用里不需要任何额外配置。

### 用 Orca 测试 {#testing-with-orca}

[Orca](https://orca.gnome.org/) 是多数 GNOME 系发行版的默认屏幕阅读器。要验证应用的无障碍表现：

1. 若尚未安装，先装上 Orca：
   ```bash
   sudo apt install orca
   ```
2. 在桌面环境中启用无障碍。在 GNOME 上，打开**设置 > 辅助功能**并打开**屏幕阅读器**开关，或者从终端启动 Orca：
   ```bash
   orca &
   ```
3. 运行你的 Avalonia 应用。控件获得焦点时，Orca 应当会念出它们。

### 用 Accerciser 测试 {#testing-with-accerciser}

[Accerciser](https://gitlab.gnome.org/GNOME/accerciser) 是一款交互式的无障碍浏览工具，可显示 AT-SPI2 树。用它来核对控件暴露的角色、名称和状态是否正确很方便：

```bash
sudo apt install accerciser
accerciser &
```

一边操作正在运行的应用，一边在 Accerciser 中浏览这棵树，就能看清每个控件都暴露了哪些信息。

关于如何让应用具备无障碍能力的通用建议，请见[无障碍](/docs/app-development/accessibility)。

## 另请参阅 {#see-also}

- [受支持的平台](/docs/supported-platforms)——Linux 发行版的支持分级
- [部署到桌面 Linux](/docs/deployment/linux)
- [嵌入式 Linux](/docs/platform-specific-guides/embedded-linux)——framebuffer 与 DRM 场景
- [无障碍](/docs/app-development/accessibility)——自动化属性与自定义自动化 peer
