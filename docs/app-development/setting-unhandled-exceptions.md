---
id: setting-unhandled-exceptions
title: 处理未捕获异常
description: 处理 Avalonia 应用中来自 UI 线程、后台线程和任务的未捕获异常。
doc-type: how-to
---

正式投产的应用需要有一套办法，去兜住那些从常规错误处理中漏出来的异常。Avalonia 提供了几种机制，用于拦截 UI 线程和后台任务抛出的未捕获异常。

## UI 线程上的异常 {#ui-thread-exceptions}

### Dispatcher.UnhandledException

当 UI 线程上的异常没有被应用代码捕获时，`Dispatcher.UIThread.UnhandledException` 事件就会触发。你可以在此记录错误，并视情况把它标记为已处理：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    Dispatcher.UIThread.UnhandledException += OnUnhandledException;

    base.OnFrameworkInitializationCompleted();
}

private void OnUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
{
    // Log the exception
    Log.Error(e.Exception, "Unhandled UI thread exception");

    // Optionally prevent the application from crashing
    e.Handled = true;
}
```

:::caution
设置 `e.Handled = true` 会吞掉该异常，让应用继续运行。请谨慎使用：如果这个异常已经让应用处于不一致的状态（数据损坏、操作只完成了一半），硬撑下去可能招来更多麻烦。能就地捕获并恢复的，尽量就地处理。
:::

### Dispatcher.UnhandledExceptionFilter

`UnhandledExceptionFilter` 事件在 `UnhandledException` 之前触发，让你决定某一类异常要不要转交给 `UnhandledException` 处理程序：

```csharp
Dispatcher.UIThread.UnhandledExceptionFilter += (sender, e) =>
{
    // Prevent certain exceptions from reaching UnhandledException
    if (e.Exception is TaskCanceledException)
    {
        e.RequestCatch = false;
    }
};
```

### 在 Main 中做全局 try-catch {#global-try-catch-in-main}

把应用入口点包在 try-catch 里，可以兜住任何导致 UI 线程终止的异常，包括那些未被标记为已处理的：

```csharp
public static void Main(string[] args)
{
    try
    {
        BuildAvaloniaApp()
            .StartWithClassicDesktopLifetime(args);
    }
    catch (Exception e)
    {
        Log.Fatal(e, "Application terminated unexpectedly");
    }
    finally
    {
        Log.CloseAndFlush();
    }
}
```

这是你最后一道防线。异常走到这个代码块时，Avalonia 应用其实已经关掉了。所以它只适合用来记日志和收尾清理，不适合做恢复。

## 后台线程上的异常 {#background-thread-exceptions}

### 未被观察的任务异常 {#unobserved-task-exceptions}

`Task.Run` 或其他异步操作中抛出的异常，若从未被 await 或观察，就成了「未被观察的任务异常」。在 .NET 中它们默认会被悄悄吞掉。订阅 `TaskScheduler.UnobservedTaskException` 即可发现它们：

```csharp
TaskScheduler.UnobservedTaskException += (sender, e) =>
{
    Log.Error(e.Exception, "Unobserved task exception");

    // Prevent the exception from terminating the process
    e.SetObserved();
};
```

:::info
未被观察的任务异常是在终结器线程上抛出的，并非异常发生的那一刻，因此事件触发可能会有延迟。要想可靠地处理错误，请始终 `await` 你的任务，或用 `ContinueWith` 来观察异常。
:::

### AppDomain.UnhandledException

对于非 UI 线程上、又不走任务模型的异常，使用 .NET 的 `AppDomain.UnhandledException` 事件：

```csharp
AppDomain.CurrentDomain.UnhandledException += (sender, e) =>
{
    var exception = e.ExceptionObject as Exception;
    Log.Fatal(exception, "Unhandled domain exception (terminating: {IsTerminating})",
        e.IsTerminating);
};
```

这个事件仅供知情之用。当 `IsTerminating` 为 `true` 时，你无法阻止应用终止。

## 推荐的做法 {#recommended-strategy}

一套可靠的异常处理方案要多层配合：

```csharp title="Program.cs"
public static void Main(string[] args)
{
    // Background thread exceptions
    AppDomain.CurrentDomain.UnhandledException += (s, e) =>
        Log.Fatal(e.ExceptionObject as Exception, "Unhandled domain exception");

    TaskScheduler.UnobservedTaskException += (s, e) =>
    {
        Log.Error(e.Exception, "Unobserved task exception");
        e.SetObserved();
    };

    try
    {
        BuildAvaloniaApp()
            .StartWithClassicDesktopLifetime(args);
    }
    catch (Exception e)
    {
        Log.Fatal(e, "Application crashed");
    }
    finally
    {
        Log.CloseAndFlush();
    }
}
```

```csharp title="App.axaml.cs"
public override void OnFrameworkInitializationCompleted()
{
    // UI thread exceptions
    Dispatcher.UIThread.UnhandledException += (s, e) =>
    {
        Log.Error(e.Exception, "Unhandled UI exception");
        e.Handled = true; // Only if safe to continue
    };

    base.OnFrameworkInitializationCompleted();
}
```

### 日志记录 {#logging}

用 [Serilog](https://serilog.net) 或 [NLog](https://nlog-project.org) 之类的结构化日志库，把异常记录到文件、控制台或外部服务。至少要记下异常类型、消息和调用栈，这样才能根据线上反馈定位问题。

## 另请参阅 {#see-also}

- [应用生命周期](/docs/fundamentals/application-lifetimes)：桌面与移动端的生命周期模型。
- [TaskScheduler.UnobservedTaskException](https://learn.microsoft.com/dotnet/api/system.threading.tasks.taskscheduler.unobservedtaskexception)：.NET 官方文档。
- [AppDomain.UnhandledException](https://learn.microsoft.com/dotnet/api/system.appdomain.unhandledexception)：.NET 官方文档。
