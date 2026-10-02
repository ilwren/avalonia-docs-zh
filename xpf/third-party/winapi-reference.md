---
id: winapi-reference
title: WinAPI Shim Reference
---

本页列出可经由 XPF shim 层使用的 Win32 API。这些 shim 的用意是让第三方 WPF 控件在非 Windows 平台上跑得起来，它并非通用的 Win32 模拟层。

配置方法请见 [Win32 API shim](/xpf/third-party/win32-api-shims)。

:::note
“已 shim”的意思是 XPF 会拦下该调用并给出跨平台实现，其行为未必在所有情形下都与原生 Win32 分毫不差。标有 (W) 的函数同时提供 ANSI 和 Unicode 两种变体。
:::

## user32.dll

### 窗口的创建与生命周期 {#window-creation-and-lifecycle}

| 功能 | 说明 |
|---|---|
| `CreateWindowEx` (W) | 创建带扩展样式的窗口，返回一个由 XPF 管理的虚拟 HWND。 |
| `RegisterClass` | 注册窗口类。 |
| `RegisterClassExW` | 注册窗口类（扩展版）。 |
| `DestroyWindow` | 销毁用 `CreateWindowEx` 创建的窗口。 |

### 窗口属性与状态 {#window-properties-and-state}

| 功能 | 说明 |
|---|---|
| `GetWindowRect` | 获取窗口在屏幕坐标系中的外接矩形。 |
| `GetClientRect` | 获取客户区矩形。 |
| `GetWindowPlacement` | 获取窗口的显示状态和位置。 |
| `GetWindowInfo` | 获取窗口信息，包括样式和边框。 |
| `IsWindow` | 判断某个句柄是否为有效窗口。 |
| `IsWindowEnabled` | 判断窗口是否接受用户输入。 |
| `IsWindowVisible` | 判断窗口是否可见。 |
| `GetWindowLong` / `SetWindowLong` | 读写窗口数据中的一个 32 位值。 |
| `GetWindowLongPtr` (W) / `SetWindowLongPtr` | 读写窗口数据中一个指针大小的值，用于窗口样式和窗口过程。 |

### 窗口位置与布局 {#window-position-and-layout}

| 功能 | 说明 |
|---|---|
| `SetWindowPos` | 设置窗口的大小、位置和 Z 序。 |
| `AdjustWindowRectEx` | 按给定的客户区尺寸算出所需的窗口尺寸。 |
| `BeginDeferWindowPos` / `EndDeferWindowPos` | 把多次窗口位置变更批量处理，以提升性能。 |

### 窗口层级 {#window-hierarchy}

| 功能 | 说明 |
|---|---|
| `GetActiveWindow` | 返回调用线程上的活动窗口。 |
| `GetTopWindow` | 返回最顶层的子窗口。 |
| `GetWindow` | 取得相关联的窗口（下一个、上一个、所有者、子窗口）。 |
| `GetDesktopWindow` | 返回桌面窗口的句柄。 |
| `FindWindow` | 按类名或标题查找顶层窗口。 |
| `WindowFromPoint` | 返回位于指定屏幕坐标处的窗口。 |
| `EnumChildWindows` | 枚举某个父窗口的子窗口。 |
| `EnumThreadWindows` | 枚举某个线程拥有的窗口。 |

### 窗口显示 {#window-display}

| 功能 | 说明 |
|---|---|
| `SetWindowRgn` | 设置窗口的可见区域。 |
| `RedrawWindow` | 重绘窗口或某个区域。 |
| `InvalidateRect` | 把某个矩形标记为需要重绘。 |
| `SetWindowDisplayAffinity` | 控制窗口能否被屏幕捕获工具录到。目前是空实现。 |

### 系统菜单 {#system-menu}

| 功能 | 说明 |
|---|---|
| `GetSystemMenu` | 返回窗口系统菜单的句柄（即点击窗口图标时弹出的那个菜单）。 |

### 焦点与输入 {#focus-and-input}

| 功能 | 说明 |
|---|---|
| `GetFocus` | 返回持有键盘焦点的窗口。 |
| `SetForegroundWindow` | 把窗口带到前台并让它获得焦点。 |
| `GetCapture` / `ReleaseCapture` | 捕获或释放鼠标。 |
| `GetKeyState` | 返回某个虚拟键的状态（抬起、按下、切换）。 |
| `GetCursorPos` | 返回光标在屏幕坐标系中的位置。 |
| `GetMessagePos` / `GetMessageTime` | 返回光标位置以及最后一条消息的时间。 |

### Messages

| 功能 | 说明 |
|---|---|
| `SendMessage` | 向窗口发送消息并等待处理完成。消息支持有限。 |
| `PostMessage` | 把消息投递到窗口的消息队列。消息支持有限。 |
| `DefWindowProc` (W) | 为窗口过程未处理的消息提供默认处理。 |
| `FormatMessageW` | 把系统错误码格式化成消息字符串。 |

### Hooks

| 功能 | 说明 |
|---|---|
| `SetWindowsHookEx` | 安装钩子过程。支持的钩子类型有限。 |
| `UnhookWindowsHookEx` | 卸载钩子过程。 |

### Caret

| 功能 | 说明 |
|---|---|
| `CreateCaret` | 为窗口创建插入符（文本光标）。 |
| `ShowCaret` / `HideCaret` | 显示或隐藏插入符。 |
| `DestroyCaret` | 销毁当前插入符。 |
| `SetCaretPos` | 设置插入符的位置。 |

### Menus

| 功能 | 说明 |
|---|---|
| `TrackPopupMenuEx` | 在指定位置显示快捷菜单。 |
| `EnableMenuItem` | 启用、禁用或灰显某个菜单项。 |

### 系统信息 {#system-information}

| 功能 | 说明 |
|---|---|
| `GetSysColor` | 返回某个显示元素（按钮面、窗口背景等）的当前颜色。 |
| `SystemParametersInfo` (W) | 读写系统级参数（滚动条尺寸、动画设置等）。 |
| `GetDoubleClickTime` | 返回判定为双击的两次点击之间的最大间隔。 |
| `GetSystemMetrics` | 返回系统度量值（屏幕尺寸、图标尺寸、滚动条尺寸等）。 |
| `GetCaretBlinkTime` | 返回插入符的闪烁间隔。 |

### Clipboard

| 功能 | 说明 |
|---|---|
| `AddClipboardFormatListener` | 注册窗口以接收剪贴板变更通知。 |

## gdi32.dll

### 设备上下文 {#device-contexts}

| 功能 | 说明 |
|---|---|
| `GetDC` / `ReleaseDC` | 获取或释放窗口的设备上下文。 |
| `CreateCompatibleDC` / `DeleteDC` | 创建或删除内存设备上下文。 |
| `GetDeviceCaps` | 返回设备能力信息（DPI、色深等）。 |

### 绘图对象 {#drawing-objects}

| 功能 | 说明 |
|---|---|
| `CreateRectRgn` | 创建矩形区域。 |
| `CreateRoundRectRgn` | 创建圆角矩形区域。 |
| `CreateRectRgnIndirect` | 根据 RECT 结构创建矩形区域。 |
| `DeleteObject` | 删除 GDI 对象（区域、画刷、画笔等）。 |
| `GetStockObject` | 返回预定义库存对象的句柄。 |

### 坐标映射 {#coordinate-mapping}

| 功能 | 说明 |
|---|---|
| `GetMapMode` / `SetMapMode` | 读写设备上下文的映射模式。 |
| `SetWindowExtEx` / `SetViewportExtEx` | 设置坐标映射所用的窗口范围或视口范围。 |
| `OffsetRect` | 按指定偏移量平移矩形。 |

## dwmapi.dll

| 功能 | 说明 |
|---|---|
| `DwmIsCompositionEnabled` | 返回桌面合成是否已启用。在非 Windows 上始终返回 true。 |
| `DwmExtendFrameIntoClientArea` | 把窗口边框延伸进客户区。 |
| `DwmGetWindowAttribute` | 获取 DWM 窗口属性。支持的属性有限。 |
| `DwmSetWindowAttribute` | 设置 DWM 窗口属性。支持的属性有限。 |

## shcore.dll / Monitor APIs

| 功能 | 说明 |
|---|---|
| `MonitorFromPoint` | 返回包含指定点的显示器。 |
| `MonitorFromRect` | 返回与指定矩形交叠面积最大的显示器。 |
| `MonitorFromWindow` | 返回容纳窗口面积最大的那台显示器。 |
| `GetMonitorInfo` | 返回某台显示器的显示区域和工作区。 |
| `EnumDisplayMonitors` | 枚举显示器。 |
| `GetDpiForMonitor` | 返回某台显示器的 DPI。 |
| `GetDpiForWindow` | 返回某个窗口的 DPI。 |
| `GetProcessDpiAwareness` | 返回某个进程的 DPI 感知设置。 |

## imm32.dll (Input Method Editor)

| 功能 | 说明 |
|---|---|
| `ImmCreateContext` / `ImmDestroyContext` | 创建或销毁 IME 输入上下文。 |
| `ImmGetContext` / `ImmReleaseContext` | 获取或释放窗口的 IME 上下文。 |
| `ImmAssociateContext` | 把 IME 上下文关联到某个窗口。 |
| `ImmSetOpenStatus` / `ImmGetOpenStatus` | 打开或关闭 IME，或查询其当前状态。 |
| `ImmNotifyIME` | 向 IME 发送通知。 |
| `ImmGetProperty` | 返回 IME 的属性。 |
| `ImmGetCompositionString` (W) | 返回组字字符串（正在输入组合中的文本）。 |
| `ImmSetCompositionFont` (W) | 设置显示组字字符串所用的字体。 |
| `ImmConfigureIMEW` | 打开 IME 配置对话框。 |
| `ImmSetCompositionWindow` | 设置组字窗口的位置。 |
| `ImmSetCandidateWindow` | 设置候选词列表窗口的位置。 |
| `ImmGetDefaultIMEWnd` | 返回默认 IME 窗口的句柄。 |

## kernel32.dll

| 功能 | 说明 |
|---|---|
| `GetCurrentThreadId` | 返回调用线程的 ID。 |
| `GetModuleFileName` | 返回已加载模块的完整路径。 |
| `GetModuleHandle` (W) | 按名称返回已加载模块的句柄。 |
| `LoadLibrary` (W) | 加载 DLL。该调用会被 shim 拦下，以便重定向 Win32 DLL 的加载。 |
| `LoadString` (W) | 从可执行文件中加载字符串资源。 |
| `CloseHandle` | 关闭对象句柄。 |
| `RtlGetVersion` | 返回操作系统版本。在非 Windows 上返回模拟出的 Windows 版本信息。 |

### 文件与内存映射 {#file-and-memory-mapping}

| 功能 | 说明 |
|---|---|
| `CreateFileMapping` | 创建或打开文件映射对象。 |
| `MapViewOfFile` / `UnmapViewOfFile` | 把文件映射的某个视图映射进进程地址空间，或解除映射。 |
| `FindFirstFile` / `FindNextFile` / `FindClose` | 枚举目录中的文件。 |

### Memory

| 功能 | 说明 |
|---|---|
| `RtlMoveMemory` | 复制一块内存。 |

## shell32.dll

| 功能 | 说明 |
|---|---|
| `SHGetFileInfo` (W) | 返回文件的相关信息（图标、显示名、类型）。 |
| `ExtractIconEx` (W) | 从可执行文件或 DLL 中提取图标。 |

## uxtheme.dll

| 功能 | 说明 |
|---|---|
| `IsThemeActive` | 返回视觉样式当前是否生效。 |
| `SetWindowThemeAttribute` | 设置窗口的主题特性。 |

## msctf.dll

| 功能 | 说明 |
|---|---|
| `TF_CreateThreadMgr` | 创建文本服务框架（TSF）线程管理器。 |
