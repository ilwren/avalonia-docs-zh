---
id: getting-started
title: 快速上手
---

:::tip[让 AI 帮你迁移]
若你用的 AI 编码助手支持 MCP（VS Code、Cursor、Rider、Claude Code 等），[Build MCP](/tools/ai-tools/build-mcp) 服务器可以一步步带你走完整个流程。只要让助手迁移你的 WPF 项目，它就会分析依赖、配置 NuGet 源、切换 SDK，并与你一来一回地排查问题。配置说明请见 [Build MCP 配置](/tools/ai-tools/build-mcp#setting-up-the-mcp-server)。
:::

## 第 1 步：准备你的 WPF 项目 {#step-1-prepare-your-wpf-project}

:::note
本文以 .NET 7.0 为例，但 XPF 支持 .NET 6.0 及以上。 

推荐使用 .NET 8（当前的 LTS）或 .NET 9。
:::

请确认你的项目至少已升级/移植到 `net6.0-windows`，并采用 SDK 风格的 `.csproj` 格式。SDK 风格的项目以 `<Project Sdk="Microsoft.NET.Sdk">` 开头，而不是带一堆 `<Import>` 元素的老式冗长格式。

若你的项目还在用老式的 `.csproj` 格式，可以借助 .NET 升级助手，也可以手动转换。关键改动有：
- 把冗长的 XML 换成 SDK 风格的 `<Project Sdk="Microsoft.NET.Sdk">` 根元素
- Set `<TargetFramework>net8.0-windows</TargetFramework>`
- Add `<UseWpf>true</UseWpf>`
- 删掉显式的文件包含项（SDK 风格项目会自动包含文件）

继续往下之前，先确认项目能在 .NET 8（或更高）上用 WPF 正常构建和运行。

:::danger
这一步**至关重要**。XPF 不支持老式的 `.csproj` 格式，也不支持低于 6.0 的 .NET 版本。你必须先转换项目，并确认 WPF 在现代 .NET 版本上跑得通，然后才谈得上用 XPF。
:::

:::danger
若你在 Linux 上开发，请**先**看 [linux](/xpf/platforms/linux) 指南，再安装 .NET。
:::

## 第 2 步：添加 `NuGet.config` {#step-2-add-a-nugetconfig}

在解决方案根目录创建一个 `NuGet.config` 文件，或修改已有的那个，使其包含以下内容：

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="api.nuget.org" value="https://api.nuget.org/v3/index.json" />
    <add key="xpf" value="https://xpf-nuget-feed.avaloniaui.net/v3/index.json" />
    <add key="avalonia-nightly" value="https://nuget-feed-all.avaloniaui.net/v3/index.json" />
  </packageSources>
  <packageSourceCredentials>
    <xpf>
      <add key="Username" value="license" />
      <add key="ClearTextPassword" value="<YOUR_LICENSE_KEY>" />
    </xpf>
  </packageSourceCredentials>
</configuration>
```

## 第 3 步：改用 XPF SDK {#step-3-use-the-xpf-sdk}

在可执行的 WPF 项目中，把 `.csproj` 里的 SDK 换成 XPF SDK。第一行：

```xml
<Project Sdk="Microsoft.NET.Sdk">
``` 

应改为：

```xml
<Project Sdk="Xpf.Sdk/1.6.0">
```

:::note
XPF 仍在活跃开发中，CI 构建版本号变动频繁。这里给出的是撰稿时的最新版本，眼下多半已有更新的版本了。最新的 CI 构建版本号可在 https://xpf-nuget-feed.avaloniaui.net/packages/xpf.sdk. 查到。更多信息请见[夜间构建](/xpf/version-info/versioning)。
:::

:::tip
若你有多个项目需要用同一个 XPF SDK 版本，可以[在 `global.json` 中统一指定](/xpf/configuration/centralizing-multiple-xpf-projects)
:::

## 第 4 步：填入许可证密钥 {#step-4-add-your-licence-key}

在可执行项目的 `.csproj` 中加上：

```xml
  <ItemGroup>
    <RuntimeHostConfigurationOption Include="AvaloniaUI.Xpf.LicenseKey" Value="<YOUR_LICENSE_KEY>" />
  </ItemGroup>  
```

注意，若你用的是正式许可证，项目的 AssemblyName 必须与许可证密钥登记的名称一致

## 第 5 步：清理解决方案 {#step-5-clean-your-solution}

换过项目 SDK 之后，必须把已有的构建产物清理干净：

- 在命令行运行 `dotnet clean`；或者
- 在 IDE 中执行 `Build -> Clean Solution`；又或者
- 手动删掉 `obj`/`bin` 目录

## 第 6 步：运行项目 {#step-6-run-the-project}

现在你应该能在惯用的 IDE 中带着 Avalonia XPF 运行项目了，也可以用 `dotnet run`。

:::tip
若在 Linux 上运行，请见 [Linux](/xpf/platforms/linux) 页，了解如何安装 .NET 和所需依赖。
:::

## 其他项目 {#additional-projects}

若你还有一些用到 WPF API 的非可执行项目，且需要在 Linux 或 macOS 上构建它们，可以照上面的办法换 SDK；若你面向的是 `net7.0-windows`，也可以在相应的项目文件中加上：

```xml
<PropertyGroup>
  <EnableWindowsTargeting>true</EnableWindowsTargeting>
</PropertyGroup>
```

加到对应的项目文件中。

或者在解决方案根目录建一个 `Directory.Build.props` 文件，内容如下：

```xml
<Project>
  <PropertyGroup>
    <EnableWindowsTargeting>true</EnableWindowsTargeting>
  </PropertyGroup>
</Project>  
```

## 目标框架 {#target-framework}

理想情况下，所有引用 XPF 的项目都该用 `net6.0-windows` 或 `net7.0-windows` TFM。你也可以用 `net6.0` 或 `net7.0` TFM，但那样就不能用 `<EnableWindowsTargeting>`，必须改用 XPF SDK。

:::tip
搭配 XPF SDK 时，`-windows` 目标框架（例如 `net8.0-windows`）在所有平台上都能用。为 Linux 或 macOS 构建、运行时，不必改动目标框架。有些第三方库非要 Windows 专属的 TFM 不可，所以保留 `net8.0-windows` 往往最省事。
:::

## 承载 WinForms（仅 Windows） {#winforms-hosting-windows-only}

若你的应用需要在 XPF 中承载 WinForms 控件，请在 `.csproj` 里加一个按 Windows 条件生效的 `PropertyGroup`，并在其中写上：

```xml
<PropertyGroup Condition="$([MSBuild]::IsOSPlatform('Windows'))">
    <XpfUseMicrosoftWindowsForms>true</XpfUseMicrosoftWindowsForms>
</PropertyGroup>
```

这会关掉 WinForms 的 shim 层，改用原生的 WinForms 集成。注意承载 WinForms 只在 Windows 上可用，若不加条件判断，在其他平台上会导致构建失败。

## 移植小贴士 {#porting-tips}

### 项目文件 {#project-files}

1. 把所有项目都转到 .NET 8.0 及以上。老式的项目文件格式（非 SDK 风格的 `.csproj`）在 Windows 之外行不通。
2. 强烈建议先在 Windows 上完成第 (1) 步，免得到了别的平台上还要跟难缠的 Windows 专属依赖问题周旋。把 .NET 7.0 中已废弃的特性换掉或删掉，比如 AppDomain、CodeDOM、WCF、`System.Web`、XmlSerializer，以及 `System.Management.Instrumentation`、`System.Drawing.Common` 这类硬绑 Windows 的 API，改用跨平台友好的替代方案。
3. 做第 (1) 步时，留意应用里可能有的自定义 MSBuild 任务。跑一下 `dotnet build`，确认这些任务在 .NET 7.0 上仍然管用。别在 Visual Studio 里测，这样才能确认它在 IDE 之外也没问题。
4. 把所有 PCL（可移植类库）转成 `netstandard` 库。
5. 删掉 `.csproj` 中所有的 `ApplicationDefinition` 条目。
6. 删掉那些逐条定义 `Configuration`、`Platform`、`ProjectGuid`、`OutputType`、`RootNamespace` 等属性的冗长 `PropertyGroup` 元素。这些东西 SDK 风格的项目都给了合理的默认值。

### Dependencies

7. 若你用的某个 nuget 包是基于 .NET Framework 的，请尽量找它更新的版本（`netstandard2.0`、`netcoreapp2.0`+、`net5.0`+）。多数时候那些 .NET Framework 包跨平台也能用，但这并无保证。 
8. 若项目文件中有 `Reference` 项链接到独立的 `dll`，请照第 (4) 条的思路到 NuGet 上找替代品。若它是托管程序集，往往还能用，但同样没有保证。
9. 若你有原生二进制文件，尽量找托管的等价物，或者为目标平台重新编译它们。在 .NET 8+ 上，原生互操作请用 `System.Runtime.InteropServices.NativeLibrary` 和 `DllImport`。
10. 把依赖都升到最新版，尤其是 Actipro、DevExpress、Syncfusion、Telerik 这些第三方组件。

### Windows

11. 尽量别用自定义窗口外壳控件（比如 WPF 的 WindowChrome、MahApps 的 MetroWindow、DevExpress 的 DXWindow），以及任何自定义窗口边框或行为的东西——它们未必契合目标平台的界面风格（想想 macOS 上的 MetroWindow 是个什么光景）。对 XPF 的目标平台来说，单视图应用（类似网站或移动应用那样）才是最合适的设计。

### 资源与设置 {#resources-and-settings}

12. 资源文件（`.resx`）在 Visual Studio 之外不会被重新生成。本地化不妨换个思路，用 JSON 文件或其他不依赖 Visual Studio 的方案。
13. Visual Studio 文本模板（T4、*.template 文件）在 .NET 7.0 上同样已废弃，请改用源生成器。
14. 资源文件（`.resx`）中的图片或位图与 .NET 7.0 不兼容，建议改用 WPF 的资源机制。
15. 尽量别用 `App.Config` / `System.Configuration.ConfigurationManager`：在那些不允许往可执行程序集所在位置写入的平台上（macOS、移动端、WASM 等），它存不住数据。应用的持久化配置请用第三方或自研的方案来写。

### 文件系统访问 {#filesystem-access}

16. 确保你的文件访问代码能应付区分大小写的文件系统，并且用 `Path.DirectorySeparatorChar` 而不是把目录分隔符写死。 

### Fonts

17. 自定义字体必须作为 `<Resource>` 项包含进你的 `.csproj`。若字体没有作为资源嵌入，应用在非 Windows 平台上可能崩溃或退回到默认字体：
    ```xml
    <ItemGroup>
        <Resource Include="Fonts\*.ttf" />
    </ItemGroup>
    ```
18. WPF 和 XPF 的字体匹配方式不同。样式名不太规范的字体（比如写成 “Condense” 而非 “Condensed”）可能匹配不上。若某款字体渲染得不对劲，请核对 XAML 中的字体族名与字体文件里的内部名称是否一致。
19. 若要定制字体回退行为（比如指定缺字时改用哪些字体），请在[自定义初始化](/xpf/configuration/customizing-initialization)中配置 `FontManagerOptions`：
    ```csharp
    .With(new FontManagerOptions
    {
        FontFallbacks = new[]
        {
            new FontFallback { FontFamily = "My Fallback Font" }
        }
    })
    ```

### 不受支持的控件 {#unsupported-controls}

20. 别用 WPF 的拼写检查和 XPS 功能，XPF 不支持它们。
21. 若你想让着色器、3D、媒体这类高级且专门的 WPF 特性在应用中跑起来，请联系 Avalonia 团队，他们会给你指条明路。
