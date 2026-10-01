---
id: windows
title: Windows 问题
sidebar_label: Windows
description: 排查 Windows 专属的 Avalonia 问题，包括签名、渲染、缩放以及深色主题下的标题栏。
doc-type: troubleshooting
---

## 打包与签名 {#packaging-and-signing}

#### 明明签过名，SmartScreen 还是弹警告 {#signed-executable-still-triggers-smartscreen-warnings}

对新证书和新应用来说这很正常。不同类型的证书，建立信任所需的时间也不同：

- **EV 证书和 Microsoft Trusted Signing**：立刻不受 SmartScreen 拦截。
- **OV 证书**：需要慢慢积累声誉（通常要持续分发 3 到 6 个月）。

想让 OV 证书的声誉积累得快些：

1. 把签过名的应用提交给 [Microsoft Intelligent Security Graph（ISG）](https://www.microsoft.com/en-us/wdsi/filesubmission)分析。
2. 通过知名的下载渠道分发你的应用，好让 Windows Defender 的遥测数据帮你建立信任。
3. 确保每个版本都用同一张证书签名——换证书会让声誉清零。

若过了几个月 SmartScreen 仍然拦着你的应用，请确认证书链完整，且签名时时间戳服务器是通的。证书链不完整或缺时间戳，都会让声誉攒不起来。

#### Azure 认证失败 {#azure-authentication-failures}

若通过 Azure Trusted Signing 签名时报认证错误：

1. 确认下列环境变量设置无误：`AZURE_TENANT_ID`、`AZURE_CLIENT_ID`、`AZURE_CLIENT_SECRET`。
2. 确认该服务主体在 Azure 门户中已被赋予 **Trusted Signing Certificate Profile Signer** 角色。
3. 确认你的 Azure Trusted Signing 账户和证书配置文件处在同一个区域。
4. 若你用的是托管标识而非服务主体，请确认承载环境（比如 Azure DevOps 或 GitHub Actions）支持它，且标识已正确关联。
5. 另一个办法是安装 [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest) 并走 [az login](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest#az-login) 流程做交互式认证，以此排除凭据方面的问题。

## Rendering

#### 应用窗口一片空白或全黑 {#application-shows-a-blank-or-black-window}

若应用窗口出来了却看不到任何内容：

1. 先看看你是不是跑在远程桌面会话里，或是没有 GPU 直通的虚拟机上。这类环境下 Avalonia 会退回软件渲染，但某些配置仍可能失败。
2. 强制走软件渲染，确认问题是不是出在 GPU 上。在构建应用之前，把下面的内容加进你的 `Program.cs`：

```csharp
AppBuilder.Configure<App>()
    .UsePlatformDetect()
    .With(new Win32PlatformOptions
    {
        RenderingMode = new[]
        {
            Win32RenderingMode.Software
        }
    })
    .StartWithClassicDesktopLifetime(args);
```

3. 更新显卡驱动。驱动过旧或有缺陷，是 Windows 上渲染失败最常见的原因。

#### 调整窗口大小时闪烁或出现画面残影 {#flickering-or-visual-artifacts-during-window-resize}

改窗口大小时闪烁，是 Win32 窗口模型的已知局限。想减轻它：

- 在顶层 `Window` 上设置 `Background`，让清屏颜色与应用主题一致，闪烁就不那么扎眼了。
- 避免因调整大小而触发繁重的布局重算。尽量用 `LayoutTransformControl` 或固定尺寸的内层面板。

## 高 DPI 与缩放 {#high-dpi-and-scaling}

#### 控件在高 DPI 显示器上显得过小或过大 {#controls-appear-too-small-or-too-large-on-high-dpi-displays}

Avalonia 在 Windows 上遵循每显示器的 DPI 设置。若应用渲染出的缩放比例不对劲：

1. 确认你的应用清单没有覆盖 DPI 感知设置。若你有 `app.manifest` 文件，请确保它声明的是每显示器 DPI 感知（或者干脆删掉所有 DPI 相关条目，交给 Avalonia 自己处理）。
2. 到**设置 > 显示 > 缩放与布局**查看显示缩放百分比，Avalonia 本应自动与之一致。
3. 若你把 Avalonia 嵌在 WPF 或 WinForms 宿主里，那么宿主应用的 DPI 感知模式说了算。请确认宿主配置为 per-monitor V2 感知。

#### 位图或图片资产显得模糊 {#bitmap-or-image-assets-appear-blurry}

若图片在高 DPI 屏幕上发虚，请为资产提供多种分辨率的版本，Avalonia 会按当前 DPI 挑最合适的那个。把缩放版本与基准资产放在一起即可：

```text
/Assets/logo.png        (1x, base)
/Assets/logo@2x.png     (2x, for 200% scaling)
```

## 主题与外观 {#theme-and-appearance}

#### Windows 10 上切到深色主题后标题栏仍是浅色 {#title-bar-stays-light-when-switching-to-dark-theme-on-windows-10}

在 Windows 10 上，原生标题栏不会自动跟随应用的 `RequestedThemeVariant`。这是平台限制：Windows 10 没有提供让标题栏变暗的官方 API。在 Windows 11 上，Avalonia 会自动处理好。

若你在 Windows 10 上确实需要深色标题栏，有两条路可走：

- **自己画标题栏。**设置 `ExtendClientAreaToDecorationsHint="True"` 和 `WindowDecorations="None"`，自绘标题栏，主题完全由你掌控。细节请见[自定义标题栏](/docs/platform-specific-guides/windows#custom-title-bars)。
- **用未公开的 DWM API。**通过 P/Invoke 调用 `DwmSetWindowAttribute`，传入 `DWMWA_USE_IMMERSIVE_DARK_MODE`（属性 20）。它在 Windows 10 内部版本 18985 及以上可用，但毕竟未公开，日后的 Windows 更新中可能变卦。

```csharp
using System.Runtime.InteropServices;
using Avalonia;

[DllImport("dwmapi.dll", PreserveSig = true)]
private static extern int DwmSetWindowAttribute(
    IntPtr hwnd, int attr, ref int value, int size);

private void SetDarkTitleBar(Window window, bool isDark)
{
    if (!OperatingSystem.IsWindows()) return;

    var handle = window.TryGetPlatformHandle()?.Handle;
    if (handle is null) return;

    int value = isDark ? 1 : 0;
    // Attribute 20: DWMWA_USE_IMMERSIVE_DARK_MODE
    DwmSetWindowAttribute(handle.Value, 20, ref value, sizeof(int));
}
```

请在窗口打开之后、以及每次主题变化时调用该方法（订阅 `ActualThemeVariantChanged`）。

## 窗口行为 {#window-behavior}

#### 窗口位置或大小没能正确恢复 {#window-position-or-size-not-restored-correctly}

若你会跨会话保存并恢复窗口边界，要留心显示器配置可能已经变了。套用之前，务必先用 `Screens.All` 对照当前的屏幕布局校验一下坐标——窗口若落到了屏幕之外，用户可就看不见了。

#### 无边框或自定义外壳的窗口在任务栏上没有图标 {#taskbar-icon-missing-for-borderless-or-custom-chrome-windows}

若你的窗口用了 `WindowDecorations="None"` 或自定义标题栏却不出现在任务栏上，请先确认你没有无意间设了 `ShowInTaskbar="False"`。Win32 套用的某些扩展窗口样式也会把任务栏项抹掉。多数情况下，显式设置 `ShowInTaskbar="True"` 就能解决。

## 另请参阅 {#see-also}

- [Windows 平台指南](/docs/platform-specific-guides/windows)——透明度、Mica 与 Win32 集成的细节
- [macOS 问题](/troubleshooting/platform-specific-issues/macos)和 [WebAssembly 问题](/troubleshooting/platform-specific-issues/webassembly)——其他平台的排查指南
- [记录错误与警告](/docs/app-development/logging-errors-and-warnings)——如何从应用中捕获诊断输出
