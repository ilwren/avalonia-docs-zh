---
id: logging-errors-and-warnings
title: 记录错误与警告
description: 用 LogToTrace 方法和日志区域启用并配置 Avalonia 的诊断日志。
doc-type: how-to
---

import LogToTraceOutputScreenshot from '/img/guides/app-development/log-to-trace-output.png';

本指南介绍如何用标准的 `System.Diagnostics.Trace` 组件在 Avalonia 中记录警告和错误。

## 启用日志 {#enabling-logs}

如果你用的是 Avalonia 解决方案模板，实现日志所需的代码已经帮你加好了。

要启用日志，或确认日志已启用，请按以下步骤操作：

-  找到你应用的 **Program.cs** 文件。
-  确认 `BuildAvaloniaApp` 方法里调用了 `LogToTrace`，例如：

```csharp
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .LogToTrace();
```

不带参数时，`LogToTrace` 会记录严重程度为 `Warning` 及以上的消息。给 `LogToTrace` 调用传入一个 `LogLevel` 参数即可改成其他级别。例如：

```csharp
using Avalonia.Logging;
...
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .LogToTrace(LogEventLevel.Verbose)
```

:::info
完整的 API 文档请参阅 [`LogEventLevel` 枚举参考](/api/avalonia/logging/logeventlevel)。
:::

日志消息随后会显示在 IDE **输出**窗口的 **调试** 视图中。比如启用详细日志后：

<Image light={LogToTraceOutputScreenshot} alt="Verbose log output in the IDE Debug Output window" position="center" maxWidth={400} cornerRadius="true"/>

若想把这些消息转发到别的地方，可以使用 `System.Diagnostics.Trace` 组件上的方法。

## 日志区域 {#log-area}

Avalonia 发出的每条消息都带有一个区域（area），可用来过滤日志。这些区域由 `Avalonia.Logging.LogArea` 静态类的成员定义：

* `Property`
* `Binding`
* `Animations`
* `Visual`
* `Layout`
* `Control`

在 `LogToTrace` 调用中、`LogEventLevel` 参数之后再追加若干 `Avalonia.Logging.LogArea` 类型的参数，即可把日志限定在一个或多个区域内。比如下面这样就只记录属性和布局相关的消息：

```csharp
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .LogToTrace(LogEventLevel.Debug, LogArea.Property, LogArea.Layout);
```

## 其他日志输出目标 {#alternative-log-targets}

### LogToDelegate

把日志消息转发给自定义的回调函数：

```csharp
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .LogToDelegate((level, area, source, messageTemplate, propertyValues) =>
        {
            Console.WriteLine($"[{area}] {messageTemplate}");
        });
```

### LogToTextWriter

把日志消息写入任意 `TextWriter`，比如文件或 `Console.Out`：

```csharp
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .LogToTextWriter(File.CreateText("avalonia.log"));
```

## 日志接收器 {#log-sinks}

`LogToTrace` 扩展方法内部用的是 `StringLogSink`。Avalonia 允许你实现 `ILogSink` 来自定义接收器，把它赋给 `Avalonia.Logging.Logger.Sink`，Avalonia 就会改用它。

```csharp title='Extension method to assign Logger.Sink'
using Avalonia.Controls;
using Avalonia.Logging;

namespace MyNamespace;
public static class MyLogExtensions
{
    public static AppBuilder LogToMySink(this AppBuilder builder, 
        LogEventLevel level = LogEventLevel.Warning, 
        params string[] areas)
    {
        Logger.Sink = new MyLogSink(level, areas);
        return builder;
    }
}
```

```csharp title='Startup with custom sink'
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .LogToMySink();
```

:::info
在 _GitHub_ 上查看源码：[`StringLogSink.cs`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Logging/StringLogSink.cs)
:::

## 另请参阅 {#see-also}

- [处理未捕获异常](/docs/app-development/setting-unhandled-exceptions)：在应用中处理未捕获的异常。
- [LogEventLevel API 参考](/api/avalonia/logging/logeventlevel)：可用的日志严重级别。
