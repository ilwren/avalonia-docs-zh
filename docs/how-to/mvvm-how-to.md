---
id: mvvm-how-to
title: "操作指南：实现常见的 MVVM 套路"
description: 学会在 Avalonia 中用 CommunityToolkit.Mvvm 实现常见的 MVVM 套路，包括可观察属性、命令、消息传递、依赖注入与校验。
doc-type: how-to
---

本指南介绍在 Avalonia 中使用 `CommunityToolkit.Mvvm`（推荐的 MVVM 框架）的实用套路。每一节都带你走一遍某个具体做法，代码可以直接改到你自己的项目里。

## 配置 CommunityToolkit.Mvvm {#setting-up-communitytoolkitmvvm}

在项目中安装 NuGet 包：

```bash
dotnet add package CommunityToolkit.Mvvm
```

装好之后，你就能用这个工具包的源生成器和基类，省去视图模型里的大量样板代码。

## 可观察属性 {#observable-properties}

用 `[ObservableProperty]` 特性自动生成带 `INotifyPropertyChanged` 支持的属性。你只需声明一个私有的后备字段，源生成器就会替你造出公共属性：

```csharp
using CommunityToolkit.Mvvm.ComponentModel;

public partial class PersonViewModel : ObservableObject
{
    [ObservableProperty]
    private string _firstName = "";

    [ObservableProperty]
    private string _lastName = "";

    // Generated: FirstName and LastName properties with INotifyPropertyChanged
}
```

你的类必须标记为 `partial`，源生成器才能往里面添加生成的成员。生成的属性名遵循 .NET 惯例：`_firstName` 会变成 `FirstName`。

### 计算属性 {#computed-properties}

当一个属性依赖另一个属性时，用 `[NotifyPropertyChangedFor]` 自动为依赖方引发变更通知：

```csharp
[ObservableProperty]
[NotifyPropertyChangedFor(nameof(FullName))]
private string _firstName = "";

[ObservableProperty]
[NotifyPropertyChangedFor(nameof(FullName))]
private string _lastName = "";

public string FullName => $"{FirstName} {LastName}";
```

`FirstName` 或 `LastName` 一变，工具包就会顺带为 `FullName` 引发 `PropertyChanged`，让界面保持同步。

### 属性变更回调 {#property-changed-callbacks}

定义若干分部方法，源生成器会自动调用它们，你就能在属性变化时执行代码：

```csharp
[ObservableProperty]
private string _searchText = "";

partial void OnSearchTextChanged(string value)
{
    // Called after SearchText changes
    ApplyFilter(value);
}

partial void OnSearchTextChanging(string value)
{
    // Called before SearchText changes
}
```

`OnSearchTextChanging` 回调在赋值之前触发，让你有机会检视传进来的值；`OnSearchTextChanged` 回调在赋值之后触发，适合用来引发筛选列表之类的副作用。

## Commands

命令让你能把界面上的操作（比如按钮点击）绑定到视图模型中的方法。

### 基本命令 {#basic-command}

给方法加上 `[RelayCommand]`，工具包就会替你生成一个 `IRelayCommand` 属性：

```csharp
[RelayCommand]
private void Save()
{
    _repository.Save(CurrentItem);
}
```

这会生成一个 `SaveCommand` 属性。命名惯例是在你的方法名后面加上「Command」。

### 带参数的命令 {#command-with-a-parameter}

给方法加一个参数，就能把数据从视图传给命令：

```csharp
[RelayCommand]
private void Delete(Item item)
{
    Items.Remove(item);
}
```

在 AXAML 中绑定命令及其参数：

```xml
<Button Content="Delete"
        Command="{Binding DeleteCommand}"
        CommandParameter="{Binding SelectedItem}" />
```

### 异步命令 {#async-command}

耗时较久的操作请用 `async Task` 方法。工具包会在执行期间自动禁用该命令，并内置了取消支持：

```csharp
[RelayCommand]
private async Task LoadDataAsync(CancellationToken token)
{
    IsLoading = true;
    var data = await _api.FetchDataAsync(token);
    Items = new ObservableCollection<Item>(data);
    IsLoading = false;
}
```

生成的命令会自动：

- 在任务运行期间禁用与之关联的按钮
- 传入一个 `CancellationToken`，供你取消操作
- 公开一个 `IsRunning` 属性，便于显示进度

```xml
<Button Content="Load" Command="{Binding LoadDataCommand}" />
<ProgressBar IsVisible="{Binding LoadDataCommand.IsRunning}" IsIndeterminate="True" />
```

### CanExecute

你可以根据视图模型的状态有条件地启用或禁用命令。给影响该条件的属性加上 `[NotifyCanExecuteChangedFor]`，命令就会自动重新判定：

```csharp
[ObservableProperty]
[NotifyCanExecuteChangedFor(nameof(SaveCommand))]
private string _name = "";

[RelayCommand(CanExecute = nameof(CanSave))]
private void Save()
{
    // Save logic
}

private bool CanSave() => !string.IsNullOrWhiteSpace(Name);
```

当 `CanSave()` 返回 `false` 时，绑定到 `SaveCommand` 的按钮会自动禁用。`Name` 一变，命令便重新判定自己能否执行。

## 视图模型之间的通信 {#view-model-communication}

### 使用 messenger {#using-a-messenger}

`WeakReferenceMessenger` 让你在视图模型之间收发消息，而不必让它们彼此持有引用，从而保持解耦：

```csharp
using CommunityToolkit.Mvvm.Messaging;

// Define a message
public record ItemSelectedMessage(Item Item);

// Send from one view model
WeakReferenceMessenger.Default.Send(new ItemSelectedMessage(selectedItem));

// Receive in another
public class DetailViewModel : ObservableRecipient, IRecipient<ItemSelectedMessage>
{
    public DetailViewModel()
    {
        IsActive = true; // Start receiving messages
    }

    public void Receive(ItemSelectedMessage message)
    {
        LoadItem(message.Item);
    }
}
```

设置 `IsActive = true` 会把视图模型注册为消息接收方。当你把它设为 `false`（或该对象被垃圾回收）时，注册会自动解除。

### 请求/响应模式 {#requestresponse-pattern}

若某个场景需要拿到回复（比如确认对话框），请使用请求消息：

```csharp
public record ConfirmDeleteRequest(Item Item);

// Request
var confirmed = WeakReferenceMessenger.Default
    .Send(new ConfirmDeleteRequest(item));

// Response handler (in the view or a coordinator)
WeakReferenceMessenger.Default.Register<ConfirmDeleteRequest>(this, async (r, m) =>
{
    // Show confirmation dialog
    m.Reply(await ShowConfirmDialogAsync());
});
```

## 依赖注入 {#dependency-injection}

把视图模型和服务注册到 DI 容器里，干净利落地管理它们的生命周期与依赖：

```csharp
public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddViewModels(this IServiceCollection services)
    {
        services.AddTransient<MainViewModel>();
        services.AddTransient<SettingsViewModel>();
        services.AddSingleton<IDataService, DataService>();
        return services;
    }
}
```

在 `App.axaml.cs` 中搭好容器：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    var services = new ServiceCollection();
    services.AddViewModels();
    var provider = services.BuildServiceProvider();

    if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
    {
        desktop.MainWindow = new MainWindow
        {
            DataContext = provider.GetRequiredService<MainViewModel>()
        };
    }

    base.OnFrameworkInitializationCompleted();
}
```

每次都应新建的视图模型用 `AddTransient`；需要跨应用维持状态的共享服务用 `AddSingleton`。

## 通过构造函数注入的视图模型 {#view-model-with-constructor-injection}

把视图模型注册进 DI 容器之后，你就能通过构造函数注入服务，容器会自动解析全部依赖：

```csharp
public partial class MainViewModel : ObservableObject
{
    private readonly IDataService _dataService;
    private readonly INavigationService _navigation;

    public MainViewModel(IDataService dataService, INavigationService navigation)
    {
        _dataService = dataService;
        _navigation = navigation;
    }

    [RelayCommand]
    private async Task LoadAsync()
    {
        var items = await _dataService.GetItemsAsync();
        Items = new ObservableCollection<Item>(items);
    }
}
```

这种写法让视图模型变得可测试——在单元测试里，你可以把 `IDataService` 和 `INavigationService` 换成模拟实现。

## ObservableCollection 的用法 {#observablecollection-patterns}

### 整体替换还是逐项添加 {#replace-vs-add}

要更新大量项目时，整体替换集合比逐个添加快得多。每调用一次 `Add` 都会触发一次界面更新，而赋一个新集合只触发一次：

```csharp
// Slow: UI updates on each Add
foreach (var item in newItems)
    Items.Add(item);

// Fast: single notification
Items = new ObservableCollection<Item>(newItems);
```

### 筛选后的集合 {#filtered-collection}

筛选的做法很简单：筛选文本一变，就把展示用的集合换掉：

```csharp
[ObservableProperty]
private string _filter = "";

[ObservableProperty]
private ObservableCollection<Item> _filteredItems = new();

partial void OnFilterChanged(string value)
{
    FilteredItems = new ObservableCollection<Item>(
        _allItems.Where(i => i.Name.Contains(value, StringComparison.OrdinalIgnoreCase)));
}
```

请把 `ItemsControl` 或 `ListBox` 绑定到 `FilteredItems`，而不是底层的 `_allItems` 集合。

## Validation

把 `ObservableValidator` 用作基类，即可为视图模型的属性启用数据注解校验：

```csharp
public partial class RegisterViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "Name is required")]
    private string _name = "";

    [RelayCommand]
    private void Submit()
    {
        ValidateAllProperties();
        if (!HasErrors)
        {
            // Proceed with submission
        }
    }
}
```

`[NotifyDataErrorInfo]` 特性告诉源生成器：属性变化时自动触发校验。Avalonia 的数据绑定系统会接住这些校验错误，并可借助 `DataValidationErrors` 把它们显示在界面上。

关于如何在视图中显示校验错误，请参阅[数据绑定中的校验](/docs/data-binding/binding-validation)。

## 另请参阅 {#see-also}

- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)
- [绑定到命令](/docs/data-binding/binding-to-commands)
- [INotifyPropertyChanged](/docs/data-binding/inotifypropertychanged)
- [依赖注入](/docs/app-development/dependency-injection)
- [数据绑定中的校验](/docs/data-binding/binding-validation)
