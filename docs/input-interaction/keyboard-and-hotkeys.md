---
id: keyboard-and-hotkeys
title: 键盘与快捷键
description: 学会在 Avalonia 中用 HotKey 属性、KeyBindings、KeyGesture 和 HotKeyManager 定义快捷键与按键绑定，做出键盘驱动的命令。
doc-type: reference
---

实现了 `ICommandSource` 的控件都有一个 `HotKey` 属性，你可以给它赋值或绑定。用户按下快捷键时，Avalonia 就会执行[绑定](/docs/input-interaction/adding-interactivity)到该控件的命令。

```xml title="XAML"
<Menu>
    <MenuItem Header="_File">
        <MenuItem x:Name="SaveMenuItem"
                  Header="_Save"
                  Command="{Binding SaveCommand}"
                  HotKey="Ctrl+S"/>
    </MenuItem>
</Menu>
```

你也可以用 `HotKeyManager` 类的静态方法在代码中设置和读取快捷键：

```csharp title="C#"
InitializeComponent();
HotKeyManager.SetHotKey(saveMenuItem, new KeyGesture(Key.S, KeyModifiers.Control));
```

## 按键与修饰键 {#keys-and-modifiers}

一个快捷键必须有一个 [`Key`](/api/avalonia/input/key)，外加零个或多个 [`KeyModifiers`](/api/avalonia/input/keymodifiers)。当你在 XAML 中用 `HotKey` 属性设置快捷键时，这个字符串会被解析成 [`KeyGesture`](/api/avalonia/input/keygesture)。Avalonia 用 `Enum.Parse` 来解析按键和修饰键，但你也可以用常见的同义写法，比如用 `Ctrl` 代替 `Control`，或者用 `Win` 代替 `Meta`。

### 手势字符串的格式 {#gesture-string-format}

手势字符串由零个或多个修饰键加上一个按键名组成，彼此用 `+` 分隔。例如：

| 手势字符串 | 含义 |
|---|---|
| `Ctrl+S` | Control（macOS 上是 Cmd）+ S |
| `Ctrl+Shift+N` | Control + Shift + N |
| `F5` | 不带修饰键的 F5 |
| `Alt+Enter` | Alt（macOS 上是 Option）+ Enter |

## 把数字键设为快捷键 {#assigning-number-keys-to-hotkeys}

要绑定数字键时，主键盘那一排用 `D0` 到 `D9`，小键盘则用 `NumPad0` 到 `NumPad9`。全部可用取值请参阅完整的 [`Key`](/api/avalonia/input/key) 枚举。

把同一个命令绑到两个控件上、再把其中一个藏起来，就能区分小键盘和主键盘：

```xml title="XAML"
<!-- Ctrl+1 on the main keyboard -->
<Button
    Command="{Binding CommandX}"
    Content="[1]"
    HotKey="Ctrl+D1" />

<!-- NumPad1 (hidden, so only the hotkey is active) -->
<Button
    Command="{Binding CommandX}"
    HotKey="NumPad1"
    IsVisible="False" />
```

:::note
`Content="_1"` 这类访问键语法并不会注册快捷键。请改用 `HotKey` 属性或 [`KeyBinding`](/api/avalonia/input/keybinding)。
:::

## KeyBindings

`KeyBinding` 让你能在控件或窗口层面定义触发命令的键盘快捷键，而不必依附于某个具体的界面元素。当你想要不绑定在特定按钮或菜单项上的全局快捷键时，这很有用。

```xml title="XAML"
<Window.KeyBindings>
    <KeyBinding Gesture="Ctrl+N" Command="{Binding NewCommand}" />
    <KeyBinding Gesture="Ctrl+O" Command="{Binding OpenCommand}" />
    <KeyBinding Gesture="Ctrl+S" Command="{Binding SaveCommand}" />
    <KeyBinding Gesture="Ctrl+Shift+S" Command="{Binding SaveAsCommand}" />
    <KeyBinding Gesture="Delete" Command="{Binding DeleteCommand}" />
</Window.KeyBindings>
```

你也可以在任意控件上定义 `KeyBindings`，把快捷键的作用范围限定在该控件及其子元素内：

```xml title="XAML"
<ListBox KeyboardNavigation.TabNavigation="Continue">
    <ListBox.KeyBindings>
        <KeyBinding Gesture="Delete" Command="{Binding DeleteSelectedCommand}" />
        <KeyBinding Gesture="F2" Command="{Binding RenameCommand}" />
    </ListBox.KeyBindings>
</ListBox>
```

### 传递参数 {#passing-parameters}

用 `KeyBinding` 上的 `CommandParameter` 属性把数据传给命令处理程序：

```xml title="XAML"
<Window.KeyBindings>
    <KeyBinding Gesture="Ctrl+1" Command="{Binding SwitchTabCommand}" CommandParameter="0" />
    <KeyBinding Gesture="Ctrl+2" Command="{Binding SwitchTabCommand}" CommandParameter="1" />
</Window.KeyBindings>
```

## 常用修饰键 {#common-modifier-keys}

| 修饰键 | Windows / Linux | macOS |
|---|---|---|
| `Ctrl` | Ctrl | Cmd |
| `Alt` | Alt | Option |
| `Shift` | Shift | Shift |
| `Meta` | Windows 键 | Cmd |

:::tip
在 macOS 上，`KeyGesture` 中的 `Ctrl` 会自动映射到 Cmd 键。也就是说 `Ctrl+S` 在 macOS 上就是 Cmd+S，无需额外配置。
:::

## 常见的快捷键套路 {#common-hotkey-patterns}

下面的例子给出了典型的撤销、重做和查找快捷键：

```xml title="XAML"
<Window.KeyBindings>
    <!-- Undo/Redo -->
    <KeyBinding Gesture="Ctrl+Z" Command="{Binding UndoCommand}" />
    <KeyBinding Gesture="Ctrl+Y" Command="{Binding RedoCommand}" />

    <!-- Find -->
    <KeyBinding Gesture="Ctrl+F" Command="{Binding FindCommand}" />
</Window.KeyBindings>
```

## 参考 {#reference}

* [`HotKeyManager`](/api/avalonia/controls/hotkeymanager)
* [`KeyGesture`](/api/avalonia/input/keygesture)
* [`KeyModifiers`](/api/avalonia/input/keymodifiers)
* [`Key`](/api/avalonia/input/key)

## 源码 {#source-code}

* [HotkeyManager.cs](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/HotkeyManager.cs)
* [KeyGesture.cs](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Input/KeyGesture.cs)

## 另请参阅 {#see-also}

- [焦点](/docs/input-interaction/focus)：焦点管理与键盘导航。
- [命令](/docs/input-interaction/commanding)：`ICommand` 接口与命令绑定。
- [加入交互](/docs/input-interaction/adding-interactivity)：事件与命令概览。
- [鼠标与键盘快捷键](/docs/input-interaction/mouse-and-keyboard-shortcuts)：更多键盘和鼠标手势的处理方式。
