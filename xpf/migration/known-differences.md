---
id: known-differences
title: 与 WPF 的已知差异
---

## 概述 {#overview}

XPF 与 WPF 保持 API 和二进制兼容，但由于渲染引擎不同（用 Skia 而非 MilCore）以及跨平台的需要，行为上仍有一些出入。本页把这些已知差异记录下来，便于你规划迁移。

## Rendering

### 虚线描边与线帽 {#dashed-strokes-and-line-caps}

Skia 渲染带线帽的虚线描边时，与 WPF 的 milcore 引擎有所不同。若你的应用用了 `StrokeDashArray` 并配上自定义线帽（三角、圆头），WPF 和 XPF 下的视觉效果可能略有差异。这是 Skia 渲染后端的固有区别。

### 模糊效果 {#blur-effects}

模糊效果（`BlurEffect`、`DropShadowEffect`）在 Skia 中比 WPF 的硬件加速管线更吃算力。大量使用模糊的应用可能掉帧。缓解办法请见[性能：模糊效果](/xpf/configuration/performance#blur-effects)。

## Controls

### ContextMenu

在 WPF 中，以编程方式打开上下文菜单时会隐式设置 `PlacementTarget`；在 XPF 中，你必须显式设置它：

```csharp
myContextMenu.PlacementTarget = targetElement;
myContextMenu.IsOpen = true;
```

右键上下文菜单的表现与 WPF 完全一致，无需任何改动。

### MessageBox

`System.Windows.MessageBox` 和 `System.Windows.Forms.MessageBox` 都受支持，但渲染出来的样子可能与 Windows 原生消息框不同：

- 文本换行的位置可能不一样（XPF 把宽度限制在约 400px）
- 图标位置可能略有出入
- 按钮样式采用平台的原生外观

### TextBox 的触摸行为 {#textbox-touch-behavior}

在触屏设备上，在 `TextBox` 上拖动手指会让文本跟着滑动。这一行为继承自 WPF。要关掉它：

```csharp
ScrollViewer.SetPanningMode(myTextBox, PanningMode.None);
```

或者在 XAML 中：

```xml
<TextBox ScrollViewer.PanningMode="None" />
```

### FlowDocument

FlowDocument 可用，但有以下限制：
- 不支持分页
- 不支持 floater
- 表格支持有限

完整清单请见[尚未支持的特性](/xpf/version-info/missing-features)。

## 窗口管理 {#window-management}

### 透明窗口 {#transparent-windows}

XPF 用的是 `WS_EX_NOREDIRECTIONBITMAP`，而非 WPF 所用的 `WS_EX_LAYERED`。这意味着：

- 不支持逐像素的命中测试透明。点在窗口透明区域上的鼠标点击不会穿透到下面的窗口。
- 若要做叠加层，请把内容放进同一个窗口，而不是把若干透明窗口摞在一起。OpenGL 的嵌入方式请见[性能：嵌入高性能内容](/xpf/configuration/performance#embedding-high-performance-content)。

### 多个 UI 线程 {#multiple-ui-threads}

WPF 允许在不同的 dispatcher 线程上创建窗口。XPF 在 macOS 上不支持多个 UI 线程（平台本身只允许一个）；在 Windows 和 Linux 上，多 dispatcher 的支持也很有限。那些把启动画面或进度窗口放在另一线程的写法，应当改造成统一走主 dispatcher。

### Window.ShowActivated

自 XPF 1.6.0 起支持 `ShowActivated` 属性。

### 窗口关闭事件 {#window-closing-event}

无论是以编程方式关闭窗口还是点关闭按钮，`Closing` 事件都只触发一次。在更早的 XPF 版本（1.6.0 之前）中，用 `Window.Close()` 时 `Closing` 可能触发两次。

要改写关闭行为，请处理 `Closing` 事件并设置 `e.Cancel = true`：

```csharp
protected override void OnClosing(CancelEventArgs e)
{
    e.Cancel = true; // Prevent close
    Hide();          // Hide instead
}
```

### Win32 窗口消息 {#win32-window-messages}

XPF 的 Win32 API shim 层会生成窗口消息（比如 `WM_ACTIVATEAPP`、`WM_SETFOCUS`），但只覆盖所支持的第三方控件所需的那些。并非所有 Win32 消息都会在所有平台上生成。若你的应用靠特定窗口消息在窗口之间通信，请改用 .NET 的 IPC 机制（比如命名管道或内存映射文件）。

## APIs

### VisualTreeHelper.GetDpi

`VisualTreeHelper.GetDpi()` 在 macOS 上未必给得出准确值，请改用 Avalonia 的互操作 API：

```csharp
using Atlantis;

var topLevel = XpfWpfAbstraction.GetAvaloniaTopLevelForWindow(myWindow);
double scaling = topLevel.RenderScaling;
```

### CursorInteropHelper.Create

`CursorInteropHelper.Create()` 没有完整实现，因为它依赖 Windows 原生的光标句柄。XPF 1.6.0+ 会回退到默认光标。自定义光标映射请见 [Windows：CefSharp](/xpf/platforms/windows#cefsharp)。

### SystemSounds.Beep

`System.Media.SystemSounds.Beep` 在 macOS 和 Linux 上会抛出 `PlatformNotSupportedException`。请给这个 API 的调用加上平台判断，或者在跨平台构建中干脆去掉它。

### System.Drawing.Common

`System.Drawing.Common`（GDI+）在非 Windows 平台上已废弃。依赖 GDI+ 渲染的第三方控件（比如某些 DevExpress 控件）在 macOS 和 Linux 上会抛异常。变通办法请见 [macOS：GDI+ 与 System.Drawing.Common](/xpf/platforms/macos#gdi-and-systemdrawingcommon)。

## 文件对话框 {#file-dialogs}

### FilterIndex

自 XPF 1.6.0 起，针对 `OpenFileDialog` 和 `SaveFileDialog` 的 `FilterIndex` 已完整支持。

### Linux 上的 `InitialDirectory` {#initialdirectory-on-linux}

在较老的 Linux 发行版上，若 GNOME 版本不支持 DBus 文件对话框协议，`InitialDirectory` 可能被忽略。变通办法请见 [Linux：老发行版上的文件对话框](/xpf/platforms/linux#file-dialogs-on-older-distributions)。

### OpenFolderDialog

跨平台选择文件夹请用 `Microsoft.Win32.OpenFolderDialog`。某些第三方的文件夹对话框实现（比如 DevExpress 的 FolderDialog）在 macOS 上可能用不了。

### FolderBrowserDialog (System.Windows.Forms)

XPF 支持 `System.Windows.Forms.FolderBrowserDialog`，但它会映射到平台原生的文件夹选取器。在 Linux 和 macOS 上，对话框的外观和行为都与 Windows 不同。想要表现一致，请优先用 `Microsoft.Win32.OpenFolderDialog`。

### 对话框的迁移套路 {#dialog-migration-patterns}

把 WPF 的对话框代码迁到 XPF 以便跨平台时：

- 尽量把 `System.Windows.Forms.OpenFileDialog` 换成 `Microsoft.Win32.OpenFileDialog`
- 别去设那些没有跨平台对应物的 Windows 专属对话框属性（比如 `DereferenceLinks`）
- 在 macOS 上，避免在窗口激活期间弹出模态对话框。请见 [macOS：启动与模态对话框](/xpf/platforms/macos#startup-and-modal-dialogs)

## Clipboard

剪贴板差异的完整说明请见[剪贴板](/xpf/migration/clipboard)。

## Fonts

- WPF 与 XPF 的字体匹配规则不同，样式名不太规范的字体可能匹配不上。
- 字体回退行为可以定制，请见[快速上手：字体](/xpf/getting-started#fonts)。
- 跨平台渲染在各平台上用的是不同的文本后端，因此视觉上有差异是正常的。
