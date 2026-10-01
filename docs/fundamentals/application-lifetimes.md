---
id: application-lifetimes
title: 应用程序生命周期
description: 为桌面、移动和浏览器平台选择并配置合适的应用程序生命周期模型。
doc-type: explanation
video:
  src: https://youtu.be/1_LLm3-YEt8
  title: Desktop, Mobile & Web All Start Your App Differently
---

各个平台并不是一个模子刻出来的。举例来说，你在 Windows Forms 或 WPF 里习以为常的那套生命周期管理，只在桌面类平台上成立。Avalonia 是跨平台框架，为了让应用具备可移植性，它提供了好几种生命周期模型；只要目标平台允许，你也完全可以手动接管全部流程。

## 生命周期是怎么运作的？ {#how-do-lifetimes-work}

桌面应用的初始化写法如下：

```csharp
class Program
{
  // This method is needed for IDE previewer infrastructure
  public static AppBuilder BuildAvaloniaApp() 
    => AppBuilder.Configure<App>().UsePlatformDetect();

  // The entry point. Things aren't ready yet, so at this point
  // you shouldn't use any Avalonia types or anything that expects
  // a SynchronizationContext to be ready
  public static int Main(string[] args) 
    => BuildAvaloniaApp().StartWithClassicDesktopLifetime(args);
}
```

主窗口则在 `Application` 类中创建：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    if (ApplicationLifetime
            is IClassicDesktopStyleApplicationLifetime desktop)
        desktop.MainWindow = new MainWindow();
    else if (ApplicationLifetime
            is IActivityApplicationLifetime activityLifetime)
        activityLifetime.MainViewFactory = () => new MainView();
    else if (ApplicationLifetime
            is ISingleViewApplicationLifetime singleView)
        singleView.MainView = new MainView();
    base.OnFrameworkInitializationCompleted();
}
```

该方法会在框架初始化完毕后被调用，此时 `ApplicationLifetime` 属性中就是选定的生命周期（如果有的话）。

:::info
如果应用运行在设计模式下（也就是 IDE 预览器进程中），`ApplicationLifetime` 为 null。
:::

## 生命周期接口 {#lifetime-interfaces}

Avalonia 提供了一组接口，让你按需挑选控制粒度。它们由 `BuildAvaloniaApp().Start[Something]` 系列方法提供。

### IControlledApplicationLifetime

提供者：

* `StartWithClassicDesktopLifetime`
* `StartLinuxFramebuffer`

可订阅 `Startup` 和 `Exit` 事件，并允许调用 `Shutdown` 方法显式关闭应用。这个接口把应用的退出流程交到了你手上。

### IClassicDesktopStyleApplicationLifetime

继承自：`IControlledApplicationLifetime`

提供者：

* `StartWithClassicDesktopLifetime`

让你像管理 Windows Forms 或 WPF 应用那样管理生命周期。该接口可以访问当前已打开的窗口列表、指定主窗口，并提供三种关闭模式：

* `OnLastWindowClose` —— 最后一个窗口关闭时退出应用
* `OnMainWindowClose` —— 主窗口关闭时退出应用（前提是已指定主窗口）。
* `OnExplicitShutdown` —— 关闭自动退出机制，需要你在代码中自行调用 `Shutdown` 方法。

### ISingleViewApplicationLifetime

提供者：

* `StartLinuxFramebuffer`
* iOS
* Web 平台（WebAssembly/WASM）

有些平台没有桌面主窗口的概念，屏幕上同一时刻只能呈现一个视图。对这类平台，生命周期改为让你设置和切换主视图类（`MainView`）。

:::info
在这类只有单一主视图的平台上实现导航栈，可以借助路由控件或导航框架。常见做法是自己维护一个视图模型栈，随用户导航压栈出栈，再配一个宿主控件自动展示对应的视图。
:::

### IActivityApplicationLifetime

提供者：

* Android

Android 可能在应用存续期间多次创建主 Activity（比如用户点开通知、或从别的应用切回来）。单个 `MainView` 实例无法跨 Activity 重建复用，因此 Android 改用工厂函数。

把 `MainViewFactory` 属性设为一个函数，每次 Activity 启动时由它创建新视图：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        desktop.MainWindow = new MainWindow();
    else if (ApplicationLifetime is IActivityApplicationLifetime activityLifetime)
        activityLifetime.MainViewFactory = () => new MainView();
    else if (ApplicationLifetime is ISingleViewApplicationLifetime singleView)
        singleView.MainView = new MainView();
    base.OnFrameworkInitializationCompleted();
}
```

每创建一个 Activity 实例，工厂就会被调用一次，产出一个自带独立状态的新视图。这样就避免了以往跨多次 Activity 启动复用同一视图实例所导致的崩溃。

## 手动管理生命周期 {#manual-lifetime-management}

有需要的话，你可以完全接管应用的生命周期管理。比如在桌面平台上，向 `BuildAvaloniaApp.Start` 方法传入一个 `AppMain` 委托，后续流程就全由你自己掌控：

```csharp
class Program
{
  // This method is needed for IDE previewer infrastructure
  public static AppBuilder BuildAvaloniaApp() 
    => AppBuilder.Configure<App>().UsePlatformDetect();

  // The entry point. Things aren't ready yet, so at this point
  // you shouldn't use any Avalonia types or anything that expects
  // a SynchronizationContext to be ready
  public static int Main(string[] args) 
    => BuildAvaloniaApp().Start(AppMain, args);

  // Application entry point. Avalonia is completely initialized.
  static void AppMain(Application app, string[] args)
  {
     // A cancellation token source that will be 
     // used to stop the main loop
     var cts = new CancellationTokenSource();
     
     // Do your startup code here
     new Window().Show();

     // Start the main loop
     app.Run(cts.Token);
  }
}
```

## 另请参阅 {#see-also}

- [主窗口](/docs/fundamentals/main-window)
- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)
