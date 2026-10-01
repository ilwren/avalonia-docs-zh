---
id: logs-tool
title: 日志工具
description: 在开发者工具中查看和筛选 Avalonia 日志消息，与 Microsoft.Extensions.Logging 集成，并创建 Serilog sink 这样的自定义日志源。
doc-type: reference
---

## 在工具中查看 Avalonia 日志 {#viewing-avalonia-logs-in-the-tool}

`Developer Tools` 默认会自动记录 `Avalonia` 的警告和错误。

主要功能包括：

1. 在数据表中合并显示消息。
2. 按详尽级别、消息和参数筛选。
3. 逐个单独展示各个参数。
4. 若日志条目的 `Source` 是挂在元素树上的视觉元素，点击它即可跳到 `Developer Tools` 中对应的元素
5. 与第三方日志库集成。

![显示 Avalonia 警告的日志工具](/img/tools/dev-tools/logs-avalonia-list.png)

## 启用 Microsoft.Extensions.Logging 集成 {#enabling-microsoftextensionslogging-integration}

默认只有 `Avalonia` 的日志会被转发到 `Developer Tools` 进程。
`Diagnostics Support` 库内置了与 Microsoft 日志抽象的集成，开启起来很容易。

照常创建 `LoggerFactory` 即可，然后把返回的对象传给 `DevToolsLoggerCollector.WithMicrosoftLogger(ILoggerFactory)` 方法。

```csharp
public override void Initialize()
{
    AvaloniaXamlLoader.Load(this);

    var loggerFactory = LoggerFactory.Create(b => b
        .SetMinimumLevel(LogLevel.Information)
        .AddConsole());

    this.AttachDeveloperTools(o =>
    {
        o.AddMicrosoftLoggerObservable(loggerFactory);
    });

    Logger = loggerFactory.CreateLogger<Application>();
}
```

若用的是 MS 依赖注入方案，可以把 `ILoggerFactory` 接口存进 `ServiceCollection` 并从中取用。

关于 `DeveloperToolsOptions` 的更多细节，请见 [DeveloperToolsOptions 参考](/tools/developer-tools/options)页。

## 挂接自定义日志源 {#attaching-custom-log-source}

![显示自定义 Serilog 事件的日志工具](/img/tools/dev-tools/logs-custom-serilog.png)

下面以 `Serilog` sink 为例，把它配置成将日志转发进 `Developer Tools`。

按 `Serilog` 的[开发 sink](https://github.com/serilog/serilog/wiki/Developing-a-sink)文档所述，需要实现一个简单的 `ILogEventSink` 接口，再加上把它与 `Developer Tools` 连起来所必需的 `ILoggerObservable`：

```csharp
public class DevToolsSerilogSink(string logArea = "Serilog") : ILogEventSink, ILoggerObservable
{
}
```

先实现 `ILoggerObservable.Subscribe`，把观察者记在一个列表里。`ILoggerObserver` 只有两个方法：`IsEnabled` 和 `Log`，本示例两个都会用到。返回值是一个可释放对象，DevTools 断开连接时会被调用。

```csharp
private readonly LinkedList<ILoggerObserver> _observers = [];

public IDisposable Subscribe(ILoggerObserver observer)
{
    _observers.AddLast(observer);
    return Disposable.Create(() => _observers.Remove(observer));
}
```

而 `ILogEventSink.Emit` 的实现则要把 Serilog 的日志事件转换成 `ILoggerObserver` 认得的参数：

```csharp
public void Emit(LogEvent logEvent)
{
    var logLevel = logEvent.Level switch
    {
        LogEventLevel.Verbose => LogEntryVerbosity.Verbose,
        LogEventLevel.Debug => LogEntryVerbosity.Debug,
        LogEventLevel.Information => LogEntryVerbosity.Information,
        LogEventLevel.Warning => LogEntryVerbosity.Warning,
        LogEventLevel.Error => LogEntryVerbosity.Error,
        LogEventLevel.Fatal => LogEntryVerbosity.Fatal,
        _ => throw new ArgumentOutOfRangeException()
    };

    // Map each parameter into a strings array:
    var parameters = new string[logEvent.Properties.Count];
    var paramIndex = 0;
    foreach (var value in logEvent.Properties.Values)
    {
        parameters[paramIndex++] = value.ToString(null, formatProvider);
    }

    foreach (var observer in _observers)
    {
        // `Developer Tools` might disable specific logging areas, so we need to check them first.
        if (observer.IsEnabled(logLevel, logArea))
        {
            // Queue log entry with our parameters.
            observer.Log(logLevel, logArea, null, logEvent.MessageTemplate.Text, logEvent.Exception, parameters);
        }
    }
}
```

两个接口都备齐后，就可以在 `Application.Initialize` 方法里把 `Serilog` 和 `Developer Tools` 一并配置好：

```csharp
public override void Initialize()
{
    AvaloniaXamlLoader.Load(this);

    var sink = new SerilogSink();

    Logger = new LoggerConfiguration()
        .MinimumLevel.Information()
        .WriteTo.Sink(sink)
        .CreateLogger();

    this.AttachDeveloperTools(o =>
    {
        o.AddLoggerObservable(sink);
    });
}
```

然后在代码的某处用起来：

```csharp
private int _clickTimes = 0;
private void Button_OnClick(object? sender, RoutedEventArgs e)
{
    _clickTimes++;
    App.Logger!.Information("Button was clicked {Times} times", _clickTimes);
}
```

<details>
  <summary>DevToolsSerilogSink 类完整代码</summary>
  
```csharp
public class DevToolsSerilogSink(string logArea = "Serilog", IFormatProvider? formatProvider = null)
    : ILogEventSink, ILoggerObservable
{
    private readonly LinkedList<ILoggerObserver> _observers = [];

    public IDisposable Subscribe(ILoggerObserver observer)
    {
        _observers.AddLast(observer);
        return Disposable.Create(() => _observers.Remove(observer));
    }

    public void Emit(LogEvent logEvent)
    {
        var logLevel = logEvent.Level switch
        {
            LogEventLevel.Verbose => LogEntryVerbosity.Verbose,
            LogEventLevel.Debug => LogEntryVerbosity.Debug,
            LogEventLevel.Information => LogEntryVerbosity.Information,
            LogEventLevel.Warning => LogEntryVerbosity.Warning,
            LogEventLevel.Error => LogEntryVerbosity.Error,
            LogEventLevel.Fatal => LogEntryVerbosity.Fatal,
            _ => throw new ArgumentOutOfRangeException()
        };

        var parameters = new string[logEvent.Properties.Count];
        var paramIndex = 0;
        foreach (var value in logEvent.Properties.Values)
        {
            parameters[paramIndex++] = value.ToString(null, formatProvider);
        }

        foreach (var observer in _observers)
        {
            if (observer.IsEnabled(logLevel, logArea))
            {
                observer.Log(logLevel, logArea, null, logEvent.MessageTemplate.Text, logEvent.Exception, parameters);
            }
        }
    }
}
```

</details>

## 另请参阅 {#see-also}

- [开发者工具选项](/tools/developer-tools/options)
- [安装开发者工具](/tools/developer-tools/installation)
