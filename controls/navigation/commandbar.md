---
id: commandbar
title: CommandBar
description: '`CommandBar` 是一个工具栏，用一行命令按钮呈现各项操作。'
doc-type: reference
---

import CommandBarLabelBottomScreenshot from '/img/controls/commandbar/commandbar-label-bottom.png';
import CommandBarLabelRightScreenshot from '/img/controls/commandbar/commandbar-label-right.png';
import CommandBarLabelCollapsedScreenshot from '/img/controls/commandbar/commandbar-label-collapsed.png';
import CommandBarSecondaryCommandsScreenshot from '/img/controls/commandbar/commandbar-secondary-commands.png';
import CommandBarContentScreenshot from '/img/controls/commandbar/commandbar-content.png';
import CommandBarToggleButtonScreenshot from '/img/controls/commandbar/commandbar-toggle-button.png';

[`CommandBar`](/api/avalonia/controls/commandbar) 是一个工具栏式控件，用一行按钮展示主要命令，再用一个溢出菜单收纳次要命令。它常用来把当前情境下最相关的操作摆到台面上，同时让不常用的命令退到「更多」按钮里，需要时仍然够得着。

主要命令直接显示在栏内。空间不够时，命令可以自动挪进溢出区。次要命令则始终待在溢出菜单里。

## ICommandBarElement

放进 `CommandBar` 的条目必须实现 `ICommandBarElement` 接口。Avalonia 提供了三个内置实现：

- **`CommandBarButton`**：一个带图标、文字或两者兼备的按钮。通过继承而来的 `Command` 属性支持命令。
- **`CommandBarToggleButton`**：一个保持选中/未选中状态的切换按钮，适合加粗、倾斜这类可开关的选项。
- **`CommandBarSeparator`**：一条视觉分隔线，用于在栏内或溢出菜单中把相关命令归为一组。

## CommandBar 的属性 {#commandbar-properties}

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `PrimaryCommands` | `IList<ICommandBarElement>` | Empty | 直接显示在栏内的主要命令集合。 |
| `SecondaryCommands` | `IList<ICommandBarElement>` | Empty | 显示在溢出菜单中的次要命令集合。 |
| `Content` | `object?` | `null` | 显示在主要命令之前的自定义内容。 |
| `DefaultLabelPosition` | `CommandBarDefaultLabelPosition` | `Bottom` | 控制栏内所有命令的文字相对图标的位置。 |
| `IsDynamicOverflowEnabled` | `bool` | `false` | 为 `true` 时，若栏宽不足以容纳全部主要命令，它们会自动挪进溢出菜单。 |
| `OverflowButtonVisibility` | `CommandBarOverflowButtonVisibility` | `Auto` | 控制溢出（「更多」）按钮何时可见。 |
| `IsOpen` | `bool` | `false` | 溢出菜单当前是否处于打开状态。 |
| `IsSticky` | `bool` | `false` | 为 `true` 时，溢出菜单会一直开着，直到用户显式关闭，而不会因点击外部而关闭。 |
| `ItemWidthBottom` | `double` | `70` | 当 `DefaultLabelPosition` 为 `Bottom` 时，动态溢出计算所用的预估条目宽度。 |
| `ItemWidthRight` | `double` | `102` | 当 `DefaultLabelPosition` 为 `Right` 时，动态溢出计算所用的预估条目宽度。 |
| `ItemWidthCollapsed` | `double` | `42` | 当 `DefaultLabelPosition` 为 `Collapsed` 时，动态溢出计算所用的预估条目宽度。 |
| `HasSecondaryCommands` | `bool` | Read-only | 指示溢出菜单当前是否有内容，包括次要命令以及被挪进溢出区的主要命令。 |
| `IsOverflowButtonVisible` | `bool` | Read-only | 根据 `OverflowButtonVisibility` 和现有命令，指示溢出按钮当前是否可见。 |
| `VisiblePrimaryCommands` | `ReadOnlyObservableCollection<ICommandBarElement>` | Read-only | 当前仍显示在栏内（未被挪进溢出区）的那部分主要命令。 |
| `OverflowItems` | `ReadOnlyObservableCollection<ICommandBarElement>` | Read-only | 溢出菜单中显示的全部内容：被挪进溢出区的主要命令，加上次要命令。 |

## CommandBar 的事件 {#commandbar-events}

| 事件 | 说明 |
| --- | --- |
| `Opened` | 溢出菜单打开时引发。 |
| `Closed` | 溢出菜单关闭时引发。 |
| `Opening` | 溢出菜单即将打开时引发。 |
| `Closing` | 溢出菜单即将关闭时引发。 |

## DefaultLabelPosition 的取值 {#defaultlabelposition-values}

| 值 | 说明 |
| --- | --- |
| `Bottom` | 文字显示在图标下方，这是默认值。 |
| `Right` | 文字显示在图标右侧。 |
| `Collapsed` | 隐藏文字，只显示图标。 |

## OverflowButtonVisibility 的取值 {#overflowbuttonvisibility-values}

| 值 | 说明 |
| --- | --- |
| `Auto` | 当存在次要命令、或有主要命令被挪进溢出区时，自动显示溢出按钮。 |
| `Visible` | 始终显示溢出按钮。 |
| `Collapsed` | 始终隐藏溢出按钮。 |

## CommandBarButton 的属性 {#commandbarbutton-properties}

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Icon` | `object?` | `null` | 按钮上显示的图标，通常是 `PathIcon`、`SymbolIcon` 或 `BitmapIcon`。 |
| `Label` | `string?` | `null` | 按钮的文字。 |
| `Command` | `ICommand?` | `null` | 按钮被点击时要调用的命令。 |
| `CommandParameter` | `object?` | `null` | 传给命令的参数。 |
| `IsCompact` | `bool` | `false` | 隐藏文字，并采用紧凑的按钮外观。 |
| `IsInOverflow` | `bool` | `false` | 指示该按钮当前是否显示在溢出菜单中，由 `CommandBar` 自动设置。 |
| `LabelPosition` | `CommandBarDefaultLabelPosition` | `Bottom` | 由父级 `CommandBar` 施加的文字位置。 |
| `DynamicOverflowOrder` | `int` | `0` | 控制空间紧张时哪些主要命令能在栏内多留一会儿。数值越小优先级越高，越晚被挪进溢出区。 |

## CommandBarToggleButton 的属性 {#commandbartogglebutton-properties}

| 属性 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `Icon` | `object?` | `null` | 切换按钮上显示的图标。 |
| `Label` | `string?` | `null` | 切换按钮的文字。 |
| `IsChecked` | `bool?` | `false` | 切换按钮当前是否处于选中状态。 |
| `Command` | `ICommand?` | `null` | 切换按钮被点击时要调用的命令。 |
| `CommandParameter` | `object?` | `null` | 传给命令的参数。 |
| `IsCompact` | `bool` | `false` | 隐藏文字，并采用紧凑的按钮外观。 |
| `IsInOverflow` | `bool` | `false` | 指示该切换按钮当前是否显示在溢出菜单中，由 `CommandBar` 自动设置。 |
| `LabelPosition` | `CommandBarDefaultLabelPosition` | `Bottom` | 由父级 `CommandBar` 施加的文字位置。 |
| `DynamicOverflowOrder` | `int` | `0` | 控制空间紧张时哪些主要命令能在栏内多留一会儿。数值越小优先级越高，越晚被挪进溢出区。 |

## CommandBarSeparator

`CommandBarSeparator` 在主要命令区画一条竖线、或在溢出菜单中画一条横线，把相关命令在视觉上归为一组。

## 示例 {#examples}

### Basic CommandBar

一个由图标按钮组成的简单命令栏：

```xml
<CommandBar>
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Add">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource AddIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Edit">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource EditIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Delete">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource DeleteIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
</CommandBar>
```

### 主要命令、次要命令与分隔线 {#primary-and-secondary-commands-with-separators}

用 `CommandBarSeparator` 把命令分组，并把不常用的操作放进 `SecondaryCommands`：

```xml
<CommandBar>
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Cut">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource CutIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Copy">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource CopyIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Paste">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource PasteIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarSeparator />
        <CommandBarButton Label="Undo">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource UndoIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Redo">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource RedoIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
    <CommandBar.SecondaryCommands>
        <CommandBarButton Label="Select All" />
        <CommandBarButton Label="Find and Replace" />
        <CommandBarSeparator />
        <CommandBarButton Label="Settings" />
    </CommandBar.SecondaryCommands>
</CommandBar>
```

<Image light={CommandBarSecondaryCommandsScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="CommandBar with secondary commands in the overflow menu"/>

### 自定义内容区 {#custom-content-area}

`Content` 属性让你在主要命令之前放置自定义内容：

```xml
<CommandBar>
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Back">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource BackIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Forward">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource ForwardIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
    <CommandBar.Content>
        <TextBox Watermark="Search..." Width="200" Margin="8,0" />
    </CommandBar.Content>
</CommandBar>
```

<Image light={CommandBarContentScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="CommandBar with custom content area"/>

### 文字位置 {#label-positions}

用 `DefaultLabelPosition` 属性控制文字相对图标的位置。

### 下方（默认） {#bottom-default}

```xml
<CommandBar DefaultLabelPosition="Bottom">
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Add">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource AddIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Edit">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource EditIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
</CommandBar>
```

<Image light={CommandBarLabelBottomScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="CommandBar with labels below icons"/>

### Right

```xml
<CommandBar DefaultLabelPosition="Right">
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Add">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource AddIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Edit">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource EditIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
</CommandBar>
```

<Image light={CommandBarLabelRightScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="CommandBar with labels to the right of icons"/>

### Collapsed

```xml
<CommandBar DefaultLabelPosition="Collapsed">
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Add">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource AddIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Edit">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource EditIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
</CommandBar>
```

<Image light={CommandBarLabelCollapsedScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="CommandBar with labels hidden"/>

### 动态溢出 {#dynamic-overflow}

当 `IsDynamicOverflowEnabled` 为 `true` 时，放不下的主要命令会自动挪进溢出菜单。用 `DynamicOverflowOrder` 控制哪些命令能在栏内多留一会儿：

```xml
<CommandBar IsDynamicOverflowEnabled="True">
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Low Priority" DynamicOverflowOrder="2">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource StarIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="High Priority" DynamicOverflowOrder="0">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource InfoIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Medium Priority" DynamicOverflowOrder="1">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource EditIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
</CommandBar>
```

本例中「High Priority」的可见优先级最高（order 0），其次是「Medium Priority」（order 1），而「Low Priority」最先被挪进溢出区（order 2）。

### 溢出按钮的可见性 {#overflow-button-visibility}

控制溢出按钮何时出现：

```xml
<!-- Always show the overflow button -->
<CommandBar OverflowButtonVisibility="Visible">
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Save">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource SaveIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
</CommandBar>

<!-- Never show the overflow button -->
<CommandBar OverflowButtonVisibility="Collapsed">
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Save">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource SaveIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
</CommandBar>
```

### 常驻溢出菜单 {#sticky-overflow}

当 `IsSticky` 为 `true` 时，溢出菜单会一直开着，直到用户显式关闭。若预期用户要在溢出菜单里多次选择或多次操作，这很有用：

```xml
<CommandBar IsSticky="True">
    <CommandBar.SecondaryCommands>
        <CommandBarToggleButton Label="Bold">
            <CommandBarToggleButton.Icon>
                <PathIcon Data="{StaticResource BoldIcon}" />
            </CommandBarToggleButton.Icon>
        </CommandBarToggleButton>
        <CommandBarToggleButton Label="Italic">
            <CommandBarToggleButton.Icon>
                <PathIcon Data="{StaticResource ItalicIcon}" />
            </CommandBarToggleButton.Icon>
        </CommandBarToggleButton>
        <CommandBarToggleButton Label="Underline">
            <CommandBarToggleButton.Icon>
                <PathIcon Data="{StaticResource UnderlineIcon}" />
            </CommandBarToggleButton.Icon>
        </CommandBarToggleButton>
    </CommandBar.SecondaryCommands>
</CommandBar>
```

### 用代码控制溢出菜单 {#controlling-overflow-programmatically}

绑定 `IsOpen` 属性即可在代码中打开或关闭溢出菜单：

```xml
<CommandBar IsOpen="{Binding IsOverflowOpen}">
    <CommandBar.SecondaryCommands>
        <CommandBarButton Label="Option A" />
        <CommandBarButton Label="Option B" />
    </CommandBar.SecondaryCommands>
</CommandBar>
```

```csharp
[ObservableProperty]
private bool _isOverflowOpen;

[RelayCommand]
private void ShowOverflow() => IsOverflowOpen = true;
```

### 响应事件 {#responding-to-events}

处理 `Opened` 和 `Closed` 事件，即可在溢出菜单状态变化时作出响应：

```csharp
public partial class MyPage : ContentPage
{
    private void OnCommandBarOpened(object? sender, RoutedEventArgs e)
    {
        // The overflow menu was opened
    }

    private void OnCommandBarClosed(object? sender, RoutedEventArgs e)
    {
        // The overflow menu was closed
    }
}
```

```xml
<CommandBar Opened="OnCommandBarOpened" Closed="OnCommandBarClosed">
    <CommandBar.SecondaryCommands>
        <CommandBarButton Label="Help" />
    </CommandBar.SecondaryCommands>
</CommandBar>
```

### ContentPage 中的 CommandBar {#commandbar-in-contentpage}

用 `ContentPage` 的 `TopCommandBar` 或 `BottomCommandBar` 属性，把 `CommandBar` 挂到页面上：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
            Header="My Page">
    <ContentPage.TopCommandBar>
        <CommandBar>
            <CommandBar.PrimaryCommands>
                <CommandBarButton Label="Refresh">
                    <CommandBarButton.Icon>
                        <PathIcon Data="{StaticResource RefreshIcon}" />
                    </CommandBarButton.Icon>
                </CommandBarButton>
                <CommandBarButton Label="Filter">
                    <CommandBarButton.Icon>
                        <PathIcon Data="{StaticResource FilterIcon}" />
                    </CommandBarButton.Icon>
                </CommandBarButton>
            </CommandBar.PrimaryCommands>
        </CommandBar>
    </ContentPage.TopCommandBar>

    <TextBlock Text="Page content here" Margin="16" />
</ContentPage>
```

### 通过 NavigationPage 附加属性使用 CommandBar {#commandbar-via-navigationpage-attached-property}

用 `NavigationPage.TopCommandBar` 附加属性可以为页面设置 `CommandBar`，这样命令栏会落在导航外壳之内：

```xml
<ContentPage xmlns="https://github.com/avaloniaui"
             Header="Details">
    <NavigationPage.TopCommandBar>
        <CommandBar>
            <CommandBar.PrimaryCommands>
                <CommandBarButton Label="Share">
                    <CommandBarButton.Icon>
                        <PathIcon Data="{StaticResource ShareIcon}" />
                    </CommandBarButton.Icon>
                </CommandBarButton>
                <CommandBarButton Label="Favorite">
                    <CommandBarButton.Icon>
                        <PathIcon Data="{StaticResource HeartIcon}" />
                    </CommandBarButton.Icon>
                </CommandBarButton>
            </CommandBar.PrimaryCommands>
        </CommandBar>
    </NavigationPage.TopCommandBar>

    <TextBlock Text="Detail content" Margin="16" />
</ContentPage>
```

### MVVM 命令绑定 {#mvvm-command-binding}

把 `CommandBarButton` 的各个命令绑定到你的视图模型：

```xml
<CommandBar>
    <CommandBar.PrimaryCommands>
        <CommandBarButton Label="Save"
                          Command="{Binding SaveCommand}">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource SaveIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
        <CommandBarButton Label="Delete"
                          Command="{Binding DeleteCommand}"
                          CommandParameter="{Binding SelectedItem}">
            <CommandBarButton.Icon>
                <PathIcon Data="{StaticResource DeleteIcon}" />
            </CommandBarButton.Icon>
        </CommandBarButton>
    </CommandBar.PrimaryCommands>
</CommandBar>
```

```csharp
[RelayCommand]
private async Task Save()
{
    await _dataService.SaveAsync();
}

[RelayCommand]
private async Task Delete(object item)
{
    await _dataService.DeleteAsync(item);
}
```

### 处理切换按钮的状态 {#toggle-button-state-handling}

用 `CommandBarToggleButton` 做可开关的选项，绑定 `IsChecked` 属性来跟踪状态：

<Image light={CommandBarToggleButtonScreenshot} position="center" maxWidth={400} cornerRadius="true" alt="CommandBar with toggle buttons"/>

```xml title="XAML"
<CommandBar>
    <CommandBar.PrimaryCommands>
        <CommandBarToggleButton Label="Bold"
                                IsChecked="{Binding IsBold}">
            <CommandBarToggleButton.Icon>
                <PathIcon Data="{StaticResource BoldIcon}" />
            </CommandBarToggleButton.Icon>
        </CommandBarToggleButton>
        <CommandBarToggleButton Label="Italic"
                                IsChecked="{Binding IsItalic}">
            <CommandBarToggleButton.Icon>
                <PathIcon Data="{StaticResource ItalicIcon}" />
            </CommandBarToggleButton.Icon>
        </CommandBarToggleButton>
        <CommandBarToggleButton Label="Underline"
                                IsChecked="{Binding IsUnderline}">
            <CommandBarToggleButton.Icon>
                <PathIcon Data="{StaticResource UnderlineIcon}" />
            </CommandBarToggleButton.Icon>
        </CommandBarToggleButton>
    </CommandBar.PrimaryCommands>
</CommandBar>
```

```csharp title="C#"
[ObservableProperty]
private bool _isBold;

[ObservableProperty]
private bool _isItalic;

[ObservableProperty]
private bool _isUnderline;
```

## 另请参阅 {#see-also}

- [ContentPage](/controls/navigation/contentpage)
- [NavigationPage](/controls/navigation/navigationpage)
- [CommandBar API 参考](/api/avalonia/controls/commandbar)
- [GitHub 上的 `CommandBar.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/CommandBar/CommandBar.cs)
