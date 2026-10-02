---
id: windows
title: Windows Deployment
description: 了解如何在 Windows 上发布、打包并部署你的 Avalonia XPF 应用，包括自包含构建、单文件发布和安装程序的各种选择。
doc-type: how-to
---

## 发布 {#publishing}

你可以用标准的 .NET CLI 把 XPF 应用发布为 Windows 版本。要做依赖框架的部署（要求目标机器装有 .NET 运行时），运行：

```bash
dotnet publish -r win-x64 -c Release
```

若要把 .NET 运行时一并打进去、让用户不必另行安装，加上 `--self-contained` 标志即可：

```bash
dotnet publish -r win-x64 -c Release --self-contained
```

若面向 ARM64 Windows 设备，请改用 `win-arm64` 运行时标识符：

```bash
dotnet publish -r win-arm64 -c Release --self-contained
```

## 单文件发布 {#single-file-publishing}

XPF 在 Windows 上支持单文件发布，可把应用及其依赖打成一个可执行文件。请在项目文件中加上下列属性：

```xml
<PropertyGroup>
    <PublishSingleFile>true</PublishSingleFile>
    <SelfContained>true</SelfContained>
    <RuntimeIdentifier>win-x64</RuntimeIdentifier>
</PropertyGroup>
```

:::caution
采用单文件发布时，`Assembly.GetEntryAssembly().Location` 返回空字符串，请改用 `AppDomain.CurrentDomain.BaseDirectory` 来获取应用目录。
:::

## ReadyToRun 编译 {#readytorun-compilation}

你可以启用 ReadyToRun（R2R）预先编译来缩短应用启动时间。在项目文件中加上这条属性：

```xml
<PropertyGroup>
    <PublishReadyToRun>true</PublishReadyToRun>
</PropertyGroup>
```

ReadyToRun 会把托管程序集预先编译成本机代码，启动时 JIT 的活儿就少了；代价是发布输出体积更大。

更多细节请见[性能优化](/xpf/configuration/performance#reducing-startup-time-with-readytorun)。

## 承载 WinForms {#winforms-hosting}

若你的应用中承载了 WinForms 控件，请在项目文件里加一个按 Windows 条件生效的属性组，并在其中加上下列属性：

```xml
<PropertyGroup Condition="$([MSBuild]::IsOSPlatform('Windows'))">
    <XpfUseMicrosoftWindowsForms>true</XpfUseMicrosoftWindowsForms>
</PropertyGroup>
```

把 `XpfUseMicrosoftWindowsForms` 设为 `true` 会关掉 WinForms 的 shim 层，改用原生的 WinForms 集成。该选项只在 Windows 上可用，所以条件判断必不可少。

## STA 线程 {#sta-threading}

有些 Windows API（尤其是剪贴板操作和 COM 互操作）要求主线程采用单线程单元（STA）模型。若你遇到消息为 “CoInitialize was not called” 的 `COMException`，请确认你的入口点带有 `[STAThread]` 特性：

```csharp
[STAThread]
public static void Main(string[] args)
{
    // Your application startup code
}
```

若采用[自定义初始化](/xpf/configuration/customizing-initialization)，STA 线程由 XPF SDK 自动处理。

## Windows 安装程序 {#windows-installers}

发布出来的 XPF 应用就是一个标准 .NET 应用，因此你可以用任何 Windows 安装技术来打包。常见的选择有：

- **MSIX**：现代的 Windows 打包格式，支持自动更新、干净地安装与卸载。
- **WiX Toolset**：开源的安装包编写框架，可生成 MSI 和 MSIX 包。
- **Inno Setup**：面向 Windows 应用、免费且用者众多的安装包制作工具。
- **NSIS**：可脚本化的安装系统，插件生态相当丰富。

## 另请参阅 {#see-also}

- [macOS Deployment](/xpf/deployment/macos)
- [Linux Deployment](/xpf/deployment/linux)
- [Customizing Initialization](/xpf/configuration/customizing-initialization)
- [Performance Optimization](/xpf/configuration/performance)
