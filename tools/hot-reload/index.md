---
id: index
title: 热重载
description: 添加 AvaloniaUI.DiagnosticsSupport.HotReload 包，即可把 XAML 和 C# 的改动实时应用到运行中的 Avalonia 应用上。
doc-type: how-to
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
  - hot reload
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

热重载能把对 `.axaml` 和 `.cs` 文件的改动应用到运行中的 Avalonia 应用上，无需重启。`AvaloniaUI.DiagnosticsSupport.HotReload` 包接入了 .NET 热重载管线：你一保存文件，相应的控件、样式、资源和数据模板就会就地重建。

## 热重载会更新什么 {#what-hot-reload-updates}

装上热重载包后，下列改动会实时应用到你运行中的应用上：

| 变更 | 行为 |
| --- | --- |
| 控件（带 `x:Class` 的文件） | 视觉树中已有的实例会就地重建，并尽可能保留原来的位置。 |
| Styles | 应用级和控件级的样式都会重新应用，选择器和 setter 的改动立刻见效。 |
| 资源字典 | 合并字典会被重新加载，依赖它们的内容随之刷新。 |
| 数据模板 | 模板会重新生成，绑定到它们的控件随之刷新。 |
| `{StaticResource}` references | 热重载期间会被改写为 `{DynamicResource}`，因此资源改动无需重启即可传播开来。 |
热重载常见的用武之地有：

- **资源画刷与取值。**在资源字典里改个颜色、画刷或字号，所有引用它的控件都会更新。`{DynamicResource}` 和 `{StaticResource}` 两种引用都能跟上改动，因为静态引用在热重载期间会被改写。
- **数据模板。**改了[数据模板](/docs/data-templates/introduction-to-data-templates)的图标、配色、间距或布局后，所有用到它的控件（包括列表项和内容呈现器）都会按新模板重建。
- **控件标记。**在视图（带 `x:Class` 的文件）中调整布局、增删元素或改文字，运行中的实例会就地重建。
- **样式。**改动应用级或控件级样式中的选择器或 setter，新样式立刻重新应用。
- **代码隐藏。**改 `.axaml.cs` 文件中的事件处理程序或方法体。C# 改动遵循标准的 .NET 热重载规则。

## 前置条件 {#prerequisites}

动手之前，请确认你具备：

1. **Avalonia 12.0 或更高版本。**
2. **含 `AvaloniaUI.DiagnosticsSupport.HotReload` 使用权的有效 Avalonia 许可证密钥。**密钥可在 [Avalonia 客户门户](https://portal.avaloniaui.net/)获取。同一个密钥往往还涵盖 `Charts`、`TreeDataGrid` 等其他需授权的 Avalonia 包。
3. **一个热重载驱动方。**要么是 `dotnet watch` 命令，要么是支持 .NET 热重载的 IDE（比如 Visual Studio）。请见[带热重载运行](#running-with-hot-reload)。

## 快速上手 {#getting-started}

1. 运行 `dotnet add package` 安装 `AvaloniaUI.DiagnosticsSupport.HotReload` NuGet 包。


2. 若不想让热重载混进发布版本，请到 `.csproj` 文件中把热重载包的 `<PackageReference>` 包在 `Debug` 条件里，这样它就绝不会被发布出去。


3. 在可执行项目文件（`.csproj`）中填入你的 Avalonia 许可证密钥。密钥可以在 [Avalonia 门户](https://portal.avaloniaui.net)中获取。


## 带热重载运行 {#running-with-hot-reload}

用支持 .NET 热重载的工具启动你的应用。

<Tabs>
<TabItem value="watch" label="dotnet watch" default>

在平台 head 项目上运行 `dotnet watch`。你一保存，它就会重新构建并应用改动。

```bash
dotnet watch --project YourApp.Desktop
```

这是最靠得住的驱动方式，在各编辑器和各平台上表现一致。

:::note
在移动平台上，`dotnet watch` 需要 .NET 11 或更高版本。
:::

</TabItem>
<TabItem value="vs" label="Visual Studio">

用调试器启动应用（<kbd>F5</kbd>）。每次改完，点工具栏上的 **Apply Code Changes**（热重载按钮），或者在该按钮的下拉菜单中打开 **Hot Reload on File Save**。

</TabItem>
<TabItem value="vscode" label="VS Code">

安装 [C# Dev Kit](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit) 扩展，它把 .NET 热重载带进了 VS Code。

接下来二选一：

- 在集成终端里用 `dotnet watch` 运行应用，或者
- 启动一次调试会话（<kbd>F5</kbd>），保存文件时热重载便会生效。

</TabItem>
<TabItem value="rider" label="Rider">

JetBrains Rider 虽有热重载功能，却不会驱动 .NET 元数据更新。你可以：

- 在 Rider 的终端里用 `dotnet watch` 运行应用，或者
- 启用[文件系统监视器](#enabling-the-file-system-watcher)，照常启动应用。

</TabItem>
</Tabs>

### 启用文件系统监视器 {#enabling-the-file-system-watcher}

即便没挂上 .NET 热重载，Avalonia 热重载仍能靠内置的文件系统监视器捕捉 `.axaml` 的改动。你在 `dotnet watch` 之外运行应用、或者用的是 Rider 时，就属于这种情形。

要启用文件系统监视器，请在 `.csproj` 中添加一个 MSBuild 属性：

```xml
<PropertyGroup>
  <AvaloniaHotReloadEnableFileWatcher>true</AvaloniaHotReloadEnableFileWatcher>
</PropertyGroup>
```

:::tip
文件系统监视器不借助 .NET 热重载也能重载 `.axaml` 文件，但对 `.cs` 文件无能为力。若你的 C# 代码隐藏也要热重载，请把监视器与 `dotnet watch` 搭配使用。
:::

## 验证热重载是否生效 {#verifying-hot-reload}

在应用运行的状态下：

1. 打开一个 `.axaml` 文件，改个属性，比如某个 `Background` 颜色或一段文字，然后保存。
2. 盯着运行中的窗口，它应当更新，且当前视图不会丢失。
3. 打开对应的 `.axaml.cs` 文件，改一下事件处理程序，然后保存。
4. 触发该事件。
5. 在运行中的窗口里确认该事件的行为已反映出你的改动。诊断输出写在跟踪日志中 `HotReload` 这一类别下。

:::info
C# 改动遵循标准的 .NET 热重载规则。
:::


## 手动初始化 {#initializing-manually}

上文的自动配置方式足以应付绝大多数热重载场景。若你需要自定义生命周期、多个 `Application` 实例或延后启动，也可以手动调用初始化器：

```csharp
using AvaloniaUI.DiagnosticsSupport.HotReload;

HotReloadExtensions.InitializeHotReload(
    Application.Current!,
    enableFileWatcher: true,
    rewriteStaticResources: true);
```

引擎每个进程只初始化一次，之后再调用也不起作用。想在日志中看到热重载的动静，请订阅 `HotReloadDiagnostics.EntryLogged`。

## 限制 {#limitations}

- WebAssembly 暂不支持。热重载只在桌面和移动平台上可用。
- C# 改动遵循常规的 [.NET 热重载规则](https://learn.microsoft.com/en-us/visualstudio/debugger/hot-reload)。添加字段或改动方法签名属于 rude edit，必须重启。
- 控件是重建而非就地修改的，因此控件重载时，非 XAML 的状态会被重置。

## 另请参阅 {#see-also}

- [安装 Avalonia Plus 开发者工具](/tools/developer-tools/installation)
- [数据模板](/docs/data-templates/introduction-to-data-templates)
- [在 Visual Studio 中借助热重载编写和调试运行中的代码（C#、Visual Basic、C++）](https://learn.microsoft.com/en-us/visualstudio/debugger/hot-reload)
