---
id: dotnet
title: 平台专属的 .NET
---

## 概述 {#overview}

.NET 中的条件编译可以按特定条件决定某段代码参与编译还是被略过。当代码需要在不同平台或不同开发环境下表现各异时，这一手尤其有用。

这些办法都不是 Avalonia 独有的，任何类型的项目都能用。

## 运行时判断 {#runtime-conditions}

.NET 6 及更高版本提供了一组在运行时获取操作系统的 API —— [OperatingSystem](https://learn.microsoft.com/en-us/dotnet/api/system.operatingsystem)。

这个类常用的静态方法有：
| 方法 | 说明 |
| --- | --- |
| IsWindows()	 | 指示当前应用是否运行在 Windows 上。 |
| IsLinux() |	指示当前应用是否运行在 Linux 上。 |
| IsMacOS() |	指示当前应用是否运行在 macOS 上。 |
| IsAndroid() |	指示当前应用是否运行在 Android 上。 |
| IsIOS() |	指示当前应用是否运行在 iOS 或 MacCatalyst 上。 |
| IsBrowser() |	指示当前应用是否以 WASM 形式运行在浏览器中。 |
| IsOSPlatform(String) | 	指示当前应用是否运行在指定平台上。 |

这些方法不要求改动项目结构，随处可用。
它们的短处在于无法在编译期把平台专属 API 隔离开来——否则就得在公共程序集里引用平台专属的依赖。

场景较简单、或者你想保持项目结构清爽时，推荐用这种办法。后一种情形下， 

:::note
对 Linux 来说，这是写条件 .NET 代码的唯一办法，因为 .NET 并没有专门的 Linux 目标框架。
:::

## 条件编译 {#conditional-compilation}

C# 本身支持用 `#if`、`#elif`、`#else`、`#endif` 做条件编译 —— 见 [C# 预处理器指令](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/preprocessor-directives#conditional-compilation)。

`DEBUG` 这个编译期常量大家都熟，但它对写平台专属代码其实帮不上什么忙。
视项目配置而定，C# 编译器可能会为项目中用到的每个[操作系统专属目标框架](https://learn.microsoft.com/en-us/dotnet/standard/frameworks#net-5-os-specific-tfms)额外定义一些常量：

|Target Framework | 常量 |
|----|----|
| net8.0 | - |
| net8.0-windows | WINDOWS |
| net8.0-macos | MACOS |
| net8.0-browser | BROWSER |
| net8.0-ios | IOS |
| net8.0-android | ANDROID |
从这张表可以看出两点：
1. 若项目没有用到任何操作系统专属的目标框架，这些常量一个都不会被定义
2. **没有 LINUX 常量**，因为目前还没有 `net8.0-linux` 目标框架。注意，这在未来的 .NET 版本中可能会变。
3. 另外，`net8.0-browser` 要到 .NET 8 SDK 才有；其余目标框架在 .NET 6 及以上均受支持。

:::note
如有需要，同样的思路也可用于为 .NET Framework 或 .NET Standard 项目编写特定代码。更多信息请看微软的[跨平台目标
](https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/cross-platform-targeting)文档。
:::

### 实例演示 {#practical-example}

假设我们想在 C# 代码里调用平台 API——可能是 Avalonia 的 API，也可能是 Xamarin 的，或者别的什么。
首先得在项目里声明预期的目标框架。为简单起见，我们在 `.csproj` 文件中设三个目标框架："net8.0"（默认）、"net8.0-ios" 和 "net8.0-android"：

```xml
<PropertyGroup>
    <TargetFrameworks>net8.0;net8.0-ios;net8.0-android</TargetFrameworks>
</PropertyGroup>
```

然后就可以写出这样一个方法：
```csharp
public enum DeviceOrientation
{
    Undefined,
    Landscape,
    Portrait
}

public static DeviceOrientation GetOrientation()
{
#if ANDROID
            IWindowManager windowManager = Android.App.Application.Context.GetSystemService(Context.WindowService).JavaCast<IWindowManager>();
            SurfaceOrientation orientation = windowManager.DefaultDisplay.Rotation;
            bool isLandscape = orientation == SurfaceOrientation.Rotation90 || orientation == SurfaceOrientation.Rotation270;
            return isLandscape ? DeviceOrientation.Landscape : DeviceOrientation.Portrait;
#elif IOS
            UIInterfaceOrientation orientation = UIApplication.SharedApplication.StatusBarOrientation;
            bool isPortrait = orientation == UIInterfaceOrientation.Portrait || orientation == UIInterfaceOrientation.PortraitUpsideDown;
            return isPortrait ? DeviceOrientation.Portrait : DeviceOrientation.Landscape;
#else
            return DeviceOrientation.Undefined;
#endif
}
```

:::note
本示例代码引自微软文档：https://learn.microsoft.com/en-us/dotnet/maui/platform-integration/invoke-platform-code?view=net-maui-8.0#conditional-compilation
:::


## 平台专属项目 {#platform-specific-projects}

与上一种办法类似，你也可以为每个平台各建一个引导项目，再把主要逻辑和布局放在共享项目里。
例如，默认的 Avalonia.Xplat 模板会生成包含下列项目的解决方案：

| 项目 | Target Framework |
| --- | --- |
| Project.Shared | net8.0 |
| Project.Desktop | net8.0 |
| Project.Android | net8.0-android |
| Project.iOS | net8.0-ios |
| Project.Browser | net8.0-browser |

Desktop 项目把 Windows、macOS 和 Linux 合在一起，移动端和浏览器平台则各有各的项目。
这是 Avalonia 项目的默认做法。若有需要，开发者也可以把 Desktop 项目继续拆开。
不过要记住，.NET SDK 至今还没有面向 Linux 的目标框架，所以那部分仍得用通用的 `net8.0` 目标框架。

通常，一旦需要平台专属代码，大家会在共享项目里定义一个新接口，再为各平台分别实现。
把前面的示例照此改写，大致是这样：
```csharp title='Project.Shared IDeviceOrientation.cs'
public interface IDeviceOrientation
{
    DeviceOrientation GetOrientation();
}
```

```csharp title='Project.Android AndroidDeviceOrientation.cs'
public class AndroidDeviceOrientation : IDeviceOrientation
{
    public DeviceOrientation GetOrientation()
    {
        IWindowManager windowManager = Android.App.Application.Context.GetSystemService(Context.WindowService).JavaCast<IWindowManager>();
        SurfaceOrientation orientation = windowManager.DefaultDisplay.Rotation;
        bool isLandscape = orientation == SurfaceOrientation.Rotation90 || orientation == SurfaceOrientation.Rotation270;
        return isLandscape ? DeviceOrientation.Landscape : DeviceOrientation.Portrait;
    }
}
```

```csharp title='Project.iOS iOSDeviceOrientation.cs'
public class iOSDeviceOrientation : IDeviceOrientation
{
    public DeviceOrientation GetOrientation()
    {
        UIInterfaceOrientation orientation = UIApplication.SharedApplication.StatusBarOrientation;
        bool isPortrait = orientation == UIInterfaceOrientation.Portrait || orientation == UIInterfaceOrientation.PortraitUpsideDown;
        return isPortrait ? DeviceOrientation.Portrait : DeviceOrientation.Landscape;
    }
}
```

之后，用你中意的依赖注入库，或者借助一个静态注册表属性，把各个实现注册进去即可。

## 另请参阅 {#see-also}

- [平台相关的 XAML](/docs/platform-specific-guides/xaml)
- [在 Android 上部署](/docs/deployment/android)
- [Deploying on iOS](/docs/deployment/ios)