---
id: adding-interactivity
title: 加入交互
doc-type: how-to
description: 用事件和命令为你的应用加入交互元素。
---

本指南用简单的例子介绍事件和命令。有了它们，你的应用才有交互可言——用户才能在界面上点击、输入、选择等等。

## 处理事件 {#handling-events}

Avalonia 中的事件让你能响应用户交互和控件特有的动作。处理事件的步骤如下：

1. **编写事件处理程序：**在[代码隐藏](/docs/fundamentals/code-behind)中写一个事件处理程序。事件触发时它就会执行，里面放的正是你想作出的响应逻辑。

2. **订阅事件：**先确定你要处理控件的哪个事件。Avalonia 中多数控件都公开了 `Click`、`SelectionChanged` 之类的事件。在 XAML 中订阅的办法是：加一个以事件名为名的特性，把它的值设成事件处理程序方法的名字。

下面这个例子为按钮的 `Click` 事件挂上了名为 `HandleButtonClick` 的处理程序。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
    <Button Name="myButton"
            Content="Click me"
            Margin="20"
            Click="HandleButtonClick" />
</UserControl>
```

```csharp
using Avalonia.Controls;
using Avalonia.Interactivity;

public partial class MyButton : UserControl
{
    private void HandleButtonClick(object? sender, RoutedEventArgs e)
    {
        if (sender is Button button)
        {
            button.Content = "Clicked!";
        }
    }
}

```

</XamlPreview>

## 使用命令 {#using-commands}

Avalonia 中的命令提供了一种更高层的交互处理方式，把用户动作与实现逻辑解耦开来。事件定义在控件的代码隐藏里，而命令通常绑定到[数据上下文](/docs/data-binding/data-context)上的某个属性或方法。

凡是带 `Command` 属性的控件都能用命令。命令一般在控件的主要交互方式发生时触发，比如按钮被点击。

### 绑定到方法 {#binding-to-a-method}

用命令最简单的办法，就是绑定到对象数据上下文中的某个方法。

1. **往数据上下文里加一个方法：**在数据上下文中定义一个方法来处理该命令。在 MVVM 应用里，数据上下文通常就是视图模型。

2. **绑定这个方法：**把方法与触发它的控件关联起来。

```xml title="XAML"
<Button Content="Save" Command="{Binding Save}" />
```

```csharp title="Data context"
public void Save()
{
    // Save logic
}
```

:::note
若该方法有[重载](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/member-overloading)，Avalonia 会按一套固定规则挑出其中之一。请参阅[直接绑定到方法](/docs/data-binding/binding-to-commands#binding-directly-to-a-method)。
:::

### `CommunityToolkit.Mvvm`

命令也可以定义成视图模型上的 `ICommand` 对象。推荐用 `CommunityToolkit.Mvvm` 中的 `[RelayCommand]` 特性来创建它们。

命令怎么写请参阅[命令](/docs/input-interaction/commanding)；绑定语法（包括如何用 `CommandParameter` 传数据）请参阅[绑定到命令](/docs/data-binding/binding-to-commands)。

```xml title="XAML"
<Button Content="Save" Command="{Binding SaveCommand}" />
```

```csharp title="View model"
public partial class MainViewModel : ObservableObject
{
    [RelayCommand]
    private void Save()
    {
        // Save logic
    }
}
```

## 事件与命令的取舍 {#events-vs-commands}

| &nbsp; | 事件 | 命令 |
|---|---|---|
| 定义位置 | Code-behind | 数据上下文 |
| Testable | 困难（得把界面跑起来） | 容易（就是个普通的 C# 方法） |
| 适用场景 | 控件特有的动作（拖动、调整尺寸） | 应用逻辑（保存、导航、删除） |
| MVVM 写法 | 不推荐 | Preferred |

## 另请参阅 {#see-also}

- [命令](/docs/input-interaction/commanding)：怎么写命令——`ICommand`、`CanExecute` 以及异步命令。
- [绑定到命令](/docs/data-binding/binding-to-commands)：绑定语法、方法绑定与 `CommandParameter`。
- [路由事件](/docs/input-interaction/routed-events)：事件如何在控件树中传递。
- [键盘与快捷键](/docs/input-interaction/keyboard-and-hotkeys)：命令的按键绑定。
