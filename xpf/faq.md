---
id: faq
title: Frequently Asked Questions
---

## .NET 版本兼容性 {#net-version-compatibility}

**XPF 支持哪些 .NET 版本？**

XPF 支持 .NET 6、7、8、9 和 10，并不要求你必须用某个特定版本。

**较新 .NET 版本里的 WPF 新特性能用吗？**

XPF 是从 .NET 6 的 WPF 分叉出来的。此后 .NET 新版本给 WPF 添的特性（比如 .NET 9 的 Fluent 主题）不会自动出现在 XPF 中。不过 XPF 团队会择要回移一部分，例如 `OpenFolderDialog`（.NET 8 WPF 引入）在 XPF 中就能用。

## 目标框架 {#target-frameworks}

**我该用 `net8.0` 还是 `net8.0-windows`？**

用 `net8.0-windows`（或者你偏好的任何带 `-windows` 后缀的 .NET 版本）。XPF SDK 让这个目标框架在所有平台上都能用，因此为 Linux 或 macOS 构建时也不必改动它。许多第三方库（比如 DevExpress）编译时就要求 Windows 专属的 TFM。

你也可以用不带后缀的 `net8.0` TFM，但前提是解决方案中所有项目都用 XPF SDK 而非 `Microsoft.NET.Sdk`。另外，`<EnableWindowsTargeting>` 没法与不带后缀的 TFM 搭配。

**能针对不同平台使用不同的目标框架吗？**

可以。若你需要平台专属 API，完全可以多目标（例如 `net8.0-windows;net8.0-macos`）。不过对多数 XPF 应用而言，单用一个 `net8.0-windows` TFM 加 XPF SDK 是最省事的做法。

## Win32 API shim {#win32-api-shims}

**我需要启用 Win32 API shim 吗？**

若你的应用用了内部会调用 Win32 API 的第三方控件，那就需要。DevExpress、Actipro、Syncfusion、Telerik 等主流 WPF 控件厂商的产品大多如此。

**怎么判断自己需不需要？**

若你的应用在 Windows 上一切正常，到了 Linux 或 macOS 上却报 `DllNotFoundException: Unable to load shared library 'user32.dll'` 之类的错，那就得启用 Win32 API shim。把下面的内容加进你的 `App` 构造函数或 `Program.Main` 中：

```csharp
AvaloniaUI.Xpf.WinApiShim.WinApiShimSetup.AutoEnable();
```

细节（包括如何排除特定程序集）请见 [Win32 API shim](/xpf/third-party/win32-api-shims)。

**在 Windows 上也需要启用 shim 吗？**

在 Windows 上启用 shim 会把 Win32 调用改走 shim 层而非原生 Win32。这通常是安全的，还能让开发期间各平台的行为保持一致。不过，若你只在 Windows 上部署，那就不需要它。

## Licensing

**许可证是靠什么来认定我的应用的？**

XPF 在运行时校验两个标识：

1. **Assembly Name**: `Assembly.GetEntryAssembly().GetName().Name`
2. **进程可执行文件名**：运行中进程的名称

两者都必须与许可证登记的值一致。

**同一个许可证能用于多个应用吗？**

每个许可证只覆盖一个应用（以程序集名和进程名认定），不同应用需要各自的许可证。

**许可证到期后会怎样？**

XPF 许可证是永久的，你的应用会一直正常运行。许可证过期只意味着你不再获得更新和工程支持，已部署的应用不受影响。

**怎么开始试用？**

Internal 和 Business 许可证可在 [Avalonia 官网](https://avaloniaui.net/xpf)申请 30 天免费试用，你随时都能在门户中开启新的试用。Enterprise 许可证请联系销售。

## 平台支持 {#platform-support}

**XPF 支持 Android 和 iOS 吗？**

Android 和 iOS 支持随 Enterprise 许可证提供，目前处于私有预览阶段。配置说明请见[移动端与浏览器](/xpf/platforms/mobile-and-browser)。

**XPF 支持 WebAssembly 吗？**

WebAssembly 支持随 Enterprise 许可证提供，目前处于私有预览阶段。配置说明请见[移动端与浏览器](/xpf/platforms/mobile-and-browser)。

**支持哪些 Linux 发行版？**

所有 XPF 许可证都支持一级（Tier 1）Linux 发行版（Ubuntu、Fedora 和 Debian 的最新版本）。Enterprise 许可证另外涵盖二级发行版，经协商还可覆盖三级。完整的分级明细请见[支持的平台](/docs/supported-platforms#desktop-linux)。

**XPF 支持 RHEL（Red Hat Enterprise Linux）吗？**

支持。RHEL 8 及以上都可以，只是比 Ubuntu 多几步配置。RHEL 专属的软件包安装说明请见 [Linux：其他依赖](/xpf/platforms/linux#other-dependencies)。

## Native AOT

**XPF 支持 Native AOT 吗？**

支持。WPF 因为依赖 COM 封送而无法用 Native AOT 编译，XPF 则不同，它支持 AOT 编译。

配置与使用说明请见 [Native AOT 部署指南](/xpf/deployment/native-aot)。

## 分配席位 {#seat-assignment}

若要把订阅席位分配给组织成员，请前往 [Avalonia 门户](https://portal.avaloniaui.net/)。

细节请见[分配席位](/tools/assigning-seats)。

## 常见问题 {#common-issues}

**我的应用在 Windows 上好好的，到 macOS/Linux 就崩，该从哪儿查起？**

1. 看看是不是需要 [Win32 API shim](/xpf/third-party/win32-api-shims)（留意 `DllNotFoundException` 之类的错误）
2. 确认 [Linux 依赖](/xpf/platforms/linux#other-dependencies)都装齐了
3. 到[排查问题](/xpf/troubleshooting)页中找你遇到的具体报错
4. 启用 [XPF 日志](/xpf/troubleshooting#listening-for-xpf-logs)以获得更详尽的诊断信息

**`Assembly.GetEntryAssembly().Location` 为什么返回 null？**

这是 .NET 5+ 对单文件发布应用的既定行为，与 XPF 无关。请改用 `AppDomain.CurrentDomain.BaseDirectory`。

**为什么同样的字体在 Windows 和 Linux 上渲染得不一样？**

Windows 和 Linux 用的文本渲染后端不同，有些视觉差异在所难免。请确认自定义字体已作为资源嵌进你的 `.csproj`，且 XAML 中的字体族名与字体文件里的内部名称一致。配置细节请见[快速上手：字体](/xpf/getting-started#fonts)。

**在 macOS 上怎么取得渲染缩放（DPI）？**

WPF 的 `VisualTreeHelper.GetDpi()` API 在 macOS 上未必给得出准确值，请改用 Avalonia 的互操作 API：

```csharp
using Atlantis;

var topLevel = XpfWpfAbstraction.GetAvaloniaTopLevelForWindow(myWpfWindow);
double scaling = topLevel.RenderScaling;
```

**能用 Visual Studio 发布我的 XPF 应用吗？**

强烈建议从命令行发布（`dotnet publish`）。用 Visual Studio 发布可能产出不完整的输出，缺掉 `libSkiaSharp` 这类原生库。正确的发布命令请见各平台的部署指南。

**排查问题时怎么启用 XPF 日志？**

启动应用之前设置这几个环境变量：
- `XPF_LOG_OUTPUT`：`console`、`trace` 或 `file=/path/to/log.txt`（与 `;` 搭配使用）
- `XPF_LOG_LEVEL`: `Verbose`, `Debug`, `Information`, `Warning`, `Error`, or `Fatal`

细节请见[排查问题：收听 XPF 日志](/xpf/troubleshooting#listening-for-xpf-logs)。

**XPF 该配哪个网页浏览器控件？**

这要看你面向哪些平台。CefSharp、NativeWebView、NativeWebDialog 和 DotNetBrowser 的横向对比请见[嵌入网页内容](/xpf/interop/web-content)。
