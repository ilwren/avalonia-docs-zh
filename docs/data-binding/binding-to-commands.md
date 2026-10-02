---
id: binding-to-commands
title: 绑定到命令
description: 按 MVVM 模式把界面控件绑定到命令，以响应用户操作。
doc-type: explanation
---

命令把用户交互和代码里的逻辑连在一起。本文讲的是绑定如何抵达命令：绑定语法、`Command` 绑定怎样解析出目标方法，以及 `CommandParameter` 的行为。

至于命令本身怎么写 —— `ICommand` 接口、`CanExecute`、异步命令和键盘快捷键 —— 请见[命令](/docs/input-interaction/commanding)。

## 用 `ICommand` 绑定 {#binding-with-icommand}

凡是实现了 `ICommandSource` 的控件（例如 `Button`、`MenuItem` 或 `ToggleButton`）都有一个 `Command` 属性，可在视图模型中加以利用。

下面的例子用 `CommunityToolkit.Mvvm` 提供的 `[RelayCommand]` 特性，生成了一个类型为 `IRelayCommand` 的 `SaveCommand` 属性。

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

:::note
命令的命名惯例是在方法名后面加上 “Command”，例如 `SaveCommand`、`UndoCommand`。
:::

## 直接绑定到方法 {#binding-directly-to-a-method}

除了 `ICommand`，你也可以把 `Command` 属性直接绑定到数据上下文中的某个方法。

```xml title="XAML"
<Button Content="Save" Command="{Binding Save}" />
```

```csharp title="Data context"
public void Save()
{
    // Save logic
}
```

### 重载是怎么选中的 {#how-the-overload-is-chosen}

如果你[重载了方法](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/member-overloading)，Avalonia 按以下规则确定具体用哪一个：

| 同名方法的情形 | 结果 |
|---|---|
| 只有一个重载接受一个参数 | 选中它，参数是什么类型都行 |
| 两个及以上的单参数重载，其中一个接受 `object` | 选中接受 `object` 的那个重载 |
| 两个及以上的单参数重载，但没有一个接受 `object` | Error |
| 只有一个无参重载 | Chosen |
| 两个及以上的重载都接受多个参数 | Error |

接受两个及以上参数的重载一律被忽略。

:::caution
编译绑定不会把 `CommandParameter` 转换成参数类型。类型对不上时，命令执行时类型转换会抛异常。反射绑定则会做这层转换。
:::

### 启用状态 {#enabled-state}

采用方法绑定时，若要决定目标控件的启用状态，请添加一个 `bool` 方法，命名格式为 `Can` 加上所绑定的方法名：

```csharp
public void Save()
{
    // Save logic
}

public bool CanSave(object? parameter) => !string.IsNullOrWhiteSpace(Name);
```

:::note
这条约定只适用于方法绑定。使用 `ICommand` 时，控件走的是命令自带的 `CanExecute`。关于 `CanExecute` 的更多内容见[命令](/docs/input-interaction/commanding#icommand-interface)。
:::

## 命令参数 {#command-parameter}

用 `CommandParameter` 把界面上的数据传给命令。本例中，视图模型借助该参数确定要删除哪一项。

```xml title="XAML"
<ListBox ItemsSource="{Binding Items}">
    <ListBox.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal" Spacing="8">
                <TextBlock Text="{Binding Name}" />
                <Button Content="Delete"
                        Command="{Binding $parent[ListBox].DataContext.DeleteCommand}"
                        CommandParameter="{Binding}" />
            </StackPanel>
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

```csharp title="Data context"
[RelayCommand]
private void Delete(Item item)
{
    Items.Remove(item);
}
```

## 跨数据上下文绑定命令 {#binding-commands-from-a-different-data-context}

当命令位于父级视图模型上，而绑定写在模板内部时：

```xml
<!-- Using $parent to reach an ancestor's DataContext -->
<Button Command="{Binding $parent[Window].DataContext.DeleteCommand}"
        CommandParameter="{Binding}" />

<!-- Using a named ancestor -->
<Button Command="{Binding #Root.((vm:MainViewModel)DataContext).DeleteCommand}"
        CommandParameter="{Binding}" />
```

更多说明见 [`DataContext` 类型推断](/docs/data-binding/compiled-bindings#datacontext-type-inference)。

## 另请参阅 {#see-also}

- [命令](/docs/input-interaction/commanding)：怎么写命令 —— `ICommand`、`CanExecute`、异步命令以及手工实现。
- [键盘与快捷键](/docs/input-interaction/keyboard-and-hotkeys)：快捷键与按键绑定的配置。
- [如何绑定 CanExecute](/docs/data-binding/how-to-bind-can-execute)：用 `CanExecute` 控制按钮可用状态的完整示例。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定路径、模式与转换器。
- [调试数据绑定](/docs/data-binding/binding-debugging#method-binding-overload-not-resolved)：排查方法绑定失败的原因。
- [添加交互](/docs/input-interaction/adding-interactivity)：事件和命令之间该怎么选。
