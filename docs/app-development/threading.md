---
id: threading
title: 线程模型
description: 了解 Avalonia 的单线程 UI 模型，以及 dispatcher、异步写法和后台任务该怎么配合。
doc-type: explanation
---

Avalonia 采用单线程 UI 模型。所有与界面有关的操作，包括读写控件属性，都必须在 UI 线程上进行。WPF、WinForms 以及大多数桌面 UI 框架用的都是同一套线程模型。

## UI 线程 {#the-ui-thread}

应用启动时，Avalonia 会创建一个 dispatcher 来管理 UI 线程上的工作项。所有控件创建、布局、渲染和输入处理都在这个线程上完成。

如果你试图从后台线程访问控件，Avalonia 会抛出 `InvalidOperationException`，消息为 "Call from invalid thread."。

## 获取 dispatcher {#accessing-a-dispatcher}

### Dispatcher.UIThread

`Dispatcher.UIThread` 属性让你在代码的任何地方都能拿到 UI 线程的 dispatcher，用它把工作从后台线程调度回 UI 线程。

### Post（投递后不管） {#post-fire-and-forget}

`Post` 把回调安排到 UI 线程上后立即返回。不需要等结果时就用它：

```csharp
Dispatcher.UIThread.Post(() =>
{
    StatusText.Text = "Processing complete";
});
```

### InvokeAsync（等待结果） {#invokeasync-await-the-result}

`InvokeAsync` 安排一个回调，并返回一个在回调执行完毕时完成的 `Task`。需要等结果、或要确认操作已完成时就用它：

```csharp
var text = await Dispatcher.UIThread.InvokeAsync(() =>
{
    return SearchBox.Text;
});
```

`InvokeAsync` 会捕获调用线程的 `ExecutionContext`，并在回调执行时将其还原。也就是说 `AsyncLocal<T>` 的值、模拟身份和区域文化设置都会从调用方流进被调度的回调里，这与 `Task.Run` 和 WPF dispatcher 的行为一致。

### CheckAccess 与 VerifyAccess {#checkaccess-and-verifyaccess}

调度之前，先看看自己是不是已经在 UI 线程上：

```csharp
if (Dispatcher.UIThread.CheckAccess())
{
    // Already on the UI thread, update directly
    StatusText.Text = "Ready";
}
else
{
    // On a background thread, marshal to UI thread
    Dispatcher.UIThread.Post(() => StatusText.Text = "Ready");
}
```

`VerifyAccess()` 在从非 UI 线程调用时会抛出 `InvalidOperationException`：

```csharp
Dispatcher.UIThread.VerifyAccess(); // Throws if not on UI thread
```

### AvaloniaObject.Dispatcher

每个 `AvaloniaObject` 都会捕获它被创建时所在线程的 dispatcher。编写控件或库时，若希望不论当前激活的是哪个 dispatcher 都能正确工作，就用这个属性：

```csharp
// Uses the object's own dispatcher rather than assuming UIThread
myControl.Dispatcher.Post(() => myControl.IsVisible = false);
```

对多数应用来说，`AvaloniaObject.Dispatcher` 和 `Dispatcher.UIThread` 返回的是同一个实例。这个区别主要对需要支持多个 dispatcher 的库作者才有意义。

### Dispatcher.CurrentDispatcher

返回调用线程的 dispatcher，若尚不存在则创建一个：

```csharp
var dispatcher = Dispatcher.CurrentDispatcher;
```

### Dispatcher.FromThread

返回与指定线程关联的 dispatcher，若不存在则返回 `null`。与 `CurrentDispatcher` 不同，它不会新建 dispatcher：

```csharp
Dispatcher? dispatcher = Dispatcher.FromThread(Thread.CurrentThread);
if (dispatcher is not null)
{
    dispatcher.Post(() => { /* work */ });
}
```

## Dispatcher 优先级 {#dispatcher-priority}

`Post` 和 `InvokeAsync` 都接受一个可选的 `DispatcherPriority` 参数，用来决定该工作项相对于队列中其他项何时执行：

```csharp
Dispatcher.UIThread.Post(
    () => StatusText.Text = "Updated",
    DispatcherPriority.Background);
```

常用优先级，由高到低：

| 优先级 | 说明 |
|---|---|
| `Send` | 先于其他异步操作处理。 |
| `Normal` | 以普通优先级处理。 |
| `Default` | 前台 dispatcher 优先级中最低的一档。 |
| `Render` | 与渲染同等优先级。 |
| `Loaded` | 在布局和渲染之后、输入之前处理。 |
| `Input` | 与输入同等优先级。 |
| `Background` | 在其他非空闲操作完成之后处理。 |
| `ContextIdle` | 在后台操作完成之后处理。 |
| `ApplicationIdle` | 在应用空闲时处理。 |
| `SystemIdle` | 在系统空闲时处理。 |

## 异步写法 {#async-patterns}

### 后台干活、完成后更新界面 {#background-work-with-ui-updates}

一种常见套路是把繁重计算放到后台线程，算完再更新界面：

```csharp
private async void OnLoadClick(object? sender, RoutedEventArgs e)
{
    LoadButton.IsEnabled = false;
    StatusText.Text = "Loading...";

    // Heavy work runs on a thread pool thread
    var data = await Task.Run(() =>
    {
        return LoadLargeDataSet();
    });

    // Back on the UI thread automatically (thanks to SynchronizationContext)
    Items = new ObservableCollection<Item>(data);
    StatusText.Text = $"Loaded {data.Count} items";
    LoadButton.IsEnabled = true;
}
```

:::info
在一个起始于 UI 线程的 `async` 方法中 `await` 某个 `Task` 时，后续代码会自动回到 UI 线程上执行——Avalonia 已经为此装好了捕获 UI 线程上下文的 `SynchronizationContext`。
:::

### 报告进度 {#progress-reporting}

对耗时较长的操作，把进度回报给界面：

```csharp
private async void OnProcessClick(object? sender, RoutedEventArgs e)
{
    var progress = new Progress<int>(percent =>
    {
        // This callback runs on the UI thread
        ProgressBar.Value = percent;
    });

    await Task.Run(() => ProcessData(progress));

    StatusText.Text = "Done";
}

private void ProcessData(IProgress<int> progress)
{
    for (int i = 0; i <= 100; i++)
    {
        Thread.Sleep(50); // Simulate work
        progress.Report(i);
    }
}
```

### 基于计时器的更新 {#timer-based-updates}

周期性的界面更新用 `DispatcherTimer`，它的回调运行在 UI 线程上：

```csharp
var timer = new DispatcherTimer
{
    Interval = TimeSpan.FromSeconds(1)
};

timer.Tick += (sender, e) =>
{
    // Runs on the UI thread
    ClockText.Text = DateTime.Now.ToString("HH:mm:ss");
};

timer.Start();
```

### 把控制权让回 dispatcher {#yielding-to-the-dispatcher}

`Dispatcher.Yield()` 会暂停当前异步方法，把它的后续部分排进 dispatcher 队列，好让待处理的输入、布局和渲染先跑完再继续：

```csharp
private async Task ProcessItemsAsync(IList<Item> items)
{
    foreach (var item in items)
    {
        ProcessItem(item);

        // Let the dispatcher handle pending events before continuing
        await Dispatcher.Yield();
    }
}
```

`Yield` 是静态方法，作用于调用线程的 dispatcher（`Dispatcher.CurrentDispatcher`）。你可以指定优先级来控制何时恢复执行：

```csharp
// Resume only when the dispatcher is idle
await Dispatcher.Yield(DispatcherPriority.ApplicationIdle);
```

若不想用静态方法，或要针对某个特定的 dispatcher 实例，请用 `Resume`：

```csharp
await myControl.Dispatcher.Resume(DispatcherPriority.Background);
```

## 完整示例 {#full-example}

下面这个例子演示如何从工作线程访问 UI 线程，以读写某个 `TextBlock` 的文本：

```xml title='MainView.axaml'
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:vm="clr-namespace:AvaloniaApplication1.ViewModels"
             x:Class="AvaloniaApplication1.Views.MainView"
             x:DataType="vm:MainViewModel">
    <StackPanel Margin="20">
        <TextBlock Name="TextBlock1" />
    </StackPanel>
</UserControl>
```

```csharp title='MainView.axaml.cs'
using Avalonia.Controls;
using Avalonia.Threading;
using System.Threading.Tasks;

namespace AvaloniaApplication1.Views;

public partial class MainView : UserControl
{
    public MainView()
    {
        InitializeComponent();
        _ = Task.Run(() => OnTextFromAnotherThread("test"));
    }

    private void SetText(string text) => TextBlock1.Text = text;
    private string GetText() => TextBlock1.Text ?? "";

    private async void OnTextFromAnotherThread(string text)
    {
        // Start the job on the UI thread and return immediately.
        Dispatcher.UIThread.Post(() => SetText(text));

        // Start the job on the UI thread and wait for the result.
        var result = await Dispatcher.UIThread.InvokeAsync(GetText);

        // This would throw because we are on a worker thread:
        // SetText(text); // InvalidOperationException: 'Call from invalid thread'
    }
}
```

## 常见错误 {#common-mistakes}

### 从 Task.Run 中访问控件 {#accessing-controls-from-taskrun}

```csharp
// WRONG: Accessing UI from background thread
await Task.Run(() =>
{
    StatusText.Text = "Done"; // Throws InvalidOperationException
});

// CORRECT: Update UI after awaiting the background work
var result = await Task.Run(() => ComputeResult());
StatusText.Text = result; // Runs on UI thread after await
```

### 在后台线程中修改集合 {#modifying-collections-from-a-background-thread}

在后台线程里修改已绑定的 `ObservableCollection` 并不一定会抛异常，更常见的是项被悄悄丢掉或只添加了一部分，让问题很难查：

```csharp
// WRONG: Collection changes may be silently lost
await Task.Run(async () =>
{
    foreach (var item in loadedItems)
    {
        Items.Add(item); // May only add the first item
    }
});

// CORRECT: Load data on background thread, update collection on UI thread
var data = await Task.Run(() => LoadItems());
Items = new ObservableCollection<Item>(data);

// ALSO CORRECT: Dispatch each addition if you need incremental updates
foreach (var item in loadedItems)
{
    await Dispatcher.UIThread.InvokeAsync(() => Items.Add(item));
}
```

如果你的 `async` 方法起始于 UI 线程，那么 `await` 之后的代码会自动回到 UI 线程（参见 [SynchronizationContext](#async-patterns)），这段后续代码里修改集合无需显式调度。出问题的情形是：方法整个跑在后台线程上，或者调用链上更早的地方用了 `ConfigureAwait(false)`。

### 阻塞 UI 线程 {#blocking-the-ui-thread}

```csharp
// WRONG: Blocks the UI thread, making the app unresponsive
var data = LoadDataFromNetwork().Result; // Deadlock risk!

// CORRECT: Use async/await
var data = await LoadDataFromNetworkAsync();
```

### 多此一举的调度 {#unnecessary-dispatching}

```csharp
// UNNECESSARY: Already on UI thread in event handlers
private void OnButtonClick(object? sender, RoutedEventArgs e)
{
    // No need to dispatch - event handlers run on the UI thread
    StatusText.Text = "Clicked";
}
```

## 另请参阅 {#see-also}

- [`Dispatcher` API 参考](/api/avalonia/threading/dispatcher)
- [应用生命周期](/docs/fundamentals/application-lifetimes)：应用生命周期与线程模型的关系。
