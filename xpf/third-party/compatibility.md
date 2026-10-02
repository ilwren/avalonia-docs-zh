---
id: compatibility
title: Library Compatibility
---

本页汇总了特定第三方库与 Avalonia XPF 的兼容性说明。关于如何启用 Win32 API shim（多数第三方库在非 Windows 平台上都要靠它），请见 [Win32 API shim](/xpf/third-party/win32-api-shims)。

## DevExpress

DevExpress 控件与 XPF 搭配的人不少。上手方法如下：

1. 在 `App` 构造函数或 `Program.Main` 中启用 Win32 API shim（DevExpress 控件必需）：
   ```csharp
   AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable();
   ```

   若你的应用还用了自带跨平台支持、不该被 shim 拦截的库，请借助筛选回调：
   ```csharp
   AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable(asm =>
   {
       var name = asm.GetName().Name?.ToLowerInvariant();
       // Skip assemblies that handle their own cross-platform support
       if (name is "sqlite" or "skiasharp")
           return true; // true = skip this assembly
       return false;
   });
   ```

2. 请确认 shim 启用在了对的地方。一个常见的疏漏是只在 macOS 启动器项目的 `Program.cs` 里启用了 shim，却漏了 `App.xaml.cs`（或者反过来）。shim 必须赶在任何第三方程序集调用 Win32 API 之前就启用。

3. 另外还要留意下列平台专属的限制：

   - **GDI+ 依赖**：某些 DevExpress 控件（DocumentPreviewControl、PdfViewerControl、XtraReport）依赖 `System.Drawing.Common`（GDI+），而它在非 Windows 平台上已废弃。能用的地方请启用 DevExpress 的 Skia 渲染引擎；具体控件对 Skia 的支持情况，请咨询 DevExpress 支持。
   - **LoadingDecorator**：带 `UseSplashScreen=true` 的 DevExpress `LoadingDecorator` 需要多个 UI 线程，而 macOS 不支持。可改用 `WaitIndicator`。
   - **Linux 依赖**：Linux 上的 DevExpress 控件需要 `libgdiplus`，请见 [Linux：其他依赖](/xpf/platforms/linux#other-dependencies)。

4. 正确的配置方式可参考官方的 DevExpress XPF 示例：[Avalonia-XPF-Samples/DevExpressApp](https://github.com/AvaloniaUI/Avalonia-XPF-Samples/tree/master/src/DevExpressApp)。

DevExpress 维护着一个演示应用，展示他们哪些控件已在 XPF 上验证过。

## CefSharp

`CefSharp.Wpf.NetCore` 是为 Windows 设计的，自带 Windows 原生的 Chromium 二进制文件，在 Linux 和 macOS 上用不了。

若 CefSharp 针对 `CursorInteropHelper.Create()` 抛出 `NotImplementedException`，请升级到 XPF 1.6.0 或更高版本，那里提供了回退方案。老版本上的变通办法是：从 `ChromiumWebBrowser` 派生并重写 `OnCursorChange`，把 CefSharp 的光标类型映射到 WPF 的 `Cursors`。

跨平台的浏览器替代方案请见[嵌入网页内容](/xpf/interop/web-content)。

## Dragablz

Dragablz 用到了一些 XPF shim 层尚未完整实现的 Win32 API（比如用于特定窗口外壳效果的 `DwmGetWindowAttribute`），在 Linux 上会抛出运行时异常。

推荐的做法是 fork 一份 Dragablz，把那些不受支持的平台 API 调用删掉或加上保护。这些调用通常集中在窗口外壳和标签页拖出的代码里，换成跨平台的实现并不难。

## Caliburn.Micro

把 Caliburn.Micro 与 XPF 搭配使用时，启动阶段可能遇到线程异常（比如 “The calling thread cannot access this object because a different thread owns it”）。这通常是 Caliburn.Micro 的 `WindowManager` 从非 UI 线程访问 WPF 窗口属性所致。请确保所有窗口操作都在 dispatcher 线程上进行。

## WinForms 控件 {#winforms-controls}

XPF 中承载 WinForms 只在 Windows 上受支持。启用原生 WinForms 集成的方法：

```xml
<PropertyGroup Condition="$([MSBuild]::IsOSPlatform('Windows'))">
    <XpfUseMicrosoftWindowsForms>true</XpfUseMicrosoftWindowsForms>
</PropertyGroup>
```

这会关掉 XPF 的 WinForms shim 层。加上条件判断，项目在其他平台上才照样构建得了。若要跨平台部署，请为 Windows 上由 WinForms 控件承担的那部分功能另备一套界面。

## Aspose

Aspose 的库会给某些程序集设置自己的 `DllImportResolver`。由于 .NET 规定每个程序集只能有一个解析器，这就与 XPF 的 WinApiShim 撞了车。变通办法请见 [Win32 API shim：解决 DllImportResolver 冲突](/xpf/third-party/win32-api-shims#resolving-dllimportresolver-conflicts)。

## 兼容性数据库 {#compatibility-database}

我们提供了一个面向第三方控件的[兼容性数据库](https://avaloniaui.net/xpf/packages)，其中收录了各大厂商控件的最新状态。

:::info
若某个被标为 `Fix In Progress` 或 `Untested` 的控件对你的应用举足轻重，请联系支持团队。Avalonia 团队乐意与你一道把兼容性问题解决掉。
:::

### 兼容性说明 {#compatibility-notes}

* **纯 WPF 控件**：纯用 WPF 实现的第三方控件通常都能正常工作，哪怕它没被收进兼容性数据库。
* **未收录的厂商**：数据库里没有某家控件厂商，并不代表它不兼容。你需要的控件，自己测一测便知。
* **常见的难题**：问题多半出在那些用到 GDI 或 WinForms 组件的控件上。
