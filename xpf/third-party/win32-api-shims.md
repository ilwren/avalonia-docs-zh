---
id: win32-api-shims
title: Win32 API Shims
---

Avalonia XPF 实现了 WPF 的 API 面，但形形色色的第三方库还依赖各种跨平台拿不到的 Win32 API。

为此，Avalonia XPF 实现了一个 Win32 API 模拟层，让第三方库在非 Windows 平台上也能跑起来。这一层需要你在 XPF 应用中显式启用。

## 什么时候该启用 Win32 API shim {#when-to-enable-win32-api-shims}

只要下列任一条符合你的应用，就该启用 shim 层：

- 用了 DevExpress、Actipro、Syncfusion、Telerik 或 Infragistics 等厂商的第三方 WPF 控件
- 在 macOS 或 Linux 上崩溃，报 `DllNotFoundException: Unable to load shared library 'user32.dll'` 或类似的 Win32 DLL 错误
- 直接调用（P/Invoke）Win32 API 来做窗口管理、获取显示信息或处理主题

若你的应用只用标准 WPF 控件，且所用的第三方库内部也不调 Win32 API，那就可以不要 shim 层。

拿不准时就启用 shim——即便并非必需，开着也无妨。

## 启用 Win32 API shim {#enabling-win32-api-shims}

这项功能必须赶在任何程序集调用 Win32 API 之前启用，所以 `App` 类的构造函数或 `Program.Main` 都是不错的落点。

要在全应用范围内启用 Win32 API 模拟，加上这行调用即可：

```csharp
  AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable();
```

已知自带非 Windows 平台支持的库可以这样排除掉：

```csharp
AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.
  .AutoEnable(asm =>
  {
    var name = asm.GetName().Name.ToLowerInvariant();
    if (name is "sqlite" or "jint" or "esprima" or "magick.net" or "magick.net.core")
      return true;
    return false;
  });
```

也可以按库逐个启用这一层：

```csharp
AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup
  .AddLibrary(typeof(Type.In.Third.Party.Library).Assembly);
```

## 解决 `DllImportResolver` 冲突 {#resolving-dllimportresolver-conflicts}

某些第三方库（比如 Aspose）会给入口程序集设置自己的 `DllImportResolver`。由于 .NET 规定每个程序集只能有一个解析器，这就与 XPF 的 WinApiShim 撞了车，从而引发 `InvalidOperationException: A resolver is already set for the assembly`。

用 `AutoEnable` 筛选回调把冲突的程序集跳过去：

```csharp
AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable(asm =>
{
    var name = asm.GetName().Name;
    if (name != null && name.Contains("Aspose"))
        return true; // true = skip this assembly
    return false;
});
```

## 自定义程序集加载时如何避免死锁 {#avoiding-deadlocks-with-custom-assembly-loading}

若你的应用有一套自定义的托管程序集加载机制（比如插件系统），`AutoEnable` 可能在启动时造成死锁。这时请改用 `AddLibrary`，在程序集解析出来之后逐个注册：

```csharp
// Instead of AutoEnable, add assemblies as they are loaded
AppDomain.CurrentDomain.AssemblyLoad += (sender, args) =>
{
    AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AddLibrary(args.LoadedAssembly);
};
```

更多细节请见[定制初始化](/xpf/configuration/customizing-initialization#custom-assembly-loading)。

## Win32 API shim 的适用范围 {#scope-of-win32-api-shims}

Win32 API shim 层的存在，是为了让那些内部会调用 Win32 API 的第三方 WPF 控件照常可用。它**不是**一个通用的 Win32 模拟层。

要点：
- shim 提供的 Win32 API 面，够让常见的第三方 WPF 控件在非 Windows 平台上跑起来
- 在 Windows 上启用 shim 后，调用会被导向 shim 的实现，而非原生 Win32
- 并非所有 Win32 API 都有（请见 [API 参考](/xpf/third-party/winapi-reference)）
- 窗口消息（比如 `WM_ACTIVATEAPP`）只生成到所支持控件够用的程度
- 能直接用 WPF 或 Avalonia 的 API，就别依赖 Win32 API shim

## 排查问题 {#troubleshooting}

### 应用在 macOS 或 Linux 上崩溃并报 DllNotFoundException {#application-crashes-on-macos-or-linux-with-dllnotfoundexception}

这是没启用 Win32 API shim 时最常见的症状。请把 `AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable()` 加进 `App` 构造函数或 `Program.Main`，并确保它在任何第三方程序集被加载之前执行。

### 用了 AutoEnable 后应用在启动时卡死 {#application-freezes-during-startup-with-autoenable}

若你的应用有自定义的程序集加载机制（比如插件系统），`AutoEnable` 可能在启动时拦截程序集加载而导致死锁。请改用 `AddLibrary` 逐个注册程序集，详见[定制初始化：自定义程序集加载](/xpf/configuration/customizing-initialization#custom-assembly-loading)。

### shim 开了，某个库还是跑不起来 {#shims-are-enabled-but-a-specific-library-still-fails}

有些库调用的 Win32 API 不在 shim 层的覆盖范围内。请对照 [WinAPI shim API 参考](/xpf/third-party/winapi-reference)，确认你那个库需要的 API 是否齐备。若缺了必需的 API，请联系 Avalonia 支持团队。

### Linux 上出现 EntryPointNotFoundException {#entrypointnotfoundexception-on-linux}

若启用 Win32 API shim 后，调用 Linux 原生 API（比如 X11 函数）时报 `EntryPointNotFoundException`，说明本该直通原生库的调用被 shim 层拦下了。请把调用 Linux 原生 API 的代码挪到单独的程序集，并把它从 shim 中排除。请见 [Linux：Win32 API shim 冲突](/xpf/platforms/linux#win32-api-shim-conflicts-with-native-apis)。

### 提示该程序集已设置了解析器 {#a-resolver-is-already-set-for-the-assembly}

这是第三方库（比如 Aspose）设置了自己的 `DllImportResolver` 所致。请用 `AutoEnable` 筛选回调把那个库的程序集跳过去，详见[解决 DllImportResolver 冲突](#resolving-dllimportresolver-conflicts)。
