---
id: how-to-bind-can-execute
title: 如何绑定 CanExecute
description: 绑定到命令的 CanExecute 方法，让按钮自动在可用与禁用之间切换。
doc-type: how-to
---

import BindCanExecuteScreenshot from '/img/guides/data/bind-canexecute.gif';

## 概述 {#overview}

一个能发起操作的控件当下是否可用，是用户体验设计中「功能可见性」的关键一环。把执行不了的命令置灰，能增强用户的信心。举例来说，如果某个按钮或菜单项因为应用处于错误状态而无法执行，就该把它显示成非激活状态，而不是等用户点下去再报错。

本文介绍如何把 [`Button`](/api/avalonia/controls/button) 绑定到一个命令上，由该命令的 `CanExecute` 逻辑自动决定控件的可用与禁用。整个做法遵循 MVVM 模式，视图和视图模型始终划分清楚。

## 前置条件 {#prerequisites}

- 一个采用 MVVM 结构的基础 Avalonia 应用（含一个视图和与之对应的视图模型）。
- 了解[数据绑定](/docs/data-binding/introduction-to-data-binding)和 `ICommand`。

## Example

本例中，只有消息不为空时按钮才可点击。操作一旦执行，消息就被重置为空字符串，按钮随即再次禁用。

### 定义视图 {#define-the-view}

`TextBox` 绑定到 `Message` 属性，`Button` 则把自己的 `Command` 绑定到 `ExampleCommand`。Avalonia 会根据命令 `CanExecute` 方法的返回值，自动设置按钮的 `IsEnabled` 状态。

```xml title='MainWindow.axaml'
<StackPanel Margin="20">
  <TextBox Margin="0 5" Text="{Binding Message}"
           PlaceholderText="Add a message to enable the button"/>
  <Button Command="{Binding ExampleCommand}">
    Run the example
  </Button>
  <TextBlock Margin="0 5" Text="{Binding Output}" />
</StackPanel>
```

### 写一个简单的 `RelayCommand` {#create-a-simple-relaycommand}

如果你没有用 CommunityToolkit.Mvvm 或 ReactiveUI 这类框架，也可以自己实现一个轻量的 `RelayCommand`。下面这个类用一个 `Action` 承担执行逻辑，再用一个可选的 `Func<bool>` 负责「能否执行」的判断。

```csharp title='RelayCommand.cs'
using System;
using System.Windows.Input;

namespace AvaloniaGuides.ViewModels
{
    public class RelayCommand : ICommand
    {
        private readonly Action _execute;
        private readonly Func<bool>? _canExecute;

        public RelayCommand(Action execute, Func<bool>? canExecute = null)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public event EventHandler? CanExecuteChanged;

        public bool CanExecute(object? parameter) => _canExecute?.Invoke() ?? true;

        public void Execute(object? parameter) => _execute();

        public void RaiseCanExecuteChanged() =>
            CanExecuteChanged?.Invoke(this, EventArgs.Empty);
    }
}
```

### 实现视图模型 {#implement-the-view-model}

构造函数中创建命令时传入两个参数：要执行的操作，以及判断命令能否执行的函数。每当 `Message` 发生变化，属性的 setter 就调用 `RaiseCanExecuteChanged`，于是绑定系统会重新评估按钮的可用状态。

```csharp title='MainWindowViewModel.cs'
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace AvaloniaGuides.ViewModels
{
    public class MainWindowViewModel : INotifyPropertyChanged
    {
        private string _message = string.Empty;
        private string _output = "Waiting...";

        public event PropertyChangedEventHandler? PropertyChanged;

        public string Message
        {
            get => _message;
            set
            {
                if (_message != value)
                {
                    _message = value;
                    OnPropertyChanged();
                    ExampleCommand.RaiseCanExecuteChanged();
                }
            }
        }

        public string Output
        {
            get => _output;
            set
            {
                if (_output != value)
                {
                    _output = value;
                    OnPropertyChanged();
                }
            }
        }

        public RelayCommand ExampleCommand { get; }

        public MainWindowViewModel()
        {
            ExampleCommand = new RelayCommand(
                PerformAction,
                () => !string.IsNullOrWhiteSpace(Message));
        }

        private void PerformAction()
        {
            Output = $"The action was called. {Message}";
            Message = string.Empty;
        }

        protected void OnPropertyChanged([CallerMemberName] string? name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }
}
```

<Image light={BindCanExecuteScreenshot} alt="App showing a button enabled and disabled based on CanExecute binding" position="center" maxWidth={400} cornerRadius="true"/>

## 运作原理 {#how-it-works}

1. 用户在 `TextBox` 中输入时，`Message` 属性的 setter 被触发。
2. setter 调用 `ExampleCommand.RaiseCanExecuteChanged()`，后者引发 `CanExecuteChanged` 事件。
3. Avalonia 响应该事件，调用命令上的 `CanExecute`。若该方法返回 `false`，绑定的 `Button` 就自动置为禁用。
4. 当用户清空文本（或操作把 `Message` 重置为空字符串）时，`CanExecute` 返回 `false`，按钮再次禁用。

## 注意事项与边界情况 {#tips-and-edge-cases}

- **凡是 `CanExecute` 函数依赖的属性，其 setter 中都要调用 `RaiseCanExecuteChanged`**（或等效的通知）。漏掉的话，按钮状态会一直停留在旧值，直到别的事件触发重新评估。
- **多个依赖项。** 如果 `CanExecute` 检查了不止一个属性，那么这些属性的 setter 中都要调用 `RaiseCanExecuteChanged`。
- **线程安全。** `CanExecuteChanged` 应当在 UI 线程上引发。若你在后台线程更新属性，请先用 `Dispatcher.UIThread.Post` 把变更调度回 UI 线程。
- **使用 CommunityToolkit.Mvvm。** `[RelayCommand(CanExecute = nameof(CanRun))]` 源生成器可以免去上面那堆样板代码。你调用 `NotifyCanExecuteChanged()` 时，生成的命令会自动引发 `CanExecuteChanged`。
- **使用 ReactiveUI。** `ReactiveCommand.Create` 接受一个 `canExecute` 可观察序列。每当该序列推出新值，命令就自动重新评估，无需你手动引发事件。
- **`CommandParameter` 绑定。** 通过绑定传入 `CommandParameter` 时，参数值会被转交给 `CanExecute(object? parameter)`。请确保你的实现能应对初次布局阶段的 `null` 参数 —— 那时绑定系统还没把参数值解析出来。
- **菜单项。** 同样的写法对 `MenuItem` 一样适用。把 `MenuItem.Command` 绑定到你的命令，`CanExecute` 返回 `false` 时菜单项会自动置灰。

## 另请参阅 {#see-also}

- [绑定到命令](/docs/data-binding/binding-to-commands)
- [Commanding](/docs/input-interaction/commanding)
- [数据绑定总览](/docs/data-binding/introduction-to-data-binding)
