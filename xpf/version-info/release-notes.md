---
id: release-notes
title: 发行说明
---

## XPF 1.6.7 (2026-09-15)

* Avalonia 版本从 11.3.20 更新到 11.3.22
* 修复光标移出窗口后工具提示不消失的问题（Linux）
* 修复 ShutdownRequested 的取消请求未被遵从的问题（macOS）
* 修复 MessageBox 被置顶窗口挡住的问题
* 修复另一个进程被激活时弹出层不关闭的问题
* 修复使用 Nvidia EGL 驱动时透明窗口显示为黑色的问题
* 实现了堆与全局内存 API 的 shim，以及 GetShortPathName、QueryPerformanceCounter/Frequency、UnregisterClass

## XPF 1.6.6 (2026-08-11)

* Avalonia 版本从 11.3.18 更新到 11.3.20
* 新增对 MahApps 窗口的基本支持
* 修复 `FontManagerOptions.DefaultFamilyName` 未指向系统字体时直接崩溃退出的问题
* 修复 macOS 27 起出现的文本输入时 `OutOfRangeException` 问题
* 修复 `TextBox.TextView` 为 null 时出现 `NullReferenceException` 的问题
* 修复无外壳的最大化窗口上弹出层出现在错误显示器上的问题
* 修复光标移出窗口后工具提示不消失的问题
* 改进了某个窗口关闭后激活另一个窗口的判断逻辑（Linux）
* 下列依赖已更新：
  * System.Security.Cryptography.Xml 从 8.0.3 更新到 8.0.4（修复安全漏洞）

## XPF 1.6.5 (2026-07-02)

* Avalonia 版本从 11.3.16 更新到 11.3.18
* 新增对 DPI 非 96 的位图的支持
* 修复系统字体回退抢占了用 pack URI 引用的字体族的问题
* 修复启用裁剪后 `TextWrapping=Wrap` 把每一行都裁掉的问题
* 修复在非活动窗口中打开上下文菜单需要多点一次的问题（macOS）
* 修复最大化窗口四周留出几像素空隙的问题（macOS、Linux）
* 修复某些鼠标光标取值会导致光标不可见的问题

## XPF 1.6.4 (2026-05-27)

* Avalonia 版本从 11.3.14 更新到 11.3.16
* 修复触控板滚动过于灵敏的问题（macOS 上尤为明显）
  * 可用 `AvaloniaUI.Xpf.DisablePreciseMouseWheelScrolling` 兼容性开关关掉这一改动
* 修复带屏幕外后代元素的 `VisualBrush` 渲染问题
* 修复 scRGB 到 sRGB 的颜色转换，此前会导致颜色略有偏差
* 修复 `TabControl` 中的 `NativeControlHost` 显示内容不对的问题

## XPF 1.6.3 (2026-04-22)

* Avalonia 版本从 11.3.12 更新到 11.3.14
* 新增对流式文档中 section 的支持
* 修复 PNG 解码器在某些情况下用错像素格式的问题
* 修复 macOS 上复制位图时红蓝通道颠倒的问题
* 下列依赖已更新：
  * System.Security.Cryptography.Xml 从 8.0.0 更新到 8.0.3（修复安全漏洞）
  * SixLabors.ImageSharp 从 3.1.9 更新到 3.1.12（修复安全漏洞）

## XPF 1.6.2 (2026-03-20)

* 修复 macOS 上剪贴板为空时右键点击 TextBox 导致崩溃的问题
* 修复从弹出层自身的按钮关闭它时需要多点一次的问题（macOS、Linux）
* 修复点击 ComboBox 内滚动条的问题 
* 修复点击已展开子菜单的菜单项的问题
* 修复在 Menu 中打开 ComboBox 的问题
* 修复项数众多的菜单占地过大、盖住父元素的问题

## XPF 1.6.1 (2026-02-19)

* Avalonia 版本从 11.3.11 更新到 11.3.12
* 支持从剪贴板粘贴 macOS 的位图格式
* 修复 AvaloniaHost 吞掉所有输入的问题
* 修复在 TabControl 中切换标签页后吞掉所有输入的问题
* 修复 WinForms 对话框在没有 FilterIndex 时崩溃的问题
* [无障碍] 支持 ItemType 和 ItemStatus 属性
* [无障碍] 修复添加子元素时不发出通知的问题
* 实现了 BringWindowToTop、DestroyWindow、IsChild、SetActiveWindow、SetFocus 这几个 API shim

已知问题：

* 从弹出层自身的按钮关闭它时可能需要多点一次（macOS、Linux）

## XPF 1.6.0 (2026-01-19)

* Avalonia 版本从 11.3.1 更新到 11.3.11
* 下列方面做了较大改动：
  * 鼠标捕获与捕获丢失
  * 剪贴板（位图支持、自定义格式、往返一致性）
* 新增对 macOS 上 Ctrl+点击的支持，并把 F10 作为系统键
* 新增对 System.Windows.Documents.Typography 属性的支持
* 新增文件对话框中筛选器索引的支持
* 弹出层相关修复（定位、显示对话框时被禁用）
* MessageBox 的行为向 Windows 看齐（标题、最大尺寸）
* 文本方面的修复与改进（行距、内联块、字体加载与匹配）
* 自动化方面的修复与改进
* DPI 与缩放方面的修复与改进
* 所有日志 sink 现已开放

已知问题：
* 在 TabControl 中切换标签页不会使 UIA 树失效
* AvaloniaHost 一旦获得焦点就吞掉所有输入
* 从弹出层自身的按钮关闭它时可能需要多点一次

## XPF 1.5.3 (2025-06-23)

* 修复 MediaContext，改用 Stopwatch 而非系统时钟
* Adjust WinForms MessageBoxTheme
* Enforce WPF LineSpacing

## XPF 1.5.2 (2025-06-09)

* 把 MessageBox 的宽度限制在 400px，以贴近 WIN32 的表现
* 把 MessageBox 限制在当前屏幕高度的 80% 以内
* 把 Avalonia 更新到稳定版 11.3.1

## XPF 1.5.1 (2025-05-21)

* 把 VB MsgBox 的默认标题改得与 Windows 一致

## XPF 1.5.0 (2025-05-07)

* 对溢出的 AVTextLine 应用 TextAlignment
* BmpBitmapDecoderHandle——支持 1 位 BMP
* 修复 Window.Closing 事件在某些情况下不触发的问题
* 修复 ImageBrush 用作不透明度蒙版时失效的问题
* 修复径向渐变和虚线数组的渲染
* 修复对话框的隐藏/显示。
* 对话框隐藏时把对话框任务置为完成
* 用裁剪边界约束子树的内容边界
* 修复文件对话框在未指定文件名时崩溃的问题
* 确保绘制圆角矩形时半径取值有效
* 菜单捕获问题的另一种修复方案
* 没有主显示器时改用第一台显示器
* 修复 AvalonEdit 补全窗口崩溃的问题
* 新增对 FontFamily.FamilyTypefaces 的支持
* 实现了 SetCursorPos API shim
* 改善位图性能
* 改为通过 BeginInvokeOnRender 调用 MediaContext 的更新处理程序
* 去掉 ribbon 控件中的原生调用
* 修复 x86 上的 win32 shim
* 为 APISHIM 调用加上日志
* 处理 file ok 相关逻辑 
* 把 System.IO.Packaging 更新到 6.0.2
* 确保 paragraphWidth 向上取整
* 新增对 VB MsgBox 函数的支持
* 新增对 VB `InputBox` 的支持。
* 修复 RichTextBox 的边框位置
* 修复 XpfContain 从树上分离时崩溃的问题
* 处理 8bpp 位图的情形
* 重做字体加载
* 处理高度为零的 RectangleNode
* Fix Font Metrics Rounding Error
* 修复帧解码的收尾处理
* 修复 PngBitmapDecoder 的 alpha 通道
* 不再让 Font 与 FontFamily 共用同一份 FontMetrics
* 加载字体集合时处理重复字体
* 修复自定义字形的模拟
* 确保本地化的字体字符串能映射到可用的区域性
* 简化解码后位图数据的目标像素格式
* 允许在没有放置目标的情况下显示弹出层。
* 新增对索引色位图源的支持
* Implement OpenFolderDialog
* 不再在 `Popup` 中调用 win32 的 `GetCursorPos`。

## XPF 1.4.0 (2025-01-08) 

* 移除 System.Configuration.ConfigurationManager 的使用
* 修复 ModifierKeys.MacControl 的取值
* 把 WebRequest/WebResponse 的基类构造函数调用换成 RuntimeHelpers.GetUninitializedObject，并修复 Frame 控件若干问题
* 修复按键重映射抛异常的问题
* 失去焦点时重置修饰键状态
* 简单的 3D 支持
* Fix Paragraph TextAlignment
* 修复 MuceViewport3DVisual 中的编译错误
* Add GetAvaloniaTopLevelForWindow
* 为浏览器这类单视图平台提供窗口边框
* 单视图窗口可调整大小，并修复窗口装饰
* 实现在线授权票据
* 把其余平台也纳入许可证校验
* 修复 avalon dock 调整大小的问题
* 修复右下角的光标
* 替换掉 binary formatter
* Stub ShowSystemMenu
* 修复 DragOver 暴露已释放 IDataObject 的问题
* 路径简化失败时不再崩溃
* 新增 ScreenToClient 的 win32 API shim。
* 修复 XPF 弹出层嵌入 Avalonia 时的问题。
* macOS 上默认改用 OpenGL
* 实现 JpegMetadata，并支持读取方向信息
* 修复 ElementProxy 中的 NRE
* 新增一个运行时开关，用于启用 DataObject 自定义格式的互操作
* 新增对 exif MakerNote 的读写支持
* 修复 “control is not in any visual tree” 的问题
* Fix Cursors.None
* 修复弹出层的内存泄漏
* 窗口失活时释放鼠标捕获。
* Update Avalonia.Licensing
* 确保视觉根的 dpi 被设上
* 修复 BitmapSource 的 4 字节对齐
* 把部分元数据查询规范为小写
* 未显式启用 ALC 支持时沿用 WPF 的默认行为
* 行未折叠时调整 TextLine 的裁剪

## XPF 1.3.0 (2024-08-12)

* 启用基于 ECDSA 的许可证密钥
* 修复多个 Geometry API
* 缓存 FontCollection 并让其支持多线程
* 修复几何图形对无描边线段做命中测试的问题
* 把 main 分支的版本号更新到 1.3
* Implement BlockUIContainer
* 更新 Avalonia 版本
* 修复派发时的异常处理
* 支持把 XPF 加载进独立的 ALC，以此实现简陋版多线程
* 修复 MUCE 几何图形的失效处理
* 修复大图解码
* 修复内联元素的 TextDecorations，并修复 BaselineAlignment
* Fix TextDecorations
* 修复 macOS 上的按键映射
* Fix GetDpiForMonitor
* 实现 F32MonitorHandle 并改用新的 Screens API 
* 对字形运行边界不正确的问题做了临时修复
* 不再把鼠标事件当作触摸处理
* 从对外公开的 Window.Close 方法中调用 InternalClose
* 初步支持生成 PDF
* 矩形几何图形新增圆角半径支持
* 新增对无描边几何线段的支持
* 更新 avalonia：修复 win32 窗口的显示状态
* 更新 avalonia：修复置顶的从属窗口失效的问题
* AvaloniaHostContainer 需要把变换原点设为零，而非默认的 50%50%
* 窗口重新激活时把焦点留在 avalonia host 内
* 添加 AdjustWindowRectEx 的空实现
* 修复保存对话框中文件名设置错误的问题
* Fix Window.Icon
* 修复“按下另一个鼠标键时鼠标事件未正确触发”的问题
* 改为在 MuceVisualBrush 中手动订阅整棵子树的视觉失效
* 修复无头平台，避免把 Skia 写死
* patcher 的小幅改进
* 新增一个开关，用于关掉针对 devexpress 的调用栈微调
* 内容若反正会被裁掉，就跳过渲染
* 改变 MuceRenderData 状态的池化方式
* 修复 FontAwesome.Sharp 的字体加载
* 升级 image sharp
* SHGetFileInfo 的桩实现
* 实现 bitmap.copypixels
* 修复 DrawingImage，并临时修复无父级的 VisualBrush
* 从所有分支发布包
* 为发布标签加上正则 semver 校验
* 更新 dotnet.yml，去掉版本号末尾的反斜杠
* Update Common.props
* 移除 UseWinForms 及若干杂项
* Disable ImportWindowsDesktopTargets
* 允许用户通过 msbuild 属性或环境变量启用日志
* 新增 XpfSingleProject 属性
* Update AvaloniaUI.Xpf.WinApiShim.targets
* 浏览器兼容性方面的改进
* 面向浏览器的实验性 WinAPI shim 支持
* 修复浏览器上的 winapi shim
* 修复浏览器 SDK
* 修复 Screen API 相关的若干 WinAPI shim
* 若干 mono 相关修复
* SystemInformation.MouseWheelScrollDelta support
* 创建新窗口时重置弹出层的 _positionInfo


## XPF 1.2.0 (2024-05-29)

* Update ImageSharp
* 让 DragDrop 处理程序可用于任意 Control，而不限于 TopLevel
* 用虚拟窗口句柄实现 GetActiveWindow
* 让 HwndWrapper 可用
* 忽略来自 avalonia 窗口的 size to content
* 给 XPF 程序集打补丁，使其在 DllImport 时抛出异常
* Update GetSizeFromHwnd
* 把 Avalonia nuget 更新到 11.2 alpha
* 判断是否推迟创建弹出层时，先检查 XpfHost 是否真的挂在了什么东西上
* 修复 ExclusivelyOwnedWindow 实为 null 的情形
* 移植 wpf 的弹出层放置逻辑
* 窗口重新激活时把焦点留在 avalonia host 内
* 让 snoop 在更多情形下可用
* 矩形几何图形新增圆角半径支持
* 创建新窗口时重置弹出层的 _positionInfo
* 针对 Telerik 的 RadTooltipWindow 的修复
* 从 .cur 文件中读取热点坐标
* 内容若反正会被裁掉，就跳过渲染
* 为 WPF 的 Brush.Transform 属性采用绝对变换原点
* 检查焦点时，先看该窗口此前是否被激活过
* 修复 VisualBrush 的回归问题
* 为 Pen 光标类型添加默认位图光标
* 初步支持生成 PDF
* Added SystemInformation.MouseWheelScrollDelta
* 在初始状态下设置窗口位置时抛出 position changed
* 控件获得焦点时激活窗口
* 修复位图编码的若干问题
* 托管拖动期间屏蔽输入
* Implemented BlockUIContainer
* X11——依据控件焦点记录窗口激活是否已完成
* Linux 上设置位置时回退为设置拖动点
* Stub UnhookWindowsHookEx
* 修复 Screen API 相关的若干 WinAPI shim
* 映射更多像素格式
* Actipro 停靠相关修复
* XPF 中不再从 ComboBox 调用 GetCapture
* 为 WriteableBitmap.AddDirtyRect 发送 MILCMD_BITMAP_INVALIDATE
* 为 PDF 文档正确配置 DPI 和页面尺寸元数据
* x11 上不允许调整已最大化窗口的大小
* ManagedWindowDragHelper——记录先前的位置，并在处理 WM_MOVING 时更新位置
* MonitorFromWindow：对未附加的视觉元素不再抛异常
* 修复若干未处理异常
* 修复若干 Geometry 问题
* 新增对无描边几何线段的支持
* 添加 SKColorFilter 的释放回调
* 允许用户通过 msbuild 属性或环境变量启用日志
* XPF 中不再从 MenuBase 调用 GetCapture
* 更新 XpfSkiaExtensions 对 PresentationCore 的引用
* 为 MessageBoxTheme.axaml 添加背景设置
* 鼠标被捕获时屏蔽非客户区输入
* 修复弹出层所用的屏幕工作区
* 修复文本框粘贴时崩溃的问题
* 修复若干停靠相关问题

### 已知问题 {#known-issues}

* Actipro 停靠：拖出面板时，macOS 上不显示预览
* DevExpress 停靠：X11 上有时不显示放置装饰
* Syncfusion 停靠：各平台均有问题
* Telerik 停靠：Windows 上首次拖动/拖出时鼠标不再被识别
