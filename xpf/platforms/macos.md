---
id: macos
title: macOS
---

## 应用名称 {#application-name}

macOS 的菜单栏和系统对话框默认把应用名显示为 “Avalonia Application”。要换成你自己的应用名，需要配置 Avalonia 的 `Application` 对象。

### 使用自定义 Avalonia 应用类 {#using-a-custom-avalonia-application}

照[定制初始化](/xpf/configuration/customizing-initialization#optional-define-a-custom-avalonia-application)中的步骤创建一个自定义的 Avalonia Application 类，然后在 AXAML 中设置 `Name` 属性：

```xml title="MyAvaloniaApp.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyXpfApp.MyAvaloniaApp"
             Name="My App Name">
  <Application.Styles>
    <SimpleTheme/>
  </Application.Styles>
</Application>
```

### Using DefaultXpfAvaloniaApplication

若你并不需要一整个自定义 Application 类，也可以继承 `DefaultXpfAvaloniaApplication` 并设置 `Name` 属性：

```csharp
public class MyAvaloniaApp : AvaloniaUI.Xpf.Helpers.DefaultXpfAvaloniaApplication
{
    public MyAvaloniaApp()
    {
        Name = "My App Name";
    }
}
```

然后在 `AppBuilder` 配置中引用这个类：

```csharp
AppBuilder.Configure<MyAvaloniaApp>()
    .UsePlatformDetect()
    .WithAvaloniaXpf()
    .SetupWithLifetime(new ClassicDesktopStyleApplicationLifetime
    {
        ShutdownMode = ShutdownMode.OnExplicitShutdown
    });
```

## 原生菜单 {#native-menus}

macOS 应用用的是屏幕顶部的全局菜单栏。XPF 通过 Avalonia 的 `NativeMenu` API 支持它。

### 用代码配置原生菜单 {#setting-up-a-native-menu-programmatically}

在 WPF 窗口的 `Loaded` 事件中，取到底层的 Avalonia 窗口并给它设置菜单：

```csharp
using Atlantis;
using Avalonia.Controls;

private void Window_Loaded(object sender, RoutedEventArgs e)
{
    var avaloniaWindow = XpfWpfAbstraction.GetAvaloniaWindowForWindow(this);

    var menu = new NativeMenu();

    var fileMenu = new NativeMenuItem("File");
    var fileSubMenu = new NativeMenu();
    fileSubMenu.Add(new NativeMenuItem("Open") { Command = /* your command */ });
    fileSubMenu.Add(new NativeMenuItemSeparator());
    fileSubMenu.Add(new NativeMenuItem("Exit") { Command = /* your command */ });
    fileMenu.Menu = fileSubMenu;

    menu.Add(fileMenu);
    NativeMenu.SetMenu(avaloniaWindow, menu);
}
```

### 跨平台的菜单回退方案 {#cross-platform-menu-fallback}

在不支持全局菜单栏的平台上（Windows 和多数 Linux 桌面环境），你可以通过 `AvaloniaHost` 在 XPF 窗口中嵌入一个 `NativeMenuBar` 控件。该控件只在没有原生全局菜单的平台上渲染出传统菜单栏，在 macOS 上则会隐藏（那里走全局菜单）。

承载 Avalonia 控件的细节请见[在 XPF 中嵌入 Avalonia](/xpf/interop/embedding-avalonia-in-xpf)。

## Dock 中的可见性 {#dock-visibility}

若要控制应用是否出现在 macOS 的 Dock 中，请在[自定义初始化](/xpf/configuration/customizing-initialization)中使用 `MacOSPlatformOptions`：

```csharp
AppBuilder.Configure<MyAvaloniaApp>()
    .UsePlatformDetect()
    .With(new MacOSPlatformOptions { ShowInDock = false })
    .WithAvaloniaXpf()
    .SetupWithLifetime(new ClassicDesktopStyleApplicationLifetime
    {
        ShutdownMode = ShutdownMode.OnExplicitShutdown
    });
```

### Info.plist interaction

`ShowInDock` 选项与 macOS 的 `Info.plist` 设置相互影响：

| 配置 | 行为 |
|---|---|
| `ShowInDock = false` | 应用不出现在 Dock 中，等同于 `LSUIElement = true`。 |
| `LSUIElement = true` in Info.plist | 应用既不出现在 Dock 中，也不出现在 Cmd+Tab 切换器里，且没有菜单栏。 |
| `LSBackgroundOnly = true` in Info.plist | 应用作为后台进程运行，完全没有界面存在感。带窗口的 XPF 应用不适合用它。 |

若你既在代码里设了 `ShowInDock = false`，又在 `Info.plist` 中设了 `LSUIElement`，请用 XPF 1.6.0 或更高版本，以免启动时 Dock 图标闪一下。

若应用只有托盘图标，请用 `ShowInDock = false`，并提供一个系统托盘图标供用户交互。

## 启动与模态对话框 {#startup-and-modal-dialogs}

在 macOS 上，于窗口激活阶段弹出模态对话框（通过 `ShowDialog`）可能让应用卡死。原因在于首次绘制通知会在渲染管线完全就绪之前触发启动代码，而此时调用 `ShowDialog` 会启动一个嵌套的 dispatcher 循环，把这次绘制堵在半道上。

### 推荐的解决办法 {#recommended-solutions}

在 `.csproj` 中加入下面的内容，把启动代码推迟到安全的 dispatcher 优先级上执行：

```xml
<ItemGroup>
    <RuntimeHostConfigurationOption Include="AvaloniaUI.Xpf.AllowBlockingCallsOnStartup" Value="true" />
</ItemGroup>
```

另一个办法是别在窗口构造函数或激活处理程序里调用 `ShowDialog`，改为在 `Application.Startup` 事件中触发对话框，或者通过 dispatcher 回调来弹：

```csharp
Dispatcher.CurrentDispatcher.BeginInvoke(DispatcherPriority.Loaded, () =>
{
    var dialog = new MyDialog();
    dialog.ShowDialog();
});
```

:::caution
在 macOS 上，涉及启动嵌套消息循环的操作（比如 `ShowDialog`）请避开 `DispatcherPriority.Normal` 或 `DispatcherPriority.Send`，改用 `DispatcherPriority.Loaded` 或更低的优先级。
:::

## DPI 与渲染缩放 {#dpi-and-render-scaling}

WPF 的 `VisualTreeHelper.GetDpi()` API 在 macOS 上未必给得出准确值。要取得正确的渲染缩放系数，请访问底层的 Avalonia 窗口：

```csharp
using Atlantis;

var avaloniaTopLevel = XpfWpfAbstraction.GetAvaloniaTopLevelForWindow(myWpfWindow);
double scaling = avaloniaTopLevel.RenderScaling;
```

## 触控板手势 {#trackpad-gestures}

macOS 的触控板手势（捏合缩放、旋转）在 XPF 中没法通过 WPF 的 manipulation API 拿到。要处理这些手势，请在底层的 Avalonia 窗口上使用 Avalonia 的手势事件：

```csharp
using Atlantis;
using Avalonia.Input;

var avaloniaWindow = XpfWpfAbstraction.GetAvaloniaWindowForWindow(this);

// Pinch-to-zoom
avaloniaWindow.AddHandler(Gestures.PointerTouchPadGestureMagnifyEvent, (sender, e) =>
{
    double scale = e.Scale;
    // Handle zoom
}, handledEventsToo: true);
```

想区分触控板滚动与鼠标滚轮事件，可在处理 `PointerWheelChanged` 时查看 `PointerDeltaEventArgs` 属性。

## GDI+ 与 System.Drawing.Common {#gdi-and-systemdrawingcommon}

`System.Drawing.Common`（GDI+）在非 Windows 平台上已废弃，在 macOS 的 XPF 中会抛异常。这通常会牵连那些依赖 GDI+ 做渲染或打印的第三方控件（比如某些 DevExpress 控件）。

若第三方控件提供基于 Skia 的渲染选项，请在非 Windows 构建中启用它。至于非 GDI 的渲染后端怎么用，请咨询控件厂商。

更多细节请见[库的兼容性](/xpf/third-party/compatibility)。

## 打包与部署 {#packaging-and-deployment}

macOS 应用必须打成 `.app` 包才能分发。XPF 应用要特别留意这几点：

- **不要**把 `IncludeNativeLibrariesForSelfExtract` 设为 `true`，它与 macOS 不兼容。
- 要分发到开发机之外，请用 `SelfContained` 方式发布。
- 代码签名时请逐个文件签，别用 `--deep` 标志。
- 请从命令行发布而非 Visual Studio，这样产出才靠谱：

```bash
dotnet publish -r osx-arm64 -c Release --self-contained
```

:::tip
Avalonia 的 **Parcel** 工具可以把 XPF 应用的 macOS 打包、代码签名和公证自动化。想使用请联系 Avalonia 团队。
:::

## 按键映射 {#key-mapping}

macOS 的修饰键与 Windows、Linux 不同。默认的映射关系如下：

- Control -> `Key.LeftCtrl` / `Key.RightCtrl` / `ModifierKeys.Control`
- Option -> `Key.LeftAlt` / `Key.RightAlt` / `ModifierKeys.Alt`
- Command -> `Key.LWin` / `Key.RWin` / `ModifierKeys.Windows`

不过这套映射有几个问题：

1. macOS 应用通常在 Windows 和 Linux 用 Control 键的地方改用 Command 键。比如“复制”在 macOS 上是 Command-C，而不是 Control+C
2. WPF 有意不把 `ModifierKeys.Windows` 纳入 `Keyboard.Modifiers`，于是靠标准的 WPF 修饰键检查根本察觉不到 Command 键
3. 文本框这类常见控件在 macOS 上的快捷键也与别处不同，比如“把插入点移到上一个词的开头”在 macOS 上是 Option+左方向键，而非 Control+左方向键

### macOS 自动按键映射 {#automatic-macos-key-mapping}

要解决上述大部分问题，可以在启动时调用 `XpfKeyboard.MapMacOSKeys()` 方法。通常把它放在和 [XPF WinAPI shim 配置](/xpf/third-party/win32-api-shims)同一个地方，也就是 `App` 类的构造函数或 `Program.Main` 中：

```csharp
using System.Windows;
using Atlantis;

namespace XpfKeyboardMappingExample;

public partial class App : Application
{
    public App()
    {
        XpfKeyboard.MapMacOSKeys();
    }
}
```

在 macOS 上调用该方法会：

- 把 Command 键映射成 Control 键
- 把一些常用的文本框快捷键映射成 XPF 中的对应组合
  - Command+Left -> Home
  - Command+Right -> End
  - Option+左方向键 -> Ctrl+左方向键
  - Option+Left Arrow -> Ctrl+Left Arrow

### macOS 自定义键盘映射 {#macos-custom-keyboard-mapping}

想要更灵活的按键映射，可以[添加自定义映射](/xpf/migration/key-mapping)。

## 上下文菜单 {#context-menus}

在 macOS 上，除了右键点击，Ctrl+点击同样可以打开上下文菜单。启动时设置 `XpfMouse.ShowContextMenuOnMacOSCtrlClick` 即可启用这项功能，通常把它放在和 [XPF WinAPI shim 配置](/xpf/third-party/win32-api-shims)同一个地方，也就是 `App` 类的构造函数或 `Program.Main` 中：

```csharp
using System.Windows;
using Atlantis;

namespace XpfKeyboardMappingExample;

public partial class App : Application
{
    public App()
    {
        XpfMouse.ShowContextMenuOnMacOSCtrlClick = true;
    }
}
```

启用之后，还可以按控件单独关掉：处理 `ContextMenuOpening` 事件，并通过 `Keyboard.Modifiers` 和/或 `Mouse.LeftButton` 判断这次上下文菜单是怎么被唤起的：

```csharp
private void OnContextMenuOpening(object sender, ContextMenuEventArgs e)
{
    // Suppress context menu on Ctrl+Click for this specific control
    if (Keyboard.Modifiers.HasFlag(ModifierKeys.Control) && Mouse.LeftButton == MouseButtonState.Pressed)
    {
        e.Handled = true;
    }
}
```

## 原生 API 互操作 {#native-api-interop}

若要在 XPF 应用中访问 macOS 专属的 API（比如钥匙串或原生 cookie），有这么几条路：

- 常见的 macOS API 可以用 `MonoMac.NetStandard` NuGet 包
- 用 C 风格的 `DllImport` 直接调用 macOS 的框架
- 访问 WebView 的 cookie 请用 XPF 提供的 `NativeWebViewCookieManager` API

:::note
MAUI Essentials 不支持 macOS（只支持 Mac Catalyst），在 macOS 上没法与 XPF 搭配使用。
:::

## 已知限制 {#known-limitations}

- **多个 UI 线程**：macOS 只允许一个 UI 线程。那些依赖多个 dispatcher 的 WPF 写法（比如把启动画面放在另一线程）在这里行不通。请把它们改造成统一走主 dispatcher，需要延后的活儿交给 `DispatcherPriority.Background`。
- **透明窗口的点击穿透**：XPF 不支持逐像素的命中测试透明（点穿窗口的透明区域）。不妨把内容放进同一个窗口，而不是用透明叠加层。
- **SystemSounds.Beep**：macOS 上不支持 `System.Media.SystemSounds.Beep`，调用会抛出 `PlatformNotSupportedException`。请加上平台判断，或者在跨平台构建中去掉这类调用。
- **工具提示抢焦点**：在某些 macOS 版本上，显示工具提示会让应用短暂地从其他应用那里抢走焦点。这是个已知问题，XPF 团队正在跟进。
