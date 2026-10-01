---
id: how-to-bind-to-an-observable
title: 如何绑定到可观察序列
description: 把控件属性绑定到 IObservable 流，实现界面的响应式更新。
doc-type: how-to
---

Avalonia 支持用 `^`（流绑定）运算符直接绑定到 `IObservable<T>` 属性。可观察序列每推出一个新值，绑定就自动更新一次。

## 何时使用可观察序列绑定 {#when-to-use-observable-bindings}

当数据是随时间持续流入的值序列时，就该用 `IObservable<T>` 绑定。常见场景包括：

- **实时数据源**，比如时钟、传感器读数或股票行情。
- **响应式搜索** —— 在请求服务之前，对用户输入做节流、防抖或变换。
- **事件驱动的状态** —— 值是被推送过来的，而不是你主动去取的。

对于大多数随用户操作而变化的视图模型属性，用一个会引发 `INotifyPropertyChanged` 的普通属性（或 Avalonia 的 `StyledProperty` / `DirectProperty`）更简单，也完全够用。只有当你确实能从 `System.Reactive` 提供的组合运算符（如 `Throttle`、`DistinctUntilChanged`、`CombineLatest`、`Switch`）中获益时，才值得改用可观察序列。

## 基本的可观察序列绑定 {#basic-observable-binding}

若 `DataContext.Name` 是一个 `IObservable<string>`，可以直接绑定到它的当前值：

```xml
<TextBlock Text="{Binding Name^}" />
```

`^` 运算符会订阅该可观察序列，每推出一个新值就刷新一次控件。

## 绑定到所推出值的某个属性 {#binding-to-a-property-of-the-emitted-value}

可以在 `^` 运算符之后继续访问属性。例如，绑定到所产出的每个字符串的 `Length`：

```xml
<TextBlock Text="{Binding Name^.Length}" />
```

## 示例：用可观察序列实现时钟 {#example-clock-using-an-observable}

```csharp
public class ClockViewModel
{
    public IObservable<string> CurrentTime { get; } =
        Observable.Interval(TimeSpan.FromSeconds(1))
            .Select(_ => DateTime.Now.ToString("HH:mm:ss"));
}
```

```xml
<TextBlock Text="{Binding CurrentTime^}" FontSize="24" />
```

## 示例：搜索结果流 {#example-search-results-stream}

```csharp
public class SearchViewModel
{
    private readonly Subject<string> _searchText = new();

    public IObservable<IReadOnlyList<string>> Results { get; }

    public SearchViewModel()
    {
        Results = _searchText
            .Throttle(TimeSpan.FromMilliseconds(300))
            .DistinctUntilChanged()
            .SelectMany(query => SearchAsync(query));
    }

    public void OnSearchTextChanged(string text) => _searchText.OnNext(text);

    private async Task<IReadOnlyList<string>> SearchAsync(string query)
    {
        // Perform search
        return new[] { $"Result for '{query}'" };
    }
}
```

```xml
<ListBox ItemsSource="{Binding Results^}" />
```

## 用 FallbackValue 处理初始状态 {#fallbackvalue-for-initial-state}

可观察序列可能还没推出过任何值，这时可以用 `FallbackValue` 显示一个占位内容：

```xml
<TextBlock Text="{Binding CurrentTime^, FallbackValue='Loading...'}" />
```

## 与任务绑定配合 {#combining-with-task-binding}

`^` 运算符同样适用于 `Task<T>` 属性，详见[如何绑定到任务结果](/docs/data-binding/how-to-bind-to-a-task-result)。

## 清理与释放 {#cleanup-and-disposal}

绑定激活时，Avalonia 会自动订阅你的 `IObservable<T>`；当绑定的控件从视觉树中移除时又会自动退订。大多数情况下，你不需要自己管理订阅。

但请留意以下几点：

- **热可观察序列**（如 `Subject<T>`）只要还有人引用就会一直存活。如果该序列由一个长生命周期的服务持有，务必确保视图销毁之后视图模型不会把它一直吊着。
- **冷可观察序列**（如 `Observable.Interval`）每次订阅都会新建一份。由于控件分离时 Avalonia 会释放订阅，不需要手动清理。
- 如果你的视图模型实现了 `IDisposable`，并且在 XAML 绑定之外还创建了订阅（比如在构造函数中为派生属性订阅），请在 `Dispose` 方法中释放这些订阅，以免内存泄漏。

## 另请参阅 {#see-also}

- [如何绑定到任务结果](/docs/data-binding/how-to-bind-to-a-task-result)
- [数据绑定语法](/docs/data-binding/data-binding-syntax)
