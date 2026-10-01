---
id: main-window
title: 主窗口
description: 在桌面、移动和浏览器平台上设置并访问主窗口或主视图。
doc-type: explanation
video:
  src: https://youtu.be/5sSJF230A64
  title: 详解 Avalonia 主窗口 —— 关闭模式与应用生命周期
---

主窗口，就是在 `App.axaml.cs` 文件的 `OnFrameworkInitializationCompleted` 方法中赋给 `ApplicationLifetime.MainWindow` 的那个窗口：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktopLifetime)
    {
        desktopLifetime.MainWindow = new MainWindow();
    }
}
```

随时可以把 `Application.Current.ApplicationLifetime` 转换成 `IClassicDesktopStyleApplicationLifetime` 来取回它。

请注意，使用静态全局变量、在应用的任意位置访问 `MainWindow`，是有风险的，有时还会拖累用户体验。所有与顶层（窗口）相关的 API，都应该从最贴近的那个顶层去调用 —— 通常是最近激活的那一个。这样才能确保对话框不会从错误的窗口弹出来。

:::caution
在 Avalonia 中，移动平台和浏览器平台没有 `Window` 的概念。iOS 和浏览器上请通过 `ISingleViewApplicationLifetime` 设置 `MainView` 控件；Android 上则要改用 `IActivityApplicationLifetime` 来设置 `MainViewFactory`，因为 Android 可能会多次重建主 Activity。详见[应用程序生命周期](/docs/fundamentals/application-lifetimes)。
:::

## 另请参阅 {#see-also}

- [顶层](/docs/fundamentals/top-level)
- [应用程序生命周期](/docs/fundamentals/application-lifetimes)
