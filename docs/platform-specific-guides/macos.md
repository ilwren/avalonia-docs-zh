---
id: macos
title: macOS
---

## Avalonia 在 macOS 上如何运行 {#how-avalonia-runs-on-macos}

Avalonia 并不使用标准的 .NET macOS 工作负载（`net10.0-macos`），而是自带一套原生平台后端：它通过一个编译好的动态库（`libAvaloniaNative.dylib`）与 macOS API 打交道，完全绕开了微软的托管 macOS 绑定。

这套原生后端用 Objective-C++（`.mm` 文件）写成，位于 Avalonia 仓库的 [`native/Avalonia.Native/src/OSX`](https://github.com/AvaloniaUI/Avalonia/tree/master/native/Avalonia.Native/src/OSX)。它提供了平台最基本的那些能力：窗口、输入处理、Metal 与 OpenGL 渲染、剪贴板、菜单、拖放、系统托盘、文件对话框和无障碍。.NET 一侧通过轻量的 COM 风格互操作层 MicroCom 与这些原生代码通信：两侧的接口定义在一个 [IDL 文件](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Native/avn.idl)中，MicroCom 据此生成负责跨边界封送调用的托管包装。

这带来一个很实在的好处：你可以在 Windows 或 Linux 上构建、编译面向 macOS 的 Avalonia 桌面应用，既不用装 macOS 工作负载，也不需要一台 Mac。默认目标框架就是 `net9.0`（或 `net10.0`），而非某个平台专属框架。

代价是 Avalonia 的原生绑定很精简：它只覆盖框架做界面所需的那部分，并不暴露 macOS 平台 API 的全貌（比如 MapKit、HealthKit、StoreKit 等）。

### 用上完整的 macOS API {#accessing-the-full-macos-api-surface}

若你的应用需要 Avalonia 未暴露的 macOS API，请把目标框架改成 macOS 专属的：

```xml
<TargetFramework>net10.0-macos</TargetFramework>
```

这样你就能用上 .NET macOS 工作负载提供的全部 API，但也随之带来一个约束：**面向 macOS TFM 的构建必须在 macOS 上进行**，你将失去从 Windows 或 Linux 交叉编译的能力。

## 应用名称与标识 {#application-name-and-identity}

macOS 会在好几处显示你的应用名称：菜单栏、"关于"对话框、"退出"菜单项、程序坞提示和窗口标题栏。要让它们都对，就得在正确的地方设置名称。

### 名称都是从哪儿来的 {#where-the-name-comes-from}

| 位置 | Source | 注释支持情况 |
|---|---|---|
| 菜单栏（粗体的应用名） | `Info.plist` 中的 `CFBundleName`（已打包），或 `Application.Name`（未打包） | `CFBundleName` 最多 15 个字符。 |
| 程序坞提示 | `Info.plist` 中的 `CFBundleDisplayName`，回退到 `CFBundleName` | 名称超过 15 个字符时请用 `CFBundleDisplayName`。 |
| "关于"菜单项 | 你的 [`NativeMenuItem`](/api/avalonia/controls/nativemenuitem) 的标题文字 | 这段文字完全由你掌控。 |
| "退出"菜单项 | `CFBundleName` or `Application.Name` | Avalonia 会自动生成 "Quit App Name"。 |
| 窗口标题栏 | `Window.Title` property | 与应用名称无关。 |

### 设置应用名称 {#setting-the-application-name}

**第 1 步：在 `App.axaml` 中设置 `Application.Name`**

它决定开发期间（还没有 `.app` 包时）显示的名称：

```xml
<Application Name="My Application" ...>
```

**第 2 步：在 `Info.plist` 中设置 `CFBundleName` 和 `CFBundleDisplayName`**

当应用以打包好的 `.app` 形式运行时，macOS 会从 `Info.plist` 而非 `Application.Name` 读取名称。请保持这些值一致：

```xml
<key>CFBundleName</key>
<string>My App</string>

<key>CFBundleDisplayName</key>
<string>My Application</string>
```

`CFBundleName` 最多 15 个字符，用于菜单栏和"退出"项；`CFBundleDisplayName` 没有长度限制，供访达和程序坞使用。若你的应用名在 15 个字符以内，只设 `CFBundleName` 就够了。

## 原生菜单栏 {#native-menu-bar}

macOS 应用的菜单栏在屏幕顶端，与应用窗口相互独立。Avalonia 通过 [`NativeMenu`](/api/avalonia/controls/nativemenu) 支持它，渲染出来就是原生的 macOS 菜单栏。

### 应用程序菜单 {#application-menu}

菜单栏最左边那个菜单顶着你的应用名，通常含有"关于"、"偏好设置"和"退出"几项。在 `App.axaml` 里给你的 `Application` 附上一个 `NativeMenu` 即可定义它：

```xml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApp.App"
             Name="My Application">

    <NativeMenu.Menu>
        <NativeMenu>
            <NativeMenuItem Header="About My Application..." Click="About_OnClick" />
            <NativeMenuItem Header="Preferences..." Click="Preferences_OnClick"
                            Gesture="Meta+Comma" />
        </NativeMenu>
    </NativeMenu.Menu>
</Application>
```

若你没有定义 `NativeMenu`，Avalonia 会生成一个默认的应用程序菜单，其中含有"About Avalonia"项。自己定义一个菜单即可取而代之。

Avalonia 会在你的自定义菜单项之后自动补上标准项，包括一条分隔线和快捷键为 <kbd>⌘</kbd><kbd>Q</kbd> 的"Quit App Name"。你不必自己添加退出项。

### 替换"关于"对话框 {#replacing-the-about-dialog}

应用程序菜单里的"关于"项是你自己定义的 `NativeMenuItem`，并无特殊的内建行为。给它的 `Click` 事件挂个处理程序，想显示什么界面都行：

```csharp
private void About_OnClick(object? sender, EventArgs e)
{
    var aboutWindow = new AboutWindow();
    aboutWindow.ShowDialog(this.GetMainWindow());
}
```

macOS 用户习惯「关于」项排在应用程序菜单的头一位，标题写成 "About My Application..."，末尾带省略号。这是惯例，框架并不强制。

### 窗口菜单 {#window-menus}

要添加「文件」「编辑」这类标准菜单，请给你的 `Window` 附上一个 `NativeMenu`：

```xml
<Window xmlns="https://github.com/avaloniaui">
    <NativeMenu.Menu>
        <NativeMenu>
            <NativeMenuItem Header="File">
                <NativeMenu>
                    <NativeMenuItem Header="Open..." Gesture="Meta+O"
                                    Click="FileOpen_OnClick" />
                    <NativeMenuItem Header="Save" Gesture="Meta+S"
                                    Command="{Binding SaveCommand}" />
                    <NativeMenuItemSeparator />
                    <NativeMenuItem Header="Close" Gesture="Meta+W"
                                    Click="FileClose_OnClick" />
                </NativeMenu>
            </NativeMenuItem>
            <NativeMenuItem Header="Edit">
                <NativeMenu>
                    <NativeMenuItem Header="Cut" Gesture="Meta+X"
                                    Command="{Binding CutCommand}" />
                    <NativeMenuItem Header="Copy" Gesture="Meta+C"
                                    Command="{Binding CopyCommand}" />
                    <NativeMenuItem Header="Paste" Gesture="Meta+V"
                                    Command="{Binding PasteCommand}" />
                </NativeMenu>
            </NativeMenuItem>
        </NativeMenu>
    </NativeMenu.Menu>
</Window>
```

在 macOS 上，名为 "Edit" 的菜单项有特殊待遇：Avalonia 会自动为任何以此为标题的菜单添上 macOS 标准的文本编辑功能（比如自动补全和字符替换）。

每个 `NativeMenuItem` 都得有 `Click` 事件处理程序或 `Command` 绑定才会启用，两者皆无则该项会呈灰色。

### 程序坞菜单 {#dock-menu}

当用户在程序坞中右键（或按住 Control 点击）你的应用图标时，macOS 会弹出一个上下文菜单。在 `App.axaml` 里给你的 `Application` 附上一个 `NativeDock.Menu` 即可自定义这个菜单：

```xml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApp.App"
             Name="My Application">

    <NativeDock.Menu>
        <NativeMenu>
            <NativeMenuItem Header="New Window" Click="NewWindow_OnClick" />
            <NativeMenuItemSeparator />
            <NativeMenuItem Header="Show Main Window" Click="ShowMainWindow_OnClick" />
        </NativeMenu>
    </NativeDock.Menu>
</Application>
```

程序坞菜单项会显示在 macOS 自动添加的系统标准项（比如"选项"和"退出"）上方。

你也可以在运行时修改程序坞菜单：

```csharp
var dockMenu = NativeDock.GetMenu(this);
if (dockMenu is not null)
{
    dockMenu.Items.Insert(0, new NativeMenuItem("Dynamic Item"));
}
```

:::note
`NativeDock.Menu` 只在 macOS 上起作用，其他平台会忽略该属性。
:::

### 键盘快捷键 {#keyboard-shortcuts}

`Gesture` 属性为菜单项指定键盘快捷键。Avalonia 在手势字符串中使用平台中立的修饰键名称，在 macOS 上它们会映射到标准修饰键：

| Avalonia 修饰键 | macOS 按键 | 符号 |
|---|---|---|
| `Meta` | Command | <kbd>⌘</kbd> |
| `Control` | Control | <kbd>⌃</kbd> |
| `Shift` | Shift | <kbd>⇧</kbd> |
| `Alt` | Option | <kbd>⌥</kbd> |

手势字符串用 `+` 连接一个或多个修饰键，后面跟上键名：

| `Gesture` 值 | macOS 快捷键 |
|---|---|
| `Meta+S` | <kbd>⌘</kbd> <kbd>S</kbd> |
| `Meta+Shift+S` | <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>S</kbd> |
| `Meta+Comma` | <kbd>⌘</kbd> <kbd>,</kbd> |
| `Meta+Alt+Q` | <kbd>⌘</kbd> <kbd>⌥</kbd> <kbd>Q</kbd> |

## macOS 平台惯例 {#macos-platform-conventions}

macOS 用户对某些标准快捷键和行为有既定预期。其中一部分 Avalonia 会自动照应，另一部分则需要你显式配置。

### 标准快捷键 {#standard-shortcuts}

下列快捷键是 macOS 用户默认会用的惯例。请用 `NativeMenu` 手势或 `KeyBinding` 来配置：

| 动作 | 快捷键 | 注释支持情况 |
|---|---|---|
| Preferences | <kbd>⌘</kbd> <kbd>,</kbd> | 应当打开你的设置/偏好设置视图 |
| Quit | <kbd>⌘</kbd> <kbd>Q</kbd> | 由原生菜单自动处理 |
| Close Window | <kbd>⌘</kbd> <kbd>W</kbd> | 绑定为关闭当前活动窗口 |
| Minimize | <kbd>⌘</kbd> <kbd>M</kbd> | 自动处理 |
| Hide | <kbd>⌘</kbd> <kbd>H</kbd> | 自动处理 |
| Full Screen | <kbd>⌘</kbd> <kbd>⌃</kbd> <kbd>F</kbd> | 自动处理 |
| Select All | <kbd>⌘</kbd> <kbd>A</kbd> | 在文本控件中自动处理 |
| Find | <kbd>⌘</kbd> <kbd>F</kbd> | 绑定到你的搜索/查找功能 |

### PlatformHotkeyConfiguration

Avalonia 会自动把常用热键适配到当前平台。在 macOS 上，复制/粘贴/剪切用的是 Cmd 而非 Ctrl。你可以在运行时通过 `PlatformSettings.HotkeyConfiguration` 查询当前平台的热键映射：

```csharp
protected override void OnKeyDown(KeyEventArgs e)
{
    var hotkeys = this.GetPlatformSettings()?.HotkeyConfiguration;
    if (hotkeys?.Copy.Any(g => g.Matches(e)) == true)
    {
        // Handle copy
    }
}
```

当你编写的自定义控件需要响应平台标准快捷键、又不想把修饰键写死时，这一手很有用。

## 嵌入原生视图 {#embedding-native-views}

借助 `NativeControlHost`，你可以在 Avalonia 控件内承载 macOS 原生视图（NSView 的子类）。当你要集成 Avalonia 没有对应物的平台专属界面组件时（比如地图视图、相机预览或平台媒体播放器），这就派上用场了。

`NativeControlHost` 的做法是在窗口中划出一块区域，让原生视图与 Avalonia 的渲染表面合成在一起。使用时，请写一个平台专属的实现，返回指向原生视图的句柄：

```csharp
public class NativeControlHostExample : NativeControlHost
{
    protected override IPlatformHandle CreateNativeControlCore(
        IPlatformHandle parent)
    {
        if (OperatingSystem.IsMacOS())
        {
            // Create and return a handle to your NSView
            // The view will be hosted within this control's bounds
        }

        return base.CreateNativeControlCore(parent);
    }

    protected override void DestroyNativeControlCore(
        IPlatformHandle control)
    {
        // Clean up native resources
        base.DestroyNativeControlCore(control);
    }
}
```

这样渲染出来的原生视图处在与 Avalonia 渲染相互独立的合成层中，因此它们要么始终在 Avalonia 内容之上、要么始终在其之下，不参与正常视觉树的 z 序。

:::note
嵌入原生视图需要 `net10.0-macos` 目标框架，因为创建原生视图得用到 macOS API。请见上文的[用上完整的 macOS API](#accessing-the-full-macos-api-surface)。
:::

### 把 Avalonia 嵌进原生 macOS 应用 {#embedding-avalonia-in-a-native-macos-app}

反过来也行：把 Avalonia 的渲染表面作为一个 NSView 嵌入你的原生视图层次结构，就能在原生 macOS（Cocoa 或 Mac Catalyst）应用中承载 Avalonia 界面。当你要把既有 macOS 应用逐步迁到 Avalonia，或者只想在一个原生应用的某些视图里用 Avalonia 时，这很有用。

## URL 协议处理程序 {#url-protocol-handlers}

你可以把应用注册为自定义 URL 方案（比如 `myapp://open`）的处理方，这样在浏览器或别的应用里点击链接就能拉起你的应用。请在 `Info.plist` 中加一条 `CFBundleURLTypes` 条目：

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLName</key>
        <string>MyApp</string>
        <key>CFBundleTypeRole</key>
        <string>Viewer</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>myapp</string>
        </array>
    </dict>
</array>
```

配好之后，`myapp://some-action` 这样的 URL 就会打开你的应用了。你可以翻看 `/Applications` 下其他应用的 `Info.plist` 文件，看看它们是怎么配置 URL 方案的。

## 文件类型关联 {#file-type-associations}

你可以把应用注册为特定文件类型的处理方，这样在访达里双击文件就会用你的应用打开。请在 `Info.plist` 中加一条 `CFBundleDocumentTypes` 条目：

```xml
<key>CFBundleDocumentTypes</key>
<array>
    <dict>
        <key>CFBundleTypeName</key>
        <string>Sketch</string>
        <key>CFBundleTypeExtensions</key>
        <array>
            <string>sketch</string>
        </array>
        <key>CFBundleTypeIconFile</key>
        <string>icon.icns</string>
        <key>CFBundleTypeRole</key>
        <string>Viewer</string>
        <key>LSHandlerRank</key>
        <string>Default</string>
    </dict>
</array>
```

| 按键 | 说明 |
|---|---|
| `CFBundleTypeName` | 该文件类型的可读名称。 |
| `CFBundleTypeExtensions` | 要关联的文件扩展名数组（不带前面的点）。 |
| `CFBundleTypeIconFile` | 该类型文件显示的图标。 |
| `CFBundleTypeRole` | 你的应用扮演的角色：`Editor`（可读可写）、`Viewer`（只读）或 `None`。 |
| `LSHandlerRank` | 优先级：`Owner`（该类型由你的应用创建）、`Default`、`Alternate` 或 `None`。 |

## 原生代码 {#native-code}

Avalonia 的 macOS 原生代码位于 `native/Avalonia.Native/src/OSX`。若你需要修改或调试原生层，请在 Xcode 中打开 `Avalonia.Native.OSX.xcodeproj` 项目。

你可以在 Xcode 中用 <kbd>⌘</kbd> <kbd>B</kbd> 编译改动，然后让 Avalonia 应用指向改过的 dylib。在 Xcode 项目导航器的 **Products** 下点击该 dylib 即可找到输出路径，再把它写进你的 `AppBuilder`：

```csharp
.With(new AvaloniaNativePlatformOptions
{
    AvaloniaNativeLibraryPath = "[Path to your dylib]",
})
```

### 开发期间以 app bundle 形式运行 {#running-as-an-app-bundle-during-development}

有些 macOS 功能要求你的应用以规规矩矩的 `.app` 包形式运行。比如不这么做，Xcode 的辅助功能检查器就认不出你的应用。

若不想走完整的打包流程，可以改一改 `.csproj` 里的输出路径，让它长得像个 bundle 结构：

```xml
<OutputPath>bin\$(Configuration)\$(Platform)\MyApp.app/Contents/MacOS</OutputPath>
<AppendTargetFrameworkToOutputPath>false</AppendTargetFrameworkToOutputPath>
<UseAppHost>true</UseAppHost>
```

然后在 `Contents` 目录里放一份有效的 `Info.plist`。关于 `Info.plist` 的细节请见 [macOS 部署指南](/docs/deployment/macos)。

## Mac Catalyst 这条路 {#mac-catalyst-alternative}

Avalonia 也支持借助 Apple 的 Mac Catalyst 框架，让 iOS 应用跑在 macOS 上。这与本页介绍的 Avalonia Native 后端是两条不同的路子。Mac Catalyst 必须在 Mac 上构建，并且依赖 `maccatalyst` .NET 工作负载，于是你会失去从 Windows 或 Linux 交叉编译的能力。它主要适用于重度依赖 UIKit API 的应用，或者要把 Avalonia 嵌进 MAUI 混合应用的场合。对多数 Avalonia 应用而言，上文介绍的默认 macOS 后端才是推荐之选。细节请见 iOS 平台指南中的 [Mac Catalyst](/docs/platform-specific-guides/ios#mac-catalyst)。

## 另请参阅 {#see-also}

- [在 macOS 上部署](/docs/deployment/macos)
- [iOS 平台指南](/docs/platform-specific-guides/ios)（含 Mac Catalyst）
- [NativeMenu 控件参考](/controls/menus/nativemenu)
- [键盘与热键](/docs/input-interaction/keyboard-and-hotkeys)
