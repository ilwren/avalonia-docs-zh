---
id: menu-how-to
title: "操作指南：使用菜单"
description: 学会使用 Avalonia 的 Menu、ContextMenu 和 NativeMenu 控件，内容涵盖命令、键盘快捷键、动态菜单项、可勾选菜单项、子菜单以及右键上下文菜单。
doc-type: how-to
---

本指南介绍 Avalonia 中 [`Menu`](/controls/menus/menu) 和 [`ContextMenu`](/controls/menus/contextmenu) 的常见用法，比如命令、键盘快捷键、动态菜单、可勾选项、子菜单以及右键上下文菜单。

## 基本菜单栏 {#basic-menu-bar}

要做一条传统的菜单栏，请把 `Menu` 放进停靠在窗口顶部的 `DockPanel` 里。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:BasicMenuBar">
  <UserControl.DataContext>
    <vm:MainViewModel />
  </UserControl.DataContext>

  <DockPanel>

    <Menu DockPanel.Dock="Top">
      <MenuItem Header="_File">
        <MenuItem Header="_New" Command="{Binding NewCommand}" />
        <MenuItem Header="_Open..." Command="{Binding OpenCommand}" />
        <MenuItem Header="_Save" Command="{Binding SaveCommand}" />
        <Separator />
        <MenuItem Header="E_xit" Command="{Binding ExitCommand}" />
      </MenuItem>
      <MenuItem Header="_Edit">
        <MenuItem Header="_Undo" Command="{Binding UndoCommand}" />
        <Separator />
        <MenuItem Header="Cu_t" Command="{Binding CutCommand}" />
        <MenuItem Header="_Copy" Command="{Binding CopyCommand}" />
        <MenuItem Header="_Paste" Command="{Binding PasteCommand}" />
      </MenuItem>
    </Menu>

    <ContentControl>
      <TextBlock Text="Main window content goes here" Padding="20" Background="Gray" />
    </ContentControl>

  </DockPanel>
</UserControl>
```

```csharp
using System;
using System.Windows.Input;

namespace BasicMenuBar;

public class MainViewModel
{
    // Replace each empty lambda with your command logic.
    public ICommand NewCommand { get; } = new RelayCommand(() => { });
    public ICommand OpenCommand { get; } = new RelayCommand(() => { });
    public ICommand SaveCommand { get; } = new RelayCommand(() => { });
    public ICommand ExitCommand { get; } = new RelayCommand(() => { });
    public ICommand UndoCommand { get; } = new RelayCommand(() => { });
    public ICommand CutCommand { get; } = new RelayCommand(() => { });
    public ICommand CopyCommand { get; } = new RelayCommand(() => { });
    public ICommand PasteCommand { get; } = new RelayCommand(() => { });
}

// A minimal ICommand for the purposes of this preview. 
// You can use CommunityToolkit.Mvvm in a real app.
public class RelayCommand : ICommand
{
    private readonly Action _execute;

    public RelayCommand(Action execute) => _execute = execute;

    public event EventHandler? CanExecuteChanged { add { } remove { } }

    public bool CanExecute(object? parameter) => true;

    public void Execute(object? parameter) => _execute();
}
```

</XamlPreview>
<br />

:::tip 小贴士
- 为了能在浏览器里预览，本示例自己定义了一个 `RelayCommand` 类。在你自己的应用里，可以改用 CommunityToolkit.Mvvm](/docs/input-interaction/commanding) 中的 [`RelayCommand` 特性。
- 字母前面的下划线用来定义快捷键（<kbd>Alt</kbd>+<kbd>按键</kbd>）。例如写成 `_File`，用户按 <kbd>Alt</kbd>+<kbd>F</kbd> 就能打开「文件」菜单。
- 在 `MenuItem` 条目之间插入 `Separator`，可以加一道分隔线，把相关的操作归拢到一起。
:::

## 带键盘快捷键的菜单 {#menu-with-keyboard-shortcuts}

### 显示快捷键提示文字 {#displaying-shortcut-hint-text}

用 `InputGesture` 可以在菜单项旁边显示快捷键提示。

注意 `InputGesture` 只负责显示文字。要让快捷键真正起作用，你还得另外注册那个调用命令的按键绑定。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:KeyboardShortcutsMenuBar">
  <UserControl.DataContext>
    <vm:MainViewModel />
  </UserControl.DataContext>

  <DockPanel>

    <Menu DockPanel.Dock="Top">
      <MenuItem Header="_Edit">
        <MenuItem Header="Cu_t" Command="{Binding CutCommand}"
                  InputGesture="Ctrl+X" />
        <MenuItem Header="_Copy" Command="{Binding CopyCommand}"
                  InputGesture="Ctrl+C" />
        <MenuItem Header="_Paste" Command="{Binding PasteCommand}"
                  InputGesture="Ctrl+V" />
      </MenuItem>
    </Menu>

    <ContentControl>
      <TextBlock Text="Main window content goes here" Padding="20" Background="Gray" />
    </ContentControl>

  </DockPanel>
</UserControl>
```

```csharp
using System;
using System.Windows.Input;

namespace KeyboardShortcutsMenuBar;

public class MainViewModel
{
    public ICommand CutCommand { get; } = new RelayCommand(() => { });
    public ICommand CopyCommand { get; } = new RelayCommand(() => { });
    public ICommand PasteCommand { get; } = new RelayCommand(() => { });
}

// A minimal ICommand for the purposes of this preview. 
// You can use CommunityToolkit.Mvvm in a real app.
public class RelayCommand : ICommand
{
    private readonly Action _execute;

    public RelayCommand(Action execute) => _execute = execute;

    public event EventHandler? CanExecuteChanged { add { } remove { } }

    public bool CanExecute(object? parameter) => true;

    public void Execute(object? parameter) => _execute();
}
```

</XamlPreview>

### 创建按键绑定 {#creating-the-key-binding}

为了让快捷键在菜单关闭时也照样管用，请把 `KeyBinding` 注册到窗口或父控件上。

```xml
<Window.KeyBindings>
    <KeyBinding Gesture="Ctrl+S" Command="{Binding SaveCommand}" />
    <KeyBinding Gesture="Ctrl+Shift+S" Command="{Binding SaveAsCommand}" />
</Window.KeyBindings>
```

:::warning
若你设了 `InputGesture` 却没有配套的 `KeyBinding`，菜单里会显示快捷键文字，但按下组合键什么也不会发生。
:::

### 随平台而变的快捷键 {#platform-aware-shortcuts}

你可以让按键绑定随目标平台而变，比如在 macOS 上用 <kbd>Cmd</kbd> 代替 <kbd>Ctrl</kbd>。办法是为各平台分别定义按键绑定，或者使用 Avalonia 的 `KeyModifiers.Meta`。

```csharp
var gesture = RuntimeInformation.IsOSPlatform(OSPlatform.OSX)
    ? new KeyGesture(Key.S, KeyModifiers.Meta)
    : new KeyGesture(Key.S, KeyModifiers.Control);
```

## 带图标的菜单 {#menu-with-icons}

用 `MenuItem.Icon` 属性为菜单项添加图标。矢量图标可以用 `PathIcon`：

```xml
<MenuItem Header="Copy">
    <MenuItem.Icon>
        <PathIcon Data="{StaticResource copy_icon}" />
    </MenuItem.Icon>
</MenuItem>
```

位图图标则用 `Image`：

```xml
<MenuItem Header="Copy">
    <MenuItem.Icon>
        <Image Source="/Assets/copy.png" Width="16" Height="16" />
    </MenuItem.Icon>
</MenuItem>
```

:::tip
`PathIcon` 在任何 DPI 下都能干净地缩放，大多数图标都推荐这么做。只有矢量路径画不出来的复杂图稿才需要动用 `Image`。
:::

## 可切换的菜单项 {#toggle-menu-items}

对于文本格式、自动换行这类可开可关的菜单项，你可以用一个复选框来表示它当前是否处于开启状态。做法是把 `CheckBox` 放进 `MenuItem.Icon` 里。

<Tabs>

<TabItem value="xaml" label="MainWindow.axaml">

```xml
<MenuItem Header="Word Wrap"
          Command="{Binding ToggleWordWrapCommand}">
    <MenuItem.Icon>
        <CheckBox IsChecked="{Binding IsWordWrapEnabled}"
                  BorderThickness="0"
                  Background="Transparent"
                  Content="" />
    </MenuItem.Icon>
</MenuItem>
```

</TabItem>

<TabItem value="csharp" label="MainViewModel.cs">

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace ToggleMenuItems.ViewModels;

public partial class MainViewModel : ViewModelBase
{
    [RelayCommand]
    private void ToggleWordWrap()
    {
        IsWordWrapEnabled = !IsWordWrapEnabled;
    }
    
    [ObservableProperty]
    private bool _isWordWrapEnabled;
}
```

</TabItem>

</Tabs>

另一种做法是把 `PathIcon` 绑定到同一个 `IsWordWrapEnabled` 属性，用图标来指示开关是否开启。 

```xml
<MenuItem Header="Word Wrap"
          Command="{Binding ToggleWordWrapCommand}">
    <MenuItem.Icon>
        <PathIcon Data="{StaticResource checkmark}"
                  IsVisible="{Binding IsWordWrapEnabled}" />
    </MenuItem.Icon>
</MenuItem>
```

:::tip
若你的菜单项要表现得像单选按钮——三个以上的选项中只有一个处于激活状态——请在视图模型里管理这个状态，选中一项时把其余的取消掉。
:::

## Submenus

嵌套 `MenuItem` 元素即可做出子菜单。Avalonia 会显示一个浮出箭头，鼠标悬停时展开子弹出层。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:SubmenuSample">
  <UserControl.DataContext>
    <vm:MainViewModel />
  </UserControl.DataContext>

  <DockPanel>

    <Menu DockPanel.Dock="Top">
      <MenuItem Header="View">
        <MenuItem Header="Zoom">
          <MenuItem Header="Zoom In" Command="{Binding ZoomInCommand}" />
          <MenuItem Header="Zoom Out" Command="{Binding ZoomOutCommand}" />
          <MenuItem Header="Reset Zoom" Command="{Binding ResetZoomCommand}" />
        </MenuItem>
      <MenuItem Header="Panels">
        <MenuItem Header="Explorer" Command="{Binding ToggleExplorerCommand}" />
        <MenuItem Header="Output" Command="{Binding ToggleOutputCommand}" />
    </MenuItem>
</MenuItem>
    </Menu>

    <ContentControl>
      <TextBlock Text="Main window content goes here" Padding="20" Background="Gray" />
    </ContentControl>

  </DockPanel>
</UserControl>
```

```csharp
using System;
using System.Windows.Input;

namespace SubmenuSample;

public class MainViewModel
{
    // Replace each empty lambda with your command logic.
    public ICommand ZoomInCommand { get; } = new RelayCommand(() => { });
    public ICommand ZoomOutCommand { get; } = new RelayCommand(() => { });
    public ICommand ResetZoomCommand { get; } = new RelayCommand(() => { });
    public ICommand ToggleExplorerCommand { get; } = new RelayCommand(() => { });
    public ICommand ToggleOutputCommand { get; } = new RelayCommand(() => { });
}

// A minimal ICommand for the purposes of this preview. 
// You can use CommunityToolkit.Mvvm in a real app.
public class RelayCommand : ICommand
{
    private readonly Action _execute;

    public RelayCommand(Action execute) => _execute = execute;

    public event EventHandler? CanExecuteChanged { add { } remove { } }

    public bool CanExecute(object? parameter) => true;

    public void Execute(object? parameter) => _execute();
}
```

</XamlPreview>

## 由集合生成的动态菜单 {#dynamic-menus-from-a-collection}

绑定 `ItemsSource` 即可由数据集合生成菜单项。最近文件、窗口列表、插件操作等动态功能都可以这么做。

下面这个例子生成了一份最近文件列表：先用一个独立的 `Models/RecentFile.cs` 类，再在主视图模型里用 `ObservableCollection` 构造出集合，之后就能用 `ItemContainerTheme` 绑定并映射各个属性。

注意 `ItemContainerTheme` 里的 `ControlTheme` 必须把数据类型设成 `RecentFile` 模型。

<Tabs>

<TabItem value="window" label="MainWindow.axaml">

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:vm="using:DynamicMenuSample.ViewModels"
        xmlns:models="using:DynamicMenuSample.Models"
        x:Class="DynamicMenuSample.Views.MainWindow"
        x:DataType="vm:MainViewModel">

  <Menu>
    <MenuItem Header="Recent Files" ItemsSource="{Binding RecentFiles}">
      <MenuItem.ItemContainerTheme>
        <ControlTheme TargetType="MenuItem"
                      BasedOn="{StaticResource {x:Type MenuItem}}"
                      x:DataType="models:RecentFile">
          <Setter Property="Header"
                  Value="{Binding Name}" />
          <Setter Property="Command" 
                  Value="{Binding OpenCommand}" />
          <Setter Property="CommandParameter"
                  Value="{Binding Path}" />
        </ControlTheme>
      </MenuItem.ItemContainerTheme>
    </MenuItem>
  </Menu>

</Window>
```

</TabItem>

<TabItem value="view-model" label="MainViewModel.cs">

```csharp
using System.Collections.ObjectModel;
using DynamicMenuSample.Models;

namespace DynamicMenuSample.ViewModels;

public partial class MainViewModel : ViewModelBase
{
    public ObservableCollection<RecentFile> RecentFiles { get; } = new();
}

```

</TabItem>

<TabItem value="model" label="RecentFile.cs">

```csharp
using System.Windows.Input;

namespace DynamicMenuSample.Models;

public class RecentFile
{
    public string? Name { get; set; }
    public string? Path { get; set; }
    public ICommand? OpenCommand { get; set; }
}

```

</TabItem>

</Tabs>

除了 `ItemContainerTheme`，你也可以改用 `DataTemplates`：

```xml
<MenuItem Header="Recent Files" ItemsSource="{Binding RecentFiles}">
  <MenuItem.DataTemplates>
    <DataTemplate DataType="models:RecentFile">
      <TextBlock Text="{Binding Name}" />
    </DataTemplate>
  </MenuItem.DataTemplates>
</MenuItem>
```

### 显示空状态提示 {#showing-an-empty-state-message}

加一个占位项，在集合为空时显示出来：

```csharp
public IEnumerable<object> RecentFilesOrPlaceholder =>
    RecentFiles.Any()
        ? RecentFiles
        : new object[] { new MenuItem { Header = "(No recent files)", IsEnabled = false } };
```

### 更新动态菜单 {#updating-dynamic-menus}

上例中的 `RecentFiles` 是个 `ObservableCollection`，因此你增删项目时它会自动更新。

若要整个替换集合，请引发 `PropertyChanged` 以便绑定刷新。

## 上下文菜单 {#context-menu}

`ContextMenu` 属性让你能给另一个控件挂上上下文菜单。用户右键单击（或作出等效手势）时菜单就会弹出。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:ContextMenuSample">
  <UserControl.DataContext>
    <vm:MainViewModel />
  </UserControl.DataContext>

  <ListBox ItemsSource="{Binding Items}"
           SelectedItem="{Binding SelectedItem}">

    <!-- Must have an ItemTemplate or the items won't display. -->
    <ListBox.ItemTemplate>
      <DataTemplate DataType="vm:Item">
        <TextBlock Text="{Binding Name}" />
      </DataTemplate>
    </ListBox.ItemTemplate>

    <ListBox.ContextMenu>
      <ContextMenu>
        <MenuItem Header="Edit"
                  Command="{Binding EditCommand}" />
        <MenuItem Header="Delete"
                  Command="{Binding DeleteCommand}" />
        <Separator />
        <MenuItem Header="Properties"
                  Command="{Binding PropertiesCommand}" />
      </ContextMenu>
    </ListBox.ContextMenu>
  </ListBox>

</UserControl>
```

```csharp
using System;
using System.Collections.ObjectModel;
using System.Windows.Input;

namespace ContextMenuSample;

public class MainViewModel
{
    // Replace each empty lambda with your command logic.
    public ICommand EditCommand { get; } = new RelayCommand(() => { });
    public ICommand DeleteCommand { get; } = new RelayCommand(() => { });
    public ICommand PropertiesCommand { get; } = new RelayCommand(() => { });

    // Create the collection that displays in the ListBox.
    public ObservableCollection<Item> Items { get; set; } = new()
    {
        new Item("Item 1"),
        new Item("Item 2"),
        new Item("Item 3"),
    };

    // Define the selected item.
    private Item? _selectedItem;

    public Item? SelectedItem { get; set; }
}

// A basic item to fill out the collection.
public class Item
{
    public string Name { get; set; }

    public Item(string name)
    {
        Name = name;
    }
}

// A minimal ICommand for the purposes of this preview. 
// You can use CommunityToolkit.Mvvm in a real app.
public class RelayCommand : ICommand
{
    private readonly Action _execute;

    public RelayCommand(Action execute) => _execute = execute;

    public event EventHandler? CanExecuteChanged { add { } remove { } }

    public bool CanExecute(object? parameter) => true;

    public void Execute(object? parameter) => _execute();
}
```

</XamlPreview>

### 把被点击的项目传出去 {#passing-the-clicked-item}

用 `CommandParameter` 配合绑定，把相关的项目传给你的命令。

```xml
<ListBox.ContextMenu>
  <ContextMenu>
    <MenuItem Header="Delete"
              Command="{Binding DeleteCommand}"
              CommandParameter="{Binding $parent[ListBox].SelectedItem}" />
  </ContextMenu>
</ListBox.ContextMenu>
```

:::tip
`$parent[ListBox]` 语法会沿视觉树向上找到最近的 `ListBox` 祖先。之所以要这么写，是因为 `ContextMenu` 与它的宿主目标分处视觉树的不同位置。
:::

### 按状态禁用菜单项 {#disabling-items-based-on-state}

若你的命令实现了 `ICommand.CanExecute`，那么当 `CanExecute` 返回 `false` 时 `MenuItem` 会自动被禁用。若用上 `CommunityToolkit.Mvvm` 的源生成器，你还可以借助 `[RelayCommand(CanExecute = ...)]` 特性。

```csharp
[RelayCommand(CanExecute = nameof(CanDelete))]
private void Delete(object item)
{
    // Delete logic
}

private bool CanDelete(object item) => item is not null;
```

### 在代码中创建上下文菜单 {#context-menu-in-code}

你也可以在代码隐藏中创建或修改上下文菜单：

```csharp
var contextMenu = new ContextMenu
{
    ItemsSource = new[]
    {
        new MenuItem { Header = "Cut", Command = CutCommand },
        new MenuItem { Header = "Copy", Command = CopyCommand },
        new MenuItem { Header = "Paste", Command = PasteCommand },
    }
};
myControl.ContextMenu = contextMenu;
```

## 打开与关闭事件 {#opening-and-closing-events}

处理菜单的生命周期事件，即可在运行时调整菜单项，或者按条件阻止菜单弹出：

```xml title="XAML"
<ContextMenu Opening="ContextMenu_Opening"
             Closing="ContextMenu_Closing">
```

```csharp title="C#"
private void ContextMenu_Opening(object? sender, CancelEventArgs e)
{
    // Customize items based on current state.
    // Set e.Cancel = true to prevent the menu from opening.
    if (sender is ContextMenu menu)
    {
        var canPaste = CheckClipboardContent();
        // Enable or disable items dynamically
    }
}

private void ContextMenu_Closing(object? sender, EventArgs e)
{
    // Clean up or log when the menu closes.
}
```

## `ContextFlyout` alternative

当你需要的内容比一列菜单项更丰富时，请改用 `ContextFlyout`。上下文浮出控件里可以放别的控件，定制空间更大。

<XamlPreview>

```xml
<Border xmlns="https://github.com/avaloniaui"
        Background="Gray"
        Padding="20">
  <Border.ContextFlyout>
    <Flyout>
      <StackPanel Spacing="8"
                  Width="200">
        <TextBlock Text="Custom flyout content"
                   FontWeight="Bold" />
        <TextBox PlaceholderText="Enter value..." />
        <Button Content="Apply" />
      </StackPanel>
    </Flyout>
  </Border.ContextFlyout>
  <TextBlock Text="Right-click for flyout" />
</Border>
```

</XamlPreview>
<br />

:::caution
一个控件不能同时拥有 `ContextMenu` 和 `ContextFlyout`。两个都设的话，只有其中一个会生效。
:::

## `NativeMenu` (macOS)

在 macOS 上，请用 [`NativeMenu`](/controls/menus/nativemenu) 接入屏幕顶部的系统菜单栏，获得原生观感。

```xml
<NativeMenu.Menu>
  <NativeMenu>
    <NativeMenuItem Header="About MyApp"
                    Command="{Binding AboutCommand}" />
    <NativeMenuItemSeparator />
    <NativeMenuItem Header="Preferences..."
                    Command="{Binding PreferencesCommand}" />
  </NativeMenu>
</NativeMenu.Menu>
```

:::note
在 macOS 以外的平台上，`NativeMenu` 会被忽略，因此不必加条件编译也能放心写上。Windows 和 Linux 上请改用标准的 [`Menu`](/controls/menus/menu)。
:::

## 另请参阅 {#see-also}

- [快捷键](/docs/input-interaction/keyboard-and-hotkeys)：注册键盘快捷键与按键绑定。
- [命令](/docs/input-interaction/commanding)：在控件上使用命令。
- [把数据绑定到命令](/docs/data-binding/binding-to-commands)：在 MVVM 中绑定命令。
