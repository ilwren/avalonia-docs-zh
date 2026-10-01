---
id: how-to-bind-to-a-task-result
title: 如何绑定到任务结果
description: 把控件属性绑定到异步 Task 的结果，任务完成时自动显示数据。
doc-type: how-to
---

Avalonia 可以用 `^`（流绑定）运算符直接绑定到 `Task<T>` 属性。任务一完成，绑定就把结果显示出来，于是你无需手动更新属性即可异步加载数据。

## 基本的任务绑定 {#basic-task-binding}

如果加载某个属性值需要做比较重的工作，可以直接绑定到 `async Task<TResult>` 的结果。

在视图模型上把任务定义成一个属性：

```csharp
public Task<string> MyAsyncText => GetTextAsync();

private async Task<string> GetTextAsync()
{
    await Task.Delay(1000); // Simulates a long-running operation
    return "Hello from async operation";
}
```

用 `^` 运算符绑定到它的结果：

```xml
<TextBlock Text="{Binding MyAsyncText^, FallbackValue='Loading...'}" />
```

任务尚在执行期间显示的是 `FallbackValue`；任务一完成，结果就取而代之。

:::tip
任务绑定一定要设置 `FallbackValue`。否则在任务完成之前，绑定属性会一直保持默认值（通常是 `null` 或空），可能造成布局跳动或控件空白。
:::

## 从 API 加载数据 {#loading-data-from-an-api}

一个常见场景是在视图模型创建时就开始加载数据：

```csharp
public class UserProfileViewModel
{
    public Task<UserProfile> Profile { get; }

    public UserProfileViewModel(IUserService userService)
    {
        Profile = userService.GetCurrentUserAsync();
    }
}
```

在 `^` 运算符之后用点号，可以继续绑定任务结果的子属性：

```xml
<StackPanel>
    <TextBlock Text="{Binding Profile^.Name, FallbackValue='Loading profile...'}" />
    <TextBlock Text="{Binding Profile^.Email}" />
</StackPanel>
```

## 显示加载指示器 {#showing-a-loading-indicator}

可以用 `FallbackValue`，或者把可见性绑定起来，在加载期间显示一个转圈的指示器：

```xml
<Panel>
    <ProgressBar IsIndeterminate="True"
                 IsVisible="{Binding !Profile^, FallbackValue=True}" />
    <TextBlock Text="{Binding Profile^.Name}"
               IsVisible="{Binding !!Profile^, FallbackValue=False}" />
</Panel>
```

`!` 前缀会把绑定值取反。任务未完成时，`Profile^` 求值为 `null`，于是 `!Profile^` 为 `True`，进度条可见。而 `!!` 这样的双重取反会把结果转回布尔值，因此只有当任务完成且结果非 null 时，`!!Profile^` 才变为 `True`。

## 刷新任务数据 {#refreshing-task-data}

由于一个 `Task<T>` 只能完成一次，每次想刷新数据，都得新建一个任务实例。记得引发 `PropertyChanged`，绑定才会接上新任务：

```csharp
public class RefreshableViewModel : INotifyPropertyChanged
{
    private readonly IUserService _userService;
    private Task<UserProfile>? _profile;

    public event PropertyChangedEventHandler? PropertyChanged;

    public Task<UserProfile>? Profile
    {
        get => _profile;
        private set
        {
            _profile = value;
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Profile)));
        }
    }

    public RefreshableViewModel(IUserService userService)
    {
        _userService = userService;
        Refresh();
    }

    public void Refresh()
    {
        Profile = _userService.GetCurrentUserAsync();
    }
}
```

每调用一次 `Refresh()` 就会赋上一个新的 `Task<UserProfile>`，绑定随即自动订阅这个新任务。

## 边界情况与限制 {#edge-cases-and-limitations}

使用任务绑定时，请留意以下几点：

- **任务失败：** 任务抛出异常时，界面上仍停留在 `FallbackValue`，Avalonia 不会把异常呈现到界面上。如果需要展示错误状态，可以在视图模型里捕获错误，并单独用一个属性暴露错误信息。
- **任务被取消：** 行为与任务失败类似 —— `FallbackValue` 继续显示，绑定拿不到任何结果。
- **已完成的任务：** 绑定到一个已经完成的任务时，结果会立即显示，没有延迟。
- **结果为 null：** 若任务以 `null` 结果完成，绑定值即为 `null`。这种情况下若想显示特定内容，请给绑定设置 `TargetNullValue`。
- **线程安全：** `^` 运算符内部用 `SynchronizationContext` 把结果调度回 UI 线程，你不必自己处理线程切换。
- **编译绑定：** 带 `^` 运算符的任务绑定可以配合编译绑定使用。请在视图上用 `x:DataType` 指明类型，确保编译期能看到任务属性的类型。

:::warning
不要把任务属性写成每次访问 getter 都新建一个 `Task` 的方法调用（例如 `public Task<string> Data => LoadAsync();`）。绑定系统每读一次属性就会创建一个新任务，可能导致网络请求被反复发起，或引发其他意料之外的副作用。正确做法是把任务存进支持字段，或者在构造函数中赋值一次。
:::

## 另请参阅 {#see-also}

- [如何绑定到可观察序列](/docs/data-binding/how-to-bind-to-an-observable)
- [数据绑定语法](/docs/data-binding/data-binding-syntax)
- [编译绑定](/docs/data-binding/compiled-bindings)
