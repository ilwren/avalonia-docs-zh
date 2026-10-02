---
id: troubleshooting
title: 排查问题
---

## NuGet 包还原不下来 {#trouble-restoring-nuget-packages}

若 XPF 和/或 Avalonia 的包还原不下来（比如提示找不到 `Xpf.Sdk` 或某个 Avalonia `cibuild` 包），请照下面几步排查：

### 检查防火墙设置 {#check-your-firewall-settings}

试着在浏览器中打开下面这几个网址：

:::tip
系统询问时，用户名填 `license`，密码填你的许可证密钥。
:::

- https://xpf-nuget-feed.avaloniaui.net/
- https://xpf-nuget-feed.avaloniaui.net/v3/index.json
- https://nuget-feed-all.avaloniaui.net/v3/index.json

第一个网址应当显示一个类似 [nuget.org](https://www.nuget.org/packages) 包列表的页面，后两个网址应当显示一段 JSON。

若其中任何一个打不开，请检查防火墙设置。

若用许可证密钥登录不上，它可能已经过期了，找支持团队要一个新的。

### 确认你配好了 NuGet.config {#check-you-have-set-up-nugetconfig}

- 确认你添加了 [NuGet.config](/xpf/getting-started#step-2-add-a-nugetconfig) 文件，**而且它与你要加载的 `.sln` 文件在同一个目录下**
- 确认你在 `NuGet.config` 文件中填了有效的许可证密钥

### 清理 NuGet 的 HTTP 缓存 {#clear-your-nuget-http-cache}

在命令行运行下列命令：

```bash
dotnet nuget locals http-cache --clear
dotnet restore
```

## Avalonia 版本冲突 {#avalonia-version-conflicts}

若你看到这样的 `TypeLoadException`：

```text
Method 'SetDataAsync' in type 'Avalonia.Win32.ClipboardImpl' does not have an implementation
```

这是因为你显式引用的某个 Avalonia 包，版本与 XPF 捆绑的那份对不上。比如引用了 11.3.8 的 `Avalonia.Desktop`，而 XPF 捆绑的是 Avalonia 11.3.0。

**解决办法**：把项目中显式的 Avalonia 包引用删掉。XPF SDK 会以传递方式提供所有必需的 Avalonia 包。若确需直接引用某个 Avalonia 包，请用 `$(XpfAvaloniaVersion)` MSBuild 属性，让版本与 XPF 捆绑的那份保持一致：

```xml
<PackageReference Include="Avalonia.Headless.XUnit" Version="$(XpfAvaloniaVersion)" />
```

## 多项目解决方案中的程序集版本冲突 {#assembly-version-conflicts-in-multi-project-solutions}

当用 `Sdk="Xpf.Sdk"` 的项目与用 `Sdk="Microsoft.NET.Sdk"` 和 `<UseWpf>true</UseWpf>` 的项目混在一个解决方案里时，构建时可能出现关于 `ReachFramework` 或 `System.Windows.Input.Manipulations` 版本冲突的警告。

这些警告可以放心无视。运行时用的会是 XPF 随附的那一份程序集。

## 用代码打不开 ContextMenu {#contextmenu-not-showing-programmatically}

若设置 `ContextMenu.IsOpen = true` 后上下文菜单不显示（而右键点击一切正常），请在打开之前显式设置 `PlacementTarget` 属性：

```csharp
myContextMenu.PlacementTarget = targetElement;
myContextMenu.IsOpen = true;
```

在 WPF 中，某些情况下 `PlacementTarget` 会被隐式设置，而 XPF 要求你把它写明。

## 发布后的应用中应用路径返回 null {#application-path-returns-null-in-published-apps}

以单文件方式发布的应用在运行时，`Assembly.GetEntryAssembly().Location` 会返回 null 或空字符串。这是 .NET 5+ 的既定行为，与 XPF 无关。

请改用 `AppDomain.CurrentDomain.BaseDirectory`：

```csharp
string appPath = AppDomain.CurrentDomain.BaseDirectory;
```

## 收听 XPF 日志 {#listening-for-xpf-logs}

XPF 的日志由环境变量控制。
* `XPF_LOG_OUTPUT`：`console`、`trace`、`file=filePath`。可以用 `;` 分隔，同时指定多个值。
* `XPF_LOG_LEVEL`: `Verbose`, `Information`, `Debug`, `Warning`, `Error`, `Fatal`.

:::caution
较老的文档里可能提到 `ATLANTIS_LOG_OUTPUTS` 和 `ATLANTIS_LOG_LEVEL`，正确的变量名其实是 `XPF_LOG_OUTPUT` 和 `XPF_LOG_LEVEL`。
:::

## 收听 Avalonia 日志 {#listening-for-avalonia-logs}

XPF 建立在 Avalonia 之上，有时把 Avalonia 的日志也收集起来会很有帮助，排查问题时尤其如此。

### 在自定义 Avalonia 初始化中用 .LogToTrace {#logtotrace-in-a-custom-avalonia-initialization}

1. 先照[这份说明](/xpf/configuration/customizing-initialization)配好自定义的 Avalonia 初始化。
2. 然后你就可以在 AppBuilder 链式调用里调 `.LogToTrace()` 了，还能带上可选的严重级别参数，像这样：
```diff
        AppBuilder.Configure<AvaloniaUI.Xpf.Helpers.DefaultXpfAvaloniaApplication>()
            .UsePlatformDetect()
+           .LogToTrace(LogEventLevel.Warning)
            .WithAvaloniaXpf()
```

这会把所有 Avalonia 日志转发给 .NET 的 `System.Diagnostics.Trace` 侦听器。你可以在应用中添加自定义的跟踪侦听器，把这些日志导向文件、控制台或你自己的日志框架：

```csharp
// Route trace output to a file
Trace.Listeners.Add(new TextWriterTraceListener("avalonia.log"));
Trace.AutoFlush = true;
```

### Override `Logger.Sink`

静态属性 `Logger.Sink` 带有公共 setter，可以用自定义实现把它换掉。
```csharp
public void Initialize()
{
    // You can override Logger.Sink value at any point of application lifetime,
    // But preferably to do it as early as possible, or even in the custom Avalonia initialization.
    Logger.Sink = new MyLogger();
}

public class MyLogger : ILogSink
{
    // Implement all members
}
```

## System.Resources.Extensions

若你遇到下面这个异常：

```text
System.IO.FileNotFoundException: Could not load file or assembly 'System.Resources.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=cc7b13ffcd2ddd51'. The system cannot find the file specified.
```

那就通过 nuget 装上 `System.Resources.Extensions` 包：

```xml
<PackageReference Include="System.Resources.Extensions" Version="7.0.0" />
```

7.0.0 版本与 .NET 6 也是兼容的。

## NullReferenceException 或 MissingMethodException {#nullreferenceexception-or-missingmethodexception}

若升级 XPF 之后出现 `NullReferenceException` 或 `MissingMethodException`，试试清理项目，或者直接删掉 `bin`/`obj` 目录。

## Linux 上找不到 libSkiaSharp {#libskiasharp-not-found-on-linux}

若你遇到：

```text
System.DllNotFoundException: Unable to load shared library 'libSkiaSharp' or one of its dependencies
```

这通常是用 Visual Studio 发布所致——它产出的输出可能不完整。请改从命令行发布：

```bash
dotnet publish -r linux-x64 -c Release
```

更多细节请见 [Linux：发布](/xpf/platforms/linux#publishing-for-linux)。

## AssemblyLoadContext（ALC）冲突 {#assemblyloadcontext-alc-conflicts}

若你的应用用了自定义 .NET 宿主，或者插件架构中存在多个独立的 `AssemblyLoadContext` 实例，XPF 初始化时可能抛出关于类型参数约束的 `VerificationException`。这是同一个程序集被加载进多个 ALC 造成的。

**解决办法**：
- 确保 XPF 的程序集加载到 `AssemblyLoadContext.Default` 中
- 若是插件架构，请在 `.csproj` 中加上：
  ```xml
  <ItemGroup>
      <RuntimeHostConfigurationOption Include="AvaloniaUI.Xpf.EnableAlcSupport" Value="true" />
  </ItemGroup>
  ```
- 在 ALC 之间通信时采用契约程序集的模式

## .NET 版本兼容性 {#net-version-compatibility}

XPF 支持 .NET 6、7、8、9 和 10。搭配 XPF SDK 时，`net8.0-windows`（或类似的）目标框架在所有平台上都管用。

比 .NET 6 更新的版本给 WPF 添的特性（比如 .NET 9 的 Fluent 主题）在 XPF 中未必有，但 .NET 8 的那些特性（比如 `OpenFolderDialog`）是支持的。

:::tip
搭配 XPF SDK 时，`-windows` 这个目标框架后缀（例如 `net8.0-windows`）在 Linux 和 macOS 上同样管用，跨平台构建不必改 TFM。反倒是用不带 `-windows` 后缀的 `net8.0` TFM 时，那些指望 Windows 专属 API 的第三方库可能编译不过。
:::

## Xpf.Sdk 导入冲突 {#xpfsdk-import-conflicts}

当用 `Sdk="Xpf.Sdk"` 的项目与标准的 `Microsoft.NET.Sdk` 项目混在一起时，可能撞上 MSBuild 导入冲突或类型重复的警告。常见症状包括：

- `ReachFramework` 或 `System.Windows.Input.Manipulations` 版本冲突
- `WindowsDesktop` SDK 被导入了两次

**解决办法**：
- 请确保只有可执行项目用 `Sdk="Xpf.Sdk"`，库项目改用 `Microsoft.NET.Sdk` 加 `<EnableWindowsTargeting>true</EnableWindowsTargeting>` 即可。
- 把用了 XPF SDK 的项目中显式的 `<UseWpf>true</UseWpf>` 删掉——该 SDK 会自动提供 WPF 支持。
- 若换过 SDK 之后出现 `Could not load file or assembly` 错误，请清理 `bin`/`obj` 目录。

## 许可证校验 {#license-validation}

XPF 用两个标识把你的应用与许可证对上号：

1. **程序集名称**：通过 `Assembly.GetEntryAssembly().GetName().Name` 取得
2. **进程可执行文件名**：运行中进程的名称

两者都必须与许可证中配置的值一致。若许可证校验失败，请核对项目的 `AssemblyName` 是否与许可证登记的名称相符。

:::note
若你改了应用可执行文件的名字，或改了 `.csproj` 中的 `AssemblyName`，就必须同步更新许可证。请联系 Avalonia 团队更新你的许可证配置。
:::

## 制作依赖 XPF 的 NuGet 包 {#creating-nuget-packages-that-depend-on-xpf}

若你想把一个内部用到 XPF 的库作为公开 NuGet 包分发：

- 使用你这个包的人必须自备 XPF 许可证
- 不要把 XPF 的程序集打进你的 NuGet 包里再分发
- 把 XPF 的包写成依赖项，让它们从有授权的 NuGet 源解析下来
- 对上许可证的是使用者入口程序集的名称，而不是你这个库的程序集名

## dispatcher 线程错误 {#dispatcher-thread-errors}

若你遇到 “The calling thread cannot access this object because a different thread owns it” 这类异常：

- 确保界面操作都在主 dispatcher 线程上进行：`Dispatcher.CurrentDispatcher.Invoke(() => { ... })`
- XPF 在 macOS 上只支持一个 UI 线程。那些在其他线程上创建窗口的 WPF 写法，必须改造成统一走主 dispatcher。
- 某些第三方库（比如 Caliburn.Micro）会在初始化期间从后台线程访问窗口属性。针对具体库的建议请见[库的兼容性：Caliburn.Micro](/xpf/third-party/compatibility#caliburnmicro)。
