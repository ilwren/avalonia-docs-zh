---
id: options
title: 开发者工具选项
sidebar_label: 选项
doc-type: reference
---

## DeveloperToolsOptions.Gesture

定义用于启动并连接 `Developer Tools` 进程的手势。
默认：<kbd>F12</kbd>。

## DeveloperToolsOptions.ApplicationName

可选的应用显示名。
若不设置，则使用 `Application.Name` 或入口程序集的名称。

## DeveloperToolsOptions.ConnectOnStartup

定义应用是否在启动时就连上开发者工具。
默认：iOS 和 Android 上为 `true`，其他平台为 `false`。

## DeveloperToolsOptions.AutoConnectFromDesignMode

定义设计模式下的应用是否连上开发者工具。
默认为 'false'。

## DeveloperToolsOptions.Runner

默认情况下，当收到请求而 `DevTools` 实例尚未运行时，`DiagnosticsSupport` 包会尝试启动全局的 `avdt` .NET 工具。

不过你可以改 `DeveloperToolsOptions.Runner` 的值来改变这一行为：

```csharp
this.AttachDeveloperTools(o =>
{
    o.Runner = DeveloperToolsRunner.DotNetTool;
});
```

可选项有：

1. `DeveloperToolsRunner.DotNetTool`——全局 .NET 工具。
2. `DeveloperToolsOptions.AppleBundle`——按 ID 运行 macOS 应用包。要让它生效，你至少得先直接运行一次 `Developer Tools` 进程。
3. `DeveloperToolsOptions.NoOp`——什么都不做。该选项假定 `Developer Tools` 应用由用户手动启动。 
4. `DeveloperToolsRunner.CreateFromExecutable(string)`——按完整路径运行可执行文件。除非你偏好自定义安装该工具，否则不推荐这一项。
5. 默认：`DeveloperToolsRunner.GetDefaultForPlatform()`——桌面端返回 `DotNetTool`，移动端/浏览器返回 `NoOp`。

## DeveloperToolsOptions.Protocol

`DiagnosticsSupport` 在用户应用与 `Developer Tools` 进程之间可用两种传输协议通信：HTTP 和命名管道。

```csharp
this.AttachDeveloperTools(o =>
{
    o.Protocol = DeveloperToolsProtocol.DefaultHttp;
});
```

可选项有：

1. `DeveloperToolsProtocol.DefaultHttp`——默认在 `29414` 端口上建立 HTTP 连接，连接超时 5 秒。
2. `DeveloperToolsProtocol.CreateHttp(Uri, TimeSpan)`——按给定参数建立 HTTP 连接。注意：你还得照[设置页](/tools/developer-tools/settings)单独改一下 `Developer Tools` 的侦听端口。
3. `DeveloperToolsProtocol.CreateHttp(IpAddress, int? port, TimeSpan)`——按给定参数建立 HTTP 连接。未指定端口时使用默认的 `29414`。 
4. `DeveloperToolsProtocol.CreateNamedPipe(string)`——建立命名管道连接。该选项仅适用于桌面平台；若本机连通性有问题，不妨优先选它。管道名称会自动传给 `Developer Tools` 实例。
5. 默认：`DeveloperToolsProtocol.GetDefaultForPlatform()`——目前在所有平台上都返回 `DefaultHttp`。

## DeveloperToolsOptions.DiagnosticLogger

定义 `AvaloniaUI.DiagnosticsSupport` 的所有日志写往哪个 sink。
该选项默认为 `AvaloniaDiagnosticLogger`，即把日志转发给 `Avalonia.Logger.TryGet`。

可选项有：

1. `DiagnosticLogger.CreateConsole(LogEntryVerbosity)`.
2. `DiagnosticLogger.CreateDebug(LogEntryVerbosity)`.
3. `DiagnosticLogger` 抽象接口的任意用户实现。

:::note
想进一步了解 `Developer Tools` 的日志，请阅读[反馈问题](/troubleshooting/tools/developer-tools)。
:::

## DeveloperToolsOptions.LoggerCollector

定义一个收集器，用来侦听待在 `Developer Tools` 中展示的日志。

默认情况下，`Developer Tools` 只侦听 Avalonia 的日志，并在[日志工具](/tools/developer-tools/logs-tool)中展示。

这一行为可通过选项改变：

1. `DeveloperToolsOptions.AddAvaloniaLoggerObservable()`——默认启用。
2. `DeveloperToolsOptions.AddMicrosoftLoggerObservable(ILoggerFactory, LogLevel)` - allows to connect devtools as a logger provider to Microsoft `ILoggerFactory`.
3. `DeveloperToolsOptions.AddLoggerObservable(ILoggerObservable)` - custom `ILoggerObservable` interface implementation. Use this option, if you want DevTools to display your third party logs provider like Serilog.
4. `DeveloperToolsOptions.ClearLoggerObservables()` - clear all observables.

## 另请参阅 {#see-also}

- [开发者工具设置](/tools/developer-tools/settings)
- [安装开发者工具](/tools/developer-tools/installation)
