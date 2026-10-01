---
id: commanding
title: 命令
description: 用 ICommand 编写命令，把用户动作接到视图模型的逻辑上。
doc-type: explanation
---

命令机制把用户动作（按钮点击、菜单选择、键盘快捷键）接到视图模型中的逻辑上。Avalonia 采用标准的 .NET `ICommand` 接口，从而把界面与业务逻辑干净地分开。

## 命令机制的运作原理 {#how-commanding-works}

支持命令的控件（比如 `Button` 和 `MenuItem`）都有一个 `Command` 属性。用户激活控件时，它会调用 `ICommand.Execute`。控件还会盯着 `ICommand.CanExecute`，在命令无法执行时自动把自己禁用。

```xml
<Button Content="Save" Command="{Binding SaveCommand}" />
```

当 `SaveCommand.CanExecute()` 返回 `false` 时，按钮会显示为禁用状态，点也点不动。

## ICommand 接口 {#icommand-interface}

`System.Windows.Input.ICommand` 接口定义了：

```csharp
public interface ICommand
{
    bool CanExecute(object? parameter);
    void Execute(object? parameter);
    event EventHandler? CanExecuteChanged;
}
```

| 成员 | 用途 |
|---|---|
| `CanExecute` | 返回命令当前能否执行。控件靠它来决定自己是启用还是禁用。 |
| `Execute` | 执行命令的动作。用户激活控件时由控件调用。 |
| `CanExecuteChanged` | 当 `CanExecute` 的返回值可能已变化时引发。控件监听这个事件，以便重新查询 `CanExecute`。 |

## Using RelayCommand (CommunityToolkit.Mvvm)

创建命令最常见的办法，是使用 CommunityToolkit.Mvvm 包中的 `[RelayCommand]` 特性：

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private string _name = "";

    [RelayCommand]
    private void Save()
    {
        // Save logic here
    }

    [RelayCommand(CanExecute = nameof(CanDelete))]
    private void Delete()
    {
        // Delete logic here
    }

    private bool CanDelete() => !string.IsNullOrEmpty(Name);
}
```

源生成器会自动造出 `SaveCommand` 和 `DeleteCommand` 属性。每当 `CanExecuteChanged` 被引发时，`DeleteCommand` 都会重新判定 `CanDelete()`。

```xml
<StackPanel Spacing="8">
    <TextBox Text="{Binding Name}" />
    <Button Content="Save" Command="{Binding SaveCommand}" />
    <Button Content="Delete" Command="{Binding DeleteCommand}" />
</StackPanel>
```

### 异步命令 {#async-commands}

`[RelayCommand]` 特性同样支持异步方法。生成的命令会处理 `Task` 返回类型，并自动跟踪忙碌状态：

```csharp
[RelayCommand]
private async Task LoadDataAsync()
{
    IsLoading = true;
    try
    {
        var data = await _dataService.GetDataAsync();
        Items = new ObservableCollection<Item>(data);
    }
    finally
    {
        IsLoading = false;
    }
}
```

`LoadDataAsync` 运行期间，`LoadDataCommand.IsRunning` 为 `true`。你可以把进度指示器绑定到它上面。

### Notifying CanExecute

当影响 `CanExecute` 的属性发生变化时，请使用 `[NotifyCanExecuteChangedFor]`：

```csharp
[ObservableProperty]
[NotifyCanExecuteChangedFor(nameof(DeleteCommand))]
private string _name = "";
```

这会让源生成器在 `Name` 变化时引发 `DeleteCommand.NotifyCanExecuteChanged()`，于是绑定了该命令的控件会重新判定它能否执行。

## CommandParameter

`CommandParameter` 属性把数据传给命令的 `Execute` 和 `CanExecute` 方法：

```xml
<Button Content="Open"
        Command="{Binding OpenCommand}"
        CommandParameter="{Binding SelectedItem}" />
```

```csharp
[RelayCommand]
private void Open(object? parameter)
{
    if (parameter is Item item)
    {
        // Open the item
    }
}
```

用 CommunityToolkit.Mvvm 搭配带类型的参数：

```csharp
[RelayCommand]
private void Open(Item item)
{
    // The source generator creates OpenCommand as RelayCommand<Item>
}
```

```xml
<Button Content="Open"
        Command="{Binding OpenCommand}"
        CommandParameter="{Binding SelectedItem}" />
```

## 手写 ICommand 实现 {#manual-icommand-implementation}

若场景中用不了源生成器，可以手动创建命令：

```csharp
public class RelayCommand : ICommand
{
    private readonly Action _execute;
    private readonly Func<bool>? _canExecute;

    public RelayCommand(Action execute, Func<bool>? canExecute = null)
    {
        _execute = execute;
        _canExecute = canExecute;
    }

    public bool CanExecute(object? parameter) => _canExecute?.Invoke() ?? true;

    public void Execute(object? parameter) => _execute();

    public event EventHandler? CanExecuteChanged;

    public void RaiseCanExecuteChanged()
        => CanExecuteChanged?.Invoke(this, EventArgs.Empty);
}
```

```csharp
public class MainViewModel
{
    public ICommand SaveCommand { get; }

    public MainViewModel()
    {
        SaveCommand = new RelayCommand(
            execute: () => { /* save logic */ },
            canExecute: () => IsModified);
    }
}
```

## 键盘快捷键与命令 {#keyboard-shortcuts-and-commands}

用 `KeyBinding` 把命令绑定到键盘快捷键：

```xml
<Window.KeyBindings>
    <KeyBinding Gesture="Ctrl+S" Command="{Binding SaveCommand}" />
    <KeyBinding Gesture="Ctrl+Z" Command="{Binding UndoCommand}" />
    <KeyBinding Gesture="Delete" Command="{Binding DeleteCommand}" />
</Window.KeyBindings>
```

`KeyBinding` 会判定 `CanExecute`，只有在手势被按下且命令可用时才触发命令。

## HotKey 附加属性 {#hotkey-attached-property}

对控件来说，`HotKey` 附加属性的写法更简单：

```xml
<Button Content="_Save"
        Command="{Binding SaveCommand}"
        HotKey="Ctrl+S" />
```

即便按钮没有焦点，`HotKey` 也能触发它的命令。

## 另请参阅 {#see-also}

- [绑定到命令](/docs/data-binding/binding-to-commands)：绑定语法、把 `Command` 直接绑到方法，以及 `CommandParameter`。
- [如何绑定 CanExecute](/docs/data-binding/how-to-bind-can-execute)：用 `CanExecute` 控制按钮可用状态的完整示例。
- [添加交互](/docs/input-interaction/adding-interactivity)：事件和命令之间该怎么选。
- [键盘与快捷键](/docs/input-interaction/keyboard-and-hotkeys)：按键绑定与键盘输入。
- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)：把界面与逻辑分开的架构。
