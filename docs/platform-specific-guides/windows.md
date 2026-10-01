---
id: windows
title: Windows
description: Windows 专属的 Avalonia 特性，包括透明、Mica、自定义标题栏、深色模式、DPI 缩放和 Win32 互操作。
doc-type: overview
---

## Avalonia 在 Windows 上如何运行 {#how-avalonia-runs-on-windows}

在 Windows 上，Avalonia 直接使用 Win32 API。除 .NET SDK 外，不需要额外的工作负载或依赖。目标框架就是 `net9.0` 或 `net10.0`，而非某个平台专属框架。

渲染用的是以 Direct3D 为底的 Skia，在 GPU 加速不可用时会自动退回软件渲染（比如远程桌面会话，或没有 GPU 直通的虚拟机）。输入、窗口、剪贴板、文件对话框、拖放和无障碍，全都由标准 Win32 API 提供。

由于不依赖 Windows 专属的 .NET 工作负载，你可以在 macOS 或 Linux 上交叉编译出 Windows 版本。产出的二进制文件在任何装有 .NET 运行时的受支持 Windows 版本上都能跑。

## 窗口透明与 Mica {#window-transparency-and-mica}

Windows 支持全部 `TransparencyLevelHint` 取值，也是唯一完整支持透明的平台。macOS 只支持 `Transparent`，Linux 的支持情况则取决于合成器。

| 层级 | 效果 | 最低版本 |
|---|---|---|
| `Transparent` | 完全透明的窗口背景 | Windows 7+ |
| `AcrylicBlur` | 模糊的半透明背景 | Windows 10 1803+ |
| `Mica` | 由 DWM 绘制的系统着色材质 | Windows 11 |

启用 Mica 背景的办法：

```xml
<Window xmlns="https://github.com/avaloniaui"
        TransparencyLevelHint="Mica"
        Background="Transparent">
    <!-- Your content -->
</Window>
```

若 Mica 不可用（比如在 Windows 10 上），窗口会按列表顺序逐级回退。读取 `ActualTransparencyLevel` 即可在运行时查看实际生效的级别：

```csharp
var actual = myWindow.ActualTransparencyLevel;
```

任何透明级别要生效，都必须把窗口的 `Background` 属性设为 `Transparent`。不透明的背景会把透明效果完全盖住。

细节请见[窗口管理](/docs/app-development/window-management)。

:::warning[请设置一个不透明的兜底方案！]
无论你在 Avalonia 里怎么配置，Windows 都可能在系统层面取消透明效果，常见原因是省电模式或远程/虚拟会话。建议你设置一个与界面相称的不透明兜底方案，以防用户正是在这类环境下运行你的应用。
:::

## 自定义标题栏 {#custom-title-bars}

Windows 支持把客户区延伸到标题栏区域，以便定制窗口外壳。设置 `ExtendClientAreaToDecorationsHint` 可把你的内容推进标题栏区域，再用 `WindowDecorationProperties.ElementRole` 把某块区域标记为可拖拽的标题栏：

```xml
<Window ExtendClientAreaToDecorationsHint="True"
        WindowDecorations="None">
    <Grid RowDefinitions="32,*">
        <Border Grid.Row="0" Background="#2D2D2D"
                WindowDecorationProperties.ElementRole="TitleBar">
            <TextBlock Text="My App" Foreground="White"
                       VerticalAlignment="Center" Margin="12,0" />
        </Border>
        <Border Grid.Row="1">
            <TextBlock Text="Window content" />
        </Border>
    </Grid>
</Window>
```

被标记的区域支持原生的窗口拖拽和双击最大化。放在标题栏区域里的交互控件照样能正常接收输入。

设置 `WindowDecorations="None"` 会彻底去掉系统外壳，窗口边框完全由你掌控。

设置 `WindowDecorations="Full"` 则保留系统的最小化、最大化和关闭按钮。若你做了自定义标题栏，它们会与之并存。在 Windows 上，被禁用的标题栏按钮是直接隐藏，而不是置灰。

细节请见[窗口管理](/docs/app-development/window-management#custom-title-bar)。

## 深色模式与系统主题检测 {#dark-mode-and-system-theme-detection}

Avalonia 通过 `PlatformSettings` 检测 Windows 的系统主题和强调色。内置的 `FluentTheme` 会自动在浅色与深色变体间切换，以贴合系统偏好。

读取当前主题并响应其变化：

```csharp
var settings = myControl.GetPlatformSettings();
var colors = settings?.GetColorValues();

// Check current theme
if (colors?.ThemeVariant == ThemeVariant.Dark)
{
    // System is in dark mode
}

// React to theme changes in real time
if (settings is not null)
{
    settings.ColorValuesChanged += (sender, values) =>
    {
        // values contains updated theme and accent colors
    };
}
```

当你要写的主题逻辑超出 `FluentTheme` 自动处理的范围时，这就有用了。比如你可以根据系统处于浅色还是深色模式，调整图表配色或图片叠加层。

:::note
在 Windows 11 上，Avalonia 会自动更新原生标题栏以匹配应用的 `RequestedThemeVariant`。在 Windows 10 上，标题栏不会变暗，因为平台没有提供官方 API。若你在 Windows 10 上确实需要深色标题栏，请使用[自定义标题栏](#custom-title-bars)，或 [Windows 排查问题](/troubleshooting/platform-specific-issues/windows#title-bar-stays-light-when-switching-to-dark-theme-on-windows-10)中介绍的那个未公开的 `DwmSetWindowAttribute` 变通办法。
:::

细节请见[平台设置](/docs/services/platform-settings)。

## 高 DPI 与逐显示器缩放 {#high-dpi-and-per-monitor-scaling}

在 Windows 上，Avalonia 默认是逐显示器 DPI 感知的。每台显示器各自报告自己的缩放系数，窗口在显示器之间移动时，Avalonia 会自动调整布局和渲染。

`Screen.Scaling` 属性给出每台显示器的 DPI 缩放系数：

| 缩放值 | DPI | 常见用途 |
|---|---|---|
| `1.0` | 96 | 标准像素密度（100%） |
| `1.25` | 120 | 125% scaling |
| `1.5` | 144 | 150% scaling |
| `2.0` | 192 | HiDPI / 200% 缩放 |

Avalonia 的全部布局都以设备无关像素为单位，因此不必手动做 DPI 换算。要读取当前屏幕的缩放系数，请用 `screen?.Scaling`：

```csharp
var screen = myWindow.Screens.ScreenFromWindow(myWindow);
var scaling = screen?.Scaling ?? 1.0;
```

对于位图资产，当显示缩放达到 2.0 或更高时，Avalonia 会自动选用 `@2x` 变体。

细节请见[窗口管理](/docs/app-development/window-management#working-with-screens)。

## 嵌入原生 Win32 控件 {#embedding-native-win32-controls}

借助 `NativeControlHost`，你可以把基于 HWND 的 Win32 控件承载进 Avalonia 布局。重写 `CreateNativeControlCore` 来创建原生控件并返回其句柄：

```csharp
public class NativeTextEditor : NativeControlHost
{
    protected override IPlatformHandle CreateNativeControlCore(
        IPlatformHandle parent)
    {
        if (OperatingSystem.IsWindows())
        {
            var hwnd = CreateWindowEx(0, "EDIT", "",
                WS_CHILD | WS_VISIBLE | ES_MULTILINE,
                0, 0, 100, 100,
                parent.Handle, IntPtr.Zero, IntPtr.Zero, IntPtr.Zero);
            return new PlatformHandle(hwnd, "HWND");
        }

        return base.CreateNativeControlCore(parent);
    }

    protected override void DestroyNativeControlCore(
        IPlatformHandle control)
    {
        if (OperatingSystem.IsWindows())
            DestroyWindow(control.Handle);
        else
            base.DestroyNativeControlCore(control);
    }
}
```

你也可以取得任意 Avalonia 窗口的 HWND，以便与既有的 Win32 代码互操作：

```csharp
var handle = TopLevel.GetTopLevel(myControl)?.TryGetPlatformHandle();
// handle.Handle contains the HWND as IntPtr
// handle.HandleDescriptor is "HWND"
```

经 `NativeControlHost` 渲染的原生控件始终位于 Avalonia 内容之上或之下，不参与正常视觉树的 z 序。它们不支持透明，也不受渲染变换（旋转、缩放）影响，裁剪只能到宿主控件的边界为止。

更多细节请见[原生平台互操作](/docs/app-development/native-interop)。

## 在 Windows Forms 中使用 Avalonia {#using-avalonia-in-windows-forms}

借助 `WinFormsAvaloniaControlHost`，Avalonia 控件可以承载在 Windows Forms 应用内部。这样既有的 Windows Forms 应用就能逐步迁到 Avalonia，不必一次性推倒重来。

典型的配置至少需要两个项目：

1. **YourApp**：一个跨平台类库，装着你的 Avalonia 控件和视图模型。
2. **YourApp.WinForms**：你既有的 Windows Forms 应用。
3. **YourApp.Desktop**（可选）：一个独立的 Avalonia 可执行程序。只有当你想用 Visual Studio 的 XAML 预览器时才需要它。

由于 Windows Forms 只能在 Windows 上跑，把 Avalonia 控件嵌进 WinForms 应用并不能让它变成跨平台。要跨平台，你必须彻底迁到 Avalonia 桌面项目。

### 配置 {#setup}

:::note
下面的说明假定你使用 Visual Studio 并装了 Avalonia for Visual Studio 扩展。若你用的是 VS Code 或 Rider，可以跳过可选的 `YourApp.Desktop` 项目。
:::

1. 用 **Avalonia C# Project** 模板往解决方案里添加一个新项目，目标平台至少勾上 **Desktop**。这会生成 `YourApp` 和 `YourApp.Desktop`。

2. 为你的 Windows Forms 项目添加以下引用：
   - 包引用：`Avalonia.Desktop`
   - 包引用：`Avalonia.Win32.Interoperability`
   - 项目引用：`YourApp.csproj`

3. 在 WinForms 的 `Program.cs` 中，于调用 `Application.Run()` 之前先初始化 Avalonia：

```csharp
AppBuilder.Configure<App>()
    .UsePlatformDetect()
    .SetupWithoutStarting();
```

4. 往窗体上放一个 `WinFormsAvaloniaControlHost` 控件。添加包引用之后，工具箱里就能找到它。

5. 在窗体构造函数里、`InitializeComponent()` 之后设置它的内容：

```csharp
winFormsAvaloniaControlHost1.Content = new MainView
{
    DataContext = new MainViewModel()
};
```

现在你应该能在 Windows Forms 应用内部看到 Avalonia 的默认视图了。

### 打开独立的 Avalonia 窗口 {#opening-standalone-avalonia-windows}

除了把 Avalonia 控件嵌进窗体，你还可以直接从 WinForms 应用打开一个顶层 Avalonia `Window`。它会作为一个独立的原生窗口出现，自带窗口装饰和任务栏项，与你的 WinForms 窗口并存。

由于两个框架都定义了名字相近的类型（比如 `Button` 或 `TextBox`），请给 Avalonia 的命名空间起别名，以免引用含混不清：

```csharp
using AvaloniaWindow = Avalonia.Controls.Window;
using AvaloniaButton = Avalonia.Controls.Button;

private void OpenWindowButton_Click(object sender, EventArgs e)
{
    var window = new AvaloniaWindow
    {
        Width = 300,
        Height = 300,
        Content = new MainView()
    };
    window.Show();
}
```

### 把键盘输入路由到 Avalonia 窗口 {#routing-keyboard-input-to-avalonia-windows}

独立的 Avalonia 窗口跑在由 `Application.Run()` 启动的 WinForms 消息循环中。WinForms 会在键盘消息抵达那些不归它管的窗口之前先行拦下，这意味着不做额外配置的话，Avalonia 窗口既收不到键入的字符，也无法用键盘导航。

要让键盘输入可用，请在 `Program.cs` 中多加一行，在启动期间注册一个 `WinFormsAvaloniaMessageFilter`。这必须发生在 `Application.Run()` 之前。

```csharp title="Program.cs"
[STAThread]
static void Main()
{
    System.Windows.Forms.Application.EnableVisualStyles();
    System.Windows.Forms.Application.SetCompatibleTextRenderingDefault(false);
    // highlight-next-line
    System.Windows.Forms.Application.AddMessageFilter(new WinFormsAvaloniaMessageFilter());

    AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .SetupWithoutStarting();

    System.Windows.Forms.Application.Run(new MainForm());
}
```

`WinFormsAvaloniaMessageFilter` 位于 `Avalonia.Win32.Interoperability` 包中。它负责派发发往顶层 Avalonia 窗口的键盘消息，同时不去碰那些发给嵌入式宿主和原生 WinForms 控件的消息。

:::note
只有独立的 Avalonia 窗口才需要这个消息过滤器，用 `WinFormsAvaloniaControlHost` 嵌入的控件无需它。
:::

## 系统托盘集成 {#system-tray-integration}

Windows 完整支持 `TrayIcon`。托盘图标会出现在 Windows 通知区域，右键可弹出 `NativeMenu` 上下文菜单。

```xml
<TrayIcon Icon="/Assets/app-icon.ico"
          ToolTipText="My Application">
    <TrayIcon.Menu>
        <NativeMenu>
            <NativeMenuItem Header="Show Window" Click="ShowWindow_OnClick" />
            <NativeMenuItemSeparator />
            <NativeMenuItem Header="Exit" Click="Exit_OnClick" />
        </NativeMenu>
    </TrayIcon.Menu>
</TrayIcon>
```

Windows 要求托盘图标为 `.ico` 格式。请把图标文件作为 Avalonia 资源写进 `.csproj`：

```xml
<ItemGroup>
    <AvaloniaResource Include="Assets/app-icon.ico" />
</ItemGroup>
```

若想让应用最小化到托盘而非任务栏，请在最小化时把窗口的 `ShowInTaskbar="False"` 设好，再从托盘图标的点击处理程序里把它恢复出来。

细节请见 [TrayIcon](/controls/navigation/trayicon)。

## 无障碍 {#accessibility}

在 Windows 上，Avalonia 通过 UI 自动化（UIA）框架把界面元素暴露给辅助技术。讲述人、NVDA 之类的屏幕阅读器可以朗读 Avalonia 应用并与之交互。

内置控件会自动提供自动化 peer，所以按钮、文本框、列表项这些标准控件开箱即可配合屏幕阅读器。对于自定义控件，请设置 `AutomationProperties.Name` 以给出有意义的标签：

```xml
<MyCustomControl AutomationProperties.Name="Star rating" />
```

更复杂的场景下，请在控件中重写 `OnCreateAutomationPeer`，返回一个能报告恰当控件类型和状态的自定义自动化 peer。

若要配合讲述人使用地标导航，请把 `AutomationProperties.AccessibilityView` 至少设为 `"Control"`，以启用讲述人的地标快捷键。

细节请见[无障碍](/docs/app-development/accessibility)。

## Windows 上的平台专属服务 {#platform-specific-services-on-windows}

在 Windows 上，Avalonia 的平台服务基于 Win32 API。下面汇总了几项常用服务的行为：

| 服务 | Windows 上的行为 |
|---|---|
| Clipboard | 通过 Win32 剪贴板 API 支持文本、HTML、RTF 和文件列表。 |
| 文件对话框 | 使用 Win32 通用文件对话框（`IFileDialog`），支持文件类型筛选、初始目录和多选。 |
| 拖放 | 支持从资源管理器拖入文件，也支持经由 OLE 拖放在应用之间传递数据。 |
| Launcher | `Launcher.LaunchUriAsync` 用默认浏览器打开 URL，`Launcher.LaunchFileAsync` 用关联的应用打开文件。 |

## 另请参阅 {#see-also}

- [为 Windows 打包](/tools/parcel/packaging-for-windows)
- [WPF 迁移指南](/docs/migration/wpf)
- [Native Platform Interop](/docs/app-development/native-interop)
- [Window Management](/docs/app-development/window-management)
- [Platform Settings](/docs/services/platform-settings)
- [键盘与热键](/docs/input-interaction/keyboard-and-hotkeys)
- [无障碍](/docs/app-development/accessibility)
