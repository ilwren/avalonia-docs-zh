---
id: cross-platform-architecture
title: 跨平台架构
description: 了解 Avalonia 如何在各平台之间共享代码，以及如何应对平台差异。
doc-type: explanation
video:
  src: https://youtu.be/-MTKwRgNSyI
  title: 深入 Avalonia 跨平台架构（Windows、Mac、Linux、iOS、Android）
---

Avalonia 用 Skia 自行绘制控件，而不是去包装各平台的原生控件。这意味着你的 AXAML 视图、视图模型和业务逻辑，在每个平台上跑出来的结果都完全一致。本文讲清楚：哪些东西可以共享、哪些需要分平台处理，以及该怎么选。

## Avalonia 的代码共享思路 {#avalonias-approach-to-code-sharing}

由于控件是 Avalonia 自己画的，Windows、macOS、Linux、iOS、Android 乃至浏览器上的外观和行为都保持一致。在一个典型的 Avalonia 应用中，下列内容是完全共享的：

- **视图**（AXAML 文件及其代码隐藏）
- **视图模型与业务逻辑**（普通的 C# 或 F# 类）
- **样式与主题**
- **平台服务**，例如[文件选择器](/docs/services/storage/storage-provider)、[剪贴板](/docs/services/clipboard)、[启动器](/docs/services/launcher)、[深色模式检测](/docs/services/platform-settings)和[安全区域处理](/docs/services/insets-manager)

偶尔需要写平台相关代码的，主要是这些方面：

- 硬件传感器（GPS、加速度计、陀螺仪）
- 推送通知
- 蓝牙、摄像头与生物识别
- 系统托盘等操作系统层面的外壳集成

对于 Avalonia 没有抽象的设备 API，[Microsoft.Maui.Essentials](https://www.nuget.org/packages/Microsoft.Maui.Essentials) 提供了一层通用封装，可在 .NET 8 及以上版本中与 Avalonia 配合使用。但要注意，Maui.Essentials 并不覆盖 Linux、浏览器，以及非 Catalyst 的 macOS 目标。

## 如何组织解决方案 {#structuring-your-solution}

标准的 Avalonia 跨平台模板会生成一组项目，其结构以最大化代码共享为目标：

| 项目 | 用途 |
|---|---|
| Core | 视图、视图模型、业务逻辑（所有平台共享） |
| Desktop | Windows、macOS 和 Linux 的入口 |
| Android | Android 的入口 |
| iOS | iOS、iPadOS 和 Mac Catalyst 的入口 |
| Browser | WebAssembly 的入口 |

你绝大部分代码都待在核心项目里，各平台项目只是引用核心项目的轻薄入口。完整演练见[搭建跨平台解决方案](/docs/app-development/cross-platform-solution-setup)。

## 处理平台差异 {#handling-platform-differences}

当你确实需要平台相关的行为时，Avalonia 和 .NET 给了四种办法，下面按由简到繁的顺序介绍。

### OnPlatform 与 OnFormFactor {#onplatform-and-onformfactor}

界面层面的微调，直接在 AXAML 中用 `OnPlatform` 或 `OnFormFactor` 标记扩展：

```xml
<TextBlock Text="{OnPlatform 'Welcome', iOS='Welcome (iOS)', Android='Welcome (Android)'}"/>
```

`OnPlatform` 针对具体的操作系统，`OnFormFactor` 则针对设备类别（如 Desktop 或 Mobile）。完整语法见[平台相关的 XAML](/docs/platform-specific-guides/xaml)。

### 运行时判断 {#runtime-detection}

C# 代码中要做简单分支，用 `OperatingSystem` 类：

```csharp
if (OperatingSystem.IsWindows())
{
    // Windows-specific logic
}
```

这种办法到哪儿都能用，也不必改动项目结构。完整 API 参考见[平台相关的 .NET](/docs/platform-specific-guides/dotnet)。

### 条件编译 {#conditional-compilation}

要调用平台专有 API 的代码，可以结合 C# 预处理指令和特定操作系统的目标框架：

```csharp
#if ANDROID
    var orientation = GetAndroidOrientation();
#elif IOS
    var orientation = GetiOSOrientation();
#else
    var orientation = DeviceOrientation.Undefined;
#endif
```

这要求你的项目做多目标编译（例如 `net8.0;net8.0-ios;net8.0-android`）。配置细节见[平台相关的 .NET](/docs/platform-specific-guides/dotnet)。

### 接口抽象 {#interface-abstraction}

对于复杂的平台功能，在共享项目中定义接口，再分平台各自实现：

```csharp
// In Core project
public interface IDeviceOrientation
{
    DeviceOrientation GetOrientation();
}

// In platform-specific project
public class AndroidDeviceOrientation : IDeviceOrientation
{
    public DeviceOrientation GetOrientation() { /* Android APIs */ }
}
```

把每个实现注册到依赖注入容器中，共享代码就能在不知道自己跑在哪个平台的情况下直接使用它。完整示例见[平台相关的 .NET](/docs/platform-specific-guides/dotnet)，依赖注入的配置见[依赖注入](/docs/app-development/dependency-injection)。

## 该选哪种办法 {#choosing-an-approach}

| 办法 | 适用场景 | 代价 |
|---|---|---|
| OnPlatform / OnFormFactor | 界面微调（间距、文案、控件） | 仅限 XAML |
| 运行时判断 | 简单的运行时分支 | 所有平台的代码都会打进每份二进制 |
| 条件编译 | 调用平台专有 API | 需要多目标编译 |
| 接口抽象 | 复杂的平台功能 | 文件变多，且需要依赖注入 |

先用能满足需求的最简单办法，确有必要时再换更灵活的。

## 另请参阅 {#see-also}

- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)
- [搭建跨平台解决方案](/docs/app-development/cross-platform-solution-setup)
- [平台相关的 .NET](/docs/platform-specific-guides/dotnet)
- [平台相关的 XAML](/docs/platform-specific-guides/xaml)
- [依赖注入](/docs/app-development/dependency-injection)
- [应用程序生命周期](/docs/fundamentals/application-lifetimes)
