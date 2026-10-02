---
id: trayicon
title: TrayIcon
description: 一个系统托盘图标控件，在操作系统通知区域显示图标和原生上下文菜单。
doc-type: reference
---

import TrayIconScreenshot from '/img/controls/trayicon/trayicon.gif';

[`TrayIcon`](/api/avalonia/controls/trayicon) 控件让你的 Avalonia 应用在系统托盘（通知区域）中显示图标和原生菜单。它支持 Windows、macOS，以及部分 Linux 发行版（已确认在 Ubuntu 上可用）。

托盘图标在 `App.axaml` 文件中定义：在 `Application` 元素上使用 `TrayIcon.Icons` 附加属性。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Icon` | `WindowIcon` | 在系统托盘中显示的图标，通常从应用资产中加载。 |
| `ToolTipText` | `string` | 鼠标悬停在托盘图标上时显示的提示文字。 |
| `IsVisible` | `bool` | 控制托盘图标是否显示，默认值为 `true`。 |
| `Command` | `ICommand` | 用户点击托盘图标时执行的命令。 |
| `CommandParameter` | `object` | 传给 `Command` 的参数。 |
| `Menu` | `NativeMenu` | 挂在托盘图标上的原生菜单控件。 |

:::info
托盘图标必须搭配 `NativeMenu` 使用，而不是 Avalonia 的 `Menu` 控件。原生菜单的完整说明请参阅 [NativeMenu](/controls/menus/nativemenu) 参考。
:::

## Example

下面的例子在 `App.axaml` 文件中定义了一个带嵌套菜单的简单托盘图标：

```xml title="App.axaml"
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApplication.App">
  <TrayIcon.Icons>
    <TrayIcons>
      <TrayIcon Icon="/Assets/avalonia-logo.ico"
                ToolTipText="Avalonia Tray Icon ToolTip">
        <TrayIcon.Menu>
          <NativeMenu>
            <NativeMenuItem Header="Settings">
              <NativeMenu>
                <NativeMenuItem Header="Option 1" />
                <NativeMenuItem Header="Option 2" />
                <NativeMenuItemSeparator />
                <NativeMenuItem Header="Option 3" />
              </NativeMenu>
            </NativeMenuItem>
          </NativeMenu>
        </TrayIcon.Menu>
      </TrayIcon>
    </TrayIcons>
  </TrayIcon.Icons>
</Application>
```

把 `.ico` 文件作为 `AvaloniaResource` 加入你的 `.csproj` 文件：

```xml title="MyApplication.csproj"
<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <AvaloniaResource Include="Assets/avalonia-logo.ico" />
  </ItemGroup>
</Project>
```

<Image light={TrayIconScreenshot} alt="TrayIcon with a context menu shown in the system tray" position="center" maxWidth={400} cornerRadius="true"/>

## 绑定菜单命令 {#binding-menu-commands}

托盘菜单项的命令可以绑定到视图模型。`TrayIcon` 自身的 `Command` 在用户直接点击图标时触发，而每个 `NativeMenuItem` 也可以有自己的 `Command`：

```xml title="App.axaml"
<TrayIcon Icon="/Assets/app-icon.ico"
          ToolTipText="My Application"
          Command="{Binding ShowWindowCommand}">
    <TrayIcon.Menu>
        <NativeMenu>
            <NativeMenuItem Header="Show" Command="{Binding ShowWindowCommand}" />
            <NativeMenuItem Header="Settings" Command="{Binding OpenSettingsCommand}" />
            <NativeMenuItemSeparator />
            <NativeMenuItem Header="Quit" Command="{Binding QuitCommand}" />
        </NativeMenu>
    </TrayIcon.Menu>
</TrayIcon>
```

:::tip
若要把命令绑定到视图模型，请在 `Application` 对象上设置 `DataContext`，或使用带 `x:DataType` 的编译绑定，这样托盘图标才能解析绑定路径。
:::

## 显示与隐藏托盘图标 {#showing-and-hiding-the-tray-icon}

绑定 `IsVisible` 属性即可在运行时切换托盘图标的可见性。应用最小化到托盘时，这很有用：

```xml title="App.axaml"
<TrayIcon Icon="/Assets/app-icon.ico"
          IsVisible="{Binding IsMinimizedToTray}"
          ToolTipText="My Application" />
```

## 实用提示 {#practical-notes}

- `TrayIcon` 定义在 `Application` 这一级，而不是某个 `Window` 内部。无论哪些窗口处于打开状态，它都一直在。
- 在 macOS 上，点击托盘图标会弹出菜单；在 Windows 上，右键弹出菜单，左键触发 `Command`。
- 如果应用需要不止一个托盘图标，可以在同一个 `TrayIcons` 集合里定义多个 `TrayIcon` 元素。
- 如果托盘图标在 Linux 上没出现，请确认你的桌面环境支持 `StatusNotifierItem` 或 `AppIndicator`。GNOME 用户可能需要安装 AppIndicator 扩展。

## 平台支持 {#platform-support}

| 平台 | 支持情况 |
|---|---|
| Windows | 完整支持 |
| macOS | 完整支持 |
| Linux | 在支持 `StatusNotifierItem` 或 `AppIndicator` 的发行版上可用（已在 Ubuntu 上确认） |

## 另请参阅 {#see-also}

- [NativeMenu](/controls/menus/nativemenu)
- [Window](/controls/primitives/window)
- [`TrayIcon` 源码（GitHub）](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/TrayIcon.cs)
