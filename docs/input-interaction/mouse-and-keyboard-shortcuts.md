---
id: mouse-and-keyboard-shortcuts
title: 创建鼠标与键盘快捷键
description: 学会在 Avalonia 控件中用 KeyBindings、手势和上下文菜单绑定键盘快捷键，并处理双击之类的鼠标事件。
doc-type: how-to
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import KeyMouseScreenshot from '/img/guides/ui-development/binding-key-mouse-test.gif';

Avalonia 让你能把键盘快捷键和鼠标动作挂到控件上，这样用户不必去够工具栏或菜单也能完成操作。本页带你走一遍最常见的几种做法：用 `KeyBindings` 把按键绑定到命令、通过 `DoubleTapped` 事件处理双击，以及添加右键上下文菜单。

## 按键绑定 {#key-bindings}

你可以往任意控件的 `KeyBindings` 集合里挂上一个或多个 [`KeyBinding`](/api/avalonia/input/keybinding) 元素。每个 `KeyBinding` 都把一个 `Gesture`（某个按键，可搭配修饰键）映射到视图模型上的某个命令。

```xml
<ListBox.KeyBindings>
    <KeyBinding Command="{Binding PrintItem}" Gesture="Enter" />
    <KeyBinding Command="{Binding DeleteItem}" Gesture="Delete" />
    <KeyBinding Command="{Binding SelectAll}" Gesture="Ctrl+A" />
</ListBox.KeyBindings>
```

`Gesture` 字符串会被解析成 `KeyGesture`。你可以使用 `Ctrl`、`Shift`、`Alt`、`Cmd` 这类修饰键简写。受支持的按键和修饰键完整清单，请参阅[键盘与快捷键](/docs/input-interaction/keyboard-and-hotkeys)参考。

:::tip
只有当控件（或它的某个子元素）持有键盘焦点时，`KeyBinding` 才会触发。若你需要一个不受焦点影响、全应用生效的快捷键，请改用 `MenuItem` 或别的 `ICommandSource` 上的 `HotKey`。
:::

## 处理双击 {#handling-double-click}

Avalonia 没有提供与 `MouseBinding` 等价的东西。要响应双击，请在代码隐藏中处理 `DoubleTapped` 事件，再把动作转交给视图模型：

```csharp
private void ListBox_DoubleTapped(object? sender, Avalonia.Input.TappedEventArgs e)
{
    if (DataContext is MainViewModel vm)
    {
        vm.PrintItem.Execute(null);
    }
}
```

在 XAML 中用 `DoubleTapped` 特性挂上处理程序：

```xml
<ListBox DoubleTapped="ListBox_DoubleTapped"
         ItemsSource="{Binding OperatingSystems}"
         SelectedItem="{Binding OS}" />
```

## 添加上下文菜单 {#adding-a-context-menu}

你可以给任意控件挂上 `ContextMenu`。用户右键单击（在触摸设备上则是长按）时菜单就会出现。把每个 `MenuItem` 绑定到视图模型上的命令：

```xml
<TextBlock Text="{Binding Result}">
    <TextBlock.ContextMenu>
        <ContextMenu>
            <MenuItem Command="{Binding Clear}" Header="Clear" />
        </ContextMenu>
    </TextBlock.ContextMenu>
</TextBlock>
```

## 完整示例 {#complete-example}

下面这个例子把三种做法揉进了同一个视图：用 `ListBox` 列出若干操作系统，按 Enter 或双击某一项会把它打印到 `TextBlock` 中，而右键点击 `TextBlock` 则会清空结果。

<Tabs
  defaultValue="xaml"
  values={[
      { label: 'XAML', value: 'xaml', },
      { label: 'Code-behind', value: 'code-behind', },
      { label: 'ViewModel', value: 'ViewModel', },
  ]}
>
<TabItem value="xaml">

```xml
<UserControl ..>
    <StackPanel>
        <ListBox
            DoubleTapped="ListBox_DoubleTapped"
            ItemsSource="{Binding OperatingSystems}"
            SelectedItem="{Binding OS}">
            <ListBox.KeyBindings>
                <!--  Enter  -->
                <KeyBinding Command="{Binding PrintItem}" Gesture="Enter" />
                <!--
                    MouseBindings are not supported.
                    Instead, handle it in the view's code-behind. (DoubleTapped event)
                -->
            </ListBox.KeyBindings>
        </ListBox>
        <TextBlock Text="{Binding Result}">
            <TextBlock.ContextMenu>
                <ContextMenu>
                    <!--  Right Click  -->
                    <MenuItem Command="{Binding Clear}" Header="Clear" />
                </ContextMenu>
            </TextBlock.ContextMenu>
        </TextBlock>
    </StackPanel>
</UserControl>
```

</TabItem>
<TabItem value="code-behind">

```csharp
public partial class MainView : UserControl
{
    public MainView()
    {
        InitializeComponent();
    }

    private void ListBox_DoubleTapped(object? sender, Avalonia.Input.TappedEventArgs e)
    {
        if (DataContext is MainViewModel vm)
        {
            vm.PrintItem.Execute(null);
        }
    }
}
```
</TabItem>

<TabItem value="ViewModel">

```csharp
public class MainViewModel : ViewModelBase
{
    public List<string> OperatingSystems =>
    [
        "Windows",
        "Linux",
        "Mac",
    ];
    public string OS { get; set; } = string.Empty;

    [Reactive]
    public string Result { get; set; } = string.Empty;

    public ICommand PrintItem { get; }
    public ICommand Clear { get; }

    public MainViewModel()
    {
        PrintItem = ReactiveCommand.Create(() => Result = OS);
        Clear = ReactiveCommand.Create(() => Result = string.Empty);
    }
}
```
</TabItem>
</Tabs>

<Image light={KeyMouseScreenshot} alt="Demo showing keyboard and mouse shortcut interactions with a ListBox" position="center" maxWidth={400} cornerRadius="true"/>

## 各平台须知 {#platform-specific-notes}

| 平台 | 行为 |
|---|---|
| **macOS** | 想要符合平台习惯的快捷键，请用 `Cmd` 而不是 `Ctrl`（比如保存写成 `Cmd+S`）。你也可以把 `Ctrl` 和 `Cmd` 两种写法都绑到同一个命令上，把各平台一网打尽。 |
| **Linux / X11** | 上下文菜单默认在右键单击时弹出。长按呼出上下文菜单的方式用不了，因为 X11 不提供触摸按住事件。 |
| **Mobile (Android / iOS)** | 没有接实体键盘时，`KeyBinding` 不起作用。触摸优先的交互请改用手势识别器和（由长按激活的）`ContextMenu`。 |
| **Browser (WASM)** | 多数按键手势都能用，但某些被浏览器占用的快捷键（比如 `Ctrl+T` 或 `Ctrl+W`）你的应用是拦不住的。 |

## 另请参阅 {#see-also}

- [键盘与快捷键](/docs/input-interaction/keyboard-and-hotkeys)：按键绑定与快捷键配置。
- [命令](/docs/input-interaction/commanding)：`ICommand` 接口与命令绑定。
- [手势](/docs/input-interaction/gestures)：轻点、双击与多指手势识别器。
- [加入交互](/docs/input-interaction/adding-interactivity)：事件与命令概览。
