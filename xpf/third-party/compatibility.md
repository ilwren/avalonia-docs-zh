---
id: compatibility
title: Library Compatibility
---

This page covers compatibility notes for specific third-party libraries with Avalonia XPF. For enabling Win32 API shims (required by most third-party libraries on non-Windows platforms), see [Win32 API Shims](/xpf/third-party/win32-api-shims).

## DevExpress

DevExpress controls are widely used with XPF. To get started:

1. Enable Win32 API shims in your `App` constructor or `Program.Main` (required for DevExpress controls):
   ```csharp
   AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable();
   ```

   If your application also uses libraries that provide their own cross-platform support (and should not be intercepted by the shim), use the filter callback:
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

2. Verify shims are enabled in the correct location. A common mistake is enabling shims in `Program.cs` for the macOS launcher project but not in `App.xaml.cs` (or vice versa). Shims must be enabled before any third-party assembly attempts to call a Win32 API.

3. Be aware of the following platform-specific limitations:

   - **GDI+ dependency**: Some DevExpress controls (DocumentPreviewControl, PdfViewerControl, XtraReport) depend on `System.Drawing.Common` (GDI+), which is deprecated on non-Windows platforms. Enable DevExpress's Skia rendering engine where available. Contact DevExpress support for guidance on Skia support for specific controls.
   - **LoadingDecorator**: The DevExpress `LoadingDecorator` with `UseSplashScreen=true` requires multiple UI threads, which is not supported on macOS. Use `WaitIndicator` as an alternative.
   - **Linux dependencies**: DevExpress controls on Linux require `libgdiplus`. See [Linux: Other Dependencies](/xpf/platforms/linux#other-dependencies).

4. Use the official DevExpress XPF sample as a reference for correct setup: [Avalonia-XPF-Samples/DevExpressApp](https://github.com/AvaloniaUI/Avalonia-XPF-Samples/tree/master/src/DevExpressApp).

DevExpress maintains a demo application showing which of their controls have been tested with XPF.

## CefSharp

`CefSharp.Wpf.NetCore` is designed for Windows and includes Windows-native Chromium binaries. It does not work on Linux or macOS.

若 CefSharp 针对 `CursorInteropHelper.Create()` 抛出 `NotImplementedException`，请升级到 XPF 1.6.0 或更高版本，那里提供了回退方案。老版本上的变通办法是：从 `ChromiumWebBrowser` 派生并重写 `OnCursorChange`，把 CefSharp 的光标类型映射到 WPF 的 `Cursors`。

For cross-platform browser alternatives, see [Web Content Embedding](/xpf/interop/web-content).

## Dragablz

Dragablz uses Win32 APIs that are not fully implemented in the XPF shim layer (such as `DwmGetWindowAttribute` for specific window chrome effects). On Linux, this causes runtime exceptions.

The recommended approach is to fork the Dragablz library and remove or guard the unsupported platform API calls. The unsupported calls are typically in window chrome and tab-tearing code that can be replaced with cross-platform alternatives.

## Caliburn.Micro

When using Caliburn.Micro with XPF, you may encounter threading exceptions (e.g., "The calling thread cannot access this object because a different thread owns it") during startup. This is typically caused by Caliburn.Micro's `WindowManager` accessing WPF window properties from a non-UI thread. Ensure all window operations occur on the dispatcher thread.

## WinForms controls

WinForms hosting within XPF is supported on Windows only. To enable native WinForms integration:

```xml
<PropertyGroup Condition="$([MSBuild]::IsOSPlatform('Windows'))">
    <XpfUseMicrosoftWindowsForms>true</XpfUseMicrosoftWindowsForms>
</PropertyGroup>
```

This disables XPF's WinForms shim layer. The conditional ensures your project still builds on other platforms. For cross-platform deployments, provide alternative UI for the functionality that WinForms controls handle on Windows.

## Aspose

Aspose libraries set their own `DllImportResolver` on certain assemblies. Because .NET allows only one resolver per assembly, this conflicts with XPF's WinApiShim. See [Win32 API Shims: Resolving DllImportResolver Conflicts](/xpf/third-party/win32-api-shims#resolving-dllimportresolver-conflicts) for the workaround.

## Compatibility database

A [compatibility database](https://avaloniaui.net/xpf/packages) is available for third-party controls. This database provides up-to-date status information for controls from major vendors.

:::info
If you find that a control marked as `Fix In Progress` or `Untested` is mission-critical for your application, contact the support team. The Avalonia team is committed to working with you to ensure compatibility.
:::

### Compatibility notes

* **Pure WPF controls**: Third-party controls that are implemented purely in WPF typically work without any issues, even if not listed in the compatibility database.
* **Unlisted vendors**: The absence of a control vendor from the database does not indicate incompatibility. Test any controls you need.
* **Known challenges**: Issues most commonly arise with controls that use GDI or WinForms components.
