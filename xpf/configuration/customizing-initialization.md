---
id: customizing-initialization
title: 定制初始化
description: 如何在 XPF 应用中关掉自动初始化，从而拿到并定制 Avalonia 的 AppBuilder API。
---

Avalonia 提供了 [`AppBuilder`](/docs/fundamentals/application-lifetimes) API，可用来定制框架的方方面面。 

由于 XPF 构建在 Avalonia 之上，在 XPF 应用里能用上这套 API 往往很有价值。

## 第 1 步：关掉 XPF 的自动初始化 {#step-1-disable-automatic-xpf-initialization}

在项目文件中把 `DisableAutomaticXpfInit` 属性设为 `true`：

```xml
<PropertyGroup>
  <DisableAutomaticXpfInit>true</DisableAutomaticXpfInit>
</PropertyGroup>
```

## 第 2 步：添加主入口点 {#step-2-add-a-main-entry-point}

添加一个 `Program.cs` 文件，其中含有 `Main` 入口点：

```csharp
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using AvaloniaUI.Xpf;

namespace MyXpfApp;

internal class Program
{
    public static void Main(string[] args)
    {
        AppBuilder.Configure<AvaloniaUI.Xpf.Helpers.DefaultXpfAvaloniaApplication>()
            .UsePlatformDetect()
            .WithAvaloniaXpf()
            .SetupWithLifetime(new ClassicDesktopStyleApplicationLifetime
            { 
                ShutdownMode = ShutdownMode.OnExplicitShutdown 
            });

        App.Main();
    }
}
```

:::tip
请把上例中的命名空间改成你自己应用的命名空间。
:::

上例中的 `App` 就是你在 `App.xaml.cs` 中定义的 XPF `Application` 类。

## 第 3 步：设置 `StartupObject` {#step-3-set-the-startupobject}

在 `.csproj` 中加入下面的内容，让项目改用新的 `Main` 方法：

```xml
 <PropertyGroup>
     <StartupObject>MyXpfApp.Program</StartupObject>
 </PropertyGroup>
```

:::tip
请把上例中的命名空间改成 `Program.cs` 里定义的那个。
:::

## AssemblyLoadContext (ALC) Support

若你的应用用了自定义 .NET 宿主，或者插件架构中存在多个独立的 `AssemblyLoadContext` 实例，请在 `.csproj` 中加入下面的内容以启用 ALC 支持：

```xml
<ItemGroup>
    <RuntimeHostConfigurationOption Include="AvaloniaUI.Xpf.EnableAlcSupport" Value="true" />
</ItemGroup>
```

这样可以避免同一个程序集被加载进多个 ALC 而引发的 `VerificationException` 错误。下列情形下你需要这项设置：

- 你的应用用了插件机制，会把程序集加载进彼此隔离的 ALC
- 你把 XPF 托管在另一个使用自定义程序集加载逻辑的应用框架里
- XPF 初始化期间出现关于类型参数约束的报错

## 自定义程序集加载 {#custom-assembly-loading}

若你有一套自定义的托管程序集加载机制，可能会发现用 `AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable` 函数会让应用卡死。遇到这种情况，不妨改用 `AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AddLibrary` 延后添加程序集，像这样：

```csharp
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using AvaloniaUI.Xpf;
using AvaloniaUI.Xpf.WinApiShim;

namespace MyXpfApp;

internal class Program
{
    public void CalledFromYourCustomAssemblyLoading(Assembly targetAssembly)
    {
        // This call will add the assembly to the list of assemblies that will 
        // be intercepted with XPF's Win32 Shimming system.
        WinApiShimSetup.AddLibrary(targetAssembly);
    }
}
```

## dispatcher 的限制 {#dispatcher-constraints}

XPF 在所有平台上都只支持单个 UI dispatcher。在 macOS 上这是操作系统强制的（只允许一个 UI 线程）；在 Windows 和 Linux 上虽有有限的多 dispatcher 支持，但并不推荐。

若你的 WPF 应用会在其他线程上创建窗口（比如启动画面或进度对话框），请把这些写法改造成统一走主 dispatcher：

```csharp
// Instead of creating a new thread for a splash screen:
Dispatcher.CurrentDispatcher.BeginInvoke(DispatcherPriority.Background, () =>
{
    var splash = new SplashWindow();
    splash.Show();
});
```

更多细节请见[尚未支持的特性：多 UI 线程](/xpf/version-info/missing-features)。

## 可选：定义自定义的 Avalonia 应用类 {#optional-define-a-custom-avalonia-application}

某些情况下你可能想用一个自定义的 Avalonia `Application` 类，典型场景包括：

- 提供应用级的 Avalonia 样式和资源
- 提供应用的 `NativeMenu`

为此，先为你的应用类添加 `.cs` 和 `.axaml` 文件：

```csharp title="MyAvaloniaApp.axaml.cs"
using Avalonia;
using Avalonia.Markup.Xaml;
using Avalonia.Styling;

namespace MyXpfApp;

public class MyAvaloniaApp : Application
{
    public MyAvaloniaApp()
    {
        RequestedThemeVariant = ThemeVariant.Light;
        AvaloniaXamlLoader.Load(this);
    }
}
```

```xml title="MyAvaloniaApp.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyXpfApp.MyAvaloniaApp">
  <Application.Styles>
    <SimpleTheme/>
  </Application.Styles>
</Application>
```

然后在第 2 步添加的 `AppBuilder` 配置中引用这个自定义 Application：

```csharp
// highlight-next-line
AppBuilder.Configure<MyAvaloniaApp>()
    .UsePlatformDetect()
    .WithAvaloniaXpf()
    .SetupWithLifetime(new ClassicDesktopStyleApplicationLifetime
    { 
        ShutdownMode = ShutdownMode.OnExplicitShutdown 
    });
```


