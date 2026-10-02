---
id: nativemenu
title: NativeMenu
---

`NativeMenu` 可以在 _macOS_ 和部分 Linux 发行版上显示菜单。它可以用在以下几种场合：

- **应用程序菜单** —— 通过 `Application` 上的 `NativeMenu.Menu`（macOS 菜单栏最左边那个菜单）
- **窗口菜单** —— 通过 `Window` 上的 `NativeMenu.Menu`（即「文件」「编辑」这类常规菜单）
- **Dock 菜单** —— 通过 `Application` 上的 `NativeDock.Menu`（右键点击 macOS Dock 图标弹出的菜单）
- **托盘图标菜单** —— 通过 `TrayIcon` 上的 `Menu` 属性

嵌套 `<MenuItem>` 元素即可创建子菜单。

加入 `<NativeMenuItemSeparator>` 元素即可添加菜单分隔线；也可以添加一个 header 设为减号的菜单项，像这样：

```xml
<NativeMenuItemSeparator Header="-" />
```

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table>
  <thead>
    <tr><th width="204">Property</th><th>说明</th></tr>
  </thead>
  <tbody>
    <tr><td><code>Header</code></td><td>菜单文字。</td></tr>
    <tr><td><code>Command</code></td><td>用户点击该菜单项时所执行的命令。</td></tr>
    <tr><td><code>Gesture</code></td><td>与该菜单项关联的键盘快捷键。</td></tr>
    <tr><td><code>ToggleType</code></td><td>切换行为： <code>None</code> (default), <code>CheckBox</code>, or <code>Radio</code>。取值来自 <code>MenuItemToggleType</code> enum.</td></tr>
    <tr><td><code>IsChecked</code></td><td>菜单项是否处于选中状态。仅当 <code>ToggleType</code> is <code>CheckBox</code> or <code>Radio</code>.</td></tr>
  </tbody>
</table>

## Example

本例修改 macOS 下的默认应用程序菜单。

:::info
改变应用的 `Name` 属性会让应用程序菜单的标题随之改变。本例中它被设成了 *Sample Application*。
:::

![image](https://github.com/user-attachments/assets/d30bab47-f133-4f79-9bdb-d4fb4569ed61)

```xml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="NativeMenuTest.App"
             xmlns:local="using:NativeMenuTest"
             RequestedThemeVariant="Default"
             Name="Sample Application">
             <!-- "Default" ThemeVariant follows system theme variant. "Dark" or "Light" are other available options. -->

    <Application.DataTemplates>
        <local:ViewLocator/>
    </Application.DataTemplates>

    <NativeMenu.Menu>
        <NativeMenu>
            <NativeMenuItem Header="About This Application…" Click="AppAbout_OnClick" />
            <NativeMenuItem Header="Preferences…" Click="AppPreferences_OnClick" />
        </NativeMenu>
    </NativeMenu.Menu>
  
    <Application.Styles>
        <FluentTheme />
    </Application.Styles>
</Application>
```

你还需要在代码隐藏中添加相应的事件处理程序。

```csharp
private void AppAbout_OnClick(object? sender, System.EventArgs args) {

}

private void AppPreferences_OnClick(object? sender, System.EventArgs args) {
    
}
```

## Example

本例添加了一个 *File* 菜单和一个 *Edit* 菜单。为了说明 `NativeMenu.Menu` 元素该放在 XAML 的什么位置，这里一并列出了其他 XML 标签，但为求简洁略去了应用正常运行所需的部分特性。

```xml
<Window>
    <Design.DataContext />

    <NativeMenu.Menu>
        <NativeMenu>
            <NativeMenuItem Header="File" IsVisible="true">
                <NativeMenu>                    
                    <NativeMenuItem Header="Open…" Click="FileOpen_OnClick" Gesture="Meta+O" />
                    <NativeMenuItem Header="Save As…" Click="FileSaveAs_OnClick" Gesture="Meta+Shift+S" />
                    <NativeMenuItem Header="Save As…" Click="FileSaveAs_OnClick" Gesture="Meta+A" />
                </NativeMenu>
            </NativeMenuItem>
            <NativeMenuItem Header="Edit" IsEnabled="true">
                <NativeMenu>
                    <NativeMenuItem Header="Cut" Command="{Binding CutCommand}" Gesture="Meta+X" />
                    <NativeMenuItem Header="Copy" Command="{Binding CopyCommand}" Gesture="Meta+C" />
                    <NativeMenuItem Header="Past" Command="{Binding PasteCommand}" Gesture="Meta+V" />
                </NativeMenu>
            </NativeMenuItem>
        </NativeMenu>
    </NativeMenu.Menu>

    <TextBlock Text="{Binding Greeting}" HorizontalAlignment="Center" VerticalAlignment="Center"/>

</Window>
```

然后在视图模型中添加这些命令函数：

```csharp
public void CutCommand() { }

public void CopyCommand() { }

public void PasteCommand() { }
```

### 手势格式 {#gesture-format}

`Gesture` 特性的值是一串以 `+` 分隔的修饰键，后跟一个 `+`，最后是单个按键字符（它本身也可以是 `+`）。允许的修饰键有 `Alt`、`Control`、`Shift` 和 `Meta`。若 `Gesture` 特性为空字符串、或只含单个按键字符，不会抛异常，但该手势也不会激活菜单项；若只给了修饰键而没有按键，或者特性值格式不对，则会抛出 `ArgumentException`。更多细节请参阅 [`KeyGesture`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Input/KeyGesture.cs)、[`Key`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Input/Key.cs) 和 [`KeyModifier`](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Base/Input/IKeyboardDevice.cs) 的源码。

:::info
请注意，如果既没有代码隐藏中的 `Click` 事件处理程序、也没有用 `Command` 特性绑定函数，该菜单项不会处于可用状态。
:::

:::info
另请注意，在 macOS 上，菜单栏一级中 header 为 `Edit` 的 `NativeMenuItem` 会默认带上一些 macOS 自有的功能项。
:::

## Example

本例定义一个可挂到托盘图标上的原生菜单：

```xml
<NativeMenu>
  <NativeMenuItem Header="Settings">
    <NativeMenu>
      <NativeMenuItem Header="Option 1"   />
      <NativeMenuItem Header="Option 2"   />
      <NativeMenuItemSeparator />
      <NativeMenuItem Header="Option 3"  />
    </NativeMenu>
  </NativeMenuItem>
</NativeMenu>
```

## Example

本例定义一个 Dock 菜单，右键点击 macOS Dock 中的应用图标时弹出：

```xml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApp.App">

    <NativeDock.Menu>
        <NativeMenu>
            <NativeMenuItem Header="New Window" Click="NewWindow_OnClick" />
            <NativeMenuItemSeparator />
            <NativeMenuItem Header="Show Main Window" Click="ShowMainWindow_OnClick" />
        </NativeMenu>
    </NativeDock.Menu>
</Application>
```

:::note
`NativeDock.Menu` 只在 macOS 上有效，其他平台会忽略该属性。
:::

## 另请参阅 {#see-also}

- [NativeMenu API 参考](/api/avalonia/controls/nativemenu)
- [GitHub 上的 `NativeMenu.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/NativeMenu.cs)
- [macOS 平台指南](/docs/platform-specific-guides/macos#dock-menu)
